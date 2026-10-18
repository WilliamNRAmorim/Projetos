import { useState } from 'react';
import { LayoutChangeEvent, StyleSheet, Text, View } from 'react-native';
import Svg, { G, Rect, Text as SvgText } from 'react-native-svg';
import { cores, espaco, fonte } from './tokens';

export type ParBarras = { rotulo: string; a: number; b: number };

/** Pares de barras por rótulo (ex.: mês). `a` = primeira série (entrou), `b` = segunda (saiu). */
export function BarChart({
  dados, rotuloA, rotuloB, corA = cores.sucesso, corB = cores.perigo, altura = 140,
}: { dados: ParBarras[]; rotuloA: string; rotuloB: string; corA?: string; corB?: string; altura?: number }) {
  const [largura, setLargura] = useState(0);
  const aoMedir = (e: LayoutChangeEvent) => setLargura(e.nativeEvent.layout.width);
  const max = Math.max(1, ...dados.flatMap((d) => [d.a, d.b]));
  const area = altura - 20; // espaço dos rótulos embaixo
  const faixa = dados.length > 0 ? largura / dados.length : 0;
  const larg = Math.max(4, Math.min(22, faixa / 3));

  return (
    <View style={{ gap: espaco.sm }}>
      <View onLayout={aoMedir} style={{ height: altura }}>
        {largura > 0 && (
          <Svg width={largura} height={altura}>
            {dados.map((d, i) => {
              const x0 = i * faixa + faixa / 2;
              const ha = (Math.max(0, d.a) / max) * area;
              const hb = (Math.max(0, d.b) / max) * area;
              return (
                <G key={d.rotulo}>
                  <Rect x={x0 - larg - 1} y={area - ha} width={larg} height={ha} rx={3} fill={corA} />
                  <Rect x={x0 + 1} y={area - hb} width={larg} height={hb} rx={3} fill={corB} />
                  <SvgText x={x0} y={altura - 4} fontSize={11} fill={cores.texto2} textAnchor="middle">{d.rotulo}</SvgText>
                </G>
              );
            })}
          </Svg>
        )}
      </View>
      <View style={s.legenda}>
        <Item cor={corA} txt={rotuloA} />
        <Item cor={corB} txt={rotuloB} />
      </View>
    </View>
  );
}

function Item({ cor, txt }: { cor: string; txt: string }) {
  return (
    <View style={s.item}>
      <View style={[s.ponto, { backgroundColor: cor }]} />
      <Text style={s.txt}>{txt}</Text>
    </View>
  );
}

const s = StyleSheet.create({
  legenda: { flexDirection: 'row', gap: espaco.lg },
  item: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  ponto: { width: 8, height: 8, borderRadius: 4 },
  txt: { color: cores.texto2, fontSize: fonte.pequena },
});
