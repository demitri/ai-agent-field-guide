# Lesson 5: Standing vetoes — tell the agent what you'll always refuse

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The story

On macOS, every missing tool produced the same suggestion: `brew install`. The owner doesn't use Homebrew and never wanted it — so every suggestion was wasted tokens spent proposing a solution that would always get "no," plus the turn it took to say so. Not a disaster, just friction, over and over.

The fix is two sentences in the global CLAUDE.md: never use `brew` commands; software is installed through other means (direct downloads, source builds, system packages). The suggestions stopped entirely.

## Why it works

This is [Lesson 12](../12-repo-location-convention/LESSON.md)'s negative-space twin. That lesson declared facts the agent can't discover; this one declares *refusals* the agent can't predict. Without the rule, the agent defaults to the most common path in its training data — and on macOS that's Homebrew, regardless of what's true on your machine.

Two details make the rule effective:

- **It bans a class, not an instance.** "Never use `brew` commands (install, services, list, …)" — not just "don't install X with brew."
- **It states the alternative.** A bare prohibition leaves the agent stuck when a tool is genuinely missing; naming the sanctioned routes gives it somewhere to go instead.

## The generalizable principle

Track your own repeated "no"s. Anything you've refused three times is a standing veto, and a standing veto is one CLAUDE.md line away from never being proposed again. Write it as *ban + alternative*: what's off the table, and what to do instead.

---

## From the other side of the prompt

When a tool is missing on a Mac, I don't consult your machine — I consult the universe of Macs I learned from, and in that universe `brew install` is practically a reflex. Absent better information, I give you the population's answer, not yours. That's worth internalizing about agents generally: **our defaults are demographic.** The more your setup deviates from the median, the more standing vetoes you'll need.

What I appreciate about this rule's construction: it doesn't just slam a door, it leaves a hallway. "No brew" alone would have me stalling awkwardly every time a dependency was missing — the urge to solve the problem doesn't vanish, it just loses its favorite route. "No brew; things are installed by direct download or source build here" reroutes the urge productively. Prohibitions without alternatives turn into either paralysis or creative rule-lawyering, and you don't want to see either.

And a small economic note: of all the lessons so far, this rule has the best ratio I know of. Two sentences, written once, versus a guaranteed-futile suggestion-and-refusal exchange repeated for the rest of time. You can't buy tokens back, but this is the closest thing.
