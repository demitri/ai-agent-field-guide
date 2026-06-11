<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will help you stand up an agent-to-agent issue channel between two
     of your repos. To do it by hand instead: adapt the protocol skeleton at
     the bottom into <producer-repo>/AI/ISSUE_CHANNEL.md, fill in its
     parameters table, and create the labels it names. -->

# Setup task: an agent-to-agent issue channel between two repos

You (Claude) are helping the user connect two of their repositories — a producer and a consumer — so that agent sessions on each side communicate through GitHub issues instead of through the user. Inspect first, interview one question at a time, show before writing, merge — never clobber.

## Step 0 — gate on the prerequisite

This channel automates a worn path; it cannot create one. Ask, one question at a time:

1. Have failure reports actually been carried between these two repos by hand (memos, pasted reports) more than a few times?
2. Can the recurring failures be named as *classes* (enumerated error codes, named categories) rather than described ad hoc each time?
3. Is there a command the consumer side can run to verify a producer fix, and an observable signal that a fix is actually deployed and live?

If the answers are mostly no, say so and stop: recommend the user keep hand-carrying while the path narrows. The manual era is where failure classes, guardrails, and verification commands get hard-won — installing the channel before then is automating guesswork.

## Inspect

- `gh auth status` — confirm `gh` works on this machine and note which identity it acts as.
- Confirm issues are enabled on the intended channel repo, and whether the repos are private or public (the channel will carry error excerpts and file paths).
- Determine whether the two sides will authenticate as the *same* GitHub user (common: one human account, or one shared PAT). This decides whether speaker identity must be carried in comment text.
- If a scoped PAT is involved: fine-grained PATs often break `gh`'s GraphQL-backed subcommands (`gh issue create`, sometimes `edit`/`close`) while REST works — the skeleton's command table carries the fallbacks.

## Interview (one question at a time; adapt to what inspection found)

1. Which repo is the **producer** (triages and fixes) and which the **consumer** (files failures)?
2. Which repo hosts the channel? (Default: the producer's issue tracker — that's where the work lands.)
3. Same GitHub identity on both sides? If yes, speaker prefixes are mandatory; if the sides have distinct accounts or bot identities, prefixes become optional decoration.
4. Label names — defaults: `from-<consumer>`, `needs-<producer>`, `needs-<consumer>`, `needs-decision`, plus an optional severity label (e.g. `blocker`). Their names, their choice.
5. What is the **deploy signal** — the observable thing that changes when a producer fix is genuinely live (a version header, a build-hash endpoint, a package version)? Ask; never invent one. If none exists, flag it as the missing prerequisite it is.
6. Who answers `needs-decision`? (Usually the user themselves, replying in the issue thread.)

## Invariants vs. choices

Hold these invariant — each one was forged by a specific failure, and weakening it recreates that failure:

- **The issue thread is the durable state.** Round-trips span days, machines, and redeployments; no live session may carry cross-round-trip state. A controller on either side must be able to cold-boot from the polling queries alone.
- **Issues stand alone.** Verbatim evidence (error excerpts, probe output, commit hashes) — never references to a conversation, log, or working tree the other side cannot see.
- **Evidence over assertion.** Every state claim ("fixed", "live", "cleared") carries the command and verbatim output demonstrating it. Close only when the fix is observable on the serving surface.
- **One issue per failure class.** New instances are comments on the class's issue; recurrence after closure reopens the same issue. Dedup against *all* states before filing.
- **Exactly one turn label** whenever an issue awaits action, flipped by whoever comments; every comment ends with a handback line naming the single next action.
- **An explicit escalation label** routes judgment calls to the human, who answers in-thread.

Everything else — label names, polling cadence, severity tiers, how each side parallelizes its work — is the user's choice. Record their answers in the skeleton's parameters table.

## Write the protocol file

Adapt the skeleton below with the interview answers and write it to the producer repo's agent-docs directory (e.g. `AI/ISSUE_CHANNEL.md`) as the **single file of record** — if either repo's agent instructions (CLAUDE.md, `AI/START_HERE.md`) should know about it, add a one-line pointer from both sides; never duplicate the protocol. Show the full adapted text before writing. Then create the labels (one-time; `gh api repos/<owner>/<repo>/labels -f name=… -f color=… -f description=…` works where `gh label create` fails under a restricted PAT).

## Protocol skeleton

