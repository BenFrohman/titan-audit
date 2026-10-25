# Contributing checklist (v1.0.0)

Before any merge:

- [ ] Every original `.lean` file has the five-line header with `Authors: Benjamin Stanley Frohman` (no trailing period, no AI names).
- [ ] No `sorry`, `admit`, or custom `axiom` in completed claims; holes are labeled as open, not disguised as `True`.
- [ ] `lake exe cache get && lake build` is green.
- [ ] `scripts/check.sh` passes: `#print axioms` on each target shows only `propext`, `Classical.choice`, `Quot.sound`.
- [ ] Classical results are pin-and-cite: explicit named hypothesis + source citation + Mathlib lemma name when available; never a global `axiom`.
- [ ] `lean-toolchain`, lakefile Mathlib `rev`, and `lake-manifest.json` agree.
- [ ] Git author/committer is `Benjamin Stanley Frohman <frohmanbenjamin@gmail.com>`; **no AI `Co-authored-by:` trailers**; AI help, if any, disclosed in the body.
- [ ] No history rewrite or force-push on `main`.
- [ ] One logical change per PR.
