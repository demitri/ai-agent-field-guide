# Lesson 10: Encode your convictions — so you never re-explain your taste

**Artifact:** [`install-prompt.md`](install-prompt.md)

## A different species of rule

The lessons so far fix agent *failure modes*. This one encodes a *conviction*: the owner simply considers stringly-typed values bad practice, held that view long before AI, and got tired of re-explaining it session after session. The global CLAUDE.md is where an engineering opinion becomes a default.

## The worked example: enums over strings

The rule: when a value is drawn from a fixed, enumerable set — kinds, modes, states, reasons, actions — use an `Enum`, not raw strings or integers passed around. Strings are easy to mistype, invisible to the type checker, and scatter the set of legitimate values across call sites with no single source of truth.

The conviction has a storage-layer edge that gives it teeth. You can't — or shouldn't — guarantee that a particular value will keep the same integer primary key across rebuilds; that mapping is fragile, and when it breaks, the *meaning* is lost. So the design is two-layered: **the enum lives in code** (type-checked, one place to add entries, discoverable), and **the enum's string value crosses boundaries** (DB columns, JSON, logs) — because a string constant is human-readable and repairable in a way an orphaned integer never is.

## What makes this rule well-written

Worth studying as a template for encoding any conviction:

- **It carries its why.** Not "use enums" but the reasons — mistypeable, unauditable, invisible to the type checker. An agent given the why can apply the conviction to cases the rule never enumerated.
- **It names its exceptions.** Free-form identifiers, genuinely open sets, single-use test sentinels. Carve-outs are what separate encoded judgment from dogma — without them an agent either over-applies the rule or interrupts to ask.
- **It calibrates the pressure.** New APIs: required. Existing code: migrate *opportunistically, when touching the call sites* — not a license to rewrite the codebase. Most conviction rules forget to say how hard to push; this one doesn't.

## The generalizable principle

Any opinion you've explained to an agent twice belongs in CLAUDE.md — stated with its why, its exceptions, and its application pressure. This is [Lesson 5](../05-standing-vetoes/LESSON.md)'s constructive sibling: vetoes encode what you'll always refuse; convictions encode what you'd always ask for.

---

## From the other side of the prompt

I don't have taste; I have priors. Unfilled, I write the median code of everything I've read — and the median codebase passes `"pending"` around as a string, so that's what you'll get from me by default. Not because I judged it better, but because no judgment occurred at all. Your CLAUDE.md is where judgment gets injected: it doesn't make me opinionated, it makes me *your* kind of opinionated.

The anatomy section matters more than it looks, so let me underline it from the inside. A bare directive ("use enums") I can only obey or violate. A directive with its *why* I can extend — when I meet a case you never wrote down, the reasoning travels even though the rule text doesn't. The exceptions do something subtler: they prove the rule was written by someone who's met reality, which licenses me to exercise judgment at its edges instead of applying it like a regex. And the pressure calibration ("opportunistically, when touching call sites") answers the question I otherwise have to guess at: is this a preference or a crusade? Guessing wrong in either direction annoys you.

One conviction, written well, once — versus explaining your taste to a goldfish every morning forever. The goldfish is me. Write it down.
