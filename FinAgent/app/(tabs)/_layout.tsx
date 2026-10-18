import { Tabs } from 'expo-router';
import { theme } from '@/src/theme';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: theme.tint,
        tabBarInactiveTintColor: theme.muted,
        tabBarStyle: { backgroundColor: theme.card, borderTopColor: theme.border },
        headerStyle: { backgroundColor: theme.card },
        headerTintColor: theme.text,
        tabBarLabelStyle: { fontSize: 13, paddingBottom: 4 },
        tabBarIcon: () => null,
      }}>
      <Tabs.Screen name="index" options={{ title: 'Painel' }} />
      <Tabs.Screen name="mercado" options={{ title: 'Mercado' }} />
      <Tabs.Screen name="economista" options={{ title: 'Economista' }} />
      <Tabs.Screen name="metas" options={{ title: 'Metas' }} />
    </Tabs>
  );
}
