# Recorte da DrawLang

A DrawLang é uma linguagem que lê dados de entrada e desenha o que encontrou neles.

O programa não descreve apenas uma figura fixa. Ele pode declarar padrões para reconhecer trechos de cada linha de um arquivo e usar os valores capturados como argumentos dos comandos de desenho.

Um exemplo básico é:

```text
INICIO

QUANDO LINHA CASA /(\d+),(\d+)/ ENTAO
    IR $1 $2;
FIM

FIM
```

Nesse caso, o padrão procura duas sequências de dígitos separadas por vírgula. Quando uma linha casa com o padrão, `$1` representa o primeiro grupo capturado e `$2` representa o segundo.

Os comandos de desenho continuam fazendo parte da linguagem:

- `MOVER` movimenta o cursor;
- `VIRAR` muda a direção;
- `CANETA` escolhe a cor;
- `LEVANTAR` e `BAIXAR` controlam se o cursor desenha;
- `IR` leva o cursor até uma posição;
- `QUADRADO`, `CIRCULO` e `TRIANGULO` desenham formas;
- `REPETIR` repete um bloco de comandos;
- `QUANDO LINHA CASA /padrao/ ENTAO ... FIM` executa um bloco quando a linha de entrada corresponde ao padrão.

Os arquivos de programa usam a extensão `.drw`.

O cursor começa na posição `(0,0)`, apontando para a direita, com a cor preta e com a caneta abaixada.

## Entrada e captura

A entrada é lida linha por linha.

Cada construção `QUANDO LINHA CASA /.../` possui uma expressão regular. Os grupos entre parênteses criam capturas numeradas da esquerda para a direita.

Por exemplo:

```text
/([0-9]+),([0-9]+)/
```

Para a linha:

```text
120,45
```

o primeiro grupo corresponde a `120` e o segundo a `45`. Dentro do bloco, esses valores são acessados como `$1` e `$2`.

A captura faz parte do reconhecimento do padrão. A proposta não prevê executar um segundo reconhecedor por retrocesso apenas para descobrir os grupos depois que o autômato já aceitou a linha.

## Separação entre compilação e execução

O projeto será dividido em duas etapas:

1. o compilador lê o programa DrawLang e gera um objeto contendo as instruções de desenho, as tabelas de transição dos padrões e as informações necessárias para preservar as capturas;
2. o executor lê esse objeto, recebe os dados de entrada e produz o desenho correspondente.

Essa separação permite que o mesmo programa compilado seja usado com arquivos de entrada diferentes.

## Exemplo canônico

O arquivo `exemplos/captura_pontos.drw` é usado com dois arquivos de entrada:

- `exemplos/entrada_pontos_01.txt`;
- `exemplos/entrada_pontos_02.txt`.

O programa é exatamente o mesmo nos dois casos. O que muda são os dados lidos e, por consequência, as posições desenhadas.

O resultado esperado está descrito em `exemplos/captura_pontos_esperado.md`.

Nesta etapa ainda não fazem parte do recorte variáveis gerais, funções definidas pelo usuário ou operações aritméticas completas. As referências `$1`, `$2`, etc. existem especificamente para acessar capturas produzidas pelos padrões.
