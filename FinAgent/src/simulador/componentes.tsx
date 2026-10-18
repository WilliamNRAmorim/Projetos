// Peças de tela usadas só pelas Metas (sobre os tokens de src/ui).
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { cores, espaco, fonte, raio } from '@/src/ui';

/** Linha "nome ........ valor". */
export function Par({ nome, valor, cor, forte }: { nome: string; valor: string; cor?: string; forte?: boolean }) {
  return (
    <View style={s.par}>
      <Text style={[s.txt, { flex: 1 }, forte ? s.forte : null]}>{nome}</Text>
      <Text style={[s.txt, forte ? s.forte : null, cor ? { color: cor } : null]}>{valor}</Text>
    </View>
  );
}

export const Nota = ({ children }: { children: string }) => <Text style={s.nota}>{children}</Text>;

/** Campo numérico com rótulo e, opcionalmente, botões - e +. */
export function CampoNumero({
  rotulo, valor, aoMudar, passo, sufixo,
}: { rotulo: string; valor: string; aoMudar: (v: string) => void; passo?: number; sufixo?: string }) {
  const ajustar = (delta: number) => {
    const n = Number(valor.replace(/\./g, '').replace(',', '.'));
    const base = Number.isFinite(n) ? n : 0;
    aoMudar(String(Math.max(0, Math.round((base + delta) * 100) / 100)).replace('.', ','));
  };
  return (
    <View style={{ gap: espaco.xs }}>
      <Text style={s.rotulo}>{rotulo}</Text>
      <View style={s.campo}>
        {passo ? <Botaozinho texto="-" aoPressionar={() => ajustar(-passo)} /> : null}
        <TextInput
          style={s.input}
          value={valor}
          onChangeText={aoMudar}
          keyboardType="decimal-pad"
          placeholder="0"
          placeholderTextColor={cores.texto2}
        />
        {sufixo ? <Text style={s.rotulo}>{sufixo}</Text> : null}
        {passo ? <Botaozinho texto="+" aoPressionar={() => ajustar(passo)} /> : null}
      </View>
    </View>
  );
}

function Botaozinho({ texto, aoPressionar }: { texto: string; aoPressionar: () => void }) {
  return (
    <Pressable onPress={aoPressionar} style={s.btn} hitSlop={6}>
      <Text style={s.btnTxt}>{texto}</Text>
    </Pressable>
  );
}

const s = StyleSheet.create({
  par: { flexDirection: 'row', gap: espaco.sm, justifyContent: 'space-between' },
  txt: { color: cores.texto, fontSize: fonte.corpo },
  forte: { fontWeight: '700' },
  nota: { color: cores.texto2, fontSize: fonte.pequena },
  rotulo: { color: cores.texto2, fontSize: fonte.pequena },
  campo: { flexDirection: 'row', alignItems: 'center', gap: espaco.sm },
  input: {
    flex: 1, backgroundColor: cores.fundo, color: cores.texto, borderColor: cores.borda, borderWidth: 1,
    borderRadius: raio.sm, paddingHorizontal: espaco.md, paddingVertical: espaco.sm, fontSize: fonte.corpo,
  },
  btn: {
    width: 40, height: 40, borderRadius: raio.sm, backgroundColor: cores.superficie2, borderColor: cores.borda,
    borderWidth: 1, alignItems: 'center', justifyContent: 'center',
  },
  btnTxt: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700' },
});
