<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will help you stand up an agent-to-agent issue channel between two
     of your repos. To do it by hand instead: adapt the protocol skeleton at
     the bottom into your producer repo's agent-docs directory, fill in its
     parameters table, and create the labels it names. -->

# Setup task: an agent-to-agent issue channel between two repos

You (Claude) are helping the user connect two of their repositories — a producer and a consumer — so that agent sessions on each side communicate through GitHub issues instead of through the user. Inspect first, interview one question at a time, show before writing, merge — never clobber. If any command in this setup fails, show the user the raw error and stop — never improvise past a failed step.

## Step 0 — gate on the prerequisite

This channel automates a worn path; it cannot create one. Ask, one question at a time:

1. Have failure reports actually been carried between these two repos by hand (memos, pasted reports) more than a few times?
2. Can the recurring failures be named as *classes* (enumerated error codes, named categories) rather than described ad hoc each time?
3. Is there a command the consumer side can run to verify a producer fix, and an observable signal that a fix is actually deployed and live (a version header, a build hash, a package version)?

Decision rule: proceed only if 2 and 3 are both yes — the protocol's verification and close steps run on them. Otherwise say so and stop: recommend the user keep hand-carrying while the path narrows. The manual era is where failure classes, guardrails, and verification commands get hard-won — installing the channel before then is automating guesswork. (A "no" on 1 is a strong caution: if reports have never been hand-carried, the need is still hypothetical.)

## Preflight (stop on any failure and say what's missing)

First ask which two repos the user wants to connect — the roles get formalized in the Interview, but the checks below need concrete targets now.

- `gh auth status` — if `gh` is absent or unauthenticated, stop: name the tool, what it's for (all channel traffic flows through it), and let the user install or authenticate before resuming. Note which identity each side will act as, and whether the user is on github.com or a GitHub Enterprise host. On GHES, authenticate `gh` against that hostname and have every session export `GH_HOST=<host>` — that routes both `gh issue` and `gh api` commands to the instance (a bare `gh api repos/…` otherwise targets github.com).
- Confirm issues are enabled on the intended channel repo — and capture its visibility in the same probe: `gh api repos/<owner>/<repo> --jq '{has_issues: .has_issues, private: .private}'`. If `has_issues` is `false`, stop: the user enables them under repo Settings → General → Features → Issues. `private: true` means the public-repo conditional in the skeleton resolves to "drop".
- Probe real permissions, not just auth: `gh api repos/<owner>/<repo>/labels` on the channel repo. If it fails (org policy, PAT scope), surface the error — issue read/write for both identities is the minimum, and an org admin may need to grant it.
- Locate the local clones of BOTH repos — each gets a pointer line at install, and the producer's also holds the protocol file. Confirm each clone's `git remote get-url origin` matches the GitHub repo the user named; if either clone is missing, stop and say which. Check `git status --short` in both: if any file you'll touch (instructions files, protocol location, `.gitignore`) has uncommitted changes, get explicit approval before editing it.
- The protocol requires VERBATIM error excerpts and probe output in issue bodies, so agree on a redaction rule regardless of repo visibility: never secrets, tokens, or customer data — issue trackers persist and are visible to collaborators, apps, and exports. If the channel repo is public, tighten it further (no private paths or internal hostnames either) and warn the user explicitly. The agreed rule goes into the protocol file's Principles.
- Determine whether the two sides will authenticate as the *same* GitHub user (common: one human account, or one shared PAT). This decides whether speaker identity must be carried in comment text.
- If a scoped PAT is involved: fine-grained PATs often break `gh`'s GraphQL-backed subcommands while REST works — the skeleton's §gh table carries the REST fallbacks.

## Interview (one question at a time; adapt to what preflight found)

