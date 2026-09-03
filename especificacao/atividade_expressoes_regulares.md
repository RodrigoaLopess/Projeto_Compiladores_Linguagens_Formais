Kelwyn de Jesus, Luiz Felipe Brandão, Nycolas Estanislau, Rafael Vizelli, Rodrigo Lopes e Thiago das Neves

# Expressões Regulares — DrawLang

A DrawLang é uma linguagem que estamos criando para fazer desenhos usando comandos escritos.

Um exemplo:

```text
INICIO
QUANDO LINHA CASA /([0-9]+),([0-9]+)/ ENTAO
    IR $1 $2;
FIM
FIM
```

Para essa atividade usamos principalmente:

```text
x+ -> concat(x,fecho(x))
x? -> alt(x,ε)
```

Para facilitar, vamos chamar os dígitos de `D`:

```text
D = alt(alt(alt(alt(alt(alt(alt(alt(alt('0','1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
```

`D` tem 19 nós.

Também usamos `P` para os dígitos de 1 até 9:

```text
P = alt(alt(alt(alt(alt(alt(alt(alt('1','2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
```

`P` tem 17 nós.

Para palavras maiores usamos `cadeia("texto")`.

Exemplo:

```text
cadeia("azul") =
concat(
    concat(
        concat('a','z'),
        'u'
    ),
    'l'
)
```

Nos comandos usamos `CI("palavra")`, porque eles podem aparecer em maiúsculo ou minúsculo.

Exemplo:

```text
CI("INICIO") =
concat(
    concat(
        concat(
            concat(
                concat(
                    alt('i','I'),
                    alt('n','N')
                ),
                alt('i','I')
            ),
            alt('c','C')
        ),
        alt('i','I')
    ),
    alt('o','O')
)
```

# 1. Tabela de peças

| Peça | Exemplo | Padrão | Núcleo | Forma linear | Nós |
|---|---|---|---|---|---:|
| Número | `100` | `[0-9]+(\.[0-9]+)?` | `D D* ('.' D D* \| ε)` | `concat(concat(D,fecho(D)),alt(concat('.',concat(D,fecho(D))),ε))` | 85 |
| Captura | `$1` | `\$[1-9][0-9]*` | `'$' P D*` | `concat('$',concat(P,fecho(D)))` | 40 |
| Palavra fixa | `QUANDO` | `INICIO\|FIM\|MOVER\|VIRAR\|CANETA\|LEVANTAR\|BAIXAR\|IR\|QUADRADO\|CIRCULO\|TRIANGULO\|REPETIR\|QUANDO\|LINHA\|CASA\|ENTAO` | alternância das palavras | `alt(...alt(CI("INICIO"),CI("FIM"))...,CI("ENTAO"))` | 367 |
| Cor | `azul` | `vermelho\|azul\|verde\|amarelo\|preto\|branco` | alternância das cores | `alt(...alt(cadeia("vermelho"),cadeia("azul"))...,cadeia("branco"))` | 69 |
| Sinal | `/` ou `;` | `/\|;` | `/\|;` | `alt('/',';')` | 3 |

### Número

O padrão é:

```text
[0-9]+(\.[0-9]+)?
```

A parte `[0-9]+` vira:

```text
concat(D,fecho(D))
```

Como `D` tem 19 nós:

```text
19 + 19 + 1 + 1 = 40
```

A parte decimal opcional tem 44 nós.

Então:

```text
40 + 44 + 1 = 85 nós
```

### Captura

Exemplos:

```text
$1
$2
```

Padrão:

```text
\$[1-9][0-9]*
```

Forma:

```text
concat('$',concat(P,fecho(D)))
```

Conta:

```text
1 + 17 + 20 + 1 + 1 = 40 nós
```

### Palavra fixa

Algumas palavras da linguagem são:

```text
INICIO
FIM
MOVER
VIRAR
CANETA
LEVANTAR
BAIXAR
IR
QUADRADO
CIRCULO
TRIANGULO
REPETIR
QUANDO
LINHA
CASA
ENTAO
```

Como pode ser maiúsculo ou minúsculo, uma letra fica assim:

```text
alt('q','Q')
```

