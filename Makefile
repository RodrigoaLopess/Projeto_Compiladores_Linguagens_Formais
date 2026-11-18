SHELL := /bin/sh

.PHONY: test run

test:
	@python -m tests.test_regex
	@python -m tests.test_automato
	@python -m tests.test_afn
	@python -m tests.test_afd

run:
	@python main.py
