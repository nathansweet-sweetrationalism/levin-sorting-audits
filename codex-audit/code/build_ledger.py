"""Build an explicitly curated claim register; this script does not adjudicate claims."""
from pathlib import Path
import json,csv,collections
ROOT=Path(__file__).resolve().parents[1]
claims=[]
def add(cid,claim,owner,kind,status,boundary,paths,method,limits,revision,needles=(),alternatives=None):
    loc=[]
    for article,needle in needles:
        hits=[i for i,line in enumerate((ROOT/'inputs'/f'{article}.txt').read_text(encoding='utf8').splitlines(),1) if needle.casefold() in line.casefold()]
        loc.extend({'path':f'inputs/{article}.txt','line':i,'search_text':needle} for i in hits)
    claims.append(dict(id=cid,claim=claim,attributed_to=owner,claim_type=kind,status=status,boundary=boundary,
        target_locations=loc,evidence=[{'path':p,'role':'audit_evidence'} for p in paths],
        check=method,limitations=limits,revision_condition=revision,
        strongest_alternative=alternatives or 'Use the narrower claim stated in the boundary; other mechanisms are not excluded by agreement alone.'))

add('M01','Every adjacent strict inversion swap decreases the global inversion count by exactly one.','both articles','formal','supported',
 'Finite ordered lists; adjacent strict inverted pair; duplicate keys permitted.',
 ['results/independent_math.json','code/check_math_and_replay.py'],
 'Pair cancellation argument; 158,323 distinct-key and 6,015 duplicate-key transition checks.',
 'Enumeration is finite; the mathematical argument supplies the unrestricted identity. Does not identify physical energy.',
 'A counterexample within the stated order and adjacent-swap assumptions, or a defect in the cancellation proof.', [('sweet','inversion')])
add('M02','The equality delta I=-1 applies to every Selection or mixed-system swap.','Dietz','formal','contradicted',
 'Nonadjacent inversion swaps in the cited move class.',
 ['results/independent_math.json','code/check_math_and_replay.py'],
 '[3,2,1] -> [1,2,3] has delta I=-3; general formula independently checked on 19,956 transitions.',
 'Strict inverted endpoints still decrease I, sometimes by more than one; arbitrary non-inversion moves are a separate claim.',
 'Restrict the equality to adjacent strict inversion swaps, or supply different program semantics.', [('dietz','every swap')])
add('M03','Adjacent error may rise while the global inversion count falls.','Sweet; Dietz formal example','formal','supported',
 '[2,4,1,3] -> [2,1,4,3].',
 ['results/independent_math.json','results/lean_kernel_output.txt'],
 'Independent I:3->2 and E:1->2 calculation; pinned Lean concrete theorem compiles.',
 'Does not invalidate adjacent error as an observable or erase comparative defect evidence.',
 'A different metric definition or an error in the supplied example.')
add('M04','Sortedness has no remaining local minimum in the defective legal-move graph.','unrestricted extrapolation','formal','contradicted',
 'Adjacent-only moves with a genuinely immovable middle cell.',
 ['results/independent_math.json'],
 '[2,frozen 1,0] has three inversions and zero legal adjacent moves.',
 'Different defect modes and nonlocal moves define different graphs.',
 'Change the move graph or restrict the no-local-minimum statement to the no-defect model.')
add('M05','A balanced random N=80 linear arrangement has expected A=0.4875 under A=H/N.','Sweet','formal','supported',
 'Fixed 40/40 labels, uniform arrangements, 79 linear edges, denominator 80.',
 ['results/independent_math.json','code/check_math_and_replay.py'],
 'Exact expectation [b(b-1)+s(s-1)]/N^2; 8,188 finite arrangements checked.',
 'N-1 normalization, ring closure and iid labels give different finite-size baselines.',
 'Change the randomization, boundary or denominator.', [('sweet','0.4875')])
add('M06','Merely refusing direct equal-key swaps guarantees global stable sorting.','former explanation','formal','contradicted',
 'Nonadjacent swaps with record identities.',
 ['results/historical_replay_summary.json','results/historical_replay_runs.json'],
 'Explicit [2a,2b,1c] counterexample and identity reversals in all 90 duplicate-key historical runs.',
 'Sweet explicitly retracts the complete stability account; this is not his revised explanation.',
 'A proof of global stability for a differently specified transition system.')
add('M07','Pure global stability predicts an increase of expected endpoint aggregation with duplicate multiplicity.','critic reconstruction of former account','formal','contradicted',
 'Labels randomized independently of keys; globally stable sorting; fixed label counts.',
 ['results/independent_math.json'],
 'A label-independent stable key permutation preserves the uniform fixed-count label distribution.',
 'This conditional consequence is not necessarily a forecast Sweet explicitly published.',
 'A non-independent label/key sampling process or a different null.')
