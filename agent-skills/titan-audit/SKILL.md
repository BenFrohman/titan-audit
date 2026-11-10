---
name: titan-audit
description: Audit a Lean 4 project (build, axioms, sorry scan, vacuity heuristics, tree hash) and emit a signed JSON/Markdown report.
---
# titan-audit skill
1. `cd /workspace/titan-audit`
2. `python3 -m titan_audit <project> --out-dir <project>/../reports` (add `--no-build` if already built)
3. `python3 -m titan_audit verify <reports>/report.json`
4. Summarize: verdict, theorem/clean counts, nonstandard axioms, in-build forbidden tokens, vacuity flags.
Never print `keys/*.pem`. Never describe PASS as proof that a statement is meaningful or that an open problem is solved.

<!--
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under the proprietary All Rights Reserved terms described in the file LICENSE.
Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
DOI: 10.5281/zenodo.23630648
-->
