# Recorte da DrawLang

A DrawLang será uma linguagem simples para fazer desenhos usando comandos escritos pelo usuário.

O programa começa com `INICIO` e termina com `FIM`.

Os principais comandos serão:

- `MOVER` para movimentar o cursor;
- `VIRAR` para mudar a direção;
- `CANETA` para escolher a cor;
- `LEVANTAR` e `BAIXAR` para controlar se o cursor desenha ou não;
- `IR` para ir até uma posição;
- `QUADRADO`, `CIRCULO` e `TRIANGULO` para criar formas;
- `REPETIR` para repetir comandos.

Os arquivos da linguagem terão extensão `.drw`.

O cursor começa na posição `(0,0)`, apontando para a direita, com a cor preta e com a caneta abaixada.

O comando `REPETIR` pode conter outros comandos e termina com `FIM`.

Nesta primeira versão não teremos variáveis, funções ou condicionais. A ideia é manter a linguagem simples e ir aumentando durante a disciplina.