add('S01','Sweet historical C=10 endpoint, stable control and conditional-permutation numbers reproduce.','Sweet','computational','reproduced',
 'Pinned bfe377c model; n=80; 40/40; 15 runs per C; specified seeds; sequential scheduler.',
 ['results/historical_replay_summary.json','results/historical_replay_runs.json','sources/primary/old_model.py','code/check_math_and_replay.py'],
 '105 fresh replay runs: C10 mixed .6591666667, stable .5033333333, conditional mean .4851166667.',
 'Replay of this surrogate is not independent replication of the threaded laboratory paper.',
 'A pinned-source or seed mismatch, incorrect record reconstruction, or reproducible disagreement.', [('sweet','0.659')])
add('S02','Historical duplicate-key trajectories are globally unstable.','Sweet','computational','reproduced',
 'All 90 duplicate-key runs among the 105 historical replays.',
 ['results/historical_replay_summary.json','results/historical_replay_runs.json'],
 'Track original record identities within each equal-key class.',
 'Does not isolate which mechanism creates type aggregation.',
 'A corrected identity tracker changes the reversals.')
add('S03','Continuing the actual sorted terminal cell objects produces no further swaps.','Sweet','computational','reproduced',
 'Pinned historical strict rules, actual final targets retained; all 105 replays.',
 ['results/historical_replay_summary.json','code/check_math_and_replay.py'],
 'Resume terminal objects with stopping-on-sortedness disabled.',
 'Absorption is not active restoration after a scramble, nor evidence about equality swaps in another model.',
 'A legal next swap using the identical source, state and target values.')
add('S04','The reported C=2 conditional exact tail is about 0.00200675.','Sweet','statistical','reproduced',
 'Observed per-key label counts held fixed; independent uniform within-tie permutations across the 15 runs.',
 ['results/C2_conditional_distribution.json','results/historical_replay_summary.json','code/check_math_and_replay.py'],
 'Exact integer counting and convolution; H=572, EH=1207/2; tail P(|H-EH|>=observed distance).',
 'Exploratory null choice; not unconditional randomness; alternative two-sided definitions differ.',
 'A counting error or a materially different justified null or tail definition.', [('sweet','0.002')])
add('S05','Fresh surrogate scheduler/reset perturbations retain some peak excess over matched controls.','this audit','computational','supported',
 '30 fresh n=40 inputs, 2x2 scheduler/reset settings, passive-label Bubble peak controls.',
 ['checkpoints/05_frozen_robustness_protocol.md','results/fresh_robustness.json','code/check_robustness.py'],
 '120 capped tests: all sorted; no cap hits; mean peak excess .0117-.0333.',
 'Descriptive local protocol, not external preregistration or original OS-thread replication.',
 'Matched expanded testing or source-faithful scheduling eliminates or reverses the effect.')
add('S06','Fourteen VERIFIED benchmark labels are computed acceptance decisions.','Dietz','source','contradicted',
 'Pinned validate_kymograph_and_paper.py benchmark dictionaries.',
 ['results/benchmark_label_audit.json','external/morpholib/sorting-morphogenesis/validate_kymograph_and_paper.py'],
 'AST inspection identifies 14 literal status strings rather than threshold decisions.',
 'Does not establish the simulations were never run; approximate agreement still has descriptive value.',
 'Executable preregistered acceptance criteria evaluated from raw replicates replace the literals.', [('dietz','fourteen')])
add('S07','One configuration reproduces every paper summary and exact implementation.','Dietz','computational','overstated',
 'Current sequential port validator and source semantic correspondence.',
 ['results/source_semantics_checks.json','external/morpholib/sorting-morphogenesis/validate_kymograph_and_paper.py'],
 'Different reset settings are used for different comparisons; original swap and merge paths differ.',
 'Port documentation discloses some choices; unpublished original source-to-paper trajectory is unavailable.',
 'One pinned source-linked configuration passes prespecified joint trajectory and uncertainty checks.')
add('S08','Pinned upstream MultiThreadCell.swap invokes update and resets targets.','port explanation','source','contradicted',
 'Original source commit 1fd2bd5; not necessarily the earlier paper experiment bytes.',
 ['results/source_semantics_checks.json','external/cell_research/modules/multithread/MultiThreadCell.py'],
 'Inspect swap AST and call graph: no update call; CellGroup merge invokes it.',
 'Published experiment version is not established by this later source.',
 'An exact paper-version source demonstrates the asserted call path.')
