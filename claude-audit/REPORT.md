# Verification audit: Dietz, "Why Michael Levin Is 77.6++% Right on Platonic Ingress" and Sweet, "Why Michael Levin's Bubble Sort 'Revelation' Is Misunderstood" (rev. 2026-10-31)

Prepared 2026-11-01 for Nathan Sweet. Every number below is produced by a script in `checks/`, written to `results/*.json`, and hashed in `results/SHA256SUMS`. `run_all.sh` rebuilds everything from pinned commits. Provenance labels: P0 observed in this session, P1 verified against a primary source in this session.

## Erratum and second pass (2026-11-01, later the same day)

This report was written before the cross-audit with the Codex bundle. Two items change; the rest stands.

- **Missed: direction of Dietz's nearest-relative result (row D4b).** His article says copying the nearest relative "won by 4%". The outcome record shows the reverse: the full 30-D predictor had 4.12% lower median error than nearest-relative copying (ratio 0.9588), with p = 0.061 against a preregistered alpha of 0.01. I quoted the ratio without flagging the reversal; the Codex audit caught it.
- **Added: Sweet's exploratory C = 2 test on the original threaded code.** `checks/r_upstream_sweet.py` reruns it on held-out inputs (p = 1.2e-7, 3.9e-6 on a rerun of the same inputs, 3.5e-9 on a second input set), with a negative control and a calibration check (`checks/r_conditional_test_calibration.py`). A peak-matched passive-label control for the transient aggregation peak is in the same results.
- **Withdrawn: row S13 (duplicated sentence fragment).** The fragment exists only in the copy of Sweet's article pasted to the audits; the live page and its October 31 capture (`codex-audit/sources/primary/sweet_live.html`) do not contain it.
- **Resolved: the source of Dietz's long quotation of Sweet** (*Religion with a Pipette*, 2026-10-04): verbatim except one change of subject.

The cross-audit article at the repository root (`CROSS_AUDIT.md`) supersedes this report where they differ.

## 1. Bottom line

The arithmetic in both articles is mostly right. The problems sit in what the arithmetic is applied to.

Sweet's computational claims all reproduce exactly (0.6592, 0.503333, 0.485117, 572 against 603.5, exact p = 0.00201, 90/90 equal-key reversals, 105/105 inert continuations, E[A] = 0.4875). All 13 of his DOIs resolve to the cited works. One factual sentence needs rescoping (the code-date sentence, Section 5), and the article has a duplicated sentence fragment.

Dietz's code reproduces its own committed outputs exactly, his inversion-versus-adjacent-descent mathematics is correct, and his Claim 3 endpoint numbers are reproduced by the authors' own threaded code. Against that:

1. His frozen-cell model is the wrong one for the public code. The upstream source implements movable frozen cells. In 30 of 30 runs of the unmodified code, frozen cells were displaced and values crossed them. "No cell walks around the wall" and Lean Theorem 1 describe the immovable condition, which the committed code does not implement.
2. The p = 10⁻¹⁰³ in Claim 4 belongs to the full 30-dimensional phylogenetic predictor, not to Thompson's grids. His own outcome nanopublication says Thompson's 7 modes are about 53% worse than that predictor, and that 4 of 7 hypotheses were supported. The article mentions one of the three failures.
3. The "93.5% alignment" for Thompson's grids is reached by 16.5% of random 8-dimensional projections of the same data. As presented it does not single out Thompson's grids.
4. Six of his DOIs resolve to unrelated papers, including both landmark datasets that his "17-dot head seesaw" argument rests on.
5. The validator behind "14/14 benchmarks replicate 100%" hard-codes `"status": "VERIFIED"`, so it cannot report a failure. The "bit-for-bit identical against upstream" claim cannot be literal, because the upstream code is nondeterministic.
6. The Lean files compile with no `sorry` and only standard axioms. Most theorems, though, are statements about single concrete lists or hard-coded integers, so they do not prove the scientific claims the article attaches to them.

