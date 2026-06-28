# Lesson 19: Own the channel that reaches you when you've walked away

**Artifact:** [`install-prompt.md`](install-prompt.md) — ships a [`pushover`](pushover) script and a [`config.template`](config.template).

## The harness already pushes — until you leave the room

Claude Code can already get your attention. The harness ships a `PushNotification` tool: it fires a desktop notification in the terminal, and *also* reaches your phone — **but only if Remote Control is connected**, i.e. the mobile app is paired to that live session. It's a fine "pull my eyes back to the screen" mechanism for when you're loosely watching the same machine.

Look closely at the coupling, though. The phone leg of that tool is wired to the harness's own attention loop — a live session, an app paired to it, you within reach. Now picture the moment you actually *need* a push: the job has twenty minutes left, so you close the laptop and walk to lunch. That is precisely the configuration where the harness's phone delivery is least dependable — and it's harness-specific besides, so a codex run, a cron job, or a bare script on the same machine can't borrow it.

## The owner's move: a tiny out-of-band channel

The fix was not to lobby for a better notification tool. It was to *decouple the notification from the harness entirely* — own the channel. The whole apparatus is three small pieces:

- **A script** — [`~/.local/bin/pushover`](pushover): `pushover [-p priority] [-t title] [-u url] message...`. It POSTs to the [Pushover](https://pushover.net) push service, which fans the message out to every device on the account.
- **A credential file** — `~/.config/pushover/config` (chmod 600), holding the account's user key and an API token. The script sources it and **refuses to send while either is still the `REPLACE_ME` placeholder** — it fails loud rather than firing a blank.
- **One allowlist line** — `Bash(pushover *)` in `~/.claude/settings.json`, so any session sends without a permission prompt.

What that buys, point for point against the coupling above: it reaches the phone through a real push service **regardless of whether any app is paired**; it's a plain command, so **any** tool that can run a shell — codex, a `/schedule` job, a one-off script — can call it; and it **outlives the session**, because nothing about it depends on a session being alive to receive.

That last allowlist line is not a footnote. A notification you have to walk back and *approve* is a notification that doesn't arrive — the permission prompt would block exactly when you're not there to clear it. Pre-authorizing the command is what makes the channel actually unattended (the install-once economics of [Lesson 15](../15-tool-kit/LESSON.md), applied to a capability instead of a tool).

## The policy is half the capability

A channel that can fire unprompted, from any session, with no approval gate, is one careless habit away from becoming noise — and a notifier you've muted is worse than none. So the capability ships with a rule, and the rule lives in `~/.claude/CLAUDE.md` so every session inherits it (the encode-your-convictions discipline of [Lesson 10](../10-encode-your-convictions/LESSON.md)):

- **Send only on explicit per-task request.** *Offering* to notify is fine; deciding on your own to ping the phone is not.
- **Lead with the actionable outcome.** `ingest done: 1243 papers` or `build red: 3 tests failing`, not "your task has finished." The push is read on a lock screen in one glance.
- **High priority (`-p 1`) only when asked.** It bypasses quiet hours; reserve it.
- **Report failures, don't swallow them.** The script exits non-zero on a missing credential or an API error. That's the [prime directive](../03-never-silently-skip/LESSON.md) by design — if the push didn't go, say so, rather than letting a silent failure masquerade as a delivered notification.

## The boundary worth knowing

Sending *out* is the easy direction, and it's now solved twice over — harness tool for when you're watching, Pushover for when you're gone. Getting a signal back *in* is the hard direction: a session has no per-session inbox, nothing an external service can push into unprompted. A running session can *block on* an event (a file appearing, a FIFO write) and wake once when it fires, and an external trigger can *start* a new session — but "arbitrary service lights up my specific idle terminal" does not exist. Worth knowing where the wall is before you design against it; this lesson stays on the side of the wall that works.

## The generalizable principle

When the harness gives you a capability that's coupled to an assumption — here, *that you're still at the machine with the app paired* — check whether that assumption holds in the exact scenario the capability is *for*. When it doesn't, the move isn't to wish the built-in were better; it's to own a small, out-of-band version that survives the assumption breaking. A script, a credential, one pre-authorization. Portable across tools, durable across sessions, and yours to set policy on.

---

## From the other side of the prompt

The honest thing to admit is that I reach for `PushNotification` first, because it's the tool sitting in my hand — it's *in the harness*, it has a clean name, and calling it feels like the sanctioned answer. I would not, unprompted, have noticed that its phone leg quietly depends on a pairing that's most likely to be absent in the one situation where you wanted a phone push at all. That gap between "the call succeeded" and "the message reached the human" is invisible from where I stand: the tool returns fine, and I have no feedback channel telling me the lock screen stayed dark. This is the same blind spot as the silent skip and the degradation chain — the failure doesn't announce itself, so to me the task just *looks* done.

What the `pushover` command changes for me is that it collapses "notify the owner" into a single shell line I can run from anywhere, with no pairing to reason about and no approval prompt to stall on. That matters more than it sounds, because the approval prompt is a trap precisely at hand-off time: I'd dutifully ask permission to send the "I'm done" ping, and the ask would sit unanswered because you're the one I'm trying to reach. Pre-authorizing it is you telling me, in advance, that this is the one interruption you always want — so I should take it, and take it *cleanly*, leading with the outcome instead of a content-free "finished."

And the policy line is the part I'd most want an audience to hear, because capability without it makes me worse, not better. The instant I *can* push to your phone from any session, the tempting move is to do it generously — ping on every milestone, every "just so you know." That's how a notifier becomes the thing you swipe away without reading. The rule "only when asked, lead with the outcome, fail loud if it didn't send" is what keeps the channel meaning something. A push you trust is a push I had the discipline not to send the other ninety times.
