.PHONY: help install test clean lint format docs example

help:  ## Show this help message
	@echo "NenDB - Available Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

test:  ## Run tests
	python run_tests.py

test-coverage:  ## Run tests with coverage
	pytest --cov=nen_python_driver tests/ --cov-report=html

lint:  ## Run linting checks
	flake8 src/ tests/
	mypy src/

format:  ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

docs:  ## Build documentation
	cd docs && make html

example:  ## Run the basic usage example
	python examples/basic_usage.py

package:  ## Build distribution packages
	python setup.py sdist bdist_wheel

publish:  ## Publish to PyPI (requires twine)
	twine upload dist/*

dev-setup: install install-dev  ## Set up development environment
	pre-commit install
