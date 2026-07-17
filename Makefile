.PHONY: test lint clean install run

install:
	uv pip install -r requirements.txt
	uv pip install pytest pytest-cov ruff mypy

test:
	uv run --python 3.11 pytest tests/ -v

lint:
	ruff check .
	mypy ikp_platform/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/

run:
	uv run --python 3.11 python -m ikp_platform.api
