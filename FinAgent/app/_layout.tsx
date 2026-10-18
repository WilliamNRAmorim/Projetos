import { DarkTheme, Stack, ThemeProvider } from 'expo-router';
import { theme } from '@/src/theme';

export { ErrorBoundary } from 'expo-router';

const navTheme = {
  ...DarkTheme,
  colors: { ...DarkTheme.colors, background: theme.bg, card: theme.card, text: theme.text, primary: theme.tint, border: theme.border },
};

export default function RootLayout() {
  return (
    <ThemeProvider value={navTheme}>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="configuracoes" options={{ title: 'Configurações' }} />
      </Stack>
    </ThemeProvider>
  );
}
