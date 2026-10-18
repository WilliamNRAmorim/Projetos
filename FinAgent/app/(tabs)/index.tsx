import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect, useRouter } from 'expo-router';
import { useCallback, useMemo, useState } from 'react';
import { Pressable, RefreshControl, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { alertasDoInicio, gerarInsights, nomeMes, serieEntrouSaiu, chaveMesDe } from '@/src/insights';
import { PERFIL_VAZIO, comprometidoDoMes, faixaLimite, livreAteSalario, mediaGastoMensal, mesesDeReserva, perfilParaNumeros, usoLimite, type PerfilTexto } from '@/src/metas';
import { COR_FAIXA } from '@/src/metasConfig';
import { brl } from '@/src/mp/analise';
import { classificarExtrato, saldoFinal, type Transacao } from '@/src/mp/extrato';
import { importarExtratos, lerExtrato, lerNome, salvarNome } from '@/src/mp/extratoStore';
import { lerPerfil } from '@/src/perfil';
import {
  BarChart, Botao, Card, EmptyState, InsightCard, Linha, MetricCard, SectionHeader, StackedBar,
  cores, espaco, fonte, paleta,
} from '@/src/ui';

const MES_CURTO = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
const maiuscula = (t: string) => t.charAt(0).toUpperCase() + t.slice(1);

export default function Inicio() {
  const router = useRouter();
  const topo = useSafeAreaInsets().top;
  const [texto, setTexto] = useState<PerfilTexto>(PERFIL_VAZIO);
  const [extrato, setExtrato] = useState<Transacao[]>([]);
  const [nome, setNome] = useState('');
  const [aviso, setAviso] = useState<string | null>(null);
  const [atualizando, setAtualizando] = useState(false);

  const carregar = useCallback(async () => {
    setAtualizando(true);
    const [p, ex, n] = await Promise.all([lerPerfil(), lerExtrato(), lerNome()]);
    setTexto(p);
    setExtrato(ex);
    setNome(n);
    setAtualizando(false);
  }, []);

  useFocusEffect(useCallback(() => { carregar(); }, [carregar]));

  const importar = async () => {
    setAviso(null);
    try {
      const r = await importarExtratos();
      if (!r) return;
      setExtrato(r.total);
      setAviso(r.linhas === 0 ? 'Nenhuma linha válida encontrada no arquivo.' : `${r.arquivos} arquivo(s) importado(s), ${r.linhas} linhas lidas.`);
    } catch {
      setAviso('Não foi possível ler o arquivo.');
    }
  };

  const hoje = new Date();
  const p = useMemo(() => perfilParaNumeros(texto), [texto]);
  const temPerfil = p.diaSalario !== null;
  const temExtrato = extrato.length > 0;

  const d = useMemo(() => {
    const lancs = classificarExtrato(extrato, nome);
    const saldo = saldoFinal(extrato)?.saldo ?? null;
    const media = mediaGastoMensal(extrato, nome, new Date())?.media ?? null;
    return {
      lancs,
      saldo,
      livre: saldo !== null ? livreAteSalario(saldo, p, new Date()) : null,
      insights: gerarInsights({ trans: extrato, lancs, perfil: p, hoje: new Date() }),
      alertas: alertasDoInicio({ trans: extrato, perfil: p, saldoConta: saldo, hoje: new Date() }),
      serie: serieEntrouSaiu(lancs, extrato),
      reserva: mesesDeReserva(p.cofrinho, media),
    };
  }, [extrato, nome, p]);

  const comp = comprometidoDoMes(p);
  const uso = usoLimite(p.limiteCartao, p.faturaAberta);
  const mes = nomeMes(chaveMesDe(hoje));
  const dias = d.livre?.dias;
  const salario = p.salario ?? 0;
  const livreSeg = Math.max(0, salario - comp.total);

  return (
    <ScrollView
      style={s.root}
      contentContainerStyle={[s.content, { paddingTop: topo + espaco.md }]}
      refreshControl={<RefreshControl refreshing={atualizando} onRefresh={carregar} tintColor={cores.primaria} />}>
      <View style={s.topo}>
        <Text style={s.mes} numberOfLines={1}>
          {maiuscula(mes)}{temPerfil ? ` · faltam ${dias ?? '-'} ${dias === 1 ? 'dia' : 'dias'} pro salário` : ''}
        </Text>
        <Pressable onPress={() => router.push('/metas')} hitSlop={10} style={s.sino} accessibilityLabel="Alertas">
          <Ionicons name={d.alertas.length > 0 ? 'notifications' : 'notifications-outline'} size={24} color={cores.texto} />
          {d.alertas.length > 0 && (
            <View style={s.contador}><Text style={s.contadorTxt}>{d.alertas.length}</Text></View>
          )}
        </Pressable>
      </View>

      {!temPerfil && (
        <EmptyState
          icone="person-circle-outline"
          titulo="Preencha seu perfil financeiro"
          texto="Salário, dia do pagamento, parcela e cartão: com isso o app mostra quanto está livre até o salário."
          botao="Abrir Perfil"
          aoBotao={() => router.push('/perfil')}
        />
      )}

      {!temExtrato && (
        <EmptyState
          icone="document-text-outline"
          titulo="Importe o extrato do Mercado Pago"
          texto="Escolha o(s) CSV de extrato, um por mês. Reimportar não duplica."
          botao="Importar extrato"
          aoBotao={importar}
        />
      )}

      {temPerfil && d.livre && (
        <Card>
          <Text style={s.rotulo}>Livre até dia {texto.diaSalario}</Text>
          <Text style={[s.heroi, d.livre.valor < 0 && { color: cores.perigo }]} numberOfLines={1} adjustsFontSizeToFit>
            {d.livre.valor < 0 ? `-${brl(-d.livre.valor)}` : brl(d.livre.valor)}
          </Text>
          <Text style={s.sub}>
            {d.livre.porDia !== null && d.livre.valor >= 0 ? `≈ ${brl(d.livre.porDia)} por dia` : d.livre.valor < 0 ? 'O saldo não cobre fatura e parcela até o salário.' : 'Hoje é dia de salário.'}
          </Text>
        </Card>
      )}

      {salario > 0 && comp.total > 0 && (
        <Card>
          <Text style={s.rotulo}>Salário já comprometido · {comp.pctSalario !== null ? comp.pctSalario.toFixed(0) : 0}%</Text>
          <StackedBar
            segmentos={[
              { rotulo: 'Fatura aberta', valor: comp.fatura, cor: paleta[4], texto: brl(comp.fatura) },
              { rotulo: 'Parcela do aparelho', valor: comp.parcela, cor: paleta[2], texto: brl(comp.parcela) },
              { rotulo: 'Livre', valor: livreSeg, cor: paleta[0], texto: brl(livreSeg) },
            ]}
          />
        </Card>
      )}

      <Linha>
        <MetricCard rotulo="Cofrinho" valor={p.cofrinho !== null ? brl(p.cofrinho) : '-'} />
        <MetricCard
          rotulo="Limite usado"
          valor={uso !== null ? `${uso.toFixed(0)}%` : '-'}
          cor={uso !== null ? COR_FAIXA[faixaLimite(uso)] : undefined}
        />
        <MetricCard rotulo="Reserva" valor={d.reserva !== null ? `${String(d.reserva).replace('.', ',')} m` : '-'} nota="meses de gasto" />
      </Linha>

      {d.serie.length > 0 && (
        <>
          <SectionHeader titulo="Entrou x saiu" />
          <Card>
            <BarChart
              dados={d.serie.map((x) => ({ rotulo: MES_CURTO[Number(x.mes.slice(5)) - 1], a: x.entrou, b: x.saiu }))}
              rotuloA="Entrou"
              rotuloB="Saiu (gastos + fatura)"
            />
          </Card>
        </>
      )}

      {d.insights.length > 0 && (
        <>
          <SectionHeader titulo="O que chamou atenção" />
          {d.insights.map((i) => (
            <InsightCard key={i.id} texto={i.texto} variante={i.tipo} icone={i.icone as never} />
          ))}
        </>
      )}

      <View style={s.botoes}>
        <View style={{ flex: 1 }}><Botao texto="Importar extrato" icone="cloud-upload-outline" secundario aoPressionar={importar} /></View>
        <View style={{ flex: 1 }}><Botao texto="Atualizar" icone="refresh" secundario aoPressionar={carregar} /></View>
      </View>
      {aviso && <Text style={s.mudo}>{aviso}</Text>}

      <Card>
        <Text style={s.rotulo}>Seu nome (para reconhecer transferências entre suas contas)</Text>
        <TextInput
          style={s.input}
          value={nome}
          onChangeText={(t) => { setNome(t); salvarNome(t); }}
          placeholder="Nome completo"
          placeholderTextColor={cores.texto2}
        />
        <Pressable onPress={() => router.push('/perfil')}><Text style={s.link}>Perfil financeiro</Text></Pressable>
        <Pressable onPress={() => router.push('/configuracoes')}><Text style={s.link}>Configurações (chaves de API)</Text></Pressable>
      </Card>

      <Text style={s.rodape}>Educativo, não é consultoria de investimentos.</Text>
    </ScrollView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: cores.fundo },
  content: { paddingHorizontal: espaco.lg, paddingBottom: espaco.xl, gap: espaco.md },
  topo: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  mes: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700', flex: 1 },
  sino: { padding: 4 },
  contador: { position: 'absolute', top: -2, right: -4, minWidth: 18, height: 18, borderRadius: 9, backgroundColor: cores.perigo, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 4 },
  contadorTxt: { color: cores.fundo, fontSize: 11, fontWeight: '800' },
  rotulo: { color: cores.texto2, fontSize: fonte.corpo, fontWeight: '600' },
  heroi: { color: cores.texto, fontSize: fonte.heroi, fontWeight: '800' },
  sub: { color: cores.texto2, fontSize: fonte.corpo },
  botoes: { flexDirection: 'row', gap: espaco.sm },
  mudo: { color: cores.texto2, fontSize: fonte.pequena },
  input: { backgroundColor: cores.fundo, color: cores.texto, borderColor: cores.borda, borderWidth: 1, borderRadius: 8, padding: 10 },
  link: { color: cores.primaria, fontSize: fonte.corpo },
  rodape: { color: cores.texto2, fontSize: 11, textAlign: 'center', opacity: 0.7 },
});