add('S09','The surrogate reverse-direction reset is source-identical.','port fidelity assertion','source','contradicted',
 'Pinned upstream reverse Insertion reset versus surrogate sentinel.',
 ['results/source_semantics_checks.json'],
 'Original resets prev=-1; surrogate uses positive infinity in descending mode.',
 'A semantic repair can be useful without being a source-identical port.',
 'Prove observational equivalence under the applicable state domain or relabel the repair.')
add('S10','Every frozen Bubble cell is an immovable barrier.','blanket wall wording','source','contradicted',
 'Pinned Bubble.should_move_to and isolated legal swap.',
 ['results/actual_source_transition_checks.json','code/check_actual_source.py'],
 'A FREEZE target is allowed passively: [2,frozen 1] -> [frozen 1,2].',
 'Truly immovable defect mode remains a valid barrier case.',
 'Restrict wording to the immovable mode or pin a different defect implementation.')
add('S11','The enabling Insertion branch affects movement over a frozen prefix.','Dietz; source check','source','supported',
 'Actual upstream is_enable_to_move extracted and tested in isolation.',
 ['results/source_semantics_checks.json','code/check_source_semantics.py'],
 'Prefix [3,frozen 1] enabled with branch and disabled when branch removed.',
 'A one-step result does not establish the original published defect advantage.',
 'Source-faithful full experiment or earlier code changes the attributed effect.')
add('S12','Cross-language equality has been verified for every synchronized trajectory.','Dietz','computational','overstated',
 'Fresh Python/Node 42-cell cases plus archived C++ artifact.',
 ['results/language_port_check.json','results/node_port_output.json','code/run_node_port.mjs'],
 'All 126 final cells and archived C++/Node summary comparisons match.',
 'C++ not recompiled; complete trajectories not independently compared; initial Windows direct-entry guard silently skipped execution.',
 'Fresh third-language execution and full synchronized state hashes establish the stronger claim.')
add('S13','The current domain law is entirely derived without fitted or hard-coded shape constants.','Dietz','source','overstated',
 'quantify_emergence_ce2.py empirical curve expression.',
 ['external/morpholib/sorting-morphogenesis/quantify_emergence_ce2.py'],
 'The curve expression contains constants .725 and 1.15.',
 'Constants could have an external derivation; the expression alone does not supply it.',
 'A documented derivation and held-out test of these constants.')
add('F01','The five checked Lean files compile without sorryAx in 92 audited declarations.','Dietz; this audit','formal','reproduced',
 'Lean 4.35.0 official checked release; sorting7, MathOfBiology76, biological loop3+3+3.',
 ['results/lean_toolchain.json','results/lean_kernel_output.txt','results/lean_additional_kernel_checks.json'],
 'Fresh kernel runs and transitive #print axioms logs on source copies.',
 'This does not certify source equivalence, model truth, all repository files, or all biological dynamics.',
 'A toolchain-integrity defect, incomplete-proof axiom, or narrower statement than reported.')
add('F02','Kernel acceptance proves the biological mechanisms or experimental dynamics.','strong article inference','causal','overstated',
 'Inspected MathOfBiology and three biological loop statement definitions.',
 ['results/lean_additional_kernel_checks.json','external/morpholib/morphoeval/lean/MathOfBiology.lean'],
 'Inspect statements: threshold arithmetic, target-returning branch and supplied capture integer expression.',
 'These conditional theorems remain valid and useful; they need a model-to-experiment bridge.',
 'Formalize actual dynamics, assumptions and measurement linkage; validate the empirical bridge.')
add('P01','All 5,180 scored fish observations and four error series reconstruct from raw data and locked predictions.','Dietz; this audit','computational','reproduced',
 '16,523 FishShapes specimens; saved predictions; supplied calibration; all scored species.',
 ['results/fish_independent_audit.json','code/check_fish.py'],
 'Raw MD5 and both prediction hashes verified; medians and calibrated absolute errors reconstructed.',
 'The complete original prediction engine was not independently reimplemented.',
 'A raw-data mapping, species normalization, calibration or arithmetic discrepancy.')
add('P02','The nearest-relative method wins by approximately four percent.','Dietz','statistical','contradicted',
 '1,122 species at tau<50 Myr; body depth/length; calibrated median absolute errors.',
 ['results/fish_independent_audit.json'],
 'Full30 .0383444031 versus nearest .0399934723: full30 is 4.1233% lower.',
 'The superiority test still fails alpha=.01; median direction and test decision are different questions.',
 'A different pinned version, metric or raw result reverses the stated comparison.', [('dietz','4%')])
