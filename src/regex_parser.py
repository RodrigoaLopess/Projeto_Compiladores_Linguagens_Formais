class ErroRegex(Exception):
    def __init__(self, posicao, mensagem):
        self.posicao = posicao
        self.mensagem = mensagem


class ParserRegex:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0

    def atual(self):
        if self.pos >= len(self.texto):
            return None
        return self.texto[self.pos]

    def ler(self):
        if self.texto == "":
            raise ErroRegex(0, "expressao vazia")

        arvore = self.alternancia()

        if self.pos != len(self.texto):
            raise ErroRegex(self.pos, "simbolo inesperado")

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
            raise ErroRegex(self.pos, "faltou expressao")

        arvore = partes[0]

        for parte in partes[1:]:
            arvore = (".", arvore, parte)

        return arvore

    def repeticao(self):
        arvore = self.atomo()

        while self.atual() in ("*", "+", "?"):
            operador = self.atual()
            self.pos += 1
            arvore = (operador, arvore)

        return arvore

    def atomo(self):
        caractere = self.atual()

        if caractere is None:
            raise ErroRegex(self.pos, "faltou expressao")

        if caractere in "*+?":
            raise ErroRegex(self.pos, "operador sem expressao")

        if caractere == "(":
            self.pos += 1
            arvore = self.alternancia()

            if self.atual() != ")":
                raise ErroRegex(self.pos, "faltou fechar parenteses")

            self.pos += 1
            return arvore

        self.pos += 1
        return ("simbolo", caractere)


def analisar_regex(texto):
    return ParserRegex(texto).ler()
