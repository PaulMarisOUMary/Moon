.PHONY: help build tests
.DEFAULT_GOAL=help

CURRENT_DIR=$(shell pwd)

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

tests: # Run tests
	@echo "Running tests"
	pytest "tests" --doctest-modules --junitxml=junit/test-results.xml

testsb: build tests # Build and run tests

build: # Build the moon library for python3.11
	@echo "Building..."
	pip install -r requirements.txt --quiet
	pip install -U . --quiet