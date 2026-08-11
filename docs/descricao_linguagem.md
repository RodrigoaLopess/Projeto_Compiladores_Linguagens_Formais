# DrawLang

## 1. Descrição

A **DrawLang** é uma linguagem de programação simples e específica para a criação de desenhos utilizando comandos de movimentação, cores, formas geométricas e repetição.

A linguagem foi desenvolvida com o objetivo de permitir que usuários criem desenhos através de comandos textuais, sem precisar utilizar diretamente uma biblioteca gráfica ou manipular pixels.

A ideia é semelhante à linguagem Logo, porém a DrawLang possui uma sintaxe própria e simplificada.

Um programa em DrawLang é interpretado sequencialmente. Cada comando modifica o estado de um "cursor", que possui uma posição, uma direção e uma cor. Conforme o cursor se movimenta, ele pode deixar uma linha na tela, permitindo a criação de desenhos.

---

## 2. Extensão dos arquivos

Os arquivos da linguagem utilizarão a extensão:

```text
.drw
```

Exemplo:

```text
desenho.drw
```

---

## 3. Comandos básicos

### 3.1. `INICIO`

Inicia um programa DrawLang.

```text
INICIO
```

### 3.2. `FIM`

Indica o final do programa.

```text
FIM
```

### 3.3. `MOVER`

Move o cursor uma determinada quantidade de pixels na direção atual.

Sintaxe:

```text
MOVER quantidade
```

Exemplo:

```text
MOVER 100
```

---

### 3.4. `VIRAR`

Altera a direção do cursor.

Sintaxe:

```text
VIRAR graus
```

Exemplo:

```text
VIRAR 90
```

Valores positivos representam uma rotação no sentido horário.

---

### 3.5. `CANETA`

Define a cor utilizada para desenhar.

Sintaxe:

```text
CANETA cor
```

Exemplo:

```text
CANETA vermelho
```

As cores básicas suportadas inicialmente serão:

* `vermelho`
* `azul`
* `verde`
* `amarelo`
* `preto`
* `branco`

---

### 3.6. `LEVANTAR`

Faz o cursor se movimentar sem desenhar uma linha.

```text
LEVANTAR
```

---

### 3.7. `BAIXAR`

Faz o cursor voltar a desenhar durante seus movimentos.

```text
BAIXAR
```

---

### 3.8. `IR`

Move o cursor diretamente para uma posição específica.

Sintaxe:

```text
IR x y
```

Exemplo:

```text
IR 200 150
```

---

## 4. Formas geométricas

A DrawLang também possui comandos simplificados para desenhar formas.

### 4.1. `QUADRADO`

Desenha um quadrado.

Sintaxe:

```text
QUADRADO tamanho
```

Exemplo:

```text
QUADRADO 100
```

---

### 4.2. `CIRCULO`

Desenha um círculo.

Sintaxe:

```text
CIRCULO raio
```

Exemplo:

```text
CIRCULO 50
```

---

### 4.3. `TRIANGULO`

Desenha um triângulo equilátero.

Sintaxe:

```text
TRIANGULO tamanho
```

Exemplo:

```text
TRIANGULO 80
```

---

## 5. Repetição

A DrawLang possui o comando `REPETIR`, utilizado para executar um conjunto de comandos várias vezes.

Sintaxe:

```text
REPETIR quantidade
comandos
FIM
```

Exemplo:

```text
REPETIR 4
MOVER 100
VIRAR 90
FIM
```

O exemplo acima desenha um quadrado.

---

## 6. Comentários

Comentários começam com o símbolo `#`.

Exemplo:

```text
# Este comando desenha um quadrado
QUADRADO 100
```

O interpretador ignora qualquer texto que esteja depois de `#` na mesma linha.

## 7. Estado inicial

Quando um programa é iniciado, o cursor terá os seguintes valores:

* Posição: `(0, 0)`
* Direção: `0°`
* Cor: `preto`
* Caneta: abaixada

A direção inicial de `0°` representa a direção para a direita.

---

## 8. Exemplo de programa

O código abaixo cria uma casa simples:

```text
INICIO

CANETA preto

QUADRADO 150

LEVANTAR
IR 40 150
BAIXAR

QUADRADO 70

LEVANTAR
IR 75 0
BAIXAR

TRIANGULO 150

FIM
```

---

## 9. Regras da linguagem

1. Cada comando deve estar em uma nova linha.
2. Os comandos não diferenciam letras maiúsculas de minúsculas.
3. Os valores numéricos devem ser números inteiros ou decimais.
4. Comandos desconhecidos devem gerar um erro.
5. A quantidade de repetição deve ser um número inteiro positivo.
6. Comentários começam com `#`.
7. Um programa deve começar com `INICIO`.
8. Um programa deve terminar com `FIM`.

---

## 10. Erros

Quando o programa encontrar um comando inválido, o interpretador deverá informar o erro e, se possível, indicar a linha onde ele ocorreu.

Exemplo:

```text
ERRO na linha 5: comando desconhecido "MOVEE"
```

Isso facilita a identificação de erros pelo usuário.

---

## 11. Objetivo

O principal objetivo da DrawLang é permitir que desenhos simples sejam criados através de uma linguagem textual fácil de aprender.

A linguagem também servirá para demonstrar conceitos fundamentais de linguagens de programação, como:

* análise léxica;
* análise sintática;
* interpretação de comandos;
* variáveis de estado;
* estruturas de repetição;
* tratamento de erros;
* geração de saída gráfica.

A implementação poderá utilizar uma biblioteca gráfica para desenhar na tela, enquanto o interpretador será responsável por transformar os comandos DrawLang em operações gráficas.
