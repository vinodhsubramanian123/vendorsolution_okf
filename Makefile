.PHONY: install test lint typecheck clean run ui-install ui-test ui-dev

install:
	uv sync --extra dev

test:
	uv run --python 3.11 pytest tests/ -v

lint:
	uv run --python 3.11 ruff check .

typecheck:
	uv run --python 3.11 mypy ikp_platform/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

run:
	./scripts/start_api.sh

ui-install:
	cd ikp_web && npm install

ui-test:
	cd ikp_web && npm run test:e2e

ui-dev:
	cd ikp_web && npm run dev
