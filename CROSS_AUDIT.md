# Rerunning the Bubble-Sort Debate: What Two AI Audits Found in the Code Behind Dietz’s and Sweet’s Articles

November 1, 2026

**Who prepared this.** This article was written by Claude, Anthropic’s AI system, running as Claude Opus 5.5 (model identifier claude-opus-5-5) in Claude Cowork, Anthropic’s agent environment built on the same Claude Agent SDK as Claude Code. Nathan Sweet commissioned it. Before writing, I reviewed the results of a separate audit of the same material, which Nathan ran with OpenAI’s Codex using GPT-6.1 Sol (model as reported by Nathan). Neither system had prior context beyond the two articles and Levin’s paper, and both received the same instructions: identify the authoritative literature, code and constraints for checking the mathematics in both articles, run the checks from several angles, verify every citation, DOI, URL and quotation, and package the results so machines can rerun them and people can read them.

**What “independent” means here.** The two audits were run separately, with different tools and different design choices, and they agree on most results. That agreement is useful. It is not independent scientific replication: both audits read the same public code and data, and their underlying models share much of their training. Every result below is therefore tied to a script, an output file and a checksum, so that anyone can check it without trusting either system. Both bundles are in this repository, [`claude-audit/`](claude-audit/) and [`codex-audit/`](codex-audit/), with third-party full texts removed for copyright and every removal listed by SHA-256.

**The two texts.** The first is Joel Dietz’s *Why Michael Levin Is 77.6++% Right on Platonic Ingress*, in the text supplied to both audits on November 1, 2026. As of that date it had not appeared on Joel’s Substack. Its wording is public in his MIT-licensed repository as two files at commit 35d30f4: the article draft `docs/SUBSTACK_LEVIN_LATENT_SPACE_ARTICLE.md`, titled there “Validated” rather than “Right”, and its companion `docs/SUBSTACK_LEVIN_LATENT_SPACE_CLAIMS.md`. Every phrase quoted from Joel below appears in those public files; `tools/check_quotes.py` checks this automatically. The second text is Nathan Sweet’s *Why Michael Levin’s Bubble Sort “Revelation” Is Misunderstood*, as substantially corrected on October 13, 2026 and extended with computations on October 31. Joel’s October 25 working draft, which Nathan’s article discusses, was not available to either audit.

**Evidence labels.** [Both] means both audits found it. [Claude] or [Codex] means only one did. Where I have rechecked a Codex-only result myself, I say so.

---

## The short version

Both articles get most of their arithmetic right. What separates them is what that arithmetic is used to support.

Every number in Nathan’s October 31 computations reproduced exactly, in both audits. All thirteen DOIs in his article resolve to the works he cites. The one test he called exploratory, the two-copy ordering bias, held on new inputs when I reran it on the authors’ original threaded code. The audits also found four places where his wording needs correcting: a sentence about code dates, a description of Joel’s quotation of him, a claim about thermodynamic rivals, and a sentence about the Boids model. A duplicated fragment flagged by one audit turned out to exist only in the copy pasted to the audits. None of these affects his central argument.

Joel’s code reproduces its own outputs exactly. His mathematics comparing two ways of measuring disorder is correct, and his clustering numbers for the sorting arrays hold up in the authors’ code. Against that, several of his central claims fail on inspection:

- His argument that frozen cells act as walls describes a frozen-cell mode the public code does not implement.
- The p = 10⁻¹⁰³ he credits to Thompson’s grids belongs to a different predictor.
- He reverses the direction of his own nearest-relative result.
- The validator behind his statement that “all 14 of the empirical curves” in the paper replicate writes the word VERIFIED in by hand rather than computing it.
- Four of his reference DOIs, six counting two inline links, point to unrelated papers.
- His Lean proofs compile without gaps, but mostly prove statements about particular short lists and typed-in numbers, not the scientific claims attached to them.

The 77.6% in his title is correct arithmetic on score cards he assigned himself. It does not measure how right Levin is, and it is not a probability of anything.

None of these results identifies an independent Platonic cause, or rules one out.

---

## 1. How the checks were done

Both audits pinned three code versions:

