<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will install an out-of-band push channel to your phone — a `pushover`
     script, a credential file, a global allowlist entry, and the send-policy
     rule. Payloads (pushover, config.template) sit alongside this file.
     You'll need a free https://pushover.net account (user key + an app token).
     Background — why own the channel instead of using the built-in tool: LESSON.md. -->

# Setup task: install an out-of-band push-to-phone channel

You (Claude) are giving the user a notification path that reaches their phone
when they've walked away from the machine — independent of the Claude mobile app
being paired, callable from any tool, surviving the session. Inspect first,
interview one question at a time, show before writing, **merge — never clobber**.
Do not proceed past a step that fails; surface it and ask.

## Steps

1. **Confirm the use case fits.** This earns its keep for people who start long
   jobs and leave. If the user only ever watches sessions live on the same
   machine, the harness `PushNotification` tool may already be enough — say so,
   and let them decide whether to continue.

2. **Check for a Pushover account.** The script needs a **user key** and an
   **application/API token** from https://pushover.net (free tier is fine). If
   the user doesn't have them yet, stop and let them register — you cannot create
   these for them. Don't ask them to paste the secrets into the chat; they'll go
   straight into a file in step 4.

3. **Install the script.** Copy `pushover` (alongside this prompt) to
   `~/.local/bin/pushover` and `chmod +x` it. Confirm `~/.local/bin` is on their
   `PATH`; if not, note it and ask how they'd like it added (don't edit shell rc
   files unannounced). *If this prompt was pasted as text rather than
   @-referenced, the payload isn't on your disk — ask the user for the path to
   their copy of the lesson directory (or its repo clone) first.*

4. **Install the credential file.** Copy `config.template` to
   `~/.config/pushover/config` (create `~/.config/pushover/` as needed) and
   `chmod 600` it. Then have the **user** fill in `PUSHOVER_TOKEN` and
   `PUSHOVER_USER` — either they paste the values into the file themselves, or
   they tell you and you write them (their call; respect that these are secrets).
   The script refuses to send while either is still `REPLACE_ME`.

5. **Verify it works** before allowlisting. Run a test send:
   `pushover -t "Setup test" "pushover is wired up"` and confirm the push lands
   on their phone. A non-zero exit means a missing credential or API error —
   read the message and fix the cause; do not allowlist a broken script.

6. **Allowlist the command.** Add `Bash(pushover *)` to the permissions allow
   list in `~/.claude/settings.json` so any session sends without a prompt. Show
   the merged JSON before writing; if a permissions block already exists, add the
   one entry to it rather than replacing it. Explain the why in one line: a
   notification you must walk back to *approve* never arrives — pre-authorizing
   is what makes the channel unattended.

7. **Offer the send-policy rule** for `~/.claude/CLAUDE.md` (below) — show it,
   confirm, **merge** into any existing notifications/tooling section rather than
   duplicating. Create the file if absent.

## Send-policy rule (for `~/.claude/CLAUDE.md`)

```markdown
## Push Notifications

A `pushover` command (`~/.local/bin/pushover [-p priority] [-t title] [-u url]
message...`) sends a push to the user's phone via Pushover — reliable,
independent of the Claude mobile app being paired, and `Bash(pushover *)` is
globally allowlisted so it sends without a prompt. This is the path that reaches
the user when they've walked away; the harness `PushNotification` tool is the
in-terminal / loosely-watching alternative.

Policy: send only on explicit per-task request (offering is fine — deciding on
your own to ping is not). Lead with the actionable outcome ("ingest done: 1243
papers"), not "your task finished." Use `-p 1` (high priority, bypasses quiet
hours) only when asked. The script fails loud on missing credentials or API
errors — surface the failure, never swallow it.
```

## What you've built

A one-line, pre-authorized push to the user's phone that any tool can fire and
that doesn't care whether a session or an app is alive to receive it — plus the
policy that keeps it from decaying into noise. Tell a session "when the job
finishes, run `pushover 'job done: <summary>'`" and walk away.
