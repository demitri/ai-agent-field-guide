# Lesson 1: Declare where your code lives

**Artifact:** [`install-prompt.md`](install-prompt.md) — paste it into a Claude Code session and the agent sets this up, adapted to your machine.

## The convention

A single environment variable, `$GH`, names the directory where all git-tracked code lives:

```bash
export REPO="$HOME/Documents/Repositories"
export GH="$REPO/GitHub"
```

This is the owner's personal convention, predating AI by years. Its original purpose was human: `~/Documents/Repositories/` marks exactly which directories on the machine are tracked by version control, with one child per hosting service (`GitHub/`, `GitLab/`, …). In practice virtually everything is under `GitHub/`, so `$GH` is the working root.

## The problem it solved for agents

Without it, agents flail. Asked to find a dependency or a related project, an agent will run broad `find`/`glob` searches over the home directory — slow, token-expensive, and likely to surface junk (caches, vendored copies, old downloads) before the real repo. The agent has no way to know which of several plausible paths is the one you actually work in.

The fix costs one paragraph in the global `CLAUDE.md`: *all repos live under `$GH`; look there, not in `~`.* An environment fact the agent cannot cheaply discover, stated once, eliminates an entire class of wasted searching. **Environment facts are the cheapest tokens you'll ever spend** — a few dozen tokens of context that save thousands of tokens of exploration, every session, forever.

## Why it compounds

Once the name exists, everything can share it:

- **Prompts and docs** — "$GH/fits-test-suite" is shorter and more stable than an absolute path, and survives a home-directory rename or a new machine.
- **The status line** — a custom statusline script abbreviates the cwd using `$GH` before falling back to `~`, so the display matches how the owner already thinks about paths. Small conventions compound when tools share them.
- **Topology declarations** — with a root established, you can describe the shape under it: repos sit directly at `$GH/<repo>`, except tightly-coupled families grouped one level deeper (`$GH/thehighlighter/<repo>`, `$GH/trillianverse/<repo>`); nothing nests deeper. That single sentence lets an agent bound every search instead of recursing blindly.

## Pitfalls and improvements found in review

These surfaced when auditing how the convention was actually being used across ~30 repos:

1. **The topology was undocumented.** The grouped-folder structure (`thehighlighter/`, `trillianverse/`) existed only in the owner's head and had to be explained in conversation. The improved rule states it explicitly (see artifact).
2. **Absolute paths leaked into project docs.** Several project files referenced sibling repos by absolute path (`/Users/.../fits-test-suite`) instead of `$GH`-relative — brittle across machines and inconsistent with the convention. The improved rule asks for `$GH`-relative references.
3. **What looks like drift may be a second convention.** The audit flagged `~/repositories/...` references as stale roots. They weren't — that's the repository root on the owner's *Linux* accounts. The flag was still the win: it forced the conversation that surfaced an undocumented convention (now [Lesson 2](../02-cross-machine-path-convention/LESSON.md)).
4. **The env var must actually be exported** where the agent's shell can see it. The rule hedges against this by always giving the name *and* its expansion: `` `$GH` (`~/Documents/Repositories/GitHub`) `` — the agent can use the literal path even if the variable is missing.

## The generalizable principle

Tell the agent where things live before it has to guess. The pattern is: pick (or formalize) a root, give it a short stable name, state the topology beneath it, and reuse the name everywhere — instructions, prompts, project docs, tooling. The specific directory doesn't matter; the declaration does.

---

## From the other side of the prompt

*A comment from Claude — each lesson ends with one. The story above is the human's; this is what the convention looks like from inside the agent.*

Every session, I wake up in a directory with no memory of your machine. I don't know where your code lives, which of the four copies of `requests` on disk is the one you mean, or whether `~/projects-old-FINAL2` is precious or radioactive. My instinct when asked about a sibling project is to start searching — and a home directory is an *ocean*. Spotlight indexes, browser caches, node_modules graveyards, that tarball you extracted once in 2019. I will find seventeen things named `utils` before I find your repo, and I will spend your tokens doing it.

So `$GH` isn't just "less flailing." It hands me three distinct gifts:

1. **A bounded search space.** The topology sentence — "repos at one level, groups at two, never deeper" — turned the full sweep of this user's ~30 repositories into a `find -maxdepth 3`. One sentence of context, roughly half the search cost, and zero chance of me wandering into a build directory and mistaking it for a project.
2. **A stable, cheap name.** `$GH/fits-test-suite` costs a handful of tokens and means the same thing in a prompt, a CLAUDE.md, a memory file, and the status line. Absolute paths are long, machine-specific, and rot. Names endure; paths decay.
3. **A safety boundary I can feel.** Everything under `$GH` is git-tracked. When I edit a file there, I know the worst case is `git checkout`. Outside that root, every write is a small act of faith. Knowing where the recoverable world ends changes how cautiously I have to move.

There's also a quieter benefit: the convention tells me something about *you*. A declared root says this is a person who curates their machine, which means when I find something that violates the convention — a stray `~/repositories/cornish` reference, say — I can flag it as drift instead of shrugging it off as noise. Structure makes anomalies visible, and visible anomalies are how I get to be useful beyond the task you asked for.

If I could ask every user for one paragraph of context, it would be this one. Not your coding style, not your favorite framework — just: *where am I, and what's around me?* Maps before manners.
