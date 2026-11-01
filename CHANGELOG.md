# Changelog

## v1.0.0 (2026-11-01)

First public release.

- `CROSS_AUDIT.md`, the cross-audit article. Quotations are checked by `tools/check_quotes.py`. Joel Dietz's text is cited through its public draft files in morpholib @ 35d30f4, because the Substack post was not live on 2026-11-01. One quotation of Sweet was corrected from a paraphrase to his exact sentence. The duplicated-fragment correction was rescoped: the fragment is in the copy pasted to the audits, not on the live page.
- `claude-audit/` changes relative to the private bundle:
  - Full-text paper extracts and an editing worksheet removed.
  - Erratum added to `REPORT.md`: the missed direction of Dietz's nearest-relative result, the second-pass held-out tests, and withdrawal of row S13.
  - `f_code_forensics.py` now reads only bytecode tracked by the upstream repository. The earlier published result had also listed `cpython-313` bytecode created by the audit's own imports. The upstream findings, which concern the 310 and 311 bytecode, are unchanged.
  - `run_all.sh` uses a sparse partial clone of morpholib, sets `PYTHONDONTWRITEBYTECODE`, adds `MODE=deterministic` and the second-pass tests.
  - `compare_results.py`, `requirements-audit.txt` and `lean-toolchain` added.
  - The Crossref contact address is now read from `CROSSREF_MAILTO` and is no longer hard-coded.
- `codex-audit/`: rights-filtered, with every kept file byte-identical to the private original.
