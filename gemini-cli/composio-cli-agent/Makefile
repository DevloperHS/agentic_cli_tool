# Composio CLI Agent - Makefile

.PHONY: help install setup test run clean

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  setup      - Run setup check"
	@echo "  test       - Run tests"
	@echo "  run        - Run the CLI agent"
	@echo "  clean      - Clean up generated files"

install:
	pip install -r requirements.txt

setup:
	python scripts/setup.py

test:
	python -m pytest tests/ -v

test-integration:
	python -m pytest tests/ -v -m integration

run:
	python -m cli.main

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/

# Development commands
dev-install:
	pip install -r requirements.txt
	pip install black flake8 mypy

format:
	black .

lint:
	flake8 .

type-check:
	mypy .