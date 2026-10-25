# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)

import json
import tempfile
from pathlib import Path
from titan_audit.scan import strip_comments, scan_file
from titan_audit.sign import load_or_create_key, sign_report, verify_report
from titan_audit.report_md import to_markdown
from titan_audit.tree_hash import tree_sha256


def _scan(src):
    d = Path(tempfile.mkdtemp())
    p = d / "T.lean"
    p.write_text(src, encoding="utf-8")
    return scan_file(p, "T.lean")


def test_comments_stripped():
    assert "sorry" not in strip_comments("/- sorry -/ -- sorry\ntheorem x : True := trivial")


def test_nested_block_comments_stripped():
    src = "/- outer /- inner sorry axiom foo : False -/ still comment -/\ntheorem t : 1 = 1 := rfl\n"
    assert _scan(src)["forbidden"] == []


def test_forbidden_detected():
    r = _scan("theorem x : 1 = 1 := by sorry\naxiom foo : False\n")
    kinds = {h["kind"] for h in r["forbidden"]}
    assert "sorry" in kinds and "axiom" in kinds


def test_native_decide_and_trust_compiler_detected():
    r = _scan("theorem b : true = true := by native_decide\n#check Lean.trustCompiler\n")
    kinds = {h["kind"] for h in r["forbidden"]}
    assert "native_decide" in kinds and "trustCompiler" in kinds


def test_commented_sorry_ignored():
    assert _scan("-- sorry\n/- axiom a : False -/\ntheorem x : True := trivial\n")["forbidden"] == []


def test_vacuity_isup():
    r = _scan("def S (f : ℕ → ℝ) : ℝ := ⨆ n, f n\n")
    vac_list = r.get("vacuity") or r.get("vacuity_heuristics", [])
    assert any(v["kind"] == "real_iSup_without_BddAbove" for v in vac_list)


def test_vacuity_isup_with_bddabove_clean():
    r = _scan("def S (f : ℕ → ℝ) (h : BddAbove (Set.range f)) : ℝ := ⨆ n, f n\n")
    vac_list = r.get("vacuity") or r.get("vacuity_heuristics", [])
    assert not any(v["kind"] == "real_iSup_without_BddAbove" for v in vac_list)


def test_vacuity_trivial_prop_and_binders():
    src = (
        "def MyGate : Prop := True\n"
        "theorem t1 (h1 : True) : 1 = 1 := rfl\n"
        "theorem t2 (h2 : False) : 1 = 2 := False.elim h2\n"
        "theorem t3 (hT : Tstar = ⊤) : 1 = 1 := rfl\n"
    )
    r = _scan(src)
    kinds = {v["kind"] for v in r["vacuity"]}
    assert "trivial_prop_def" in kinds
    assert "true_hypothesis" in kinds
    assert "false_hypothesis" in kinds
    assert "assumes_top" in kinds


def test_tree_sha256_deterministic(tmp_path):
    (tmp_path / "A.lean").write_text("theorem a : True := trivial\n")
    (tmp_path / "lean-toolchain").write_text("leanprover/lean4:v4.30.0-rc1\n")
    h1, entries1 = tree_sha256(tmp_path)
    h2, entries2 = tree_sha256(tmp_path)
    assert h1 == h2
    assert len(entries1) == 2
    assert entries1 == entries2


def test_sign_verify_roundtrip(tmp_path):
    key = load_or_create_key(tmp_path / "k.pem")
    assert oct((tmp_path / "k.pem").stat().st_mode)[-3:] == "600"
    rep = sign_report({"verdict": {"status": "PASS"}, "x": 1}, key)
    assert verify_report(rep)
    rep["x"] = 2
    assert not verify_report(rep)


def test_markdown_and_example_attestation():
    p = Path(__file__).resolve().parent.parent / "examples" / "ns_millennium_proof_audit" / "report.json"
    assert p.exists()
    data = json.loads(p.read_text())
    assert verify_report(data)
    md = to_markdown(data)
    assert "Verdict" in md
    assert "NS_Millennium_Proof" in md