The 77.6% averages three different kinds of quantity: fidelity of Levin's sentences to code, adequacy of Dietz's own reduced models, and a new fish result that is not a claim Levin makes. A number built that way has no defined measurand, so it cannot be read as "how right Levin is".

## 2. What to check against, and why (ranked)

Tribunal order. Primary artifacts first (paper text, code at a pinned commit, the record of the preregistration). Then exact mathematics. Then reproduction (same code, same data). Then replication (independent code, same question). Then interpretation. A higher tier can overturn a lower tier. The reverse never holds.

| Need | Most authoritative source or tool | Why it matters here |
|---|---|---|
| What the paper claims and measures | Zhang, Goldstein & Levin, arXiv:2401.05375 (text checked), *Adaptive Behavior* 33(1):25–54, doi:10.1177/10597123241269740 (online 2024-08-19) | It defines movable vs immovable frozen cells, Sortedness, DG, and aggregation, and it states the efficiency hypothesis itself |
| What the code does | `Zhangtaining/cell_research` at 1fd2bd5; cell files unchanged since 4a01069 (2023-08-26); `__pycache__` bytecode read via PEP 552 header layout and `xdis` | The only ground truth for the "no added code" sentence; the bytecode exposes an earlier version |
| What Levin claims | Ingressing Minds, PsyArXiv v3 doi:10.31234/osf.io/5g2xj_v3 (quotes checked by string match); Philosophies 11(5):161 (blocked from sandbox) | Scope of each scored "claim" |
| Inversions and stability | Knuth, TAOCP Vol. 3 §5.1.1 (inversions), §5.2; Cormen et al. (stability); Franceschini 2007, doi:10.1007/s00224-006-1311-1 | Exact facts behind Claim 2 and the stability argument |
| Null for adjacency aggregation | Wald & Wolfowitz 1940 runs test, doi:10.1214/aoms/1177731909 (A = (N − R)/N); exact enumeration | Gives the 0.4875 benchmark as a classical result rather than a bespoke one |
| Composite scores | OECD/JRC *Handbook on Constructing Composite Indicators* 2008, doi:10.1787/9789264043466-en; Cronbach & Meehl 1955, doi:10.1037/h0040957; Messick 1995, doi:10.1037/0003-066X.50.9.741 | The 77.6% needs a defined construct, a weighting rationale, and a sensitivity analysis |
| Preregistration and severity | Nosek et al. 2018, doi:10.1073/pnas.1708274114; Mayo 2018, doi:10.1017/9781107286184; Simmons et al. 2011, doi:10.1177/0956797611417632; ASA statement, doi:10.1080/00031305.2016.1154108 | Beating a constant baseline is not a severe test; tiny p-values carry no effect-size information |
| Comparative morphometrics | Rohlf & Slice 1990, doi:10.2307/2992207; Schluter 1996, doi:10.1111/j.1558-5646.1996.tb03563.x; Felsenstein 1985, doi:10.1086/284325; Uyeda et al. 2018, doi:10.1093/sysbio/syy031; Stone 1997, doi:10.1016/S0025-5564(96)00186-1 | g_max/r_max alignment, phylogenetic non-independence, prior empirical tests of Thompson grids |
| Reproducibility standards | NASEM 2019, doi:10.17226/25303 (reproducibility vs replicability); Peng 2011, doi:10.1126/science.1213847; Sandve et al. 2013, doi:10.1371/journal.pcbi.1003285; Collberg & Proebsting 2016, doi:10.1145/2812803; Ivie & Thain 2018, doi:10.1145/3186266; FAIR, doi:10.1038/sdata.2016.18 | Three ports agreeing with each other is reproduction of one model, not replication of the original |
| Formal proof | Lean 4 (de Moura & Ullrich 2021, doi:10.1007/978-3-030-79876-5_37), `#print axioms`; Fetzer 1988, doi:10.1145/48529.48530 | "0 sorry" certifies the proof. Whether the theorem states the claim is a separate question |
| Provenance records | Trusty URIs (Kuhn & Dumontier 2014, doi:10.1007/978-3-319-07443-6_27); nanopublications (Kuhn et al. 2016, doi:10.7717/peerj-cs.78) | A trusty URI fixes the content. It does not prove when the content was written relative to data access |
| Citation integrity | DOI content negotiation (doi.org, CSL-JSON) for Crossref and DataCite; Walters & Wilder 2023, doi:10.1038/s41598-023-41032-5 (documents DOI errors as a known class in AI-assisted drafting) | Six mismatches found in one article |

