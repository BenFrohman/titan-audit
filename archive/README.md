# Archived files

These files are kept for provenance. They are not deleted.

## `workflows/`

`archive/workflows/titan-audit.yml` and `archive/workflows/titan-audit-ci.yml`
were early copies of this repository's own pytest job. They did not invoke the
GitHub Marketplace action, and they were never wired under `.github/workflows/`.

The living consumer example is [`examples/github-workflow.yml`](../examples/github-workflow.yml).
This repository's integration test is [`.github/workflows/self-test.yml`](../.github/workflows/self-test.yml).
