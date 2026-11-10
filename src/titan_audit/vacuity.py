# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
# DOI: 10.5281/zenodo.23630648
"""Semantic vacuity heuristics and forbidden-token scanner interface."""
from .scan import FORBIDDEN, DECL_RE, strip_comments, declarations, scan_file

__all__ = ["FORBIDDEN", "DECL_RE", "strip_comments", "declarations", "scan_file"]
