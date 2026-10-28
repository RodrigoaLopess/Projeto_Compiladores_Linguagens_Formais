from dataclasses import dataclass, field


EPSILON = "ε"   # transicao vazia
QUALQUER = "."  # coringa: casa com qualquer simbolo (menos ε)


@dataclass
class TransicaoAfn:
    simbolo: str   # simbolo, ε ou coringa
    destino: int   # estado de destino


@dataclass
class Passo:
    simbolo: str   # simbolo lido ("" no passo inicial)
    ativos: list   # estados ativos depois de ler o simbolo


@dataclass
class Simulacao:
    passos: list = field(default_factory=list)
    maiorConjuntoAtivo: int = 0
    aceita: bool = False


class Afn:
    def __init__(self):
        self.transicoes = []  # transicoes[estado] = lista de TransicaoAfn
        self.inicial = None
        self.aceitacao = None

    # ---------- criacao e configuracao ----------

    def novoEstado(self):
        self.transicoes.append([])
        return len(self.transicoes) - 1

    def adicionarTransicao(self, origem, simbolo, destino):
        self.transicoes[origem].append(TransicaoAfn(simbolo, destino))

    def definirInicial(self, estado):
        self.inicial = estado

    def definirAceitacao(self, estado):
        self.aceitacao = estado

    def quantidadeDeEstados(self):
        return len(self.transicoes)

    def quantidadeDeTransicoes(self):
        total = 0
        for saidas in self.transicoes:
            total += len(saidas)
        return total

    def quantidadeDeTransicoesVazias(self):
        total = 0
        for saidas in self.transicoes:
            for t in saidas:
                if t.simbolo == EPSILON:
                    total += 1
        return total

    # ---------- fecho-ε ----------

    def fechoVazio(self, conjunto):
        visitado = [False] * len(self.transicoes)
        pilha = []
        resultado = []

        # 1. adiciona os estados do conjunto inicial
        for estado in conjunto:
            if not visitado[estado]:
                visitado[estado] = True
                pilha.append(estado)
                resultado.append(estado)

        # 2. busca em profundidade pelas transicoes ε
        while pilha:
            estado = pilha.pop()

            for t in self.transicoes[estado]:
                # 3. o vetor visitado evita ficar preso em ciclos
                if t.simbolo == EPSILON and not visitado[t.destino]:
                    visitado[t.destino] = True
                    pilha.append(t.destino)
                    resultado.append(t.destino)

        # 4. todos os estados alcancaveis por ε
        resultado.sort()
        return resultado

    # ---------- simulacao ----------

    def simular(self, cadeia):
        simulacao = Simulacao()

        # comeca com o fecho-ε do inicial, nao so com o inicial
        ativos = self.fechoVazio([self.inicial])
        simulacao.passos.append(Passo("", ativos))
        simulacao.maiorConjuntoAtivo = len(ativos)

        for simbolo in cadeia:
            presente = [False] * len(self.transicoes)
            proximos = []

            for estado in ativos:
                for t in self.transicoes[estado]:
                    casa = t.simbolo == simbolo or t.simbolo == QUALQUER

                    # o vetor presente tira os repetidos
                    if casa and not presente[t.destino]:
                        presente[t.destino] = True
                        proximos.append(t.destino)

            ativos = self.fechoVazio(proximos)
            simulacao.passos.append(Passo(simbolo, ativos))

            if len(ativos) > simulacao.maiorConjuntoAtivo:
                simulacao.maiorConjuntoAtivo = len(ativos)

            if not ativos:
                break

        simulacao.aceita = self.aceitacao in ativos
        return simulacao

    def aceita(self, cadeia):
        return self.simular(cadeia).aceita


# ---------- AFN a partir da arvore do regex_parser (Thompson) ----------

def construirAfn(arvore):
    afn = Afn()
    inicio, fim = _fragmento(afn, arvore)
    afn.definirInicial(inicio)
    afn.definirAceitacao(fim)
    return afn


def _fragmento(afn, no):
    tipo = no[0]

    if tipo == "simbolo":
        inicio = afn.novoEstado()
        fim = afn.novoEstado()
        # o "." da regex vira o coringa
        simbolo = QUALQUER if no[1] == "." else no[1]
        afn.adicionarTransicao(inicio, simbolo, fim)
        return inicio, fim

    if tipo == "vazio":
        inicio = afn.novoEstado()
        fim = afn.novoEstado()
        afn.adicionarTransicao(inicio, EPSILON, fim)
        return inicio, fim

    if tipo == ".":
        a1, a2 = _fragmento(afn, no[1])
        b1, b2 = _fragmento(afn, no[2])
        afn.adicionarTransicao(a2, EPSILON, b1)
        return a1, b2

    if tipo == "|":
        inicio = afn.novoEstado()
        a1, a2 = _fragmento(afn, no[1])
        b1, b2 = _fragmento(afn, no[2])
        fim = afn.novoEstado()
        afn.adicionarTransicao(inicio, EPSILON, a1)
        afn.adicionarTransicao(inicio, EPSILON, b1)
        afn.adicionarTransicao(a2, EPSILON, fim)
        afn.adicionarTransicao(b2, EPSILON, fim)
        return inicio, fim

    if tipo == "*":
        inicio = afn.novoEstado()
        a1, a2 = _fragmento(afn, no[1])
        fim = afn.novoEstado()
        afn.adicionarTransicao(inicio, EPSILON, a1)
        afn.adicionarTransicao(inicio, EPSILON, fim)
        afn.adicionarTransicao(a2, EPSILON, a1)
        afn.adicionarTransicao(a2, EPSILON, fim)
        return inicio, fim

    raise ValueError(f"no desconhecido: {tipo}")


def mostrarSimulacao(simulacao):
    for passo in simulacao.passos:
        simbolo = passo.simbolo if passo.simbolo else EPSILON
        print(f"le {simbolo!r:5} -> ativos {set(passo.ativos) or '{}'}")

    print("maior conjunto ativo:", simulacao.maiorConjuntoAtivo)
    print("ACEITA" if simulacao.aceita else "REJEITA")


def exemploProfessor():
    # AFN do padrao a*b: 0 --a--> 0, 0 --ε--> 1, 1 --b--> 2
    afn = Afn()
    q0 = afn.novoEstado()
    q1 = afn.novoEstado()
    q2 = afn.novoEstado()

    afn.adicionarTransicao(q0, "a", q0)
    afn.adicionarTransicao(q0, EPSILON, q1)
    afn.adicionarTransicao(q1, "b", q2)

    afn.definirInicial(q0)
    afn.definirAceitacao(q2)
    return afn


if __name__ == "__main__":
    afn = exemploProfessor()
    print("AFN a*b")
    print("estados:", afn.quantidadeDeEstados())
    print("transicoes:", afn.quantidadeDeTransicoes())
    print("transicoes vazias:", afn.quantidadeDeTransicoesVazias())
    print()
    mostrarSimulacao(afn.simular("ab"))
