# MEL-231 — Monitor Mandril sem Power Automate (proposta, nada aplicado)

Fluxo atual: `Monitor Solda Mandril` (agendado). A tela `scr_Monitor_Mandril` só LÊ a lista `Estado_Trancadeiras`; o fluxo é quem calcula e grava. Lido em 08/10/2026 pelo Code view, sem alterar nada.

## O que o fluxo faz hoje
1. Lê `Estado_Trancadeiras` (uma linha por trançadeira; chave `Maquina_Vel`, `Title` = nome na tela), `DM_Velocidade` (sem filtro) e `ficha_producao` com `field_11 eq 'Aguardando' or field_11 eq 'Em processo'`.
2. Normaliza as fichas (nomes internos): Maquina = `Tran_x00e7_adeira`, Status = `field_11`, Processo = `field_10`, Mangueira, Bitola, OP, Metros = `int(field_14)`, Prod1/2/3 = `Qtd_Turno1/2/3`. Fica só `Processo = 'Trançadeira'`.
3. Velocidade: de `DM_Velocidade`, Mangueira = `field_2`, Maquina = `field_1`, Velocidade = `field_3` (m/h).
4. Para cada linha de `Estado_Trancadeiras`:
   - `OPEmProcesso` = fichas da máquina com Status `Em processo`; `FilaAguardando` = com Status `Aguardando`.
   - `RestanteAtual` = se há OP em processo: `max(0, Metros − (Prod1+Prod2+Prod3))`, senão 0.
   - `TotalFila` = soma de `Metros` da fila (Aguardando).
   - `MaterialTotal` = `RestanteAtual + TotalFila`.
   - `MangueiraAtual` = mangueira da OP em processo, senão da primeira da fila, senão vazio.
   - `Velocidade` = velocidade da combinação (máquina, MangueiraAtual) em `DM_Velocidade`; 0 se não achar.
   - `HoraParada` = se `MaterialTotal > 0` e `Velocidade > 0`: agora + `MaterialTotal / Velocidade * 3600` segundos; senão nulo.
   - Grava em `Estado_Trancadeiras`: Status (`Produzindo` se há OP em processo ou fila, senão `SemPlano`), Mangueira_Atual, Quantidade_m, Bitola, Velocidade, Hora_Parada, Proxima_Mangueira (1ª da fila), Atualizado_Em, Critico (parada em 0 a 30 min).

## Proposta (padrão do Painel da Célula: dado no app, sem fluxo)
No `OnVisible` e no timer de refresh da tela (a cada 30 s, sem `Patch` no Timer), carregar as três fontes delegáveis e calcular numa coleção:

```
ClearCollect(
    colFichaTranc,
    Filter(ficha_producao, field_10 = "Trançadeira" && (field_11 = "Aguardando" || field_11 = "Em processo"))
);
```
e uma fórmula nomeada (`fx_EstadoTrancadeiras`) que devolve uma linha por trançadeira com Mangueira_Atual, Quantidade_m, Velocidade, Hora_Parada, Proxima_Mangueira e Critico, com as mesmas contas acima (`DateAdd(Now(), Int(Material / Velocidade * 3600), TimeUnit.Seconds)`). A galeria troca `colMonitor` por essa saída; `Estado_Trancadeiras` fica só como cadastro das máquinas (Title, Maquina_Vel, Status de manutenção).

## Cuidados antes de aplicar
- **Manutenção:** a tela mostra "MAN." quando `Status = "Manutencao"`, mas o fluxo reescreve o Status a cada rodada com Produzindo/SemPlano. Descobrir quem grava Manutencao (outro fluxo/app?) antes de desligar este.
- **Nomes internos** (`field_10`, `field_11`, `field_14`, `Tran_x00e7_adeira`, `field_1/2/3` do DM_Velocidade): usar estes no app; os de exibição falham (lição MEL-240).
- **Delegação:** o `Filter` por texto com `=` e `||` é delegável; somas só sobre a coleção já filtrada (fila pequena).
- **Fuso:** o fluxo grava UTC; no app `Now()` já é local, então `Hora_Parada` calculada no app dispensa conversão.
- **Corte:** testar lado a lado com o fluxo ligado (comparar Hora_Parada e Critico por máquina) antes de desligar o fluxo. Desligar, não apagar.
- Qualquer mudança na tela só com aprovação do William.