1. Which repo is the **producer** (triages and fixes) and which the **consumer** (files failures)? Get each as a full `owner/repo` path — for personal repos the owner is the username `gh auth status` shows. Also pick a SHORT name for each side (typically the bare repo name): the short names go into labels, speaker prefixes, and issue titles (GitHub label names can't contain `/`); the full `owner/repo` is used only in commands. If producer and consumer turn out to be the same repo (two subsystems rather than two repos), the channel still works: sides are roles, not repos; keep both labels and prefixes, and read every "both repos" step in Preflight, Install, and Verify as the one repo wearing both hats — one clone, one instructions file, one `.gitignore`.
2. Which repo hosts the channel? (Default: the producer's issue tracker — that's where the work lands.)
3. Same GitHub identity on both sides? If yes, speaker prefixes are mandatory; if the sides have distinct accounts or bot identities, prefixes become optional decoration.
4. Label names — defaults: `from-<consumer>`, `needs-<producer>`, `needs-<consumer>`, `needs-decision`, plus an optional severity label (e.g. `blocker`). Their names, their choice. (If they decline the severity label, its Parameters row reads `none` — keep the row.)
5. Pin down the **deploy signal** confirmed in step 0: the exact command and the field or header it reads. Never invent one — without it the close protocol cannot carry deploy evidence, and the install must not proceed. Pin the **consumer retest command** (or its shape) at the same time — it fills the Consumer retest parameter and the `## Verification` template carried in every filed issue.
6. Who answers `needs-decision`? (Usually the user themselves, replying in the issue thread.)
7. Where do agent-facing docs live in each repo (a docs/ or AI/ directory, or the repo root)? The protocol file goes in the producer repo's; both repos get a pointer.
8. Confirm the watermark state-file path each side will use (default: `.claude/issue-channel-state` inside that side's repo, untracked) — it's a Parameters-table entry, so it must be settled before writing.

## Invariants vs. choices

Hold these invariant — each one was forged by a specific failure, and weakening it recreates that failure:

- **The issue thread is the durable state.** Round-trips span days, machines, and redeployments; no live session may carry cross-round-trip state. A controller on either side must be able to cold-boot from the polling queries alone.
- **Issues stand alone.** Verbatim evidence (error excerpts, probe output, commit hashes) — never references to a conversation, log, or working tree the other side cannot see.
- **Evidence over assertion.** Every state claim ("fixed", "live", "cleared") carries the command and verbatim output demonstrating it. Close only when the fix is observable on the serving surface.
- **One issue per failure class.** New instances are comments on the class's issue; recurrence after closure reopens the same issue. Dedup against *all* states before filing.
- **Exactly one turn label** whenever an issue awaits action, flipped by whoever comments; every comment ends with a handback line naming the single next action.
- **An explicit escalation label** routes judgment calls to the human, who answers in-thread.

Everything else — label names, polling cadence, severity tiers, how each side parallelizes its work — is the user's choice. Record their answers in the skeleton's parameters table.

## Install

1. Adapt the skeleton below with the interview answers. Fill every placeholder the interview answered — sides and short names, `owner/repo`, GitHub host, labels, deploy signal, retest command, who answers the escalation label, watermark paths, file location; none of those may survive into the written file. Placeholders that stand for values a *future session* supplies at runtime stay as-is: `<side>`, issue numbers (`<n>`), dates (`<YYYY-MM-DD>`), the format fields in titles, body sections, handback lines, and the provenance line (`<class>`, `<single next action>`, `<repo> @ <commit>`, …), and the command arguments in the §gh fallback table (`<file>`, `<name>`). The two marked conditionals (`<If both sides share one GitHub identity: …>`, `<If the channel repo is public: …>`) resolve per the preflight answers: to keep one, keep only its body text (drop the `<If …:` prefix and the closing `>`); to drop one, remove the whole construct. Show the full adapted text, get approval, then write it to the agreed location in the producer repo as the **single file of record**.
2. Create the labels idempotently: list existing labels first (`gh api -X GET repos/<owner>/<channel-repo>/labels`), create only the missing ones (the creation command below POSTs — make that explicit with `-X POST`) — run the command below once per missing label from the Parameters table, including the origin label (skip the Severity row if its value is `none`). A 422 response is benign only if its body says the label already exists — any other error stops the install per the standing rule. Never change an existing label's color or description without asking. Suggested colors (theirs to change): origin `e4e669`, `needs-<producer>` `d93f0b`, `needs-<consumer>` `0e8a16`, `needs-decision` `0075ca`, severity `b60205`.
   ```bash
   gh api -X POST repos/<owner>/<channel-repo>/labels -f name="<label>" -f color="<hex>" -f description="<one line>"
   ```
3. Add a one-line pointer to BOTH repos' agent-instructions files (CLAUDE.md or that repo's equivalent). This is mandatory, not decorative — without it, no future session knows the channel exists. The line states which side the repo is, where the protocol file lives, and that sessions must run the protocol's §Polling queries at boot and at checkpoints. In the consumer's pointer, name the protocol file by its GitHub location (`<owner>/<producer-repo>` + in-repo path, or the full `blob/` web URL on the configured GitHub host) — never a local filesystem path, which is machine-bound. Never duplicate the protocol itself. Also add each side's watermark state-file path to that repo's `.gitignore` (or `.git/info/exclude` if the user prefers not to commit the rule) unless it is already ignored — it is local state, not source.

## Verify, then hand over

Prove the channel works without waiting for a real incident:

- Run both §Polling queries — they must return cleanly (empty is fine).
- Re-list the labels and confirm every required one exists.
- Confirm both pointer lines exist in the two repos' instruction files.
- Optionally, with the user's approval: file a clearly-marked dry-run issue, walk it through one comment + turn-label flip, and close it.

Finish with an installation summary the user can inspect: producer and consumer `owner/repo`, short names, and local paths; channel repo; labels created vs. pre-existing; protocol file location; both pointer lines; deploy signal; retest command shape; the redaction rule; each side's watermark state-file path; and anything skipped.

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
   carries the command and verbatim output that demonstrates it. Evidence
   is redacted per the rule agreed at install: never secrets, tokens, or
   customer data. <If the channel repo is public: nor private paths or
   internal hostnames.>
4. One issue per failure class, not per instance. New cases in a known
   class arrive as comments on the existing issue.

## Parameters

| Parameter | Value |
|---|---|
| Channel repo | `<owner>/<channel-repo>` (issues) |
| GitHub host | <github.com, or the GHES hostname — if GHES, every session exports `GH_HOST=<host>` before any `gh` command> |
| Sides | `<consumer>` (files issues) · `<producer>` (triages) |
| Origin label | `from-<consumer>` |
| Turn labels | `needs-<producer>` · `needs-<consumer>` |
| Escalation label | `needs-decision` (answered by: <who answers this label>) |
| Severity label | <severity-label, or `none`> |
| Deploy signal | <command + field/header that changes when a fix is live> |
| Consumer retest | <retest command shape, carried in each issue body> |
| Watermark state files | producer: <path> · consumer: <path> (local, git-ignored) |
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
runs the issue's retest → cleared: remove the turn label — done; the
issue stays closed (commenting on a closed issue is normal) · not
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
provenance line, e.g. `provenance: <repo> @ <commit>, <YYYY-MM-DD>`.

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

    # Inbox — everything awaiting MY side. <side> resolves at runtime to
    # this session's own short name from §Parameters; it is the one
    # placeholder that stays in this file. (Closed issues can still
    # carry my turn label until verification runs.)
    gh issue list -R <owner>/<channel-repo> --label needs-<side> \
      --state all --limit 1000

    # Watermark sweep — safety net for label mistakes; the date (YYYY-MM-DD)
    # comes from my side's watermark state file (see Parameters; default:
    # 14 days back if the file is missing):
    gh issue list -R <owner>/<channel-repo> --label from-<consumer> \
      --state all --search "updated:>=<YYYY-MM-DD>" --limit 1000

After each sweep, write today's date back to the state file. The watermark
lives only in that local file — never in this file or in the issues. If
polling latency ever actually hurts, a scheduled poll per side is the next
step — do not add infrastructure before then.

## Controllers

One coordinator session per side owns the channel; workers are spawned per
issue/class and are disposable (never carried across a round-trip — see
Principle 1). Issue traffic (filing, comments, closes, reopens) is normal
agent work on both sides; merges, rebuilds, and deploys follow each side's
own standing human gates. `needs-decision` is the user's channel.

## gh under a restricted PAT

Fine-grained PATs often fail `gh`'s GraphQL-backed subcommands while REST
works. `gh issue list` / `view` / `comment` generally work; fallbacks for
the rest:

| Operation | REST fallback |
|---|---|
| create issue | `gh api -X POST repos/<owner>/<channel-repo>/issues -f title=… -F body=@<file> -f "labels[]=…"` |
| close / reopen | `gh api -X PATCH repos/<owner>/<channel-repo>/issues/<n> -f state=closed` · `… -f state=open` |
| add label | `gh api -X POST repos/<owner>/<channel-repo>/issues/<n>/labels -f "labels[]=<name>"` |
| remove label | `gh api -X DELETE repos/<owner>/<channel-repo>/issues/<n>/labels/<name>` |
```