add('P03','Full30 meets the registered nearest-relative superiority test.','stronger interpretation','statistical','contradicted',
 'Species-wise one-sided Wilcoxon; registered alpha .01.',
 ['results/fish_independent_audit.json'],
 'Recomputed p=.0606819870148897.',
 'Failure to pass is not proof that the rival is better or that effects are equal.',
 'A justified independent preregistered test with adequate dependence treatment changes the conclusion.')
add('P04','The approximately 1e-103 p-value describes the seven-mode predictor.','Dietz','statistical','contradicted',
 'Calibrated tau<50 body-depth comparison with consensus.',
 ['results/fish_independent_audit.json'],
 'Full30 p=1.04905e-103; Thompson7 p=7.38314e-81.',
 'Both are species-wise calculations and do not establish an evolutionary law.',
 'Relabel predictor or provide an explicitly different version and comparison.')
add('P05','Only H2 misses the registered calibrated criteria.','incomplete summary','statistical','contradicted',
 'Pinned result file, calibrated H1-H7 decisions.',
 ['results/fish_independent_audit.json'],
 'H1 pass,H2 fail,H3 pass,H4 fail,H5 fail,H6 pass,H7 pass.',
 'H4 can fail because performance is better beyond the claimed horizon; failed direction must still be retained.',
 'Show a different preregistered criterion/version without retrospective redefinition.')
add('P06','Species-wise Wilcoxon p-values adequately settle phylogenetically correlated predictive performance.','unqualified inference','statistical','overstated',
 'Related species sharing training relatives, taxa and measurement sources.',
 ['results/fish_independent_audit.json','results/recommended_literature.json'],
 'Exploratory 54-family mean-difference test gives p=.28056; dependence remains.',
 'Coarse family averaging is not a full phylogenetic correction or definitive null result.',
 'A preregistered phylogenetic or blocked evaluation, with uncertainty and overlapping-source audit.')
add('P07','Calibration coefficients independently reproduce to numerical precision.','this audit','computational','reproduced',
 'Original 791-species landmarks, source GPA/proxies, 710/711 matched training species.',
 ['results/morphometrics_calibration_check.json','code/check_morphometrics_calibration.py'],
 'Fresh fitting agrees with saved alpha/beta within 4.4e-16.',
 'Shares source GPA and proxy definitions; prediction engine and independent measurement choice not validated.',
 'Independent landmark processing or species matches reveal material discrepancy.')
add('P08','The 93.5-98.9% alignments should be distinguished from variance explained.','Dietz explicitly qualifies this','semantic','supported',
 'Cosines between selected drift representations.',
 ['sources/primary/dietz_fish.txt'],
 'Identify cosine definition and raw-versus-selected coordinate dependence.',
 'Dietz explicitly preserves the distinction. The complete large-compilation alignment was not independently recomputed here.',
 'Provide a separate variance-explained metric with held-out baseline and dimensions.')
add('P09','The displayed factors show 3.3-9.3-times-faster head evolution.','Dietz','statistical','overstated',
 'Ratios of variance-loading percentages, not change per unit time.',
 ['sources/primary/dietz_fish.txt'],
 'Ratios 47/14.41 and 85.4089/9.21807 reproduce the factors.',
 'Loading ratios need not equal evolutionary rates; phylogenetic timing not in this calculation.',
 'A module-specific time-scaled evolutionary rate model validates the rate claim.')
add('P10','Positive sampled Jacobian determinants prove global bijectivity.','strong topology inference','formal','contradicted',
 'Finite grid checks of a shape map; arbitrary domain.',
 ['AUDIT_REPORT.md'],
 'Counterexample exp(x)*(cos y,sin y) has positive determinant but repeats beyond one angular turn.',
 'Does not prove the specific tested map folds; more domain-specific proof may be available.',
 'A valid global injectivity and boundary/domain argument for the actual map.')
add('P11','The extant fish analysis establishes a universal vertebrate law over 150 Myr.','Dietz','empirical','overstated',
 'Selected extant reef-fish datasets and dated phylogeny.',
 ['results/fish_independent_audit.json','sources/primary/dietz_fish.txt'],
 'Audit sampling boundary, measurement overlap, model dimensions and tested endpoints.',
 'No new fossil trajectory, vertebrate-wide, or experimental validation here.',
 'Held-out clades, independent measurements and causal/mechanistic predictions validate broader transport.')
add('B01','The idealized 40-mV Nernst ratio is about 4.7.','Dietz','formal','supported',
 'Monovalent species, positive coupling, zero flux, fixed voltages/temperature and compatible boundaries.',
 ['results/independent_math.json'],
 'At298.15K exp(F*.04/RT)=4.743948; stated25.85mV thermal voltage is about300K.',
 'Tiny temperature precision issue; equation at G=0 does not determine the ratio or memory.',
 'Different valence, reactions, boundary conditions or finite-time model changes the inference.')
