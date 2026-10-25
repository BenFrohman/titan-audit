# Dual-Track Open-Core & Commercial Enterprise Licensing

**Copyright © 2026 Benjamin Stanley Frohman** (`ORCID: 0009-0006-7068-3718`)  
**Repository:** [`BenFrohman/titan-audit`](https://github.com/BenFrohman/titan-audit) · **Zenodo DOI:** [`10.5281/zenodo.23630648`](https://doi.org/10.5281/zenodo.23630648)

`titan-audit` and the Frohmanian Four-Layer Verification Architecture are distributed under a **Dual-Track Open-Core / Commercial Enterprise** model designed to maximize open academic reproducibility while providing enterprise-grade verification guarantees for AI laboratories, formal-methods contractors, and autonomous theorem-proving pipelines.

---

## Track 1: Open-Core Community Edition (`Apache-2.0`)

All code, Lean 4 kernel harnesses, and documentation contained in this public repository are licensed under the **Apache License, Version 2.0** (see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)):

- **Core `titan-audit` Python CLI (`src/titan_audit/`):**
  - Stage 1: Reproducible `lake build` & Mathlib cache orchestration
  - Stage 2: In-kernel metaprogramming `Lean.collectAxioms` walker over every compiled `ConstantInfo.thmInfo`
  - Stage 3: Comment-aware forbidden-token scanner (`sorry`, `admit`, `axiom`, `native_decide`, `Lean.trustCompiler`, `Lean.ofReduceBool`)
  - Stage 4: Standard 5-rule semantic vacuity heuristics (`real_iSup_without_BddAbove`, `trivial_prop_def`, `true_hypothesis`, `assumes_top`, `false_hypothesis`)
  - Stage 5: Deterministic SHA-256 Merkle/tree hashing over sorted `.lean` sources, `lakefile`, `lake-manifest.json`, and `lean-toolchain`
  - Stage 6: Local Ed25519 canonical JSON signing & verification (`titan-audit verify`)
- **Lean 4 Kernel & Environment Harnesses (`lean-kernel-gate/` & `agent-skills/`):**
  - `StandardStack.lean` decidable environment contract (`the_standard_stack`)
  - `AxiomAudit.lean` standalone metaprogramming axiom walker
  - `.grok/skills/` (`lean-standard-stack`, `frohmanian-lean-encoding`, `titan-audit`)
- **GitHub Marketplace Action (`action.yml`):**
  - Drop-in CI/CD step (`uses: BenFrohman/titan-audit@v1`) for public and private repositories.

**Obligations under Apache-2.0:**
Downstream users, forks, and benchmark suites enjoy the full Apache-2.0 copyright and patent grants, subject to preserving the copyright notice and [`NOTICE`](NOTICE) file attributing **Benjamin Stanley Frohman** (`ORCID: 0009-0006-7068-3718`, DOI: `10.5281/zenodo.23630648`) under Apache-2.0 Section 4(d).

---

## Track 2: Enterprise & Custom Benchmark Edition (Commercial License)

For organizations requiring proprietary reward-firewall integration, domain-specific semantic vacuity detectors beyond the open-core ruleset, or managed cryptographic attestation, a **Commercial Enterprise License** is available directly from the author (**Benjamin Stanley Frohman**):

1. **Domain-Specific Semantic Vacuity Rulesets:**
   - **PDE & Continuum Mechanics Analytical Bridge Auditors:** Automated detection of totalized-derivative vacuity (`deriv` vs. `derivWithin` without `DifferentiableAt`), infinite-measure Haar vs. compact torus $\mathbb{T}^d$ measure conflation, $C^1$ (`DifferentiableAt`) vs. $C^2$ (`ContDiffAt ℝ 2` + `IsSymmSndFDerivAt`) mixed-partial violations, and automated synthesis of zero-state / quiescent counterexample witnesses (`stepField` / `nonvacuous_at_zero`).
   - **Cryptographic Protocol & Zero-Knowledge Circuit Auditors:** Detection of under-constrained field arithmetic, totalized modular division (`x / 0 = 0` in $\mathbb{F}_p$), and soundness-vacating witness binders in Lean 4 / zkVM formalizations.
   - **Smart-Contract & Consensus Invariant Auditors:** Detection of vacuously unreachable state-transition hypotheses and liveness/safety specification mutations.
2. **RLHF & Autonomous Agent Reward-Firewall Integration:**
   - High-throughput, low-latency anti-specification-gaming reward gates for autonomous prover training loops (preventing LLM agents from mutating statement signatures or exploiting totalized partial functions during reinforcement learning).
3. **Managed Hardware-Backed (HSM / KMS) Ed25519 Attestation Authority:**
   - Third-party cryptographic signing and timestamping of formal verification audit reports for regulatory, DARPA/defense, or financial compliance without Apache-2.0 `NOTICE` redistribution requirements in proprietary closed-source appliances.

---

## Commercial Inquiries & Licensing Contact

- **Licensor & Sole Author:** Benjamin Stanley Frohman
- **ORCID:** [`0009-0006-7068-3718`](https://orcid.org/0009-0006-7068-3718)
- **Email:** `frohmanbenjamin@gmail.com`
- **X (Twitter):** [`@Investor0x`](https://x.com/Investor0x)
- **GitHub:** [`@BenFrohman`](https://github.com/BenFrohman)
