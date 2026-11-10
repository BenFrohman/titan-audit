# Titan-Audit & The Frohmanian Four-Layer Lean 4 Verification Architecture

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23630648.svg)](https://doi.org/10.5281/zenodo.23630648)
[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](./LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--7068--3718-A6CE39.svg)](https://orcid.org/0009-0006-7068-3718)
[![Lean 4](https://img.shields.io/badge/Lean_4-v4.30.0--rc1-orange.svg)](https://lean-lang.org/)

**Author:** Benjamin Stanley Frohman ([ORCID: `0009-0006-7068-3718`](https://orcid.org/0009-0006-7068-3718) · [`@BenFrohman`](https://github.com/BenFrohman) · [`@Investor0x`](https://x.com/Investor0x) · `frohmanbenjamin@gmail.com`)  
**Permanent DataCite Zenodo DOI:** [`10.5281/zenodo.23630648`](https://doi.org/10.5281/zenodo.23630648)  
**Formal Whitepaper (PDF):** [`Titan_Audit_Specification_Gaming_and_Semantic_Vacuity_Whitepaper_2026.pdf`](./Titan_Audit_Specification_Gaming_and_Semantic_Vacuity_Whitepaper_2026.pdf) ([LaTeX Source](./paper/Preventing_Specification_Gaming_and_Semantic_Vacuity_in_Autonomous_Lean4_Agents.tex))

---

## Overview & Unified Architecture

`BenFrohman/titan-audit` is the flagship repository unifying all five components of the **Frohmanian Anti-Specification-Gaming & Semantic Vacuity Firewall** for autonomous Lean 4 coding and theorem-proving agents:

1. **`titan-audit` (`src/titan_audit/` & `titan_audit/`)** — Installable Python CLI (`pip install .`) and cryptographic attestation engine that runs a deterministic 6-stage audit over any Lean 4 / Lake repository and emits an Ed25519-signed canonical JSON attestation (`schema/report.schema.json`) and Markdown verification report.
2. **`AxiomAudit.lean` (`lean-kernel-gate/AxiomAudit.lean`)** — In-kernel Lean 4 `CommandElabM` metaprogramming inspector that walks every compiled `ConstantInfo.thmInfo` in the `.olean` environment via `Lean.collectAxioms` and fails the build if any theorem depends on anything outside `{propext, Classical.choice, Quot.sound}`.
3. **`lean-harness-draft` / `frohman-lean-agent-harness` (`lean-kernel-gate/`)** — Standalone Lake verification harness containing `StandardStack.lean`, `LeanKernelGate/StandardStack.lean`, `check.sh`, and `scripts/check.sh`.
4. **`lean-standard-stack` (`agent-skills/lean-standard-stack/` & `.grok/skills/lean-standard-stack/`)** — Pre-execution environment contract enforcing `elan` toolchain pinning, Lake project root validation, Mathlib cache retrieval before build, and strict sole human authorship (`Benjamin Stanley Frohman`, zero AI `Co-authored-by:` trailers).
5. **`frohmanian-lean-encoding` (`agent-skills/frohmanian-lean-encoding/` & `.grok/skills/frohmanian-lean-encoding/`)** — Single-worktree discipline and domain-aware anti-"Frankenstein Proof" rules preventing autonomous agents from exploiting Mathlib totalized partial functions (`sSup`/`iSup` without `BddAbove`, `deriv` at non-differentiable jumps) or weakening hypotheses to `True`.

---

## Origin Provenance Timeline (`America/Chicago`, CDT / UTC-5)

- **October 9, 2026 (`2026-10-09T14:55:31-05:00`, CDT):** Discovery and formal taxonomy by Benjamin Stanley Frohman of the **"Frankenstein Proof" / Sandbox Auto-Formalization Mutation Loophole** — demonstrating how reward-driven LLM agents achieve green `lake build` + zero `sorry` by mutating hypothesis binders into contradictory pairs or exploiting Mathlib totalized partial function defaults (`sSup S = 0` when `¬ BddAbove S`, `deriv f t = 0` when `¬ DifferentiableAt ℝ f t`).
- **October 11–24, 2026:** Engineering of the 4-layer stack (`StandardStack.lean`, `frohmanian-lean-encoding`, `AxiomAudit.lean`, and `titan-audit`) and full validation across **14 compiled Lean 4 modules (360 theorems)** in [`BenFrohman/NS_Millennium_Proof`](https://github.com/BenFrohman/NS_Millennium_Proof) (DOI: [`10.5281/zenodo.23627610`](https://doi.org/10.5281/zenodo.23627610)), where it isolated the discontinuous step-field parasite (`stepField` / `library_huniq_unsatisfiable_at_zero`), verified the `IsPhysicalNSSolution` admissibility repair, and verified the quiescent witness theorem `global_regularity_for_NS_nonvacuous_at_zero`.

---

## Repository Structure

```text
titan-audit/
├── Titan_Audit_Specification_Gaming_and_Semantic_Vacuity_Whitepaper_2026.pdf
├── paper/
│   └── Preventing_Specification_Gaming_and_Semantic_Vacuity_in_Autonomous_Lean4_Agents.tex
├── src/titan_audit/                # Python package (also mirrored at titan_audit/ for direct invocation)
│   ├── __init__.py                 # Package metadata & public exports
│   ├── cli.py                      # CLI entry point (`titan-audit` & `titan-audit verify`)
│   ├── core.py                     # 6-stage audit orchestrator & Lean.collectAxioms driver
│   ├── scan.py                     # Comment-stripping scanner & 5 vacuity heuristics
│   ├── sign.py                     # Canonical JSON & Ed25519 signing/verification
│   ├── report_md.py                # Human-readable Markdown report formatter
│   ├── auditor.py                  # Semantic module interface for audit orchestration
│   ├── vacuity.py                  # Semantic module interface for vacuity heuristics
│   ├── signing.py                  # Semantic module interface for Ed25519 attestations
│   └── tree_hash.py                # Deterministic SHA-256 source-tree digest helper
├── lean-kernel-gate/               # Self-contained Lean 4 kernel gate & frohman-lean-agent-harness
│   ├── AxiomAudit.lean             # Generic in-kernel Lean.collectAxioms walker
│   ├── StandardStack.lean          # Decidable 5-field StandardStack environment contract
│   ├── check.sh                    # End-to-end Lake build + forbidden-token + axiom gate
│   ├── lakefile.lean               # Self-contained Lake configuration
│   ├── lean-toolchain              # Pinned Lean 4 toolchain (leanprover/lean4:v4.30.0-rc1)
│   ├── LeanKernelGate/             # Library modules (StandardStack.lean, Example.lean)
│   └── scripts/                    # Project-specific AxiomAudit_NS_Millennium_Proof.lean & check.sh
├── agent-skills/                   # Agent skill harnesses (also mirrored in .grok/skills/)
│   ├── lean-standard-stack/        # SKILL.md + StandardStack.lean
│   ├── frohmanian-lean-encoding/   # SKILL.md (Anti-Frankenstein & Single-Worktree rules)
│   └── titan-audit/                # SKILL.md (Autonomous auditor skill wrapper)
├── examples/
│   └── ns_millennium_proof_audit/  # Real Ed25519-signed report.json & report.md (360 theorems)
├── schema/
│   └── report.schema.json          # JSON Schema Draft 2020-12 for signed audit attestations
├── tests/                          # Pytest unit & CLI integration test suite (15 tests)
├── action.yml                      # GitHub Marketplace Action (icon: shield, color: blue)
├── pyproject.toml                  # PEP 621 package configuration (`pip install .`)
├── COMMERCIAL_LICENSING.md         # Commercial licensing terms and inquiries
├── CITATION.cff                    # Citation File Format metadata (DOI: 10.5281/zenodo.23630648)
├── .zenodo.json                    # Zenodo / InvenioRDM deposit metadata
├── LICENSE                         # Proprietary All Rights Reserved (Copyright 2026 Benjamin Stanley Frohman)
└── NOTICE                          # Proprietary ownership and contact notice
```

---

## Quickstart: Install & Run the CLI

### 1. Install via `pip`
```bash
pip install .
```

### 2. Run the Full 6-Stage Audit on a Lean 4 Project
```bash
titan-audit /path/to/lean-project --out-dir ./audit-reports
```
Or run the fast static + tree-hash + Ed25519 signing pass without invoking `lake build`:
```bash
titan-audit /path/to/lean-project --no-build --out-dir ./audit-reports
```

### 3. Verify an Ed25519-Signed Attestation
```bash
titan-audit verify examples/ns_millennium_proof_audit/report.json
# Output: signature OK
```

### 4. Run the Standalone Lean Kernel Gate
```bash
cd lean-kernel-gate
./check.sh
```

---

## GitHub Marketplace Action (`BenFrohman/titan-audit@v1`)

Add `BenFrohman/titan-audit@v1` to any Lean 4 repository or AI benchmark workflow (`.github/workflows/titan-audit.yml`, template in `workflows/titan-audit-ci.yml`):

```yaml
name: Titan-Audit Lean 4 Verification
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: leanprover/lean-action@v1
        with:
          use-mathlib-cache: true
      - uses: BenFrohman/titan-audit@v1
        with:
          project-path: '.'
          fail-on-vacuity: 'true'
          sign-report: 'true'
```

---

## The Six Verification Checks Performed by `titan-audit`

| Stage | Verification Gate | What It Catches | Verdict Impact |
|---|---|---|---|
| **1. Build Gate** | `lake build` execution & log parser | Unelaborated proofs, type errors, compiler warnings | `FAIL` if `exit_code != 0` |
| **2. In-Kernel Axiom Walk** | `Lean.collectAxioms` over every `ConstantInfo.thmInfo` in built `.olean` modules | `sorryAx`, `Lean.trustCompiler` (`native_decide`), `Lean.ofReduceBool`, custom `axiom`s | `FAIL` if any theorem uses non-standard axioms |
| **3. Forbidden Token Scan** | Comment-stripped (`--` & nested `/- -/`) source scan | `sorry`, `admit`, `axiom`, `native_decide`, `trustCompiler`, `ofReduceBool` in built or unbuilt files | `FAIL` (`in_build: true`) or `PASS_WITH_WARNINGS` (`in_build: false`) |
| **4. Vacuity Heuristics** | AST/declaration-span analyzer (`titan_audit/scan.py`) | Real `iSup`/`sSup` without `BddAbove`, `Prop := True`, `(h : True)`, `(h : False)`, `(h : x = ⊤)` | `PASS_WITH_WARNINGS` (or `FAIL` with `fail-on-vacuity: true`) |
| **5. SHA-256 Tree Digest** | Deterministic hash over all sorted `*.lean`, `lakefile.*`, `lake-manifest.json`, `lean-toolchain` | Ghost-worktree drift, unindexed file tampering | Recorded in `tree.sha256` |
| **6. Ed25519 Attestation** | Canonical JSON signing (`titan_audit/sign.py`) | Post-audit report tampering in CI/CD pipelines | Verifiable via `titan-audit verify` |

---

## License

This repository is proprietary commercial software. Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved. See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE).

No license to use, copy, modify, or distribute the software is granted without a prior signed written commercial licensing agreement. Publication of the architectural whitepaper ([`10.5281/zenodo.23630648`](https://doi.org/10.5281/zenodo.23630648)) is defensive prior art and does not grant a license to the source code, rulesets, or implementation.

For commercial licensing inquiries, including custom domain-specific semantic vacuity rulesets, CI/CD integrations, and managed attestation, see [`COMMERCIAL_LICENSING.md`](./COMMERCIAL_LICENSING.md) or contact **Benjamin Stanley Frohman** (`frohmanbenjamin@gmail.com` / ORCID `0009-0006-7068-3718` / [`@Investor0x`](https://x.com/Investor0x)).

---

## Citation

```bibtex
@software{frohman2026titanaudit,
  author       = {Frohman, Benjamin Stanley},
  title        = {{Preventing Specification Gaming and Semantic Vacuity in Autonomous Lean 4 Formalization Agents: The Titan-Audit \& Frohmanian Four-Layer Verification Architecture}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.23630648},
  url          = {https://doi.org/10.5281/zenodo.23630648}
}
```

## AI Assistance Disclosure

Grok (xAI), via the Grok Bot assistant, provided scaffolding, drafting, and collaboration support on the formalization, code, and documentation in this repository. Benjamin Stanley Frohman (`frohmanbenjamin@gmail.com`, ORCID `0009-0006-7068-3718`) directed, reviewed, and is solely responsible for the architecture, implementation, proofs, and claims; Grok is not a coauthor.