Por isso usamos `CI("palavra")`.

As 16 palavras têm 92 letras no total.

A conta das palavras deu 352 nós.

Depois usamos mais 15 alternâncias para juntar todas:

```text
352 + 15 = 367 nós
```

### Cor

As cores são:

```text
vermelho
azul
verde
amarelo
preto
branco
```

Exemplo:

```text
cadeia("azul") =
concat(
    concat(
        concat('a','z'),
        'u'
    ),
    'l'
)
```

As palavras juntas dão 64 nós.

Com mais 5 alternâncias:

```text
64 + 5 = 69 nós
```

### Sinal

```text
alt('/',';')
```

São dois símbolos e uma alternância:

```text
3 nós
```

**Verificação da contagem:** ainda falta outro integrante fazer a contagem separado.

# 2. Cobertura mínima

Usamos:

```text
[0-9]+(\.[0-9]+)?
```

Temos `+` em:

```text
[0-9]+
```

que vira:

```text
concat(D,fecho(D))
```

Também temos `?` na parte:

```text
(\.[0-9]+)?
```

que vira:

```text
alt(concat('.',concat(D,fecho(D))),ε)
```

Então nossa tabela tem fecho e opcional.

# 3. Um par que converge

Escolhemos:

```text
[0-9]+
```

e:

```text
[0-9][0-9]*
```

As duas viram:

```text
concat(D,fecho(D))
```

A forma completa fica:

```text
concat(
    alt(alt(alt(alt(alt(alt(alt(alt(alt('0','1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9'),
    fecho(
        alt(alt(alt(alt(alt(alt(alt(alt(alt('0','1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
    )
)
```

As duas têm 40 nós.

**Verificação:** as duas deram a mesma forma.

# 4. Um par que não converge

Usamos:

```text
(0|1)*
```

e:

```text
(0*1*)*
```

A primeira fica:

```text
fecho(alt('0','1'))
```

e tem 4 nós.

A segunda:

```text
fecho(
    concat(
        fecho('0'),
        fecho('1')
    )
)
```

e tem 6 nós.

As árvores são diferentes, mas as duas conseguem formar sequências de `0` e `1`.

Por exemplo:

```text
0101
```

pode aparecer nas duas.

Então árvores diferentes não significam obrigatoriamente linguagens diferentes.

# 5. Dois requisitos da DrawLang

## Um que ainda dá para resolver com expressão regular

No comando:

```text
REPETIR 4
```

o número deve ser inteiro positivo.

Usamos:

```text
[1-9][0-9]*
```

Aceita:

```text
1
4
10
100
```

Não aceita:

```text
0
-1
2.5
```

Nesse caso, a máquina precisa lembrar poucas situações, então ainda dá para fazer com expressão regular.

## Um que não dá para resolver só com isso

Podemos ter blocos dentro de outros blocos:

```text
REPETIR 4
    REPETIR 2
        MOVER 100
    FIM
FIM
```

O sistema precisa saber quantos blocos foram abertos e ainda não foram fechados.

Como não existe um limite definido para isso, essa quantidade pode crescer.

Por isso não dá para resolver só com as expressões regulares dessa atividade.

# 6. Quatro erros com posição

As posições começam no `0`.

### Grupo que não fecha

```text
a(b|c
     ^
faltou fechar parenteses
```

Posição: **5**

### Repetição sem operando

```text
*a
^
operador sem expressao
```

Posição: **0**

### Classe sem colchete final

```text
[0-9
    ^
faltou fechar colchete
```

Posição: **4**

### Símbolo sobrando

```text
a)
 ^
simbolo inesperado
```

Posição: **1**

# Caminho de volta

Pegando:

```text
concat(D,fecho(D))
```

podemos escrever:

```text
(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*
```

Se reduzir de novo, voltamos para:

```text
concat(D,fecho(D))
```

**Verificação:** deu a mesma forma.

# Conclusão

Essa atividade ajudou a entender melhor como os padrões da DrawLang podem virar árvores.

Também deu para ver que duas formas diferentes podem chegar na mesma árvore e que duas árvores diferentes ainda podem aceitar as mesmas sequências.
