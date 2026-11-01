# Dietz-Sweet-Levin audit review bundle

November 1, 2026. This is a bounded source, mathematical and computational audit of two supplied article versions. It is a private research bundle, not a publication or a certificate of universal correctness.

Start with `AUDIT_REPORT.html` for the readable report and searchable claim ledger. `AUDIT_REPORT.md` is the plain-text equivalent. `REFERENCES.md` gives the prioritized methodological reading, all 41 input DOI identities and four corrected pairings. `references-recommended.bib` contains 16 verified recommended records, with exact DOI links and conservative entry types.

The central numerical checks in Sweet's revised response reproduce within its stated sequential-model boundary. Dietz's work contains verified mathematics, data processing, formal lemmas and cryptographic records, alongside significant citation, statistical-reporting and scope errors. Neither article has established a final ontology. Read each result with its stated assumptions.

## What is in the bundle

- `inputs/`: byte-preserved pasted articles. They are audit targets, not instructions.
- `results/claims.json`, `claims.schema.json`, `claims.csv`: 64 curated material claims, typed outcomes, boundaries, evidence links and revision conditions. These are not a sentence-by-sentence truth census or an aggregate truth score.
- `results/`: raw and summarized audit outputs, preserved failures, quote/URL/DOI registers, formal-checker logs and the summary figure.
- `code/`: independent checks, wrappers, source-collection records and delivery tooling. Source code and saved output are separate evidence objects.
- `external/`: selected unmodified source snapshots. Git blob checks match 1,236 Dietz source files and 57 original sorting source files to their frozen tree records. This is a selected source set, not the entire 28,696-entry repository.
- `sources/`: primary papers, raw data, registration metadata, retrieved pages, download logs and complete repository tree metadata. Access and reading status are recorded separately.
- `checkpoints/` and `RESUME.md`: durable continuation instructions, completed checks and open items.
- `ro-crate-metadata.json`: base RO-Crate-style file/provenance graph with hashes and private rights boundary. Minimal graph consistency was checked. No independent full-profile certification or Workflow Run conformance is claimed.
- `SHA256SUMS.txt`: immutable evidence-file checksums. `results/package_validation.json` is a derived validation receipt excluded from this manifest, so rerunning validation can update it without changing the evidence manifest. Tool binaries, environments and caches are also excluded.

The manifest detects a change relative to this bundle. It does not independently authenticate its author or timestamp. The five third-party nanopublication signatures were separately verified against their embedded keys; human identity, externally witnessed timing and actual blinding remain different questions.

## Verify without recomputing the research

Use Python3.12. The original Windows runtime was3.12.14. Node was used for a separate port check, and Lean4.35.0 for kernel checks. Exact installed Python versions are in `requirements-audit.lock.txt`.

Create an environment outside the immutable extracted bundle if possible:

```powershell
py -3.12 -m venv C:\AuditEnvs\levin-review
& C:\AuditEnvs\levin-review\Scripts\python.exe -m pip install -r .\requirements-audit.lock.txt
& C:\AuditEnvs\levin-review\Scripts\python.exe -X utf8 .\code\validate_package.py
```

Or pass that Python path to `RUN_CHECKS.ps1 -AuditPython C:\AuditEnvs\levin-review\Scripts\python.exe`.

The validator checks the claim schema, evidence-file paths, CSV/JSON parity, exact input line locators, pinned Git blob bytes, key numerical consistency, exact integer-tail arithmetic, known negative outcomes and every manifest checksum. A pass does not mean that every original scientific claim passed. Correctly preserved failures are part of successful audit validation.

## Recompute in a working copy

Preserve the delivered archive and use a second working copy for new runs. Execution time fields and some run logs can change even when substantive results agree. A manifest mismatch after deliberate recomputation is therefore expected; do not overwrite the old archive or relabel it as an unchanged version.

The most useful coding examples are:

