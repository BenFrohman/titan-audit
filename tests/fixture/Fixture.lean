/-
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Benjamin Stanley Frohman
-/

/-!
# tests.fixture.Fixture

Minimal Mathlib-free Lean 4 project used by the titan-audit GitHub Action
self-test. Two kernel-checked theorems, no `sorry`, and no non-standard axioms.
-/

/-- Immediate numerical identity, closed by `rfl`. -/
theorem two_add_two : 2 + 2 = 4 := rfl

/-- Right-zero law for `Nat` addition, closed by `rfl`. -/
theorem add_zero (n : Nat) : n + 0 = n := rfl