add('B02','The zero-flux ratio alone proves persistent planarian target memory under complete blockade.','strong mechanism inference','causal','overstated',
 'Reduced equation versus persistent tissue-level experiment.',
 ['results/independent_math.json','sources/primary/durant_2017.pdf'],
 'At zero conductance the flux equation imposes no ratio; persistence needs feedback, turnover and timescale.',
 'The persistent phenotype experiment remains independent empirical evidence.',
 'A calibrated dynamical model predicts persistent editing and discriminating interventions.')
add('B03','The public Cervera script is an exact reproduction of the full paper.','article-level reproduction implication','source','contradicted',
 'Pinned qualitative analogue script and access disclosure.',
 ['external/morpholib/models/2021-Cervera–Levin–Mafe.py'],
 'Source explicitly says full text not consulted and constants are the script\'s.',
 'An abstract-guided analogue can be informative; it is not source-faithful equation reproduction.',
 'Read and map the full paper equations, parameters and numerical methods to source.')
add('B04','A quadratic target gradient model dissipates its defined potential.','Dietz','formal','supported',
 'Continuous dynamics xdot=-eta*grad(V),eta>0; positive-definite target potential.',
 ['sources/primary/dietz_methods.txt','AUDIT_REPORT.md'],
 'Chain rule gives Vdot=-eta*||grad(V)||^2.',
 'Assumes the target; does not establish biological storage or unconditional discrete-time convergence.',
 'A changed dynamical equation or numerical step violates the assumptions.')
add('B05','Three pinned biological self-tests run successfully from the public repository.','public reproducibility claim','computational','unreproduced',
 'Current public tree and unmodified self-test entry points.',
 ['results/upstream_execution_checks.json','results/missing_public_fixtures.json'],
 'All three exit with missing required reference fixtures; complete tree checked.',
 'Does not imply the author never ran a private version; no invented fixture substituted.',
 'Publish exact missing fixtures and dependencies; rerun unchanged tests and raw checks.')
add('B06','The cited pinned xenobot model establishes a 105-degree optimum.','Dietz','computational','unreproduced',
 'Pinned public xenobot script, available parameters and missing fixture.',
 ['results/xenobot_selftest.json','results/missing_public_fixtures.json','sources/primary/dietz_fish.txt'],
 'Public script repeatedly uses65degrees; required capture fixture absent.',
 'Angle convention or private version may differ; not a refutation of experimental C-shape advantage.',
 'Pin exact105degree code, convention, parameters and independent sweep output.', [('dietz','105')])
add('B07','The 2021 sphere comparison is exactly one generation versus four.','Dietz simplified wording','empirical','overstated',
 'Published xenobot replication rounds with supplied dissociated cells.',
 ['sources/europepmc/PMC8670470.txt'],
 'Primary reports spheroids mean1.2/max2, semitoroids mean3/max4; offspring spheroids.',
 'The relative C-shape benefit survives; no new experiment conducted.',
 'A distinct experimental condition or corrected exact wording.')
add('C01','A positive inversion-count macro effectiveness gain occurs in the checked accepted-swap model.','Dietz','computational','reproduced',
 'All-Bubble,no-defects,n3..6,uniform interventions,accepted-swap clock.',
 ['results/causal_measures_independent.json','results/author_causal_code_recomputed.json','code/check_causal_and_ports.py'],
 'Independent transition construction; n6 micro .849566 vs macroI .96875.',
 'Not the full mixed or defective system, nor an ontological identity.',
 'A clock/partition/matrix or intervention-distribution correction changes the score.')
add('C02','The same causal-gain sign survives raw proposal-time dynamics.','clock-independent inference','computational','contradicted',
 'All-Bubble,n6,raw proposal clock with unchanged intervention convention.',
 ['results/causal_measures_independent.json'],
 'Micro .813044 vs macroI .762873 gives negative .050172.',
 'Changing clock changes the model; sign reversal is not by itself a contradiction in the measure.',
 'A defended same-clock comparison or a corrected matrix alters this result.')
add('C03','Adjacent-error partition defines autonomous multistep Markov dynamics automatically.','unqualified coarse-graining','formal','contradicted',
 'Accepted-swap all-Bubble process.',
 ['results/actual_source_transition_checks.json','results/source_semantics_checks.json','AUDIT_REPORT.md'],
 'Same E=1 states [1,3,2,4] and [1,3,4,2] have different projected next-step outcomes.',
 'Averaged row-stochastic matrix can still be defined; autonomy requires lumpability/history qualification.',
 'Prove lumpability for the actual partition or use a sufficient augmented macrostate.')
