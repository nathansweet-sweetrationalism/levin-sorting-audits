# Checkpoint 10: verification-tool correction and delivery

Negative controls caught a signature-checking defect in nanopub2.2.2. It reports a signature pass for altered assertions because it ignores the cryptographic Boolean failure; its normalized input also includes the signature triple. The initial client-only result is not sufficient evidence.

The corrected direct method excludes that triple and checks RSA PKCS#1 v1.5 with two cryptographic interfaces. All five originals validate; all five altered assertions fail. Trusty hashes and RDF structure also pass for the originals. Shared RDF normalization, human identity, timing and blinding remain explicit limitations. Failed and corrected methods are preserved rather than erased. No external bug report or message was sent.

The final review surface is AUDIT_REPORT.html, with a readable report, summary figure and searchable 64-claim ledger. Markdown, JSON, CSV, schema, BibTeX, source registers and all numerical outputs are included. The report was rendered in an isolated headless browser; its initial viewport was visually inspected, 64 claim elements were found and the filter script initialized correctly.

The final package validator checks schema, line locators, source bytes, input hashes, numerical consistency, retained negative results and the manifest. Its final receipt is results/package_validation.json. A successful audit-package check includes failures of original scientific claims and failures of the initial verification tool.

The archive excludes the local Python environment, large downloaded tools and caches. Keep the immutable archive before recomputing. The workspace mirror contains the same review bundle and its checksum; no public deposit is claimed. Resume with RESUME.md, the relevant claim and its open revision condition. The original threaded experiment, missing biological fixtures, selected image optimizations and fuller phylogenetic/biological bridges remain unresolved.
