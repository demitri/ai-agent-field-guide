<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will help you capture your standing vetoes. Background and
     a worked example (the no-Homebrew rule): LESSON.md. -->

# Setup task: capture standing vetoes

You (Claude) are helping the user record things they will *always* refuse, so agents stop proposing them. Each veto is written as **ban + alternative**: what's off the table, and what to do instead.

## Steps

1. **Interview, one question at a time.** Prompts to draw the vetoes out:
   - "What do AI agents (or colleagues, or tools) keep suggesting that you always turn down?"
   - Package managers or installers they avoid? Frameworks/languages they won't adopt? Services they refuse (cloud uploads, telemetry)? Actions they never want unprompted (force-push, auto-commit, file deletion)?
   - If they're unsure, offer to scan recent conversation history or shell history for repeated refusal patterns — with their permission.

2. **For each veto, get the alternative.** "No Homebrew" needs "software is installed by direct download / source build here." A ban without a route leaves the agent stuck the next time the need genuinely arises. Ban the *class*, not the instance (all `brew` commands, not one).

3. **Show before writing.** Render the rules, confirm wording, then merge into `~/.claude/CLAUDE.md` (or the project CLAUDE.md for project-specific vetoes). Extend existing rules rather than duplicating.

## Worked example (as actually deployed)

```markdown
## Package Management

The user does NOT use Homebrew and does not want to. Never use `brew`
commands (install, services, list, etc.). Software is installed and
managed through other means (direct downloads, source builds, system
packages, etc.).
```
