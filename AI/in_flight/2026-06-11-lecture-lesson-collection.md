# Build the claude-wisdom lesson collection: review the user's global/per-project Claude customizations one by one, producing a LESSON.md + install-prompt.md pair per item, toward a shareable lecture.

Parked: 2026-06-11 (end of Session 2) America/New_York

STATUS: Lessons 01–16 plus the front-page HIGHLIGHT (`highlights/issue-channel/` — the multi-agent issue channel; was briefly "lesson 17" until the user re-scoped it). OBSERVATIONS at 35 entries. Prime directive ("fail fast, fail loud") and the Highlight section added to README. Stale 30KB references fixed (lessons 13, 16; lesson 16 retitled "The 24KB tripwire"). IN PROGRESS: user-directed review fan-out — independent sonnet review of all 17 install prompts + codex review of the issue-channel prompt (installability focus); findings being triaged/fixed under the dry-round rule. NOT done: the niche category, the undecided small items (statusline/settings/codex-MCP), $GH-on-Linux (user action), the meta-lesson, lecture assembly. Session-3 work NOT yet committed.

## Resume context

- Boot documents (read in this order): `README.md` (incl. lessons index 01–16), `TODO.md`, `notes/process-log.md` (sessions 1 AND 2), `OBSERVATIONS.md` (30 entries), `notes/per-project-customizations-sweep.md` (reference only — don't re-sweep).
- Binding working rules (unchanged from session 1, plus one new):
  - Interactive review = one item at a time, conversational; NEVER AskUserQuestion batches.
  - Per lesson: human-facing `LESSON.md` (story + first-person "From the other side of the prompt" Claude commentary) + agent-directed `install-prompt.md` (inspect → interview one question at a time → adapt → show before writing → merge don't clobber); payloads grepped for personal info; **separate the invariant from the user's personal preference — install prompts ask, never assume (OBSERVATIONS #28, learned via lesson 15 correction)**.
  - Docs stay tight; **date volatile numbers** (month/year stamp on drifting figures — project memory `date-volatile-numbers`); verify external facts before shipping them (claude-api skill / claude-code-guide agent — both used in session 2).
  - Process per item: present read + ask origin → user tells story → write pair → update README index + process log (+ OBSERVATIONS).
  - Live deployments to the real global CLAUDE.md happen on explicit per-rule user approval (4 precedents).
- Done — do not redo: lessons 01–16; observations 1–30; global CLAUDE.md deployments; tesseretica memory-triage TODO (top of `$GH/thehighlighter/tesseretica/AI/TODO.md`) and MEMORY.md tripwire lowered 30000→24000 bytes (`.claude/settings.local.json`) — **both uncommitted in the tesseretica repo; user handles via tesseretica's own protocol**; AI-directory variant migration prompt written for a separate clean session: `AI/prompts/migrate-ai-directory-variants.md`.

## Work plan (remaining, in order)

1. **Multi-agent, cross-repo, GitHub-issue protocol** (user-flagged priority, added at session 2 close). The user: "I have created a working multi-agent, cross repo, GH/issue protocol — this should be documented as a thing that is visible." Opening move next session: ask the user to walk through the protocol — repos involved, how issues carry work between agents/machines, the lunchtime worker's role (GitHub top-level memory mentions "ingest→bug→fix automation via GitHub issues"; multi-session status uses in_flight/), and what "visible" means (lesson? standalone doc? both?).
2. **Niche category**: create `lessons/niche/`; write the omnigraffle-tools item there. dedup-video is omitted. Statusline / settings.json / codex-MCP small items: ask for a ruling (fold somewhere, niche, or drop).
3. $GH on Linux — user action; offer to write the snippet when he does it.
4. Meta-lesson (last): the process log + OBSERVATIONS #28 (don't ship your taste) and the correction history are its raw material.
5. Lecture assembly from lessons + OBSERVATIONS.

## Working tree state at park

- claude-wisdom: all session-2 work committed (lessons 12–16, OBSERVATIONS 19–30, process log, TODO, README, AI/prompts/, this park doc).
- `~/.claude/CLAUDE.md`: two sections added this session (Where Knowledge Lives; Known Quantities; Missing Tools — all user-approved). Not a repo.
- Project memory: `date-volatile-numbers` added; MEMORY.md index updated.
- tesseretica repo: TWO uncommitted changes (AI/TODO.md triage item; settings.local.json tripwire) — user's tesseretica sessions own committing these.

## First actions on resume

1. Read boot documents (order above).
2. Confirm `git -C . status` is clean (session 2 committed everything; if not, investigate before writing).
3. Open work-plan item 1: ask the user to describe the multi-agent GH-issue protocol (question above, verbatim is fine) and continue the one-by-one process.
4. Cleanup rule: when the collection COMPLETES, remove ONLY the registry entry whose Details link matches `2026-06-11-lecture-lesson-collection.md`, then delete this file. If superseded or abandoned, update STATUS and the registry instead — never silently delete.