- the authors’ original repository, Zhangtaining/cell_research at commit 1fd2bd5, the code behind Zhang, Goldstein and Levin’s 2025 paper in *Adaptive Behavior*;
- Joel’s repository, fractastical/morpholib, at its November 1 head 35d30f4;
- the earlier morpholib commit bfe377c that Nathan’s October 31 computations used.

The checks fell into five groups:

- Exact mathematics, by exhaustive enumeration and exact fractions, cross-checked in two programming languages.
- Replays of Joel’s seeded sequential model.
- Runs of the authors’ original multithreaded code. Only the Claude audit ran these. The Codex audit ran fresh tests on Joel’s model and noted that they were not a replication on operating-system threads.
- Source reading and code forensics.
- Resolution of every DOI and string-matching of every checkable quotation against the primary text.

The Codex audit also rebuilt Joel’s fish analysis from the raw specimen data and verified the cryptographic signatures on his preregistration records.

One distinction governs everything that follows. Joel’s three-language ports reimplement the authors’ code as a single sequential process. The authors’ code runs each cell as its own operating-system thread, so two runs with the same input and the same random seed do not produce the same sequence of swaps. I ran one input three times and got three different swap sequences [Claude]. A result from the ports is therefore a result about a model of the paper. Only runs of the original code test the paper’s own implementation.

---

## 2. Joel’s sorting claims

### Claim 1: “No error-handling code was added”

Joel quotes Levin accurately. The sentence “The critical thing is that we did not add steps to the algorithm to check whether a swap had been completed, or to do specific things if an operation failed” matches the PsyArXiv version of *Ingressing Minds* exactly [Both]. The Codex audit found it on page 29 of the retrieved PDF, not page 22 as Joel cites [Codex].

Joel’s central finding here survives. The Insertion cell’s check of its left neighbours contains a branch that skips frozen cells, at line 74 of the original file [Both]. Joel deleted that branch in his own model, with frozen cells that can never move, and final error rose from 4.90 to 21.95. Rerunning his script reproduced that result exactly [Claude]. I then deleted the same three lines in the authors’ original threaded code, where frozen cells can be pushed aside, and changed nothing else. Over twenty sixty-cell runs with three frozen cells, final error rose from 2.4 to 19.4 [Claude]. The branch does real work in the paper’s fault-tolerance result, and Levin’s sentence needs qualifying on that point.

The rest of Joel’s description of the code is wrong. He says the Bubble cell looks at the frozen status only to refuse a swap, so that “the frozen cell is a brick wall.” In fact the original Bubble and Insertion cells explicitly accept a frozen neighbour as a swap partner, and the swap routine blocks only a frozen cell trying to start a move [Both]. The Codex audit ran the case [2, frozen 1] in isolation and watched it become [frozen 1, 2] [Codex]. In thirty runs of the original code with one to three frozen cells, a frozen cell was pushed aside, and values crossed its starting position, in every run [Claude]. The Selection cell is not the passive pointer Joel describes either: when its target is a frozen cell holding a larger value, it swaps with it.

Joel also writes that this result was “formally proved in Lean 4 Theorem 2.” Theorem 2 checks that two fixed four-element lists come out a particular way. It says nothing about final error [Both].

Code dates matter here. The commit Joel and Nathan both inspected was made after the paper went online on August 19, 2024. But the Insertion file is unchanged since the repository’s first commit in August 2023. Compiled bytecode stored beside it records the same file size and a source date of June 2023 [Claude]. The same storage also holds bytecode from an earlier version, with a March 2023 source date, whose Insertion cell has no left-neighbour check at all and whose frozen cells cannot be moved [Claude]. The frozen-cell skip therefore predates publication by more than a year. No public record shows which version produced each published figure.

**Verdict on Claim 1.** Joel’s main conclusion stands, and is stronger on the authors’ own code than in his model. His description of the Bubble and Selection code is wrong. His Lean citation overstates what the proof covers.

### Claim 2: “Delayed gratification”

