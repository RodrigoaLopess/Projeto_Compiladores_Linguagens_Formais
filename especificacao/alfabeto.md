# Alfabeto da DrawLang

O alfabeto da linguagem DrawLang é o conjunto finito de caracteres que podem aparecer em um programa escrito na linguagem.

Podemos representar o alfabeto por:

[
\Sigma = L \cup D \cup E
]

onde:

* **L** é o conjunto de letras;
* **D** é o conjunto de dígitos;
* **E** é o conjunto de símbolos especiais.

## Letras

A linguagem aceita letras do alfabeto latino, maiúsculas e minúsculas:

```text
A B C D E F G H I J K L M
N O P Q R S T U V W X Y Z

a b c d e f g h i j k l m
n o p q r s t u v w x y z
```

Como os comandos da DrawLang não diferenciam letras maiúsculas de minúsculas, por exemplo:

```text
MOVER
mover
Mover
```

devem ser interpretados da mesma forma.

## Dígitos

Os dígitos permitidos são:

```text
0 1 2 3 4 5 6 7 8 9
```

Eles são utilizados para representar valores numéricos, como coordenadas, ângulos, distâncias, raios e tamanhos.

Exemplos:

```text
MOVER 100
VIRAR 90
IR 200 150
CIRCULO 50
```

## Símbolos especiais

Os símbolos especiais utilizados pela linguagem são:

```text
#
+
-
.
espaço
tabulação
quebra de linha
```

Seus usos são:

* `#` — início de um comentário;
* `+` — sinal opcional para números positivos;
* `-` — representação de números negativos;
* `.` — separador da parte decimal de números;
* espaço — separação entre comandos e argumentos;
* tabulação — caractere de espaço em branco;
* quebra de linha — separação dos comandos do programa.

## Representação do alfabeto

Portanto, de forma simplificada, o alfabeto da DrawLang é:

```text
Σ = {
    A-Z,
    a-z,
    0-9,
    #,
    +,
    -,
    .,
    espaço,
    tabulação,
    quebra de linha
}
```

Esse conjunto é finito e contém todos os caracteres necessários para escrever os programas definidos inicialmente pela DrawLang.
