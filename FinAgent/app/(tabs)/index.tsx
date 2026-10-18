import { Link, useFocusEffect } from 'expo-router';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, Pressable, RefreshControl, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { theme } from '@/src/theme';
import {
  brl, chaveMes, classificar, gastoPorCategoria, gastoPorTipo, maioresGastos, mesAnterior, totaisDoMes,
} from '@/src/mp/analise';
import {
  classificarExtrato, mesesDisponiveis, saldoFinal, totaisMes, type Transacao,
} from '@/src/mp/extrato';
import { importarExtratos, lerExtrato, lerNome, salvarNome } from '@/src/mp/extratoStore';
import { DadosMP, SemTokenError, atualizar, lerCache } from '@/src/mp/api';
import { parseValorBR } from '@/src/mp/extrato';
import { PERFIL_VAZIO, validarCampo, type PerfilTexto } from '@/src/metas';
import { lerPerfil, salvarPerfil } from '@/src/perfil';

export default function Painel() {
  const [dados, setDados] = useState<DadosMP | null>(null);
  const [erro, setErro] = useState<'token' | string | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [perfil, setPerfil] = useState<PerfilTexto>(PERFIL_VAZIO);
  const [extrato, setExtrato] = useState<Transacao[]>([]);
  const [meuNome, setMeuNome] = useState('');
  const [mesSel, setMesSel] = useState<string | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);

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
      setExtrato(await lerExtrato());
      setMeuNome(await lerNome());
      const c = await lerCache();
      if (c) setDados(c);
      await carregar();
    })();
  }, [carregar]);

  useFocusEffect(
    useCallback(() => {
      lerPerfil().then(setPerfil);
    }, []),
  );

  const mudarReserva = (k: 'cofrinho' | 'separadoAparelho', v: string) => {
    const novo = { ...perfil, [k]: v };
    setPerfil(novo);
    if (!validarCampo(k, v)) salvarPerfil(novo);
  };

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

  const meses = useMemo(() => mesesDisponiveis(extrato), [extrato]);
  const mesExt = mesSel && meses.includes(mesSel) ? mesSel : meses[0] ?? null;
  const ext = useMemo(() => {
    if (extrato.length === 0 || !mesExt) return null;
    const lancs = classificarExtrato(extrato, meuNome);
    return { totais: totaisMes(lancs, mesExt), saldo: saldoFinal(extrato) };
  }, [extrato, meuNome, mesExt]);

  const cofrinhoNum = parseValorBR(perfil.cofrinho);
  const aparelhoNum = parseValorBR(perfil.separadoAparelho);

  return (
    <ScrollView
      style={s.root}
      contentContainerStyle={s.content}
      refreshControl={<RefreshControl refreshing={carregando} onRefresh={() => { setCarregando(true); carregar(); }} tintColor={theme.tint} />}
    >
      <Text style={s.titulo}>Painel</Text>

      <View style={s.card}>
        <Text style={s.rotulo}>Cofrinho (reserva, informe manualmente)</Text>
        <TextInput
          style={s.input}
          value={perfil.cofrinho}
          onChangeText={(t) => mudarReserva('cofrinho', t)}
          placeholder="0,00"
          placeholderTextColor={theme.muted}
          keyboardType="decimal-pad"
        />
        {cofrinhoNum !== null && <Text style={s.grande}>{brl(cofrinhoNum)}</Text>}
        <Text style={s.rotulo}>Separado para a parcela do aparelho (Emergências)</Text>
        <TextInput
          style={s.input}
          value={perfil.separadoAparelho}
          onChangeText={(t) => mudarReserva('separadoAparelho', t)}
          placeholder="0,00"
          placeholderTextColor={theme.muted}
          keyboardType="decimal-pad"
        />
        {aparelhoNum !== null && <Text style={s.grande}>{brl(aparelhoNum)}</Text>}
        <Link href="/perfil" style={s.link}>Perfil financeiro</Link>
      </View>

      <View style={s.card}>
        <Pressable style={s.botao} onPress={importar}>
          <Text style={s.botaoTxt}>Importar extrato</Text>
        </Pressable>
        <Text style={s.mudo}>Escolha o(s) CSV de extrato do Mercado Pago (um por mês). Reimportar não duplica.</Text>
        {aviso && <Text style={s.mudo}>{aviso}</Text>}
        <TextInput
          style={s.input}
          value={meuNome}
          onChangeText={(t) => { setMeuNome(t); salvarNome(t); }}
          placeholder="Seu nome completo (para reconhecer transferências entre suas contas)"
          placeholderTextColor={theme.muted}
        />
      </View>

      {ext && (
        <>
          <View style={s.card}>
            <Text style={s.rotulo}>Saldo no extrato até {ext.saldo ? `${ext.saldo.data.slice(8)}/${ext.saldo.data.slice(5, 7)}` : '-'}</Text>
            <Text style={s.grande}>{brl(ext.saldo?.saldo ?? 0)}</Text>
            <Text style={s.mudo}>{meses.length} {meses.length === 1 ? 'mês importado' : 'meses importados'}.</Text>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8 }}>
            {meses.map((m) => (
              <Pressable key={m} style={[s.chip, m === mesExt && s.chipOn]} onPress={() => setMesSel(m)}>
                <Text style={[s.texto, m === mesExt && { color: theme.bg }]}>{m.slice(5)}/{m.slice(0, 4)}</Text>
              </Pressable>
            ))}
          </ScrollView>
          <View style={s.card}>
            <Text style={s.rotulo}>Mês {mesExt}</Text>
            <Linha nome="Entradas" valor={brl(ext.totais.entradas)} cor={theme.tint} />
            {ext.totais.entradasOutraConta > 0 && (
              <Text style={s.mudo}>Inclui {brl(ext.totais.entradasOutraConta)} da sua outra conta.</Text>
            )}
            <Linha nome="Gastos" valor={brl(ext.totais.gastos)} cor="#ef7b7b" />
            <Linha nome="Fatura do cartão" valor={brl(ext.totais.fatura)} />
            <Linha nome="Rendimentos" valor={brl(ext.totais.rendimentos)} />
            <Linha
              nome={ext.totais.reservaLiquida >= 0 ? 'Foi para o separado do aparelho (Emergências)' : 'Saiu do separado do aparelho (Emergências)'}
              valor={brl(Math.abs(ext.totais.reservaLiquida))}
            />
            {ext.totais.variacaoGasto !== null && (
              <Text style={s.mudo}>
                Gastos {ext.totais.variacaoGasto >= 0 ? '+' : ''}{ext.totais.variacaoGasto.toFixed(1).replace('.', ',')}% contra o mês anterior.
              </Text>
            )}
          </View>
          <Barras titulo="Gasto por categoria" itens={ext.totais.porCategoria} />
        </>
      )}

      {!ext && erro === 'token' && (
        <View style={s.card}>
          <Text style={s.texto}>Configure o token do Mercado Pago para ver seus dados.</Text>
          <Link href="/configuracoes" style={s.link}>Abrir Configurações</Link>
        </View>
      )}
      {!ext && erro && erro !== 'token' && (
        <View style={s.card}>
          <Text style={[s.texto, { color: '#ef7b7b' }]}>{erro}</Text>
          <Text style={s.mudo}>Puxe a tela para baixo para tentar de novo.</Text>
        </View>
      )}
      {carregando && !dados && !erro && <ActivityIndicator color={theme.tint} />}

      {!ext && analise && analise.atual.recebido === 0 && analise.atual.gasto === 0 && (
        <Text style={s.mudo}>Nenhuma movimentação neste mês ainda.</Text>
      )}

      {!ext && analise && (
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
  botao: { backgroundColor: theme.tint, borderRadius: 8, padding: 12, alignItems: 'center' },
  botaoTxt: { color: theme.bg, fontSize: 15, fontWeight: '700' },
  chip: { borderColor: theme.border, borderWidth: 1, borderRadius: 16, paddingVertical: 6, paddingHorizontal: 12 },
  chipOn: { backgroundColor: theme.tint },
  barra: { height: 6, backgroundColor: theme.tint, borderRadius: 3 },
});
