# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)

import json
from pathlib import Path
from titan_audit.cli import main
from titan_audit import auditor, vacuity, signing, tree_hash


def test_alias_modules_importable():
    assert "propext" in auditor.STANDARD_AXIOMS
    assert "sorry" in vacuity.FORBIDDEN
    assert callable(signing.sign_report)
    assert callable(tree_hash.tree_sha256)


def test_cli_version(capsys):
    rc = main(["--version"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "titan-audit 1.0.0" in out


def test_cli_verify_example_report(capsys):
    ex = Path(__file__).resolve().parent.parent / "examples" / "ns_millennium_proof_audit" / "report.json"
    rc = main(["verify", str(ex)])
    assert rc == 0
    assert "signature OK" in capsys.readouterr().out


def test_cli_audit_no_build(tmp_path):
    proj = tmp_path / "sample_proj"
    proj.mkdir()
    (proj / "lean-toolchain").write_text("leanprover/lean4:v4.30.0-rc1\n")
    (proj / "Sample.lean").write_text("theorem clean_thm : 1 + 1 = 2 := rfl\n")
    out_dir = tmp_path / "out"
    key_path = tmp_path / "test_ed25519.pem"
    rc = main([str(proj), "--no-build", "--out-dir", str(out_dir), "--key", str(key_path)])
    assert rc == 0
    rep_file = out_dir / "report.json"
    assert rep_file.exists()
    assert (out_dir / "report.md").exists()
    assert main(["verify", str(rep_file)]) == 0