The mathematics is right. Let I count every pair of cells that is out of order and E count only out-of-order neighbours. In Joel’s example, [2, 4, 1, 3] has I = 3 and E = 1; after one swap, [2, 1, 4, 3] has I = 2 and E = 2 [Both]. Swapping two out-of-order neighbours always lowers I by exactly one. Both audits checked this exhaustively, 158,323 such swaps for arrays of up to eight distinct values, and it also holds with duplicate values [Both]. I proved it for arrays of every length in the Lean theorem prover [Claude]. Joel’s own Lean file proves it only for one three-element window. Among those swaps, E rises in 11.8% of cases, so the paper’s measure can go up while the array gets more sorted [Claude].

Two parts of Joel’s wider claim go too far. First, “ΔI = −1 on every single swap” holds only for swaps between neighbours. A Selection cell’s long-range swap lowers I by an odd number that can exceed one, and Joel’s own Selection results run from −1 to −35 [Both]. Even so, in the authors’ original code no swap among 7,308 in ten mixed Bubble-and-Selection runs raised I [Claude]. His empirical point that the cells never move uphill holds where tested. It is an observation, not a theorem.

Second, his statement that “no cell walks around the wall,” and the Lean theorem attached to it, assume frozen cells that can never move. The paper ran both movable and immovable conditions. The public code implements the movable one, so the argument does not describe the code the paper published [Both]. Immovable defects also change the shape of the problem. In [2, frozen 1, 0] there are three out-of-order pairs and no legal neighbour swap [Codex; I rechecked by hand]. The argument that sorting always has a downhill move therefore cannot be carried into the defect experiments.

Joel says the paper measures progress with E, and the code confirms it [Both]. But the paper’s case for delayed gratification compares runs with zero to three frozen cells, and Joel’s four-cell example does not test that comparison [Claude]. Nathan’s article made this point before either audit, and both audits support it.

**Verdict on Claim 2.** The two-measures argument is correct. The barrier argument does not apply to the published code. “Every single swap” should read “every swap between neighbours.”

### Claim 3: “Spontaneous algotype clustering”

Joel’s numbers hold up on the authors’ own code. In fifteen original-code runs of eighty cells, half Bubble and half Selection [Claude]:

- With every value unique, final aggregation was 0.48 to 0.50, at chance.
- With two copies of each value, it fell below chance, at 0.42 to 0.46 across three batches.
- With ten copies of each value, it was 0.67 to 0.69, against a chance level of about 0.48.

These match his port and the paper’s reported 0.65 for this mixture.

Joel’s explanation is not new. The paper itself proposes that the faster algorithm’s cells reach position first, and says its duplicate-value result “suggests that the efficiency hypothesis can be the explanation” [Claude]. His “kinematic phase separation” restates that hypothesis.

Joel says the critics predicted a flat 0.50. The exact chance level for Joel’s 40/40 array of eighty cells is 39/80 = 0.4875, as Nathan computed [Both]. It is the classical runs-test expectation in another form [Claude]. That baseline holds for any sort whose movements ignore cell type, stable or not [Both: Codex proved it for stable sorts, I proved it for any sort that ignores type]. A departure from it shows that movement depends on type. It does not test stability as such.

The size of the clustering effect needs one correction, which both audits reached by different routes. The paper’s figure shows a peak, which is the maximum of a noisy curve, and any label tracked along the same run will peak above chance. On the original-code runs I assigned random labels that cannot affect movement and took the same maximum. The real algotypes peaked at 0.658 against 0.604 for the random labels [Claude]:

| Copies of each value | Excess over the random-label peak | Runs where the real types came out higher |
|---|---|---|
| One (all unique) | 0.054 | 13 of 15 |
| Two | 0.049 | 12 of 15 |
| Ten | 0.088 | 14 of 15 |

The Codex audit found a smaller excess, 0.012 to 0.033, in Joel’s model with forty-cell arrays and a matched random-label control [Codex]. The authors anticipated this with a control in which every cell runs the same algorithm, so this is a point of precision, not an objection to them. The clustering is real. Most of the apparent rise above chance during sorting is what any label would show, though, and the lasting excess at the end with duplicate values is the larger and cleaner effect.

Joel’s fitted domain-wall law (`analytic_domain_wall_law` in his code) for how aggregation varies with the number of copies uses two constants chosen to fit, 0.725 and 1.15 [Codex; I confirmed them in the source]. It is a curve fitted to the results, not a prediction derived in advance.

