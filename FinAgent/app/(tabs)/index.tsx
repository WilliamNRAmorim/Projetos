import { Link } from 'expo-router';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, RefreshControl, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { theme } from '@/src/theme';
import {
  brl, chaveMes, classificar, gastoPorCategoria, gastoPorTipo, maioresGastos, mesAnterior, totaisDoMes,
} from '@/src/mp/analise';
import { DadosMP, SemTokenError, atualizar, lerCache, lerSaldo, parseValor, salvarSaldo } from '@/src/mp/api';

export default function Painel() {
  const [dados, setDados] = useState<DadosMP | null>(null);
  const [erro, setErro] = useState<'token' | string | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [saldo, setSaldo] = useState('');

  const carregar = useCallback(async () => {
    setErro(null);
    try {
      setDados(await atualizar());
    } catch (e) {
      setErro(e instanceof SemTokenError ? 'token' : e instanceof Error ? e.message : 'Falha ao atualizar.');
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    (async () => {
      setSaldo(await lerSaldo());
      const c = await lerCache();
      if (c) setDados(c);
      await carregar();
    })();
  }, [carregar]);

  const mesAtual = chaveMes(new Date().toISOString());
  const analise = useMemo(() => {
    if (!dados) return null;
    const movs = classificar(dados.pagamentos, dados.userId);
    return {
      atual: totaisDoMes(movs, mesAtual),
      anterior: totaisDoMes(movs, mesAnterior(mesAtual)),
      cats: gastoPorCategoria(movs, mesAtual),
      tipos: gastoPorTipo(movs, mesAtual),
      maiores: maioresGastos(movs, mesAtual, 8),
    };
  }, [dados, mesAtual]);

  const saldoNum = parseValor(saldo);

  return (
    <ScrollView
      style={s.root}
      contentContainerStyle={s.content}
      refreshControl={<RefreshControl refreshing={carregando} onRefresh={() => { setCarregando(true); carregar(); }} tintColor={theme.tint} />}
    >
      <Text style={s.titulo}>Painel</Text>

      <View style={s.card}>
        <Text style={s.rotulo}>Saldo (informe manualmente)</Text>
        <TextInput
          style={s.input}
          value={saldo}
          onChangeText={(t) => { setSaldo(t); salvarSaldo(t); }}
          placeholder="0,00"
          placeholderTextColor={theme.muted}
          keyboardType="decimal-pad"
        />
        {saldoNum !== null && <Text style={s.grande}>{brl(saldoNum)}</Text>}
      </View>

      {erro === 'token' && (
        <View style={s.card}>
          <Text style={s.texto}>Configure o token do Mercado Pago para ver seus dados.</Text>
          <Link href="/configuracoes" style={s.link}>Abrir Configurações</Link>
        </View>
      )}
      {erro && erro !== 'token' && (
        <View style={s.card}>
          <Text style={[s.texto, { color: '#ef7b7b' }]}>{erro}</Text>
          <Text style={s.mudo}>Puxe a tela para baixo para tentar de novo.</Text>
        </View>
      )}
      {carregando && !dados && !erro && <ActivityIndicator color={theme.tint} />}

      {analise && analise.atual.recebido === 0 && analise.atual.gasto === 0 && (
        <Text style={s.mudo}>Nenhuma movimentação neste mês ainda.</Text>
      )}

      {analise && (
        <>
          <View style={s.card}>
            <Text style={s.rotulo}>Este mês ({mesAtual})</Text>
            <Linha nome="Recebido" valor={brl(analise.atual.recebido)} cor={theme.tint} />
            <Linha nome="Gasto" valor={brl(analise.atual.gasto)} cor="#ef7b7b" />
            <Linha
              nome={analise.atual.sobra >= 0 ? 'Sobra' : 'Falta'}
              valor={brl(Math.abs(analise.atual.sobra))}
              cor={analise.atual.sobra >= 0 ? theme.tint : '#ef7b7b'}
            />
            <Text style={s.mudo}>
              Mês anterior: recebido {brl(analise.anterior.recebido)}, gasto {brl(analise.anterior.gasto)}.
            </Text>
            {analise.atual.interno > 0 && (
              <Text style={s.mudo}>Movimentação interna (fora dos totais): {brl(analise.atual.interno)}.</Text>
            )}
          </View>

          <Barras titulo="Gasto por categoria" itens={analise.cats} />
          <Barras titulo="Gasto por tipo de pagamento" itens={analise.tipos} />

          <View style={s.card}>
            <Text style={s.rotulo}>Maiores gastos do mês</Text>
            {analise.maiores.length === 0 && <Text style={s.mudo}>Sem gastos.</Text>}
            {analise.maiores.map((m) => (
              <Linha key={m.id} nome={`${m.dia.slice(8)}/${m.dia.slice(5, 7)} ${m.descricao || m.categoria}`} valor={brl(m.valor)} />
            ))}
          </View>
          {dados && <Text style={s.mudo}>Atualizado em {new Date(dados.atualizadoEm).toLocaleString('pt-BR')}</Text>}
        </>
      )}

      <Link href="/configuracoes" style={s.link}>Configurações (chaves de API)</Link>
      <Text style={s.mudo}>App educativo. Não é consultoria de investimentos registrada.</Text>
    </ScrollView>
  );
}

function Linha({ nome, valor, cor }: { nome: string; valor: string; cor?: string }) {
  return (
    <View style={s.linha}>
      <Text style={[s.texto, { flex: 1 }]} numberOfLines={1}>{nome}</Text>
      <Text style={[s.texto, cor ? { color: cor } : null]}>{valor}</Text>
    </View>
  );
}

function Barras({ titulo, itens }: { titulo: string; itens: { nome: string; total: number }[] }) {
  const max = Math.max(1, ...itens.map((i) => i.total));
  return (
    <View style={s.card}>
      <Text style={s.rotulo}>{titulo}</Text>
      {itens.length === 0 && <Text style={s.mudo}>Sem gastos.</Text>}
      {itens.map((i) => (
        <View key={i.nome} style={{ gap: 4 }}>
          <Linha nome={i.nome} valor={brl(i.total)} />
          <View style={s.trilho}>
            <View style={[s.barra, { width: `${(i.total / max) * 100}%` }]} />
          </View>
        </View>
      ))}
    </View>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
  content: { padding: 20, gap: 12 },
  titulo: { color: theme.text, fontSize: 24, fontWeight: '700' },
  card: { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1, borderRadius: 10, padding: 14, gap: 8 },
  rotulo: { color: theme.muted, fontSize: 13, fontWeight: '600' },
  texto: { color: theme.text, fontSize: 15 },
  mudo: { color: theme.muted, fontSize: 12 },
  grande: { color: theme.text, fontSize: 22, fontWeight: '700' },
  link: { color: theme.tint, fontSize: 16 },
  input: { backgroundColor: theme.bg, color: theme.text, borderColor: theme.border, borderWidth: 1, borderRadius: 8, padding: 10 },
  linha: { flexDirection: 'row', gap: 8, justifyContent: 'space-between' },
  trilho: { height: 6, backgroundColor: theme.border, borderRadius: 3 },
  barra: { height: 6, backgroundColor: theme.tint, borderRadius: 3 },
});
