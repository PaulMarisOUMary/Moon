.PHONY: help build tests
.DEFAULT_GOAL=help

CURRENT_DIR=$(shell pwd)

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

tests: 
	@echo "Running tests (without building before)..."
	pytest

testsb: build
	@echo "Running tests..."
	pytest

build:
	@echo "Building..."
	pip3.11 install -r requirements.txt --quiet
	pip3.11 install -U . --quiet