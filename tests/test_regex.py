from src.regex_parser import ErroRegex, analisar_regex


def testar_validas():
    analisar_regex("ab")
    analisar_regex("a|b")
    analisar_regex("a*")
    analisar_regex("a(b|c)")


def testar_erros():
    try:
        analisar_regex("*ab")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 0

    try:
        analisar_regex("a(b")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 3


if __name__ == "__main__":
    testar_validas()
    testar_erros()
    print("testes ok")
