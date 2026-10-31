# MEL-009: auditoria de Patch sem checagem de erro (08/10/2026)

Regra: toda escrita em fonte de produção (Patch, Remove, RemoveIf, UpdateIf, Collect) precisa de `IfError` em volta ou de `Errors(<fonte>)` logo depois, com `Notify` para o operador.

Ferramenta nova: `python gms_qa_patch.py [janela]` (na pasta GMS). Lê `Telas/scr*.txt` e `TelaImpressao.txt`, acha cada escrita nas 20 fontes de produção e confere se há checagem nos 900 caracteres seguintes (ou `IfError` nos 400 anteriores).

## Resultado
| | Antes | Depois |
|---|---|---|
| Escritas em fonte analisadas | 147 | 147 |
| Sem checagem | 2 | **0** |
| Com checagem fora da janela, justificadas | 13 | 13 |

## Corrigido
- `scr_tubo_1` (v0.5.3): zerar a sobra do carretel no Iniciar não avisava se falhasse. Agora avisa "A sobra do carretel X NÃO foi zerada" com a mensagem do SharePoint.
- `scr_ExtrusoraMandril_1` (v0.3.2): o desfazer do início, quando o carretel não reserva, apagava o registro de controle sem checar. Agora avisa a supervisão se o registro aberto não fechou.

## Justificadas (a checagem existe, mas depois do bloco)
| Tela | Fonte | Por quê |
|---|---|---|
| `scr_DescartarOP_1` | `ficha_producao` (12 Patch) | Um Patch por etapa dentro do `Switch`; a checagem é uma só, logo depois do `Switch` |
| `scr_Vulcanizacao_1` | `Historico_Carretel`, `ficha_producao` | Lote com `ForAll`; checagem agregada depois do laço (falha parcial mantém só as OPs que faltam) |
| `scr_Debandagem_2` | `lista_carreteis` | Dois Patch seguidos (saída e entrada do carretel) e uma checagem depois dos dois |

Os Hora-Hora (`scr_HoraHora_Trancagem_2` e `_Cobertura_1`) e o Packing manual (`TelaImpressao`) usam `IfError` com coleção de falhas, e o script já os reconhece.

## O que a auditoria não cobre
- `SubmitForm` da `scr_Catenaria_1`: tem `OnFailure` no formulário.
- Patch em coleções locais (`col*`): não gravam em fonte.
- Se a checagem existe mas a mensagem é ruim, isso é revisão de texto, não de erro calado.
