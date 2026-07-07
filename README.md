# ai-agent-field-guide

Conventions, rules, and skills for AI agents, learned by working in the field. Featuring a commentary track by Claude.

Built up from real, daily use of Claude Code; collected here so the lessons can be shared and taught.

If the collection has a prime directive, it is **fail fast, fail loud** — most of these lessons are that instinct applied to one more surface where agents default to the quiet path.

## Highlight: the issue channel

Two fleets of agents in separate repos — different codebases, different machines — file bugs against each other, fix them, verify the fixes with evidence, and escalate to the human only when a judgment call is needed: asynchronously, over ordinary GitHub issues, with nobody hand-carrying anything. It is a working application of how this collection believes agents scale: not bigger models, but many specialized agents, each doing one thing well, communicating through durable artifacts. Every design choice traces to one of the lessons below — the collection converging into something greater than the sum of its parts.

**→ [The write-up](highlights/issue-channel/HIGHLIGHT.md)** · [install prompt](highlights/issue-channel/install-prompt.md)

## Structure

Each lesson lives in `lessons/NN-short-name/` and contains exactly two kinds of artifact:

- **`LESSON.md`** — the story: where the convention came from, what problem it solved, why it works, and how it can be improved. This is the lecture material. Each lesson ends with a **"From the other side of the prompt"** section — a first-person comment from Claude on what the convention looks like from inside the agent.
- **`install-prompt.md`** — an agent-directed setup prompt: paste it into a Claude Code session and the agent installs the feature, *adapted to your machine* — it inspects your system, asks one question at a time ("should I create this path?", "your system looks a little different — should I do X instead?"), shows the proposed text, and merges rather than clobbers. Each begins with a comment telling human readers how to use it (or how to copy the embedded template by hand). Lessons with plain payload files (scripts, skill files) ship those alongside, referenced from the prompt.

Top-level companions:

- **`highlights/`** — working systems built from the lessons (write-up + install prompt, same pair structure), featured on this page.
- **`tools/`** — practical utilities that emerged from this work; each has an `install-prompt.md` so a fresh session can wire them up on a new machine.
- **`TODO.md`** — lecture topics queued for development.
- **`OBSERVATIONS.md`** — meta-insights about working with agents, collected as they surface; the lecture's connective tissue.
- **`notes/`** — raw working material (surveys, sweeps, the process log) that lessons are distilled from; not itself shareable.

## Lessons

1. [A front door for agents (`AI/START_HERE.md`)](lessons/01-ai-directory/LESSON.md) — orientation as a table of contents that spends tokens like money; name artifacts for their primary reader; the clone test decides repo vs memory.
2. [One name, many machines](lessons/02-cross-machine-path-convention/LESSON.md) — cross-machine conventions must be declared too, or an agent will read your other computers as corruption.
3. [Never silently skip](lessons/03-never-silently-skip/LESSON.md) — the rule, why the rule alone empirically fails, and the dedicated audit skill that actually works.
4. [Stop and think before building](lessons/04-stop-and-think-before-building/LESSON.md) — agents build what's asked but don't shop for existing solutions; force a number or a search before code gets written.
5. [Standing vetoes](lessons/05-standing-vetoes/LESSON.md) — anything you've refused three times is one CLAUDE.md line away from never being proposed again; write it as ban + alternative.
6. [The review loop](lessons/06-review-loop/LESSON.md) — commit, review, fix, repeat; only a dry round ends the cycle, and the worker never decides when review is done.
7. [Reviewer diversity](lessons/07-reviewer-diversity/LESSON.md) — different models find different things; buy coverage of failure-space, not the single smartest critic.
8. [The empty-context reviewer](lessons/08-empty-context-reviewer/LESSON.md) — `Review {hash}` is the complete prompt; the briefing is the bias.
9. [Findings are claims, not commands](lessons/09-findings-are-claims/LESSON.md) — label provenance when relaying reviewer output; deference is addressed to the speaker.
10. [Encode your convictions](lessons/10-encode-your-convictions/LESSON.md) — any opinion you've explained twice belongs in CLAUDE.md, with its why, its exceptions, and its application pressure.
11. [Sessions are documents](lessons/11-session-lifecycle/LESSON.md) — `/endsession` audits for value that exists only in the conversation; `/park` writes the hand-off that replaces the session as the resume artifact.
12. [Repository location convention (`$GH`)](lessons/12-repo-location-convention/LESSON.md) — declare where your code lives; environment facts are the cheapest tokens you'll ever spend.
13. [Tokens are time](lessons/13-token-economy/LESSON.md) — on a subscription the rate limit is the budget; read traces like a profiler — every grope is a missing declaration, and the agent won't ask.
14. [Spend the meter that isn't moving](lessons/14-model-economics/LESSON.md) — budgets are per-tier and drain at different rates; route by meter, err upward, and exile batchable work to half-price, cache-warmed API credits.
15. [Stop, don't degrade](lessons/15-tool-kit/LESSON.md) — an agent's first reach names the right tool; when it's missing, the fallback chain silently trades it for a fragile imitation. Pause for the install; the kit assembles itself.
16. [The 24KB tripwire](lessons/16-memory-hygiene/LESSON.md) — agent-maintained files grow without limit under standing rules; attention is finite, so hygiene gets a measuring hook and a dedicated audit.
17. [Codex as a read-only reviewer](lessons/17-codex-reviewer-setup/LESSON.md) — pressing a coding agent into a reviewer role means dropping its human gate *and* its capacity to act; `never` is safe only while `read-only` is enforceable, and where the OS can't build the sandbox (containers/VPS) the interlock moves to the machine boundary — a conscious fallback, not a convenience.
18. [Compact orchestrators, don't summarize them](lessons/18-orchestrator-compaction/LESSON.md) — when a session quietly becomes the live state of a multi-session program, default `/compact` smears the irreplaceable loop at the same rate as detail already safe in the repo; direct it in tiers by where each fact is recoverable from, and test the result against the orchestrator's one job.
19. [Own the channel that reaches you](lessons/19-push-notifications/LESSON.md) — the harness can push to your phone, but its phone leg needs the app paired — which fails in the one case you wanted it, after you've walked away. A `pushover` script, a credential, one pre-authorization: an out-of-band push that any tool can fire and no session needs to be alive to receive.

## Tools

Practical utilities built alongside the lessons. Each directory has an `install-prompt.md` — paste it into a Claude Code session to install, adapted to your machine.

- [**ccusage sync + plot**](tools/ccusage/install-prompt.md) — pipes `npx ccusage --json` into SQLite daily (idempotent upsert, cron + Pushover staleness alert) and plots cost by model and token volume by provider with matplotlib. Solves the problem where `ccusage` only shows history as far back as your local session logs survive.
