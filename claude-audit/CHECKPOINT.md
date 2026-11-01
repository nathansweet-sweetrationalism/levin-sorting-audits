# Audit checkpoint log: Dietz "77.6++%" vs Sweet "Bubble Sort" (Oct 31 2026 rev.)

Session start 2026-11-01. Each checkpoint lists what is verified (P0/P1), what is pending, and how to resume.

## Checkpoint 1 (upstream code forensics)

Sources pinned:
- Zhangtaining/cell_research HEAD 1fd2bd5 (2024-10-30). Cell files (Bubble/Insertion/Selection/MultiThreadCell) last changed in commit 4a01069, 2023-08-26 (git log -- path). Later commits touch only an analysis script.
- fractastical/morpholib HEAD 35d30f4 (2026-10-31).
- arXiv:2401.05375 PDF (Zhang, Goldstein, Levin), saved as sources/zhang2024_arxiv.pdf.

Findings (P0, direct inspection):
F1. Upstream frozen cells are MOVABLE in the committed .py source: MultiThreadCell.swap only returns early when the *initiator* is FREEZE (the target-FREEZE clause is commented out); BubbleSortCell.should_move_to and InsertionSortCell.should_move_to explicitly accept a FREEZE target. SelectionSortCell.should_move_to calls self.swap(target) on a FREEZE target when value < target.value (comment says "to count attempts" but the swap executes).
  -> Dietz's "frozen cell is a brick wall" / "decline a swap with a frozen neighbor" description of BubbleSortCell.py is false for the committed source. It matches the paper's *immovable* condition, which the committed source does not implement.
F2. The repo ships two bytecode generations in __pycache__. cpython-310 .pyc headers record source mtimes Mar 2023 and source sizes that DIFFER from the committed files; cpython-311 .pyc record Jun 2023 mtimes and sizes that MATCH the committed files.
  - 310 MultiThreadCell.swap: returns if initiator OR target is FREEZE (immovable frozen cells).
  - 310 InsertionSortCell: no is_enable_to_move method at all (no prefix gate, no FREEZE reset).
  - 311 = committed source: prefix gate with FREEZE reset (line 74), movable frozen cells.
  -> The FREEZE reset existed by ~2023-06-04 (source mtime in pyc header), i.e. before arXiv v1 (Jan 2024). Which version produced each published figure is still undetermined from public artifacts.
