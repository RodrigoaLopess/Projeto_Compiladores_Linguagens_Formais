class ErroRegex(Exception):
    def __init__(self, posicao, mensagem, expressao=None):
        self.posicao = posicao
        self.mensagem = mensagem
        self.expressao = expressao
        super().__init__(mensagem)

    def __str__(self):
        if self.expressao is None:
            return f"{self.mensagem} na posicao {self.posicao}"

        marcador = " " * self.posicao + "^"
        return f"{self.expressao}\n{marcador}\n{self.mensagem}"


class ParserRegex:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0

    def erro(self, mensagem):
        raise ErroRegex(self.pos, mensagem, self.texto)

    def atual(self):
        if self.pos >= len(self.texto):
            return None
        return self.texto[self.pos]

    def ler(self):
        if self.texto == "":
            self.erro("expressao vazia")

        arvore = self.alternancia()

        if self.pos != len(self.texto):
            self.erro("simbolo inesperado")

        return arvore

    def alternancia(self):
        esquerda = self.concatenacao()

        while self.atual() == "|":
            self.pos += 1
            direita = self.concatenacao()
            esquerda = ("|", esquerda, direita)

        return esquerda

    def concatenacao(self):
        partes = []

        while self.atual() is not None and self.atual() not in "|)":
            partes.append(self.repeticao())

        if len(partes) == 0:
            self.erro("faltou expressao")

        arvore = partes[0]

        for parte in partes[1:]:
            arvore = (".", arvore, parte)

        return arvore

    def repeticao(self):
        arvore = self.atomo()

        while self.atual() in ("*", "+", "?"):
            operador = self.atual()
            self.pos += 1

            if operador == "*":
                arvore = ("*", arvore)
            elif operador == "+":
                arvore = (".", arvore, ("*", arvore))
            else:
                arvore = ("|", arvore, ("vazio",))

        return arvore

    def atomo(self):
        caractere = self.atual()

        if caractere is None:
            self.erro("faltou expressao")

        if caractere in "*+?":
            self.erro("operador sem expressao")

        if caractere == "(":
            self.pos += 1
            arvore = self.alternancia()

            if self.atual() != ")":
                self.erro("faltou fechar parenteses")

            self.pos += 1
            return arvore

        if caractere == "[":
            return self.classe()

        if caractere == "\\":
            return self.escape()

        if caractere == ".":
            self.pos += 1
            return ("qualquer",)

        self.pos += 1
        return ("simbolo", caractere)

    def classe(self):
        # [0-9] vira alt('0', alt('1', ...)), igual ao D da atividade
        self.pos += 1
        simbolos = []

        while self.atual() is not None and self.atual() != "]":
            inicio = self.atual()
            self.pos += 1

            if self.atual() == "-" and self.pos + 1 < len(self.texto) \
                    and self.texto[self.pos + 1] != "]":
                fim = self.texto[self.pos + 1]
                self.pos += 2

                if fim < inicio:
                    self.erro("intervalo invalido")

                for codigo in range(ord(inicio), ord(fim) + 1):
                    simbolos.append(chr(codigo))
            else:
                simbolos.append(inicio)

        if self.atual() != "]":
            self.erro("faltou fechar colchete")

        if len(simbolos) == 0:
            self.erro("classe vazia")

        self.pos += 1
        return alternativas(simbolos)

    def escape(self):
        # \d = digito; \. \/ \( ... = o proprio simbolo
        self.pos += 1
        caractere = self.atual()

        if caractere is None:
            self.erro("faltou simbolo depois da barra")

        self.pos += 1

        if caractere == "d":
            return alternativas("0123456789")

        return ("simbolo", caractere)


def alternativas(simbolos):
    arvore = ("simbolo", simbolos[-1])

    for simbolo in reversed(simbolos[:-1]):
        arvore = ("|", ("simbolo", simbolo), arvore)

    return arvore


def analisar_regex(texto):
    return ParserRegex(texto).ler()
