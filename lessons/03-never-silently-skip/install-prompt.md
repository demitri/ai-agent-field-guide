<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will install the rule and the audit skill for you.
     The skill payload is in no-silent-skip-review/SKILL.md alongside this
     file; the rule template is at the bottom. Background: LESSON.md. -->

# Setup task: install the never-silently-skip rule + audit skill

You (Claude) are installing a two-part defense against silent error swallowing: a global CLAUDE.md rule, and a dedicated audit skill that enforces it. Read LESSON.md alongside this file if you want the rationale — in short, the rule alone is empirically insufficient, so both parts are required.

## Steps

1. **Show the user the rule** (template below) and ask whether to adapt it: the examples are Python-flavored (`pass`, `except`); offer equivalents for their primary language (`catch {}`, `.unwrap_or_default()`, swallowed promise rejections, …). Keep the structure and the crash-loudly close.

2. **Merge into `~/.claude/CLAUDE.md`** (create it, and `~/.claude/`, if absent). If a similar rule already exists — look for a heading like "Never Silently Skip" — extend it rather than duplicating. Ask if they'd rather scope it to one project's CLAUDE.md — but recommend global; this failure mode is language- and project-independent.

3. **Install the skill.** Copy `no-silent-skip-review/SKILL.md` (shipped alongside this prompt) to `~/.claude/skills/no-silent-skip-review/SKILL.md`, creating directories as needed. If this prompt was pasted as text rather than @-referenced, the payload file isn't on your disk — ask the user for the path to their copy of the lesson directory (or its repo clone) before this step. Show the user the file first. Mirror the language adaptations from step 1 in the skill's check list — its examples are Python-flavored too.

4. **Explain the operating doctrine** — without it the installation is decorative:
   - Run the skill after any work touching error handling, parsers, validators, filters, or external-input processing.
   - Iterate until the verdict is clean: invoke → fix → re-invoke. "Concerns" means fix and re-run, not ship.
   - If they have a review process, suggest adding: the silent-skip audit is a mandatory pre-pass before other review of error-handling code.

5. **Offer a live demonstration:** run the skill on their current diff or most recent commit. Finding a real violation in their own code is worth more than any explanation.

## Rule template

```markdown
## CRITICAL: Never Silently Skip Content or Errors

**NEVER write code that silently discards data, skips content, or
suppresses errors to make something "work."** This is the single most
important coding rule. Violations include:

- Broadening a filter/regex to exclude content that was causing an error
- Adding `pass`, `continue`, or fallback logic that hides failures
- Marking content as "not content" or "not relevant" to avoid processing it
- Stripping, ignoring, or downgrading data to bypass a validation check
- Any approach where the "fix" is to stop looking at the thing that failed

**The correct approach when content causes an error:**
1. Understand what the content IS
2. Handle it properly (parse it, store it, or explicitly route it)
3. If it genuinely should be skipped, make that an explicit, documented,
   auditable decision — not a side effect of error suppression

When in doubt: **crash loudly.** A crash that surfaces a real problem is
infinitely better than silent data loss.
```