All 24 methodological DOIs above were resolved by `checks/d_method_refs.py`.

Constraints that matter most:

- Pin every artifact by commit hash and record the tool versions. This run used Python 3.13, numpy 2.5.3, sympy 1.14, xdis 6.3, Node 22.23, and Lean 4.35.0.
- Separate deterministic checks (exact) from stochastic ones (threads), and report the stochastic ones as distributions.
- Compute pass/fail from a stated tolerance in the code. Never write it in by hand.
- Test the model the paper actually ran: movable and immovable frozen cells are different experiments.
- Hold a theorem to its statement, not its docstring.
- Compare every predictor with its strongest cheap rival (nearest relative, random subspace), not only with a constant.

## 3. Ledger: Dietz

| ID | Claim (Dietz) | Verdict | Evidence |
|---|---|---|---|
| D1a | Insertion relies on a 3-line FREEZE reset (InsertionSortCell.py L68–82) | EXACT. Line 74 of the committed file; the cpython-311 bytecode (source mtime 2023-06-04, same size) also checks FREEZE inside is_enable_to_move | f_code_forensics.json |
| D1b | Removing it raises final error 4.90 → 21.95 (n = 60, f = 3) | REPRODUCED from his code, but both arms use immovable frozen cells and the ablated arm uses a different scheduler. Under the upstream movable semantics the effect survives: 2.4 → 19.35 | dietz_ablation_rerun.json; r_upstream.json R2 |
| D1c | Bubble only declines swaps with frozen cells ("brick wall"); Selection's FREEZE branch only nudges the pointer | FALSE for the committed source. `should_move_to` in Bubble and Insertion accepts FREEZE targets, `swap()` blocks only a frozen initiator, and Selection swaps into a frozen target when its value is smaller. In 30/30 runs a frozen cell moved | f_code_forensics.json F1; r_upstream.json R1 |
| D1d | "Formally proved in Lean 4 Theorem 2" | OVERSTATED. Theorem 2 evaluates two fixed 4-element lists by `decide` and says nothing about final error | Loop_zhang_sorting_morphogenesis.lean |
| D2a | [2,4,1,3] → [2,1,4,3]: I 3 → 2, E 1 → 2 | EXACT | M1; Lean `ruler_witness` |
| D2b | Every adjacent swap lowers I by exactly 1 | TRUE in general. Our Lean proof covers every list and every position. Dietz's Lean covers one 3-element window. Among strictly downhill adjacent swaps, E rises in 11.8% (n ≤ 8, exhaustive) | M2, M2b; lean/AdjacentSwap.lean; Node cross-check |
| D2c | "ΔI = −1 on every single swap"; "never move against their gradient" | TRUE only for adjacent swaps. Non-adjacent swaps change I by an odd amount 1 + 2k. Empirically there were 0 uphill swaps on I in 7,308 swaps of upstream mixed B+S arrays: supported in that test, not proven in general | M3; r_upstream.json R3 |
| D2d | "100% deterministically downhill" | Monotone descent on I holds. Determinism does not: the upstream runs differ trace to trace | r_upstream.json R4 |
| D2e | Freeze a cell and nothing crosses it (Lean Thm 1) | TRUE for immovable cells only. Thm 1 is a single-swap index lemma; the induction is in a comment. FALSE for the public code | R1; Lean file |
| D2f | The paper's ruler is E | TRUE: Sortedness = (N − E)/N in `analysis/utils.py`. The paper's DG argument compares 0–3 frozen cells, which the 4-cell example does not address | zhang.txt; upstream code |
| D3a | Unique keys: aggregation rises then returns to chance; duplicate C = 2 below chance, C = 10 ≈ 0.659 | REPRODUCED in the upstream threaded code: C = 1 final 0.4825, C = 2 0.4625 ± 0.0155, C = 10 0.6675 ± 0.013. Port peak 0.624 is low against upstream 0.674 and the arXiv text 0.72 | r_upstream_agg.json |
| D3b | Critics predict "flat 0.50" | The exact null is 1/2 − 1/N = 0.4875 at N = 80 (runs test). It holds for any sort whose permutation ignores labels, stable or not, so departures refute label-independence, not stability as such | M6, M7, M12 |
| D3c | Kinematic phase separation as the audit's finding | The paper states the efficiency hypothesis and says the duplicate result "suggests" it | zhang.txt (Mixed Algotype section) |
| D4a | p = 10⁻¹⁰³ for "the Thompson predictor" | MISATTRIBUTED. That p is H1, the full 30-D PGLS predictor. Thompson-7 is H6 (p = 7.4e-81), with median error 0.0588 against 0.0383 for full-30 | np_RAJancwG….trig |
| D4b | "The loss is in the same record as the win" | INCOMPLETE. The outcome record reports 4/7 supported (2/4 primary); H2, H4 and H5 failed; the article reports H2 | same |
| D4c | 93.5%–98.9% alignment along Thompson's grids "across 10,303 species" | The numbers are \|cos\| of g_max vs r_max after projection: 0.935 (791 spp.), 0.989 (6,614 spp.). The 10,303-species dataset has only a raw-trait cos of 0.256. A random-subspace null on the 791-species data: median 0.728, and 16.5% of 200 random 8-D subspaces reach ≥ 0.935 (k = 7: 20%) | t_alignment_null.json; thompson_3dataset_validation_summary.json |
| D4d | 57.9% vs 86.2% variance | CONSISTENT: Eckart–Young requires PCA ≥ any 7-D subspace | M10 |
| D4e | "+13% to +48% (15× better)" over 2.4% | UNDEFINED. Over 2.4% these are 6.4×–21× | M10 |
| D4f | Claverie & Wainwright 2014, Evolution 68(12), doi:10.1111/evo.12502; Friedman et al. 2019, Syst Biol 69(1), doi:10.1093/sysbio/syz029 | WRONG. The DOIs resolve to Posavi et al. and Prasanna et al. Correct: PLoS ONE 9(11):e112732 (10.1371/journal.pone.0112732); Proc R Soc B 287:20201053 (10.1098/rspb.2020.1053) | d_references.json |
| D4g | Claim 4 as one of the claims Ingressing Minds makes | SCOPE MISMATCH. Levin cites Thompson's grids as structure with "no known physical basis". He makes no claim about fish macroevolution alignment | ing3.txt |
| D5 | Serotonin z = +1, ratio ≈ 4.7 across 40 mV, conductance cancels at equilibrium | CORRECT: 4.74 at 25 °C (4.87 at 20 °C, 4.47 at 37 °C) | M8 |
| D6 | Pinet et al. doi:10.1242/dev.175950; Vandenberg inline doi:10.1016/j.ydbio.2012.01.027; Pezzulo inline doi:10.1098/rsif.2015.0772; Pietak BETSE doi:10.3389/fphys.2016.00178 | WRONG. Correct: 10.1242/dev.175893; 10.1002/dvdy.23770; 10.1039/c5ib00221d; Front Bioeng Biotechnol 4:55, 10.3389/fbioe.2016.00055 | d_references.json |
| D7 | Xenobots: sphere 1 generation, C-shape 3–4 | APPROXIMATE. Paper: spheroids 1.2 ± 0.4 (max 2), semitoroids 3 ± 0.8 (max 4). The 105° angle and "flat slab manages none" are his model outputs | kriegman2021 (PMC8670470) |
| D8a | Score arithmetic 77.6, 65.7, 88.1 | EXACT | M9 |
| D8b | Superseded pillar mean 81.6 | 81.68 → 81.7 from the exact cards; 81.6 needs Thompson written as 96.0 (it is 96.1 elsewhere) | M9 |
| D8c | Validity of the 77.6% | NO DEFINED CONSTRUCT. Claims 5–7 grade his reduced models ("gaps in our reduced equations"). Claim 4 grades a result Levin did not claim. 85% of the sorting deductions are the "dualist" deductions (3.7, 7.4, 1.5 points). No weighting rationale or sensitivity analysis is given | M9; article text |
| D9 | Four-language ports bit-for-bit identical "against the upstream commit"; "all 14 curves replicate 100%" | The 0 mismatches are among his three ports sharing SplitMix64. Upstream is nondeterministic. The validator hard-codes VERIFIED. Most of his benchmarks land within 4%; Bubble DG f = 3 is +32% and B(dec)+S(inc) is +12% | R4; validate_kymograph_and_paper.py; results_joel_validator.log |
| D10 | 0 sorry, kernel-checked | TRUE (Lean 4.35.0; propext, Quot.sound only). Thm 6 subtracts hard-coded integers and verifies nothing about CE 2.0 | lean run |
| D11 | Huh et al. hypothesize convergence toward Plato's ideal reality "because Platonism is basically correct" | The quoted phrase is EXACT. The "because" clause is Dietz's gloss, not in the source | arXiv abstract |

