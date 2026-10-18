import { StyleSheet, Text, View } from 'react-native';
import { cores, espaco, fonte, raio } from './tokens';

/** Rótulo pequeno em cima, número grande embaixo, nota opcional. Pensado para ficar em linha (flex: 1). */
export function MetricCard({ rotulo, valor, nota, cor }: { rotulo: string; valor: string; nota?: string; cor?: string }) {
  return (
    <View style={s.card}>
      <Text style={s.rotulo} numberOfLines={1}>{rotulo}</Text>
      <Text style={[s.valor, cor ? { color: cor } : null]} numberOfLines={1} adjustsFontSizeToFit>{valor}</Text>
      {nota ? <Text style={s.nota} numberOfLines={2}>{nota}</Text> : null}
    </View>
  );
}

const s = StyleSheet.create({
  card: { flex: 1, backgroundColor: cores.superficie, borderColor: cores.borda, borderWidth: 1, borderRadius: raio.md, padding: espaco.md, gap: 2 },
  rotulo: { color: cores.texto2, fontSize: fonte.pequena },
  valor: { color: cores.texto, fontSize: fonte.numero, fontWeight: '700' },
  nota: { color: cores.texto2, fontSize: 11 },
});
