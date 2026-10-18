import { ReactNode } from 'react';
import { StyleProp, StyleSheet, View, ViewStyle } from 'react-native';
import { cores, espaco, raio } from './tokens';

export function Card({ children, style, borda }: { children: ReactNode; style?: StyleProp<ViewStyle>; borda?: string }) {
  return <View style={[s.card, borda ? { borderColor: borda } : null, style]}>{children}</View>;
}

const s = StyleSheet.create({
  card: { backgroundColor: cores.superficie, borderColor: cores.borda, borderWidth: 1, borderRadius: raio.lg, padding: espaco.lg, gap: espaco.sm },
});
