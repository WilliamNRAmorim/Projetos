import { useFocusEffect, useRouter } from 'expo-router';
import { useCallback, useMemo, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Switch, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { nomeMes } from '@/src/insights';
import { ModalCategoria } from '@/src/gastos/ModalCategoria';
import {
  REGRAS_VAZIAS, adicionarRegra, agruparPorDia, descricaoLimpa, filtrarTransacoes, formatarDia, linhasOrcamento,
  mediaUltimos3Meses, porCategoriaNoPeriodo, type Faixa, type Periodo, type RegrasSalvas, type Tetos,
} from '@/src/gastos/gastos';
import { lerRegras, lerTetos, salvarRegras, salvarTetos } from '@/src/gastos/gastosStore';
import { brl } from '@/src/mp/analise';
import { CAT, ehMovimentoInterno } from '@/src/mp/categorias';
import { classificarExtrato, mesesDisponiveis, type Lancamento, type Transacao } from '@/src/mp/extrato';
import { lerExtrato, lerNome } from '@/src/mp/extratoStore';
import {
  Badge, Botao, Card, DonutChart, EmptyState, Linha, MetricCard, ProgressBar, SectionHeader,
  cores, espaco, fonte, paleta, raio, type Variante,
} from '@/src/ui';

const COR_FAIXA: Record<Faixa, string> = { ok: cores.sucesso, atencao: cores.alerta, estourou: cores.perigo };
const PERIODOS: { id: Periodo; rotulo: string }[] = [
  { id: 'mes', rotulo: 'Mês atual' }, { id: '3m', rotulo: '3 meses' }, { id: 'tudo', rotulo: 'Tudo' },
];
const POR_PAGINA = 40;
const rotuloMes = (m: string) => `${nomeMes(m)} ${m.slice(2, 4)}`;

function variante(l: Lancamento): Variante {
  if (l.valor > 0) return 'sucesso';
  return l.categoria === CAT.OUTROS || l.categoria === CAT.PIX_PESSOAS ? 'alerta' : 'info';
}

const Chip = ({ texto, ativo, aoPressionar }: { texto: string; ativo: boolean; aoPressionar: () => void }) => (
  <Pressable onPress={aoPressionar} style={[s.chip, ativo ? s.chipOn : null]}>
    <Text style={[s.chipTxt, ativo ? { color: cores.primaria } : null]}>{texto}</Text>
  </Pressable>
);

export default function Gastos() {
  const router = useRouter();
  const topo = useSafeAreaInsets().top;
  const [extrato, setExtrato] = useState<Transacao[]>([]);
  const [nome, setNome] = useState('');
  const [carregado, setCarregado] = useState(false);
  const [tetos, setTetos] = useState<Tetos>({});
  const [regras, setRegras] = useState<RegrasSalvas>(REGRAS_VAZIAS);
  const [editando, setEditando] = useState<string | null>(null);
  const [valorTeto, setValorTeto] = useState('');
  const [periodo, setPeriodo] = useState<Periodo>('mes');
  const [busca, setBusca] = useState('');
  const [catFiltro, setCatFiltro] = useState<string | null>(null);
  const [mesFiltro, setMesFiltro] = useState<string | null>(null);
  const [internos, setInternos] = useState(false);
  const [limite, setLimite] = useState(POR_PAGINA);
  const [alvo, setAlvo] = useState<Lancamento | null>(null);

  useFocusEffect(
    useCallback(() => {
      (async () => {
        const [ex, n, t, r] = await Promise.all([lerExtrato(), lerNome(), lerTetos(), lerRegras()]);
        setExtrato(ex);
        setNome(n);
        setTetos(t);
        setRegras(r);
        setCarregado(true);
      })();
    }, []),
  );

  const lancs = useMemo(() => classificarExtrato(extrato, nome, regras), [extrato, nome, regras]);
  const meses = useMemo(() => mesesDisponiveis(lancs), [lancs]);
  const mesRef = meses[0] ?? ''; // "mês atual" = mês mais recente do extrato importado
  const orc = useMemo(() => (mesRef ? linhasOrcamento(lancs, mesRef, tetos) : null), [lancs, mesRef, tetos]);
  const fatias = useMemo(() => (mesRef ? porCategoriaNoPeriodo(lancs, periodo, mesRef) : []), [lancs, periodo, mesRef]);
  const totalFatias = fatias.reduce((a, f) => a + f.total, 0);
  const filtradas = useMemo(
    () => filtrarTransacoes(lancs, { busca, categoria: catFiltro, mes: mesFiltro, mostrarInternos: internos }),
    [lancs, busca, catFiltro, mesFiltro, internos],
  );
  const grupos = useMemo(() => agruparPorDia(filtradas.slice(0, limite)), [filtradas, limite]);
  const categoriasPresentes = useMemo(
    () => [...new Set(lancs.filter((l) => internos || !ehMovimentoInterno(l.categoria)).map((l) => l.categoria))].sort(),
    [lancs, internos],
  );

  const abrirTeto = (cat: string, atual: number | null) => {
    setEditando(cat);
    const sug = atual ?? mediaUltimos3Meses(lancs, mesRef, cat);
    setValorTeto(sug ? String(sug) : '');
  };
  const salvarTeto = async () => {
    if (!editando) return;
    const n = Number(valorTeto.replace(',', '.'));
    const novo = { ...tetos };
    if (Number.isFinite(n) && n > 0) novo[editando] = n;
    else delete novo[editando];
    setTetos(novo);
    setEditando(null);
    await salvarTetos(novo);
  };

  const salvarCategoria = async (cat: string, soEsta: boolean) => {
    if (!alvo) return;
    const novas = adicionarRegra(regras, alvo, cat, soEsta);
    setRegras(novas);
    setAlvo(null);
    await salvarRegras(novas);
  };

  const formTeto = (cat: string) =>
    editando === cat ? (
      <View style={s.edicao}>
        <TextInput
          value={valorTeto}
          onChangeText={setValorTeto}
          keyboardType="numeric"
          placeholder="Teto mensal (R$)"
          placeholderTextColor={cores.texto2}
          style={s.input}
        />
        <Text style={s.nota}>
          {mediaUltimos3Meses(lancs, mesRef, cat) ? 'Sugestão: média dos últimos 3 meses. ' : ''}Deixe vazio para remover o teto.
        </Text>
        <Linha>
          <View style={{ flex: 1 }}><Botao texto="Cancelar" secundario aoPressionar={() => setEditando(null)} /></View>
          <View style={{ flex: 1 }}><Botao texto="Salvar" aoPressionar={salvarTeto} /></View>
        </Linha>
      </View>
    ) : null;

  if (carregado && lancs.length === 0) {
    return (
      <View style={[s.root, { paddingTop: topo + espaco.md, padding: espaco.lg, gap: espaco.md }]}>
        <Text style={s.titulo}>Gastos</Text>
        <EmptyState
          icone="document-text-outline"
          titulo="Sem extrato importado"
          texto="Importe o extrato do Mercado Pago no Início para ver orçamento, categorias e transações."
          botao="Ir para o Início"
          aoBotao={() => router.push('/')}
        />
      </View>
    );
  }

  return (
    <ScrollView style={s.root} contentContainerStyle={[s.content, { paddingTop: topo + espaco.md }]} keyboardShouldPersistTaps="handled">
      <Text style={s.titulo}>Gastos</Text>

      <SectionHeader titulo={mesRef ? `Orçamento de ${nomeMes(mesRef)}` : 'Orçamento'} />
      {orc && (
        <>
          <Linha>
            <MetricCard rotulo="Orçado" valor={brl(orc.totalOrcado)} />
            <MetricCard
              rotulo="Gasto (com teto)"
              valor={brl(orc.totalGasto)}
              cor={orc.totalOrcado > 0 && orc.totalGasto > orc.totalOrcado ? cores.perigo : undefined}
            />
          </Linha>
          {orc.linhas.map((l) => (
            <Card key={l.categoria}>
              <View style={s.linha}>
                <Text style={s.nome}>{l.categoria}</Text>
                <Text style={s.valor}>{brl(l.gasto)}{l.teto ? ` de ${brl(l.teto)}` : ''}</Text>
              </View>
              {l.teto && l.pct !== null && l.faixa ? (
                <>
                  <ProgressBar pct={l.pct} cor={COR_FAIXA[l.faixa]} />
                  <View style={s.linha}>
                    <Text style={[s.nota, { color: COR_FAIXA[l.faixa] }]}>
                      {l.faixa === 'estourou' ? `Estourou em ${brl(l.gasto - l.teto)}` : l.faixa === 'atencao' ? 'Atenção' : 'Dentro do teto'} · {Math.round(l.pct)}%
                    </Text>
                    <Pressable onPress={() => abrirTeto(l.categoria, l.teto)} hitSlop={8}><Text style={s.link}>Editar teto</Text></Pressable>
                  </View>
                </>
              ) : (
                <Pressable onPress={() => abrirTeto(l.categoria, null)} hitSlop={8}><Text style={s.link}>Definir teto</Text></Pressable>
              )}
              {formTeto(l.categoria)}
            </Card>
          ))}
          {orc.linhas.length === 0 && <Text style={s.nota}>Nenhum gasto neste mês ainda.</Text>}
          {!orc.linhas.some((l) => l.categoria === CAT.FATURA) && (
            <Card>
              <Pressable onPress={() => abrirTeto(CAT.FATURA, null)} hitSlop={8}>
                <Text style={s.link}>Definir teto da fatura do cartão</Text>
              </Pressable>
              {formTeto(CAT.FATURA)}
            </Card>
          )}
        </>
      )}

      <SectionHeader titulo="Pra onde foi" />
      <View style={s.chips}>
        {PERIODOS.map((p) => <Chip key={p.id} texto={p.rotulo} ativo={periodo === p.id} aoPressionar={() => setPeriodo(p.id)} />)}
      </View>
      <Card>
        {fatias.length === 0 ? (
          <Text style={s.nota}>Sem gastos no período.</Text>
        ) : (
          <DonutChart
            fatias={fatias.map((f, i) => ({
              rotulo: f.nome,
              valor: f.total,
              cor: paleta[i % paleta.length],
              texto: `${brl(f.total)} · ${Math.round(f.pct)}%`,
            }))}
            centro={<Text style={s.nome}>{brl(totalFatias)}</Text>}
          />
        )}
      </Card>

      <SectionHeader titulo="Transações" />
      <TextInput
        value={busca}
        onChangeText={(t) => { setBusca(t); setLimite(POR_PAGINA); }}
        placeholder="Buscar por descrição ou categoria"
        placeholderTextColor={cores.texto2}
        style={s.input}
      />
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={s.chips}>
        <Chip texto="Todos os meses" ativo={mesFiltro === null} aoPressionar={() => setMesFiltro(null)} />
        {meses.map((m) => <Chip key={m} texto={rotuloMes(m)} ativo={mesFiltro === m} aoPressionar={() => setMesFiltro(m)} />)}
      </ScrollView>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={s.chips}>
        <Chip texto="Todas as categorias" ativo={catFiltro === null} aoPressionar={() => setCatFiltro(null)} />
        {categoriasPresentes.map((c) => <Chip key={c} texto={c} ativo={catFiltro === c} aoPressionar={() => setCatFiltro(c)} />)}
      </ScrollView>
      <View style={s.linha}>
        <Text style={s.nota}>Mostrar movimentos internos</Text>
        <Switch value={internos} onValueChange={setInternos} trackColor={{ true: cores.primaria }} />
      </View>

      {filtradas.length === 0 && <Text style={s.nota}>Nada encontrado com esses filtros.</Text>}
      {grupos.map((g) => (
        <View key={g.data} style={{ gap: espaco.sm }}>
          <Text style={s.dia}>{formatarDia(g.data)}</Text>
          {g.itens.map((l) => (
            <Pressable key={`${l.data}|${l.seq}|${l.ref}`} onPress={() => setAlvo(l)}>
              <Card style={s.trans}>
                <View style={{ flex: 1, gap: 4 }}>
                  <Text style={s.nome} numberOfLines={1}>{descricaoLimpa(l)}</Text>
                  <Badge texto={l.excluida ? `${l.categoria} (ignorada)` : l.categoria} variante={variante(l)} />
                </View>
                <Text style={[s.valor, { color: l.valor >= 0 ? cores.sucesso : cores.texto }]}>
                  {l.valor >= 0 ? '+' : '-'}{brl(Math.abs(l.valor))}
                </Text>
              </Card>
            </Pressable>
          ))}
        </View>
      ))}
      {filtradas.length > limite && <Botao texto="Mostrar mais" secundario aoPressionar={() => setLimite(limite + POR_PAGINA)} />}

      {alvo && (
        <ModalCategoria
          titulo={descricaoLimpa(alvo)}
          atual={alvo.categoria}
          temContraparte={!!alvo.contraparte}
          aoSalvar={salvarCategoria}
          aoFechar={() => setAlvo(null)}
        />
      )}
    </ScrollView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: cores.fundo },
  content: { padding: espaco.lg, gap: espaco.md, paddingBottom: 48 },
  titulo: { color: cores.texto, fontSize: fonte.numero, fontWeight: '700' },
  linha: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: espaco.sm },
  nome: { color: cores.texto, fontSize: fonte.corpo, fontWeight: '600', flexShrink: 1 },
  valor: { color: cores.texto, fontSize: fonte.corpo, fontWeight: '600' },
  nota: { color: cores.texto2, fontSize: fonte.pequena },
  link: { color: cores.primaria, fontSize: fonte.corpo },
  edicao: { gap: espaco.sm, marginTop: espaco.sm },
  input: { backgroundColor: cores.superficie2, color: cores.texto, borderRadius: raio.md, paddingHorizontal: espaco.md, paddingVertical: 10, fontSize: fonte.corpo, borderWidth: 1, borderColor: cores.borda },
  chips: { flexDirection: 'row', gap: espaco.sm },
  chip: { borderWidth: 1, borderColor: cores.borda, borderRadius: raio.pill, paddingHorizontal: 12, paddingVertical: 6 },
  chipOn: { borderColor: cores.primaria },
  chipTxt: { color: cores.texto2, fontSize: fonte.pequena },
  dia: { color: cores.texto2, fontSize: fonte.pequena, marginTop: espaco.sm },
  trans: { flexDirection: 'row', alignItems: 'center', gap: espaco.md, padding: espaco.md },
});
