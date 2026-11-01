# Third-party material included in this release

| Material | Location | Source | Licence |
|---|---|---|---|
| Selected files of fractastical/morpholib (code, the article draft builders, the bfe377c model, Lean files) | `codex-audit/external/morpholib/`, `codex-audit/sources/primary/old_*.py`, `lean_sorting.lean`, `port_js.mjs` and related files | https://github.com/fractastical/morpholib, © 2026 Joel Dietz | MIT (`codex-audit/sources/primary/morpholib_LICENSE`) |
| FishShapes v1 specimen measurements | `codex-audit/sources/primary/FishShapes_specimensv1.csv` | Price et al. 2022, Dryad, doi:10.5061/dryad.vt4b8gtvf | CC0-1.0 |
| Vespinae wing landmarks and specimen list | `codex-audit/sources/primary/wing_*.tab` | Abels & Wedmann, PANGAEA, doi:10.1594/PANGAEA.937651 and doi:10.1594/PANGAEA.937635 | CC BY 4.0 |
| Nanopublication records | `claude-audit/sources/np_*.trig`, `codex-audit/sources/nanopub_registry/` | Knowledge Pixels nanopublication registry | CC BY 4.0 or CC0 (as declared in each record) |
| nanopub 2.2.2 signing utilities, an excerpt kept to document a verification-client defect | `codex-audit/sources/tool_checks/nanopub_2_2_2_sign_utils.py` | https://pypi.org/project/nanopub/2.2.2/ | Apache-2.0 |
| D'Arcy Thompson, *On Aristotle as a Biologist* (1913), OCR text | `codex-audit/sources/primary/thompson1913_ocr.txt` | 1913 publication | Public domain |
| Registry metadata (Crossref, DataCite, Europe PMC, GitHub API, arXiv API) | `codex-audit/sources/*metadata*`, `claude-audit/results/d_*.json` | Public APIs | Factual metadata |
| Nathan Sweet's own articles | `codex-audit/inputs/sweet.txt`, `codex-audit/sources/primary/sweet_*`, `claude-audit/sources/sweet_*` | sweetrationalism.com | © Nathan Sweet; CC BY 4.0 for this release |

Zhangtaining/cell_research, the original sorting code, has no licence file, so it is not redistributed. Both audits pin it to commit 1fd2bd5921c1f6b423a71f691d5189106a8a1020 and fetch it at run time.
