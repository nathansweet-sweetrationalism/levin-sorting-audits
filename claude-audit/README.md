# levin-sorting-audit

Machine-checkable audit (Claude Opus 5.5 in Claude Cowork, for Nathan Sweet) of the mathematics, code and citations in Joel Dietz, "Why Michael Levin Is 77.6++% Right on Platonic Ingress" (Substack, 2026-11-01 draft as supplied), and Nathan Sweet, "Why Michael Levin's Bubble Sort 'Revelation' Is Misunderstood" (revision of 2026-10-31).

- `REPORT.md`: findings, verdicts, recommended literature and tools, and the limits of the audit.
- `claims_ledger.json`: one row per claim, with verdict label, evidence, and SHA-256 of each cited result file.
- `CHECKPOINT.md`: the dated work log, written as the audit progressed.
- `run_all.sh`: one command to rebuild every result from pinned commits:
  cell_research 1fd2bd5, morpholib 35d30f4, and morpholib bfe377c for the replay of Sweet's numbers.
- `checks/`: the scripts. `m_*` exact mathematics (Python and an independent Node implementation); `f_*` code forensics; `u_*` isolated unit test of upstream code; `n_*` replay of Dietz's seeded model; `t_*` null model for Claim 4; `d_*` DOI resolution; `r_*` runs of the unmodified threaded upstream code (stochastic), including `r_upstream_sweet.py` (Sweet's endpoint tests on held-out inputs) and `r_conditional_test_calibration.py`; `compare_results.py` checks regenerated deterministic results against the published ones.
- `lean/AdjacentSwap.lean`: a general proof that an adjacent swap of an inverted pair lowers the inversion count by exactly one, for every list and position, plus witnesses. Lean 4 core only.
- `results/`: outputs plus `SHA256SUMS`. `sources/`: text extracts and nanopublication records used for string-matched quotations.

Deterministic checks must match exactly. Threaded-upstream results (`r_upstream*.json`) are distributions; compare means within the reported SE.

Full-text extracts of third-party papers used for quotation string-matching were removed for the public release; `PUBLIC_RELEASE_REMOVED_FILES.json` lists them with SHA-256 so the exact copies can be re-fetched and checked. Exact dependency versions: `requirements-audit.txt`; Lean toolchain: `lean-toolchain`.
