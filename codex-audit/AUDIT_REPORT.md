# Mathematical and source audit: Dietz, Sweet and the Levin sorting debate

November 1, 2026. Primary targets: the two supplied article versions, preserved verbatim in `inputs/`. Conclusions concern those versions and the explicitly identified code, data and source boundaries.

**The central numerical checks in Nathan Sweet's revised response reproduce. Joel Dietz's project contains genuine reproducible findings and valid formal lemmas, but several major statements need correction.** The clearest problems are four DOI-to-paper mismatches; reversal of the nearest-relative comparison; attribution of a full-30-dimensional predictor's p-value to a seven-mode predictor; fourteen hard-coded benchmark verdicts; missing public biological fixtures; and transfer from limited mathematical results to stronger implementation, biological or ontological conclusions.

These findings do not erase the observed clustering or the underlying laboratory experiments. The audit also verifies substantial strengths: the historical sorting replay, the raw FishShapes observations and calibration, 92 Lean declarations, and the five nanopublications' cryptographic integrity. A failed stability explanation does not identify a Platonic cause. A successful computational model does not establish its universal absence.

No procedure can guarantee acceptance by every reviewer. The appropriate deliverable is evidence that can be inspected, rerun, challenged and corrected. This package supplies that evidence, with explicit unresolved items rather than a blanket certification.

## 1. Scope, versions and evidence levels

The work includes both pasted texts; 41 unique cited DOI identities; 37 explicit pasted URL strings; 135 curly-quoted phrase candidates; primary papers and public correspondence; two Dietz source versions; the original sorting source; 105 historical replay runs; 120 fresh surrogate sensitivity runs; exact combinatorial counting; independent finite-state causal calculations; source-method perturbations; five Lean files; biological self-test attempts; raw FishShapes specimens; prediction locks; all 5,180 scored fish observations and errors; and re-estimation of measurement calibration.

`Supported` means the stated conditional claim survives its indicated check. `Reproduced` identifies exactly which code and data were rerun. `Verified source` concerns words, identity or metadata. `Contradicted`, `overstated`, `unreproduced`, `untested proposal` and `unverified` remain distinct. Lack of access is not falsehood. A source's self-description, a generated referee score and an archived result are evidence of different kinds.

| Object | Frozen boundary |
|---|---|
| Supplied articles | Attachment bytes; SHA-256 in `results/input_hashes.json` |
| Current Dietz repository | `fractastical/morpholib@35d30f4cfd5397ee1ed769f96494e018603e293d` |
| Historical model cited by Sweet | `bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e` |
| Original sorting source | `Zhangtaining/cell_research@1fd2bd5921c1f6b423a71f691d5189106a8a1020` |
| Formal checker | Lean 4.35.0; official release digest checked |
| Fish measurements | FishShapes v1, Zenodo 6642650; CSV MD5 `122b495274d0167c5447db104c7acbfe` |

The original sorting paper appeared online on August 19, 2024. The inspected original-source commit is dated October 30, 2024. Later source code does not establish which exact bytes generated the published data. Sweet explicitly recognizes this limit; it also limits Dietz's historical inference about defect handling.

The primary Levin publication retrieved for quotation checking contains 53 pages. Manuscript and code versions must be pinned separately. A main-branch link does not freeze the artifact described by a pasted article.

## 2. The most important literature and constraints

Authority is claim-specific. Actual pinned source and executable transitions outrank a general survey for implementation claims. Proof and exact counting outrank a simulation average for a finite identity. Independent intervention data outrank a chosen equation for biological mechanism claims.