add('C04','A state with no incoming transitions is physically impossible.','unqualified state-support inference','formal','overstated',
 'Uniform interventions versus observational stationary support.',
 ['AUDIT_REPORT.md','external/morpholib/docs/CAUSAL_EMERGENCE_PRACTITIONERS_GUIDE.md'],
 'Initial states and interventions may place probability on no-incoming states.',
 'Some physical realization constraints could prohibit a particular intervention; they must be stated.',
 'An explicit realization restriction or intervention distribution establishes impossibility.')
add('R01','Every cited DOI points to the intended paper.','both article bibliographies','source','contradicted',
 '41 unique input DOI identities, all occurrences retained.',
 ['results/reference_checks.json','results/doi_occurrences.json','results/doi_metadata_summary.json'],
 'Registry title/author/journal/date comparison finds four Dietz mismatches.',
 'Other identity matches do not validate contents, quality, full reading or exhaustive retraction absence.',
 'Correct four entries with correct title/journal/year as well as DOI.')
add('R02','All direct quotations and locators in both articles are independently authenticated.','scope requested by user','source','unverified',
 '135 extracted curly-quote candidates plus supplemental span audit.',
 ['results/quote_checks.json','results/quote_inventory.json','AUDIT_REPORT.md'],
 'Preserved-source normalized word matching and manual adjudication; unresolved types retained.',
 'Private question,YouTube comments,Huang recording,other audiovisual and translation locators remain open.',
 'Acquire primary records and adjudicate every genuine quotation with exact source/version/locator.')
add('R03','The no-added-steps quotation matches the published Levin text at the cited page.','Dietz','source','partially_supported',
 'Retrieved53page published PDF,section6.3.',
 ['results/ingressing_quote_page.png','sources/primary/ingressing.txt','results/quote_checks.json'],
 'Wording verified and rendered page inspected; actualpage29, articlelocator22.',
 'A different draft may have different pagination; pin it rather than silently mixing versions.',
 'Supply exact earlier draft or correct the published locator.')
add('R04','The gradient/recoup phrase is verbatim in the cited published passage.','Dietz','source','contradicted',
 'Published section6.3, page29, rather than unspecified lecture or earlier draft.',
 ['results/quote_checks.json','sources/primary/ingressing.txt'],
 'Published passage uses different goal wording.',
 'Could come from another source; call it a paraphrase until an exact locator is provided.',
 'An exact independently inspectable alternate primary source matches those words.')
add('R05','The public exchange includes Sweet\'s higher-information defense and Levin\'s reductionist characterization.','Sweet','source','verified_source',
 'Symposium comments4345,4350,4449 with dates and surrounding text.',
 ['results/symposium_comment_excerpts.json'],
 'Primary public comment thread retrieved and context inspected.',
 'Verifying speech does not settle whether either philosophical argument is correct.',
 'A source/version/context correction changes the attributed words.')
add('R06','The October25 invitation to comment on a draft is dated by the original message.','Sweet chronology','source','verified_source',
 'Connected mailbox original metadata2026-10-25T19:50:01Z; bounded relevant read.',
 ['results/private_chronology_check.json'],
 'Original message metadata and draft-comment invitation inspected; no messages sent.',
 'Email body not redistributed; linked preview history and October13 revision date not independently frozen.',
 'Original-header provenance contradicts date or exact historical preview is recovered.')
add('R07','HTTP access failure establishes a reference or URL is false.','possible checking shortcut','source','contradicted',
 '37 explicit pasted URL strings and DOI endpoint retries.',
 ['results/url_checks.json','results/url_resolution.json'],
 'Separate route/access failures from bibliographic identity; some YouTube pasted captions corrupt raw URL strings.',
 'HTTP200 can be a challenge page; neither200nor403 alone authenticates content.',
 'A correct canonical URL and content identity check resolves each case.')
add('R08','All five nanopublications have valid content hashes, embedded-key signatures and RDF structure.','Dietz; this audit','computational','reproduced',
 'Five canonical production records retrieved via w3id; nanopub2.2.2 read-only checks.',
 ['results/nanopub_crypto_checks.json','results/nanopub_identifier_checks.json','results/rsa_direct_checks.json','results/crypto_negative_controls.json','code/check_rsa_independently.py'],
 'All five hashes/structures valid. Initial client signature checker fails tamper controls; direct RSA verification with required signature-triple exclusion validates all originals and rejects all five tampered copies.',
 'RDF normalization shared with nanopub2.2.2;direct RSA acceptance checked through two interfaces. Does not independently prove human identity, external timestamp, blinding or scientific truth.',
 'Cryptographic/profile defect or independently witnessed provenance changes the claim.')
