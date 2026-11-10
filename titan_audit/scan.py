# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Source scanning: forbidden tokens and semantic vacuity heuristics (comment-aware)."""
from __future__ import annotations

import re
from pathlib import Path

FORBIDDEN = {
    "sorry": re.compile(r"(?<![\w.'])sorry(?![\w'])"),
    "admit": re.compile(r"(?<![\w.'])admit(?![\w'])"),
    "axiom": re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|public\s+|protected\s+)*axiom\s+(\S+)", re.M),
    "native_decide": re.compile(r"(?<![\w.'])native_decide(?![\w'])"),
    "trustCompiler": re.compile(r"Lean\.trustCompiler|Lean\.ofReduceBool"),
}


def strip_comments(src: str) -> str:
    """Blank out `--` line comments, nested `/- -/` block comments and string
    literals, preserving newlines so line numbers stay valid."""
    out = []
    i, n, depth = 0, len(src), 0
    in_str = False
    while i < n:
        c = src[i]
        two = src[i:i + 2]
        if depth == 0 and not in_str and two == "--":
            j = src.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
            continue
        if not in_str and two == "/-":
            depth += 1
            out.append("  ")
            i += 2
            continue
        if depth > 0:
            if two == "-/":
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
            continue
        if c == '"' and (i == 0 or src[i - 1] != "\\") and src[i - 1:i] != "'":
            in_str = not in_str
            out.append(" ")
            i += 1
            continue
        out.append(("\n" if c == "\n" else " ") if in_str else c)
        i += 1
    return "".join(out)


def _line(src: str, pos: int) -> int:
    return src.count("\n", 0, pos) + 1


DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:(?:private|public|protected|noncomputable|nonrec|partial|unsafe)\s+)*"
    r"(def|abbrev|theorem|lemma|structure|class|instance|opaque|axiom|example)\b\s*([^\s(:{\[]*)",
    re.M,
)


def declarations(clean: str):
    """Yield (kind, name, start, end) spans of top-level declarations."""
    ms = list(DECL_RE.finditer(clean))
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(clean)
        yield m.group(1), m.group(2), m.start(), end


def scan_file(path: Path, rel: str) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    clean = strip_comments(raw)
    hits = []
    for kind, rx in FORBIDDEN.items():
        for m in rx.finditer(clean):
            hits.append({"kind": kind, "file": rel, "line": _line(clean, m.start()),
                         "text": raw.splitlines()[_line(clean, m.start()) - 1].strip()[:200]})
    vac = []
    for kind, name, s, e in declarations(clean):
        body = clean[s:e]
        ln = _line(clean, s)
        # 1. real-valued iSup / sSup without any BddAbove guard in the same declaration
        if re.search(r"⨆|\biSup\b|\bsSup\b|\bciSup\b", body) and "BddAbove" not in body \
                and re.search(r"ℝ|Real", body) and kind in ("def", "abbrev"):
            vac.append({"kind": "real_iSup_without_BddAbove", "file": rel, "line": ln, "decl": name,
                        "detail": "Real iSup/sSup is 0 on unbounded ranges; downstream bounds on it may be vacuous unless BddAbove is required."})
        # 2. Prop definitions that are literally True / ⊤
        if kind in ("def", "abbrev") and re.search(r":\s*Prop\s*:=\s*(True|⊤)\s*$", body.strip(), re.M):
            vac.append({"kind": "trivial_prop_def", "file": rel, "line": ln, "decl": name,
                        "detail": "Prop definition is `True`/`⊤`; anything gated on it is vacuous."})
        # 3. binders of type True, or ': ... = ⊤' style assumed-top hypotheses
        for m in re.finditer(r"\((h\w*)\s*:\s*True\)", body):
            vac.append({"kind": "true_hypothesis", "file": rel, "line": _line(clean, s + m.start()),
                        "decl": name, "detail": f"binder `{m.group(1)} : True` carries no content."})
        if kind in ("theorem", "lemma"):
            for m in re.finditer(r"\((h\w*)\s*:[^()]*?=\s*⊤\)", body):
                vac.append({"kind": "assumes_top", "file": rel, "line": _line(clean, s + m.start()),
                            "decl": name,
                            "detail": f"hypothesis `{m.group(1)}` assumes something equals ⊤ (e.g. global existence time); check the conclusion is not circular."})
            for m in re.finditer(r"\((h\w*)\s*:\s*False\)", body):
                vac.append({"kind": "false_hypothesis", "file": rel, "line": _line(clean, s + m.start()),
                            "decl": name, "detail": "hypothesis of type False: theorem is vacuous."})
    return {"forbidden": hits, "vacuity": vac}