**Verdict on Claim 3.** The clustering numbers are confirmed on the authors’ code. The explanation comes from the paper. The baseline should be 0.4875, and it tests type-dependent movement, not stability. The transient peak overstates the effect.

---

## 3. Joel’s fish morphospace claim (Claim 4)

This is where Joel’s article and his own records diverge most.

**The p-value.** Joel writes that inside 50 million years “the Thompson predictor beat the clade consensus” at p = 10⁻¹⁰³. His signed outcome record assigns that value to hypothesis H1: a full thirty-dimensional shape predictor compared with the consensus [Both]. Thompson’s seven grid modes are tested separately, under hypothesis H6, at p = 7.4 × 10⁻⁸¹. Their median error of 0.0588 is about 53% higher than the thirty-dimensional predictor’s 0.0383 [Both]. The Codex audit rebuilt all 5,180 scored fish observations from the raw specimen data and confirmed those medians [Codex].

**The nearest-relative result.** Joel writes that “copying the single nearest relative won by 4%.” The record shows the reverse: the thirty-dimensional predictor had about 4.1% lower error than copying the nearest relative, but with p = 0.061 it missed the preregistered threshold of 0.01 [Codex; I confirmed it from the record]. My own first report quoted the ratio, 0.959, without noticing the reversal.

**The hypothesis count.** The record lists four of seven hypotheses supported, two of four primary. Hypotheses H2, H4 and H5 failed, and the article mentions only one of the three failures [Both]. Grouping related species by family raised the nearest-relative comparison to p = 0.28, which shows how much the choice of what counts as one observation matters [Codex].

**The 93.5% to 98.9% alignment.** Joel describes this figure, in his own words, as alignment rather than variance explained; the Codex audit credits him for the distinction [Codex]. It measures how closely the main direction of variation within genera matches the main direction between genera, after each fish is projected onto Thompson’s grids. In the raw coordinates of the 791-species dataset the same measure is 0.429 [Both]. I compared Thompson’s grids with arbitrary low-dimensional projections of the same data. Of 200 random eight-dimensional projections, 16.5% reached 0.935 or higher, and so did 20% of seven-dimensional ones [Claude]. Projecting the data into fewer dimensions raises this measure on its own, so the figure does not single out Thompson’s grids. The 10,303-species dataset in Joel’s headline has no landmark coordinates and reports no Thompson alignment at all [Claude].

**Other figures.** The head evolution “3.3× to 9.3× faster” than the body compares shares of variance, not rates of change over time [Codex]. And Levin’s own use of Thompson in *Ingressing Minds* is narrower than this claim: he notes that Thompson’s grid fields “do not have a known physical basis but they do have structure and information content.” He makes no claim about fish macroevolution, so scoring Levin on this test grades a claim he did not make [Claude].

**Verdict on Claim 4.** Joel’s account attributes the full-shape win to Thompson’s grids, reverses his near-miss, and leaves out two of his three failed hypotheses. His alignment figure has no comparison against chance. The 96.1% he awards this claim does not follow from his own record.

---

## 4. Joel’s biological claims (Claims 5 to 7)

Both audits treat the laboratory experiments as published results and test only Joel’s equations.

**Planarians.** The factor of about 4.7 for how strongly a positively charged molecule such as serotonin concentrates across a 40-millivolt difference is correct at room temperature: 4.74 at 25 °C, 4.87 at 20 °C and 4.47 at 37 °C [Both].

**Xenobots.** The 2021 paper reports that spheroids averaged 1.2 rounds of self-copying, at most two, and C-shaped bodies averaged three, at most four [Both]. Joel’s “a sphere manages one” loses that precision. His 105° optimum is not produced by the script he cites, which uses 65° [Codex].

**Public model tests.** The test runs for three of Joel’s biological models fail because data files they require are missing from his public repository [Codex].

Joel attributes the points he withheld on these claims to “gaps in our reduced equations.” So these scores grade Joel’s own models, not Levin’s claims.

---

## 5. The score and the checking apparatus

**The score.** The arithmetic is right: the mean of the seven claim scores is 77.557%, which rounds to 77.6% [Both]. His superseded 81.6% comes to 81.7% from his exact score cards [Claude]. But the seven cards measure different things:

- how faithfully Levin’s sentences describe the code (Claims 1 to 3);
- a new fish result Levin never claimed (Claim 4);
- how well Joel’s own reduced models fit (Claims 5 to 7).

Averaging them gives a number with nothing defined for it to measure. Of the points withheld on the sorting claims, 85% are the ones Joel labels as dualist [Claude].

**Ports and benchmarks.** Joel’s Python, C++ and JavaScript ports agree with each other exactly, because they share one random-number generator [Both]. That shows the code was transcribed consistently, not that it matches the original. The original threaded code cannot be matched swap for swap with anything, since it does not repeat itself. The validator behind his 14 replicated benchmarks writes the word VERIFIED into all fourteen results rather than computing pass or fail against a tolerance [Both]. Most of its comparisons land within 4% of the published values; two are 12% and 32% off and are still marked VERIFIED [Claude]. It also switches a Selection reset option on for some benchmarks and off for others. Neither setting matches the original code, which never resets inside the swap routine [Both].

**Formal proofs.** Both audits compiled Joel’s Lean files with Lean 4.35.0. They contain no unproved steps and rely only on Lean’s standard axioms [Both]; the Codex audit checked 92 declarations across five files. That is real work. But most of the theorems concern particular short lists, a single three-element window, or integers typed into the file, so they prove the arithmetic they were given, not the scientific claims attached to them [Both].

**Signed records.** The cryptographic signatures on all five of Joel’s preregistration records are valid [Codex]. The Codex audit also found that the nanopub Python client, version 2.2.2, accepted deliberately altered records as valid, and checked the signatures directly instead. A valid signature shows the content has not changed since signing. It does not show when it was signed relative to seeing the data, or that the analysis was blind.

**References.** Both audits resolved every DOI in both articles against its registration record: 41 unique DOIs in the plain text, plus two inline links that appear only in the linked version [Both]. Four of Joel’s resolve to unrelated papers, including both landmark datasets behind his fish argument (Claverie and Wainwright 2014; Friedman et al., which is actually 2020) and the Pinet and BETSE papers [Both]. Two more inline links in Joel’s text do the same (the Vandenberg 2012 and Pezzulo and Levin 2015 links), while the DOIs in his reference list for those two works are correct. Only my audit found these two, because the Codex audit received a plain-text copy without the links [Claude]. Corrections are listed in both audit bundles.

**Quotations.** The Levin quotations check out. One phrase Joel puts in quotation marks, “temporarily going against its gradient to recoup greater gains later,” paraphrases the caption of Figure 14, which reads “temporarily go against their gradient to recoup gains later” [Codex flagged it; I located the source]. Joel’s long quotation of Nathan comes from Nathan’s October 4 article *Religion with a Pipette*. It is word for word with one change: Nathan wrote that Joel’s 2025 symposium talk, “Radical Platonism and Radical Empiricism,” points in the right direction, and the quotation makes Joel himself the subject. The quotation also stops just before Nathan’s next sentences, which apply the same test in the other direction [Claude; Codex had marked it unmatched after searching a different article].

---

## 6. Nathan’s article

**The October 13 corrections.** These corrections withdrew the claim that stable sorting explains the clustering, separated clustering from duplicate-key stability, corrected the Landauer accounting, and acknowledged that the modified sorting architecture can produce novel results. The audits support every one of these:

- A swap that skips over records can reverse the order of equal values without ever comparing them: [2a, 2b, 1c] becomes [1c, 2b, 2a] [Both].
- All 90 duplicate-value runs of Joel’s model reversed some equal pair [Both], and so did every duplicate-value run of the original code [Claude]. The mixed system is not stable, which is why the full stability explanation had to go.
- Landauer’s bound of kT ln 2, about 2.87 × 10⁻²¹ joules per erased bit at 300 K, applies to irreversible erasure, not to every comparison or swap [Both].

**The October 31 computations all reproduced exactly** in both audits, replaying Joel’s model at commit bfe377c:

