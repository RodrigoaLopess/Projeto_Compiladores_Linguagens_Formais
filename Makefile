SHELL := /bin/sh

.PHONY: test

test:
	@test -f docs/01_recorte.md
	@test -f docs/02_gramatica.txt
	@test -f exemplos/exemplo01.drw
	@test -f exemplos/exemplo01_esperado.md
	@echo "Projeto verificado."
