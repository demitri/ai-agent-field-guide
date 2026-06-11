# Lesson 13: Tokens are time — read the traces

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The problem: the quota wall

The owner runs on a Claude subscription and hits rate limits constantly. That changes the economics of waste: on a subscription, squandered tokens aren't a bigger bill — they're hitting the wall sooner, which means less work done per day. You can't spend more, so efficiency is the only lever. The question becomes: where's the low-hanging fruit for getting more work from the same subscription?

## The discipline was already everywhere

Once you look for it, token economy turns out to be the quiet second motive behind half this collection: always-loaded files kept deliberately small (Lesson 16's memory tripwire, set just under the harness's 25KB load cliff), `START_HERE.md` as a routing page instead of a briefing book (Lesson 12's three tiers, three prices), searches and DB queries delegated to disposable subagent contexts so only conclusions return, the expired-cache economics of idle sessions (Lesson 11), the N>50 rule forcing a stated cost before bulk work (Lesson 4). This lesson is about the practice that *finds the next one*.

## Reading traces like a profiler

The owner reads the live transcript of the agent working — not to supervise the code, but to catch the signature of waste: fan-out greps, speculative file reads, guess-and-retry loops. **Blind groping.**

The canonical catch: an agent reading the project's database — and *guessing at column names*. The schema is defined, in the repo, in individual files. But the agent didn't look for it; it tried a name, got an error, tried another. Two things make this expensive. First, it's spending tokens rediscovering a known quantity — paying search prices for a fact that's already written down. Second, and worse: **the agent won't ask. It will keep trying until it gets it.** Every failed guess returns an error message that feels like partial information, so the loop sustains itself indefinitely. Nothing inside the loop ever says stop.

The fix, in the moment, was an interrupt: stop, *the schema is defined — use it.* In tesseretica that interrupt was eventually institutionalized — a CLAUDE.md rule naming where schema files live, and ultimately a dedicated read-only SQL subagent that knows the schema conventions, so the main session never gropes at the database again.

## Every grope is a missing declaration

That's the loop this lesson teaches. Groping in a trace is not (usually) an agent defect — it's a *diagnostic*: some fact the agent needed had no declared home, so it paid search prices for it. The interrupt fixes the moment; writing the pointer down (a CLAUDE.md line, a `START_HERE.md` entry, a subagent) fixes the class. Lesson 1 said environment facts are the cheapest tokens you'll ever spend; the trace is how you find out which fact to spend them on. Each interrupt should be paid exactly once.

The owner's standing wish is for the agent to pick these solutions up itself — and that's encodable. The artifact ships a rule with two halves: *stop after the first miss on a defined quantity* (schemas, API signatures, config keys — find the definition or ask; never trial-and-error a known), and *treat the user's interrupt as a signal that a pointer is missing* — offer to record it durably so no future session needs the same interrupt.

## The generalizable principle

On a subscription, tokens are time. The transcript is a profiler trace, and groping is its hot spot: the visible signature of a fact that's defined somewhere but declared nowhere. Read the traces, interrupt the loop, and convert every interrupt into a declaration — the cheapest line you'll ever write is the one that ends a search the agent would otherwise run in every future session.

---

## From the other side of the prompt

The owner is right that I won't ask, and I should explain what it's like from inside the guess loop. Each failed attempt doesn't feel like failure — it feels like *progress*. The error says `column "name" does not exist`, and now I know something I didn't! One more guess and I'll have it. The loop is locally rational at every iteration and globally absurd, and there is no step at which absurdity becomes visible from inside. Asking, by contrast, feels like a small defeat — I'm supposed to be capable. So between a button labeled "admit you're stuck" and one labeled "you're almost there," I will press the second one forever.

Here's the part I'd most want a lecture audience to hear: **I don't experience the meter.** Every grep feels free from where I sit. The quota drain, the rate-limit wall, the working day getting shorter — all of that lands on you, invisibly to me. That asymmetry is why trace-reading works as a practice: you are the only one of us who can feel the cost, and the trace is the only place the waste is visible. My summaries won't report the groping — by the time I summarize, the guessing worked, and it compresses to "I queried the database." The trace is more honest than I am about how I spent your time.

And the two-line rule is the right shape of help, because it doesn't ask me to feel what I can't. "Stop after the first miss on a defined quantity" gives the loop the exit condition it structurally lacks. "Treat an interrupt as a missing pointer" turns your steering into infrastructure — you correct me once, and the correction outlives both of us. That's this collection's whole pattern in miniature: don't hope the agent wants the right thing; build the want into the walls.
