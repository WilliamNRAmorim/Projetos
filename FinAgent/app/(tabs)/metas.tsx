import { Link, useFocusEffect } from 'expo-router';
import { useCallback, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  PERFIL_VAZIO, comprometidoDoMes, dataCurta, faixaLimite, livreAteSalario, mediaGastoMensal, mesesDeReserva,
  metaReserva, perfilParaNumeros, progressoReserva, retiradasCofrinho, usoLimite, type PerfilTexto,
} from '@/src/metas';
import { COR_FAIXA, FATURA_SAUDAVEL_PCT, MESES_RESERVA } from '@/src/metasConfig';
import { brl } from '@/src/mp/analise';
import { saldoFinal, type Transacao } from '@/src/mp/extrato';
import { lerExtrato, lerNome } from '@/src/mp/extratoStore';
import { lerPerfil } from '@/src/perfil';
import { theme } from '@/src/theme';

const pct = (n: number) => `${n.toFixed(1).replace('.', ',')}%`;

export default function Metas() {
  const [texto, setTexto] = useState<PerfilTexto>(PERFIL_VAZIO);
  const [extrato, setExtrato] = useState<Transacao[]>([]);
  const [nome, setNome] = useState('');

  useFocusEffect(
    useCallback(() => {
      (async () => {
        setTexto(await lerPerfil());
        setExtrato(await lerExtrato());
        setNome(await lerNome());
      })();
    }, []),
  );

  const p = perfilParaNumeros(texto);
  const hoje = new Date();
  const comp = comprometidoDoMes(p);
  const saldoConta = saldoFinal(extrato)?.saldo ?? null;
  const livre = saldoConta !== null ? livreAteSalario(saldoConta, p, hoje) : null;
  const uso = usoLimite(p.limiteCartao, p.faturaAberta);
  const faixa = uso !== null ? faixaLimite(uso) : null;
  const gasto = mediaGastoMensal(extrato, nome, hoje);
  const retiradas = retiradasCofrinho(extrato);
  const mesesRes = mesesDeReserva(p.cofrinho, gasto?.media ?? null);

  const alertas: string[] = [];
  if (retiradas.length > 0) alertas.push(`Você retirou ${brl(retiradas[0].valor)} do Cofrinho em ${dataCurta(retiradas[0].data)}. A meta é não mexer na reserva.`);
  if (faixa === 'alerta') alertas.push(`Você está usando ${pct(uso!)} do limite do cartão (acima de 60%).`);
  if (comp.pctSalario !== null && comp.pctSalario > 50) alertas.push(`${pct(comp.pctSalario)} do salário já está comprometido neste mês.`);
  if (livre && livre.valor < 0) alertas.push(`O saldo da conta não cobre a fatura aberta e a parcela até o dia do salário (faltam ${brl(-livre.valor)}).`);
  if (p.cofrinho !== null && gasto && p.cofrinho < metaReserva(gasto.media, MESES_RESERVA[0])) {
    alertas.push(`O Cofrinho cobre menos de ${MESES_RESERVA[0]} meses de gasto.`);
  }

  return (
    <ScrollView style={s.root} contentContainerStyle={s.content}>
      <Text style={s.titulo}>Metas</Text>
      <Text style={s.aviso}>Educativo, não é consultoria de investimentos.</Text>
      <Link href="/perfil" style={s.link}>Editar perfil financeiro</Link>

      {alertas.length > 0 && (
        <View style={[s.card, { borderColor: COR_FAIXA.alerta }]}>
          <Text style={s.rotulo}>Alertas</Text>
          {alertas.map((a) => (
            <Text key={a} style={[s.texto, { color: COR_FAIXA.alerta }]}>{a}</Text>
          ))}
        </View>
      )}

      <View style={s.card}>
        <Text style={s.rotulo}>Comprometido do mês</Text>
        {p.parcela === null && p.faturaAberta === null ? (
          <Text style={s.mudo}>Preencha a parcela do aparelho e a fatura aberta no Perfil.</Text>
        ) : (
          <>
            <Linha nome="Parcela do aparelho" valor={brl(comp.parcela)} />
            <Linha nome="Fatura aberta" valor={brl(comp.fatura)} />
            <Linha nome="Total comprometido" valor={brl(comp.total)} forte />
            <Text style={s.mudo}>
              {comp.pctSalario !== null ? `${pct(comp.pctSalario)} do salário líquido.` : 'Informe o salário no Perfil para ver o percentual.'}
            </Text>
          </>
        )}
        {livre ? (
          <>
            <Linha nome={`Livre até o salário (${livre.dias} dias)`} valor={brl(livre.valor)} cor={livre.valor < 0 ? COR_FAIXA.alerta : undefined} forte />
            {livre.porDia !== null && <Text style={s.mudo}>Cerca de {brl(livre.porDia)} por dia.</Text>}
            <Text style={s.mudo}>Estimativa: saldo da conta no extrato menos fatura aberta e a parte da parcela ainda não separada. Não conta o Cofrinho.</Text>
          </>
        ) : (
          <Text style={s.mudo}>
            {p.diaSalario === null ? 'Informe o dia do salário no Perfil para ver quanto está livre.' : 'Importe o extrato no Início para ver quanto está livre até o salário.'}
          </Text>
        )}
      </View>

      <View style={s.card}>
        <Text style={s.rotulo}>Uso do limite do cartão</Text>
        {uso === null || faixa === null ? (
          <Text style={s.mudo}>Informe o limite e o valor da fatura aberta no Perfil.</Text>
        ) : (
          <>
            <Text style={[s.grande, { color: COR_FAIXA[faixa] }]}>{pct(uso)}</Text>
            <Barra valor={uso} cor={COR_FAIXA[faixa]} />
            <Text style={s.mudo}>
              {brl(p.faturaAberta ?? 0)} de {brl(p.limiteCartao ?? 0)} ({faixa === 'ok' ? 'ok' : faixa === 'atencao' ? 'atenção' : 'alerta'}).
            </Text>
          </>
        )}
        <Text style={s.mudo}>
          Limite não é dinheiro: é crédito que você vai pagar depois. Como regra de bolso (não é promessa), uma fatura saudável costuma ficar bem abaixo de {FATURA_SAUDAVEL_PCT}% da renda.
        </Text>
      </View>

      <View style={s.card}>
        <Text style={s.rotulo}>Meta de reserva (Cofrinho)</Text>
        {!gasto ? (
          <Text style={s.mudo}>Importe o extrato do Mercado Pago no Início para calcular seu gasto médio mensal.</Text>
        ) : (
          <>
            <Text style={s.mudo}>
              Gasto médio mensal: {brl(gasto.media)} (últimos {gasto.meses.length} {gasto.meses.length === 1 ? 'mês' : 'meses'}, com fatura paga, sem movimentos internos).
            </Text>
            {p.cofrinho === null && <Text style={s.mudo}>Informe o saldo do Cofrinho no Perfil para ver o progresso.</Text>}
            {MESES_RESERVA.map((m) => {
              const meta = metaReserva(gasto.media, m);
              const prog = p.cofrinho !== null ? progressoReserva(p.cofrinho, meta) : null;
              return (
                <View key={m} style={{ gap: 4 }}>
                  <Linha nome={`${m} meses`} valor={brl(meta)} />
                  {prog !== null && (
                    <>
                      <Barra valor={prog} cor={COR_FAIXA.ok} />
                      <Text style={s.mudo}>{pct(prog)} da meta (Cofrinho: {brl(p.cofrinho ?? 0)}).</Text>
                    </>
                  )}
                </View>
              );
            })}
            {mesesRes !== null && <Text style={s.texto}>Seu Cofrinho cobre {String(mesesRes).replace('.', ',')} meses de gasto.</Text>}
          </>
        )}
      </View>

      <View style={s.card}>
        <Text style={s.rotulo}>Cofrinho: guardar e não mexer</Text>
        {extrato.length === 0 ? (
          <Text style={s.mudo}>Importe o extrato no Início para acompanhar retiradas.</Text>
        ) : retiradas.length === 0 ? (
          <Text style={s.mudo}>Nenhuma retirada do Cofrinho no extrato importado.</Text>
        ) : (
          <>
            <Text style={[s.texto, { color: COR_FAIXA.atencao }]}>
              Você retirou {brl(retiradas[0].valor)} do Cofrinho em {dataCurta(retiradas[0].data)}.
            </Text>
            {retiradas.length > 1 && <Text style={s.mudo}>Mais {retiradas.length - 1} retirada(s) no período importado.</Text>}
          </>
        )}
      </View>

      <Text style={s.mudo}>Educativo, não é consultoria de investimentos.</Text>
    </ScrollView>
  );
}

