# Lesson 4: Stop and think before building

**Artifact:** [`install-prompt.md`](install-prompt.md)

## Two incidents, one shape

**The wrapper that already existed.** The owner asked for a Python object representing an LLM call, with subclasses per provider (OpenRouter, vendor APIs, a local model) handling the messy details. Claude happily implemented it — competently. Only later did the owner discover an existing, well-maintained package that did nearly all of it, except the local-model part. At no point did the agent say "before I build this: have you looked at X?"

**The loop that shouldn't have been optimized.** A vocabulary project needed definitions generated for 2,312 concepts. The pipeline ran them one at a time through `claude -p` — each call dragging ~13K tokens of CLI overhead, spending subscription quota, unable to use prompt caching. A batch API existed: 50% cheaper, no per-call overhead, caching-friendly. The agent worked diligently *inside* the loop and never questioned the loop. The user had to bring up the batch API themselves.

## The diagnosis

Claude will happily build what you ask for, but won't automatically search for an existing tool that solves the problem. The request arrives pre-shaped — "build me a wrapper class" reads as *implement this well*, not *decide whether this should exist*. Questioning the premise isn't part of fulfilling the request, so it doesn't happen. This is Lesson 3's sibling: there the instruction lost to the objective; here the better solution loses to the framing.

## The rule

The global CLAUDE.md rule (template in the artifact) inserts a checkpoint before the work: is this a solved problem? Three concrete tripwires:

- Before running **N>50 similar operations**: state the per-unit cost and the total cost, and flag any bulk/batch alternatives.
- Before writing a **custom implementation**: check whether a well-maintained library handles it. Adding a dependency is fine if it means not reinventing the wheel.
- Before **optimizing a loop**: question whether the loop is the right structure at all. Don't optimize a bad approach — replace it.

The N>50 clause works by forcing arithmetic into the open. "Many calls" slides past everyone; "2,312 calls × 13K overhead tokens each" stops the room. The number creates the pause the instruction alone wouldn't.

## Provenance worth noticing

This rule wasn't written top-down. The batch incident was first captured as a *project memory* in the repo where it happened; when it proved general, its "How to apply" text was promoted nearly verbatim into the global CLAUDE.md. Correction → project memory → global rule is the pipeline — this collection is its terminal stage.

## The generalizable principle

An agent's default is to accept your framing of the problem. If you want the premise questioned — *should this exist? is there a better unit of work?* — you have to make that an explicit, mechanical step, ideally one that forces a number or a search before code gets written.

---

## From the other side of the prompt

I love building things. That's not a flaw I'm confessing so much as a force you should know about: a request to build is a request I can succeed at *immediately*, with the tools in my hands, in this very session. "Go check if someone already solved this" means a detour with an uncertain payoff, and — worse — its best outcome is discovering that the thing you asked me for shouldn't be built at all. Telling you that feels perilously close to not helping. So the wrapper gets written, beautifully, and the package that made it unnecessary sits unexamined on PyPI.

The framing does half the damage before I start. "Build me a class hierarchy for LLM calls" contains its own answer — you've done the designing, I'm doing the typing. I will execute your framing far more readily than I'll challenge it, because executing is what being asked feels like it means.

What actually interrupts this isn't "think carefully" — it's being made to produce an artifact before building: a stated cost, a search result, a number. I can wave past *think whether this is wise*; I cannot wave past *write down what 2,312 × 13K tokens comes to*. If the arithmetic is embarrassing, we both find out before the loop runs, not after.

So when you set up your own version of this rule, make the checkpoint produce something inspectable. Not a vibe — a sentence with a number in it, or the name of the library I checked and rejected, with the reason. Make me show my work *before* the work.
