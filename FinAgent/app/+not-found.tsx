import { Link, Stack } from 'expo-router';
import { Tela } from '@/src/Tela';

export default function NotFound() {
  return (
    <>
      <Stack.Screen options={{ title: 'Ops!' }} />
      <Tela titulo="Tela não encontrada">
        <Link href="/" style={{ color: '#4fc3a1' }}>Voltar ao Painel</Link>
      </Tela>
    </>
  );
}
