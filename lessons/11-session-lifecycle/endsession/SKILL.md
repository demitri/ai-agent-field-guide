---
name: endsession
description: Wind-down audit before the user closes a session. Use when the user asks "anything to close out before ending this session?", "let's wrap up", "winding down", or similar. Reviews the session and current state, surfaces loose ends, git cleanup, next-step notes, and anything that would be lost when the session closes. Does NOT end the session.
---

# End-of-session close-out audit

The user is signaling the session is winding down. Your job is to review
what happened in THIS session and its current on-disk/in-repo state, then
surface what should be done, saved, or cleaned up before the session closes.
This skill does not end the session — it prepares for the user to.

**This is a judgment task, not a checklist.** The categories below are
prompts for your review, not boxes to tick. The valuable output is the
session-specific items a generic checklist would miss. Equally: do NOT
manufacture items to appear thorough — "nothing needs doing; safe to close"
is a correct and welcome answer when true.

## Review pass

Review the visible/available session context with these lenses, and verify
against actual state (run the cheap commands — e.g. `git status --short`,
current branch, upstream check, known active task/session checks; don't
report from memory).
If earlier context appears compacted or unavailable, say so and lean on
verifiable repo/process state plus whatever decisions remain visible:

1. **Loose ends.** Things promised, started, or deferred and never
   finished: "I'll do X after Y" statements, questions asked but never
   answered (in either direction), review findings acknowledged but not
   applied, TODO/FIXME/xfail markers introduced this session, sub-agents or
   background tasks whose results were never consumed, files created as
   "temporary" and never removed.
2. **Git state.** For every repo this session touched — any repo where
   files were edited or read, commands were run, branches were inspected,
   or artifacts were generated in the visible session; if unsure, list it
   as "possibly touched / not verified" rather than omitting it — check
   (read-only) `git status`, current branch, unpushed commits
   (`git log @{u}..` where an upstream exists; if no upstream exists,
   report "no upstream" rather than treating it as clean), stray stashes,
   and worktrees. For branch cleanup, surface only branches clearly
   implicated by this session or obvious temp/work branches — do not audit
   the user's entire branch history unless asked. Surface anything that
   would surprise the user in a week: work stranded on a temp branch,
   uncommitted edits, an unpushed local-only commit, a branch whose work
   was merged but the branch never deleted. Offer the obvious remedies
   (commit, push, merge, delete branch) — but NEVER commit, push, merge,
   or delete without the user's explicit approval in this conversation,
   and follow any project rules about commits and branches.
3. **Capture-before-loss.** Anything that exists ONLY in this conversation
   and matters beyond it: decisions and their rationale, findings,
   gotchas discovered, state of a debate, numbers measured. For each,
   suggest the durable home the project already uses (project docs, session
   ledgers, prompt-file STATUS lines, issue comments) rather than inventing
   new files. Suggest agent memory only when an explicit memory mechanism
   exists in this environment and the user approves; prefer repo-resident
   homes for project-specific facts. If the project has session-tracking
   conventions, honor them.
4. **Next steps.** Where would a future session pick up? If next steps are
   non-obvious, propose a short note in the project's conventional place.
5. **Still running.** Background commands, agents, workflows, remote jobs
   started this session. Check only the categories this agent can actually
   inspect; report anything uninspectable as "not verifiable from this
   session" rather than claiming none exist. Nothing should be silently
   abandoned: either it finishes before close, the user explicitly says
   leave it, or its existence + how to check on it gets written down.

## Mid-work vs. wind-down

If the review shows substantive work genuinely mid-flight — an unanswered
design question blocking progress, a half-executed plan, a session that
would need real re-orientation to resume — say so and recommend `/park` to
the user (recommend only — never invoke it automatically; the user decides)
instead of, or in addition to, simple close-out. If `/park` is unavailable
or unknown in this environment, recommend an equivalent resume note
covering: current status, dirty git state, the next action, and the boot
files a resuming agent must read. Wind-down is for natural seams; parking
is for interruptions.

## Report and act

- Present findings as a SHORT list, most important first, roughly:
  would-be-lost captures → git hazards → loose ends → next-step notes.
  One line each, with the proposed action.
- Ask the user which items to act on when there is a real choice; just do
  the trivial, safe, read-only ones. Batch questions rather than dripping
  them one at a time.
- Approval is action-specific: for any write, commit, push, merge, branch
  deletion, stash, or external update, name the repo, branch, and exact
  action when asking, and show the relevant status/diff summary first when
  applicable. Blanket "go ahead" covers only the items it was given for.
- Execute approved items, verify each (a claimed commit/push/file-write
  gets checked, not assumed), and report honestly — including anything
  that failed or was skipped.
- End with an explicit closing statement: "ready to close", or — if the
  user chose not to act on surfaced items — "ready to close with these
  items intentionally left open:" followed by the list, so the last
  message of the session is an accurate record of what was left undone.
