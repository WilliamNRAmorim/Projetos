# Moldes (não publicados)

`scr_HoraHora_Mandril_2.txt` e `scr_HoraHora_Tubo_2.txt` foram gerados da `scr_HoraHora_Cobertura_1` (padrão Hora-Hora da Trançagem), gravando na lista `Hora-Hora` com Célula = "Mandril" / "Tubo". As telas antigas (`scrHoraHora_Mandril`, `scrHoraHora_Tubo`, listas `Hora_Hora_Mandril` e `Hora_Hora_Tubo`) NÃO foram tocadas.

Falta validar com o William antes de publicar:
1. Fonte da velocidade por hora (hoje a coluna MFG sai 0 e a Meta fica em branco; a lista de mangueiras vem das OPs "Em processo" da etapa).
2. Lista de máquinas/células (hoje uma célula só por etapa).
3. Lista de motivos de parada (hoje `fx_MotivosParada`).
4. Destino dos dados: o BI lê `Hora-Hora` ou as listas antigas?

Ao publicar: colar a tela, trocar o `Navigate` do botão Hora a Hora (scr_mandril_1 / scr_tubo_1) para a tela nova, mover o arquivo para `Telas/` e retirar a tela antiga.
