import { StyleSheet, View } from 'react-native';
import { cores } from './tokens';

export type Faixas = { ate: number; cor: string }[];

/** Padrão: verde até 30%, amarelo até 60%, vermelho acima (mesma regra do limite do cartão). */
export const FAIXAS_PADRAO: Faixas = [
  { ate: 30, cor: cores.sucesso },
  { ate: 60, cor: cores.alerta },
  { ate: Infinity, cor: cores.perigo },
];

export function corDaFaixa(pct: number, faixas: Faixas = FAIXAS_PADRAO): string {
  return (faixas.find((f) => pct <= f.ate) ?? faixas[faixas.length - 1]).cor;
}

/** pct de 0 a 100. `cor` fixa ignora as faixas. */
export function ProgressBar({ pct, cor, faixas, altura = 8 }: { pct: number; cor?: string; faixas?: Faixas; altura?: number }) {
  const p = Math.max(0, Math.min(100, Number.isFinite(pct) ? pct : 0));
  return (
    <View style={[s.trilho, { height: altura, borderRadius: altura / 2 }]}>
      <View style={{ width: `${p}%`, height: '100%', borderRadius: altura / 2, backgroundColor: cor ?? corDaFaixa(p, faixas) }} />
    </View>
  );
}

const s = StyleSheet.create({ trilho: { backgroundColor: cores.borda, overflow: 'hidden' } });
