import { ComponentProps, ReactNode } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Card } from './Card';
import { cores, corDaVariante, espaco, fonte, raio, type Variante } from './tokens';

type Icone = ComponentProps<typeof Ionicons>['name'];

/** Título de seção, com ação opcional à direita (ex.: "Ver tudo"). */
export function SectionHeader({ titulo, acao, aoAcao }: { titulo: string; acao?: string; aoAcao?: () => void }) {
  return (
    <View style={s.secao}>
      <Text style={s.secaoTxt}>{titulo}</Text>
      {acao ? <Pressable onPress={aoAcao} hitSlop={8}><Text style={s.acao}>{acao}</Text></Pressable> : null}
    </View>
  );
}

/** Etiqueta pequena colorida. */
export function Badge({ texto, variante = 'info' }: { texto: string; variante?: Variante }) {
  const cor = corDaVariante[variante];
  return (
    <View style={[s.badge, { borderColor: cor }]}>
      <Text style={[s.badgeTxt, { color: cor }]}>{texto}</Text>
    </View>
  );
}

const ICONE_PADRAO: Record<Variante, Icone> = {
  info: 'information-circle', alerta: 'warning', sucesso: 'checkmark-circle', perigo: 'alert-circle',
};

/** Card com ícone + texto curto. */
export function InsightCard({ texto, variante = 'info', icone }: { texto: string; variante?: Variante; icone?: Icone }) {
  const cor = corDaVariante[variante];
  return (
    <Card style={s.insight}>
      <Ionicons name={icone ?? ICONE_PADRAO[variante]} size={20} color={cor} />
      <Text style={s.insightTxt}>{texto}</Text>
    </Card>
  );
}

/** Estado vazio com ícone, texto e botão opcional. */
export function EmptyState({
  icone = 'file-tray-outline', titulo, texto, botao, aoBotao,
}: { icone?: Icone; titulo: string; texto?: string; botao?: string; aoBotao?: () => void }) {
  return (
    <Card style={s.vazio}>
      <Ionicons name={icone} size={36} color={cores.texto2} />
      <Text style={s.vazioTitulo}>{titulo}</Text>
      {texto ? <Text style={s.vazioTxt}>{texto}</Text> : null}
      {botao ? <Botao texto={botao} aoPressionar={aoBotao} /> : null}
    </Card>
  );
}

/** Botão. `secundario` = contorno. */
export function Botao({
  texto, aoPressionar, secundario, icone, desabilitado,
}: { texto: string; aoPressionar?: () => void; secundario?: boolean; icone?: Icone; desabilitado?: boolean }) {
  const cor = secundario ? cores.texto : cores.fundo;
  return (
    <Pressable
      onPress={aoPressionar}
      disabled={desabilitado}
      style={[s.botao, secundario ? s.botaoSec : s.botaoPri, desabilitado ? { opacity: 0.5 } : null]}>
      {icone ? <Ionicons name={icone} size={16} color={cor} /> : null}
      <Text style={[s.botaoTxt, { color: cor }]}>{texto}</Text>
    </Pressable>
  );
}

/** Linha de itens lado a lado (ex.: MetricCards). */
export function Linha({ children }: { children: ReactNode }) {
  return <View style={{ flexDirection: 'row', gap: espaco.sm }}>{children}</View>;
}

const s = StyleSheet.create({
  secao: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'baseline', marginTop: espaco.sm },
  secaoTxt: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700' },
  acao: { color: cores.primaria, fontSize: fonte.corpo },
  badge: { alignSelf: 'flex-start', borderWidth: 1, borderRadius: raio.pill, paddingHorizontal: 8, paddingVertical: 2 },
  badgeTxt: { fontSize: 11, fontWeight: '600' },
  insight: { flexDirection: 'row', alignItems: 'center', gap: espaco.md, padding: espaco.md },
  insightTxt: { flex: 1, color: cores.texto, fontSize: fonte.corpo, lineHeight: 20 },
  vazio: { alignItems: 'center', gap: espaco.md, paddingVertical: espaco.xl },
  vazioTitulo: { color: cores.texto, fontSize: fonte.titulo, fontWeight: '700', textAlign: 'center' },
  vazioTxt: { color: cores.texto2, fontSize: fonte.corpo, textAlign: 'center', lineHeight: 20 },
  botao: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, borderRadius: raio.md, paddingVertical: 12, paddingHorizontal: espaco.lg },
  botaoPri: { backgroundColor: cores.primaria },
  botaoSec: { borderWidth: 1, borderColor: cores.borda, backgroundColor: cores.superficie },
  botaoTxt: { fontSize: fonte.corpo, fontWeight: '700' },
});