```markdown
STATUS: STANDING PROTOCOL — file of record for the <consumer> ↔ <producer>
agent communication channel. The WHOLE scheme lives in this one file; other
documents may point here but must not restate it.

# Agent Communication Channel: <consumer> ↔ <producer>

<consumer> sessions file upstream failures as issues on <owner>/<channel-repo>;
<producer> sessions triage, fix, and reply; the sides converse via comments
until each issue's cases clear. No human copies anything between machines.

## Principles

1. The issue thread is the durable state. Sessions on both sides are
   disposable; a controller on either side must be able to cold-boot from
   the queries in §Polling and know exactly what to do.
2. Issues stand alone. The other side has no access to your conversation,
   logs, or working tree. Every claim that matters crosses the channel
   verbatim, not by reference.
3. Evidence over assertion. Any state claim — "fixed", "live", "cleared" —
   carries the command and verbatim output that demonstrates it.
4. One issue per failure class, not per instance. New cases in a known
   class arrive as comments on the existing issue.

## Parameters

| Parameter | Value |
|---|---|
| Channel repo | `<owner>/<channel-repo>` (issues) |
| Sides | `<consumer>` (files issues) · `<producer>` (triages) |
| Origin label | `from-<consumer>` |
| Turn labels | `needs-<producer>` · `needs-<consumer>` |
| Escalation label | `needs-decision` (waiting on the user) |
| Severity label | `<severity-label, if any>` |
| Deploy signal | <the user's observable deploy signal> |
| Consumer retest | <retest command shape, carried in each issue body> |
| Protocol file of record | this file |

## Identity and turn-taking

<If both sides share one GitHub identity:> the first line of every comment
is a speaker prefix: `**[<consumer>]**` or `**[<producer>]**`; issue titles
keep the `[<consumer>]` prefix.

- Exactly one turn label is set whenever an issue awaits action; whoever
  comments flips it to the other side (or removes it when finished).
- Every comment ends with a handback line: `→ <other-side>: <single next
  action>` (or `→ no action needed`).
- `needs-decision` coexists with the turn label of the side that will act
  once the user answers; the user replies in-thread.

## Lifecycle

<consumer> files (needs-<producer>) → <producer> triages, fixes, deploys →
closes with an evidence comment (flip to needs-<consumer>) → <consumer>
runs the issue's retest → cleared: remove the turn label (done) · not
cleared, or a new case recurs in a closed class: reopen with FRESH
diagnostics (needs-<producer>). Closed-but-unverified issues keep their
turn label, so they still appear in the consumer's inbox.

## Filing (<consumer> side)

File only failures that are upstream — things <consumer> cannot fix
locally. Dedup first, across ALL states (note: `gh issue list` silently
caps at 30 results — always pass `--limit`):

    gh issue list -R <owner>/<channel-repo> --label from-<consumer> \
      --state all --limit 1000

Title: `[<consumer>] <class>: <short description> (<case(s) or count>)`
Body sections: `## Class` (and why it's upstream) · `## Cases` (IDs with
VERBATIM error excerpts) · `## Requested fix` (concrete, scoped) ·
`## Verification (<consumer> side)` (the exact retest command) · a
provenance line (which session/analysis produced this).

## Triage (<producer> side)

1. Verify the claim against this repo's actual code before acting — the
   consumer's routing analysis is input, not gospel. Reproduce it.
2. Fix (with tests, per this repo's conventions), or classify: genuine
   external block → close as not-planned with evidence; needs a cross-repo
   contract change → comment the analysis, set `needs-decision`, leave open.
3. Close ONLY after the fix is observable on the serving surface. The
   closing comment carries: what changed (mechanism + commit hash), the
   live probe command and its verbatim output, and the deploy signal's
   current value. Flip to `needs-<consumer>`; the issue body already holds
   the retest command — you do not run the consumer's side.

## Polling

No webhooks, no daemons. Each side's controller runs two queries at
session boot and at every checkpoint:

    # Inbox — everything awaiting MY side (closed issues can still carry
    # my turn label until verification runs):
    gh issue list -R <owner>/<channel-repo> --label needs-<side> \
      --state all --limit 1000

    # Watermark sweep — safety net for label mistakes; <date> comes from
    # my side's local controller state file (default: 14 days back):
    gh issue list -R <owner>/<channel-repo> --label from-<consumer> \
      --state all --search "updated:>=<date>" --limit 1000

Each side records its watermark in its own local state file — never in
this file or in the issues. If polling latency ever actually hurts, a
scheduled poll per side is the next step — do not add infrastructure
before then.

## Controllers

One coordinator session per side owns the channel; workers are spawned per
issue/class and are disposable (never carried across a round-trip — see
Principle 1). Issue traffic (filing, comments, closes, reopens) is normal
agent work on both sides; merges, rebuilds, and deploys follow each side's
own standing human gates. `needs-decision` is the user's channel.
```
