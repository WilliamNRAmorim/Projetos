import { useState } from 'react';
import { Modal, Pressable, StyleSheet, Text, View } from 'react-native';
import { Botao, cores, espaco, fonte, raio } from '@/src/ui';
import { CATEGORIAS_GASTO } from './gastos';

type Props = {
  titulo: string;
  atual: string;
  temContraparte: boolean;
  aoSalvar: (categoria: string, soEsta: boolean) => void;
  aoFechar: () => void;
};

/** Escolha de categoria para uma transação. Mostra a opção "só esta" quando há contraparte. */
export function ModalCategoria({ titulo, atual, temContraparte, aoSalvar, aoFechar }: Props) {
  const [sel, setSel] = useState(atual);
  const [soEsta, setSoEsta] = useState(!temContraparte);
  const lista = CATEGORIAS_GASTO.includes(atual) ? CATEGORIAS_GASTO : [atual, ...CATEGORIAS_GASTO];
  return (
    <Modal transparent animationType="slide" onRequestClose={aoFechar}>
      <Pressable style={s.fundo} onPress={aoFechar}>
        <Pressable style={s.painel} onPress={() => {}}>
          <Text style={s.titulo} numberOfLines={2}>{titulo}</Text>
          <View style={s.lista}>
            {lista.map((c) => (
              <Pressable key={c} onPress={() => setSel(c)} style={[s.item, sel === c ? s.itemSel : null]}>
                <Text style={[s.itemTxt, sel === c ? { color: cores.primaria } : null]}>{c}</Text>
              </Pressable>
            ))}
          </View>
          {temContraparte && (
            <Pressable onPress={() => setSoEsta(!soEsta)} style={s.opcao}>
              <View style={[s.caixa, soEsta ? s.caixaOn : null]} />
              <Text style={s.opcaoTxt}>Aplicar só nesta transação</Text>
            </Pressable>
          )}
          {temContraparte && !soEsta && <Text style={s.dica}>Vale para todas as transações com a mesma contraparte.</Text>}
          <View style={s.botoes}>
            <View style={{ flex: 1 }}><Botao texto="Cancelar" secundario aoPressionar={aoFechar} /></View>
            <View style={{ flex: 1 }}><Botao texto="Salvar" aoPressionar={() => aoSalvar(sel, soEsta)} /></View>
          </View>
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const s = StyleSheet.create({
  fundo: { flex: 1, backgroundColor: '#000a', justifyContent: 'flex-end' },
  painel: { backgroundColor: cores.superficie, borderTopLeftRadius: raio.lg, borderTopRightRadius: raio.lg, padding: espaco.lg, gap: espaco.md },
  titulo: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700' },
  lista: { flexDirection: 'row', flexWrap: 'wrap', gap: espaco.sm },
  item: { borderWidth: 1, borderColor: cores.borda, borderRadius: raio.pill, paddingHorizontal: 12, paddingVertical: 8 },
  itemSel: { borderColor: cores.primaria },
  itemTxt: { color: cores.texto, fontSize: fonte.corpo },
  opcao: { flexDirection: 'row', alignItems: 'center', gap: espaco.sm },
  caixa: { width: 20, height: 20, borderRadius: 4, borderWidth: 1, borderColor: cores.texto2 },
  caixaOn: { backgroundColor: cores.primaria, borderColor: cores.primaria },
  opcaoTxt: { color: cores.texto, fontSize: fonte.corpo },
  dica: { color: cores.texto2, fontSize: fonte.pequena },
  botoes: { flexDirection: 'row', gap: espaco.sm },
});
