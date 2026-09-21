from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class Transicao:
    proximoEstado: int
    tipo: str
    simbolo: object = None
    acoes: tuple = ()


class Automato:
    """
    Estrutura equivalente ao AFD fornecido pelo professor:

      Q  -> estados
      Σ  -> alfabeto
      δ  -> transicoes
      q0 -> estadoInicial
      F  -> estadosFinais

    A DrawLang usa transicoes epsilon porque precisa preservar capturas.
    """

    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = defaultdict(list)
        self.estadoInicial = None
        self.estadosFinais = set()
        self._proximo = 0

    def adicionarEstado(self):
        estado = self._proximo
        self._proximo += 1
        self.estados.add(estado)
        return estado

    def adicionarSimbolo(self, simbolo):
        self.alfabeto.add(simbolo)

    def definirEstadoInicial(self, estado):
        self.estadoInicial = estado

    def adicionarEstadoFinal(self, estado):
        self.estadosFinais.add(estado)

    def adicionarTransicao(self, estado, proximoEstado, tipo="epsilon",
                           simbolo=None, acoes=()):
        self.transicoes[estado].append(
            Transicao(proximoEstado, tipo, simbolo, tuple(acoes))
        )

    def aceita(self, palavra):
        return self.executar(palavra) is not None

    def executar(self, palavra):
        configuracoes = self._fechoEpsilon([(self.estadoInicial, {})], 0)

        for posicao, caractere in enumerate(palavra):
            proximas = []

            for estado, capturas in configuracoes:
                for transicao in self.transicoes.get(estado, []):
                    if self._consome(transicao, caractere):
                        proximas.append(
                            (transicao.proximoEstado, dict(capturas))
                        )

            configuracoes = self._fechoEpsilon(proximas, posicao + 1)

            if not configuracoes:
                return None

        finais = self._fechoEpsilon(configuracoes, len(palavra))

        for estado, capturas in finais:
            if estado in self.estadosFinais:
                return self._extrairCapturas(capturas, palavra)

        return None

    def _consome(self, transicao, caractere):
        if transicao.tipo == "simbolo":
            return caractere == transicao.simbolo

        if transicao.tipo == "classe" and transicao.simbolo == "digito":
            return caractere.isdigit()

        return False

    def _fechoEpsilon(self, configuracoes, posicao):
        fila = deque(configuracoes)
        resultado = []
        vistos = set()

        while fila:
            estado, capturas = fila.popleft()
            chave = (estado, tuple(sorted(capturas.items())))

            if chave in vistos:
                continue

            vistos.add(chave)
            resultado.append((estado, capturas))

            for transicao in self.transicoes.get(estado, []):
                if transicao.tipo == "epsilon":
                    novas = dict(capturas)

                    for acao, grupo in transicao.acoes:
                        inicio, fim = novas.get(grupo, (None, None))

                        if acao == "inicio":
                            novas[grupo] = (posicao, None)
                        elif acao == "fim":
                            novas[grupo] = (inicio, posicao)

                    fila.append((transicao.proximoEstado, novas))

        return resultado

    def _extrairCapturas(self, capturas, palavra):
        resultado = {}

        for grupo, (inicio, fim) in capturas.items():
            if inicio is not None and fim is not None:
                resultado[grupo] = palavra[inicio:fim]

        return resultado


class ConstrutorAutomato:
    def __init__(self):
        self.automato = Automato()

    def construir(self, arvore):
        inicio, fim = self._fragmento(arvore)
        self.automato.definirEstadoInicial(inicio)
        self.automato.adicionarEstadoFinal(fim)
        return self.automato

    def _novo(self):
        return self.automato.adicionarEstado()

    def _fragmento(self, no):
        tipo = no[0]

        if tipo == "simbolo":
            inicio, fim = self._novo(), self._novo()
            self.automato.adicionarSimbolo(no[1])
            self.automato.adicionarTransicao(
                inicio, fim, "simbolo", no[1]
            )
            return inicio, fim

        if tipo == "classe":
            inicio, fim = self._novo(), self._novo()
            self.automato.adicionarSimbolo(no[1])
            self.automato.adicionarTransicao(
                inicio, fim, "classe", no[1]
            )
            return inicio, fim

        if tipo == "vazio":
            inicio, fim = self._novo(), self._novo()
            self.automato.adicionarTransicao(inicio, fim)
            return inicio, fim

        if tipo == ".":
            a1, a2 = self._fragmento(no[1])
            b1, b2 = self._fragmento(no[2])
            self.automato.adicionarTransicao(a2, b1)
            return a1, b2

        if tipo == "|":
            inicio, fim = self._novo(), self._novo()
            a1, a2 = self._fragmento(no[1])
            b1, b2 = self._fragmento(no[2])

            self.automato.adicionarTransicao(inicio, a1)
            self.automato.adicionarTransicao(inicio, b1)
            self.automato.adicionarTransicao(a2, fim)
            self.automato.adicionarTransicao(b2, fim)

            return inicio, fim

        if tipo == "*":
            inicio, fim = self._novo(), self._novo()
            a1, a2 = self._fragmento(no[1])

            self.automato.adicionarTransicao(inicio, fim)
            self.automato.adicionarTransicao(inicio, a1)
            self.automato.adicionarTransicao(a2, a1)
            self.automato.adicionarTransicao(a2, fim)

            return inicio, fim

        if tipo == "captura":
            grupo = no[1]
            inicio, fim = self._novo(), self._novo()
            a1, a2 = self._fragmento(no[2])

            self.automato.adicionarTransicao(
                inicio, a1, acoes=(("inicio", grupo),)
            )
            self.automato.adicionarTransicao(
                a2, fim, acoes=(("fim", grupo),)
            )

            return inicio, fim

        raise ValueError(f"no desconhecido: {tipo}")


def construirAutomato(arvore):
    return ConstrutorAutomato().construir(arvore)
