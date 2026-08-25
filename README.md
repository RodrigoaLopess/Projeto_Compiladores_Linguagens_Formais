# DrawLang

A DrawLang é uma linguagem simples para criar desenhos usando comandos de texto.

O usuário escreve os comandos em um arquivo `.drw`. O programa lê esses comandos e faz o desenho.

Exemplo:

```text
INICIO
CANETA azul
REPETIR 4
MOVER 100
VIRAR 90
FIM
FIM
```

O exemplo acima deve formar um quadrado azul.

## Estrutura do projeto

- `docs/` - documentação da linguagem
- `especificacao/` - alfabeto e classes léxicas
- `exemplos/` - exemplos de programas DrawLang
- `src/` - código do projeto, que será feito nos próximos módulos

## Teste

Para verificar a estrutura atual do projeto:

```bash
make test
```
