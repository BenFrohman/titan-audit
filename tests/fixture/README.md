# Action self-test fixture

A tiny Lean 4 / Lake project with no Mathlib dependency. It exists so
`.github/workflows/self-test.yml` can run `titan-audit` against a fast,
deterministic target and assert the action outputs.

Pin: `leanprover/lean4:v4.30.0-rc1`. Expected audit: `verdict=PASS`,
`theorems-total=2`, `theorems-clean=2`, `vacuity-warnings=0`.
