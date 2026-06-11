<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will install the rule for you. To do it by hand, copy the
     template at the bottom into ~/.claude/CLAUDE.md. Background: LESSON.md. -->

# Setup task: install the stop-and-think-before-building rule

You (Claude) are installing a checkpoint rule: before implementing something complex, scaling up an approach, or running a large batch of similar operations, the agent must first check whether the problem is already solved and state the costs out loud.

## Steps

1. **Show the user the template below** and ask about thresholds: the N>50 trigger suits LLM/API call campaigns; if their work involves other expensive units (cloud jobs, CI runs, paid lookups), adapt the clause to name those too. Keep the requirement that the agent *states a number* — that's the mechanism, not decoration.

2. **Merge into `~/.claude/CLAUDE.md`**, extending any existing build-vs-buy or cost rule rather than duplicating.

3. **Explain the behavior they should expect** (and demand): before writing a custom implementation, the agent names the existing libraries it checked and why they don't fit; before a large operation, it states per-unit and total cost and any batch alternative — *before* the work, not in the post-mortem.

## Rule template

```markdown
## Stop and Think Before Building

Before implementing something complex or scaling up an existing approach,
pause and ask: **is this a solved problem?** Check whether a better
library, API feature, or established pattern already exists. Don't
optimize a bad approach — replace it. Adding a dependency is fine if it
means not reinventing the wheel.

Concretely: before running N>50 similar operations, state the per-unit
cost and total cost, and flag any bulk/batch alternatives. Before writing
a custom implementation, check if a well-maintained library handles it.
Before optimizing a loop, question whether the loop is the right
structure at all.
```
