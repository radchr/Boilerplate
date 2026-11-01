export UV_LOCKED := "1"

fix:
    uv run ruff check --fix .
    uv run ruff format .

check:
    uv run ruff format --check .
    uv run ruff check .
    uv run ty check

test:
    uv run pytest --cov=boilerplate --cov-report=term-missing

package:
    #!/usr/bin/env bash
    set -euo pipefail
    package_dir="$(mktemp -d)"
    trap 'rm -rf "$package_dir"' EXIT
    uv build --out-dir "$package_dir"
    wheels=("$package_dir"/*.whl)
    test "${#wheels[@]}" -eq 1
    test -f "${wheels[0]}"
    unset UV_LOCKED
    uv run --isolated --no-project --with "${wheels[0]}" python -I -c \
        'from boilerplate import clamp; assert clamp(12, 0, 10) == 10'

ci: check test package
