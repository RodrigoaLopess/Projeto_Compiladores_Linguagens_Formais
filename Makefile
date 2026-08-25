SHELL := /bin/sh

.PHONY: test

test:
	@python -m tests.test_regex
