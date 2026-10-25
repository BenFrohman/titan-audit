#!/usr/bin/env bash
# Copyright 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman (ORCID: 0009-0006-7068-3718)
set -euo pipefail
exec "$(dirname "$0")/scripts/check.sh" "$@"
