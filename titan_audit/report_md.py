# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Markdown summary renderer for a titan-audit report."""


def to_markdown(r: dict) -> str:
    b, a, s, v = r["build"], r["axiom_audit"], r["source_scan"], r["verdict"]
    L = [f"# titan-audit report: `{r['project']['name']}`", "",
         f"**Verdict: {v['status']}**" + (f" ({'; '.join(v['reasons'])})" if v["reasons"] else ""), "",
         f"- Generated (UTC): {r['generated_at_utc']}",
         f"- Tool: titan-audit {r['tool']['version']} ({r['tool']['author']})",
         f"- Toolchain: `{r['project']['lean_toolchain']}`  Git HEAD: `{r['project']['git_head']}`",
         f"- Tree SHA-256: `{r['tree']['sha256']}` over {r['tree']['files']} files", "",
         "## Build", ""]
    if b.get("requested"):
        L += [f"- Success: {b.get('success')}  Jobs: {b.get('jobs')}  Errors: {len(b.get('errors', []))}",
              f"- `sorry` warnings: {b.get('sorry_warnings')}  Unused-variable warnings: {len(b.get('unused_variable_warnings', []))}"]
    else:
        L.append("- Build skipped (`--no-build`); audit used existing .olean files.")
    L += ["", "## Axiom audit", "",
          f"- Modules: {a['modules']}  Theorems: {a['theorems']}  Clean (only propext/Classical.choice/Quot.sound): {a['clean_theorems']}",
          f"- Nonstandard: {len(a['nonstandard'])}", "", "| Module | Theorems | Nonstandard |", "|---|---:|---:|"]
    for m, e in sorted(a["per_module"].items()):
        L.append(f"| `{m}` | {e['theorems']} | {e['nonstandard']} |")
    for t in a["nonstandard"][:50]:
        L.append(f"- `{t['name']}`: {', '.join(t['axioms'])}")
    L += ["", "## Source scan", "", "Counts: " + (", ".join(f"{k}={n}" for k, n in sorted(s["counts"].items())) or "none"), ""]
    for h in [h for h in s["forbidden"] if h["in_build"]][:50]:
        L.append(f"- **{h['kind']}** `{h['file']}:{h['line']}`: `{h['text']}`")
    L += ["", "### Vacuity heuristics (in build)", ""]
    vb = [h for h in s["vacuity_heuristics"] if h["in_build"]]
    L += [f"- {h['kind']} `{h['file']}:{h['line']}` `{h['decl']}`: {h['detail']}" for h in vb[:80]] or ["- none"]
    L += ["", "Heuristics are advisory: a flag means *look here*, not *wrong*.", "",
          "## Signature", "", f"- ed25519 public key (base64): `{r.get('signature', {}).get('public_key_b64', 'unsigned')}`",
          "- Verify: `titan-audit verify report.json`", ""]
    return "\n".join(L)
