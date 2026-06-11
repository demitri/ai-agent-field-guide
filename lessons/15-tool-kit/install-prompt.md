<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will install the stop-don't-degrade rule and survey your machine
     for the agent toolkit. To do it by hand instead: copy the rule block below
     into your ~/.claude/CLAUDE.md and install whatever you're missing from the
     starter kit list. -->

# Setup task: install the agent toolkit and the stop-don't-degrade rule

You (Claude) are helping the user equip their machine with the tools agents reach for, and installing the rule that prevents silent degradation when a tool is missing. Inspect first, interview one question at a time, show before writing, merge — never clobber.

## Steps

1. **Ask about installation policy first.** How does software get onto this machine — which package manager, or none? Is anything vetoed (some users ban specific managers entirely)? Record any veto as a Lesson-5-style standing rule if they want it durable. Never assume a route.

2. **Ask the who-installs question.** When a session hits a missing tool, should the agent (a) install it via their stated route and continue — the choice most users prefer — or (b) stop and let them install it themselves? Their answer picks the rule variant in step 5.

3. **Survey the machine** against the starter kit below (`command -v` each). Report what's present and missing in one table.

4. **Offer to install the missing ones** — via their stated route only, with confirmation, skipping any they don't want. Don't push tools for media/document work they never do; ask what kinds of files their projects actually touch.

5. **Offer the matching global rule variant** (below) for `~/.claude/CLAUDE.md` — show it, confirm, merge.

## Starter kit (what agents repeatedly reach for — as of June 2026)

| Tool | Job |
|---|---|
| `rg` (ripgrep), `fd` | fast code/file search — the agent's bread and butter |
| `jq` | JSON slicing without regex improvisation |
| `gh` | GitHub PRs, issues, API from the shell |
| `pandoc`, `pdftotext` | document conversion and PDF text extraction |
| `mediainfo`, `ffmpeg` | media metadata and processing |
| `tesseract` | OCR on images and scans |
| `sqlite3`, `psql` | poking at databases directly |
| `tree` | orienting in directory structures |

## Global rule (for `~/.claude/CLAUDE.md`) — pick the variant from step 2

**Variant A — agent installs (most users):**

```markdown
## Missing Tools: Install, Don't Degrade

Reach for the best tool for the job. If it isn't installed, say so —
name the tool and what it's for — then install it via <their package
manager> and continue. Never degrade silently to a worse method (a
clumsier tool, hand-rolled parsing, skipping the check): the fallback
chain costs more tokens now and in every future session; an install is
paid once. If the install fails or the tool isn't available, proceed
with the fallback and say so.
```

**Variant B — user installs:**

```markdown
## Missing Tools: Stop, Don't Degrade

Reach for the best tool for the job. If it isn't installed, stop and say
so — name the tool and what it's for — and let the user install it
rather than degrading to a worse method. Never degrade silently: the
fallback chain costs more tokens now and in every future session; an
install is paid once. Do not install tools yourself unless asked —
installation routes are the user's policy. If the user declines the
install, proceed with the fallback and say so.
```
