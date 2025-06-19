.PHONY: help install install-dev test lint format type-check clean build publish

help:
	@echo "Available commands:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install the package in development mode with dev dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code (black, isort)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  publish      Publish to PyPI"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	flake8 hyperevals/ tests/

format:
	black hyperevals/ tests/
	isort hyperevals/ tests/

type-check:
	mypy hyperevals/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

# Development workflow
dev-setup: install-dev
	@echo "Development environment set up successfully!"

check: lint type-check test
	@echo "All checks passed!" 