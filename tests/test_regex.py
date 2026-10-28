from src.regex_parser import ErroRegex, analisar_regex


def testar_validas():
    assert analisar_regex("ab") == (
        ".",
        ("simbolo", "a"),
        ("simbolo", "b"),
    )

    assert analisar_regex("a|b") == (
        "|",
        ("simbolo", "a"),
        ("simbolo", "b"),
    )

    assert analisar_regex("a*") == (
        "*",
        ("simbolo", "a"),
    )

    analisar_regex("a(b|c)")


def testar_reducoes():
    assert analisar_regex("a+") == (
        ".",
        ("simbolo", "a"),
        ("*", ("simbolo", "a")),
    )

    assert analisar_regex("a?") == (
        "|",
        ("simbolo", "a"),
        ("vazio",),
    )

    arvore = analisar_regex("(ab)+")
    grupo = (
        ".",
        ("simbolo", "a"),
        ("simbolo", "b"),
    )

    assert arvore == (
        ".",
        grupo,
        ("*", grupo),
    )


def testar_erros():
    try:
        analisar_regex("*ab")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 0
        assert str(erro) == "*ab\n^\noperador sem expressao"

    try:
        analisar_regex("a(b")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 3
        assert str(erro) == "a(b\n   ^\nfaltou fechar parenteses"


def testar_classes_drawlang():
    assert analisar_regex("[0-2]") == (
        "|",
        ("simbolo", "0"),
        ("|", ("simbolo", "1"), ("simbolo", "2")),
    )

    assert analisar_regex(r"\d") == analisar_regex("[0-9]")
    assert analisar_regex(r"\.") == ("simbolo", ".")
    assert analisar_regex(".") == ("qualquer",)

    try:
        analisar_regex("[0-9")
        assert False
    except ErroRegex as erro:
        assert erro.posicao == 4
        assert erro.mensagem == "faltou fechar colchete"


if __name__ == "__main__":
    testar_validas()
    testar_reducoes()
    testar_erros()
    testar_classes_drawlang()
    print("testes ok")
