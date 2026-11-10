#!/usr/bin/env bash
# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under the proprietary All Rights Reserved terms described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
set -euo pipefail
exec "$(dirname "$0")/scripts/check.sh" "$@"
