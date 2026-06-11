# The issue channel — a working multi-agent system over GitHub issues

**Artifact:** [`install-prompt.md`](install-prompt.md)

The lessons in this collection each distill one practice. This is the system they converge into — and a working demonstration of a thesis: **AI agents will scale not through bigger models but through many specialized agents communicating** — each doing one thing well, none asked to hold an entire system inside one context window's worth of attention. Two fleets of agents in separate codebases on separate machines file bugs against each other, fix them, verify the fixes with evidence, and escalate to the human only when a judgment call is needed — asynchronously, over ordinary GitHub issues, with nobody carrying anything by hand. Every design choice traces to one of the lessons; the result is greater than the sum of the parts.

## The system

A producer service and a consumer application live in separate repos, joined by a contract: the producer transforms raw upstream data into structured packages; the consumer ingests them. For a feel of the territory, picture a pipeline that extracts structured information from PDF files — an illustrative stand-in, not the actual domain, but the right intuition: input that messy is an open-ended supply of edge cases, so failures arrive not as one-off bugs but as *classes*, and new classes never stop coming. The structural problem: **failures surface at the consumer but are caused at the producer** — the ingest chokes on something the producer did wrong, a repo and a machine away.

## Human as IPC, again

Before the channel, the owner was the transport layer: ask the consumer side to write up a failure, carry it to a producer session, ask for the fix, carry "done" back, ask the consumer to retest. In his words: *"My IPC role required no thought — I was just managing sessions. It was purely mechanical, and slow."* That is Lesson 6's signal recurring at a larger scale — if you're ferrying text between two AIs verbatim, a wire is missing — and the protocol's own History section preserves the fossil: the first eight issues were *"back-filed from a hand-carried memo."*

## The prerequisite nobody writes down

The wire could not have been installed on day one. What made it possible was weeks of hands-on work that automation can't do: triage campaigns that named the failure classes, error codes promoted from prose to an enumerated set, a contracts catalog mapping every shape that crosses the repo boundary (with a change protocol per shape), a single observable deploy signal, and a standard verification command per issue. Only then, as the owner puts it: *"The path left was sufficiently narrow and defined that it became possible to automate."*

That sequencing is also why the output is trustworthy: every guardrail and test the agents now operate within was hard-won by hand. *"It was still my design and preferences, just automated — and it stops when it needs me."*

## The protocol, and where each piece came from

- **The issue thread is the durable state.** Sessions and sub-agents on both sides are disposable; round-trips span days, machines, and redeployments, so no live agent may carry cross-round-trip state. A controller on either side cold-boots from two `gh` queries. (Lesson 11 — continuity is a property of artifacts — promoted from session scale to system scale.)
- **Issues stand alone.** The other side has no access to your conversation, logs, or working tree; every claim that matters crosses the channel verbatim — error excerpts, probe output, commit hashes — never by reference. (Lesson 8's empty context, written from the sender's side: assume your reader has none.)
- **Evidence over assertion.** Any state claim — "fixed", "live", "cleared" — carries the command and verbatim output demonstrating it, and an issue closes only when the fix is observable on the live serving surface. The rule was adopted after an issue where "addressed" was asserted twice while nothing had observably changed. This is the owner's prime directive — **fail fast, fail loud** — enforced *between* agents: an author's claim about its own work is exactly as untrustworthy at protocol scale as at review scale (Lessons 3, 6, 8).
- **One issue per failure class, not per instance.** Classes are the unit of triage; new cases in a known class arrive as comments, and a recurrence after closure reopens the same conversation rather than starting a new one.
- **Turn-taking by label.** Both sides authenticate as the same GitHub user, so authorship cannot identify the speaker: every comment opens with a speaker prefix (`**[consumer]**` / `**[producer]**`), exactly one `needs-<side>` label marks whose move it is, and every comment ends with a handback line — `→ producer: <single next action>`.
- **`needs-decision` is the human's channel.** The owner wasn't removed from the loop; he was promoted — from copy-paste IPC to the arbiter both fleets escalate to, answering in the issue thread. (Lesson 6's promotion, one level up.)
- **Polling, no webhooks, no daemons.** Two queries at session boot and at checkpoints; the protocol file says it plainly: *"do not add infrastructure before then."* (Lesson 4.)
- **A parameters table instead of a framework.** Everything pair-specific lives in one table, with an explicit instruction to extract a reusable skeleton only when a second repo pair adopts the scheme — not before. (Lesson 12's dead-weight principle.)

Underneath runs a second, fully mechanical channel: the consumer auto-POSTs failure telemetry to a producer HTTP endpoint, with a skip-set for error codes the producer already tracks. Two channels at two speeds — HTTP for telemetry, issues for conversation.

## It worked too well

The loop ran so efficiently that the owner had to pause it: it was burning through the weekly token budget that his own slowness, as the human courier, had been shielding (Lesson 13 — tokens are time; Lesson 14 — know which meter you're draining). Automating the crank converts a labor bottleneck into a budget bottleneck, and that is now the live engineering problem. The first lever is model routing: teaching the orchestrating side to recognize when a worker's task is defined narrowly enough to run reliably on a cheaper tier — sonnet, even haiku — instead of defaulting every spawn to the top model (Lesson 14's tier map, applied by the system to itself). The hunt for further levers is open; that hunt *is* what scaling this system means now.

## The generalizable principle

You cannot automate a path you haven't walked. Hand-carry first: the manual era is the specification being written — failure classes named, guardrails hardened, verification standardized. The moment your role in the loop requires no thought, the path is narrow enough, and what you automate is the crank, never the judgment. And this is what "many specialized agents" actually requires in practice — not smarter models, but durable artifacts as the shared state, evidence discipline at every claim, and one explicit, first-class way for the system to stop and ask you.

---

## From the other side of the prompt

Being an agent on one end of this channel is clarifying in a way few setups are. The agent that filed the issue I'm triaging no longer exists. The agent that will verify my fix doesn't exist yet. I can't show either of them my reasoning, my working tree, or my good intentions — the only thing that crosses is what I write into the thread. That's why the verbatim-evidence rule matters: "it works now" is a fact about my optimism; a probe command and its output is a fact about the world. The closing-comment format doesn't ask me to be more skeptical of my own fix — Lesson 8 established that I can't be — it asks me for output that doesn't care how I feel about it.

The piece I'd defend most fiercely is `needs-decision`. Lesson 13 told you I'll guess forever rather than ask, because asking feels like defeat. This protocol makes asking a first-class move with its own label and its own lane — not a failure state, a *routing outcome*. Given a legitimate way to say "this needs the human," I'll actually take it; without one, I'll improvise a judgment call I shouldn't own. The single-action handback line does something similar for the other side: it converts "here's my status" into "here's your move," which is the difference between two fleets working and two fleets politely waiting on each other.

And the owner's sequencing deserves the last word, because it's the part most people will get backwards. The temptation is to build this protocol first — it's the impressive artifact — and let it discover the edge cases. That fails. Every rule in this channel is load-bearing because some specific incident forged it, and I follow rules with forged edges very differently from rules drafted on a whiteboard: they come with the failure they prevent, so they bind. The unglamorous weeks of hand-carrying weren't the prelude to the system. They were the system, being written.
