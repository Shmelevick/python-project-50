rebuild:
	rm dist/hexlet_code-0.1.0-py3-none-any.whl
	rm dist/hexlet_code-0.1.0.tar.gz
	uv build
	uv sync

test-simple-json:
	uv run gendiff tests/fixtures/file1.json tests/fixtures/file2.json