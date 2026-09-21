# Código-fonte

A implementação atual da DrawLang já possui:

- `regex_parser.py`: leitura da expressão regular e construção da árvore;
- `automato.py`: estrutura do autômato alinhada ao modelo AFD fornecido pelo professor;
- `main.py`: demonstração simples de aceitação e captura.

A organização do autômato segue os mesmos elementos do exemplo do professor:

- estados (Q);
- alfabeto (Σ);
- transições (δ);
- estado inicial (q0);
- estados finais (F).

Na DrawLang, também preservamos grupos de captura para recuperar valores como `$1` e `$2`.
