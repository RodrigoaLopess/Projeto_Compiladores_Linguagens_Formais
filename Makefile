SHELL := /bin/sh

.PHONY: test run afn

test:
	@python -m tests.test_regex
	@python -m tests.test_afn
	@python -m tests.test_automato

run:
	@python main.py

afn:
	@python -m src.afn