## 4. Ledger: Sweet

| ID | Claim (Sweet) | Verdict | Evidence |
|---|---|---|---|
| S1 | [2a, 2b, 1c] long swap reverses equal keys | EXACT | M5 |
| S2 | 90/90 duplicate runs reverse some equal-key pair | EXACT | n_replay_bfe377c.json |
| S3 | 105/105 continuations from the final state make no swaps | EXACT | same |
| S4 | C = 10 final 0.6592; stable benchmark 0.503333; within-block conditional 0.485117 | EXACT | same |
| S5 | E[A] = [b(b−1)+s(s−1)]/N², 0.4875 at 40/40; other denominators differ | EXACT (symbolic, exhaustive Python + independent Node). Alternatives: 0.4937 for N − 1, 0.49375 for coin-flip labels | M6, Node |
| S6 | C = 2: observed 572 vs conditional 603.5; exact two-sided p ≈ 0.00201; simulation 0.00208 | EXACT: 0.0020067. Our seeded 100k simulation gives 0.00183; the gap is about 1.8 Monte Carlo SE. Exploratory, as Sweet says | same |
| S7 | Every strict adjacent inversion swap lowers I by one (checked through 8 keys) | TRUE, now proved for all lengths | Lean AdjacentSwap |
| S8 | Upstream Insertion admits movement with prefix [3, frozen 1]; removing the branch blocks it | EXACT | u_isolated_prefix.json |
| S9 | "The inspected code version postdates the paper's first online publication" | TRUE of the commit (2024-10-30 vs online 2024-08-19), MISLEADING about the file. InsertionSortCell.py is byte-unchanged since 2023-08-26, and the bytecode header implies the same contents by 2023-06-04. An older version without the prefix gate, and with immovable frozen cells, also ships as bytecode. The open question is which version produced which figure | f_code_forensics.json |
| S10 | Quotes from the Lex Fridman transcript ("neither prescribed nor forbidden", "free compute ... physical costs") and from the paper (Section 4.4 "not something that can be predicted a priori") | EXACT | lex transcript; zhang.txt |
| S11 | Landauer kT ln 2; Bennett; logically reversible swaps | CORRECT | M11 |
| S12 | 13 DOIs | 13/13 resolve to the cited works | d_references.json |
| S13 | Text: "Repetition does not supply the additional designer's missing evidence.petition does not supply the additional designer's missing evidence." | WITHDRAWN: present only in the copy pasted to the audits, not on the live page (see Erratum) | article |
| S14 | "Reynolds showed with the Boids model that patterns ... can be extremely sensitive to initial conditions" | NOT CHECKED in this audit. Cite the specific Reynolds result or scope the sentence | none |

