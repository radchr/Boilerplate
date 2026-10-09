# Universal Python Boilerplate — Design

**Date:** 2026-10-09
**Status:** Approved design; implementation not started

## Purpose

Provide a small, framework-free Python foundation for starting different
applications and libraries. It must make the common quality checks easy to
run while avoiding dependencies whose value depends on a specific domain,
such as a web framework, database, message broker, or formal-verification
workflow.

## Success criteria

- A contributor can set up the project and run all routine checks through a
  small, documented command surface.
- Source code is installed and tested through a `src/` layout, preventing
  accidental imports from the repository root.
- Formatting, linting, type checks, examples, deterministic tests,
  property-based tests, and coverage reporting run locally and in CI.
- The repository never tracks local credentials. A committed `.env.example`
  documents optional environment variables without containing values.
- Advanced tooling is optional and added only when the project gains the
  relevant kind of code or infrastructure.

## Scope

### Included

- Python 3.13 package skeleton named `boilerplate`.
- Dependency and environment management through `uv`.
- Code formatting and linting with Ruff.
- Static type checking with `ty`.
- Tests with pytest and Hypothesis.
- Coverage reporting with pytest-cov.
- Repeatable developer commands in a `Justfile`.
- A local pre-commit hook configuration.
- GitHub Actions CI for the routine quality gate.
- A minimal, pure example module plus ordinary and property-based tests.
- Documentation of routine workflow and criteria for adopting advanced tools.

### Explicitly excluded

- Web, CLI, database, queue, ORM, logging, dependency-injection, or API
  frameworks.
- Runtime configuration libraries such as Pydantic unless an application
  boundary actually needs them.
- `deal`, CrossHair, Z3, Nagini, Tach, Testcontainers, and mutation testing
  as default dependencies.
- Coverage targets presented as a proof of correctness.

## Architecture

```text
src/boilerplate/
  __init__.py        Public package surface
  core.py            Small pure example function
tests/
  test_core.py       Example-based and property-based tests
```

The initial package contains only pure logic. Future applications may add
adapters around this core; framework or infrastructure choices remain outside
the boilerplate.

## Tooling decisions

| Concern | Choice | Rationale |
| --- | --- | --- |
| Python and packages | `uv` | Reproducible environments and lockfile. |
| Formatting and linting | `ruff` | One fast formatter/linter with a focused ruleset. |
| Type checking | `ty` | Fast default checker; use Pyright only as a deliberate compatibility comparison, not a duplicate routine gate. |
| Tests | `pytest`, `hypothesis` | Example-based regression tests plus input-space exploration. |
| Coverage | `pytest-cov` | Visibility into untested code, without a misleading universal percentage threshold. |
| Commands | `just` | Stable, short commands for people and automation. |
| Hooks | `pre-commit` | Fast feedback before a commit; CI remains authoritative. |
| CI | GitHub Actions | A fresh-environment check of the same routine gate. |

## Quality gate

`just ci` runs, in order:

1. `ruff format --check`.
2. `ruff check`.
3. `ty check`.
4. `pytest` with coverage reporting.

`just fix` applies safe Ruff fixes and formatting. Tests must not depend on
network access, Docker, local credentials, or a manually activated virtual
environment.

## Secrets and configuration

`.env` is local-only and must be listed in `.gitignore`. The project provides
`.env.example` with comments and blank values only. Tests use explicit
fixtures or `monkeypatch`; they never read a developer's real `.env` file.

## Advanced-tool adoption guide

- Add **Pydantic** and **pydantic-settings** when untrusted API, file, or
  environment input needs a typed boundary.
- Add **Tach** when independently changing modules need enforced import
  boundaries.
- Add **Testcontainers** once adapters depend on PostgreSQL, Redis, or another
  real service.
- Add **Deal and CrossHair** only for compact, side-effect-free algorithms
  with meaningful, reviewable contracts.
- Run **mutmut** only under WSL/Linux or CI, targeted at a fast pure core.
- Use **Nagini** only in a separately scoped verification workflow with its
  Java/Viper toolchain.

## Verification

Implementation is complete only when the quality gate passes from a clean
environment, the package imports after installation, the example tests show
both ordinary and property-based testing, and no credential-bearing file is
tracked by Git.