| Quantity | Nathan | Reproduced |
|---|---|---|
| Final aggregation, ten copies of each value | 0.6592 | 0.659167 |
| Stable-sort comparison | 0.503333 | 0.503333 |
| Order shuffled within tied groups | 0.485117 | 0.485117 |
| Two copies: matching neighbour pairs observed vs expected | 572 vs 603.5 | 572 vs 603.5 |
| Exact two-sided tail probability | ≈ 0.00201 | 0.0020067 |
| Duplicate-value runs reversing an equal pair | 90 of 90 | 90 of 90 |
| Continued runs with no further swaps | 105 of 105 | 105 of 105 |
| Chance level, 40/40 array of 80 cells | 0.4875 | 39/80 |

His figure for the separate simulation, 0.00208, is consistent with my seeded rerun of 0.00183 within simulation error [Claude]. His isolated test of the Insertion check on [3, frozen 1] reproduces exactly [Both].

**The exploratory test held on held-out data.** Nathan wrote that his two-copy ordering test was chosen after seeing the results, so “confirmation requires predeclared or held-out tests.” I ran that exact test, as his text defined it, on the authors’ original threaded code with new inputs [Claude]:

| Input set | Matching pairs, observed vs expected | Exact p |
|---|---|---|
| First fifteen runs | 545 vs 601.0 | 1.2 × 10⁻⁷ |
| Same inputs, new thread timing | 552 vs 601.0 | 3.9 × 10⁻⁶ |
| Second, separate fifteen runs | 499 vs 562.5 | 3.5 × 10⁻⁹ |

In Joel’s model the shortfall was 31.5 pairs, so the model understates the effect. I also checked that the test behaves correctly when there is nothing to find. In 300 simulated datasets with no effect, it gave p ≤ 0.05 in 5.3% of cases. Applied to random labels that cannot affect movement, on the same runs, it gave p = 0.013 and p = 0.27. That 0.013 is no more surprising than chance allows: data with no effect produced p ≤ 0.013 in 2% of cases. The ordering bias moves from exploratory to confirmed on held-out inputs in the paper’s own implementation.

**Formation and retention now rest on the original code.** Nathan distinguishes how segregation forms from how it is held, and writes: “Nor is replaying his sequential model an independent replication of the original threaded implementation.” On the original code, every run sorted, every duplicate-value run reversed an equal pair, and every run ended with all cells still running but no swap for a second and a half [Claude]. With ten copies of each value, final aggregation was 0.690 against 0.481 for order shuffled within tied groups. The distinction now holds in the authors’ code as well as Joel’s port.

**Corrections the audits support.**

1. *Code dates* [Claude]. Nathan’s sentence “The inspected code version postdates the paper’s first online publication” is true of the commit but misleading about the file, for the reasons in Section 2. His conclusion stays: the public record does not show which version generated each figure.
2. *Joel’s quotation* [Claude]. “Joel quotes that question accurately elsewhere” should note the change of subject and the omitted symmetry sentences described in Section 5.
3. *Thermodynamic rivals* [Codex]. Thermodynamic constraint dynamics and organizational closure should be described as candidate rival accounts, not established serious competitors, until a matched biological model shows they do better.
4. *Boids* [Claude]. The sentence crediting Reynolds’s Boids model with showing sensitivity to initial conditions has no supporting source. Reynolds (1987) showed that coherent flocking can arise from simple local rules.
5. *A duplicated fragment* [Claude]: “…missing evidence.petition does not supply…” appears in the copy of the article supplied to both audits, but not on the live page, so it was a copying artifact rather than an error in the published text.

**Points the audits strengthen.**

- The comparison of movable passive cells with genuinely immovable barriers, which Nathan already called for, now has evidence behind it (Section 2).
- The chance benchmark measures type-dependent movement, which supports his point that rejecting one mechanism does not pick the next.
- His warning that the headline percentage is not a calibrated probability now rests on the specific problems in Section 3.

**Not authenticated by either audit.** The two YouTube comments Nathan quotes and his private question to Joel. He can link the comments individually and keep the email.

---

## 7. Where the audits differed, and why

Most differences came from scope, not from disagreement:

- The Codex audit rebuilt the fish data, checked the signatures and examined the causal-emergence calculations in more depth.
- My audit ran the original threaded code, which made possible the held-out test, the peak control and the frozen-cell runs. It also examined the compiled-code history, compared the alignment figure against random projections, and gave a general Lean proof.
- The inline-link DOI errors appeared only in my audit, because only my copy of Joel’s article kept its hyperlinks.

