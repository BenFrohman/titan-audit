# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Ed25519 cryptographic signing and verification of canonical JSON audit reports."""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def load_or_create_key(path: Path) -> Ed25519PrivateKey:
    path = Path(path)
    if path.exists():
        return serialization.load_pem_private_key(path.read_bytes(), password=None)
    path.parent.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                            serialization.NoEncryption())
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(pem)
    pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    path.with_suffix(".pub").write_text(base64.b64encode(pub).decode() + "\n")
    return key


def public_b64(key: Ed25519PrivateKey) -> str:
    raw = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def sign_report(report: dict, key: Ed25519PrivateKey) -> dict:
    body = {k: v for k, v in report.items() if k != "signature"}
    sig = key.sign(canonical(body))
    report = dict(body)
    report["signature"] = {"alg": "ed25519", "public_key_b64": public_b64(key),
                           "payload": "canonical JSON of report without 'signature' (sort_keys, compact, UTF-8)",
                           "value_b64": base64.b64encode(sig).decode()}
    return report


def verify_report(report: dict, public_key_b64: str | None = None) -> bool:
    sig = report.get("signature") or {}
    pk = public_key_b64 or sig.get("public_key_b64")
    if not pk or "value_b64" not in sig:
        return False
    body = {k: v for k, v in report.items() if k != "signature"}
    try:
        Ed25519PublicKey.from_public_bytes(base64.b64decode(pk)).verify(
            base64.b64decode(sig["value_b64"]), canonical(body))
        return True
    except Exception:
        return False
