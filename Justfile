fix:
    uv run ruff check --fix .
    uv run ruff format .

check:
    uv run ruff format --check .
    uv run ruff check .
    uv run ty check

test:
    uv run pytest --cov=boilerplate --cov-report=term-missing

ci: check test