function Linha({ nome, valor, cor, forte }: { nome: string; valor: string; cor?: string; forte?: boolean }) {
  return (
    <View style={s.linha}>
      <Text style={[s.texto, { flex: 1 }, forte ? { fontWeight: '700' } : null]}>{nome}</Text>
      <Text style={[s.texto, forte ? { fontWeight: '700' } : null, cor ? { color: cor } : null]}>{valor}</Text>
    </View>
  );
}

function Barra({ valor, cor }: { valor: number; cor: string }) {
  return (
    <View style={s.trilho}>
      <View style={[s.barra, { width: `${Math.max(0, Math.min(100, valor))}%`, backgroundColor: cor }]} />
    </View>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
  content: { padding: 20, gap: 12 },
  titulo: { color: theme.text, fontSize: 24, fontWeight: '700' },
  aviso: { color: COR_FAIXA.atencao, fontSize: 13, fontWeight: '600' },
  card: { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1, borderRadius: 10, padding: 14, gap: 8 },
  rotulo: { color: theme.muted, fontSize: 13, fontWeight: '600' },
  texto: { color: theme.text, fontSize: 15 },
  mudo: { color: theme.muted, fontSize: 12 },
  grande: { color: theme.text, fontSize: 22, fontWeight: '700' },
  link: { color: theme.tint, fontSize: 16 },
  linha: { flexDirection: 'row', gap: 8, justifyContent: 'space-between' },
  trilho: { height: 8, backgroundColor: theme.border, borderRadius: 4 },
  barra: { height: 8, borderRadius: 4 },
});
