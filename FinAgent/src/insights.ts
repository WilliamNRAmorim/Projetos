// Insights e alertas do Início: funções puras (sem React Native), regras simples e texto factual.
import { CAT } from './mp/categorias.ts';
import { mesAnteriorDe, mesesDisponiveis, totaisMes, type Lancamento, type Transacao } from './mp/extrato.ts';
import { comprometidoDoMes, dataCurta, faixaLimite, livreAteSalario, retiradasCofrinho, usoLimite, type PerfilNum } from './metas.ts';

export type TipoInsight = 'info' | 'alerta' | 'sucesso';
export type Insight = { id: string; tipo: TipoInsight; icone: string; texto: string; prioridade: number };

const NOMES_MES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
export const nomeMes = (mes: string) => NOMES_MES[Number(mes.slice(5, 7)) - 1] ?? mes;
export const chaveMesDe = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;

const fmt = (v: number) => `R$ ${v.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
const pct = (n: number) => `${Math.abs(n).toFixed(0)}%`;
const dia = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

export type EntradaInsights = { trans: Transacao[]; lancs: Lancamento[]; perfil: PerfilNum; hoje: Date };

function gastoPorCat(lancs: Lancamento[], mes: string): Map<string, number> {
  const m = new Map<string, number>();
  for (const x of totaisMes(lancs, mes).porCategoria) m.set(x.nome, x.total);
  return m;
}

/** Até 4 insights ordenados por prioridade (menor = mais importante). */
export function gerarInsights(e: EntradaInsights, max = 4): Insight[] {
  const { trans, lancs, perfil, hoje } = e;
  const lista: Insight[] = [];
  const meses = mesesDisponiveis(trans); // mais recente primeiro
  if (meses.length === 0) return lista;
  const atualChave = chaveMesDe(hoje);
  const ref = meses.includes(atualChave) ? atualChave : meses[0];
  const ant = mesAnteriorDe(ref);

  // 1. Retirada do Cofrinho nos últimos 30 dias
  const ret = retiradasCofrinho(trans)[0];
  if (ret) {
    const idade = Math.round((dia(hoje).getTime() - new Date(`${ret.data}T00:00:00`).getTime()) / 86400000);
    if (idade >= 0 && idade <= 30) {
      lista.push({ id: 'cofrinho', tipo: 'alerta', icone: 'wallet', prioridade: 1, texto: `Retirada de ${fmt(ret.valor)} do Cofrinho em ${dataCurta(ret.data)}.` });
    }
  }

  // 2. Fatura paga no mês vs mês anterior
  const tRef = totaisMes(lancs, ref);
  const tAnt = totaisMes(lancs, ant);
  if (tRef.fatura > 0 && tAnt.fatura > 0) {
    const v = ((tRef.fatura - tAnt.fatura) / tAnt.fatura) * 100;
    const base = `Fatura paga em ${nomeMes(ref)}: ${fmt(tRef.fatura)}`;
    if (Math.abs(v) >= 5) {
      lista.push({
        id: 'fatura', tipo: v > 0 ? 'alerta' : 'sucesso', icone: 'card', prioridade: 2,
        texto: `${base}, ${pct(v)} ${v > 0 ? 'a mais' : 'a menos'} que em ${nomeMes(ant)}.`,
      });
    } else {
      lista.push({ id: 'fatura', tipo: 'info', icone: 'card', prioridade: 4, texto: `${base}, parecida com ${nomeMes(ant)}.` });
    }
  } else if (tRef.fatura > 0 && perfil.salario && perfil.salario > 0) {
    lista.push({ id: 'fatura', tipo: 'info', icone: 'card', prioridade: 4, texto: `Fatura paga em ${nomeMes(ref)}: ${fmt(tRef.fatura)}, ${pct((tRef.fatura / perfil.salario) * 100)} do salário.` });
  }

  // 3. Maior categoria do mês
  const top = tRef.porCategoria[0];
  if (top && tRef.gastos > 0) {
    lista.push({
      id: 'maior', tipo: 'info', icone: 'pie-chart', prioridade: 3,
      texto: `Maior gasto de ${nomeMes(ref)}${ref === atualChave ? ' até agora' : ''}: ${top.nome}, ${fmt(top.total)} (${pct((top.total / tRef.gastos) * 100)} dos gastos).`,
    });
  }

  // 4. Categoria que mais cresceu/caiu entre os dois últimos meses fechados
  const fechados = meses.filter((m) => m < atualChave);
  if (fechados.length >= 2 && fechados[1] === mesAnteriorDe(fechados[0])) {
    const novo = gastoPorCat(lancs, fechados[0]);
    const velho = gastoPorCat(lancs, fechados[1]);
    let melhor: { nome: string; dif: number } | null = null;
    for (const nome of new Set([...novo.keys(), ...velho.keys()])) {
      const dif = (novo.get(nome) ?? 0) - (velho.get(nome) ?? 0);
      if (Math.abs(dif) >= 30 && (!melhor || Math.abs(dif) > Math.abs(melhor.dif))) melhor = { nome, dif };
    }
    if (melhor) {
      const sobe = melhor.dif > 0;
      lista.push({
        id: 'variacao', tipo: sobe ? 'alerta' : 'sucesso', icone: sobe ? 'trending-up' : 'trending-down', prioridade: 3,
        texto: `${melhor.nome} ${sobe ? 'subiu' : 'caiu'} ${fmt(Math.abs(melhor.dif))} de ${nomeMes(fechados[1])} para ${nomeMes(fechados[0])}.`,
      });
    }
  }

  // 5. Dias sem gasto com delivery
  const datasDelivery = lancs
    .filter((l) => l.categoria === CAT.COMIDA && l.valor < 0 && !l.excluida && l.data <= isoDe(hoje))
    .map((l) => l.data)
    .sort();
  if (datasDelivery.length > 0) {
    const ultima = datasDelivery[datasDelivery.length - 1];
    const dias = Math.round((dia(hoje).getTime() - new Date(`${ultima}T00:00:00`).getTime()) / 86400000);
    if (dias >= 3) {
      lista.push({ id: 'delivery', tipo: 'sucesso', icone: 'restaurant', prioridade: 5, texto: `${dias} dias sem gasto com comida/delivery.` });
    }
  }

  return lista.sort((a, b) => a.prioridade - b.prioridade).slice(0, max);
}

function isoDe(d: Date): string {
  return `${chaveMesDe(d)}-${String(d.getDate()).padStart(2, '0')}`;
}

/** Alertas do sino: condições que pedem atenção, em texto curto. */
export function alertasDoInicio(e: { trans: Transacao[]; perfil: PerfilNum; saldoConta: number | null; hoje: Date }): string[] {
  const { trans, perfil, saldoConta, hoje } = e;
  const out: string[] = [];
  const ret = retiradasCofrinho(trans)[0];
  if (ret) {
    const idade = Math.round((dia(hoje).getTime() - new Date(`${ret.data}T00:00:00`).getTime()) / 86400000);
    if (idade >= 0 && idade <= 30) out.push(`Retirada de ${fmt(ret.valor)} do Cofrinho em ${dataCurta(ret.data)}.`);
  }
  const uso = usoLimite(perfil.limiteCartao, perfil.faturaAberta);
  if (uso !== null && faixaLimite(uso) === 'alerta') out.push(`Limite do cartão em ${uso.toFixed(0)}%.`);
  const comp = comprometidoDoMes(perfil);
  if (comp.pctSalario !== null && comp.pctSalario > 50) out.push(`${comp.pctSalario.toFixed(0)}% do salário comprometido.`);
  if (saldoConta !== null) {
    const livre = livreAteSalario(saldoConta, perfil, hoje);
    if (livre && livre.valor < 0) out.push(`Saldo não cobre fatura e parcela até o salário (faltam ${fmt(-livre.valor)}).`);
  }
  return out;
}

/** Série do gráfico Entrou x Saiu: últimos `n` meses, do mais antigo ao mais novo. Saiu = gastos + fatura. */
export function serieEntrouSaiu(lancs: Lancamento[], trans: Transacao[], n = 6): { mes: string; entrou: number; saiu: number }[] {
  return mesesDisponiveis(trans)
    .slice(0, n)
    .reverse()
    .map((mes) => {
      const t = totaisMes(lancs, mes);
      return { mes, entrou: t.entradas, saiu: Math.round((t.gastos + t.fatura) * 100) / 100 };
    });
}
