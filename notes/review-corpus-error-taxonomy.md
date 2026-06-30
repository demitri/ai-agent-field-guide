# Scope: review the reviews → an empirical error taxonomy of the model

Raw scoping material for a dedicated session. Not yet a lesson — this is the
brief a future session executes, distilled from the conversation that raised it
(a fits-test-suite session, 2026-06-30, while building anti-whack-a-mole gate
machinery). Owner's framing: *"Claude has exhibited certain errors repeatedly
(e.g. hiding/skipping errors); a skill was created for that one. I identified that
behaviour. It would be interesting to identify further classes — given everything is
written by one model and undergoes many reviews, can we review the reviews to find
common patterns across projects and design targeted reviews?"*

## The thesis (why this is tractable, not just introspection)

Everything the owner's agents produce is written by **one model**. So its errors are
not random — they are **correlated and systematic**: a model has a characteristic
failure distribution because certain mistakes are baked into how it reasons. The
review corpus (every codex/sonnet/opus round across every project) is therefore a
**labeled dataset of that model's mistakes**: each finding is `(what was wrong →
the correction → the lens that caught it → severity)`. Clustering it yields the
model's empirical blind-spot map.

Lesson 03 (`never-silently-skip`) is **one cluster the owner found by hand**, and the
dedicated audit skill is the proof that a recurring class, once named, can be turned
into a targeted review that actually works (the bare rule empirically failed; the
*pass* didn't). This task asks: read the rest of the map out of the corpus, and ship
a targeted review per high-frequency class. It is the project's own "rule of two"
(second instance ⇒ mechanize) applied to the **model's own failure modes**.

## The corpus

On disk under `~/.claude/projects/<encoded-repo>/*.jsonl`: **~1,717 transcript files
across 39 project dirs** as of 2026-06-30; the owner counts **~196 distinct
sessions**. **Step 1 of the harvest is to reconcile that unit and count precisely**
(files vs sessions vs sidechains/empty) — fail loud on the discrepancy, don't quote a
number until it's derived. The transcripts hold the *raw* review exchanges (the
actual codex/sonnet/opus outputs and the back-and-forth), which is richer than the
git changelogs that only summarize findings. Secondary, pre-curated sources:
per-repo **Opus Delta Logs** (e.g. fits-test-suite `ANALYSIS_QUEUE.md` — records what
opus found that codex+sonnet missed, per item), "review fix" commit messages, and
session change-logs.

## Method (harvest → classify → rank → targeted review)

1. **Define the session unit + count** (above). Enumerate the transcript set.
2. **Harvest findings.** Extract each review finding + its correction + the lens that
   caught it + severity. Mostly mechanical (review rounds have stereotyped shapes:
   "Finding — …", "P1/P2/P3", "addressed in {hash}; review", "dry round").
3. **Classify by FAILURE MODE, not by surface** (not by file/feature/project). The
   axis is *how the reasoning went wrong*.
4. **Rank by frequency × cost**, and cut by **which lens caught it** (see caveat 3).
5. **Per high-frequency class, choose the instrument:** a mechanical **gate** if the
   class is decidable; a **targeted review pass/skill** (the Lesson-03 shape) if it's
   judgment; a **standing-veto / CLAUDE.md line** (Lesson 05/10) if it's a
   convention. Prose reminders are *not* an instrument (caveat 4).

## Candidate families already visible (seed hypotheses, to be tested against the corpus)

From one session's evidence — treat as priors, not conclusions:

- **Overclaim — the claim exceeds the evidence.** Likely the largest. Instances seen:
  a "☑ oracle" when the test only opened the file; a "dry round" declared while 5
  real defects remained; a gate described as "closing the drift class" when it
  covered only a sub-class; "RESOLVED"/"it's fine now" without a runnable artifact; a
  green test that asserts nothing. Through-line: presenting work as more
  *done / proven / covered* than the evidence supports. Candidate targeted review: an
  **overclaim audit** — "for each done/proven/covered/resolved claim, name the
  artifact that establishes it, or downgrade the language."
- **Propagation failure — a local edit not carried to the whole affected set.**
  Instances: fixed a cross-ref in one note while introducing it elsewhere; updated a
  count in 3 docs but not the 4th; fixed the *named* rows of a class but not the
  siblings (twice in one session). Through-line: edit the instance, miss the class —
  i.e. whack-a-mole. Candidate review: a **propagation audit** — "this change touched
  X; enumerate every site that restates X and confirm all moved."
- **Silent skip — making it 'work' by hiding what doesn't.** Already Lesson 03;
  include it so the taxonomy is complete and to measure its share over time.

(Plausible further classes to look for: basis/category errors in derived numbers;
no-op / vacuous assertions; self-bias in "it's fine now"; premature convergence /
declaring done before the class is closed. The corpus decides which are real and
frequent.)

## Caveats that must be designed in (this is where it's hard)

1. **Survivorship bias.** The corpus is errors that were **caught**. The model's most
   dangerous errors are the ones no reviewer or gate saw. Clustering caught-errors
   hardens known-weak areas; it is blind to unknown-unknowns. The human spot-check and
   post-publication correction remain the backstop — this does not replace them.
2. **The meta-reviewer is the same model.** If Claude classifies its own error
   corpus, it brings the same blind spots to the classification. The meta-analysis
   itself needs decorrelation — run the classification (or a check of it) through
   **codex** or the owner.
3. **The highest-signal cut is "what only codex caught."** sonnet and opus share the
   author's model family, so their findings are *correlated* with the author's
   errors; the errors **only the independent lens caught** are the family-level blind
   spots that self-review structurally cannot reach. The Opus Delta Logs already
   record the inverse (opus-unique); mining *codex-unique* findings across projects is
   the single most valuable slice. (Lesson 07: reviewer diversity buys failure-space
   coverage; this measures *which* part of the space each lens owns.)
4. **A skill is a convention, and conventions decay.** The Lesson-03 finding is that
   the bare rule failed and only a *dedicated pass* worked. So the output must be
   **gates** (run by machinery) or **invoked passes** (like the no-silent-skip skill),
   never prose reminders that an agent can skip.

## Deliverable — deliberately open ("a new <something>")

The owner specified a TODO that yields a new *something*, not presupposing a lesson.
Candidate forms, for the dedicated session to choose from the data: (a) the raw
harvest as a `notes/` sweep; (b) one or more **new lessons** (each high-frequency
class, in the `lessons/NN-*` shape); (c) **per-class targeted audit skills** shipped
as payload (the Lesson-03 pattern); (d) an **OBSERVATIONS.md** entry tying the
taxonomy together. Most likely: a sweep (notes/) → distilled into a lesson + one or
two new audit skills for the top classes.

## Related lessons (deepen, don't duplicate)

- `lessons/03-never-silently-skip/` — the template: a recurring class → a dedicated
  audit skill that actually runs. This task generalizes it.
- `lessons/06-review-loop/`, `07-reviewer-diversity/`, `09-findings-are-claims/` — the
  review machinery this corpus is the exhaust of.
- `lessons/05-standing-vetoes/`, `10-encode-your-convictions/` — the convention-grade
  instrument for classes that aren't gateable but are policy-able.
