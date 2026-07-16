.DEFAULT_GOAL := help

.PHONY: help sync install format lint test docs docs-clean build wheel check clean distclean

UV := uv
SPHINXBUILD := sphinx-build
DOCS_SOURCE := docs/source
DOCS_BUILD := docs/build/html

help: ## Show available commands.
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Synchronize the uv environment.
	$(UV) sync --all-groups

install: sync ## Alias for sync.

format: ## Format source, tests, and docs-aware config files.
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

lint: ## Run lint and formatting checks.
	$(UV) run ruff check .
	$(UV) run ruff format --check .

test: ## Run tests.
	$(UV) run pytest

docs: ## Build documentation strictly.
	$(UV) run $(SPHINXBUILD) -W -b html $(DOCS_SOURCE) $(DOCS_BUILD)

docs-clean: ## Remove generated documentation.
	rm -rf docs/build

build: ## Build wheel and source distribution.
	$(UV) build

wheel: ## Build only a wheel.
	$(UV) build --wheel

check: lint test docs build ## Run the normal local quality gate.

clean: ## Remove local build artifacts.
	rm -rf dist docs/build .pytest_cache .ruff_cache
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +

distclean: clean docs-clean ## Remove all generated artifacts.
	rm -rf build *.egg-info src/*.egg-info .mypy_cache htmlcov
