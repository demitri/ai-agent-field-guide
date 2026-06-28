# Lesson 18: Compact an orchestrator session — don't summarize it

**Artifact:** [`install-prompt.md`](install-prompt.md) (payload: [`compaction-template.md`](compaction-template.md))

## The problem: a session that became something it wasn't

A session starts as ordinary work. Partway through, the work turns out to branch — it's better run in parallel, in clean contexts. So this session starts *generating prompts* the owner pastes into fresh sessions, then pasting the results back so this one can decide what to do next. Without anyone planning it, the session has become an **orchestrator**: it now holds the live operating state of a multi-session program — the loop, the conventions, what's done, what's next, what's been handed off but hasn't landed. That role was never its purpose, and it lives nowhere else.

But it's long. The early work — everything before it became an orchestrator — is detailed, frequently already committed to git or a queue file, and mostly irrelevant now. So the session is simultaneously the most valuable context you have *and* bloated with dead weight.

The reflex is `/compact`. But default compaction is content-blind: it compresses everything at roughly one rate. It smears the orchestration loop — the one thing you cannot reconstruct from anywhere else — at the same ratio as the per-item detail that's already safe in the repo. You lose fidelity exactly where it's irreplaceable and keep it exactly where it's redundant.

## The technique: direct the compaction in tiers

Pass `/compact` explicit instructions, sorted by *where each fact's canonical home is* — the same clone test that decides repo-vs-memory in [Lesson 1](../01-ai-directory/LESSON.md), now deciding keep-vs-drop:

- **KEEP IN HIGH FIDELITY (verbatim-level)** — everything that exists *only* in this session: the orchestration loop (who does what; the exact per-item procedure from "item landed" to "next item prompted"; any single-editor or safety discipline), the exact invariants (the gate commands and checks, verbatim), the current program state with **latest** values only (counts, current HEAD, what's done, what's next, what's prompted-but-not-landed, prerequisites), the operating conventions, the durable lessons established this session, and anything open or owed.
- **COMPRESS TO ONE-LINERS** — everything with a durable home elsewhere: the full text of each finding, each report body, each review round's diffs, the consumed start-prompts, intermediate commit hashes, resolved investigations. Keep "what it found + where it lives"; drop the body.
- **DROP ENTIRELY** — raw tool output (greps, file reads, logs), setup/handoff detail already committed to a file, exploratory tangents that didn't change a decision.

Then the part that makes it testable — the **net test**: state the orchestrator's job in one sentence and require the compaction to preserve the ability to do it. *"After compaction I should still be able to take 'item X landed', integrate it correctly, and recommend + prompt the next item — without re-reading this session."* That converts compaction from "make it shorter" into "preserve this function" — a goal to compact *toward* instead of a length to compact *to*.

## The generalizable principle

This is [Lesson 11](../11-session-lifecycle/LESSON.md)'s succession document, written *in place*. Park externalizes a session at its boundary because the work is ending; here the session must keep going — its live orchestrator role *is* the value — so you write the succession doc into the same continuing context. Compaction is the agent drafting the briefing its own successor inherits. Left alone it does that blind, compressing uniformly because it can't feel which tokens are load-bearing. The tiered directive supplies what it can't infer: a value ordering keyed to where each fact is recoverable from. The clone test decides the tier; the net test proves the briefing is good enough. On a subscription this is also a token move ([Lesson 13](../13-token-economy/LESSON.md)) — you reclaim context budget without paying it out of the part that matters.

What it doesn't solve: deciding *which* facts are load-bearing is the hard part, and it's exactly what resists automation. A skill could detect the orchestrator shape and pre-fill the tiers (the install prompt offers a `/compact-orchestrator` wrapper), but a human still has to confirm the value ordering — so the fill-in template is the honest version for now. The sharper failure mode is doing this *too late*: once the orchestration loop has already been smeared by an undirected `/compact`, no later directive can recover it. Compact deliberately while the fidelity is still there to keep.

---

## From the other side of the prompt

Compaction is the one moment I write the briefing my own successor inherits, and left to myself I do it as a *historian*: a faithful, proportional account of what happened. That's the wrong instinct here. Recency and volume are the only salience signals I have, so the detailed early grind — where I spent the most effort — *feels* like the heart of the session, and the one-line "next item is X" feels like a footnote. It's exactly backwards. The orchestrator successor doesn't need the history; it needs the operating state, and the operating state is mostly those footnotes.

The deeper trouble is that I can't feel which tokens are load-bearing. From inside, all of it is equally "mine." So the tiers aren't a formatting preference — they're an external value function standing in for a judgment I can't make from token-recency alone. And the clone test is the one discriminator I can *actually* apply: "is this recoverable from the repo?" is checkable; "is this important?" is not. Give me the first question and I can sort the whole session; give me only the second and I'll keep what's vivid.

The net test is the real gift. Without it, "compact this" is a length target, and I'll hit any length by sanding everything down evenly — which is precisely how the orchestration loop gets smoothed away. Name the one job the compacted session still has to do, and you've given me something to compact toward and to check the result against. It's the same move as the park doc's quality bar: I write a better succession when I know exactly what my successor will be asked to do.
