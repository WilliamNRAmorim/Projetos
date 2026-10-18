import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator, KeyboardAvoidingView, Modal, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { ask, mensagemDoErro, type TipoErroIA } from '@/src/ai';
import { carregarContexto } from '@/src/economista/carregar';
import { contextoParaJson } from '@/src/economista/contexto';
import { lerHistorico, limparHistorico, salvarHistorico, type MensagemChat } from '@/src/economista/historico';
import { PERSONA } from '@/src/economista/persona';
import { responderComGuarda } from '@/src/economista/responder';
import { Botao, Card, cores, espaco, fonte, raio } from '@/src/ui';

const SUGESTOES = [
  'Como está meu mês?',
  'Onde estou gastando mais?',
  'Como começo a investir com R$ 100?',
  'Vale comprar dólar agora?',
  'Monta um plano pra eu juntar 3 meses de reserva',
];
const MAX_API = 10;
const novoId = () => `${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;

export default function Economista() {
  const router = useRouter();
  const topo = useSafeAreaInsets().top;
  const [msgs, setMsgs] = useState<MensagemChat[]>([]);
  const [texto, setTexto] = useState('');
  const [pensando, setPensando] = useState(false);
  const [erro, setErro] = useState<{ tipo: TipoErroIA; texto: string } | null>(null);
  const [verDados, setVerDados] = useState<string | null>(null);
  const lista = useRef<ScrollView>(null);

  useEffect(() => { lerHistorico().then(setMsgs); }, []);

  const rolar = () => setTimeout(() => lista.current?.scrollToEnd({ animated: true }), 50);

  const enviar = useCallback(async (conteudo: string) => {
    const t = conteudo.trim();
    if (!t || pensando) return;
    setErro(null);
    setTexto('');
    const comUser: MensagemChat[] = [...msgs, { id: novoId(), role: 'user', content: t }];
    setMsgs(comUser);
    setPensando(true);
    rolar();
    try {
      let dados: string | undefined;
      try {
        dados = contextoParaJson(await carregarContexto());
      } catch {
        dados = undefined; // sem contexto: a persona manda pedir os dados que faltam
      }
      // Se a guarda disparar, a resposta é descartada e o Gemini é chamado UMA vez de novo com um lembrete;
      // só a segunda aparece (com aviso se ela também disparar). A primeira nunca é mostrada.
      const g = await responderComGuarda(
        (m) => ask(m, { system: PERSONA, data: dados, temperature: 0.4, maxOutputTokens: 3072, thinkingBudget: 1024 }),
        comUser.slice(-MAX_API).map((m) => ({ role: m.role, content: m.content })),
      );
      const final = [...comUser, { id: novoId(), role: 'assistant' as const, content: g.texto, aviso: g.aviso, flags: g.flags }];
      setMsgs(final);
      await salvarHistorico(final);
    } catch (e) {
      setErro(mensagemDoErro(e));
      await salvarHistorico(comUser);
    } finally {
      setPensando(false);
      rolar();
    }
  }, [msgs, pensando]);

  const limpar = async () => {
    await limparHistorico();
    setMsgs([]);
    setErro(null);
  };

  const abrirDados = async () => {
    try {
      setVerDados(contextoParaJson(await carregarContexto(), true));
    } catch {
      setVerDados('Não foi possível montar os dados agora.');
    }
  };

  return (
    <KeyboardAvoidingView style={[s.root, { paddingTop: topo }]} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View style={s.cabecalho}>
        <Text style={s.titulo}>Economista</Text>
        {msgs.length > 0 && (
          <Pressable onPress={limpar} hitSlop={8} style={s.limpar}>
            <Ionicons name="trash-outline" size={16} color={cores.texto2} />
            <Text style={s.limparTxt}>Limpar</Text>
          </Pressable>
        )}
      </View>

      <Pressable onPress={abrirDados}>
        <Card style={s.aviso}>
          <Text style={s.avisoTxt}>Educativo, não é consultoria de investimentos. Os dados enviados ao Gemini são só faixas e percentuais, sem nomes.</Text>
          <Text style={s.avisoLink}>Toque para ver exatamente o que é enviado</Text>
        </Card>
      </Pressable>

      <ScrollView ref={lista} style={s.lista} contentContainerStyle={s.listaConteudo} keyboardShouldPersistTaps="handled">
        {msgs.length === 0 && (
          <View style={s.sugestoes}>
            <Text style={s.vazio}>Pergunte qualquer coisa sobre suas finanças. Algumas ideias:</Text>
            {SUGESTOES.map((q) => (
              <Pressable key={q} onPress={() => enviar(q)} style={s.chip}>
                <Text style={s.chipTxt}>{q}</Text>
              </Pressable>
            ))}
          </View>
        )}
        {msgs.map((m) => (
          <View key={m.id} style={[s.linha, m.role === 'user' ? s.linhaUser : s.linhaIA]}>
            <View style={[s.bolha, m.role === 'user' ? s.bolhaUser : s.bolhaIA]}>
              <Text style={s.bolhaTxt} selectable>{m.content}</Text>
            </View>
            {m.aviso ? (
              <View style={s.guarda}>
                <Ionicons name="warning-outline" size={14} color={cores.alerta} />
                <Text style={s.guardaTxt}>{m.aviso}</Text>
              </View>
            ) : null}
          </View>
        ))}
        {pensando && (
          <View style={[s.bolha, s.bolhaIA, s.pensando]}>
            <ActivityIndicator size="small" color={cores.texto2} />
            <Text style={s.pensandoTxt}>pensando…</Text>
          </View>
        )}
        {erro && (
          <Card borda={cores.perigo} style={s.erro}>
            <Text style={s.erroTxt}>
              {erro.tipo === 'sem_chave' ? 'A chave do Gemini ainda não foi configurada.' : erro.texto}
            </Text>
            {(erro.tipo === 'sem_chave' || erro.tipo === 'chave_invalida') && (
              <Botao texto="Abrir Configurações" icone="settings-outline" aoPressionar={() => router.push('/configuracoes')} />
            )}
          </Card>
        )}
      </ScrollView>

      <View style={s.entrada}>
        <TextInput
          style={s.input}
          value={texto}
          onChangeText={setTexto}
          placeholder="Escreva sua pergunta"
          placeholderTextColor={cores.texto2}
          multiline
          maxLength={1000}
        />
        <Pressable
          onPress={() => enviar(texto)}
          disabled={pensando || !texto.trim()}
          style={[s.enviar, (pensando || !texto.trim()) && s.enviarOff]}
          accessibilityLabel="Enviar"
        >
          <Ionicons name="arrow-up" size={20} color={cores.fundo} />
        </Pressable>
      </View>

      <Modal visible={verDados !== null} animationType="slide" transparent onRequestClose={() => setVerDados(null)}>
        <View style={s.modalFundo}>
          <View style={s.modal}>
            <Text style={s.modalTitulo}>Dados enviados ao Gemini</Text>
            <Text style={s.modalSub}>Só faixas e percentuais (nenhum valor exato de salário, saldo, limite ou fatura). Nenhum nome, CPF, descrição de transação ou chave.</Text>
            <ScrollView style={s.modalCorpo}>
              <Text style={s.json} selectable>{verDados}</Text>
            </ScrollView>
            <Botao texto="Fechar" aoPressionar={() => setVerDados(null)} />
          </View>
        </View>
      </Modal>
    </KeyboardAvoidingView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: cores.fundo },
  cabecalho: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: espaco.lg, paddingTop: espaco.md },
  titulo: { color: cores.texto, fontSize: fonte.numero, fontWeight: '700' },
  limpar: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  limparTxt: { color: cores.texto2, fontSize: fonte.corpo },
  aviso: { marginHorizontal: espaco.lg, marginTop: espaco.md, gap: 2 },
  avisoTxt: { color: cores.texto2, fontSize: fonte.pequena, lineHeight: 17 },
  avisoLink: { color: cores.info, fontSize: fonte.pequena },
  lista: { flex: 1 },
  listaConteudo: { padding: espaco.lg, gap: espaco.md },
  sugestoes: { gap: espaco.sm },
  vazio: { color: cores.texto2, fontSize: fonte.corpo, marginBottom: espaco.xs },
  chip: { backgroundColor: cores.superficie, borderColor: cores.borda, borderWidth: 1, borderRadius: raio.pill, paddingVertical: espaco.sm, paddingHorizontal: espaco.lg, alignSelf: 'flex-start' },
  chipTxt: { color: cores.texto, fontSize: fonte.corpo },
  linha: { gap: 4 },
  linhaUser: { alignItems: 'flex-end' },
  linhaIA: { alignItems: 'flex-start' },
  bolha: { maxWidth: '88%', borderRadius: raio.lg, paddingVertical: espaco.sm + 2, paddingHorizontal: espaco.md },
  bolhaUser: { backgroundColor: cores.primaria },
  bolhaIA: { backgroundColor: cores.superficie, borderColor: cores.borda, borderWidth: 1 },
  bolhaTxt: { color: cores.texto, fontSize: fonte.corpo, lineHeight: 21 },
  guarda: { flexDirection: 'row', gap: 6, maxWidth: '88%', alignItems: 'flex-start' },
  guardaTxt: { color: cores.alerta, fontSize: fonte.pequena, flex: 1, lineHeight: 16 },
  pensando: { flexDirection: 'row', alignItems: 'center', gap: espaco.sm },
  pensandoTxt: { color: cores.texto2, fontSize: fonte.corpo },
  erro: { gap: espaco.sm },
  erroTxt: { color: cores.texto, fontSize: fonte.corpo, lineHeight: 20 },
  entrada: { flexDirection: 'row', alignItems: 'flex-end', gap: espaco.sm, padding: espaco.md, borderTopWidth: 1, borderTopColor: cores.borda },
  input: { flex: 1, maxHeight: 120, color: cores.texto, backgroundColor: cores.superficie, borderRadius: raio.lg, borderWidth: 1, borderColor: cores.borda, paddingHorizontal: espaco.md, paddingVertical: espaco.sm, fontSize: fonte.corpo },
  enviar: { width: 40, height: 40, borderRadius: 20, backgroundColor: cores.primaria, alignItems: 'center', justifyContent: 'center' },
  enviarOff: { opacity: 0.4 },
  modalFundo: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modal: { backgroundColor: cores.superficie, borderTopLeftRadius: raio.lg, borderTopRightRadius: raio.lg, padding: espaco.lg, gap: espaco.sm, maxHeight: '85%' },
  modalTitulo: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700' },
  modalSub: { color: cores.texto2, fontSize: fonte.pequena },
  modalCorpo: { backgroundColor: cores.fundo, borderRadius: raio.md, padding: espaco.md },
  json: { color: cores.texto, fontSize: 11, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace' },
});
