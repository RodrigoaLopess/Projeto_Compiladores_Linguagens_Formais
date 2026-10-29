"""AFN com transições vazias e construção de Thompson."""
from dataclasses import dataclass
from pathlib import Path
import re

from .regex_parser import analisar_regex

EPSILON = "ε"
QUALQUER = "<QUALQUER>"


@dataclass
class TransicaoAfn:
    simbolo: str
    destino: int


class Afn:
    def __init__(self):
        self.transicoes = []
        self.inicial = None
        self.aceitacao = None

    def novoEstado(self):
        numero = len(self.transicoes)
        self.transicoes.append([])
        return numero

    def adicionarTransicao(self, origem, simbolo, destino):
        self.transicoes[origem].append(TransicaoAfn(simbolo, destino))

    def definirInicial(self, estado):
        self.inicial = estado

    def definirAceitacao(self, estado):
        self.aceitacao = estado

    def quantidadeDeEstados(self):
        return len(self.transicoes)

    def quantidadeDeTransicoes(self):
        return sum(len(lista) for lista in self.transicoes)

    def quantidadeDeTransicoesVazias(self):
        return sum(t.simbolo == EPSILON for lista in self.transicoes for t in lista)

    def fechoVazio(self, conjunto):
        visitados = [False] * self.quantidadeDeEstados()
        pilha = list(conjunto)
        for estado in pilha:
            visitados[estado] = True
        while pilha:
            estado = pilha.pop()
            for transicao in self.transicoes[estado]:
                destino = transicao.destino
                if transicao.simbolo == EPSILON and not visitados[destino]:
                    visitados[destino] = True
                    pilha.append(destino)
        return {i for i, visitado in enumerate(visitados) if visitado}

    def simular(self, cadeia):
        ativos = self.fechoVazio({self.inicial})
        passos = [("ε", set(ativos))]
        maior = len(ativos)
        for simbolo in cadeia:
            destinos = set()
            for estado in ativos:
                for transicao in self.transicoes[estado]:
                    if transicao.simbolo == simbolo or transicao.simbolo == QUALQUER:
                        destinos.add(transicao.destino)
            ativos = self.fechoVazio(destinos)
            passos.append((simbolo, set(ativos)))
            maior = max(maior, len(ativos))
            if not ativos:
                break
        return self.aceitacao in ativos, passos, maior


def construirAfn(arvore):
    afn = Afn()

    def fragmento(no):
        tipo = no[0]
        if tipo == "captura":
            return fragmento(no[2])
        if tipo in ("simbolo", "qualquer", "vazio"):
            inicio, fim = afn.novoEstado(), afn.novoEstado()
            simbolo = no[1] if tipo == "simbolo" else QUALQUER if tipo == "qualquer" else EPSILON
            afn.adicionarTransicao(inicio, simbolo, fim)
            return inicio, fim
        if tipo == ".":
            a, b = fragmento(no[1])
            c, d = fragmento(no[2])
            afn.adicionarTransicao(b, EPSILON, c)
            return a, d
        if tipo == "|":
            inicio, fim = afn.novoEstado(), afn.novoEstado()
            a, b = fragmento(no[1])
            c, d = fragmento(no[2])
            for origem, destino in ((inicio, a), (inicio, c), (b, fim), (d, fim)):
                afn.adicionarTransicao(origem, EPSILON, destino)
            return inicio, fim
        if tipo == "*":
            inicio, fim = afn.novoEstado(), afn.novoEstado()
            a, b = fragmento(no[1])
            for origem, destino in ((inicio, fim), (inicio, a), (b, a), (b, fim)):
                afn.adicionarTransicao(origem, EPSILON, destino)
            return inicio, fim
        raise ValueError(f"nó desconhecido: {tipo}")

    inicio, fim = fragmento(arvore)
    afn.definirInicial(inicio)
    afn.definirAceitacao(fim)
    return afn


def lerPadroes(caminho):
    texto = Path(caminho).read_text(encoding="utf-8")
    return re.findall(r"QUANDO\s+LINHA\s+CASA\s*/((?:\\.|[^/])*)/", texto, re.IGNORECASE)


def main():
    base = Path(__file__).resolve().parent.parent / "exemplos"
    padroes = lerPadroes(base / "captura_pontos.drw")
    linhas = (base / "entrada_pontos_01.txt").read_text(encoding="utf-8").splitlines()
    for padrao in padroes:
        print("Padrão:", padrao)
        afn = construirAfn(analisar_regex(padrao))
        for linha in linhas:
            aceita, passos, maior = afn.simular(linha)
            print(f"{linha!r}: {'ACEITA' if aceita else 'REJEITA'} (maior conjunto: {maior})")
            for simbolo, ativos in passos:
                print(f"  {simbolo}: {sorted(ativos)}")


if __name__ == "__main__":
    main()
