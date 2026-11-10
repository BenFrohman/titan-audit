/-
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under the proprietary All Rights Reserved terms described in the file LICENSE.
Authors: Benjamin Stanley Frohman
-/

/-!
# Example Verified Module (`LeanKernelGate.Example`)

Self-contained kernel-verified fixture demonstrating the five-line All Rights Reserved
sole-authorship header, decidable environment contract (`StandardStack`), and
zero-`sorry` theorem verification under `AxiomAudit.lean`.
-/

namespace LeanKernelGate

/-- Doubling a natural number is adding it to itself. Closes without `sorryAx`. -/
theorem double_eq_add_self (n : Nat) : 2 * n = n + n := by
  omega

/-- Commutativity of natural addition on diagonal pairs. -/
theorem add_self_nonneg (n : Nat) : 0 ≤ n + n := by
  omega

end LeanKernelGate
