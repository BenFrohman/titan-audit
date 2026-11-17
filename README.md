# Titan-Audit: Lean 4 Axiom & Vacuity Firewall

[![Self-test](https://github.com/BenFrohman/titan-audit/actions/workflows/self-test.yml/badge.svg)](https://github.com/BenFrohman/titan-audit/actions/workflows/self-test.yml)
[![CI](https://github.com/BenFrohman/titan-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/BenFrohman/titan-audit/actions/workflows/ci.yml)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-titan--audit-blue.svg)](https://github.com/marketplace/actions/titan-audit-lean-4-axiom-vacuity-firewall)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24293479.svg)](https://doi.org/10.5281/zenodo.24293479)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--7068--3718-A6CE39.svg)](https://orcid.org/0009-0006-7068-3718)
[![Lean 4](https://img.shields.io/badge/Lean_4-v4.30.0--rc1-orange.svg)](https://lean-lang.org/)

**Author:** Benjamin Stanley Frohman ([ORCID: `0009-0006-7068-3718`](https://orcid.org/0009-0006-7068-3718) · [`@BenFrohman`](https://github.com/BenFrohman) · [`@Frohmanian`](https://x.com/Frohmanian) · `frohmanbenjamin@gmail.com`)  
**GitHub Marketplace:** [`titan-audit-lean-4-axiom-vacuity-firewall`](https://github.com/marketplace/actions/titan-audit-lean-4-axiom-vacuity-firewall)  
**Software v1.2.0 DOI:** [`10.5281/zenodo.24293479`](https://doi.org/10.5281/zenodo.24293479) (concept [`10.5281/zenodo.24096789`](https://doi.org/10.5281/zenodo.24096789))  
**Whitepaper DOI:** [`10.5281/zenodo.23630648`](https://doi.org/10.5281/zenodo.23630648)  
**Formal Whitepaper (PDF):** [`Titan_Audit_Specification_Gaming_and_Semantic_Vacuity_Whitepaper_2026.pdf`](./Titan_Audit_Specification_Gaming_and_Semantic_Vacuity_Whitepaper_2026.pdf) ([LaTeX Source](./paper/Preventing_Specification_Gaming_and_Semantic_Vacuity_in_Autonomous_Lean4_Agents.tex))

---

## Usage

Copy the workflow below into `.github/workflows/titan-audit.yml` of a Lean 4 repository. Pin a release tag; the current Marketplace release is `v1.2.0`. A copy of this example also lives at [`examples/github-workflow.yml`](./examples/github-workflow.yml).

`titan-audit` does not install Lean. In a typical Lean repository, `lean-toolchain` is at the repo root, so `leanprover/lean-action` can install the toolchain first.

```yaml
name: Titan-Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: leanprover/lean-action@v1
        with:
          use-mathlib-cache: true

      - name: Run titan-audit
        id: audit
        uses: BenFrohman/titan-audit@v1.2.0
        with:
          project-path: "."
          fail-on-vacuity: "true"
          sign-report: "true"
          use-mathlib-cache: "false"
          no-build: "false"
          output-dir: titan-audit-report

      - name: Use audit outputs
        run: |
          echo "verdict=${{ steps.audit.outputs.verdict }}"
          echo "theorems-total=${{ steps.audit.outputs.theorems-total }}"
          echo "theorems-clean=${{ steps.audit.outputs.theorems-clean }}"
          echo "vacuity-warnings=${{ steps.audit.outputs.vacuity-warnings }}"
          echo "tree-sha256=${{ steps.audit.outputs.tree-sha256 }}"
          echo "report-json-path=${{ steps.audit.outputs.report-json-path }}"
          echo "report-md-path=${{ steps.audit.outputs.report-md-path }}"
```

This repository's integration test is [`.github/workflows/self-test.yml`](./.github/workflows/self-test.yml). It runs the action against a Mathlib-free fixture at [`tests/fixture`](./tests/fixture) twice: once with `uses: ./` and once pinned to `BenFrohman/titan-audit@v1.2.0`.

### Inputs

| Input | Default | Description |
|---|---|---|
| `project-path` | `.` | Path to the Lean 4 / Lake project root to audit. |
| `fail-on-vacuity` | `false` | Fail the workflow if semantic vacuity warnings (`PASS_WITH_WARNINGS`) are detected. |
| `sign-report` | `true` | Sign the canonical JSON audit report with Ed25519. If `signing-key-path` is empty, the action creates an ephemeral key and embeds its public key in the report. |
| `use-mathlib-cache` | `false` | Run `lake exe cache get` before `lake build`. |
| `no-build` | `false` | Skip `lake build` and audit pre-existing `.olean` files. |
| `output-dir` | `titan-audit-report` | Directory where `report.json` and `report.md` will be written. |
| `signing-key-path` | *(empty)* | Optional path to an Ed25519 PEM private key for signing. |

### Outputs

| Output | Description |
|---|---|
| `verdict` | Audit verdict (`PASS`, `PASS_WITH_WARNINGS`, or `FAIL`). |
| `theorems-total` | Total compiled theorems audited by `Lean.collectAxioms`. |
| `theorems-clean` | Compiled theorems that use only the standard axioms (`propext`, `Classical.choice`, `Quot.sound`), or no axioms. |
| `vacuity-warnings` | Count of semantic vacuity heuristic warnings in built modules. |
| `tree-sha256` | Deterministic SHA-256 hash over sorted Lean sources, lakefile, manifest, and toolchain. |
| `report-json-path` | Path to the generated `report.json`. |
| `report-md-path` | Path to the generated `report.md`. |

---

## Overview & Unified Architecture

`BenFrohman/titan-audit` is the flagship repository unifying all five components of the **Frohmanian Anti-Specification-Gaming & Semantic Vacuity Firewall** for autonomous Lean 4 coding and theorem-proving agents:

1. **`titan-audit` (`src/titan_audit/` & `titan_audit/`)** — Installable Python CLI (`pip install .`) and cryptographic attestation engine that runs a deterministic 6-stage audit over any Lean 4 / Lake repository and emits an Ed25519-signed canonical JSON attestation (`schema/report.schema.json`) and Markdown verification report. The same package is published as the GitHub Marketplace Action [`titan-audit-lean-4-axiom-vacuity-firewall`](https://github.com/marketplace/actions/titan-audit-lean-4-axiom-vacuity-firewall).
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
│   ├── github-workflow.yml         # Copy-paste consumer workflow pinning @v1.2.0
│   └── ns_millennium_proof_audit/  # Real Ed25519-signed report.json & report.md (360 theorems)
├── tests/
│   ├── test_basic.py               # Pytest unit tests
│   ├── test_cli_and_schema.py      # CLI and schema tests
│   └── fixture/                    # Mathlib-free Lean 4 project for the action self-test
├── .github/workflows/
│   ├── ci.yml                      # Python tests and LeanKernelGate build
│   ├── lean-header.yml             # Lean copyright-header check
│   └── self-test.yml               # Action integration test (`uses: ./` and `@v1.2.0`)
├── archive/workflows/              # Early pytest templates, kept for provenance
├── schema/
│   └── report.schema.json          # JSON Schema Draft 2020-12 for signed audit attestations
├── action.yml                      # GitHub Marketplace Action (icon: shield, color: blue)
├── pyproject.toml                  # PEP 621 package configuration (`pip install .`)
├── COMMERCIAL_LICENSING.md         # Historical commercial terms (pre-16 November 2026 copies only)
├── CITATION.cff                    # Citation File Format metadata (DOI: 10.5281/zenodo.24293479)
├── .zenodo.json                    # Zenodo / InvenioRDM deposit metadata
├── LICENSE                         # Apache License 2.0 (Copyright 2026 Benjamin Stanley Frohman)
└── NOTICE                          # Copyright and Apache 2.0 notice
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

Copyright (c) 2026 Benjamin Stanley Frohman.

Licensed under the Apache License, Version 2.0. See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE).

Commercial-license documents in [`legal/`](./legal/) and [`COMMERCIAL_LICENSING.md`](./COMMERCIAL_LICENSING.md) apply only to releases and copies distributed before 16 November 2026. They are preserved for provenance. Contact **Benjamin Stanley Frohman** (`frohmanbenjamin@gmail.com` / ORCID `0009-0006-7068-3718` / [`@Frohmanian`](https://x.com/Frohmanian)).

---

## Citation

```bibtex
@software{frohman2026titanaudit,
  author       = {Frohman, Benjamin Stanley},
  title        = {{Preventing Specification Gaming and Semantic Vacuity in Autonomous Lean 4 Formalization Agents: The Titan-Audit \& Frohmanian Four-Layer Verification Architecture}},
  month        = nov,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {1.2.0},
  doi          = {10.5281/zenodo.24293479},
  url          = {https://doi.org/10.5281/zenodo.24293479}
}
```

The architectural whitepaper is [`10.5281/zenodo.23630648`](https://doi.org/10.5281/zenodo.23630648). The concept DOI for this software deposit is [`10.5281/zenodo.24096789`](https://doi.org/10.5281/zenodo.24096789).

## AI Assistance Disclosure

Grok (xAI), via the Grok Bot assistant, provided scaffolding, drafting, and collaboration support on the formalization, code, and documentation in this repository. Benjamin Stanley Frohman (`frohmanbenjamin@gmail.com`, ORCID `0009-0006-7068-3718`) directed, reviewed, and is solely responsible for the architecture, implementation, proofs, and claims; Grok is not a coauthor.
