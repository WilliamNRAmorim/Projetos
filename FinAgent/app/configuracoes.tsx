import { Fragment, useEffect, useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, TextInput } from 'react-native';
import { Tela } from '@/src/Tela';
import { CHAVES, NomeChave, getSecret, setSecret } from '@/src/secrets';
import { theme } from '@/src/theme';

export default function Configuracoes() {
  const [valores, setValores] = useState<Record<NomeChave, string>>({ mercadopago: '', gemini: '', brapi: '' });
  const [salvas, setSalvas] = useState<Record<NomeChave, boolean>>({ mercadopago: false, gemini: false, brapi: false });

  useEffect(() => {
    (async () => {
      const r = { mercadopago: false, gemini: false, brapi: false };
      for (const c of CHAVES) r[c.nome] = !!(await getSecret(c.nome));
      setSalvas(r);
    })();
  }, []);

  async function salvar(nome: NomeChave) {
    await setSecret(nome, valores[nome]);
    setSalvas((s) => ({ ...s, [nome]: !!valores[nome].trim() }));
    setValores((v) => ({ ...v, [nome]: '' }));
    Alert.alert('Pronto', 'Chave guardada com segurança neste aparelho.');
  }

  return (
    <Tela titulo="Configurações" texto="Cole cada chave abaixo. Elas ficam só no armazenamento seguro do aparelho e nunca são exibidas de volta.">
      {CHAVES.map((c) => (
        <Fragment key={c.nome}>
          <Text style={s.rotulo}>
            {c.rotulo} {salvas[c.nome] ? '(salva)' : '(não configurada)'}
          </Text>
          <TextInput
            style={s.input}
            value={valores[c.nome]}
            onChangeText={(t) => setValores((v) => ({ ...v, [c.nome]: t }))}
            placeholder="Cole aqui"
            placeholderTextColor={theme.muted}
            secureTextEntry
            autoCapitalize="none"
            autoCorrect={false}
          />
          <Pressable style={s.botao} onPress={() => salvar(c.nome)}>
            <Text style={s.botaoTxt}>Salvar</Text>
          </Pressable>
        </Fragment>
      ))}
    </Tela>
  );
}

const s = StyleSheet.create({
  rotulo: { color: theme.text, fontSize: 15, marginTop: 8 },
  input: { backgroundColor: theme.card, color: theme.text, borderColor: theme.border, borderWidth: 1, borderRadius: 8, padding: 12 },
  botao: { backgroundColor: theme.tint, borderRadius: 8, padding: 12, alignItems: 'center' },
  botaoTxt: { color: '#0e1116', fontWeight: '700' },
});
