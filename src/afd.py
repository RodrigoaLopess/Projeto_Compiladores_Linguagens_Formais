"""Determinização e minimização de autômatos."""

from collections import deque
from .afn import QUALQUER


class Afd:
    def __init__(self, alfabeto):
        self.alfabeto = tuple(sorted(set(alfabeto)))
        self.transicoes = []
        self.aceitacao = set()
        self.subconjuntos = []
        self.inicial = 0

    def simular(self, cadeia):
        estado = self.inicial
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False
            estado = self.transicoes[estado].get(simbolo)
            if estado is None:
                return False
        return estado in self.aceitacao

    def completar(self):
        erro = None
        for linha in self.transicoes:
            for simbolo in self.alfabeto:
                if simbolo not in linha:
                    if erro is None:
                        erro = len(self.transicoes)
                    linha[simbolo] = erro
        if erro is not None:
            self.transicoes.append({s: erro for s in self.alfabeto})
            self.subconjuntos.append(frozenset())
        return self


def determinizar(afn, alfabeto):
    afd = Afd(alfabeto)
    inicial = frozenset(afn.fechoVazio({afn.inicial}))
    indices = {inicial: 0}
    afd.subconjuntos.append(inicial)
    afd.transicoes.append({})
    fila = deque([inicial])
    while fila:
        conjunto = fila.popleft()
        origem = indices[conjunto]
        if afn.aceitacao in conjunto:
            afd.aceitacao.add(origem)
        for simbolo in afd.alfabeto:
            destinos = {
                t.destino for estado in conjunto
                for t in afn.transicoes[estado]
                if t.simbolo == simbolo or t.simbolo == QUALQUER
            }
            proximo = frozenset(afn.fechoVazio(destinos))
            if proximo not in indices:
                indices[proximo] = len(afd.transicoes)
                afd.transicoes.append({})
                afd.subconjuntos.append(proximo)
                fila.append(proximo)
            afd.transicoes[origem][simbolo] = indices[proximo]
    return afd


def minimizar(original):
    afd = Afd(original.alfabeto)
    afd.transicoes = [dict(linha) for linha in original.transicoes]
    afd.aceitacao = set(original.aceitacao)
    afd.subconjuntos = list(original.subconjuntos)
    afd.inicial = original.inicial
    afd.completar()

    alcancaveis = {afd.inicial}
    fila = deque([afd.inicial])
    while fila:
        for destino in afd.transicoes[fila.popleft()].values():
            if destino not in alcancaveis:
                alcancaveis.add(destino)
                fila.append(destino)

    finais = alcancaveis & afd.aceitacao
    nao_finais = alcancaveis - finais
    partes = [p for p in (finais, nao_finais) if p]
    while True:
        grupo = {estado: i for i, parte in enumerate(partes) for estado in parte}
        novas = []
        for parte in partes:
            blocos = {}
            for estado in sorted(parte):
                assinatura = tuple(grupo[afd.transicoes[estado][s]] for s in afd.alfabeto)
                blocos.setdefault(assinatura, set()).add(estado)
            novas.extend(blocos.values())
        if len(novas) == len(partes):
            partes = novas
            break
        partes = novas

    grupo = {estado: i for i, parte in enumerate(partes) for estado in parte}
    minimo = Afd(afd.alfabeto)
    minimo.inicial = grupo[afd.inicial]
    for i, parte in enumerate(partes):
        representante = min(parte)
        minimo.transicoes.append({s: grupo[afd.transicoes[representante][s]] for s in afd.alfabeto})
        minimo.subconjuntos.append(frozenset(parte))
        if parte & afd.aceitacao:
            minimo.aceitacao.add(i)
    return minimo
