# AFN e simulação

Nesta etapa fizemos o AFN seguindo o modelo do professor (`src/afn.py`) e usamos ele nos padrões da DrawLang.

Na DrawLang a entrada é lida linha por linha e cada `QUANDO LINHA CASA /padrao/ ENTAO` precisa saber se a linha casa com o padrão. É isso que o AFN faz:

```text
programa .drw  ->  padrao /.../  ->  arvore (regex_parser)  ->  AFN  ->  simula cada linha
```

## Estrutura

- `transicoes[estado]` guarda a lista de transições de cada estado;
- cada transição tem um `simbolo` e um `destino`;
- o AFN guarda o estado `inicial` e o estado de `aceitacao`.

Símbolos especiais:

| Constante | Na regex | Significado |
| --- | --- | --- |
| `EPSILON` | — | transição vazia (ε) |
| `QUALQUER` | `.` | coringa, casa com qualquer símbolo |

Para escrever um ponto de verdade (como no número decimal) usamos `\.`.

## Métodos

- `novoEstado()` cria um estado e devolve o número dele;
- `adicionarTransicao(origem, simbolo, destino)`;
- `definirInicial(estado)` e `definirAceitacao(estado)`;
- `quantidadeDeEstados()`, `quantidadeDeTransicoes()` e `quantidadeDeTransicoesVazias()`;
- `fechoVazio(conjunto)` faz uma busca em profundidade só pelas transições ε, usando um vetor de visitados para não entrar em ciclo;
- `simular(cadeia)` devolve os passos, o maior conjunto ativo e se aceitou.

## Simulação

1. Começa com o fecho-ε do estado inicial (não só com o inicial).
2. Para cada símbolo: pega os destinos das transições que casam (ou do coringa), tira os repetidos e aplica o fecho-ε.
3. Se ficar sem estados ativos, para.
4. Aceita se o estado de aceitação estiver nos ativos no final.

## Padrões da DrawLang

Para os padrões da DrawLang funcionarem, o `regex_parser` agora também lê:

| Escrito | Vira |
| --- | --- |
| `[0-9]` | `alt('0', alt('1', ... '9'))` (o D da atividade) |
| `\d` | o mesmo que `[0-9]` |
| `\.`, `\/`, `\(` ... | o próprio símbolo |
| `.` | `("qualquer",)`, o coringa |

Erros novos: `faltou fechar colchete` (ex.: `[0-9`, posição 4) e `classe vazia`.

## Exemplo: `captura_pontos.drw`

```text
INICIO

QUANDO LINHA CASA /([0-9]+),([0-9]+)/ ENTAO
    IR $1 $2;
FIM

FIM
```

Rodando `make afn` (usa `exemplos/entrada_pontos_01.txt`):

```text
Padrao: /([0-9]+),([0-9]+)/
estados: 158
transicoes: 197
transicoes vazias: 156

Linha: '10,20'
  ...
  ACEITA

Linha: 'oi'
  le 'ε'   -> ativos {0, 1, 3, 4, 6, ...}
  le 'o'   -> ativos {}
  maior conjunto ativo: 19
  REJEITA

Linha: '7,'
  ...
  REJEITA
```

Na linha `oi` o conjunto ativo fica vazio logo no primeiro símbolo e a simulação para.
Em `7,` a simulação chega no fim, mas o estado de aceitação não está entre os ativos.

Para usar outro programa ou outra entrada:

```bash
python -m src.afn exemplos/captura_pontos.drw exemplos/entrada_pontos_02.txt
```

## Exemplo do professor (`a*b`)

O exemplo do material continua nos testes (`tests/test_afn.py`):

```text
0 --a--> 0
0 --ε--> 1
1 --b--> 2
```

Simulando `ab`: `{0, 1}` → lê `a` → `{0, 1}` → lê `b` → `{2}` → aceita.

## O que ainda falta

O AFN só diz se a linha casa ou não. Os valores de `$1` e `$2` (capturas) ainda não saem dele; isso fica para a próxima etapa.
