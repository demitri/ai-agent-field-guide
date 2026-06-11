---
name: no-silent-skip-review
description: Audit code, diffs, or commits for silent error swallowing — broad except, pass in error paths, regex broadening, fallback returns. Run after any work touching error handling, parsers, locators, validators, or content processors.
---

# no-silent-skip-review

Audit a target (file / diff / commit) for violations of the universal "Never Silently Skip Content or Errors" rule. Read-only — surface findings, do NOT modify code.

## When to invoke

Run after any work that:
- Modifies error handling (`except`, `raise`, `try`)
- Adds or changes parsing/extraction logic
- Modifies regexes used to identify or filter content
- Changes data validation or pre-processing
- Processes external input (files, network, user-supplied data)

In short: anywhere "skipping is easy and wrong" is a plausible failure mode.

## What you'll need

A target. The invoker should pass one of:
- A commit SHA → use `git show <sha>`
- A file path → read current state
- A diff specification → `git diff <ref>..<ref>` or `git diff` for HEAD vs working tree

If unspecified, default to current uncommitted changes (`git diff HEAD`).

## Required checks

For each, grep + read code in the target. Report findings with file:line references.

1. **Broad except clauses.** Search for `except:`, `except Exception`, `except BaseException`. Each must have a justified narrow purpose documented in a comment OR re-raise immediately. Otherwise: violation.

2. **Pass in error paths.** Search for `pass` (or `continue`, `return None`) immediately after `except` or in a no-op error handler. Each must justify why suppression is correct. Default: violation.

3. **Regex broadening.** If auditing a diff: did any regex become more permissive? Look for added `?`, `*`, broader character classes, removed `\b`, removed `^`/`$`. Surface and ask whether the broader regex was added to "swallow" problematic input the prior pattern surfaced.

4. **Fallback returns that mask failure.** Search for:
   - `return search_end` or any "safe-but-wrong" default value where a raise would surface a real problem
   - `return None` where None propagates silently rather than being checked
   - Default values in error paths (`except: return []`, `except: return ""`)

5. **Skipping content via filter widening.** If auditing a diff: did any filter, denylist, allowlist, or content classifier change to EXCLUDE content that previously caused an error? This is the most insidious form — the "fix" is to stop looking at the failing content. Surface immediately.

6. **Crash-loud principle.** A crash that surfaces a real problem is infinitely better than silent data loss. Verify any new code path that encounters unexpected input either raises or routes the input through an explicit, documented decision (not a side effect of error suppression).

## Output format

```
## Verdict
<clean | concerns | violations>

## Findings
<one bullet per finding: severity (low/med/high), location (file:line), violation type, what the code does, why it's a violation, suggested remediation shape (raise / explicit handling / route to dedicated path)>

## Audit completeness
- Checks run: <list>
- Checks skipped: <if any, why>
- Audit target: <commit SHA / file path / diff spec>
```

## Constraints

- **Read-only.** Never modify code. Findings reported; fixes queued separately.
- **No paraphrasing.** Quote the offending code snippet directly with file:line citation.
- **No verdict softening.** Do not classify a likely-violation as "probably fine" without specific evidence (code comment, surrounding logic, documented invariant). When uncertain, classify as concerns and explain.

## References

This skill codifies the universal "Never Silently Skip Content or Errors" rule. The full rationale and forbidden-pattern catalogue typically lives in the host's `CLAUDE.md` (look under "CRITICAL: Never Silently Skip Content or Errors" if present).
