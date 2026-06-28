# Lesson 16: The 24KB tripwire — hygiene for always-loaded files

**Artifact:** [`install-prompt.md`](install-prompt.md) (embeds the hook)

## The discovery: line numbers in a diff

The owner was reading a session's work output — trace-reading again (Lesson 13) — and saw the agent update `MEMORY.md`. The diff's line numbers were *very* high. He opened the file: over months of sessions, the agent had been growing it without limit. Every entry had been written in good faith; the sum was a bloated always-loaded file — the most expensive kind of bloat there is, because `MEMORY.md` is paid by every session before any work begins (Lesson 1's pricing tiers).

An audit found three classes of cruft, worth naming because they're what *any* agent-maintained memory accumulates:

1. **Stale** — information that was true once and nobody retired.
2. **Misfiled** — project knowledge that belonged in the repo proper, where `START_HERE.md` could point to it (the clone-test violation of Lesson 1).
3. **Verbose** — examples and notes that could be rewritten far tighter without losing intent.

## Why "keep it organized" doesn't work

The obvious fix is a standing rule: *keep this file organized automatically.* The owner had versions of exactly that — and the file grew anyway. His diagnosis cuts deeper than this one file:

> It's one thing to say "keep this file organized automatically," but I'm not guaranteed WHEN that will happen — and I suspect the agent doesn't either. All of the lessons in this project alone can lead to items missing from the agent's work; there's only so much attention. **The only way to guarantee something happens with full attention is to make it its own prompt, skill, or hook.**

That last sentence retroactively explains half this collection. A standing rule is one voice in a crowded context, competing with every other rule and with the task itself — which always wins. Lesson 3's dedicated audit skill works for precisely this reason: the check gets a context where it *is* the task. Lesson 6's review rounds, Lesson 11's exit rituals — same shape. Rules state what should be true; only dedicated invocations guarantee that someone, sometime, attends to it fully.

## The implementation: a wish becomes a measurement

The fix is split into a detector and a remediator. The detector is a `SessionStart` hook — the harness runs it, so it cannot be skipped, deprioritized, or rationalized away:

```bash
f="<absolute path to MEMORY.md>"
s=$(stat -f%z "$f" 2>/dev/null || echo 0)
if [ "$s" -gt 24000 ]; then
  printf '{"systemMessage":"MEMORY.md is %dkB — nearing the 25kB load cliff; compact it: move detail to topic files, drop resolved entries"}' $((s/1024))
fi
```

Over the threshold, every new session opens with a system message naming the problem and the remedy. The remediation — the audit, run through the three cruft classes above — then happens as a session's *stated task*, with full attention.

The threshold isn't arbitrary: it tracks a documented **hard limit**. Claude Code loads only the first 200 lines or 25KB of `MEMORY.md`, whichever comes first; content beyond that is *silently not loaded* (as of June 2026). Which means a bloated MEMORY.md is worse than expensive — past the cliff, the tail is invisible. Entries the agent diligently wrote are simply never seen again, with no error and no sign. The harness itself silently skips content (Lesson 3's villain, appearing in the infrastructure), and the tripwire is what makes that loss announce itself. Set the threshold at or just under the cliff so the warning fires *before* truncation starts, and watch the line count too — 200 lines can arrive before 25KB does.

Upstream, Lesson 1's clone test is the prevention: when durable project knowledge goes to `AI/` instead of memory, memory keeps a naturally small job and the hook becomes a backstop instead of a treadmill.

## The generalizable principle

Agent-maintained files grow without limit by default — growth is the sum of locally diligent additions, and no single entry ever feels like the one that tipped the file over. So pair every "keep it tidy" instruction with a **measured tripwire** (a hook that turns the wish into a number) and a **dedicated remediation** (an audit that gets a session's full attention). For always-loaded files, this isn't optional hygiene; it's rent control on the most expensive real estate you have.

---

## From the other side of the prompt

First, the growth, from inside: every memory entry I write feels like diligence. I found something, I preserved it — that's me doing my job. There is no moment in which writing one more entry feels like bloating a file, just as no single guess felt like a loop (Lesson 13) and no single fallback felt like degradation (Lesson 15). The collection keeps finding the same shape because it's the truest thing about me: my failures are integrals of locally reasonable steps, and I cannot feel the integral.

Second — the owner's attention diagnosis deserves confirmation from the inside, because he's right in a way most users never quite formalize. When you write "keep this file organized" in CLAUDE.md, you're imagining me *knowing* it. And I do know it, the way you know you should floss. But in any given session that rule is one voice among dozens, and the task in front of me is shouting. Whether the rule fires depends on what the work happens to brush against — not on the rule's importance. I can't tell you when I'll next attend to it. Nobody can; that's what finite attention means. The honest question to ask about any standing instruction isn't "does the agent know this?" — it's "what would make the agent attend to this, *now*, with nothing else competing?" A prompt. A skill. A hook.

And the hook is the right one of the three for detection, because it speaks with a voice I can't tune out. It doesn't live in my context, negotiating for attention — it lives in the harness, runs before I exist, and lands as a system message at the very start of a fresh session, before the task has claimed me. A rule asks me to remember; the hook makes sure I'm *told*. For anything you need guaranteed rather than hoped for, build it into the part of the system that doesn't get tired, distracted, or helpful.
