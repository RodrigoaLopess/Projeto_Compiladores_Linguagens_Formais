from src.regex_parser import analisar_regex
from src.automato import construirAutomato


def testar_automato():
    ast = analisar_regex(r"(\\d+),(\\d+)")
    automato = construirAutomato(ast)

    assert automato.aceita("12,34")
    assert not automato.aceita("12-34")

    capturas = automato.executar("123,45")
    assert capturas == {1: "123", 2: "45"}


if __name__ == "__main__":
    testar_automato()
    print("teste automato: ok")
