# Textos dos testes 3 e 4 (internos, não publicar)

## Teste 3 (10 s): debounce do botão do Will Station

STATUS: BLOQUEADO PELO CÓDIGO. O código do Will Station (Arduino Uno + Shield Joystick) não está no repositório: busquei `debounce` e `joystick` em todo o projeto e só existe `Conteudo_Bit/WillStation/sobre_o_projeto.txt` (texto, sem código). Sem arquivo e linhas reais, não cito algoritmo nem valores. Preciso que o William coloque o .ino em `Conteudo_Bit/WillStation/` (ou me diga o caminho).

Estrutura já definida, para preencher assim que o código chegar (nada abaixo é número):
- Algoritmo a animar (padrão, a confirmar contra o código): leitura do pino do botão -> se mudou em relação à última leitura, reinicia o cronômetro -> só aceita o novo estado depois que o sinal fica estável pelo intervalo definido no código -> registra UM aperto.
- Cena: linha de sinal ruidoso (quicadas do contato) entrando em um filtro; saída limpa com um único degrau. Valor do intervalo e pino: ler do código, mostrar só o que estiver lá.
- Rótulos de tela (curtos):
  1. "o botão treme"
  2. "espera o sinal firmar"
  3. "um aperto, um evento"
  4. (fecho, opcional) "ponto e vírgula também"  [referência ao texto-base do projeto: o erro era ponto e vírgula]
- Fonte a citar em `plano.md` quando houver: arquivo e linhas do .ino. Conferir com WebSearch o conceito de "contact bounce" antes de afirmar qualquer fato técnico geral.

## Teste 4 (8 s): frase cinética

Frase (9 palavras, sem ponto final):

Engenharia é o erro que você aprendeu a ler

- Objeto-guia: a palavra "erro" vira o objeto (o ponto e vírgula que faltava, base do texto do Will Station) e guia a câmera/movimento pelo resto da frase.
- Destaque vermelho #FF3B1F: na palavra "ler".
- Ritmo sugerido: "Engenharia é o" entra seca; "erro" para e vira objeto; "que você aprendeu a" corre; "ler" crava em vermelho no último compasso.
