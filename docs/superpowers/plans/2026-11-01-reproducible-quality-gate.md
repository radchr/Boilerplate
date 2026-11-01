# Reproducible Quality Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Python boilerplate's tests, dependency resolution, and built-package verification reproducible locally and in CI.

**Architecture:** Keep the existing package and command surface. Strengthen the behavioral test, pin the uv toolchain in project metadata, and extend `just ci` with a wheel build plus isolated import smoke test so GitHub Actions exercises the same gate.

**Tech Stack:** Python 3.13, uv 0.13.6, uv-build 0.13.x, Ruff, ty, pytest, Hypothesis, just, GitHub Actions

**Spec:** `docs/superpowers/specs/2026-11-01-reproducible-quality-gate-design.md`

## Global Constraints

- Python remains `>=3.13`.
- Runtime dependencies remain empty.
- `uv.lock` is authoritative and quality commands must not update it.
- Do not stage or modify the attached untracked analysis document.
- Preserve the small framework-free architecture.

## Review Focus

- A stale lockfile must make CI fail rather than be rewritten.
- Values below and above the interval must clamp to the exact respective bound.
- Equal bounds and values already on either bound must remain valid.
- The wheel smoke test must not import from the source checkout.
- A fresh CI runner must install the pinned uv version before reading the lock.

---

### Task 1: Strengthen the clamp property contract

**Files:**
- Modify: `tests/test_core.py`

**Interfaces:**
- Consumes: `boilerplate.clamp(value: int, lower: int, upper: int) -> int`
- Produces: a property test that rejects every result except the exact clamped value

- [ ] Replace the partial interval assertions with a hand-derived three-branch expected result.
- [ ] Temporarily mutate an out-of-range branch and run the property test to prove it fails for the intended reason.
- [ ] Restore production code and run `uv run --locked pytest tests/test_core.py`.
- [ ] Commit as `test: strengthen clamp property contract`.

### Task 2: Pin and describe the package toolchain

**Files:**
- Create: `LICENSE`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

**Interfaces:**
- Consumes: uv project configuration and uv-build backend metadata
- Produces: uv `==0.13.6`, uv-build `>=0.13.0,<0.14.0`, complete description and MIT license metadata

- [ ] Replace placeholder metadata, add the MIT license declaration, configure uv `required-version`, and add the license file.
- [ ] Regenerate the lockfile with uv 0.13.6.
- [ ] Run `uv lock --check` with uv 0.13.6 and verify the build emits no version-range warning.
- [ ] Commit as `chore: pin packaging toolchain`.

### Task 3: Make packaging part of the shared quality gate

**Files:**
- Modify: `Justfile`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-11-01-reproducible-quality-gate-design.md`
- Modify: `docs/superpowers/plans/2026-11-01-reproducible-quality-gate.md`

**Interfaces:**
- Consumes: the pinned uv project and built wheel
- Produces: `just package`, locked `just ci`, and setup/build documentation

- [ ] Add a `package` recipe that builds distributions and imports the wheel in an isolated no-project environment.
- [ ] Include `package` in `ci`, set `UV_LOCKED=1` in GitHub Actions, and have setup-uv read the project version pin.
- [ ] Document locked setup, package verification, supported Python policy, metadata adaptation, and licensing.
- [ ] Run the complete gate with uv 0.13.6 and confirm the source tree remains unchanged except for intended files.
- [ ] Commit as `ci: verify locked install and wheel`.