## 5. Corrections and additions this licenses for Sweet's article

1. **Rescope the code-date sentence (S9).** The file containing the FREEZE reset is unchanged since August 2023 and is probably older. What remains open is that the repository also ships bytecode of an earlier Insertion cell with no prefix gate and immovable frozen cells. So the public artifacts do not settle which version generated the published figures.
2. **Add the frozen-cell semantics objection.** Dietz's "no cell walks around the wall" and his Lean Theorem 1 assume immovable cells. The committed code moves frozen cells (30/30 runs). The paper itself ran both conditions. This is a stronger and cleaner objection to the Claim 2 reasoning than any point currently in the article, and it leaves the I-versus-E mathematics, which is correct, untouched.
3. **Sharpen the benchmark paragraph (M7, M12).** The 0.4875 endpoint is the runs-test null, and it holds for any label-independent permutation, stable or not. Departing from it refutes label-independent movement. It does not test stability as such. That fits the article's own conclusion that rejecting the old mechanism does not select a new one.
4. **Strengthen the warning about the headline percentage.** It is not a calibrated probability, and it has no defined construct (OECD/JRC; Cronbach & Meehl). Its largest component, Claim 4 at 96.1%, rests on a p-value that belongs to a different predictor and on a record with 3 of 7 hypotheses failed.
5. **Fix S13**, and scope or source S14.

