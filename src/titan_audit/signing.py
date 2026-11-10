# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Ed25519 cryptographic attestation signing and verification interface."""
from .sign import canonical, load_or_create_key, public_b64, sign_report, verify_report

__all__ = ["canonical", "load_or_create_key", "public_b64", "sign_report", "verify_report"]
