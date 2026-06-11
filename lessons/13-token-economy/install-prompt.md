<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will install token-economy practices adapted to your projects. To do
     it by hand instead: copy the "Known Quantities Are Never Guessed" block below
     into your global CLAUDE.md, and add pointers to your projects' sources of
     truth (schemas, API specs, configs) in each project's CLAUDE.md or
     AI/START_HERE.md. -->

# Setup task: install token-economy practices

You (Claude) are helping the user get more work out of their token budget. Inspect first, interview one question at a time, show proposed text before writing, merge — never clobber.

## Steps

1. **Ask how they pay** — subscription or API credits? It sets the framing: on a subscription, wasted tokens mean hitting rate limits sooner (lost working time); on API credits they're money. The practices are the same; the urgency differs.

2. **Ask where they've seen waste** — "Have you watched a session and caught the agent groping — guessing at names, fanning out greps, re-reading files — for something that's actually defined somewhere?" Each story names a missing declaration. If they haven't watched, suggest the practice: read the trace like a profiler; groping is the hot spot.

3. **Inspect the current project for guessable knowns.** Look for defined quantities an agent might trial-and-error instead of reading: database schemas, API specs, config formats, generated-code layouts. For each, propose a one-line pointer in the project CLAUDE.md or `AI/START_HERE.md` (see Lesson 12) naming where the definition lives.

4. **Offer the global rule below** for `~/.claude/CLAUDE.md` — it gives the guess loop an exit condition and turns the user's interrupts into durable fixes.

5. **Offer delegation for search-heavy work** if their projects involve large sweeps or databases: a read-only subagent (e.g. a SQL agent that knows the schema conventions) keeps exploration tokens out of the main context — only conclusions return.

6. **Show everything before writing**, then write.

## Global rule (for `~/.claude/CLAUDE.md`)

```markdown
## Known Quantities Are Never Guessed

If something has an authoritative definition — a database schema, an API
signature, a config key, a file format — do not discover it by trial and
error. Stop after the first miss: find the definition (schema files, docs,
source) and read it; if it can't be found, ask. Guess-and-retry on a defined
quantity burns tokens rediscovering what is already written down, and the
loop has no natural exit — every error message feels like progress.

When the user interrupts to point at a source of truth, the interrupt itself
is a finding: a pointer is missing. Offer to record it durably (project
CLAUDE.md, AI/START_HERE.md, or memory) so no future session needs the same
interrupt.
```