F3. Neither source nor either bytecode generation calls update() inside swap(). morpholib's port docstring says swap() resets the Selection target via update(); not supported by upstream code (update() is only called from CellGroup.merge_with_group).
F4. Metric definitions in upstream code: Sortedness = (N - E)/N with E = adjacent descents (utils.get_monotonicity). Aggregation (Fig 8 plotting code) = (# i with type[i]==type[i+1]) / N, i.e. A = H/N. The paper's prose definition ("cells whose adjacent neighbours were all the same Algotype") does not match that code.
F5. The paper itself states the efficiency hypothesis for clustering and says the duplicate-value result "suggests that the efficiency hypothesis can be the explanation" (arXiv text, Mixed Algotype section). Dietz's "kinematic phase separation" is that hypothesis, not a new finding.
F6. Paper's Delayed Gratification argument is comparative across 0-3 frozen cells (context sensitivity), not the existence of a dip alone.

Pending: exact math, replication runs, Lean audit, DOI audit, claims 4-7, packaging.

## Checkpoint 2 (exact math + Lean)

checks/m_exact_math.py (Python, exact Fractions + sympy + exhaustive enumeration) and checks/m_crosscheck.mjs (independent Node.js, BigInt) all pass.
- M1/M2: [2,4,1,3] example correct; every adjacent strict-inversion swap has dI = -1 (158,323 swaps, n<=8; Node count identical). Among those downhill swaps E rises in 11.8%.
- M3: non-adjacent swaps change I by an odd amount 1+2k; so "dI = -1 on every single swap" (Dietz Claim 2 verdict) is true only for adjacent swaps; Selection swaps can drop I by more, and a non-inverted swap raises I.
- M6: E[H/N] = [b(b-1)+s(s-1)]/N^2 = 1/2 - 1/N for equal counts. N=80: 0.4875 (Sweet correct); N=100: 0.49. Dietz's "0.50" baseline is the rounded value.
- M7 (new): the endpoint chance benchmark holds for ANY sort whose permutation ignores labels, stable or not. A departure falsifies label-independence of movement; it does not test stability per se.
- M8: Boltzmann factor for z=+1 over 40 mV = 4.74 at 25 C (4.87 at 20 C, 4.47 at 37 C). Dietz's ~4.7 holds at room temperature.
- M9: 77.6, 65.7, 88.1 reproduce. Superseded pillar mean is 81.68 (81.7) from exact cards; 81.6 only appears from rounded inputs with Thompson as 96.0 vs 96.1 elsewhere. Implied dualist deductions: 3.7, 7.4, 1.5 points = 85% of all sorting deductions.
- M10: 57.9% <= 86.2% is forced by Eckart-Young (PCA optimal). "+13 to +48%" over 2.4% is 6.4x-21x; "15x" has no stated base.
Lean: morpholib Loop_zhang_sorting_morphogenesis.lean compiles on Lean 4.35.0, 0 sorry, only standard axioms. But: Thm 1 is a single-swap index lemma for IMMOVABLE barriers (upstream has movable); Thm 2 is two concrete list evaluations by decide, it does not prove the 4.90 -> 21.95 ablation the article attributes to it; Thm 3 is one concrete list; Thm 4 a 3-window; Thm 6 is subtraction of hard-coded integers, verifies nothing about CE 2.0. "Formally checked" here certifies arithmetic, not the scientific claims (specification gap).
Our lean/AdjacentSwap.lean proves the general adjacent-swap theorem for all lists/positions (propext, Quot.sound only).

## Checkpoint 3 (replications, partial)

- Dietz's own audit script (HEAD 35d30f4) reproduces his committed JSON exactly (4.90 -> 21.95; 192 swaps / 47 E-uphill / 0 I-uphill; 0.624 -> 0.501). Computational reproducibility: PASS.
  But design: both Insertion arms use IMMOVABLE frozen cells (upstream implements movable), and the ablated arm uses a different hand-written scheduler loop, so the 4.5x contrast changes more than the three lines. The 0/192 and 47 are one trajectory (n=40, one seed).
  Port deviations from upstream: scheduler picks only active cells; Selection target reset on every swap (selection_reset_on_swap=True), which upstream code does not do.
- Sweet's Oct 31 numbers, replayed at bfe377c (checks/n_replay_bfe377c.py): ALL reproduce. C=10 final 0.6592; stable benchmark 0.503333; within-block conditional mean 0.485117; C=2 observed H 572 vs conditional 603.5; exact two-sided tail p = 0.0020067; 90/90 duplicate runs reverse some equal-key pair; 105/105 continuations make zero swaps. Our seeded 100k Monte Carlo gives 0.00183 (Sweet 0.00208; difference ~1.8 MC standard errors).
- Upstream threaded code R1: in 30/30 Bubble runs with frozen cells, a frozen cell was displaced and values crossed the initial frozen index. The "brick wall" premise of Dietz Claim 2 / Lean Thm 1 is false for the public code.

## Checkpoint 4 (references, primary-source quotes, preregistration record)

DOI audit (checks/d_references.py, doi.org CSL-JSON): all 13 DOIs in Sweet's article resolve to the cited works. In Dietz's article 6 DOIs resolve to DIFFERENT papers:
- 10.1111/evo.12502 -> Posavi et al. (salinity dominance), not Claverie & Wainwright 2014. Correct: PLoS ONE 9(11):e112732, doi:10.1371/journal.pone.0112732 (journal, volume also wrong).
- 10.1093/sysbio/syz029 -> Prasanna et al. (phylogenomics), not Friedman et al. Correct: Proc R Soc B 287:20201053 (2020), doi:10.1098/rspb.2020.1053.
- 10.3389/fphys.2016.00178 -> Kovach et al., not Pietak & Levin BETSE. Correct: Front Bioeng Biotechnol 4:55, doi:10.3389/fbioe.2016.00055.
- 10.1242/dev.175950 -> Ruthig et al. (DND1), not Pinet et al. Correct: doi:10.1242/dev.175893.
- inline 10.1016/j.ydbio.2012.01.027 -> Turlo et al. (integrin), not Vandenberg 2012 (reference list DOI 10.1002/dvdy.23770 is correct).
- inline 10.1098/rsif.2015.0772 -> Lin et al. (bursting noise), not Pezzulo & Levin 2015 (reference list DOI 10.1039/c5ib00221d is correct).
Two of these are the landmark datasets behind Claim 4's "17-dot head seesaw".

Ingressing Minds (PsyArXiv v3, 2025-02-07, 53 pp.): quote "The critical thing is that we did not add steps to the algorithm to check whether a swap had been completed, or to do specific things if an operation failed." EXACT. "side-quests – not incompatible with, but not predicted, explained, or produced, by that medium" EXACT. Thompson appears only as: coordinate-grid transformations exist; such fields "do not have a known physical basis but they do have structure and information content". No claim about fish macroevolution alignment. MDPI final version blocked (403) from the sandbox; page numbers for the Philosophies version unverified.

Preregistration nanopubs (fetched .trig): outcome record = "4/7 hypotheses supported (2/4 primary), 5180 species".
- p = 1.05e-103 is H1: the FULL 30-D phylogenetic (PGLS) predictor vs grand consensus. It is NOT the Thompson predictor. Thompson-7 vs consensus is H6, p = 7.4e-81, and Thompson-7 median error 0.0588 is 53% worse than full-30 (0.0383).
- H2 (full-30 beats nearest relative) failed: ratio 0.959, p = 0.061. H4 and H5 also failed; the article mentions only H2.
- So the article attributes the full-shape-space win to Thompson's grid and reports 1 of 3 failures. Claim 4's 96.1% does not follow from its own record.
- Prereg and outcome both dated 2026-10-22 (self-declared dcterms:created). Trusty URIs fix content, not timing relative to data access.

## Checkpoint 5 (upstream replications R1-R4; port audit)

Upstream threaded code, unmodified (checks/upstream_driver.py + r_upstream.py; results/r_upstream.json):
- R1 (n=60 Bubble, 1-3 frozen, 30 runs): frozen cells displaced in 30/30 runs; values crossed the initial frozen index in 30/30. Every Bubble swap dI = -1. Final E by f: 0, 0.5, 0.9.
- R2 Insertion ablation under upstream MOVABLE semantics (n=60, 20 runs each): with reset 0.95 / 1.7 / 2.4; strict (3 lines removed) 11.15 / 17.35 / 19.35. The qualitative Claim-1 finding (Insertion's tolerance depends on the FREEZE-aware prefix rule) is ROBUST to the semantics error; Dietz's specific 4.90 -> 21.95 is a property of his immovable port.
- R3 Mixed 30B/30S, 10 runs, 7,308 swaps: 0 swaps raised I. The empirical "no uphill on I" claim survives in upstream mixed arrays (not proven in general; M3 shows a non-inverted long swap would raise I).
- R4 Same input, same seed, 3 runs: traces differ (equal length 416 = initial inversions). Upstream is nondeterministic, so "bit-for-bit identical kymographs against the upstream commit" cannot be literal; the 0-mismatch result is among Dietz's three ports of one reimplementation sharing a SplitMix64 stream.
Port/validator audit:
- validate_kymograph_and_paper.py hard-codes "status": "VERIFIED" for all 14 benchmarks; the validator cannot return a failure. "14/14 replicate 100%" is therefore not a test result.
- Several validator "published_value"s differ from the arXiv text (e.g. immovable Selection f=3 3.00 vs 2.91; B+S chimeric peak 0.645 vs text 0.72; duplicate B+S final 0.690 vs text 0.65). Journal version not checked (paywall).
- Movable-frozen benchmarks (paper Fig 5B: Selection f=3 13.24, Bubble 2.64) are not among the 14; port gives 3.0 and 1.13.
- Port uses selection_reset_on_swap=True for one benchmark family and False for another; upstream has neither behaviour in swap().

## Checkpoint 6 (Claim 3 upstream, Claim 4 alignment null, quotes, Kriegman)

- Upstream aggregation (r_upstream_agg.py, n=80 40B/40S, 15 runs each): C=1 final 0.4825 (null 0.4875), peak 0.674; C=2 final 0.4625 +/- 0.0155 (below null, ~1.6 SE); C=10 final 0.6675 +/- 0.013. Dietz's Claim-3 endpoint numbers (0.477, 0.659) are reproduced by the upstream code itself; his port's transient peak (0.624) is lower than upstream (0.674) and the arXiv text (0.72).
- Dietz's validator, run: 12/14 within ~4% of his chosen published values; Bubble DG f=3 0.49 vs 0.37 (+32%) and B(dec)+S(inc) 47.6 vs 42.5 (+12%) still printed VERIFIED.
- Claim 4 "93.5% alignment" = |cos| between leading within-genus and between-genus eigenvectors after projecting onto Thompson grids (raw 34-D: 0.429, reproduced exactly). Null (t_alignment_null.py): PCA-8 subspace 0.427; RANDOM 8-D subspaces median 0.728, and 16.5% of 200 random 8-D subspaces reach >= 0.935 (k=7: 20%; k=4: 30%). Low-dimensional projection alone produces Thompson-level alignment about 1 time in 6, so the 0.935 is not evidence for Thompson's grids specifically. The 10,303-species dataset (11 traits, no landmarks) has only a raw cos (0.256); the 93.5-98.9 figures come from the 791- and 6,614-species datasets.
- Quotes verified exact: Levin (PsyArXiv v3) "did not add steps..." and "side-quests"; Lex transcript "neither prescribed nor forbidden by the algorithm" (02:18-02:19) and "free compute ... don't require you to pay physical costs"; Huh et al. abstract "a shared statistical model of reality, akin to Plato's concept of an ideal reality" (the gloss "because Platonism is basically correct" is Dietz's); Jiang et al. 26K queries, inter-model homogeneity.
- Kriegman 2021 (PMC8670470): spheroids 1.2 +/- 0.4 rounds (max 2), semitoroid 3 +/- 0.8 (max 4). "A sphere manages one" understates the max; "105 deg" and "flat slab none" are Dietz-model outputs, not in the paper.

## Checkpoint 7 (final verification)

Independent rerun of run_all.sh in a fresh directory (/home/claude/verify/rerun): all 7 deterministic result files byte-identical after key-sorted JSON normalisation (m_exact_math, m_crosscheck_node, n_replay_bfe377c, t_alignment_null, f_code_forensics, u_isolated_prefix, dietz_ablation_rerun). Lean files recheck with the same axiom sets. DOI audit identical. Stochastic upstream runs: R1/R2 summary values identical; R3 7,238 swaps, 0 uphill; aggregation C=2 0.4583 +/- 0.0166, C=10 0.6758 +/- 0.0127 (first run 0.4625, 0.6675): consistent within SE.
Deliverables: REPORT.md, claims_ledger.json (43 rows, SHA-256 per result file), run_all.sh, results/SHA256SUMS.

## Checkpoint 8 (second pass: cross-audit with the Codex bundle; Sweet's tests on the original threaded code)

New scripts: checks/r_upstream_sweet.py (identity-tracking wrapper around the unmodified swap()), checks/r_conditional_test_calibration.py.
- Original threaded code, n=80, 40B/40S, 15 runs per batch, all sorted, all ended by 1.5 s with zero swaps:
  C=10 final A 0.690 (SE 0.009); within-block conditional mean 0.481; passive-label endpoint 0.486; 15/15 equal-key reversals.
  C=2 batch A (seeds 7000): H 545 vs 601.0, exact p 1.2e-7; same inputs rerun 552 vs 601.0, p 3.9e-6; batch B (seeds 8000): 499 vs 562.5, p 3.5e-9. 15/15 reversals each.
  Negative control (passive labels, same trajectories): p 0.013 (batch A), 0.27 (batch B). Calibration of the test under its null, 300 draws: P(p<=0.05)=0.053, P(p<=0.013)=0.020.
  Transient peak vs matched passive-label peak on the same trajectory: C=1 0.658 vs 0.604 (excess 0.054, 13/15 positive); C=2 excess 0.049 (12/15); C=10 excess 0.088 (14/15).
- Source of Dietz's long quotation of Sweet located: sweetrationalism.com "Religion with a Pipette" (published 2026-10-04, modified 2026-10-07). Word-level diff: identical except "Joel Dietz's 2025 Radical Platonism and Radical Empiricism points" -> "Joel Dietz points"; quotation stops before "Symmetry cuts both ways..." (Codex had marked this quotation unmatched.)
- Codex-only findings adopted after reading their report: H2 direction reversed in Dietz's text (full-30 had 4.12% LOWER error than nearest relative; p 0.061 failed alpha 0.01); [2, frozen 1, 0] dead end under immovable defects; 3.3-9.3x are loading ratios not rates; 105 deg not reproduced by pinned script (65 deg); upstream reverse-direction Insertion reset uses -1; nanopub signatures valid via direct RSA. My earlier report recorded H2's ratio 0.959 without flagging the reversal.
