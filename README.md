# Two AI audits of the Levin bubble-sort debate (Dietz and Sweet)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23866304.svg)](https://doi.org/10.5281/zenodo.23866304) [![verify](https://github.com/nathansweet-sweetrationalism/levin-sorting-audits/actions/workflows/verify.yml/badge.svg)](https://github.com/nathansweet-sweetrationalism/levin-sorting-audits/actions/workflows/verify.yml)

This repository holds two separately run, machine-checkable audits of the mathematics, code, citations and quotations in two articles about the self-sorting-array experiments of Zhang, Goldstein and Levin (2025):

- Joel Dietz, *Why Michael Levin Is 77.6++% Right on Platonic Ingress*. The text was supplied to the audits on November 1, 2026. Its public draft is in [fractastical/morpholib @ 35d30f4](https://github.com/fractastical/morpholib/tree/35d30f4cfd5397ee1ed769f96494e018603e293d/docs).
- Nathan Sweet, [*Why Michael Levin’s Bubble Sort “Revelation” Is Misunderstood*](https://sweetrationalism.com/articles/physics/computer-science/why-michael-levins-bubble-sort-revelation-is-misunderstood-classical-algorithm-theory-meets-god-of-the-gaps-argument/), revised October 13 and 31, 2026.

| Path | What it is |
|---|---|
| [`CROSS_AUDIT.md`](CROSS_AUDIT.md) | **Start here.** *Rerunning the Bubble-Sort Debate: What Two AI Audits Found in the Code Behind Dietz’s and Sweet’s Articles*: the readable comparison of both audits, claim by claim, with evidence labels |
| [`claude-audit/`](claude-audit/) | Audit run with Claude Opus 5.5 (model id `claude-opus-5-5`) in Claude Cowork. Python, Node.js and Lean 4 checks; runs of the original threaded code; `run_all.sh`; a claims ledger |
| [`codex-audit/`](codex-audit/) | Audit run with OpenAI Codex (GPT-6.1 Sol, as reported by the commissioning author). Python checks, FishShapes rebuild, nanopublication signature checks, a 64-claim ledger, RO-Crate metadata |
| [`verify_public_release.py`](verify_public_release.py) | Standard-library integrity check of this release |
| [`tools/check_quotes.py`](tools/check_quotes.py) | Confirms every quotation in `CROSS_AUDIT.md` is present in its pinned source |
| [`PROVENANCE.md`](PROVENANCE.md) | How this public release was derived from the two private bundles, with their SHA-256 |

## Verify

```bash
python3 verify_public_release.py          # manifest, Codex byte-identity to the private original, result checksums
python3 tools/check_quotes.py             # needs network and pdftotext (poppler-utils)
cd claude-audit && MODE=deterministic ./run_all.sh && python3 checks/compare_results.py <copy-of-original-results> results
```

The [`verify`](.github/workflows/verify.yml) workflow runs all three on every push and every week. Its actions are pinned to commit SHAs, and its Lean installer is pinned by SHA-256. The runs of the original multithreaded code are stochastic: run `claude-audit/run_all.sh` without `MODE` and compare means within their reported standard errors.

## What these audits are, and are not

- Both audits were run by AI coding agents at the request of Nathan Sweet, who is responsible for this release. The agents are tools, not authors. Agreement between the two is not independent scientific replication, because both read the same public code and data and their models share much of their training. Every result is therefore tied to a script, an output and a checksum.
- Each audit's findings, open items and limits are stated in its own report and in `CROSS_AUDIT.md`. Neither audit claims to settle any metaphysical question.
- Corrections are welcome, and an issue on this repository is the preferred channel. Released versions are immutable on Zenodo; corrections appear as new versions, with changes recorded in [`CHANGELOG.md`](CHANGELOG.md).

## Licences and third-party material

Code is MIT ([`LICENSE`](LICENSE)). Text, reports and results are CC BY 4.0 ([`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt)). Third-party material that is included, and its licences, are listed in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Copyrighted full texts, page captures, unlicensed upstream code and private correspondence metadata were removed. Each removal is listed with its SHA-256 in `*/PUBLIC_RELEASE_REMOVED_FILES.json`, so the exact files can be re-fetched and checked.

## Cite

Sweet, N. (2026). *Rerunning the Bubble-Sort Debate: Two AI audits of the Dietz and Sweet articles on Zhang, Goldstein & Levin's self-sorting arrays* [Software and audit archive]. Zenodo. https://doi.org/10.5281/zenodo.23866304

That concept DOI always resolves to the latest version. Each release also has its own DOI; v1.0.0 is https://doi.org/10.5281/zenodo.23866305. Use a version DOI when you need to cite exact bytes. GitHub’s “Cite this repository” button reads [`CITATION.cff`](CITATION.cff).

## Extracting the archive

Zenodo stores each release as a zip. One filename contains an en dash (`codex-audit/external/morpholib/models/2021-Cervera–Levin–Mafe.py`). Some builds of Info-ZIP `unzip` without Unicode support write that name as `#U2013`, and `verify_public_release.py` then reports it missing. Extract with `python3 -m zipfile -e <zip> <dir>`, 7-Zip, or a UTF-8-aware `unzip`, or clone the repository instead.