add('R09','The exact described manuscript page counts and twelve-row authorship table are pinned.','Dietz','source','unverified',
 'Retrieved methods/sorting/fish PDFs and two inspected authorship renderer versions.',
 ['results/authorship_arithmetic.json','sources/primary/dietz_methods.pdf','sources/primary/dietz_sorting.pdf','sources/primary/dietz_fish.pdf'],
 'PDF lengths4/13/36 differ from article4/8/28; inspected renderers8rows rather than12.',
 'Earlier private versions may exist; contribution estimates themselves are not established by arithmetic.',
 'Publish exact version hashes, twelve-row source and matching rendered outputs.')
add('O01','The displayed mean score rounds to77.6%; the structural mean is88.1%.','Dietz','formal','supported',
 'Seven displayed point cards and their stated weights.',
 ['results/independent_math.json'],
 'Recompute arithmetic:77.557142857 and88.100000000.',
 'Editorial decomposition and points are not calibrated truth probabilities or exhaustive content measurement.',
 'Change cards,weights or denominator explicitly; calibration needs external scored outcomes.')
add('O02','Convergence or output-diversity papers establish the attached metaphysical or phenomenological conclusions.','Dietz','ontological','overstated',
 'Platonic Representation Hypothesis and Artificial Hivemind versus broad system-boundary claims.',
 ['sources/primary/platonic_representation.txt','sources/primary/hivemind.txt'],
 'Inspect measured outputs, stated hypothesis and inferential reach.',
 'Neither tested phenomenology nor all tool-using cognitive systems\' capacity to incorporate observations.',
 'Separate independently specified bridge evidence discriminates the broader rival hypotheses.')
add('O03','Failure of a complete stability explanation identifies a Platonic causal contribution.','inference disputed by Sweet','ontological','unsupported',
 'Sorting observation, candidate mechanisms and explanation type.',
 ['AUDIT_REPORT.md','results/historical_replay_summary.json'],
 'Alternative ordinary mechanisms remain; observed fit alone does not select a unique cause.',
 'Does not prove universal absence of nonphysical patterns; constitutive mathematical explanations need separate evaluation.',
 'Specify a distinctive comparative prediction/intervention or defended explanatory advantage and test it.')
add('O04','Broad thermodynamic or organizational alternatives have already quantitatively explained every biological case.','possible overreading of Sweet','causal','unsupported',
 'Suggested explanatory families versus the particular biological datasets.',
 ['AUDIT_REPORT.md','inputs/sweet.txt'],
 'No matched calibrated alternative supplied here for every experiment.',
 'These remain serious research programmes and constraints, not automatically completed explanations.',
 'A specific validated model produces discriminating predictions for the matched case.')
add('O05','Generation of an additional useful mathematical output has zero physical energy cost.','unqualified free-lunch inference','empirical','unsupported',
 'Computational reuse versus measured realization,clock,energy and information loss.',
 ['AUDIT_REPORT.md','results/reference_checks.json'],
 'Logical superposition or extra measured output does not specify incremental energy accounting.',
 'Reversible/logically nonerasing operations and implementation reuse can lower cost; no universal per-output cost asserted here.',
 'Matched measured energy and error-controlled outputs establish a narrower efficiency claim.')

add('P12','The wing data reproduce the stated65.8% perimeter projection statistic.','Dietz','computational','reproduced',
 '1030raw wing rows;1027retained specimens;30species;19landmarks;later anatomical partition.',
 ['results/wing_checks.json','code/check_wings.py','sources/primary/wing_landmarks.tab','sources/primary/wing_specimens.tab'],
 'Fresh source-GPA/basis reconstruction matches species means;perimeter .658212,interior -.003748,global .387760.',
 'Shares original GPA/basis. Specimens are not independent evolutionary replicates;later partition needs new validation.',
 'Independent landmark or partition validation changes the representation statistic.')
add('P13','The original wing test records0of7passes rather than suppressing its failed predictions.','Dietz','computational','partially_supported',
 'Saved W1-W7 results,30species and their prediction error outputs.',
 ['results/wing_checks.json','external/morpholib/thompson/portfolio/results/vespinae_wings.json'],
 'All seven stored decisions false;medians,selected tests and Brier .448214 recomputed.',
 'Full fitting,all noise/allometry controls and independent preregistration timing were not re-established.',
 'Independent refitting or externally witnessed provenance changes the stored test assessment.')