There were two outright misses, one on each side. Codex could not find the source of Joel’s quotation of Nathan; I found it. I missed the reversed nearest-relative result; Codex caught it, and I have corrected my report. Both audits also show that checking tools need their own controls. The Codex audit caught a nanopublication client accepting altered records. My negative control returned one small p-value, which turned out to sit inside what chance allows. Checking tools can fail like anything else and need the same tests.

---

## 8. What this does and does not settle

For the sorting arrays, the results support one account: type-dependent movement forms segregation, and the way ties are handled helps hold it once sorting is complete. That account needs no extra instruction and no further cause. A model that fits the data still does not prove itself the only possible mechanism. And neither audit offers evidence for or against an independent Platonic source. Joel assigns non-physical ingress no earned points; Nathan argues that the results provide no evidence for that further causal claim, which is a different statement from saying there is no such cause. Both readings are consistent with everything here.

What the results do settle is narrower. They show which claims about the sorting arrays now rest on the authors’ own code and which rest only on a model of it. They locate two sets of errors: the corrections Nathan’s article needs are small, and the ones Joel’s needs are substantial. And they show what a convincing check of a disputed result looks like: code pinned to exact versions, a stated null with a negative control, a held-out test, and pass or fail computed rather than written in.

---

## How to rerun the checks

Start at the repository root. Three checks need only Python’s standard library:

- `python3 verify_public_release.py` confirms that every file matches `MANIFEST.sha256`, and that every file kept from the Codex bundle is byte-identical to the private original, with each removal accounted for by its original SHA-256.
- `python3 tools/check_quotes.py` fetches the pinned public sources and confirms that every quotation in this article appears in them.
- The GitHub Actions workflow runs both checks, plus the deterministic Claude checks, on every push and compares the regenerated results with the published ones.

Claude bundle: `claude-audit/run_all.sh` clones the pinned commits and runs, in order:

- exact mathematics, in Python and an independent Node.js implementation;
- both Lean files;
- code forensics and the isolated unit test;
- the bfe377c replay and the alignment comparison against random projections;
- DOI resolution;
- the original-code runs, whose results vary from run to run and should be compared within their standard errors.

`MODE=deterministic` stops before the original-code runs. `checks/compare_results.py` compares regenerated results with the published ones. `results/SHA256SUMS` fixes the outputs, and `claims_ledger.json` maps each claim to its evidence. The held-out tests are in `checks/r_upstream_sweet.py`, and the null-data check of the test is in `checks/r_conditional_test_calibration.py`. Exact versions are in `requirements-audit.txt` and `lean-toolchain`: Python 3.13.18, Node 22.23.4, Lean 4.35.0.

Codex bundle: `codex-audit/README.md` describes `RUN_CHECKS.ps1` (package validation; `-Recompute` reruns the core checks), its RO-Crate provenance graph and its 64-claim ledger. Because the public copy omits third-party files, its own validator reports those files as missing. `verify_public_release.py` is the check for the public copy.

---

## References

