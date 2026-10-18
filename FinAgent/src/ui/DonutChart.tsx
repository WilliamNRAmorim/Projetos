import { ReactNode } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, G } from 'react-native-svg';
import { cores, espaco, fonte } from './tokens';

export type FatiaDonut = { rotulo: string; valor: number; cor: string; texto?: string };

/** Rosca proporcional aos valores (>0). `centro` é desenhado no meio (ex.: total). Legenda opcional ao lado/abaixo. */
export function DonutChart({
  fatias, tamanho = 140, espessura = 18, centro, legenda = true,
}: { fatias: FatiaDonut[]; tamanho?: number; espessura?: number; centro?: ReactNode; legenda?: boolean }) {
  const ativas = fatias.filter((f) => f.valor > 0);
  const total = ativas.reduce((a, f) => a + f.valor, 0);
  const r = (tamanho - espessura) / 2;
  const circ = 2 * Math.PI * r;
  let acumulado = 0;
  return (
    <View style={s.raiz}>
      <View style={{ width: tamanho, height: tamanho }}>
        <Svg width={tamanho} height={tamanho}>
          <G rotation={-90} origin={`${tamanho / 2}, ${tamanho / 2}`}>
            <Circle cx={tamanho / 2} cy={tamanho / 2} r={r} stroke={cores.borda} strokeWidth={espessura} fill="none" />
            {total > 0 && ativas.map((f) => {
              const parte = (f.valor / total) * circ;
              const el = (
                <Circle
                  key={f.rotulo}
                  cx={tamanho / 2}
                  cy={tamanho / 2}
                  r={r}
                  stroke={f.cor}
                  strokeWidth={espessura}
                  fill="none"
                  strokeDasharray={`${Math.max(0, parte - 1)} ${circ - Math.max(0, parte - 1)}`}
                  strokeDashoffset={-acumulado}
                />
              );
              acumulado += parte;
              return el;
            })}
          </G>
        </Svg>
        {centro ? <View style={s.centro} pointerEvents="none">{centro}</View> : null}
      </View>
      {legenda && (
        <View style={s.legenda}>
          {fatias.map((f) => (
            <View key={f.rotulo} style={s.item}>
              <View style={[s.ponto, { backgroundColor: f.cor }]} />
              <Text style={s.txt} numberOfLines={1}>{f.rotulo}{f.texto ? ` · ${f.texto}` : ''}</Text>
            </View>
          ))}
        </View>
      )}
    </View>
  );
}

const s = StyleSheet.create({
  raiz: { flexDirection: 'row', alignItems: 'center', gap: espaco.lg, flexWrap: 'wrap' },
  centro: { ...StyleSheet.absoluteFill as object, alignItems: 'center', justifyContent: 'center' },
  legenda: { flex: 1, minWidth: 120, gap: 6 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  ponto: { width: 8, height: 8, borderRadius: 4 },
  txt: { color: cores.texto2, fontSize: fonte.pequena, flexShrink: 1 },
});
