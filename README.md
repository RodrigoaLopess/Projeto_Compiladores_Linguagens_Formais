# DrawLang

A DrawLang é uma linguagem simples para criar desenhos usando comandos de texto.

O projeto está sendo desenvolvido por etapas na disciplina de Compiladores e Linguagens Formais.

## Estrutura

- `docs/` - documentação
- `especificacao/` - definições da linguagem
- `exemplos/` - exemplos da DrawLang
- `src/` - código do projeto
- `tests/` - testes

## Expressões regulares

Neste módulo foi feito um analisador simples de expressões regulares.

Ele aceita concatenação, `|`, `*`, `+`, `?` e parênteses.

Para testar:

```bash
make test
```

## AFN, AFD e minimização

O projeto usa a árvore produzida por `src/regex_parser.py` para construir o AFN de Thompson em `src/afn.py`. A simulação e o fecho vazio também estão nesse arquivo. A determinização por subconjuntos, o estado de erro e a minimização por refinamento de partições estão em `src/afd.py`.

Os testes estão em `tests/test_afn.py` (AFN), `tests/test_afd.py` (comparação das três máquinas), `tests/test_regex.py` (parser) e `tests/test_automato.py` (autômato existente). Todos rodam com:

```bash
make test
```

Para `(a|b)*c`, o AFN tem 10 estados, 12 transições e 9 transições vazias. O AFD completo tem 5 estados e o mínimo tem 3. Nas 121 cadeias sobre `{a,b,c}` até comprimento 4, as três máquinas concordam e aceitam 15.

No padrão `(a|b)*a(a|b)(a|b)(a|b)`, que exige `a` na quarta posição a partir do fim, o AFD determinizado tem 17 estados (incluindo o erro) e o mínimo tem 16. O teste compara todas as cadeias até comprimento 7.
