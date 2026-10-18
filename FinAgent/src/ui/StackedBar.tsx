import { StyleSheet, Text, View } from 'react-native';
import { cores, espaco, fonte } from './tokens';

export type Segmento = { rotulo: string; valor: number; cor: string; texto?: string };

/** Barra segmentada proporcional aos valores (>0), com legenda embaixo. `texto` é o valor já formatado da legenda. */
export function StackedBar({ segmentos, altura = 14 }: { segmentos: Segmento[]; altura?: number }) {
  const ativos = segmentos.filter((x) => x.valor > 0);
  const total = ativos.reduce((a, x) => a + x.valor, 0);
  return (
    <View style={{ gap: espaco.sm }}>
      <View style={[s.trilho, { height: altura, borderRadius: altura / 2 }]}>
        {total > 0 && ativos.map((x) => <View key={x.rotulo} style={{ flex: x.valor / total, backgroundColor: x.cor }} />)}
      </View>
      <View style={s.legenda}>
        {segmentos.map((x) => (
          <View key={x.rotulo} style={s.item}>
            <View style={[s.ponto, { backgroundColor: x.cor }]} />
            <Text style={s.txt}>{x.rotulo}{x.texto ? ` · ${x.texto}` : ''}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}

const s = StyleSheet.create({
  trilho: { flexDirection: 'row', backgroundColor: cores.borda, overflow: 'hidden', gap: 2 },
  legenda: { flexDirection: 'row', flexWrap: 'wrap', columnGap: espaco.md, rowGap: 4 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  ponto: { width: 8, height: 8, borderRadius: 4 },
  txt: { color: cores.texto2, fontSize: fonte.pequena },
});