| Question | Most useful authority | Constraint supplied |
|---|---|---|
| What was studied? | [Zhang, Goldstein and Levin](https://doi.org/10.1177/10597123241269740), author manuscript and original source | Specify distributed policies, metrics, defect modes, scheduler and stopping rule; textbook Bubble sort is not the complete mixed experiment |
| What does stability mean? | [Franceschini](https://doi.org/10.1007/s00224-006-1311-1), Knuth, relevant Cormen edition | Preserve every equal-key record's relative order globally, rather than merely avoiding direct equal-key swaps |
| What must a simulation disclose? | [MIASE](https://doi.org/10.1371/journal.pcbi.1001122), [ODD update](https://doi.org/10.18564/jasss.4259), [principled simulation modelling](https://doi.org/10.1371/journal.pcbi.1009917) | Initial conditions, state, processes, scheduling, randomness, numerical methods and analysis all belong to the specification |
| How should code and proofs be checked? | [Hypothesis](https://doi.org/10.21105/joss.01891), [Lean 4](https://doi.org/10.1007/978-3-030-79876-5_37), [official proof-validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/) | Adversarial generated cases, exact statements, transitive axioms and semantic correspondence |
| How can results be reproduced? | [Sandve et al.](https://doi.org/10.1371/journal.pcbi.1003285), [FAIR](https://doi.org/10.1038/sdata.2016.18) | Preserve versions, inputs, seeds, intermediate outputs and statement-to-result links |
| What does simulation agreement establish? | [Oreskes, Shrader-Frechette and Belitz](https://doi.org/10.1126/science.263.5147.641) | Partial confirmation under assumptions, with nonunique explanations still possible |
| How should fish shape be assessed? | [Bookstein](https://doi.org/10.1109/34.24792), [Claverie and Wainwright](https://doi.org/10.1371/journal.pone.0112732), [FishShapes](https://doi.org/10.1002/ecy.3829), [Felsenstein](https://doi.org/10.1086/284325), [Roberts et al.](https://doi.org/10.1111/ecog.02881) | Homology, alignment, dimensions, phylogenetic dependence, data overlap and blocked validation |
| What do causal-emergence scores measure? | [Hoel et al. 2013](https://doi.org/10.1073/pnas.1314922110), [Hoel 2026](https://doi.org/10.1016/j.patter.2025.101472), [Eberhardt and Lee](https://doi.org/10.3390/philosophies7020030) | Fix the transition system, intervention distribution, partition, clock and state support |
| Is an additional output physically free? | [Landauer](https://doi.org/10.1147/rd.53.0183), [Bennett](https://doi.org/10.1016/S1355-2198(03)00039-X) | Distinguish computational reuse, incremental measured energy and irreversible information loss |
| How should the audit be distributed? | [RO-Crate](https://doi.org/10.3233/DS-210053), [Workflow Run RO-Crate](https://doi.org/10.1371/journal.pone.0309210), [Kuhn and Dumontier](https://doi.org/10.1109/TKDE.2015.2419657) | Link claims, inputs, code, outputs and provenance; content integrity does not establish scientific truth |

These are a focused reading order. Registry identity verification, available full text, relevant passages read and visually inspected PDF pages are separate access levels. The download and literature-access registers preserve those distinctions. They do not imply every work was read cover to cover. Methodological papers, software papers, experiments, preprints and software archives retain their publication types.

## 3. Sorting mathematics

Let `I(v)` count strict inverted pairs and `E(v)` count adjacent descents. Swapping an adjacent inverted pair changes only that pair's contribution to I: `delta I = -1`. Outside-pair contributions cancel. This remains true for strict swaps with duplicate keys.

Independent enumeration checked 158,323 distinct-key transitions through eight keys, 6,015 duplicate-key adjacent transitions, and 19,956 nonadjacent inversion swaps. For a nonadjacent inversion with endpoint values `a>b`, the reduction in I is

`1 + sum over intermediate x of (1[b <= x < a] + 1[b < x <= a])`.

Thus `[3,2,1] -> [1,2,3]` decreases I by three. Dietz's own archived Selection metrics range from -35 to -1. The repeated equality `delta I=-1 on every swap` must be restricted to adjacent strict inversion swaps.

| Array | I | E |
|---|---:|---:|
| `[2,4,1,3]` | 3 | 1 |
| `[2,1,4,3]` | 2 | 2 |

The checked four-cell example shows that adjacent error can increase without a defect or anticipation. It does not make E an illegitimate observable or dispose of comparative defect results. An always-decreasing potential does not, by itself, settle every behavioral conception of intelligence. Identifying I with physical energy requires a further bridge with units and realization evidence.

A truly immovable cell partitions a line under adjacent-only moves. The general one-step Lean invariant supports a finite-trace induction. The legal move graph matters: `[2, frozen 1, 0]` is blocked under adjacent-only moves despite remaining inversions. The no-defect descent argument cannot be transported to this graph. Movable defects, nonlocal moves and scheduling fairness require separate treatment.

### Stability and chance aggregation

For a linear array, fixed type counts b and s, `N=b+s>=2`, matching edges H, and the actual metric `A=H/N`, uniform random arrangement gives

`E[A] = (b(b-1)+s(s-1))/N^2`.

There are N-1 edges and each matches with probability `(b(b-1)+s(s-1))/(N(N-1))`. Dividing the expected count by N yields the identity. The audit also enumerated 8,188 fixed-count arrangements through length twelve. Balanced N=80 gives exactly `39/80 = 0.4875`.

Using N-1 as denominator, ring closure, or independently sampled labels changes the finite-size result. Under a globally stable sort and labels randomized independently of keys, the expected endpoint stays constant across duplicate multiplicities. Dietz's conditional objection to Sweet's former complete-stability account is therefore legitimate. The finite-size correction does not rescue that former account. It also does not turn Dietz's reconstructed forecast into words Sweet directly published.

Global stability is stronger than refusing direct equal-key swaps. `[2a,2b,1c] -> [1c,2b,2a]` reverses equal records through a nonadjacent swap. Sweet explicitly withdraws the complete account in the supplied revision. A critique must identify its historical target rather than treating it as his surviving explanation.

## 4. Historical replay and fresh sensitivity checks

The historical sequential model cited by Sweet was independently replayed: 80 cells, 40 B and 40 S, fifteen runs at each of seven multiplicities, NumPy seed 42 and the specified per-run seeds. Every initial record, final identity, algotype and Selection target is saved in `results/historical_replay_runs.json`.

The key C=10 quantities reproduce: mixed final aggregation 0.659166667; the stable-sort control 0.503333333; and conditional within-key permutation mean approximately 0.485117. The complete table is in `results/historical_replay_summary.json`.

All ninety duplicate-key runs reverse some equal-key identities. Continuing the actual final cell objects, with existing internal targets and strict rules, produces no further swaps in all 105 runs. These results support the response's distinction between formation, global stability and endpoint persistence. They do not prove that tie handling uniquely causes formation or that a scrambled endpoint will actively repair itself.

For two copies per key, exact independent counting and convolution give total H=572, conditional expectation `1207/2=603.5`, and distance-from-expectation two-sided tail probability `0.002006748976705476`. This null fixes each equal-key block's observed type counts and randomizes internal order. It differs from the unconditional fixed-count reference. The choice is exploratory, as Sweet states. Other definitions of two-sided extremeness define different tests.

Fresh testing followed a saved local protocol written before those new runs: thirty new n=40 inputs and a 2x2 change in scheduler and Selection-target reset, with matched passive-label Bubble controls. All 120 runs sorted without hitting a cap. Mean peak aggregation ranged from 0.6500 to 0.6717; mean excess over the matched control's peak ranged from 0.0117 to 0.0333. The control also takes a maximum, incorporating peak-selection bias. These are descriptive sensitivity results, not externally preregistered confirmation or OS-thread replication.

The domain-law curve in `quantify_emergence_ce2.py` uses constants 0.725 and 1.15. It may be a useful approximation, but its presence is not a derivation showing that transport equations predict every curve a priori.

## 5. Implementation and benchmark fidelity

Fourteen benchmark dictionaries in `validate_kymograph_and_paper.py` contain the literal status `VERIFIED`. The status is not calculated from a tolerance, uncertainty interval, equivalence test or relative error. This is a reporting defect. It does not imply the simulations were never run or that approximate comparisons have no value. It means the label and the all-fourteen assertion are not independent acceptance tests.

The validator uses Selection reset-on-swap enabled for one comparison and disabled for another. The port guide discloses this, which is useful. Matching separate summaries under altered dynamics nevertheless does not establish one exact implementation reproducing the complete paper. Source-linked configurations, raw replicates, uncertainty and predeclared acceptance criteria are needed.

The pinned upstream `MultiThreadCell.swap()` does not call `update()`; `CellGroup.merge_with_group()` does. The default surrogate resets targets on swaps. The primary reverse-direction Insertion branch resets prev to -1, whereas the surrogate changes that to positive infinity. A repair may be sensible, but it changes semantics and must be disclosed.

Primary Bubble code permits a FREEZE cell as a passive swap target. A legal isolated example changes `[2, frozen 1]` to `[frozen 1, 2]`. The wall description therefore needs an immovable-mode restriction. This distinction exists in the underlying study and parts of the port documentation; blanket article wording loses it.

Fresh Python and Node results match all 126 final cells in the three 42-cell cases and agree with archived C++ output. C++ was not recompiled here. The supplied verifier asserts final arrays and C++/Node summary metrics, not every synchronized kymograph state. Final identity is genuine evidence but does not certify trajectory identity or source equivalence. On Windows the Node direct-entry URL guard initially skipped execution silently; a separate path-normalizing wrapper ran the unmodified module. A zero exit status without expected output was not accepted as a completed benchmark.

## 6. What the formal proofs establish

Five files compile with Lean 4.35.0 and report 92 declaration axiom closures without `sorryAx`: seven in the sorting file, 76 in MathOfBiology, and three each in the planarian, tadpole and xenobot files. This is real formal work. Standard axiom dependencies and no-axiom declarations are preserved in the logs.

| Formal statement | Actual scope | Remaining bridge |
|---|---|---|
| Barrier partition | Arbitrary indices under a legal adjacent-swap predicate | Connect that predicate and finite-trace induction to the actual program and defect policy |
| Insertion reset | Concrete prefix examples distinguish two folds | Full defect experiment and source-to-paper version |
| I/E result | Concrete four-element list and a three-element-window theorem | Arbitrary-list proof and correspondence to every move class |
| Selection descent | Three-element window | Arbitrary distance and target/state invariants |
| Segregation example | Explicit eight-element type lists | Dynamics creating the arrangement from random mixtures |
| Causal arithmetic | Supplied scaled integer scores | Correct transition matrix, partitions and derived numerical scores |
| Planarian memory | Threshold outputs for supplied integers | Persistence of coupled tissue state, measured thresholds and perturbation validity |
| Tadpole symmetry | A branch directly returns the target, plus concrete contraction arithmetic | Derive biological target storage and the dynamics that reach it |
| Xenobot generations | Supplied integer capture expression and examples | Repeated generations, hydrodynamics and calibrated tissue mechanism |

Kernel acceptance does not transform an assumption inside a definition into an observed mechanism. A limited theorem is also not an invalid theorem. The repair is a theorem-to-equation-to-code-to-data map.

## 7. FishShapes: a major numerical correction

The raw specimen CSV checksum and both registered prediction-file hashes match their source locks. All 5,180 scored observations and the full30, Thompson7, consensus and nearest-relative errors were independently reconstructed. Calibration coefficients were then re-estimated from the original 791-species landmark dataset and training species in FishShapes; they match to floating-point precision. This last step uses the source GPA and registered proxy definitions, so it is reproducibility evidence, not a replacement independent morphometrics implementation. The complete phylogenetic predictor was not rebuilt from scratch.

For the 1,122 species within the 50-Myr criterion:

| Predictor | Median absolute body-depth / length error |
|---|---:|
| Full 30-dimensional | 0.0383444031 |
| Copy nearest training relative | 0.0399934723 |
| Seven-mode Thompson | 0.0587579992 |
| Consensus | 0.0927060552 |

The full30 predictor has **4.1233% lower**, not higher, median error than the nearest-relative method. Its one-sided Wilcoxon result, `p=0.0606819870`, fails the preregistered alpha 0.01 superiority criterion. Failure to meet that threshold does not mean the rival won by four percent.

The `p=1.0490516938e-103` comparison belongs to full30 versus consensus. Thompson7 versus consensus gives `p=7.3831436387e-81`. Both are the stated species-wise calculations, not dependence-corrected probabilities that an evolutionary law is true. Dietz's text needs to name the actual predictor for each value.

The complete calibrated registered decisions are: H1 pass, H2 fail, H3 pass, H4 fail, H5 fail, H6 pass and H7 pass. H4 concerns the claimed deep-time horizon; H5 concerns the specified monotonic-error rule. A summary that identifies only the nearest-relative miss is incomplete. A failed expectation can sometimes mean better-than-expected performance, but it still must retain its original direction and criterion.

Related species and shared training relatives create dependence. A coarse exploratory sensitivity that averages full30-minus-nearest error within 54 families gives one-sided family-level Wilcoxon `p=0.28056`. This does not fully correct phylogenetic dependence and is not a replacement preregistered test. It demonstrates why the observational unit matters. See `results/fish_independent_audit.json` and `results/morphometrics_calibration_check.json`.

### Shape interpretation, rates and topology

The 93.5-98.9% quantities are cosines in selected representations, not percentages of biological variance explained. Dietz explicitly makes that distinction in the supplied article, which deserves credit. The repository's reported raw 34-coordinate alignment is about 0.429 versus about 0.935 in selected Thompson coordinates. Representation is therefore material. These large-compilation alignment calculations were traced in the manuscript and source but were not rebuilt here from every original shape and tree. The three compilations need a taxon, specimen and source-overlap audit before they count as independent replications.

The claimed 3.3-9.3-times-faster head-evolution factors equal ratios of variance-loading percentages: roughly `47/14.41` and `85.4089/9.21807`. They are dimensionless loading ratios, not rates of evolutionary change per unit time. Rate language requires a time-scaled module-specific phylogenetic model.

A positive Jacobian sampled on a finite grid is useful evidence against folding at those points. It does not prove global bijectivity. For example, `f(x,y)=(exp(x)cos(y), exp(x)sin(y))` has positive determinant everywhere and still repeats points when the y-domain spans more than a turn. Domain, boundary and global-injectivity arguments matter. A comparison with thin-plate splines should also match anatomical correspondence, regularization and topology restrictions, rather than treating unconstrained interpolation as the strongest shape-preserving rival.

Fitting extant fish data and a dated tree does not directly observe 150 million years of trajectories. It does not establish a law of all vertebrates. Useful narrower evidence should survive model-recovery tests, dimension-matched nulls, held-out clades and independent measurement choices before that expansion.

The individual illustration numbers, including the 2.4% fin-tip match, 40.6-to-56.2% silhouette mismatch and six-of-six thin-plate-spline folding outcomes, were traced to their source descriptions but were not independently rebuilt from the digitized image sources here. They are not certified quantitative results of this audit. Fitting and selecting anatomical correspondences, optimization bounds, image masks, comparison denominators and sampling domains must be frozen for that reproduction. Illustrative figure code also contains literal display values; an attractive figure is not an additional experiment.

### The hornet-wing negative test

Raw [PANGAEA wing coordinates](https://doi.org/10.1594/PANGAEA.937651) and the [specimen register](https://doi.org/10.1594/PANGAEA.937635) give 1,030 rows, of which the analysis retains 1,027 wings across 30 matched species and 19 landmarks. Those specimens are not 1,027 independent evolutionary units. Repeating the source GPA/basis analysis reconstructs the saved species means within 3.9e-16. The global seven-mode variance fraction is 0.387760; the later perimeter split yields 0.658212, with interior fraction -0.003748. The reported 65.8% therefore reproduces as this particular representation statistic.

The saved prediction results retain zero of seven original wing hypotheses passed; their error medians, selected Wilcoxon calculations and Brier score 0.448214 were recomputed. Full prediction fitting and every noise/allometry alternative were not independently rebuilt. Reporting the negative test is a genuine methodological strength. The later anatomical partition and repaired phylogeny need fresh held-out confirmation; they cannot retroactively turn the original failed test into a passed prediction or establish a general law. See `results/wing_checks.json`.

## 8. Biological equations and experiments

The planarian, craniofacial and xenobot experiments are substantive empirical results. Their findings must be separated from what Dietz's reduced equations establish. No new laboratory experiments were performed here.

**Planarians.** The zero-flux Nernst ratio is correct under fixed valence, voltages and temperature, positive coupling, and compatible reaction/boundary conditions. At complete blockade, multiplying by zero means the flux equation no longer determines a concentration ratio. Turnover, feedback and timescales also matter. Approximately 4.7 is reasonable under the idealization. The source's stated 25.85-mV thermal voltage corresponds approximately to 300 K rather than its stated 298 K; this small precision issue is not the main mechanism problem. The persistent-editing claim should directly cite [Durant et al. 2017](https://doi.org/10.1016/j.bpj.2017.04.011). No deliberate genetic modification is a more defensible description than an unrestricted claim that no DNA changed anywhere.

The Cervera script explicitly discloses that it is a qualitative analogue built without consulting the paper's full text, and that its constants are the script's. This is useful candor. It prevents treating the script as an exact source-faithful reproduction of that paper's equations or biological mechanism.

**Tadpoles.** A positive-definite quadratic target model yields continuous-time `dV/dt=-eta*||grad V||^2<=0`. That result assumes the target and dynamics. It does not explain how tissue stores or reads the target. Numerical step size, viscoelastic coupling and intervention data are separate checks. For quadratic Hessian H, explicit Euler needs an appropriate step-size bound; continuous dissipation does not certify the discretization. The [2012 experiment](https://doi.org/10.1002/dvdy.23770) and [correct 2019 Pinet paper](https://doi.org/10.1242/dev.175893) should anchor correction and remodeling-inhibition claims.

**Xenobots.** The [2021 primary paper](https://doi.org/10.1073/pnas.2112672118) reports spheroid progenitors with mean 1.2 replication rounds and maximum two, versus semitoroidal progenitors with mean three and maximum four. Offspring are spheroids; additional dissociated cells are supplied. The sphere-one-round wording loses this precision. The pasted 105-degree optimum is not reproduced by the pinned cited script, which repeatedly uses 65 degrees and lacks a required parameter fixture. The exact 105-degree version, angle convention, parameters and sweep output are needed. This is not a refutation of the experimental C-shape advantage.

### Public execution failures

| Self-test attempted | Required fixture absent from the complete pinned Git tree |
|---|---|
| Pietak model | `datasets/bioelectric_morphogen_coupling/voronoi_ca_ip3_branching_reference.json` |
| Craniofacial model | `datasets/xenopus_craniofacial_remap/cartilage_mmp_zymography_reference.json` |
| Xenobot model | `datasets/xenobot_evolutionary_biobots/lattice3d_stokes_capture_reference.json` |

All three fail before completing their checks. This shows incompleteness of the pinned public reproduction package, not that the author never ran a private local version. No fabricated fixture was substituted to produce a pass. Logs and tree checks are preserved.

## 9. Causal-emergence calculations

Independent construction of all-Bubble transition matrices for n=3 through 6 reproduces the important clock-dependent sign change. At n=6, under accepted-swap time, microscale effectiveness is approximately 0.849566 and inversion-count macro effectiveness 0.96875, a gain of 0.119184. With raw proposal steps retained, the values are approximately 0.813044 and 0.762873, a loss of 0.050172.

A changed clock is a changed comparison. Clock dependence does not by itself contradict the measure. A raw microscale compared with an accepted-event macro mixes temporal and spatial changes and must be labelled. A uniform intervention distribution is also not an empirical stationary distribution. A state with no incoming transitions may still be a permitted initial condition or intervention. Calling it physically impossible requires another argument.

The adjacent-error partition is not generally lumpable. The saved witness has `[1,3,2,4]` and `[1,3,4,2]`, both with E=1, but different next accepted-swap macro outcomes. An averaged row-stochastic macro matrix can be defined, but arbitrary multistep projected dynamics need a lumpability or history argument.

These are checks on a small all-Bubble, no-defect model. They do not establish the mixed, target-bearing, defective system's full hierarchy. The later practitioner guide recognizes several such distinctions; that qualification should survive the article's shorter presentation. The recomputed mesoscale numbers also differ from the older scaled constants used in the sorting Lean arithmetic example. The kernel correctly proves the arithmetic supplied to it; it does not certify that those constants came from the current matrix.

## 10. References, quotations and identifiers

All 41 input DOI identities were checked against registration metadata, with retries after rate limiting. A functioning DOI is insufficient: title, authors, date, journal and claimed support must match. Four pairings fail:

| Intended work in Dietz | Incorrect DOI actually identifies | Correct reference |
|---|---|---|
| Claverie and Wainwright, reef-fish morphospace | `10.1111/evo.12502`: a copepod dominance-reversal paper | [PLoS ONE 9:e112732, 2014](https://doi.org/10.1371/journal.pone.0112732) |
| Friedman et al., benthic-pelagic diversification | `10.1093/sysbio/syz029`: Basidiomycota phylogenomics | [Friedman, Price, Corn, Larouche, Martinez and Wainwright, Proc. R. Soc. B 287:20201053, 2020](https://doi.org/10.1098/rspb.2020.1053) |
| Pinet et al., craniofacial correction | `10.1242/dev.175950`: DND1 and germ-cell reprogramming | [Development 146:dev175893, 2019](https://doi.org/10.1242/dev.175893) |
| Pietak and Levin, BETSE | `10.3389/fphys.2016.00178`: mitochondrial/Kv1.3 signaling | [Front. Bioeng. Biotechnol. 4:55, 2016](https://doi.org/10.3389/fbioe.2016.00055) |

Friedman and BETSE also require corrections to journal/year/bibliographic description. Merely replacing a DOI is insufficient. The Planform database article and separately linked Biology Open conceptual article should have separate titles and entries.

The complete register preserves every input occurrence. Registration does not certify peer review, validity, or exhaustive absence of retraction. Software archives and preprints retain their publication types. No blanket no-retraction assurance is made.

### Quotations and version linkage

The no-added-steps quotation matches the published Levin PDF, but the locator is page 29 in the retrieved publication, not the article's page 22. The gradient/recoup wording is not verbatim in that published passage; use an exact alternative source or label it a paraphrase. Rewriting a goal statement into a mathematical gradient statement can change what readers think was claimed.

The official Lex transcript supports the traceability concession and prescribed/forbidden wording at 02:18:32 onward. Feynman's words match the [Caltech source](https://calteches.library.caltech.edu/51/02/CargoCult.htm), with punctuation differences. The [public symposium thread](https://thoughtforms.life/symposium-on-the-platonic-space/) contains Sweet's higher-level-information defense, Levin's reductionist characterization and his November clarification. The October 25, 2026 invitation date was also verified from the original connected-mailbox record; email bodies are not redistributed. That date does not authenticate the changing linked preview's historical contents or independently prove the October 13 article revision date.

The private null-model question, the two YouTube comment quotations, exact Huang wording/original slide, and detailed audiovisual clip timing are not all independently authenticated. They remain typed unresolved entries. Constructed questions, author-reported speech and scare-quoted terms are different categories. The initial 135 phrase candidates are an extraction aid, not a claim that every quotation is verified. A supplemental 136-span multiline/ASCII inventory includes the long two-paragraph Sweet quotation; that wording did not match the retrieved companion article version and needs an exact version or private source. These inventories overlap and their counts must not be added as unique quotations. Figure text and nested quotations still require manual source classification.

The historical comparison has a real primary basis. Thompson's original 1913 lecture supports the biology-to-philosophy discussion and graded-soul analogy; Aristotle's *De Anima* II.3 (414b28-32) supports the geometric inclusion analogy, and II.4 (415b8-12) gives the three-cause account. Exact English wording depends on translation. The lecture also discusses the reasoning soul in stronger language, so it should not be collapsed into a simple modern materialist position. The *Seventh Letter* passage supports a non-writing/ineffability theme, but its authorship is disputed, and it alone does not document a blanket Eleusinian/Delphic ritual prohibition or establish the reliability of direct knowing. See `results/historical_text_checks.json`, the [primary Aristotle translation](https://classics.mit.edu/Aristotle/soul.2.ii.html), [Thompson's original edition](https://doi.org/10.5962/bhl.title.25007), and the [authorship discussion](https://plato.stanford.edu/entries/plato/).

The [Platonic Representation Hypothesis](https://arxiv.org/abs/2405.07987) presents convergence evidence and a hypothesis with limitations; it does not prove the metaphysical interpretation attached to it in Dietz's article. [Artificial Hivemind](https://arxiv.org/abs/2510.22954) addresses studied output distributions. Neither establishes that all tool-using cognitive systems cannot absorb new observations, lack phenomenology, or cannot assess a proposed ontology. Those are separate claims requiring separate evidence.

The retrieved methods, sorting and fish PDFs contain four, thirteen and thirty-six pages; the article describes four, eight and twenty-eight. Both inspected authorship renderers have eight rows, whereas the pasted text describes twelve and different means. These are version-linkage problems, not proof that older private artifacts never existed. Authorship cells are estimates; verifying their arithmetic would not validate the estimated contributions.

### Cryptographic checks

All five listed nanopublication codes resolve through the canonical w3id resolver to production records. The original direct-server attempts returned 404 and are retained as route failures. All five pass trusty-hash and RDF-structure checks. The first client-only signature result was insufficient: a negative control found that the installed `nanopub` 2.2.2 client reports a valid signature even after an assertion is altered. Its verification code includes the signature triple in the signed input and ignores a Boolean failure return from the legacy cryptographic interface. That client result is retained as a failed checking method.

Direct RSA verification then excluded the signature triple, as required by the [nanopublication signing method](https://pmc.ncbi.nlm.nih.gov/articles/PMC7959648/), and used the cryptographic verifier's actual success/failure decision. All five original signatures validate and all five altered assertion copies fail. The two direct cryptographic interfaces agree. RDF normalization is still shared with the Python client; a completely separate canonicalization implementation was not run. The initial signature-included direct attempt is also preserved as an incorrect verification construction, not evidence that the original signatures were invalid. See `results/rsa_direct_checks.json`, `results/crypto_negative_controls.json` and `code/check_rsa_independently.py`.

These final checks establish integrity relative to the embedded public keys. They do not independently establish the human signer's identity, externally witnessed publication time, actual pre-unblinding access control or truth of assertions. Prediction-file hashes also match their signed registration. The audit's own checking tools were therefore subjected to the same negative-control and revision requirements applied to the articles.

A candidate DOI in this audit's own recommended reading list failed title matching. It was rejected, retained in the rejection log and replaced with the verified Kuhn-Dumontier TKDE record. The identity gate applies symmetrically.

## 11. What the philosophical comparison earns

Sweet's strongest surviving point is comparative: defeating stability does not identify an independent Platonic cause; useful behavioral or mathematical descriptions do not by themselves do so either. Dietz's implemented dynamics and unearned-nonphysical-points ledger overlap with that narrow point. Neither demonstrates universal absence of nonphysical patterns.

A structural or constitutive account of mathematical explanation need not posit another physical force. Evaluate it as that kind of account. If a claim adds a causal supplier, specify what it changes relative to serious rivals. Define the extra variable, relation or invariant independently of the residual; freeze the bridge and update rule; test held-out prediction, intervention, compression or another defended comparative advantage. A productive research heuristic can earn its keep without its ontology inheriting the success. Apply the same rule to naturalistic accounts.

The 77.6% and 88.1% calculations are arithmetically correct for the displayed cards. The first equals 77.557142857% before rounding. Claim decomposition, denominators, point assignments and weights are editorial constructs. These percentages are not calibrated probabilities or exhaustive measurements of a 53-page paper's truth. Transparent reweighting does not solve that measurement problem. Expected improvement also needs a horizon and loss condition before it becomes a scored forecast.

Applicable reasoning hazards can be identified without labelling every disagreement a fallacy. Switching between a sorting task and a complete transition specification is equivocation if the inference relies on the switch. Inferring a unique mechanism merely from simulation agreement has the affirming-the-consequent form. Expanding selected fish results into a vertebrate law exceeds the sampled domain. Refuting a withdrawn explanation does not refute a revised argument. A critic's training provenance does not refute a particular checked derivation. Conversely, thermodynamics and organizational closure in Sweet's response should remain candidate explanatory families unless a particular matched biological model has actually earned an advantage.

## 12. Review, distribution and stopping conditions

The machine-checkable core is a numbered claim ledger with boundaries, evidence paths, typed outcomes and revision conditions. Schema validation checks structure; a separate validator checks files, digests and material numerical results. Human readers receive the same evidence in this report, a self-contained HTML rendering, tables, a summary figure and explicit correction priorities. There is no overall truth grade.

For public scholarly release, archive an immutable version with DOI, source commits, dependency lock, commands, inputs, raw result tables, claim ledger, exact derivations, counterexamples and change history. A real RO-Crate should connect those objects; Workflow Run provenance should record executions. Nanopublications can then link individual assertions and superseding corrections to that archive. Scientific replication, peer review and cryptographic integrity remain distinct.

The local evidence archive is a private research bundle. A public release must separately check third-party licenses and replace restricted full texts/private material with appropriate links and hashes. No outside submission or message has been sent. No ChatGPT Library synchronization is claimed.

Checkpoints and `RESUME.md` are the continuation surface. Resume by verifying the manifest and reading the claim ledger, then perform the next discriminating check. Do not repeat completed enumeration without a new discrepancy or silently redefine a failed criterion.

Material unresolved work is explicit: recover the missing biological fixtures; pin the 105-degree model and twelve-row renderer; obtain original comment/audiovisual/private-quotation records; obtain independent evidence of registration time and actual blinding; reconstruct original paper experiment versions and synchronized trajectories; independently reimplement the complete morphometric predictor and phylogenetic uncertainty; and obtain domain-expert review of biological bridges. These are open items, not passed checks. Extending work is warranted where it can materially change a claim or action; exhaustive repetition of already settled arithmetic is not.

Personal recollections, employment history, motives, the lab's broad publication count, every flagship model outside the named checks, and the identity/independence of each reported model-based referee were not independently authenticated. Cross-provider disagreement can be useful adversarial review, but shared source data, prompts and model-training histories prevent treating it as independent scientific replication by default. The stated 24-equation methods inventory is not equivalent to 24 externally validated mechanisms. These coverage limits should remain visible in any public description of this audit.
