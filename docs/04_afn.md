# AFN e simulação

Nesta etapa fizemos o AFN seguindo o modelo do professor (`src/afn.py`).

## Estrutura

- `transicoes[estado]` guarda a lista de transições de cada estado;
- cada transição tem um `simbolo` e um `destino`;
- o AFN guarda o estado `inicial` e o estado de `aceitacao`.

Símbolos especiais:

| Constante | Valor | Significado |
| --- | --- | --- |
| `EPSILON` | `ε` | transição vazia |
| `QUALQUER` | `.` | coringa, casa com qualquer símbolo |

## Métodos

- `novoEstado()` cria um estado e devolve o número dele;
- `adicionarTransicao(origem, simbolo, destino)`;
- `definirInicial(estado)` e `definirAceitacao(estado)`;
- `quantidadeDeEstados()`, `quantidadeDeTransicoes()` e `quantidadeDeTransicoesVazias()`;
- `fechoVazio(conjunto)` faz uma busca em profundidade só pelas transições ε, usando um vetor de visitados para não entrar em ciclo;
- `simular(cadeia)` devolve os passos, o maior conjunto ativo e se aceitou.

## Simulação

1. Começa com o fecho-ε do estado inicial.
2. Para cada símbolo: pega os destinos das transições que casam (ou do coringa), tira os repetidos e aplica o fecho-ε.
3. Se ficar sem estados ativos, para.
4. Aceita se o estado de aceitação estiver nos ativos no final.

## Exemplo `a*b`

```text
0 --a--> 0
0 --ε--> 1
1 --b--> 2
```

Rodando `make afn`:

```text
le 'ε'   -> ativos {0, 1}
le 'a'   -> ativos {0, 1}
le 'b'   -> ativos {2}
maior conjunto ativo: 2
ACEITA
```

## Ligação com a DrawLang

A função `construirAfn(arvore)` monta o AFN a partir da árvore do `regex_parser` (construção de Thompson).
Assim os padrões de `QUANDO LINHA CASA /.../` podem ser testados com o AFN:

```python
from src.regex_parser import analisar_regex
from src.afn import construirAfn

afn = construirAfn(analisar_regex("(ab|c)+"))
afn.aceita("cabc")  # True
```

O `.` da regex vira o coringa `QUALQUER`.
