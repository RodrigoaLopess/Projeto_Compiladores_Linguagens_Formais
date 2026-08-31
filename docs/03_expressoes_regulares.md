# Expressões Regulares

A DrawLang aceita uma sintaxe pequena de expressões regulares, mas o restante do compilador trabalha com um núcleo ainda menor.

## Sintaxe aceita

- `ab` para concatenação;
- `a|b` para alternância;
- `a*` para repetição zero ou mais vezes;
- `a+` para uma ou mais vezes;
- `a?` para expressão opcional;
- parênteses para agrupamento e captura.

## Núcleo interno

Depois da leitura, a árvore é reduzida para apenas quatro formas:

| Forma | Significado |
| --- | --- |
| `("simbolo", x)` | símbolo da expressão |
| `(".", a, b)` | concatenação |
| `("|", a, b)` | alternância |
| `("*", a)` | fecho de Kleene |
| `("vazio",)` | palavra vazia usada pelas reduções |

Os operadores `+` e `?` são apenas açúcar sintático. Eles não seguem para as próximas etapas do compilador.

## Reduções

| Sintaxe escrita | Árvore usada internamente |
| --- | --- |
| `x+` | `concat(x, fecho(x))` |
| `x?` | `alt(x, vazio)` |

Assim:

```text
a+
```

é reduzido para:

```text
(".", ("simbolo", "a"), ("*", ("simbolo", "a")))
```

e:

```text
a?
```

é reduzido para:

```text
("|", ("simbolo", "a"), ("vazio",))
```

A redução acontece durante o parsing. Dessa forma, construção do autômato, determinização e etapas posteriores só precisam conhecer concatenação, alternância, fecho e vazio.

## Precedência

A precedência, da maior para a menor, é:

1. agrupamento;
2. repetição (`*`, `+`, `?`);
3. concatenação;
4. alternância (`|`).

Por isso `ab|c` é lido como `(ab)|c`, e não como `a(b|c)`.

## Erros

Quando a expressão é inválida, `ErroRegex` informa a posição e também pode formatar o erro mostrando a expressão e uma seta sob a coluna correspondente.

Exemplo:

```text
a(b
   ^
faltou fechar parenteses
```
