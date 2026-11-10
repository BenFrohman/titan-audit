# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Build, in-kernel metaprogramming axiom-audit, SHA-256 tree hash, and report assembly."""
from __future__ import annotations

import datetime as _dt
import hashlib
import re
import subprocess
import tempfile
from pathlib import Path

from . import __version__
from .scan import scan_file

STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXCLUDE_DIRS = {".lake", ".git", "lake-packages", "build", ".github", "node_modules"}
HASHED_NAMES = {"lakefile.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain"}


def run(cmd, cwd, timeout):
    import os
    elan_bin = str(Path.home() / ".elan" / "bin")
    env = {**os.environ, "TERM": "dumb", "PATH": f"{elan_bin}:{os.environ.get('PATH', '')}"}
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def source_files(root: Path):
    for p in sorted(root.rglob("*.lean")):
        rel = p.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts[:-1]):
            continue
        yield p, rel.as_posix()


def tree_sha256(root: Path) -> tuple[str, list[dict]]:
    entries = []
    files = [p for p, _ in source_files(root)] + [root / n for n in HASHED_NAMES if (root / n).exists()]
    for p in sorted(set(files)):
        entries.append({"path": p.relative_to(root).as_posix(),
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    entries.sort(key=lambda e: e["path"])
    manifest = "".join(f"{e['sha256']}  {e['path']}\n" for e in entries)
    return hashlib.sha256(manifest.encode()).hexdigest(), entries


def built_modules(root: Path) -> list[str]:
    olean_root = root / ".lake" / "build" / "lib" / "lean"
    mods = []
    for p, rel in source_files(root):
        if rel in ("lakefile.lean",):
            continue
        if (olean_root / Path(rel).with_suffix(".olean")).exists():
            mods.append(rel[:-5].replace("/", "."))
    return mods


AUDIT_TEMPLATE = """import Lean
{imports}
open Lean Elab Command
#eval show CommandElabM Unit from do
  let env ← getEnv
  let targets : Array Name := #[{targets}]
  for (n, ci) in env.constants.toList do
    if n.isInternal then continue
    let some idx := env.getModuleIdxFor? n | continue
    let mod := env.header.moduleNames[idx.toNat]!
    unless targets.contains mod do continue
    unless ci matches .thmInfo _ do continue
    let axs ← liftCoreM <| Lean.collectAxioms n
    let axStr := String.intercalate "," (axs.toList.map toString)
    IO.println s!"TA\t{{mod}}\t{{n}}\t{{axStr}}"
"""


def axiom_audit(root: Path, modules: list[str], timeout: int):
    if not modules:
        return {"ran": False, "error": "no built modules found"}, []
    src = AUDIT_TEMPLATE.format(imports="\n".join(f"import {m}" for m in modules),
                                targets=", ".join(f"`{m}" for m in modules))
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, dir=root) as f:
        f.write(src)
        tmp = Path(f.name)
    try:
        code, out = run(["lake", "env", "lean", str(tmp)], root, timeout)
    finally:
        tmp.unlink(missing_ok=True)
    thms = []
    for line in out.splitlines():
        if line.startswith("TA\t"):
            _, mod, name, axs = line.split("\t", 3)
            ax = [a for a in axs.split(",") if a]
            thms.append({"module": mod, "name": name, "axioms": ax,
                         "nonstandard": sorted(set(ax) - STANDARD_AXIOMS)})
    errors = [l for l in out.splitlines() if ": error" in l][:50]
    return {"ran": True, "exit_code": code, "errors": errors}, thms


def audit(project: Path, *, build: bool = True, cache: bool = False, timeout: int = 7200) -> dict:
    root = Path(project).resolve()
    started = _dt.datetime.now(_dt.timezone.utc)
    rep: dict = {"tool": {"name": "titan-audit", "version": __version__,
                          "author": "Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)",
                          "doi": "10.5281/zenodo.23630648"},
                 "project": {"path": str(root), "name": root.name}}
    tc = root / "lean-toolchain"
    rep["project"]["lean_toolchain"] = tc.read_text().strip() if tc.exists() else None
    code, out = run(["git", "rev-parse", "HEAD"], root, 30) if (root / ".git").exists() else (1, "")
    rep["project"]["git_head"] = out.strip() if code == 0 else None

    b: dict = {"requested": build}
    if cache:
        c, o = run(["lake", "exe", "cache", "get"], root, timeout)
        b["cache_get_exit"] = c
    if build:
        c, o = run(["lake", "build"], root, timeout)
        m = re.search(r"Build completed successfully \((\d+) jobs?\)", o)
        b.update({"exit_code": c, "success": c == 0, "jobs": int(m.group(1)) if m else None,
                  "errors": [l for l in o.splitlines() if l.startswith("error")][:50],
                  "sorry_warnings": len(re.findall(r"declaration uses 'sorry'", o)),
                  "unused_variable_warnings": [l for l in o.splitlines() if "unused variable" in l][:200]})
    rep["build"] = b

    mods = built_modules(root)
    meta, thms = axiom_audit(root, mods, timeout)
    nonstd = [t for t in thms if t["nonstandard"]]
    rep["axiom_audit"] = {**meta, "modules": len(mods), "theorems": len(thms),
                          "clean_theorems": len(thms) - len(nonstd),
                          "nonstandard": [{"name": t["name"], "module": t["module"], "axioms": t["nonstandard"]} for t in nonstd],
                          "per_module": _per_module(thms)}

    forbidden, vac = [], []
    for p, rel in source_files(root):
        r = scan_file(p, rel)
        forbidden += r["forbidden"]
        vac += r["vacuity"]
    built_files = {m.replace(".", "/") + ".lean" for m in mods}
    for h in forbidden + vac:
        h["in_build"] = h["file"] in built_files
    rep["source_scan"] = {"forbidden": forbidden, "vacuity_heuristics": vac,
                          "counts": _counts(forbidden, vac, built_files)}

    tree, entries = tree_sha256(root)
    rep["tree"] = {"sha256": tree, "files": len(entries), "entries": entries,
                   "method": "sha256 of 'sha256  path\\n' lines, sorted by path, over *.lean (excluding .lake/.git) + lakefile/manifest/toolchain"}
    rep["verdict"] = _verdict(rep)
    rep["generated_at_utc"] = started.isoformat(timespec="seconds")
    return rep


def _per_module(thms):
    d: dict = {}
    for t in thms:
        e = d.setdefault(t["module"], {"theorems": 0, "nonstandard": 0})
        e["theorems"] += 1
        e["nonstandard"] += bool(t["nonstandard"])
    return d


def _counts(forbidden, vac, built):
    c: dict = {}
    for h in forbidden + vac:
        k = h["kind"] + ("" if h["file"] in built else "_outside_build")
        c[k] = c.get(k, 0) + 1
    return c


def _verdict(rep):
    reasons = []
    b = rep["build"]
    if b.get("requested") and not b.get("success"):
        reasons.append("build failed")
    if b.get("sorry_warnings"):
        reasons.append(f"{b['sorry_warnings']} sorry warnings in build")
    if rep["axiom_audit"]["nonstandard"]:
        reasons.append(f"{len(rep['axiom_audit']['nonstandard'])} theorems use nonstandard axioms")
    inb = [h for h in rep["source_scan"]["forbidden"] if h["in_build"]]
    if inb:
        reasons.append(f"{len(inb)} forbidden tokens in built sources")
    warn = [h for h in rep["source_scan"]["vacuity_heuristics"] if h["in_build"]]
    status = "FAIL" if reasons else ("PASS_WITH_WARNINGS" if warn else "PASS")
    return {"status": status, "reasons": reasons, "vacuity_warnings_in_build": len(warn)}
