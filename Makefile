.PHONY: help install install-dev test lint format type-check clean build publish build-upgrade

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
	@echo "  build-upgrade Upgrade the package version and build it"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	flake8 hyperevals/

format:
	black hyperevals/
	isort hyperevals/

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

build-upgrade:
	@echo "Upgrading version..."
	@current_version=$$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/'); \
	major=$$(echo $$current_version | cut -d. -f1); \
	minor=$$(echo $$current_version | cut -d. -f2); \
	patch=$$(echo $$current_version | cut -d. -f3); \
	new_patch=$$((patch + 1)); \
	new_version="$$major.$$minor.$$new_patch"; \
	echo "Upgrading from $$current_version to $$new_version"; \
	sed -i.bak "s/^version = \"$$current_version\"/version = \"$$new_version\"/" pyproject.toml && rm pyproject.toml.bak; \
	$(MAKE) build

publish: build
	python -m twine upload dist/*

# Development workflow
dev-setup: install-dev
	@echo "Development environment set up successfully!"

check: lint type-check test
	@echo "All checks passed!" 