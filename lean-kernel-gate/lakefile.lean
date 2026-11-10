/-
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under the proprietary All Rights Reserved terms described in the file LICENSE.
Authors: Benjamin Stanley Frohman
-/
import Lake
open Lake DSL

package «lean-kernel-gate» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

@[default_target]
lean_lib «LeanKernelGate» where
  roots := #[`LeanKernelGate]
