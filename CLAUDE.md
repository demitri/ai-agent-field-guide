# ai-agent-field-guide — working rules

New session: read **[`AI/START_HERE.md`](AI/START_HERE.md)** first for orientation. This file is rules only.

This repo *is* a collection of lessons about working with AI agents, so it eats its own cooking — the conventions below are themselves Lesson 1 (front door), Lesson 16 (keep `AI/` current), and the fail-loud prime directive, applied to this repo.

## Prime directive

**Fail fast, fail loud.** When something is wrong — a broken link, a convention you can't satisfy, a fact you can't verify — surface it; never paper over it to make the repo "look done." Most of the lessons here are that instinct applied to one more surface.

## Anatomy of a lesson

Each lesson lives in `lessons/NN-short-name/` and contains exactly two artifacts (plus any payload files it ships):

- **`LESSON.md`** — the story: where the convention came from, the problem it solved, why it works, how it can be improved. It **must end** with a `## From the other side of the prompt` section — a first-person comment from Claude on what the convention looks like from inside the agent. Voice: literate, opinionated, concrete; the human is "the owner."
- **`install-prompt.md`** — an agent-directed setup prompt. It **opens with an HTML comment** telling a human how to use it (paste/@-reference). The prompt itself inspects the user's machine, **asks one question at a time**, shows proposed text before writing, and **merges rather than clobbers**. Adapt to the machine; don't assume paths.
- **Payload files** (scripts, skill dirs) ship alongside, referenced from the prompt — see `03-never-silently-skip/` and `11-session-lifecycle/`.

## When you add or change a lesson

1. Number it next in sequence; pick a terse `short-name`.
2. Add a one-line entry to the **Lessons** list in `README.md` (the annotated index is canonical there — don't re-list lessons elsewhere).
3. If it resolves a queued item in `TODO.md`, update that line rather than deleting the history.
4. **Cross-reference** related lessons by relative link, both directions — a new lesson usually deepens an existing one (e.g. 17 deepens 7).

## One canonical home per fact

Don't duplicate prose across files. The README holds the lesson index; `START_HERE.md` routes; each `LESSON.md` owns its topic. Other files get a one-line pointer, not a paragraph. A fact in two places is a fact that will disagree with itself.

## Keep `AI/` and this file current — proactively

When the repo's shape changes (a new top-level dir, a changed convention, a resolved TODO), update `START_HERE.md` / this file in the same change, without being asked. The front door is only worth having if it's true.

## Reference material, not rules

- `OBSERVATIONS.md` — meta-insights about working with agents; the connective tissue between lessons.
- `notes/` — raw working material (sweeps, the process log) that lessons are distilled from; not itself shareable, not lesson-shaped.
- `highlights/` — working systems built *from* the lessons (write-up + install prompt, same pair structure as a lesson).
