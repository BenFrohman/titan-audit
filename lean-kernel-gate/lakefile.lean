/-
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Benjamin Stanley Frohman
-/

import Lake

/-!
# lean-kernel-gate.lakefile

Machine-checked Lean 4 module.
-/

open Lake DSL

package «lean-kernel-gate» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

@[default_target]
lean_lib «LeanKernelGate» where
  roots := #[`LeanKernelGate]
