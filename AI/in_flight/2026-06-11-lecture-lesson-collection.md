# Build the claude-wisdom lesson collection: review the user's global/per-project Claude customizations one by one, producing a LESSON.md + install-prompt.md pair per item, toward a shareable lecture.

Parked: 2026-06-11 14:19 America/New_York

STATUS: Lessons 01–11 written and user-reviewed in discussion (all six global CLAUDE.md rule sections covered; review policy became lessons 06–09; session-lifecycle skills became lesson 11 with skill payloads). NOT done: the `AI/` directory convention lesson (next up — origin question pending, reproduced below), all TODO.md topics, the settings/statusline/MCP/utility-skills items, the meta-lesson, and lecture assembly. The repo is not git-initialized.

## Last session output (verbatim)

(written at park time — the last substantive end-of-work message, reproduced from the session; it ended on the question the user deferred to the next session)

> Both done.
>
> **Lesson 8 upgraded:** the extra line now gets its due — "worth its weight in gold," with the mechanism spelled out: without it reviewers check the diff's correctness; with it they also step back and ask *is this the right approach at a higher level*, and that question pays off almost every time. The asymmetry stays as the rule: widening the reviewer's scope is fine; narrowing it is the sin.
>
> **Lesson 11** (`11-session-lifecycle/`) ships both skills verbatim as payloads (I grepped them for personal/machine-specific content first — clean). The story runs from your working pattern (concurrent projects, parent/child sessions, windows-as-sticky-notes eating a 16GB laptop, reboot = a dozen loose ends at once) through the two skills as opposite ends of one problem: `/endsession` audits for value that exists only in the conversation; `/park` saves the session-as-document — the work summary plus, verbatim, the final summary you hadn't dealt with. The install prompt has the agent check working style first (single-session users may only need `/endsession`) and adapt the `AI/in_flight/` path convention rather than assuming it.
>
> The commentary produced what might be my favorite observation of the collection (#16): **an agent's continuity is a property of artifacts, not the agent.** [...]
>
> **Next**, I'd suggest the biggest remaining item: the **`AI/` directory convention** — `START_HERE.md`, `in_flight/`, TODO files, the whole organizing-files-for-agents layer that ~25 of your repos share [...]. It's also the TODO item where you said you'd definitely want my tips on your current setup. To start: how did `AI/START_HERE.md` begin? And one thing the sweep noticed that I'd like your read on before I form tips: the convention has drifted variants — `AI Agents/` in openalex-local, `@AI Notes/` referenced in tesseretica's CLAUDE.md — plus a documented split between auto-memory and `AI/` in fitsjs. Was the AI-directory-vs-memory boundary ever deliberately designed, or did it accrete?

User's reply before parking (binding correction): `AI/in_flight/` is the implementation detail of `/park`, not a separate convention — do not frame it as part of the `AI/` directory layer. (Already recorded in notes/process-log.md.)

## Resume context

- Boot documents (read in this order):
  1. `README.md` — repo structure, lesson-format conventions, lessons index.
  2. `TODO.md` — remaining lecture topics.
  3. `notes/process-log.md` — per-lesson origin stories collected so far, corrections, decisions.
  4. `OBSERVATIONS.md` — 17 meta-insights; the lecture's connective tissue.
  5. `notes/per-project-customizations-sweep.md` — raw catalog of ~30 repos (reference; consult when an item needs examples, don't re-sweep).
  (Project memory auto-loads: subagent model selection, interactive-means-discussion, docs-stay-tight.)
- Binding working rules (from user, this session):
  - Interactive review = one item at a time, conversational; NEVER AskUserQuestion batches.
  - Per lesson: human-facing `LESSON.md` (story/reasoning, ends with a first-person "From the other side of the prompt" Claude commentary) + agent-directed `install-prompt.md` (inspect → interview one question at a time → adapt → show before writing → merge don't clobber), plus payload files where a real skill/script is shipped (grep for personal info before shipping).
  - Docs stay tight — resist verbosity; watch CLAUDE.md/MEMORY.md sizes.
  - Subagent model rule: sonnet for deterministic search, haiku for trivial, err upward on any doubt.
  - Sanitization is decided per item in discussion ("a mix of both").
  - Process per item: present my read + ask for the origin story → user tells it → write the pair → update README lessons list + process log (+ OBSERVATIONS when a genuine meta-insight emerged).
- Done — do not redo: lessons 01–11 (see README index); global `~/.claude/CLAUDE.md` repo-location rule already tightened/deployed (topology + Linux mapping) [stable]; global CLAUDE.md survey and $GH-wide sweep both complete and written down.
- Work plan (remaining, roughly in order):
  1. `AI/` directory convention lesson (START_HERE.md, proactive-update rules, AI-vs-memory boundary) — overlaps TODO "organizing files for agents," where the user explicitly wants my tips on their current setup. Pending question, re-ask on resume: **"How did `AI/START_HERE.md` begin? And was the AI-directory-vs-memory boundary deliberately designed or did it accrete? (Sweep found drifted variants: `AI Agents/` in openalex-local, `@AI Notes/` in tesseretica's CLAUDE.md; fitsjs documents an explicit auto-memory vs AI/ split.)"** — remember the in_flight correction above when discussing.
  2. TODO.md topics: token usage; model/subscription value (fold in the subagent-model memory + "sonnet effectively free" policy); tools agents reach for; memory hygiene (tesseretica 30KB hook); $GH on Linux (user action); meta-lesson last.
  3. Smaller inventory items: settings.json choices, statusline (partly covered in lesson 1), codex MCP (partly covered in lesson 7), utility skills (omnigraffle-tools, dedup-video) — possibly one "skills as personal tooling" lesson.
  4. Eventually: assemble the actual lecture from lessons + OBSERVATIONS (user: "maybe when done we can turn this into an actual lecture"); document the build process in detail (process log feeds this).
- Pending user decisions:
  1. The AI/ convention origin question (verbatim above).
  2. NEW, not yet asked: claude-wisdom is not a git repository — initialize it? (Park doc and registry are currently untracked-by-definition.)

## Working tree state at park

- `claude-wisdom`: **not a git repository** — no VCS state to capture. All session artifacts on disk: `README.md`, `TODO.md`, `OBSERVATIONS.md`, `notes/{per-project-customizations-sweep,process-log}.md`, `lessons/01–11/*` (11 lesson dirs incl. payload copies of no-silent-skip-review, park, endsession skills), `AI/in_flight/*` (this park).
- `~/.claude` (not a repo): `CLAUDE.md` repo-location section edited this session (deliberate, user-approved).
- Project memory dir: 4 memory files + MEMORY.md index written this session.
- Possibly touched / not verified: none — the $GH-wide sweep was read-only (background Explore agent).

## First actions on resume

1. Read the boot documents (order above).
2. Confirm git status of claude-wisdom (`git -C . rev-parse --git-dir`) — if still not a repo, raise pending decision 2 (git init) before writing more artifacts.
3. Re-ask pending question 1 verbatim and continue the one-by-one interactive process with the `AI/` convention lesson.
4. Cleanup rule: when the lesson collection work COMPLETES, remove ONLY the registry entry whose Details link exactly matches `2026-06-11-lecture-lesson-collection.md`, then delete this file. If the work is superseded or abandoned, do NOT silently delete — update STATUS here and the registry entry to match, or ask the user.
