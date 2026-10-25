#!/usr/bin/env bash
# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
#
# Frohmanian Green-Build & Kernel Axiom Gate:
# 1. Runs `lake exe cache get` (if Mathlib is configured) and `lake build`
# 2. Rejects forbidden tokens (`sorry`, `admit`, `axiom`, `native_decide`) in comment-stripped source modules
# 3. Verifies `#print axioms` on all targets in `scripts/audit_targets.txt`
# 4. Runs the in-kernel metaprogramming `AxiomAudit.lean` (`Lean.collectAxioms` walker)

set -euo pipefail
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")/.."
LIB="${LIB:-LeanKernelGate}"

if grep -q mathlib lakefile.toml 2>/dev/null || grep -q mathlib lakefile.lean 2>/dev/null; then
  lake exe cache get || echo "warn: cache miss"
fi

lake build

echo "--- scanning comment-stripped source for sorry/admit/axiom/native_decide ---"
python3 - "$LIB" "$LIB.lean" <<'PY'
import pathlib, re, sys

FORBIDDEN = re.compile(r"\b(sorry|admit|native_decide)\b|^\s*axiom\b", re.MULTILINE)

def strip_comments(s: str) -> str:
    out, i, n, depth = [], 0, len(s), 0
    while i < n:
        if depth == 0 and s[i:i+2] == "--":
            while i < n and s[i] != "\n":
                out.append(" "); i += 1
        elif s[i:i+2] == "/-":
            depth += 1; out.append("  "); i += 2
        elif depth > 0 and s[i:i+2] == "-/":
            depth -= 1; out.append("  "); i += 2
        else:
            out.append("\n" if s[i] == "\n" else (" " if depth > 0 else s[i]))
            i += 1
    return "".join(out)

files = []
for arg in sys.argv[1:]:
    p = pathlib.Path(arg)
    if p.is_dir():
        files.extend(sorted(p.rglob("*.lean")))
    elif p.is_file():
        files.append(p)

hits = []
for f in files:
    cleaned = strip_comments(f.read_text(encoding="utf-8", errors="replace"))
    for lineno, line in enumerate(cleaned.splitlines(), 1):
        m = FORBIDDEN.search(line)
        if m:
            hits.append(f"{f}:{lineno}: forbidden token `{m.group(0).strip()}`")

if hits:
    for h in hits:
        print(h)
    print("FAIL: forbidden token found")
    sys.exit(1)
print("OK: 0 forbidden tokens in comment-stripped source")
PY

echo "--- #print axioms target audit ---"
tmp=".axiom_target_audit_$$.lean"
trap 'rm -f "$tmp"' EXIT
{
  echo "import $LIB"
  while read -r d; do
    [ -n "$d" ] && echo "#print axioms $d"
  done < scripts/audit_targets.txt
} > "$tmp"
out=$(lake env lean "$tmp")
echo "$out"
rm -f "$tmp"

if echo "$out" | grep -q sorryAx; then
  echo "FAIL: sorryAx detected"
  exit 1
fi
if echo "$out" | grep -oE "\[[^]]*\]" | tr -d '[] ' | tr ',' '\n' | grep -vxE 'propext|Classical\.choice|Quot\.sound|' ; then
  echo "FAIL: nonstandard axiom detected"
  exit 1
fi

echo "--- in-kernel Lean.collectAxioms audit (AxiomAudit.lean) ---"
lake env lean AxiomAudit.lean

echo "PASS"
