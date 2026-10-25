# Lean toolchain note (v1.0.0)

**Current pin:** `leanprover/lean4:v4.30.0-rc1`, matched with Mathlib tag `v4.30.0-rc1`.

Why: this is the pin `BenFrohman/NS_Millennium_Proof` builds green on (2,704 jobs,
axiom-clean). Reusing it means modules move between projects without porting.

Caveat: `-rc1` is a release candidate. For a long-lived public harness, consider
moving to the next stable Lean release once Mathlib tags a matching version.

Bumping:
1. Pick a Mathlib tag; copy its `lean-toolchain` exactly into this repo.
2. Set `rev` in `lakefile.toml` to the same tag.
3. `lake update mathlib && lake exe cache get && lake build && scripts/check.sh`.
4. Restart the Lean server in the editor. Commit `lean-toolchain`, `lakefile.toml`, `lake-manifest.json` together.
