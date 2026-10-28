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

## AFN

O `src/afn.py` tem o AFN com fecho-ε e simulação passo a passo, seguindo o modelo do professor.

Para ver o exemplo `a*b`:

```bash
make afn
```

Mais detalhes em `docs/04_afn.md`.