Nothing here revives the withdrawn stability explanation, and nothing bears on the further causal claim either way.

## 6. What could not be checked

- The *Philosophies* final text (MDPI returned 403); quotes were checked against PsyArXiv v3. The *Adaptive Behavior* final text (paywall); arXiv text was used.
- Dietz's fish analyses beyond the 791-species alignment null (the 6,614 and 10,303 pipelines were not rerun); the 40.6% → 56.2% silhouette, box-stretch, TPS-folding and hornet-wing numbers; his PDE, Stokeslet and xenobot simulations.
- Whether the preregistration preceded data access (self-declared dates only).
- Levin's X post; the referee model identities and logs; the authorship heatmap.

## 7. How to distribute results so they are machine-checkable and persuasive

1. Publish this bundle as a versioned repository with a Zenodo DOI, and archive the exact upstream commits in Software Heritage (SWHID) so the pins survive repository deletion.
2. Make `run_all.sh` the single entry point, and run it in CI (for example a GitHub Actions badge) inside a pinned container (Dockerfile with a digest). Exact checks then fail loudly, and stochastic checks report means with SE against stated tolerances.
3. Ship `claims_ledger.json`: each claim, its source quotation, its verdict, the script, and the SHA-256 of the result file. Readers can diff verdicts across versions, as Dietz's errata log intends, but with computed statuses.
4. Keep reproduction (same code), replication (independent code), and formal proof (theorem statement shown next to the prose claim) in separate columns, using the NASEM terms.
5. For any composite score, publish the weights, the per-item measurand, and a sensitivity table over reasonable weightings.
6. For preregistrations, deposit to a timestamping registry (OSF or AsPredicted) or the nanopub server network, whose server-side time proves precedence. Name the strongest cheap rival as the primary comparison.
7. Human readers trust a short table of claim, test and result with links to one-command reproduction. This report's Sections 3 and 4 are written for that use.
