# Makefile for delegate-skills
SHELL := /usr/bin/env bash
VERSION ?= $(shell python3 -c 'import json; print(json.load(open("plugin.json"))["version"])' 2>/dev/null || echo "1.0.0")

.PHONY: all test lint install install-all install-antigravity install-claude install-codex install-omp install-orca uninstall dist clean

all: test

test:
	python3 -m unittest discover -s tests -p "test_*.py"

lint:
	python3 -m py_compile skills/delegate/scripts/*.py tests/*.py

install:
	./install.sh

install-all:
	./install.sh --harness all

install-antigravity:
	./install.sh --harness antigravity

install-claude:
	./install.sh --harness claude

install-codex:
	./install.sh --harness codex

install-omp:
	./install.sh --harness omp

install-orca:
	./install.sh --harness orca

uninstall:
	./install.sh --uninstall

dist: clean
	mkdir -p dist
	tar -czf dist/delegate-skills.tar.gz \
		--exclude='*.pyc' \
		--exclude='__pycache__' \
		--exclude='.git*' \
		--exclude='dist' \
		plugin.json \
		README.md \
		install.sh \
		bin \
		commands \
		rules \
		skills
	@echo "Built release package: dist/delegate-skills.tar.gz (version $(VERSION))"

clean:
	rm -rf dist
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
