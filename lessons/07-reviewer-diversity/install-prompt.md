<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will extend your review policy with a multi-model panel.
     Prerequisite: the review loop from Lesson 6. Background: LESSON.md. -->

# Setup task: add reviewer diversity to the review policy

You (Claude) are extending the user's review loop with a panel of diverse reviewers — multiple models, at least one from a different vendor than the author model.

## Steps

1. **Inventory the available reviewers.** Same-vendor models via subagents (e.g. sonnet/opus alongside an opus author) work immediately. For cross-vendor: do they have access to another vendor's coding agent (e.g. OpenAI's codex CLI)? If codex is installed, offer to register it as an MCP server, read-only:

   ```bash
   claude mcp add codex-reviewer -- codex -c approval_policy=never -c sandbox_mode=read-only mcp-server
   ```

   Adapt for whatever agent they have; the requirements are: it can read the repo, it cannot write, and it can be driven programmatically.

2. **Discuss panel roles.** Different models reliably notice different things; suggest they let each reviewer's role emerge from observed strengths over a few cycles rather than assigning roles up front.

3. **Account for cost.** Ask which models are effectively free on their plan and which are constrained; the policy should encourage free reviewers liberally and position constrained ones where they add the most (typically design/policy review after mechanical findings are cleared).

4. **Show, adapt, merge** the template into the existing Review Policy section of `~/.claude/CLAUDE.md`.

## Policy template (extends the Lesson 6 section)

```markdown
- Use multiple reviewer models — at least one from a different vendor
  than the author model. Each reviewer is a different lens; never rely
  on a single reviewer for anything expensive, irreversible, or
  launch-shaped.
- Reviewer disagreement is high-value signal: adjudicate against the
  actual code, never by vote.
- <cheap-model> reviews are effectively free — use them liberally;
  reserve <constrained-model> for design/policy review once mechanical
  findings are cleared.
```
