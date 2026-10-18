import { Ionicons } from '@expo/vector-icons';
import { ComponentProps } from 'react';
import { ColorValue } from 'react-native';
import { Tabs } from 'expo-router';
import { cores } from '@/src/ui';

type Icone = ComponentProps<typeof Ionicons>['name'];

const aba = (nome: Icone, nomeAtivo: Icone) =>
  ({ color, size, focused }: { color: ColorValue; size: number; focused: boolean }) => (
    <Ionicons name={focused ? nomeAtivo : nome} size={size} color={color} />
  );

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: cores.primaria,
        tabBarInactiveTintColor: cores.texto2,
        tabBarStyle: { backgroundColor: cores.superficie, borderTopColor: cores.borda },
        headerStyle: { backgroundColor: cores.superficie },
        headerTintColor: cores.texto,
        tabBarLabelStyle: { fontSize: 11 },
      }}>
      <Tabs.Screen name="index" options={{ title: 'Início', headerShown: false, tabBarIcon: aba('home-outline', 'home') }} />
      <Tabs.Screen name="gastos" options={{ title: 'Gastos', tabBarIcon: aba('receipt-outline', 'receipt') }} />
      <Tabs.Screen name="metas" options={{ title: 'Metas', tabBarIcon: aba('flag-outline', 'flag') }} />
      <Tabs.Screen name="mercado" options={{ title: 'Mercado', tabBarIcon: aba('trending-up-outline', 'trending-up') }} />
      <Tabs.Screen name="economista" options={{ title: 'Economista', tabBarIcon: aba('chatbubbles-outline', 'chatbubbles') }} />
    </Tabs>
  );
}
