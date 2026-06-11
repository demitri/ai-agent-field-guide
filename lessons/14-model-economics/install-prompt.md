<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will help you map your token budgets and install a model-routing
     policy adapted to your plan. To do it by hand instead: check your usage
     page for per-model meters, then copy the rule templates at the bottom into
     your ~/.claude/CLAUDE.md with the model names adjusted to your plan. -->

# Setup task: install model-routing economics

You (Claude) are helping the user get more work from their plan by routing each kind of work to the right budget. Inspect and interview first, one question at a time; show proposed text before writing; merge — never clobber.

## Steps

1. **Map the budgets.** Ask what plan they're on, then have them check their usage page (claude.ai → usage) for separate per-model meters and how fast each moves. The key question: *which models draw from a meter you actually exhaust, and which from one you don't?* Don't assume the answer — plans differ and change; the meters are the ground truth.

2. **Draft the tier map** (template below), filling in their actual models per tier:
   - Constrained tier → judgment-heavy work only.
   - Workhorse tier (the slow meter) → searches, sweeps, review passes, subagents — never cost-caveated.
   - Trivial tier → mechanical tasks.
   - Always include the tiebreak: **err upward when in doubt** — without it, a cost-optimizing agent will gradually decide everything is a trivial task.

3. **Pin routing decisions in config, not conversation.** Where they have recurring subagents (a SQL agent, an explore agent), set the model in the agent definition so the choice is made once.

4. **Ask about batchable work** — anything where no human waits for the answer (annotation pipelines, evaluations, bulk processing). If they have any, propose routing it to API credits with both multipliers (numbers below are as of June 2026 — verify against current pricing docs before quoting them):
   - **Batch API: 50% of standard prices** (typically completes within an hour; max 24h).
   - **Prompt front-loading:** static content first, per-item content last, `cache_control` on the last static block → the shared prefix bills at **~0.1× base input price** (writes cost 1.25×; break-even at two requests). Caveats to state: minimum cacheable prefix varies by model and provider (Anthropic: 1,024–4,096 tokens; some providers need tens of thousands), and the default TTL is 5 minutes — it pays on consecutive calls, not occasional ones.
   - Verify with `usage.cache_read_input_tokens` — if it's zero across repeated calls, something volatile (a timestamp, an ID) is in the prefix.

5. **Show the rules, confirm, merge** into `~/.claude/CLAUDE.md`.

## Tier-map rule template (adapt model names to their plan)

```markdown
## Model Tiering

- <constrained models> draw from the constrained budget — reserve for
  judgment-heavy work (design, policy review, the hardest problems).
- <workhorse model> is effectively free on this plan (separate, slower
  meter) — never cost-caveat its use; route searches, review passes,
  sweeps, and recurring subagents there.
- <trivial-tier model> for trivial mechanical tasks.
- When in doubt, err upward — cheap routing must never quietly degrade
  quality.
```

## API-credit routing rule template

```markdown
## API-Credit Routing

Work that is batchable and has no human waiting (pipelines, evaluations,
bulk jobs) leaves the subscription: run it on API credits via the Batch
API (50% discount). Structure batch prompts with all static content
first and the per-item content at the very end so the shared prefix
caches (reads ≈ 0.1× input price; mind the per-model minimum prefix and
the cache TTL). Verify cache hits via usage.cache_read_input_tokens.
```
