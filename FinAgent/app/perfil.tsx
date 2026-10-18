import { useEffect, useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { Tela } from '@/src/Tela';
import { PERFIL_VAZIO, validarCampo, validarPerfil, type PerfilTexto } from '@/src/metas';
import { lerPerfil, salvarPerfil } from '@/src/perfil';
import { theme } from '@/src/theme';

type Campo = { k: keyof PerfilTexto; rotulo: string; dica?: string };

const GRUPOS: { titulo: string; campos: Campo[] }[] = [
  {
    titulo: 'Renda',
    campos: [
      { k: 'salario', rotulo: 'Salário líquido mensal (R$)' },
      { k: 'diaSalario', rotulo: 'Dia em que o salário cai', dica: '1 a 31' },
    ],
  },
  {
    titulo: 'Parcela do aparelho',
    campos: [
      { k: 'parcela', rotulo: 'Valor da parcela mensal (R$)' },
      { k: 'diaParcela', rotulo: 'Dia aproximado do Pix (opcional)' },
      { k: 'parcelasRestantes', rotulo: 'Parcelas restantes (opcional)' },
      { k: 'parcelasMin', rotulo: 'Se incerto: mínimo de parcelas restantes (opcional)' },
      { k: 'parcelasMax', rotulo: 'Se incerto: máximo de parcelas restantes (opcional)' },
    ],
  },
  {
    titulo: 'Reservas',
    campos: [
      { k: 'cofrinho', rotulo: 'Saldo do Cofrinho (reserva de verdade) (R$)' },
      { k: 'separadoAparelho', rotulo: 'Separado para a parcela do aparelho (Emergências) (R$)' },
    ],
  },
  {
    titulo: 'Cartão de crédito',
    campos: [
      { k: 'limiteCartao', rotulo: 'Limite do cartão (R$)' },
      { k: 'faturaAberta', rotulo: 'Valor usado na fatura aberta (R$)' },
      { k: 'diaFechamento', rotulo: 'Dia de fechamento (opcional)' },
      { k: 'diaVencimento', rotulo: 'Dia de vencimento (opcional)' },
    ],
  },
];

export default function Perfil() {
  const [p, setP] = useState<PerfilTexto>(PERFIL_VAZIO);
  const [erros, setErros] = useState<Partial<Record<keyof PerfilTexto, string>>>({});
  const [aviso, setAviso] = useState<string | null>(null);

  useEffect(() => {
    lerPerfil().then(setP);
  }, []);

  const mudar = (k: keyof PerfilTexto, v: string) => {
    setP((x) => ({ ...x, [k]: v }));
    setErros((e) => ({ ...e, [k]: validarCampo(k, v) ?? undefined }));
    setAviso(null);
  };

  const salvar = async () => {
    const e = validarPerfil(p);
    setErros(e);
    if (Object.keys(e).length > 0) {
      setAviso('Corrija os campos em vermelho.');
      return;
    }
    await salvarPerfil(p);
    setAviso('Perfil salvo neste aparelho.');
  };

  return (
    <Tela titulo="Perfil financeiro" texto="Tudo é digitado por você e fica só neste aparelho. Campos em branco são ignorados.">
      {GRUPOS.map((g) => (
        <View key={g.titulo} style={s.card}>
          <Text style={s.grupo}>{g.titulo}</Text>
          {g.campos.map((c) => (
            <View key={c.k} style={{ gap: 4 }}>
              <Text style={s.rotulo}>{c.rotulo}</Text>
              <TextInput
                style={[s.input, erros[c.k] ? { borderColor: '#ef7b7b' } : null]}
                value={p[c.k]}
                onChangeText={(v) => mudar(c.k, v)}
                placeholder={c.dica ?? '0,00'}
                placeholderTextColor={theme.muted}
                keyboardType="decimal-pad"
              />
              {erros[c.k] ? <Text style={s.erro}>{erros[c.k]}</Text> : null}
            </View>
          ))}
        </View>
      ))}
      <Pressable style={s.botao} onPress={salvar}>
        <Text style={s.botaoTxt}>Salvar</Text>
      </Pressable>
      {aviso ? <Text style={s.mudo}>{aviso}</Text> : null}
    </Tela>
  );
}

const s = StyleSheet.create({
  card: { backgroundColor: theme.card, borderColor: theme.border, borderWidth: 1, borderRadius: 10, padding: 14, gap: 10 },
  grupo: { color: theme.text, fontSize: 16, fontWeight: '700' },
  rotulo: { color: theme.muted, fontSize: 13 },
  input: { backgroundColor: theme.bg, color: theme.text, borderColor: theme.border, borderWidth: 1, borderRadius: 8, padding: 10 },
  erro: { color: '#ef7b7b', fontSize: 12 },
  mudo: { color: theme.muted, fontSize: 13 },
  botao: { backgroundColor: theme.tint, borderRadius: 8, padding: 12, alignItems: 'center' },
  botaoTxt: { color: theme.bg, fontSize: 15, fontWeight: '700' },
});
