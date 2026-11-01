# Universal Python Boilerplate

A framework-free Python foundation with a fast, repeatable quality gate. It
uses a `src/` layout and keeps the initial package intentionally small, so it
can become a library, CLI, service, or other application later.

## Requirements

- Python 3.13 or newer
- [uv 0.13.6](https://docs.astral.sh/uv/) (enforced by project metadata)
- [just](https://just.systems/)

## Quick start

```console
uv sync --locked --all-groups
uv run pre-commit install
just fix
just ci
```

## Daily workflow

| Command | Purpose |
| --- | --- |
| `just fix` | Apply safe Ruff fixes and format the project. |
| `just check` | Check formatting, linting, and types without changing files. |
| `just test` | Run tests and show missing coverage lines. |
| `just package` | Build distributions and import the wheel in isolation. |
| `just ci` | Run the complete, non-mutating local quality gate. |

Every recipe exports `UV_LOCKED=1`, so an out-of-date lockfile fails instead
of being rewritten. `just ci` checks formatting, linting, types,
coverage-backed tests, distribution builds, and an isolated wheel import. It
is a useful guardrail, not a proof that the implementation or its requirements
are correct.

## Package layout

```text
src/boilerplate/
  __init__.py
  core.py
tests/
  test_core.py
```

`boilerplate.clamp` is a deliberately small pure-function example. Its tests
show ordinary examples and a Hypothesis property test without forcing an
application architecture on future code.

## Local configuration

Use `.env` for local secrets and machine-specific values. It is ignored by
Git. Copy `.env.example` when a future application needs configuration, and
keep the committed example value-free. Tests must use explicit fixtures or
`monkeypatch`, never a developer's real `.env`.

## Adapt the template

Before starting product work, replace the project name, import package,
description, author, and version in `pyproject.toml`; update the package and
test directories to match. The template uses the MIT license, so replace
`LICENSE` and the project license metadata if the derived project needs a
different license.

Python 3.13 is the tested baseline. The package metadata permits newer Python
versions, but projects that promise compatibility with several versions should
add those versions to the CI matrix.

## Add tools when the code needs them

- Add Pydantic and pydantic-settings at untrusted input or configuration
  boundaries.
- Add Tach when independently changing modules need enforced import rules.
- Add Testcontainers after introducing adapters that need real services such
  as PostgreSQL or Redis.
- Add Deal and CrossHair only for small, side-effect-free algorithms with
  reviewable contracts.
- Run mutmut only in WSL/Linux or CI and only against a fast pure core.
- Use Nagini in a separately scoped verification workflow with its required
  Java/Viper toolchain.
