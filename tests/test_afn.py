from src.afn import Afn, EPSILON, QUALQUER, construirAfn, lerPadroes
from src.regex_parser import analisar_regex, ErroRegex


def testar_exemplo_professor():
    afn = Afn()
    for _ in range(3):
        afn.novoEstado()
    afn.definirInicial(0)
    afn.definirAceitacao(2)
    afn.adicionarTransicao(0, "a", 0)
    afn.adicionarTransicao(0, EPSILON, 1)
    afn.adicionarTransicao(1, "b", 2)
    aceita, passos, maior = afn.simular("ab")
    assert aceita and passos[0][1] == {0, 1} and maior == 2
    assert afn.quantidadeDeEstados() == 3
    assert afn.quantidadeDeTransicoes() == 3
    assert afn.quantidadeDeTransicoesVazias() == 1


def testar_ciclo_e_coringa():
    afn = construirAfn(analisar_regex(".*a"))
    assert afn.simular("xyz a")[0]
    assert not afn.simular("xyz")[0]
    assert construirAfn(analisar_regex(r"a\.b")).simular("a.b")[0]
    assert not construirAfn(analisar_regex(r"a\.b")).simular("acb")[0]


def testar_pontos():
    afn = construirAfn(analisar_regex("([0-9]+),([0-9]+)"))
    for linha in ("10,20", "7,8"):
        assert afn.simular(linha)[0]
    for linha in ("oi", "7,", "12;34"):
        assert not afn.simular(linha)[0]
    assert construirAfn(analisar_regex(r"\d+")).simular("123")[0]


def testar_erro():
    try:
        analisar_regex("abcd(")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 5


if __name__ == "__main__":
    testar_exemplo_professor()
    testar_ciclo_e_coringa()
    testar_pontos()
    testar_erro()
