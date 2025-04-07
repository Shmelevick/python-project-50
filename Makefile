install:
	uv sync

rebuild:
	uv build
	rm dist/hexlet_code-0.1.0-py3-none-any.whl
	rm dist/hexlet_code-0.1.0.tar.gz
	uv sync

test:
	uv run pytest -v   

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --diff|| true
	uv run ruff check --fix

test-cov:
	uv run pytest --cov=gendiff