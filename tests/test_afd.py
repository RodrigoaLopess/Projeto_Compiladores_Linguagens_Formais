from itertools import product

from src.afn import construirAfn
from src.afd import determinizar, minimizar
from src.regex_parser import analisar_regex


def cadeias(alfabeto, tamanho):
    for n in range(tamanho + 1):
        for letras in product(alfabeto, repeat=n):
            yield ''.join(letras)


def comparar(padrao, alfabeto, tamanho):
    afn = construirAfn(analisar_regex(padrao))
    afd = determinizar(afn, alfabeto)
    minimo = minimizar(afd)
    aceitas = 0
    total = 0
    for cadeia in cadeias(alfabeto, tamanho):
        resultados = (afn.simular(cadeia)[0], afd.simular(cadeia), minimo.simular(cadeia))
        assert resultados[0] == resultados[1] == resultados[2], (padrao, cadeia, resultados)
        total += 1
        aceitas += resultados[0]
    return afn, afd, minimo, total, aceitas


def testar_thompson():
    afn, afd, minimo, total, aceitas = comparar('(a|b)*c', 'abc', 4)
    assert (afn.quantidadeDeEstados(), afn.quantidadeDeTransicoes(),
            afn.quantidadeDeTransicoesVazias()) == (10, 12, 9)
    assert afn.simular('ababac')[0]
    assert not afn.simular('abab')[0]
    assert (total, aceitas) == (121, 15)
    assert len(afd.transicoes) == 5
    assert len(minimo.transicoes) == 3
    print('Thompson: 10 estados, 12 transições, 9 vazias')
    print(f'AFD: {len(afd.transicoes)} estados; mínimo: {len(minimo.transicoes)} estados')
    print(f'Cadeias verificadas: {total}; aceitas: {aceitas}')


def testar_operadores():
    casos = [
        ('a+', '', False), ('a+', 'aaa', True),
        ('ab?', 'a', True), ('ab?', 'abb', False),
        ('a(b|c)', 'ac', True), ('a(b|c)', 'ad', False),
        (r'a\\.b', 'a.b', True), (r'a\\.b', 'acb', False),
        ('[0-9]+', '123', True), ('[0-9]+', 'a', False),
        ('a.*b', 'axyb', True), ('a.*b', 'axy', False),
    ]
    for padrao, cadeia, esperado in casos:
        afn = construirAfn(analisar_regex(padrao))
        alfabeto = 'abcdefghijklmnopqrstuvwxyz0123456789.'
        afd = determinizar(afn, alfabeto)
        minimo = minimizar(afd)
        assert (afn.simular(cadeia)[0], afd.simular(cadeia), minimo.simular(cadeia)) == (esperado,) * 3
    for padrao in ('a*', 'a+', 'ab?', '(a|b)*c', 'a.*b', '[0-9]+'):
        comparar(padrao, 'abc012', 3)


def testar_crescimento():
    padrao = '(a|b)*a(a|b)(a|b)(a|b)'
    _, afd, minimo, _, _ = comparar(padrao, 'ab', 7)
    print(f'Crescimento: {padrao}')
    print(f'AFD antes: {len(afd.transicoes)}; depois: {len(minimo.transicoes)}')
    assert len(minimo.transicoes) == 16


if __name__ == '__main__':
    testar_thompson()
    testar_operadores()
    testar_crescimento()
    print('testes de autômatos ok')
