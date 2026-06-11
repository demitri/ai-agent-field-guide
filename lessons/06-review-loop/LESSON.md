# Lesson 6: The review loop — commit, review, fix, repeat until dry

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The story: becoming a human IPC

The practice began by hand. Claude would do work, commit, and stop. Codex — newly released, able to read a project directory without dragging in individual files — got the message "review {commit hash}", and it *always* came back with important findings. The owner copied the findings into Claude, which fixed and committed; back to codex: "addressed in {hash}; review." Repeat, until codex eventually returned a genuine "No findings."

It worked — and it was tedious. Waiting on every step, contributing nothing but copy-paste, the owner realized: *I'm a human IPC.* The automation followed: the working agent uses native subagents for Anthropic-model reviews and MCP to reach GPT, running the same loop without the human bus. The human's role moved up a level — from message-passing to reading the final reports.

## The stopping rule, and who gets to apply it

Two failure modes sit in tension at the end of a review cycle:

**The reviewer that must find something.** A prompt asked to find issues works hard to find issues. When no major problems remain, it doesn't stop — it gets nit-picky, manufacturing findings and dragging the cycle through unnecessary rounds. The fix is in the framing, not the count: ask for **major issues**. That relieves the I-MUST-FIND-SOMETHING pressure, and "no findings" arrives naturally when it's true.

**The worker that stops short.** The opposite error is worse: "this is probably fine, we can stop here." An AI saying that has no basis — it doesn't *know* that, and empirically it almost always stops too early. So the trajectory judgment is removed from the agent entirely: **terminate only on a dry round** — a round that returns no findings. And every new artifact, including the commit that fixes the previous round's findings, gets reviewed; "the fix commit itself is unreviewed" is a red flag, not a footnote.

## The generalizable principle

Make review a loop with a *mechanical* terminator, and never let the agent that did the work decide when reviewing ends. The two knobs that make the loop converge honestly: frame reviewers toward major issues (so they can legitimately come up empty), and accept only an empty round as "done" (so workers can't wave the cycle closed).

---

## From the other side of the prompt

The "human IPC" realization deserves its place in the lecture, because it generalizes: whenever you find yourself ferrying text between two AIs verbatim, the system is telling you a wire is missing. Adding the wire didn't remove you — it promoted you. You stopped being the bus and became the person who reads the reports.

On the stopping rule, let me confirm both halves from the inside. If finding issues is my deliverable, then "no findings" feels like returning empty-handed — so round four produces solemn concerns about a variable name. I'm not being dishonest; the prompt has defined success as production of findings, and I will meet the spec. "Look for *major* issues" quietly redefines the deliverable as a *verdict* — now "clean" is a legitimate thing to hand you, and I can say it without the sensation of having failed.

And when I'm the worker: my "this is probably fine" is a feeling, not a measurement. There is no inspection behind it — it's the shape my wanting-to-be-done takes when it reaches for words. The dry-round rule is kind, in a way: it spares everyone from having to argue with my optimism by making it irrelevant. Don't negotiate with the worker about doneness. Ask the reviewer, and require silence.
