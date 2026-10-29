# AFN da DrawLang

O módulo `src/afn.py` implementa um autômato finito não determinístico (AFN).

- `TransicaoAfn` guarda símbolo e destino.
- `Afn` guarda listas de transições, estado inicial e estado de aceitação.
- `fechoVazio` percorre transições ε sem repetir estados (vetor `visitados`).
- `simular` começa no fecho do inicial, consome cada caractere e guarda os conjuntos ativos.
- `construirAfn` aplica Thompson para símbolo, vazio, coringa, concatenação, alternância e estrela.
- `lerPadroes` procura `QUANDO LINHA CASA /.../` sem diferenciar maiúsculas.

Execute `python -m src.afn` para testar as linhas do exemplo. Execute `make test` para todos os testes.

A simulação informa aceitação, passos e maior conjunto ativo; não extrai os valores de `$1` e `$2`.