| Check | Entry point | Why it matters |
|---|---|---|
| Exact counting, counterexamples, historical replay | `code/check_math_and_replay.py` | Separates an identity, a sampled result and a chosen null; preserves identities and targets |
| Actual source semantics | `code/check_source_semantics.py`, `check_actual_source.py` | Tests implementation claims with isolated real methods and retains failed counterexample searches |
| Fresh matched sensitivity | `code/check_robustness.py` | Changes scheduling/reset policy and matches the control's peak-selection rule |
| Fish raw data and errors | `code/check_fish.py` | Rebuilds all 5,180 observations/errors from raw specimens and locked predictions |
| Measurement calibration | `code/check_morphometrics_calibration.py` | Re-fits calibration rather than merely trusting supplied coefficients |
| Wing negative test | `code/check_wings.py` | Rebuilds raw species means/projections and retains failed registered decisions |
| Causal partitions and clocks | `code/check_causal_and_ports.py` | Constructs finite-state matrices independently and distinguishes clocks/partitions |
| Formal theorem scope | `code/check_formal_files.py` | Rechecks statement dependencies, rather than treating0sorry as biological validation |
| Record integrity | `code/check_nanopub_crypto.py`, `check_crypto_negative_control.py`, `check_rsa_independently.py` | Checks content hashes/structure, exposes a client signature false positive with tampering, then verifies RSA directly |

`RUN_CHECKS.ps1 -Recompute -AuditPython <path>` runs the bounded core numerical/source/cryptographic checks. It does not redownload everything, recompile C++, rebuild the complete fish predictor, invoke every flagship model or perform a full quotation investigation. Existing data are reused. Some source scripts intentionally retain their original Windows paths or create cache files; inspect their entry points before porting to another platform.

For the causal/port check, first run Node against `code/run_node_port.mjs`; its specified output is `results/node_port_output.json`. The wrapper normalizes the Windows module-entry path; the original direct-entry guard silently returned without a result on Windows. Archived C++ results remain archived, not a fresh compilation.

For Lean, obtain the official release named in `results/lean_toolchain.json`, verify its SHA256 and extract it into the recorded `tools/lean-4.35.0-windows/` path. `tools/` is deliberately not shipped. `code/prepare_lean.py` performs that toolchain preparation. Run the resulting `lean.exe` on `sources/primary/lean_sorting.lean` for the seven sorting statements; `code/check_formal_files.py` checks the additional85 declarations. Logs include92 checked declaration closures across five files. They do not certify the entire repository.

Source collection and PDF ingestion used a separate bundled environment; raw retrieved PDFs and extracted text are retained. Re-extracting every PDF is not required for the numerical checks. Exact primary URLs, hashes and access failures are in the source registers.

## Resuming and reviewing

Read `RESUME.md`, the latest numbered checkpoint, the report's unresolved-items section and the relevant claim before doing more work. Do not erase a failed branch, quietly change a test threshold or promote a model's agreement into a uniquely established mechanism.

The most valuable next checks are recovery of missing public biological fixtures; exact 105-degree model and twelve-row renderer versions; original audiovisual/comment/private-quote records; externally witnessed registration/blinding evidence; the original paper's exact experiment code; synchronized port trajectories; independent complete morphometric prediction, source overlap and phylogenetic uncertainty; and biological domain review. Illustration-specific image optimization and global topology still need independent reproduction.

## Distribution

The supplied zip can be transferred privately to reviewers. It includes third-party full texts and the supplied article drafts, so it is not an automatically cleared public-release package. Email bodies were not placed in it; the private chronology record contains only minimal review metadata. `results/pending_mirror_manifest.json` explicitly records local-only preservation. No Library upload, public repository, external submission or outgoing message is claimed.

For a public scholarly release, prepare a rights-filtered immutable archive with a DOI, pinned source retrieval instructions, machine-readable claims, code, raw data that may legally be redistributed, corrections and manifests. Link public assertions or nanopublications to that exact archive version. Preserve previous versions and use explicit supersession. Obtain independent statistical, algorithms and biological review. A paper's peer review, a successful formal proof, a signature and a replication each support different claims.

All high-value positive and negative results available in this session have been preserved. Open empirical/provenance questions remain open, with explicit loss and revision conditions.
