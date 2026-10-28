# Resultado esperado

O programa `captura_pontos.drw` leva o cursor para cada ponto `x,y` da entrada (`IR $1 $2`).
Linhas que não casam com `/([0-9]+),([0-9]+)/` são ignoradas.

- `entrada_pontos_01.txt`: casam `10,20` e `150,40`; `oi` e `7,` são ignoradas.
- `entrada_pontos_02.txt`: casam `0,0`, `100,0`, `100,100` e `0,100` (os cantos de um quadrado); `12;34` é ignorada.
