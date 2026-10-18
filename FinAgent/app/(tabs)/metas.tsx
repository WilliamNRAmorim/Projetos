import { Link, useFocusEffect } from 'expo-router';
import { useCallback, useState } from 'react';
import { ScrollView, StyleSheet, Text } from 'react-native';
import {
  PERFIL_VAZIO, comprometidoDoMes, dataCurta, faixaLimite, livreAteSalario, mediaGastoMensal, mesesDeReserva,
  metaReserva, perfilParaNumeros, progressoReserva, retiradasCofrinho, usoLimite, type PerfilTexto,
} from '@/src/metas';
import { COR_FAIXA, FATURA_SAUDAVEL_PCT, MESES_RESERVA } from '@/src/metasConfig';
import { brl } from '@/src/mp/analise';
import { parseValorBR, saldoFinal, type Transacao } from '@/src/mp/extrato';
import { lerExtrato, lerNome } from '@/src/mp/extratoStore';
import { lerRegras } from '@/src/gastos/gastosStore';
import { REGRAS_VAZIAS, type RegrasSalvas } from '@/src/gastos/gastos';
import { lerPerfil } from '@/src/perfil';
import { metasDeCorte } from '@/src/cortes';
import { lerInicioCorte } from '@/src/cortesStore';
import { classificarExtrato } from '@/src/mp/extrato';
import {
  amostrarSerie, faixaDeParcelas, fimDoAparelho, formatarMesAno, mediaLiquidoMensal, mesesCobertos, projetarCofrinho,
  projetarConta, redirecionarParcela, simularCofrinho, taxaAnualDoProduto, taxaMensal,
} from '@/src/simulador/calc';
import { carregarCdi, dataBR, lerCdiManual, salvarCdiManual, type CdiInfo } from '@/src/simulador/cdi';
import { CampoNumero, Nota, Par } from '@/src/simulador/componentes';
import {
  BarChart, Badge, Card, InsightCard, Linha, MetricCard, ProgressBar, SectionHeader, cores, espaco, fonte,
} from '@/src/ui';

const pct = (n: number) => `${n.toFixed(1).replace('.', ',')}%`;
const dec = (n: number) => String(n).replace('.', ',');
const num = (t: string) => (t.trim() ? parseValorBR(t) : null);
const fmtCampo = (n: number | null) => (n === null ? '' : dec(n));

