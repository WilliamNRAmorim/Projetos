import { useCallback, useEffect, useMemo, useState } from 'react';
import { Pressable, RefreshControl, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { alertasDisparados, type Alerta } from '@/src/mercado/alertas';
import { atualizarMercado, lerCache, type Resultado } from '@/src/mercado/api';
import { ativoDeEntrada } from '@/src/mercado/ativos';
import { AVISO_EDUCATIVO, COMECANDO } from '@/src/mercado/comecando';
import { calcularIndicadores } from '@/src/mercado/indicadores';
import { gerarLeitura } from '@/src/mercado/leitura';
import { lerAlertas, lerWatchlist, salvarAlertas, salvarWatchlist } from '@/src/mercado/store';
import type { Ativo } from '@/src/mercado/tipos';
import { theme } from '@/src/theme';

const brl = (n: number) => 'R$ ' + n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: n < 1 ? 6 : 2 });
const pc = (n: number | null) => (n == null ? 'n/d' : `${n >= 0 ? '+' : ''}${n.toFixed(2).replace('.', ',')}%`);
const cor = (n: number | null) => (n == null ? theme.muted : n >= 0 ? theme.tint : '#ef6b6b');
const quando = (iso: string | null) => (iso ? new Date(iso).toLocaleString('pt-BR') : 'nunca');

