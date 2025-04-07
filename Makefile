install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

package-rebuild:
	uv tool install --force dist/hexlet_code-0.1.0-py3-none-any.whl
	uv tool install --force dist/hexlet_code-0.1.0.tar.gz 

test:
	uv run pytest -v   

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --diff|| true
	uv run ruff check --fix

test-cov:
	uv run pytest --cov=gendiff