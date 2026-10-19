# MEL-239 fase 2 — pallet dividido sem repetir lance

Problema: `ficha_producao.PackListCabine` guarda um link só (o 2º pallet sobrescreve o 1º) e o app não sabia quais lances já saíram em outro pallet.

## 1. Criar a lista SharePoint `Packing_Pallets` (OperationsGuaratingueta) e adicionar como fonte no app
| Coluna | Tipo | Conteúdo |
|---|---|---|
| Title | Texto | OP (8 dígitos) |
| FichaID | Número | ID do item em `ficha_producao` (chave de busca) |
| Pallet | Número | nº do pallet (1–99) |
| LanceIDs | Várias linhas de texto | IDs dos lances (RegistrosInspeção) separados por `;` |
| QtdLances | Número | quantos lances |
| TotalM | Número (2 casas) | metros do pallet |
| Turno | Número | turno da impressão |
| DataHoraImp | Data e hora | quando imprimiu |
| LinkPDF | Hiperlink | vazio por enquanto (fluxo GMS_PackListParaFicha v3 grava aqui) |

Indexar `FichaID`. Uma linha por pallet: reimprimir o mesmo nº de pallet da mesma ficha **atualiza** a linha, não duplica.

## 2. O que mudou em `scr_Finalização_1` (nada bloqueia a impressão)
- **Dividir pallet** lê `Packing_Pallets` da ficha (`colPalletJa`) e marca por padrão **só os lances que ainda não saíram**; lance já impresso fica desmarcado, em laranja, com "· já no pallet N".
- **PALLET Nº** já vem sugerido: maior pallet da ficha + 1.
- Marcar um lance que já saiu em **outro** pallet mostra "⚠ N lance(s) marcado(s) já saíram em outro pallet. Pode imprimir, mas confira." — só aviso.
- **Imprimir este pallet** grava/atualiza a linha em `Packing_Pallets` e navega. Se a gravação falhar, a impressão segue e a `TelaImpressao` mostra (fora da folha) "Não registrou no sistema (sem rede?)…".
- Sem `Notify` na hora da impressão (norma MEL-236): o flag `varFalhaRegManual` vira label com `!Parent.Printing`.
- `TelaImpressao`: o label de aviso passou a valer também no pallet dividido (não só no packing manual); o `OnVisible` deixou de zerar o flag, quem zera são os botões de entrada.

## 3. Ordem para colar
1. Criar a lista e adicionar a fonte `Packing_Pallets` no Studio.
2. Colar a `scr_Finalização_1` (patch por bloco: btn_DividirPalletExt, gal_PalletExt/btn_ItemPalletExt, inp_PalletNumExt, lbl_AvisoJaImpressoExt novo, btn_ImprimirPalletExt, btn_ImprimirExt e btn_PackingManualExt) e a `TelaImpressao`.
3. Testar: OP com 10 lances → pallet 1 com 7 → reabrir Dividir: os 7 aparecem "já no pallet 1" desmarcados, 3 marcados, número sugerido 2.

## 4. Fora desta fase
PDF no `LinkPDF` por pallet (fluxo GMS_PackListParaFicha chamado no app) — depende da aprovação do MEL-237.
