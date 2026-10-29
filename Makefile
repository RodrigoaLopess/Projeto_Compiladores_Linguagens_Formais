SHELL := /bin/sh

.PHONY: test run

test:
	@python -m tests.test_regex
	@python -m tests.test_automato

run:
	@python main.py
