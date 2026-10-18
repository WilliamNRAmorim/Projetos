import { ReactNode } from 'react';
import { ScrollView, StyleSheet, Text } from 'react-native';
import { theme } from './theme';

export function Tela({ titulo, texto, children }: { titulo: string; texto?: string; children?: ReactNode }) {
  return (
    <ScrollView style={s.root} contentContainerStyle={s.content}>
      <Text style={s.titulo}>{titulo}</Text>
      {texto ? <Text style={s.texto}>{texto}</Text> : null}
      {children}
    </ScrollView>
  );
}

const s = StyleSheet.create({
  root: { flex: 1, backgroundColor: theme.bg },
  content: { padding: 20, gap: 12 },
  titulo: { color: theme.text, fontSize: 24, fontWeight: '700' },
  texto: { color: theme.muted, fontSize: 15, lineHeight: 22 },
});
