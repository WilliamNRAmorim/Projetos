import { Link } from 'expo-router';
import { Text } from 'react-native';
import { Tela } from '@/src/Tela';
import { theme } from '@/src/theme';

export default function Painel() {
  return (
    <Tela titulo="Painel" texto="Visão geral das suas finanças (em construção).">
      <Link href="/configuracoes" style={{ color: theme.tint, fontSize: 16 }}>
        Configurações (chaves de API)
      </Link>
      <Text style={{ color: theme.muted, fontSize: 12 }}>
        App educativo. Não é consultoria de investimentos registrada.
      </Text>
    </Tela>
  );
}
