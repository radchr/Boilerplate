# Reproducible Quality Gate — Design

**Date:** 2026-11-01
**Status:** Implemented

## Intent

Strengthen the existing minimal Python boilerplate without adding runtime
dependencies or application architecture. A contributor and CI should use the
same locked toolchain, verify the full `clamp` contract, and prove that the
published wheel imports independently of the source checkout.

## Goals

- Reject an out-of-date `uv.lock` instead of updating it during quality checks.
- Pin uv 0.13.6 and use the matching uv-build 0.13 release line.
- Make the Hypothesis test assert the exact `clamp` result for all integers.
- Build a wheel and import `boilerplate` from an isolated environment in CI.
- Replace placeholder package metadata and add an MIT license.
- Keep one documented local command, `just ci`, equivalent to the CI gate.

## Non-goals

- Add frameworks, runtime dependencies, release automation, security scanners,
  documentation sites, or support for Python versions below 3.13.
- Introduce Copier/Cruft or redesign the package structure.

## Approach

Three options were considered: a large batteries-included template, CI-only
hardening, and a minimal end-to-end quality-gate improvement. The approved
approach is the third: retain the current architecture, enforce locked uv
operations globally, strengthen the existing property test, and add packaging
verification to the shared `Justfile` gate. This provides the requested
guarantees with the smallest maintenance surface.

## Constraints

- Python remains `>=3.13` and the package keeps zero runtime dependencies.
- The checked-in lockfile remains authoritative.
- The attached analysis document is reference material and is not committed.
- All repository edits must pass formatting, linting, typing, tests, lockfile
  validation, build, and isolated wheel-import verification.
