<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will install a mandatory review-loop policy.
     Companion lessons: 07 (reviewer diversity), 08 (minimal review
     prompts) — install those too; this is the core. Background: LESSON.md. -->

# Setup task: install the review-loop policy

You (Claude) are installing a working discipline: every substantive change is committed, then reviewed by a fresh context, in a loop that only a findings-free round can end.

## Steps

1. **Check what's available.** Does the user have an external reviewer wired up (an MCP server to another vendor's model, e.g. codex)? Native subagents always work for same-vendor review. Note what exists; Lesson 7's prompt covers adding a cross-vendor reviewer.

2. **Confirm commit discipline.** The loop reviews *commits*, not working trees — small, reviewable commits are a prerequisite. If the user's habit is large uncommitted sessions, flag that this policy will change their rhythm, and ask.

3. **Show the template, adapt, merge** into `~/.claude/CLAUDE.md`.

4. **Explain the two failure modes the policy guards against** (they'll see both): reviewers manufacturing nit-picks when asked merely to "find issues" (hence the *major issues* framing), and workers declaring "probably fine, stop here" (hence: only a dry round terminates — that judgment is never the worker's).

## Policy template

```markdown
## Review Policy

- Every substantive change is committed, then reviewed by a fresh context
  (subagent or external model). Review is mandatory, not optional.
- The loop: commit → "Review <hash>" (framed toward major issues) →
  verify and fix findings → commit → "addressed in <hash>; review" →
  repeat.
- **Terminate only on a dry round** — a round with no findings. Never
  stop on "findings feel minor" or a diminishing-returns judgment; the
  working agent does not decide when review ends.
- Every new artifact gets at least one round — including the commit that
  fixes the previous round's findings.
```
