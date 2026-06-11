<!-- Human: paste this file into a Claude Code session (or @-reference it) in the
     repo you want set up, and Claude will install the AI/ directory convention
     adapted to that project. To do it by hand instead: copy the two templates at
     the bottom, fill in the skeleton, and merge the rules into your CLAUDE.md. -->

# Setup task: install the `AI/` agent-knowledge directory

You (Claude) are installing an agent-orientation layer in this repository: an `AI/` directory with a `START_HERE.md` entry point, plus CLAUDE.md rules that make every future session read it and keep it current. Inspect first, interview one question at a time, show proposed text before writing, and merge — never clobber.

## Steps

1. **Inspect before asking.** Read the repo root, README, and CLAUDE.md (if any). Check for an existing agent-notes directory under any name (`AI/`, `AI Notes/`, `docs/ai/`, `notes/`…).
   - If one exists, ask whether to adopt it as-is or consolidate into `AI/` — one question, their call. (Avoid spaces in the directory name; they trip up agents.)

2. **Interview for the orientation content — one question at a time**, and only what inspection couldn't answer:
   - What is this project, in a paragraph? (Draft it yourself from the repo; ask the user to correct rather than compose.)
   - What's the current state — phase, what works, what's actively in flight?
   - What would a fresh session most likely get wrong, or waste time re-discovering? (These become the pointers and conventions sections.)

3. **Draft `AI/START_HERE.md`** from the skeleton below — tailored, concise, pointer-heavy. It is a table of contents: a fresh session should be oriented in one page and know where detail lives without grepping for it. Detail goes in topic-specific `AI/` files. Create `AI/TODO.md` only if there are real items today.

4. **Merge the CLAUDE.md rules** (template below) into the existing CLAUDE.md, or create a minimal one if absent. Sometimes the pointer line is the entire CLAUDE.md — that's fine.

5. **Offer the boundary rule** if the user's `~/.claude/CLAUDE.md` doesn't already say where project knowledge vs auto-memory goes: show the "Where Knowledge Lives" block below and ask once.

6. **Show everything before writing**, then write.

## CLAUDE.md rules (as deployed across ~15 of the author's repos)

```markdown
- Read `AI/START_HERE.md` first — mandatory session-start orientation.
- Keep `AI/` files current proactively — update `START_HERE.md`, `TODO.md`, and
  topic files whenever work changes project state (phase, layout, decisions,
  dependencies, scope), without being asked.
- `AI/START_HERE.md` stays concise — it is a table of contents; detail goes in
  topic-specific `AI/` files.
```

## `AI/START_HERE.md` skeleton

```markdown
# START HERE

<one sentence: what this project is and what phase it's in>

## What this is
<2–4 sentences, written for an agent with zero context>

## Current state
<a few lines: what works, what's in flight, what's next — updated as it changes>

## Where things are
- `<path>` — <what lives there and when to read it>
- `AI/TODO.md` — open work items
<topic files listed here as they accrue>

## Conventions a fresh session would otherwise violate
<only those; everything else is noise>
```

## Where Knowledge Lives (optional, for `~/.claude/CLAUDE.md`)

```markdown
## Where Knowledge Lives: Repo `AI/` vs Auto-Memory

Apply the clone test: would a fresh session on another machine — or another
tool entirely (e.g. a second AI reviewer) — be wrong or slower without this
fact? If yes, it is project knowledge and belongs in the repo (an `AI/` topic
file, or the project CLAUDE.md if it is rule-bearing), where it is versioned,
reviewable, and visible to every tool. Auto-memory holds only the collaboration
layer — user preferences, corrections, working-style feedback — and
machine-local facts. Memory is also the staging area: corrections incubate
there before being promoted into project or global rules.
```