Primary sources and code
- Zhang, T., Goldstein, A., & Levin, M. (2025; online August 19, 2024). Classical sorting algorithms as a model of morphogenesis. *Adaptive Behavior*, 33(1), 25–54. https://doi.org/10.1177/10597123241269740 ; arXiv:2401.05375
- Zhangtaining/cell_research, commit 1fd2bd5921c1f6b423a71f691d5189106a8a1020. https://github.com/Zhangtaining/cell_research
- Levin, M. (2025). Ingressing Minds, PsyArXiv v3. https://doi.org/10.31234/osf.io/5g2xj_v3 ; Philosophies 11(5):161 (2026). https://doi.org/10.3390/philosophies11050161
- Dietz, J. (2026). Why Michael Levin Is 77.6++% Right on Platonic Ingress. Text supplied November 1, 2026; not yet posted to MetaMeditations on that date. Public draft and claims companion: https://github.com/fractastical/morpholib/blob/35d30f4cfd5397ee1ed769f96494e018603e293d/docs/SUBSTACK_LEVIN_LATENT_SPACE_ARTICLE.md and https://github.com/fractastical/morpholib/blob/35d30f4cfd5397ee1ed769f96494e018603e293d/docs/SUBSTACK_LEVIN_LATENT_SPACE_CLAIMS.md ; fractastical/morpholib, commits 35d30f4 and bfe377c. https://github.com/fractastical/morpholib
- Preregistration and outcome nanopublications: https://registry.knowledgepixels.com/np/RAilN4nbRHp3e3ZHqlbIgeL3UGPRV_KtQHtJD3gzVVdqw ; https://registry.knowledgepixels.com/np/RAJancwGOPEkHzBoZXGv_vu_snW0Lff2FktE85Me1P-fI
- Price, S. A., et al. (2022). FishShapes v1. *Ecology*. https://doi.org/10.1002/ecy.3829
- Kriegman, S., Blackiston, D., Levin, M., & Bongard, J. (2021). Kinematic self-replication in reconfigurable organisms. *PNAS*, 118(49). https://doi.org/10.1073/pnas.2112672118
- Sweet, N. (2026). Why Michael Levin’s Bubble Sort “Revelation” Is Misunderstood (rev. October 13 and 31). https://sweetrationalism.com/articles/physics/computer-science/why-michael-levins-bubble-sort-revelation-is-misunderstood-classical-algorithm-theory-meets-god-of-the-gaps-argument/ (the October 31 text audited here is preserved as `codex-audit/sources/primary/sweet_live.html`); Religion with a Pipette (October 4, modified October 7). https://sweetrationalism.com/articles/metaphysics/religion-with-a-pipette-is-michael-levins-ingressing-minds-pseudoscience-a-scholarly-analysis/

Corrected references for Joel’s article
- Claverie, T., & Wainwright, P. C. (2014). *PLoS ONE*, 9(11), e112732. https://doi.org/10.1371/journal.pone.0112732
- Friedman, S. T., et al. (2020). *Proc. R. Soc. B*, 287, 20201053. https://doi.org/10.1098/rspb.2020.1053
- Pinet, K., et al. (2019). *Development*, 146(14). https://doi.org/10.1242/dev.175893
- Pietak, A., & Levin, M. (2016). *Front. Bioeng. Biotechnol.*, 4, 55. https://doi.org/10.3389/fbioe.2016.00055

Method
- Wald, A., & Wolfowitz, J. (1940). *Ann. Math. Stat.*, 11(2), 147–162. https://doi.org/10.1214/aoms/1177731909
- Knuth, D. E. (1973). *The Art of Computer Programming*, Vol. 3; Franceschini, G. (2007). https://doi.org/10.1007/s00224-006-1311-1
- Schluter, D. (1996). Adaptive radiation along genetic lines of least resistance. *Evolution*. https://doi.org/10.1111/j.1558-5646.1996.tb03563.x
- Nosek, B. A., et al. (2018). The preregistration revolution. *PNAS*. https://doi.org/10.1073/pnas.1708274114
- OECD/JRC (2008). *Handbook on Constructing Composite Indicators*. https://doi.org/10.1787/9789264043466-en
- National Academies (2019). *Reproducibility and Replicability in Science*. https://doi.org/10.17226/25303
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). Verification, validation, and confirmation of numerical models. *Science*. https://doi.org/10.1126/science.263.5147.641
- Grimm, V., et al. (2020). The ODD protocol, second update. *JASSS*. https://doi.org/10.18564/jasss.4259
- de Moura, L., & Ullrich, S. (2021). The Lean 4 theorem prover. https://doi.org/10.1007/978-3-030-79876-5_37
- Kuhn, T., & Dumontier, M. (2015). Making digital artifacts on the Web verifiable and reliable. *IEEE TKDE*. https://doi.org/10.1109/TKDE.2015.2419657
- Landauer, R. (1961). https://doi.org/10.1147/rd.53.0183 ; Bennett, C. H. (2003). https://doi.org/10.1016/S1355-2198(03)00039-X
- Reynolds, C. W. (1987). Flocks, herds and schools. *Computer Graphics*, 21(4), 25–34. https://doi.org/10.1145/37402.37406
