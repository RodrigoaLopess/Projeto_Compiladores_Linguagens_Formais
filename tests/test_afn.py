from src.regex_parser import analisar_regex
from src.afn import (
    EPSILON, QUALQUER, Afn, construirAfn, exemploProfessor, padroesDoPrograma
)


def testar_exemplo_professor():
    afn = exemploProfessor()

    assert afn.quantidadeDeEstados() == 3
    assert afn.quantidadeDeTransicoes() == 3
    assert afn.quantidadeDeTransicoesVazias() == 1

    simulacao = afn.simular("ab")

    assert simulacao.aceita
    assert [p.ativos for p in simulacao.passos] == [[0, 1], [0, 1], [2]]
    assert [p.simbolo for p in simulacao.passos] == ["", "a", "b"]
    assert simulacao.maiorConjuntoAtivo == 2


def testar_fecho_vazio():
    afn = exemploProfessor()

    assert afn.fechoVazio([0]) == [0, 1]
    assert afn.fechoVazio([2]) == [2]


def testar_fecho_com_ciclo():
    afn = Afn()
    q0 = afn.novoEstado()
    q1 = afn.novoEstado()
    afn.adicionarTransicao(q0, EPSILON, q1)
    afn.adicionarTransicao(q1, EPSILON, q0)

    assert afn.fechoVazio([q0]) == [0, 1]


def testar_rejeita_e_para():
    afn = exemploProfessor()

    assert afn.aceita("b")
    assert afn.aceita("aaab")
    assert not afn.aceita("")
    assert not afn.aceita("ba")

    # depois de ficar sem estados ativos a simulacao para
    simulacao = afn.simular("cab")
    assert simulacao.passos[-1].ativos == []
    assert len(simulacao.passos) == 2


def testar_coringa():
    afn = Afn()
    q0 = afn.novoEstado()
    q1 = afn.novoEstado()
    afn.adicionarTransicao(q0, QUALQUER, q1)
    afn.definirInicial(q0)
    afn.definirAceitacao(q1)

    assert afn.aceita("x")
    assert afn.aceita("7")
    assert not afn.aceita("")
    assert not afn.aceita("xy")


def testar_afn_da_regex():
    afn = construirAfn(analisar_regex("a*b"))

    assert afn.aceita("b")
    assert afn.aceita("aab")
    assert not afn.aceita("aa")

    afn = construirAfn(analisar_regex("(ab|c)+"))

    assert afn.aceita("ab")
    assert afn.aceita("cabc")
    assert not afn.aceita("")
    assert not afn.aceita("ac")

    afn = construirAfn(analisar_regex("a.c"))

    assert afn.aceita("abc")
    assert afn.aceita("a9c")
    assert not afn.aceita("ac")


def testar_padrao_drawlang():
    # padrao do exemplo captura_pontos.drw
    with open("exemplos/captura_pontos.drw") as arquivo:
        padroes = padroesDoPrograma(arquivo.read())

    assert padroes == ["([0-9]+),([0-9]+)"]

    afn = construirAfn(analisar_regex(padroes[0]))

    assert afn.aceita("10,20")
    assert afn.aceita("150,40")
    assert not afn.aceita("oi")
    assert not afn.aceita("7,")
    assert not afn.aceita("12;34")

    simulacao = afn.simular("7,")
    assert [p.simbolo for p in simulacao.passos] == ["", "7", ","]
    assert not simulacao.aceita


def testar_numero_drawlang():
    # numero da DrawLang: [0-9]+(\.[0-9]+)?
    afn = construirAfn(analisar_regex(r"[0-9]+(\.[0-9]+)?"))

    assert afn.aceita("100")
    assert afn.aceita("2.5")
    assert not afn.aceita("2.")
    assert not afn.aceita("2x5")  # \. e ponto, nao coringa

    afn = construirAfn(analisar_regex(r"\d+"))
    assert afn.aceita("45")


def testar_padroes_do_programa():
    texto = (
        "INICIO\n"
        "quando linha casa /[0-9]+/ entao\n"
        "    MOVER $1;\n"
        "FIM\n"
        "FIM\n"
    )

    assert padroesDoPrograma(texto) == ["[0-9]+"]


if __name__ == "__main__":
    testar_exemplo_professor()
    testar_fecho_vazio()
    testar_fecho_com_ciclo()
    testar_rejeita_e_para()
    testar_coringa()
    testar_afn_da_regex()
    testar_padrao_drawlang()
    testar_numero_drawlang()
    testar_padroes_do_programa()
    print("teste afn: ok")