export default function Metas() {
  const [texto, setTexto] = useState<PerfilTexto>(PERFIL_VAZIO);
  const [extrato, setExtrato] = useState<Transacao[]>([]);
  const [nome, setNome] = useState('');
  const [regras, setRegras] = useState<RegrasSalvas>(REGRAS_VAZIAS);
  const [auto, setAuto] = useState<CdiInfo | null>(null);
  const [cdiManual, setCdiManual] = useState('');
  const [aporteTxt, setAporteTxt] = useState<string | null>(null); // null = usa a parcela do Perfil
  const [prazoTxt, setPrazoTxt] = useState('12');
  const [pctCdiTxt, setPctCdiTxt] = useState('100');
  const [inicioCorte, setInicioCorte] = useState<string | null>(null);

  useFocusEffect(
    useCallback(() => {
      (async () => {
        setTexto(await lerPerfil());
        setExtrato(await lerExtrato());
        setNome(await lerNome());
        setRegras(await lerRegras());
        setInicioCorte(await lerInicioCorte());
        const manual = await lerCdiManual();
        setCdiManual(manual);
        setAuto(await carregarCdi(num(manual)));
      })();
    }, []),
  );

  const mudarCdiManual = (v: string) => {
    setCdiManual(v);
    salvarCdiManual(v);
  };

  const p = perfilParaNumeros(texto);
  const hoje = new Date();
  const comp = comprometidoDoMes(p);
  const saldoConta = saldoFinal(extrato)?.saldo ?? null;
  const livre = saldoConta !== null ? livreAteSalario(saldoConta, p, hoje) : null;
  const uso = usoLimite(p.limiteCartao, p.faturaAberta);
  const faixa = uso !== null ? faixaLimite(uso) : null;
  const gasto = mediaGastoMensal(extrato, nome, hoje, undefined, regras);
  const retiradas = retiradasCofrinho(extrato);
  const mesAtual = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}`;
  const cortes = inicioCorte && extrato.length > 0 ? metasDeCorte(classificarExtrato(extrato, nome, regras), inicioCorte, mesAtual) : [];
  const mesesRes = mesesDeReserva(p.cofrinho, gasto?.media ?? null);

  // CDI efetivo: BC (hoje) > valor manual > cache antigo
  const manualNum = num(cdiManual);
  const cdi: CdiInfo | null =
    auto && auto.fonte === 'bcb' ? auto
    : manualNum !== null && manualNum > 0 ? { taxa: manualNum, fonte: 'manual', dataRef: null, buscadoEm: null }
    : auto;

  // Simulador
  const pctCdi = num(pctCdiTxt) ?? 0;
  const prazo = Math.max(0, Math.min(600, Math.floor(num(prazoTxt) ?? 0)));
  const aporte = num(aporteTxt ?? fmtCampo(p.parcela)) ?? 0;
  const saldoIni = p.cofrinho ?? 0;
  const sim = cdi && prazo > 0 ? simularCofrinho({ saldoInicial: saldoIni, aporte, meses: prazo, cdiAnualPct: cdi.taxa, pctCdi }) : null;
  const taxaM = cdi ? taxaMensal(taxaAnualDoProduto(cdi.taxa, pctCdi)) : null;

  // Fim do aparelho
  const faixaParc = faixaDeParcelas(p.parcelasMin, p.parcelasMax, p.parcelasRestantes);
  const fim = faixaParc ? fimDoAparelho(hoje, faixaParc, p.diaParcela) : null;

  // Se continuar assim
  const liq = mediaLiquidoMensal(extrato, nome, hoje, undefined, regras);
  const proj = liq && saldoConta !== null ? projetarConta(saldoConta, liq, hoje, p.diaSalario) : null;
  const mesesFimMes = proj ? Math.round((proj.mesesAteDezembro - (11 - hoje.getMonth())) * 100) / 100 : 0;

  const alertas: { texto: string; variante: 'alerta' | 'perigo' }[] = [];
  if (retiradas.length > 0) alertas.push({ variante: 'alerta', texto: `Você retirou ${brl(retiradas[0].valor)} do Cofrinho em ${dataCurta(retiradas[0].data)}. A meta é não mexer na reserva.` });
  if (faixa === 'alerta') alertas.push({ variante: 'perigo', texto: `Você está usando ${pct(uso!)} do limite do cartão (acima de 60%).` });
  if (comp.pctSalario !== null && comp.pctSalario > 50) alertas.push({ variante: 'perigo', texto: `${pct(comp.pctSalario)} do salário já está comprometido neste mês.` });
  if (livre && livre.valor < 0) alertas.push({ variante: 'perigo', texto: `O saldo da conta não cobre a fatura aberta e a parcela até o dia do salário (faltam ${brl(-livre.valor)}).` });
  if (p.cofrinho !== null && gasto && p.cofrinho < metaReserva(gasto.media, MESES_RESERVA[0])) {
    alertas.push({ variante: 'alerta', texto: `O Cofrinho cobre menos de ${MESES_RESERVA[0]} meses de gasto.` });
  }

  return (
    <ScrollView style={s.root} contentContainerStyle={s.content}>
      <Text style={s.titulo}>Metas</Text>
      <Badge texto="Educativo, não é consultoria de investimentos" variante="alerta" />
      <Link href="/perfil" style={s.link}>Editar perfil financeiro</Link>

      {/* 1. Reserva */}
      <SectionHeader titulo="Reserva (Cofrinho)" />
      <Card>
        {!gasto ? (
          <Nota>Importe o extrato do Mercado Pago no Início para calcular seu gasto médio mensal e o progresso da reserva.</Nota>
        ) : p.cofrinho === null ? (
          <Nota>Informe o saldo do Cofrinho no Perfil para ver o progresso.</Nota>
        ) : (
          <>
            <Linha>
              <MetricCard rotulo="Cofrinho" valor={brl(p.cofrinho)} />
              <MetricCard rotulo="Cobre" valor={mesesRes !== null ? `${dec(mesesRes)} meses` : '-'} nota="de gasto médio" />
            </Linha>
            {MESES_RESERVA.map((m) => {
              const meta = metaReserva(gasto.media, m);
              const prog = progressoReserva(p.cofrinho!, meta) ?? 0;
              return (
                <Card key={m} style={s.interno}>
                  <Par nome={`Meta de ${m} meses`} valor={brl(meta)} />
                  <ProgressBar pct={prog} cor={prog >= 100 ? cores.sucesso : cores.info} />
                  <Nota>{prog >= 100 ? 'Meta atingida.' : `${pct(prog)} da meta. Faltam ${brl(meta - p.cofrinho!)}.`}</Nota>
                </Card>
              );
            })}
            <Nota>{`Gasto médio mensal: ${brl(gasto.media)} (últimos ${gasto.meses.length} ${gasto.meses.length === 1 ? 'mês' : 'meses'}, com fatura paga, sem movimentos internos)${gasto.parcial ? ' (estimativa com mês incompleto)' : ''}.`}</Nota>
          </>
        )}
      </Card>

      {/* Alertas */}
      {alertas.map((a) => (
        <InsightCard key={a.texto} texto={a.texto} variante={a.variante} />
      ))}

      {/* Comprometido */}
      <SectionHeader titulo="Comprometido do mês" />
      <Card>
        {p.parcela === null && p.faturaAberta === null ? (
          <Nota>Preencha a parcela do aparelho e a fatura aberta no Perfil.</Nota>
        ) : (
          <>
            <Par nome="Parcela do aparelho" valor={brl(comp.parcela)} />
            <Par nome="Fatura aberta" valor={brl(comp.fatura)} />
            <Par nome="Total comprometido" valor={brl(comp.total)} forte />
            {comp.pctSalario !== null && <ProgressBar pct={comp.pctSalario} />}
            <Nota>{comp.pctSalario !== null ? `${pct(comp.pctSalario)} do salário líquido.` : 'Informe o salário no Perfil para ver o percentual.'}</Nota>
          </>
        )}
        {livre ? (
          <>
            <Par nome={`Livre até o salário (${livre.dias} dias)`} valor={brl(livre.valor)} cor={livre.valor < 0 ? COR_FAIXA.alerta : undefined} forte />
            {livre.porDia !== null && <Nota>{`Cerca de ${brl(livre.porDia)} por dia.`}</Nota>}
            <Nota>Estimativa: saldo da conta no extrato menos fatura aberta e a parte da parcela ainda não separada. Não conta o Cofrinho.</Nota>
          </>
        ) : (
          <Nota>{p.diaSalario === null ? 'Informe o dia do salário no Perfil para ver quanto está livre.' : 'Importe o extrato no Início para ver quanto está livre até o salário.'}</Nota>
        )}
      </Card>

      {/* Limite */}
      <SectionHeader titulo="Uso do limite do cartão" />
      <Card>
        {uso === null || faixa === null ? (
          <Nota>Informe o limite e o valor da fatura aberta no Perfil.</Nota>
        ) : (
          <>
            <Text style={[s.grande, { color: COR_FAIXA[faixa] }]}>{pct(uso)}</Text>
            <ProgressBar pct={uso} />
            <Nota>{`${brl(p.faturaAberta ?? 0)} de ${brl(p.limiteCartao ?? 0)} (${faixa === 'ok' ? 'ok' : faixa === 'atencao' ? 'atenção' : 'alerta'}).`}</Nota>
          </>
        )}
        <Nota>{`Limite não é dinheiro: é crédito que você vai pagar depois. Como regra de bolso (não é promessa), uma fatura saudável costuma ficar bem abaixo de ${FATURA_SAUDAVEL_PCT}% da renda.`}</Nota>
      </Card>

      {/* Retiradas */}
      <SectionHeader titulo="Cofrinho: guardar e não mexer" />
      <Card>
        {extrato.length === 0 ? (
          <Nota>Importe o extrato no Início para acompanhar retiradas.</Nota>
        ) : retiradas.length === 0 ? (
          <Nota>Nenhuma retirada do Cofrinho no extrato importado.</Nota>
        ) : (
          <>
            <Text style={[s.texto, { color: COR_FAIXA.atencao }]}>{`Você retirou ${brl(retiradas[0].valor)} do Cofrinho em ${dataCurta(retiradas[0].data)}.`}</Text>
            {retiradas.length > 1 && <Nota>{`Mais ${retiradas.length - 1} retirada(s) no período importado.`}</Nota>}
          </>
        )}
      </Card>

      {/* 2. CDI */}
      <SectionHeader titulo="CDI" />
      <Card>
        {cdi ? (
          <>
            <Text style={s.grande}>{`${dec(cdi.taxa)}% ao ano`}</Text>
            <Nota>
              {cdi.fonte === 'bcb'
                ? `Fonte: Banco Central (SGS 4389), taxa de ${cdi.dataRef ? dataBR(cdi.dataRef) : '-'}, consultada em ${cdi.buscadoEm ? dataBR(cdi.buscadoEm) : '-'}.`
                : cdi.fonte === 'manual'
                  ? 'Fonte: valor digitado por você.'
                  : `Fonte: última consulta ao Banco Central (taxa de ${cdi.dataRef ? dataBR(cdi.dataRef) : '-'}); sem internet agora, pode estar desatualizada.`}
            </Nota>
          </>
        ) : (
          <Nota>Não consegui buscar o CDI no Banco Central. Digite o valor abaixo para usar o simulador.</Nota>
        )}
        <CampoNumero rotulo="CDI manual (% ao ano), usado se a consulta falhar" valor={cdiManual} aoMudar={mudarCdiManual} sufixo="%" />
      </Card>

      {/* 3. Simulador */}
      <SectionHeader titulo="Simulador do Cofrinho" />
      <Card>
        <Par nome="Saldo inicial (do Perfil)" valor={brl(saldoIni)} />
        <CampoNumero rotulo="Aporte mensal (R$)" valor={aporteTxt ?? fmtCampo(p.parcela)} aoMudar={setAporteTxt} passo={50} />
        <CampoNumero rotulo="Prazo (meses)" valor={prazoTxt} aoMudar={setPrazoTxt} passo={1} />
        <CampoNumero rotulo="Rendimento (% do CDI)" valor={pctCdiTxt} aoMudar={setPctCdiTxt} passo={5} sufixo="%" />
        <Nota>O rendimento real depende do produto e pode ser diferente do CDI. Confira a taxa no seu Cofrinho.</Nota>
        {!sim ? (
          <Nota>{cdi ? 'Informe um prazo em meses.' : 'Sem CDI não dá para simular.'}</Nota>
        ) : (
          <>
            <Linha>
              <MetricCard rotulo="Valor líquido" valor={brl(sim.liquido)} cor={cores.sucesso} />
              <MetricCard rotulo="Rendimento bruto" valor={brl(sim.rendimentoBruto)} />
            </Linha>
            <Par nome="Total aportado" valor={brl(sim.aportado)} />
            <Par nome={`IR estimado (${dec(sim.aliquota * 100)}%)`} valor={brl(sim.ir)} />
            <Par nome="Saldo bruto final" valor={brl(sim.saldoBruto)} />
            {gasto && (
              <Text style={s.texto}>{`Isso daria cerca de ${dec(mesesCobertos(sim.liquido, gasto.media) ?? 0)} meses de reserva (gasto médio de ${brl(gasto.media)}${gasto.parcial ? ', estimativa com mês incompleto' : ''}).`}</Text>
            )}
            <BarChart
              dados={amostrarSerie(sim.serie, 12).map((x) => ({ rotulo: String(x.mes), a: saldoIni + x.aportado, b: x.saldo }))}
              rotuloA="Saldo + aportes"
              rotuloB="Saldo com rendimento"
              corA={cores.info}
              corB={cores.sucesso}
            />
            <Nota>Eixo: mês do prazo. Juros compostos mensais pela taxa equivalente ((1 + CDI x %)^(1/12) - 1), aporte no fim de cada mês.</Nota>
            <Nota>IR é estimativa: tabela regressiva de renda fixa (22,5% até 180 dias, 20% até 360, 17,5% até 720, 15% acima) aplicada pelo prazo total sobre o rendimento. Educativo, não é consultoria de investimentos.</Nota>
            <Nota>Estimativa: aportes recentes pagam alíquota maior; IOF só em resgates antes de 30 dias.</Nota>
          </>
        )}
      </Card>

      {/* 4. Fim do aparelho */}
      <SectionHeader titulo="Fim do aparelho" />
      <Card>
        {!faixaParc || !fim ? (
          <Nota>Informe as parcelas restantes (ou a faixa mínimo e máximo) no Perfil.</Nota>
        ) : !fim.de || !fim.ate ? (
          <Nota>O aparelho já está quitado.</Nota>
        ) : (
          <>
            <Text style={s.grande}>
              {fim.de.ano === fim.ate.ano && fim.de.mes === fim.ate.mes
                ? `Termina em ${formatarMesAno(fim.ate)}`
                : `Termina entre ${formatarMesAno(fim.de)} e ${formatarMesAno(fim.ate)}`}
            </Text>
            <Nota>{`Com ${faixaParc.min === faixaParc.max ? faixaParc.max : `${faixaParc.min} a ${faixaParc.max}`} parcelas restantes, contando a deste mês.`}</Nota>
            {p.parcela !== null && taxaM !== null ? (
              <>
                <Text style={s.rotulo}>Se a parcela passar a ir para o Cofrinho depois do fim (12 meses)</Text>
                {[...new Set([faixaParc.min, faixaParc.max])].map((n) => {
                  const r = redirecionarParcela({ saldoInicial: saldoIni, parcela: p.parcela!, mesesAteFim: n, taxaMensal: taxaM });
                  return (
                    <Card key={n} style={s.interno}>
                      <Par nome={`Se terminar em ${formatarMesAno(n === faixaParc.min ? fim.de! : fim.ate!)}`} valor={`${n} parcelas`} />
                      <Par nome="Cofrinho no fim do aparelho" valor={brl(r.saldoNoFim)} />
                      <Par nome={`Mais 12 aportes de ${brl(p.parcela!)} (bruto)`} valor={brl(r.depois.saldoBruto)} forte />
                      <Nota>{`Valor bruto, antes do IR, depois de 12 meses (aportado ${brl(r.depois.aportado)}, rendimento bruto ${brl(r.depois.rendimentoBruto)}).`}</Nota>
                    </Card>
                  );
                })}
                <Nota>Cenário, não promessa: usa o CDI e o % do CDI do simulador acima.</Nota>
              </>
            ) : (
              <Nota>Informe a parcela no Perfil e o CDI para ver o cenário de redirecionar a parcela ao Cofrinho.</Nota>
            )}
          </>
        )}
      </Card>

      {/* Corte de gastos */}
      <SectionHeader titulo="Corte de gastos (Uber, 99 e iFood)" />
      <Card>
        {cortes.length === 0 ? (
          <Nota>Importe o extrato e as faturas do cartão para calcular a base do corte.</Nota>
        ) : (
          <>
            {cortes.map((c) => (
              <Card key={c.grupo.id} style={s.interno}>
                <Text style={s.rotulo}>{c.grupo.nome}</Text>
                {c.base === null || c.teto === null ? (
                  <Nota>Sem gasto nos meses anteriores ao plano para calcular a base.</Nota>
                ) : (
                  <>
                    <Linha>
                      <MetricCard rotulo="Gasto no mês" valor={brl(c.gasto)} cor={c.faixa === 'estourou' ? cores.perigo : c.faixa === 'atencao' ? cores.alerta : cores.sucesso} />
                      <MetricCard rotulo={`Teto (-${c.degrau}%)`} valor={brl(c.teto)} nota={`base ${brl(c.base)}`} />
                    </Linha>
                    {c.pct !== null && <ProgressBar pct={c.pct} cor={c.faixa === 'estourou' ? cores.perigo : c.faixa === 'atencao' ? cores.alerta : cores.sucesso} />}
                    <Text style={s.texto}>
                      {c.faixa === 'estourou' ? `Passou ${brl(c.gasto - c.teto)} do teto.` : `Ainda cabem ${brl(c.teto - c.gasto)} neste mês.`}
                    </Text>
                    <Nota>{`Mês que vem: teto de ${brl(c.proximoTeto ?? 0)} (-${c.proximoDegrau}%).`}</Nota>
                  </>
                )}
              </Card>
            ))}
            <Nota>{`Corte progressivo a partir de ${inicioCorte}: -10% no 1º mês, -20% no 2º, -30% no 3º, depois mantém. A base é a média dos 3 meses anteriores. O mês atual só inclui o cartão depois de importar a fatura dele.`}</Nota>
          </>
        )}
      </Card>

      {/* 5. Se continuar assim */}
      <SectionHeader titulo="Se continuar assim" />
      <Card>
        {!liq || saldoConta === null || !proj ? (
          <Nota>Importe o extrato com pelo menos um mês fechado no Início para ver a projeção.</Nota>
        ) : (
          <>
            <Text style={s.texto}>
              {`Se o padrão dos últimos ${liq.meses.length} ${liq.meses.length === 1 ? 'mês fechado' : 'meses fechados'} se repetir, sobra em média ${brl(liq.media)} por mês (entradas menos gastos e fatura, sem movimento interno).`}
            </Text>
            <Linha>
              <MetricCard rotulo="Conta no fim do mês" valor={brl(proj.fimDoMes)} nota="projeção da conta" />
              <MetricCard rotulo="Conta em dezembro" valor={brl(proj.dezembro)} nota="projeção da conta" />
            </Linha>
            {p.cofrinho !== null && taxaM !== null && (
              <Linha>
                <MetricCard rotulo="Cofrinho no fim do mês" valor={brl(projetarCofrinho(p.cofrinho, taxaM, mesesFimMes))} nota="só rendimento, bruto" />
                <MetricCard rotulo="Cofrinho em dezembro" valor={brl(projetarCofrinho(p.cofrinho, taxaM, proj.mesesAteDezembro))} nota="só rendimento, bruto" />
              </Linha>
            )}
            <Nota>{`A projeção é da conta, sem o Cofrinho (a reserva fica fora do saldo do extrato). Parte do saldo do extrato; ${proj.salarioPendente ? 'o salário (menos a fatura, paga no mesmo dia) ainda vai cair neste mês e entra inteiro' : 'o salário deste mês já caiu e não entra de novo'}; os gastos do dia a dia entram proporcionais ao tempo que falta. O Cofrinho não recebe aportes (meta: não mexer) e rende pelo CDI e % do simulador, valor bruto, antes do IR. Estimativa, não promessa.`}</Nota>
          </>
        )}
      </Card>

      <Nota>Educativo, não é consultoria de investimentos.</Nota>
    </ScrollView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: cores.fundo },
  content: { padding: espaco.lg, gap: espaco.md, paddingBottom: espaco.xl * 2 },
  titulo: { color: cores.texto, fontSize: fonte.numero, fontWeight: '700' },
  link: { color: cores.primaria, fontSize: 16 },
  interno: { backgroundColor: cores.superficie2, padding: espaco.md },
  texto: { color: cores.texto, fontSize: fonte.corpo },
  rotulo: { color: cores.texto2, fontSize: fonte.pequena, fontWeight: '600' },
  grande: { color: cores.texto, fontSize: fonte.numero, fontWeight: '700' },
});
