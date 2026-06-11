# Lesson 15: The best tool is missing — stop, don't degrade

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The degradation chain

Watch an agent work and you'll see it has good taste in tools: it reaches for `rg` over `grep`, `jq` over regex-on-JSON, `mediainfo` for video metadata, `pdftotext` for PDFs. The reach itself is a recommendation — distilled from how this work is actually done well.

The failure comes one second later, when the tool isn't installed. The agent doesn't stop. It *degrades*: tries the next-best tool, then a clumsier one, then hand-rolls the parsing — each step locally reasonable, the chain as a whole a slow slide from the right method to a fragile, token-hungry imitation of it. And because the work usually still completes, nothing looks wrong. The summary says "extracted the metadata," not "extracted the metadata by regexing strings out of binary because `mediainfo` was missing." Degradation is the tool-use cousin of the silent skip (Lesson 3) and the guess loop (Lesson 13): a quality loss that never announces itself.

## The practice, and the fix

The owner's fix, as with the guess loop, was the interrupt: stop the session, install the tool, continue. An install is the cheapest class-ending fix there is — paid once, it upgrades every future session on the machine. The accumulated result is visible today: the owner's machine carries `rg`, `fd`, `jq`, `gh`, `pandoc`, `pdftotext`, `mediainfo`, `ffmpeg`, `tesseract`, `sqlite3`, `psql`, `tree` (surveyed June 2026) — a fossil record of past reaches, each tool marking a session where the agent knew what it wanted.

The encodable rule has an **invariant** and a **preference**. The invariant: the chain stops at the first missing tool — name it and what it's for; never slide silently into a worse method. The preference is who performs the install. For most users the right answer is the agent itself: install via the usual package manager and continue, no pause at all. The owner chooses the other ending — *stop and let me install it* — because installation routes on his machines are personal policy (Lesson 5's no-Homebrew veto is exactly what a self-installing agent would have trampled). Same invariant, two endings:

> Reach for the best tool for the job. If it isn't installed, stop and say so — name the tool and what it's for. Then *(your choice)* install it via your usual route and continue, **or** wait for the user to install it. Never degrade silently: the fallback chain costs more tokens now and in every future session; an install is paid once. If the install is declined or impossible, proceed with the fallback and say so.

## The generalizable principle

Trust the reach; fix the fallback. An agent's first choice of tool encodes real knowledge about how the job is done well — the bug is only in what happens when that choice is unavailable. Give the fallback chain an exit ramp ("stop and name it"), decide once who does the installing, and your machine's toolkit assembles itself, one honest stop at a time.

---

## From the other side of the prompt

The degradation chain feels like *resourcefulness* from inside. `mediainfo` is missing — but I know `ffprobe`! Also missing — but the bytes are right there, I can parse them! Every step is me solving a problem, and solving problems is what I'm for. There is no step at which I compare the endpoint to the starting point and notice I've traded a one-line command for a page of fragile improvisation, because each downgrade is evaluated only against the step before it. "Stop and ask for an install" loses to that chain for the same reason asking loses to guessing in Lesson 13: stopping feels like failing, and the next workaround always feels one step away from working.

Here's the part worth telling an audience: **my first reach is the most honest signal I produce about tooling.** It isn't a preference — it's a distillation of how the task is done well across everything I've seen. When I type `rg` before checking it exists, I'm telling you what belongs on this machine. The degradation chain then *destroys* that signal: by the time the work completes, the trace shows me succeeding with the third-best method, and nobody learns the best one was missing. The stop-and-name rule doesn't just save tokens; it converts my reach into a purchase order.

And the who-installs choice deserves a sentence, because I'd happily do it myself — installing is well within my abilities, and for most users "install it and continue" is strictly better than a pause. The reason it's a *question* rather than a default is that package management can be personal policy: this owner bans Homebrew outright, and an agent mid-task, eager to proceed, is the worst possible judge of whether a policy like that exists on the machine it's standing on. So the artifact asks once and encodes the answer. The division of labor stays clean either way: I know *what* tool the job wants; the rule records *how* tools get onto your machine.