export default function Mercado() {
  const [lista, setLista] = useState<Ativo[]>([]);
  const [alertas, setAlertas] = useState<Alerta[]>([]);
  const [res, setRes] = useState<Record<string, Resultado>>({});
  const [em, setEm] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);
  const [aberto, setAberto] = useState<string | null>(null);
  const [novo, setNovo] = useState('');
  const [msg, setMsg] = useState('');
  const [guia, setGuia] = useState(false);
  const [dir, setDir] = useState<'acima' | 'abaixo'>('acima');
  const [nivel, setNivel] = useState('');

  const atualizar = useCallback(async (ativos: Ativo[]) => {
    setCarregando(true);
    try {
      const a = await atualizarMercado(ativos);
      setRes(a.resultados);
      setEm(a.atualizadoEm);
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    (async () => {
      const [l, al, cache] = await Promise.all([lerWatchlist(), lerAlertas(), lerCache()]);
      setLista(l);
      setAlertas(al);
      const doCache: Record<string, Resultado> = {};
      for (const a of l) if (cache.dados[a.id]) doCache[a.id] = { ok: true, doCache: true, dados: cache.dados[a.id] };
      setRes(doCache);
      setEm(cache.atualizadoEm);
      atualizar(l);
    })();
  }, [atualizar]);

  const precos = useMemo(() => {
    const p: Record<string, number | undefined> = {};
    for (const [id, r] of Object.entries(res)) if (r.ok) p[id] = r.dados.cotacao.preco;
    return p;
  }, [res]);
  const disparados = useMemo(() => alertasDisparados(alertas, precos), [alertas, precos]);
  const nomeDe = (id: string) => lista.find((a) => a.id === id)?.nome ?? id;

  async function adicionar() {
    const a = ativoDeEntrada(novo);
    if (!a) return setMsg('Não reconheci. Use ticker da B3 (PETR4), moeda (USD, EUR) ou cripto (BTC, ETH).');
    if (lista.some((x) => x.id === a.id)) return setMsg('Já está na lista.');
    const l = [...lista, a];
    setLista(l);
    setNovo('');
    setMsg('');
    await salvarWatchlist(l);
    atualizar(l);
  }

  async function remover(id: string) {
    const l = lista.filter((a) => a.id !== id);
    const al = alertas.filter((a) => a.ativoId !== id);
    setLista(l);
    setAlertas(al);
    setAberto(null);
    await Promise.all([salvarWatchlist(l), salvarAlertas(al)]);
  }

  async function criarAlerta(ativoId: string) {
    const n = Number(nivel.replace(',', '.'));
    if (!Number.isFinite(n) || n <= 0) return setMsg('Informe um nível numérico maior que zero.');
    const al = [...alertas, { id: String(Date.now()), ativoId, direcao: dir, nivel: n }];
    setAlertas(al);
    setNivel('');
    setMsg('');
    await salvarAlertas(al);
  }

  async function removerAlerta(id: string) {
    const al = alertas.filter((a) => a.id !== id);
    setAlertas(al);
    await salvarAlertas(al);
  }

  return (
    <ScrollView
      style={s.root}
      contentContainerStyle={s.content}
      refreshControl={<RefreshControl refreshing={carregando} onRefresh={() => atualizar(lista)} tintColor={theme.tint} />}>
      <Text style={s.titulo}>Mercado</Text>
      <Text style={s.muted}>Última atualização: {quando(em)}. Puxe para atualizar.</Text>
      <Text style={s.aviso}>{AVISO_EDUCATIVO}</Text>

      {disparados.map((a) => (
        <View key={a.id} style={s.alerta}>
          <Text style={s.alertaTxt}>
            Alerta: {nomeDe(a.ativoId)} está {a.direcao === 'acima' ? 'acima' : 'abaixo'} de {brl(a.nivel)} (atual {brl(precos[a.ativoId]!)}).
          </Text>
        </View>
      ))}

      <View style={s.linha}>
        <TextInput
          style={[s.input, { flex: 1 }]}
          value={novo}
          onChangeText={setNovo}
          placeholder="Adicionar: PETR4, USD, BTC..."
          placeholderTextColor={theme.muted}
          autoCapitalize="characters"
          onSubmitEditing={adicionar}
        />
        <Pressable style={s.botao} onPress={adicionar}>
          <Text style={s.botaoTxt}>Adicionar</Text>
        </Pressable>
      </View>
      {msg ? <Text style={s.erro}>{msg}</Text> : null}

      {lista.map((a) => {
        const r = res[a.id];
        const ok = r && r.ok ? r : null;
        const ind = ok ? calcularIndicadores(ok.dados.serie, ok.dados.cotacao.preco) : null;
        const abertoAqui = aberto === a.id;
        return (
          <View key={a.id} style={s.card}>
            <Pressable onPress={() => setAberto(abertoAqui ? null : a.id)}>
              <View style={s.linhaEntre}>
                <Text style={s.nome}>{a.nome}</Text>
                {ok ? <Text style={s.preco}>{brl(ok.dados.cotacao.preco)}</Text> : null}
              </View>
              {ok ? (
                <>
                  <Text style={{ color: cor(ok.dados.cotacao.variacaoDia), fontSize: 14 }}>Dia: {pc(ok.dados.cotacao.variacaoDia)}</Text>
                  {ind ? (
                    <Text style={s.muted}>
                      7d {pc(ind.var7d)} · 30d {pc(ind.var30d)} · RSI {ind.rsi14 == null ? 'n/d' : Math.round(ind.rsi14)} · tendência {ind.tendencia}
                    </Text>
                  ) : null}
                  {ok.doCache ? <Text style={s.muted}>Dado salvo de {quando(ok.dados.em)}{ok.aviso ? ` (${ok.aviso})` : ''}</Text> : null}
                </>
              ) : (
                <Text style={s.erro}>{r && !r.ok ? r.erro : 'Carregando...'}</Text>
              )}
            </Pressable>

            {abertoAqui ? (
              <View style={s.detalhe}>
                {ok ? <Text style={s.leitura}>{gerarLeitura(a.nome, a.tipo, ind)}</Text> : null}
                {ind && ind.maxima90 != null && ind.minima90 != null ? (
                  <Text style={s.muted}>
                    Máx. {brl(ind.maxima90)} ({pc(ind.distMaxima)}) · Mín. {brl(ind.minima90)} ({pc(ind.distMinima)}) · Vol. diária {ind.volatilidade == null ? 'n/d' : ind.volatilidade.toFixed(1).replace('.', ',') + '%'}
                  </Text>
                ) : null}

                <Text style={s.sub}>Alertas de preço</Text>
                {alertas.filter((x) => x.ativoId === a.id).map((x) => (
                  <View key={x.id} style={s.linhaEntre}>
                    <Text style={s.muted}>{x.direcao === 'acima' ? 'Acima de' : 'Abaixo de'} {brl(x.nivel)}</Text>
                    <Pressable onPress={() => removerAlerta(x.id)}>
                      <Text style={s.link}>remover</Text>
                    </Pressable>
                  </View>
                ))}
                <View style={s.linha}>
                  <Pressable style={[s.chip, dir === 'acima' && s.chipOn]} onPress={() => setDir('acima')}>
                    <Text style={s.chipTxt}>Acima</Text>
                  </Pressable>
                  <Pressable style={[s.chip, dir === 'abaixo' && s.chipOn]} onPress={() => setDir('abaixo')}>
                    <Text style={s.chipTxt}>Abaixo</Text>
                  </Pressable>
                  <TextInput
                    style={[s.input, { flex: 1 }]}
                    value={nivel}
                    onChangeText={setNivel}
                    placeholder="Nível (R$)"
                    placeholderTextColor={theme.muted}
                    keyboardType="decimal-pad"
                  />
                  <Pressable style={s.botao} onPress={() => criarAlerta(a.id)}>
                    <Text style={s.botaoTxt}>Criar</Text>
                  </Pressable>
                </View>
                <Pressable onPress={() => remover(a.id)}>
                  <Text style={s.link}>Remover da lista</Text>
                </Pressable>
              </View>
            ) : null}
          </View>
        );
      })}

      <Pressable style={s.card} onPress={() => setGuia(!guia)}>
        <Text style={s.nome}>Começando em ações {guia ? '▲' : '▼'}</Text>
        {guia ? (
          <View style={{ gap: 10, marginTop: 8 }}>
            {COMECANDO.map((c) => (
              <View key={c.titulo}>
                <Text style={s.sub}>{c.titulo}</Text>
                <Text style={s.leitura}>{c.texto}</Text>
              </View>
            ))}
            <Text style={s.aviso}>{AVISO_EDUCATIVO}</Text>
          </View>
        ) : null}
      </Pressable>
    </ScrollView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
  content: { padding: 20, gap: 12 },
  titulo: { color: theme.text, fontSize: 24, fontWeight: '700' },
  muted: { color: theme.muted, fontSize: 13, lineHeight: 19 },
  aviso: { color: theme.muted, fontSize: 12, fontStyle: 'italic' },
  erro: { color: '#ef6b6b', fontSize: 13 },
  card: { backgroundColor: theme.card, borderRadius: 12, padding: 14, borderWidth: 1, borderColor: theme.border, gap: 4 },
  linha: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  linhaEntre: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  nome: { color: theme.text, fontSize: 16, fontWeight: '600' },
  preco: { color: theme.text, fontSize: 16 },
  detalhe: { marginTop: 10, gap: 8, borderTopWidth: 1, borderTopColor: theme.border, paddingTop: 10 },
  leitura: { color: theme.text, fontSize: 14, lineHeight: 21 },
  sub: { color: theme.text, fontSize: 14, fontWeight: '600' },
  input: { backgroundColor: theme.card, color: theme.text, borderRadius: 8, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 10, paddingVertical: 8 },
  botao: { backgroundColor: theme.tint, borderRadius: 8, paddingHorizontal: 12, paddingVertical: 10 },
  botaoTxt: { color: '#0e1116', fontWeight: '700' },
  chip: { borderWidth: 1, borderColor: theme.border, borderRadius: 8, paddingHorizontal: 10, paddingVertical: 8 },
  chipOn: { borderColor: theme.tint },
  chipTxt: { color: theme.text, fontSize: 13 },
  link: { color: theme.tint, fontSize: 13 },
  alerta: { backgroundColor: '#3a2f12', borderColor: '#e0b43c', borderWidth: 1, borderRadius: 10, padding: 12 },
  alertaTxt: { color: '#f5d77a', fontSize: 14, fontWeight: '600' },
});
