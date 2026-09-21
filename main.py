from src.regex_parser import analisar_regex
from src.automato import construirAutomato


def main():
    regex = r"(\\d+),(\\d+)"
    entrada = "12,34"

    arvore = analisar_regex(regex)
    automato = construirAutomato(arvore)

    print("Regex:", regex)
    print("Entrada:", entrada)
    print()
    print("Q =", automato.estados)
    print("Sigma =", automato.alfabeto)
    print("q0 =", automato.estadoInicial)
    print("F =", automato.estadosFinais)
    print()

    capturas = automato.executar(entrada)

    if capturas is not None:
        print("ACEITA")
        print("$1 =", capturas.get(1))
        print("$2 =", capturas.get(2))
    else:
        print("REJEITADA")


if __name__ == "__main__":
    main()
