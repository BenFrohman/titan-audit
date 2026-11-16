# IP scope (Copyright 2026 Benjamin Stanley Frohman, Apache License 2.0)

**Not the user's IP.** These are third-party works under their own licenses
(Apache-2.0) and are used, not owned:
- the Lean 4 elaborator, compiler, and C++ kernel (`leanprover/lean4`);
- Lean core, `Std`, Lake, and Batteries;
- Mathlib (`leanprover-community/mathlib4`) and all its tactics (`simp`, `ring`, `linarith`, `omega`, `decide`, ...);
- elan and the VS Code Lean extension.

This harness copies no code from any of them; it only references them by name and pins versions.

**In scope (user's authored work, under the user's control):**
- Lean modules authored by Benjamin Stanley Frohman (e.g. the `NS_Millennium_Proof` modules carrying his header);
- this harness's documentation (`README.md`, `STANDARD_STACK.md`, `CONTRIBUTING.md`, `LEAN_TOOLCHAIN_NOTE.md`, `IP_SCOPE.md`);
- harness scripts (`scripts/check.sh`) and configuration skeletons.

Note: authored modules already published under Apache-2.0 remain usable by others under that license; authorship is retained, exclusivity is not.

**License (as of 16 November 2026):** this harness, in this repository, is licensed under the Apache License, Version 2.0, as described in the root `LICENSE`. Third-party Lean, Mathlib, and related tools remain under their own licenses.
