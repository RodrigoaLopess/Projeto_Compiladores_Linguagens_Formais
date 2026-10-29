class ErroRegex(Exception):
    def __init__(self, posicao, mensagem, expressao=None):
        self.posicao = posicao
        self.mensagem = mensagem
        self.expressao = expressao
        super().__init__(mensagem)

    def __str__(self):
        if self.expressao is None:
            return f"{self.mensagem} na posicao {self.posicao}"
        return f"{self.expressao}\n{' ' * self.posicao}^\n{self.mensagem}"


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
        if not self.texto:
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
        if not partes:
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

    def digitos(self):
        arvore = ("simbolo", "0")
        for digito in "123456789":
            arvore = ("|", arvore, ("simbolo", digito))
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
            if self.texto[self.pos:self.pos + 5] != "[0-9]":
                self.erro("classe de caracteres invalida")
            self.pos += 5
            return self.digitos()
        if caractere == "\\":
            self.pos += 1
            seguinte = self.atual()
            if seguinte is None:
                self.erro("faltou caractere apos barra")
            self.pos += 1
            if seguinte == "d":
                return self.digitos()
            return ("simbolo", seguinte)
        self.pos += 1
        if caractere == ".":
            return ("qualquer",)
        return ("simbolo", caractere)


def analisar_regex(texto):
    return ParserRegex(texto).ler()
