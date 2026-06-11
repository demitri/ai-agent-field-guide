<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will audit your auto-memory files and install a size-tripwire hook.
     To do it by hand instead: copy the hook template at the bottom into the
     project's .claude/settings.local.json under hooks.SessionStart, with the
     absolute path to that project's MEMORY.md filled in. -->

# Setup task: memory hygiene — audit + size tripwire

You (Claude) are auditing the user's always-loaded memory files and installing a hook that measures them. Inspect first, interview one question at a time, show before writing, merge — never clobber.

## Steps

1. **Measure first.** List the user's project memory directories (`~/.claude/projects/*/memory/`) with each `MEMORY.md` size and file count, plus their global and project `CLAUDE.md` sizes. Report as one table, largest first. These files are paid by every session — size here is recurring cost.

2. **Offer an audit of the worst offender.** Classify each entry into the three cruft classes, and show the proposed disposition table before changing anything:
   - **Stale** — no longer true → propose deletion.
   - **Misfiled** — durable project knowledge that belongs in the repo (apply the clone test: would a fresh session on another machine, or another tool, need this?) → propose a destination (`AI/` topic file or project CLAUDE.md).
   - **Verbose** — keepable but compressible → propose the tighter rewrite.
   Move nothing without approval.

3. **Offer the tripwire hook** for the project(s) with significant memory. Compute the absolute `MEMORY.md` path for each project yourself and substitute it for `<ABSOLUTE_PATH_TO_MEMORY.md>` in the template — angle brackets removed; no placeholder may survive into the installed hook. Threshold guidance: Claude Code hard-truncates MEMORY.md at the first 200 lines or 25KB, whichever comes first — content beyond is silently not loaded (as of June 2026; verify against the Claude Code memory docs). The template fires just *under* both cliffs (24,000 bytes / 190 lines) so the warning lands before truncation begins, and its `stat` chain covers both Linux (`-c%s`) and macOS (`-f%z`).

4. **Explain the contract** in one sentence when installing: the hook detects (harness-run, can't be skipped); the audit remediates (run as its own session task, full attention). Standing "keep it tidy" rules guarantee neither.

5. **Show the settings change, confirm, merge** into the project's `.claude/settings.local.json` (or `settings.json` if they share settings with collaborators).

## Hook template (per project — localize the path)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "f=\"<ABSOLUTE_PATH_TO_MEMORY.md>\"; s=$(stat -c%s \"$f\" 2>/dev/null || stat -f%z \"$f\" 2>/dev/null || echo 0); l=$(wc -l < \"$f\" 2>/dev/null || echo 0); if [ \"$s\" -gt 24000 ] || [ \"$l\" -gt 190 ]; then printf '{\"systemMessage\":\"MEMORY.md is %d bytes / %d lines — nearing the 25kB/200-line load cliff; compact it: move detail to topic files, drop resolved entries\"}' \"$s\" \"$l\"; fi",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```
