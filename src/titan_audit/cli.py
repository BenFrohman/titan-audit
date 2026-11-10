# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Command line: `titan-audit <lean-project-dir>` and `titan-audit verify <report.json>`."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import audit
from .report_md import to_markdown
from .sign import load_or_create_key, sign_report, verify_report

DEFAULT_KEY = Path(__file__).resolve().parent.parent / "keys" / "dev_ed25519.pem"


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("--version", "-V"):
        print(f"titan-audit {__version__} (Author: Benjamin Stanley Frohman, ORCID: 0009-0006-7068-3718)")
        return 0
    if argv and argv[0] == "verify":
        ap = argparse.ArgumentParser(prog="titan-audit verify",
                                     description="Verify an Ed25519-signed titan-audit JSON attestation.")
        ap.add_argument("report", help="Path to report.json")
        ap.add_argument("--public-key", help="Expected base64 ed25519 public key (defaults to embedded key)")
        ns = ap.parse_args(argv[1:])
        ok = verify_report(json.loads(Path(ns.report).read_text()), ns.public_key)
        print("signature OK" if ok else "signature INVALID")
        return 0 if ok else 1

    ap = argparse.ArgumentParser(
        prog="titan-audit",
        description="Reproducible, Ed25519-signed verification & semantic vacuity audit of a Lean 4 / Lake project."
    )
    ap.add_argument("project", help="Path to the Lean 4 / Lake project root")
    ap.add_argument("--out-dir", default=None, help="Output directory (default: <project>/titan-audit-report)")
    ap.add_argument("--no-build", action="store_true", help="Skip `lake build` (use existing .olean artifacts)")
    ap.add_argument("--cache", action="store_true", help="Run `lake exe cache get` before building (Mathlib projects)")
    ap.add_argument("--key", default=str(DEFAULT_KEY), help="Ed25519 PEM private key path (created with 0600 if missing)")
    ap.add_argument("--no-sign", action="store_true", help="Omit Ed25519 cryptographic signature")
    ap.add_argument("--no-entries", action="store_true", help="Omit per-file SHA-256 entries from JSON output")
    ap.add_argument("--timeout", type=int, default=7200, help="Subprocess timeout in seconds (default: 7200)")
    ap.add_argument("--fail-on-warn", action="store_true", help="Exit 1 on PASS_WITH_WARNINGS (strict vacuity gate)")
    ns = ap.parse_args(argv)

    rep = audit(Path(ns.project), build=not ns.no_build, cache=ns.cache, timeout=ns.timeout)
    if ns.no_entries:
        rep["tree"].pop("entries", None)
    if not ns.no_sign:
        rep = sign_report(rep, load_or_create_key(Path(ns.key)))
    out = Path(ns.out_dir or Path(ns.project) / "titan-audit-report")
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n")
    (out / "report.md").write_text(to_markdown(rep))
    st = rep["verdict"]["status"]
    print(f"{st}: theorems={rep['axiom_audit']['theorems']} clean={rep['axiom_audit']['clean_theorems']} "
          f"jobs={rep['build'].get('jobs')} tree={rep['tree']['sha256'][:16]} -> {out}")
    if st == "FAIL" or (ns.fail_on_warn and st != "PASS"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
