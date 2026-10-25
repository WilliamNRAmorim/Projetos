import { Link } from 'expo-router';
import { Fragment, useEffect, useState } from 'react';
import { Alert, Pressable, Share, StyleSheet, Text, TextInput } from 'react-native';
import { gerarExport } from '@/src/exportarCarregar';
import { Sonda, rodarDiagnostico } from '@/src/mp/diagnostico';
import { Tela } from '@/src/Tela';
import { CHAVES, NomeChave, getSecret, setSecret } from '@/src/secrets';
import { theme } from '@/src/theme';

export default function Configuracoes() {
  const [valores, setValores] = useState<Record<NomeChave, string>>({ mercadopago: '', gemini: '', brapi: '' });
  const [salvas, setSalvas] = useState<Record<NomeChave, boolean>>({ mercadopago: false, gemini: false, brapi: false });

  useEffect(() => {
    (async () => {
      const r = { mercadopago: false, gemini: false, brapi: false };
      for (const c of CHAVES) r[c.nome] = !!(await getSecret(c.nome));
      setSalvas(r);
    })();
  }, []);

  const [diag, setDiag] = useState<Sonda[] | null>(null);
  const [rodando, setRodando] = useState(false);

  async function diagnosticar() {
    setRodando(true);
    try {
      setDiag(await rodarDiagnostico());
    } catch {
      setDiag([{ nome: 'Diagnóstico', resultado: 'sem conexão', linhas: [] }]);
    }
    setRodando(false);
  }

  async function salvar(nome: NomeChave) {
    await setSecret(nome, valores[nome]);
    setSalvas((s) => ({ ...s, [nome]: !!valores[nome].trim() }));
    setValores((v) => ({ ...v, [nome]: '' }));
    Alert.alert('Pronto', 'Chave guardada com segurança neste aparelho.');
  }

  const exportar = () =>
    Alert.alert(
      'Exportar para o Claude',
      'Gera um texto com seu perfil, gastos, metas, padrões e transações. Chaves, CPF, e-mail e seu nome não vão. Nomes de pessoas em Pix viram "pessoa", e vendedores de marketplace e restaurantes de app viram só a marca. Você escolhe para onde enviar (ex.: você mesmo) e cola na conversa com o Claude.',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Gerar e compartilhar',
          onPress: async () => {
            try {
              const texto = await gerarExport();
              await Share.share({ title: 'FinAgent: exportação para o economista', message: texto });
            } catch {
              Alert.alert('Não foi possível exportar', 'Tente de novo.');
            }
          },
        },
      ],
    );

  return (
    <Tela titulo="Configurações" texto="Cole cada chave abaixo. Elas ficam só no armazenamento seguro do aparelho e nunca são exibidas de volta.">
      <Link href="/perfil" style={s.link}>Perfil financeiro (salário, parcela, cartão, reservas)</Link>
      <Pressable style={s.botao} onPress={exportar}>
        <Text style={s.botaoTxt}>Exportar tudo para o Claude (economista)</Text>
      </Pressable>
      <Pressable style={s.botao} onPress={diagnosticar} disabled={rodando}>
        <Text style={s.botaoTxt}>{rodando ? 'Rodando...' : 'Diagnóstico da API do Mercado Pago'}</Text>
      </Pressable>
      {diag?.map((d) => (
        <Text key={d.nome} style={s.diag} selectable>
          {`${d.nome}: ${d.resultado}${d.linhas.length ? '\n' + d.linhas.join('\n') : ''}`}
        </Text>
      ))}
      {CHAVES.map((c) => (
        <Fragment key={c.nome}>
          <Text style={s.rotulo}>
            {c.rotulo} {salvas[c.nome] ? '(salva)' : '(não configurada)'}
          </Text>
          <TextInput
            style={s.input}
            value={valores[c.nome]}
            onChangeText={(t) => setValores((v) => ({ ...v, [c.nome]: t }))}
            placeholder="Cole aqui"
            placeholderTextColor={theme.muted}
            secureTextEntry
            autoCapitalize="none"
            autoCorrect={false}
          />
          <Pressable style={s.botao} onPress={() => salvar(c.nome)}>
            <Text style={s.botaoTxt}>Salvar</Text>
          </Pressable>
        </Fragment>
      ))}
    </Tela>
  );
}

const s = StyleSheet.create({
  link: { color: theme.tint, fontSize: 16 },
  rotulo: { color: theme.text, fontSize: 15, marginTop: 8 },
  input: { backgroundColor: theme.card, color: theme.text, borderColor: theme.border, borderWidth: 1, borderRadius: 8, padding: 12 },
  botao: { backgroundColor: theme.tint, borderRadius: 8, padding: 12, alignItems: 'center' },
  diag: { color: theme.muted, fontSize: 12 },
  botaoTxt: { color: '#0e1116', fontWeight: '700' },
});
