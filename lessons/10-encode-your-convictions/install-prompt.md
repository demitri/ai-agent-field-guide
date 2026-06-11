<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will help you encode your engineering convictions as
     CLAUDE.md rules. Worked example (enums over strings): LESSON.md. -->

# Setup task: encode engineering convictions

You (Claude) are helping the user turn engineering opinions they keep re-explaining into durable CLAUDE.md rules. Each conviction is written with three parts: the **why**, the **exceptions**, and the **application pressure**.

## Steps

1. **Draw the convictions out, one at a time:**
   - "What code style or design choice do you keep correcting in agent (or human) output?"
   - "What's an opinion you hold that most codebases get wrong?"
   - If they have past sessions or review threads, offer to scan for repeated corrections.

2. **For each conviction, capture all three parts:**
   - *Why* — the reasoning, so the rule generalizes to unenumerated cases.
   - *Exceptions* — where it legitimately doesn't apply; carve-outs prevent both over-application and constant clarifying questions.
   - *Pressure* — required for new code? opportunistic migration when touching old code? never a license for codebase-wide rewrites?

3. **Show, confirm, merge** into `~/.claude/CLAUDE.md` (global taste) or a project CLAUDE.md (project-specific).

## Worked example (as actually deployed)

```markdown
## Prefer Enum-Typed Values Over Stringly-Typed

When a value is drawn from a fixed, enumerable set — error reasons,
dispatch actions, kinds, modes, states, categories — use an `Enum` (or
`StrEnum` / `IntEnum`) rather than passing raw strings or integers
around. Stringly-typed values are easy to mistype, hard to audit (the
set of legitimate values is scattered across call sites), and invisible
to the type checker.

Concretely:
- New API surfaces that take a "kind" / "reason" / "mode" / "action"
  parameter should declare an `Enum` and accept that type, not `str`.
- When refactoring existing code, opportunistically migrate string
  discriminants to enums when touching the call sites.
- The enum's name and docstring become the discoverable source of truth
  for the value set; new entries are added in one place and type-checked
  everywhere.
- Storage / serialization at boundaries (DB columns, JSON, log messages)
  can use the enum's `.value` — the type-safety lives in the in-process
  code.

Exceptions where strings remain fine:
- Free-form identifiers (paper IDs, file paths, user input).
- Values that genuinely span an open set.
- Single-use sentinel strings in test code where the value is local and
  trivially auditable.
```