add('P14','The illustration-specific shape-fit and TPS folding percentages have been independently reproduced in this audit.','scope requested by user','computational','unverified',
 'Six selected image pairs;2.4%fin-tip,40.6to56.2%mismatch and6of6folding statements.',
 ['AUDIT_REPORT.md','external/morpholib/thompson/generate_13yo_visual_guide.py'],
 'Trace to source descriptions and note literal display values; full image-source optimization not rerun.',
 'No claim that these values are false. Need masks,homology choices,optimizer bounds and global topology analysis.',
 'Reproduce the pinned original images and optimization with matched competitors and acceptance criteria.')
add('R10','The triangle/square analogy and three-cause account have primary historical support.','Dietz','source','partially_supported',
 'DeAnima II.3 andII.4;Thompson1913original OCRpp26-27.',
 ['results/historical_text_checks.json','sources/primary/aristotle_soul_mit.plain.txt','sources/primary/thompson1913_ocr.txt'],
 'Inspect translated primary passages and original lecture context.',
 'Exact wording translation-dependent;OCRGreek not image-verified;not a mathematical confirmation of modern ontology.',
 'A critical-edition or contextual correction changes the interpretation.')
add('R11','The Seventh Letter supports the full historical ritual and epistemic-reliability claims.','Dietz','source','overstated',
 '341c-d ineffability/non-writing passage and broader claims about direct knowing.',
 ['sources/primary/plato_letter7.plain.txt','results/historical_text_checks.json'],
 'Primary translation read;authorship controversy checked in SEP.',
 'Passage supports a narrower theme;does not alone establish ritual prohibition or reliable modern inference.',
 'Independent primary ritual records and critical historical scholarship establish the broader claim.')
add('R12','All flagship models,referee identities,counts and personal-history claims are independently verified here.','scope requested by user','source','unverified',
 'Named computations and paper identities versus broader autobiographical and project-scale claims.',
 ['AUDIT_REPORT.md'],
 'Explicitly separate material named checks from unauthenticated project/personal claims.',
 'Cross-provider model outputs do not automatically constitute independent scientific replication.',
 'Obtain public source-linked run receipts,exact model metadata,independent checks and relevant historical records.')

schema={
 '$schema':'https://json-schema.org/draft/2020-12/schema','$id':'https://example.invalid/levin-audit/claims.schema.json',
 'title':'Dietz-Sweet audit material-claim ledger','type':'object','additionalProperties':False,
 'required':['schema_version','created','scope','not_a_truth_oracle','claims'],
 'properties':{
  'schema_version':{'const':'1.0'},'created':{'type':'string'},'scope':{'type':'string'},'not_a_truth_oracle':{'const':True},
  'claims':{'type':'array','minItems':1,'items':{'type':'object','additionalProperties':False,
   'required':['id','claim','attributed_to','claim_type','status','boundary','target_locations','evidence','check','limitations','revision_condition','strongest_alternative'],
   'properties':{
    **{k:{'type':'string','minLength':1} for k in ['id','claim','attributed_to','claim_type','boundary','check','limitations','revision_condition','strongest_alternative']},
    'status':{'enum':['supported','reproduced','contradicted','overstated','unreproduced','unverified','verified_source','partially_supported','unsupported']},
    'target_locations':{'type':'array','items':{'type':'object','required':['path','line','search_text'],'properties':{'path':{'type':'string'},'line':{'type':'integer','minimum':1},'search_text':{'type':'string'}},'additionalProperties':False}},
    'evidence':{'type':'array','minItems':1,'items':{'type':'object','required':['path','role'],'properties':{'path':{'type':'string'},'role':{'type':'string'}},'additionalProperties':False}}
   }}}
 }}
data={'schema_version':'1.0','created':'2026-11-01','scope':'Material claims in the supplied article versions and audited sources. Claim wording is an audit restatement, not necessarily a verbatim author quotation. Not every sentence is a separate claim. Target locators are lexical aids.','not_a_truth_oracle':True,'claims':claims}
(ROOT/'results/claims.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
(ROOT/'results/claims.schema.json').write_text(json.dumps(schema,indent=2),encoding='utf8')
with (ROOT/'results/claims.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','claim','attributed_to','claim_type','status','boundary','check','limitations','revision_condition','strongest_alternative','evidence','target_locations']);w.writeheader()
 for row in claims:
  r=dict(row);r['evidence']=' | '.join(x['path'] for x in row['evidence']);r['target_locations']=' | '.join(f"{x['path']}:{x['line']}" for x in row['target_locations']);w.writerow(r)
print(json.dumps({'claims':len(claims),'status_counts':dict(collections.Counter(x['status'] for x in claims))},indent=2))
