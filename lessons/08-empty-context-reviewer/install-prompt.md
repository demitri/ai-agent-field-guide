<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will install the minimal-review-prompt discipline.
     Prerequisite: the review loop from Lesson 6. Background: LESSON.md. -->

# Setup task: install the minimal review-prompt discipline

You (Claude) are adding a prompt discipline to the user's review policy: reviewers get the commit hash and nothing else. This rule constrains *you* — when you delegate a review, you will feel that adding context is helpful. It is not. The reviewer's value is its empty context.

## Steps

1. **Show the user the template** and confirm the optional extra line they want (the scope-*widening* line is allowed; anything scope-narrowing is not).

2. **Merge into the Review Policy section** of `~/.claude/CLAUDE.md`.

3. **Demonstrate the failure mode** so the user can police it: show them a dossier-style review prompt (problem description, solution summary, line pointers) next to the minimal one, and explain that the dossier biases the reviewer toward exactly what the author chose to present — the surviving bugs are outside that presentation by definition.

## Policy template (extends the Lesson 6 section)

```markdown
- Review prompts are minimal. The complete prompt is: `Review <hash>` —
  optionally plus the single line "Review not only the changes, but make
  higher level suggestions or improvements if you have any."
  Follow-up rounds: `addressed in <hash>; review`.
- Do NOT include change summaries, intent, implemented solutions, line
  pointers, or question lists. The reviewer reads the commit and explores
  freely; the briefing is the bias. When an agent delegates a review,
  this prompt is sent verbatim — do not add more.
- If design intent must be seeded for a specific reason, never seed all
  reviewers in a round — an unseeded reviewer must remain.
```
