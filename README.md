# claude-wisdom

Conventions, rules, and skills for AI agents, learned by working in the field. Featuring a commentary track by Claude.

Built up from real, daily use of Claude Code; collected here so the lessons can be shared and taught.

## Structure

Each lesson lives in `lessons/NN-short-name/` and contains exactly two kinds of artifact:

- **`LESSON.md`** — the story: where the convention came from, what problem it solved, why it works, and how it can be improved. This is the lecture material. Each lesson ends with a **"From the other side of the prompt"** section — a first-person comment from Claude on what the convention looks like from inside the agent.
- **`install-prompt.md`** — an agent-directed setup prompt: paste it into a Claude Code session and the agent installs the feature, *adapted to your machine* — it inspects your system, asks one question at a time ("should I create this path?", "your system looks a little different — should I do X instead?"), shows the proposed text, and merges rather than clobbers. Each begins with a comment telling human readers how to use it (or how to copy the embedded template by hand). Lessons with plain payload files (scripts, skill files) ship those alongside, referenced from the prompt.

Top-level companions:

- **`TODO.md`** — lecture topics queued for development.
- **`OBSERVATIONS.md`** — meta-insights about working with agents, collected as they surface; the lecture's connective tissue.
- **`notes/`** — raw working material (surveys, sweeps, the process log) that lessons are distilled from; not itself shareable.

## Lessons

1. [Repository location convention (`$GH`)](lessons/01-repo-location-convention/LESSON.md) — declare where your code lives; environment facts are the cheapest tokens you'll ever spend.
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
