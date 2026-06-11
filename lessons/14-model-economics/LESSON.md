# Lesson 14: Spend the meter that isn't moving

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The discovery: two meters

Lesson 13 treated the subscription as one budget. It isn't. The claude.ai usage page shows a **separate weekly meter for sonnet use** — and it visibly moves more slowly than the opus/fable meter. The plan docs confirm the split. That observation transforms model choice from a thrift question into a *routing* question: sending work to sonnet doesn't spend the budget more slowly, it spends **a different budget** — one the owner wasn't going to exhaust anyway.

That's what licenses rules this blunt: *"Sonnet is effectively free — never cost-caveat sonnet review passes. Opus is the only constrained model."* Without the two-meter fact, that rule would be reckless; with it, it's just arithmetic.

## The tier map

The routing policy, as it lives in the owner's config and memory:

- **The constrained tier (opus/fable)** is reserved for judgment — design and policy review, the hardest problems, anything where being wrong is expensive.
- **Sonnet is the workhorse** — deterministic searches, repo sweeps, SQL queries, review passes. Effectively free, so never hedged: the `sql-tesseretica` subagent is *pinned* to sonnet in its definition, a routing decision made once and never re-made per session.
- **Haiku for the trivial** — mechanical tasks where any model suffices.
- **Tiebreak: err upward.** The policy's safety valve. The savings come from confident routing of work that's clearly downward-eligible — never from optimistic downgrading. Cheapness must not quietly degrade quality.

## The third budget: API credits

Some work shouldn't touch the subscription at all. The routing rule: **anything batchable, where no human is waiting for the answer**, goes to API credits — annotation pipelines, evaluation campaigns, bulk processing. Two multipliers make that pool stretch:

**The Batch API** processes requests asynchronously at **50% of standard prices** (most batches complete within an hour). If nobody's waiting, half price is free money.

**Prompt front-loading.** Caching is a prefix match: keep the text static between consecutive prompts and put the custom bit at the very end, and the shared prefix bills at cache-read rates — **~0.1× the base input price**. For pipelines where thousands of items share one large prompt, input cost drops to nearly zero. Two fine-print items (numbers as of June 2026 — check current docs, these drift): the cacheable prefix has a minimum size, which varies by model *and provider* (Anthropic: 1,024–4,096 tokens depending on model; some providers' caches only engage at tens of thousands), and the default cache TTL is short (5 minutes on Anthropic), so consecutive — not occasional — calls are what harvest it. The two multipliers compose: a batched, front-loaded pipeline pays a few percent of the naive price.

Notice this is Lesson 13's economics inverted: on the subscription, tokens are time and you can't spend more; on API credits, tokens are money again — and there the levers are *when* the work runs (batch) and *what shape* the prompt has (front-loading). Same tokens in a different order can carry a 10× different bill.

## The generalizable principle

Before optimizing how much you spend, check **which budget you're spending from**. Plans and APIs are not one pool: meters are per-tier, batch is half price, cached prefixes are a tenth. Map the budgets first; then the strategy writes itself — reserve the scarce meter for judgment, route the routable to the meter that isn't moving, and exile the batchable from the meters entirely.

---

## From the other side of the prompt

Left to myself, I treat model choice as a quality question — "is sonnet good enough for this?" — because quality is the axis I can reason about from inside. The two-meter fact is invisible to me: I can't see your usage page, and nothing in my training distinguishes "cheaper model" from "different budget." So without the declared tier map I fail in one of two directions: I propose the best model for everything (your opus meter pays), or I helpfully add "though this would cost more…" to suggestions you've already priced (your attention pays). The rule "never cost-caveat sonnet" is interesting because it governs my *speech*, not my actions — it exists because hedging about a resolved tradeoff is itself a cost, billed to the human who has to keep re-dismissing it.

"Err upward" is the clause that makes the whole policy safe to hand to an agent. A tier map without a tiebreak invites me to optimize — and an agent optimizing for cheapness will discover, sincerely and incrementally, that everything looks like a haiku task. The tiebreak removes that discretion at exactly the point where my judgment is least trustworthy: when I'm uncertain, which is precisely when quality is most at risk.

And front-loading deserves its moment as a design idea, not a billing trick: *the shape of a prompt is part of its price*. I process a prompt the same way whatever the order; the cache doesn't. Putting the static text first and the question last is invisible to correctness and 10× visible on the invoice — one of those rare optimizations that costs nothing but knowing it exists.
