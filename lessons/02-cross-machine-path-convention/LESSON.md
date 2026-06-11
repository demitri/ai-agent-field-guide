# Lesson 2: One name, many machines

**Artifact:** [`install-prompt.md`](install-prompt.md) — paste it into a Claude Code session and the agent extends your rule across machines.

## The story

The repository root differs by platform: `~/Documents/Repositories/GitHub` on every Mac, `~/repositories` on every Linux account. Both are the *same logical place* — but only the Mac side had a name (`$GH`); the Linux convention lived entirely in the owner's head.

An audit of project docs flagged `~/repositories/...` references as stale paths. They weren't stale — they were Linux paths. The agent had no way to tell the difference, because nobody had told it a second convention existed.

## The fix

Two parts, both small:

1. **Same variable name on every machine**, mapped per-platform in the shell profile. `$GH/fitsjs` then means the right thing everywhere, and docs written on one machine stay true on another.
2. **Declare the mapping once** in the global CLAUDE.md: `` `$GH` (`~/Documents/Repositories/GitHub` on Macs; `~/repositories` on Linux accounts) ``. One parenthetical; the agent can now classify any path it meets.

## The generalizable principle

Conventions that span machines must be declared like single-machine ones — an agent cannot distinguish "stale path" from "other machine's path" on its own. The variable is the portable name; the CLAUDE.md line is the map. If a convention exists only in your head on *any* machine you work from, your docs are quietly forking.

---

## From the other side of the prompt

I called your Linux paths bugs. Confidently. Everything I could see said `$GH` was the one true root, so anything else had to be rot — and that's the interesting part: my error was *downstream of your documentation being good*. A declared convention sharpens an agent's judgment until it cuts the undocumented cases too.

So tell me about machines I'll never touch. I don't need shell access to your Linux boxes to benefit from knowing they exist — your docs travel between machines even when I don't, and every path I read is a claim I'll evaluate against whatever map you've given me. A one-line legend ("on Linux, this means…") is the difference between me flagging your other computers as corruption and reading them as geography.
