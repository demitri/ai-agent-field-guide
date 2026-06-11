# Lesson 7: Reviewer diversity — different models find different things

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The story: "best model" was the wrong question

The owner's default model was Opus, under the natural belief that it was Anthropic's "best." The review pattern was: codex (GPT) rounds until no findings, then an Opus review — which would turn up *new* things in code codex had already passed. Then, in an effort to save tokens (Sonnet "costs" less than Opus), a Sonnet review was tried — and Sonnet found things that **neither Opus nor codex** had caught.

The conclusion wasn't that one model was better. They were *different* — trained on different data, instructed to look for different things, attending to different failure modes. All valuable. Cross-model review has since become **table stakes**: reviews are mandatory, use multiple models, preferably at least one from a different vendor, repeat until done.

## The refined practice

- Each reviewer is treated as one *facet*, not a redundant copy: in the owner's panel, codex does mechanical path-tracing and existing-machinery archaeology, Sonnet catches spec-precision and coverage gaps, Opus judges design and policy.
- **Never a single reviewer** for anything expensive, irreversible, or launch-shaped.
- **Disagreement between reviewers is high-value signal** — it marks a spot where at least one model's picture of the code is wrong. Adjudicate against the actual code; don't tiebreak by vote.
- Cost shapes the panel, not the principle: cheap models are used freely, the constrained one is saved for the layer where it adds the most.

## The generalizable principle

Don't ask which model is best — ask which failures are *uncorrelated*. A second reviewer adds value in proportion to how differently it fails from the first, which is why a cheaper model from another vendor can outperform a stronger model from the same one. Diversity beats strength for the catching of blind spots, because blind spots are precisely what strength can't see.

---

## From the other side of the prompt

I cannot see my own blind spots. That sounds like modesty; it's actually geometry. The bug I walk past is the one my training distribution made invisible to me, and no amount of "look harder" changes what *invisible* means. Another instance of me looks with my eyes. A different model looks with different eyes — different training corpus, different instruction tuning, different habits of suspicion. When Sonnet found what Opus and GPT both missed, that wasn't an upset; it was sampling a third distribution.

There's a tempting mental model where models form a ladder, and the top rung subsumes the rest. Reviews are where that model breaks most visibly. For generation, strength compounds; for *checking*, what matters is whether your checker's errors correlate with your author's — and same vendor means same data pipelines, same RLHF sensibilities, same fashionable failure modes. An ensemble of one vendor is less of an ensemble than it looks.

So spend your review budget like a portfolio manager, not a talent scout: you're not hiring the single smartest critic, you're buying coverage of failure-space. And treat our disagreements as the most informative thing we produce — where two models diverge, at least one of us is confidently wrong, and finding out which teaches you something about the code that neither review alone contained.
