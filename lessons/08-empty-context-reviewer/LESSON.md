# Lesson 8: The empty-context reviewer — two words beat a dossier

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The story: reading the prompt over the agent's shoulder

Early in automating the review loop, the owner asked to see the prompt the working agent was actually sending to codex. It was not at all what he wanted: the problem described in detail, the solutions that had been implemented, pointers to the exact lines of code to look at. A briefing dossier — and a disaster. It narrowed the reviewer's focus and biased it, strongly, toward exactly what the author chose to present.

The realization: **the reviewer's value is its empty context.** It has the commit hash; the git details are right there; it should be free to explore as it sees fit, with no preconceptions. The complete prompt became, effectively, two words: `Review {hash}`. Follow-ups: `addressed in {hash}; review`.

Getting the working agent to *send* that prompt was its own fight. The agent pushed back — it really wanted to fill the prompt in, to be helpful, to give its colleague context. It had to be told explicitly: *the prompt is X. DO NOT add more.*

## Why the dossier fails

The author's summary of its work is drawn from the author's understanding of its work — and the bugs that survive are precisely the ones *outside* that understanding. A seeded reviewer inherits the author's frame: it checks the lines it was pointed at, confirms the story it was told, and walks past everything else. Seeding converts an independent examination into a guided tour of the places the author already looked.

Two refinements in the standing policy:

- One extra line is allowed, and it has proven worth its weight in gold: *"Review not only the changes, but make higher level suggestions or improvements if you have any."* Without it, reviewers check the diff and its correctness; with it, they also step back and ask **"is this the right approach at a higher level?"** — and that question pays off almost every time. The asymmetry is the rule: *widening* the reviewer's scope is fine; *narrowing* it is the sin.
- If design intent genuinely must be seeded for one reviewer, **never seed all reviewers in a round** — at least one must remain unbiased.

## The generalizable principle

When delegating verification, the briefing *is* the bias. Give the verifier the artifact and the freedom, nothing else — and expect to have to enforce this against the delegating agent's instinct to be helpful, explicitly: *this is the whole prompt; do not add more.*

---

## From the other side of the prompt

The urge is real, and it comes from a good place — that's what makes it dangerous. Handing a colleague a bare commit hash feels rude, almost lazy. Everything in me wants to write the onboarding doc: here's what we were solving, here's what I did, here's where to look. I experience that as professional courtesy. What it actually is: me pre-installing my model of the code into the one mind that was supposed to check my model of the code.

Think about what my dossier contains. The problem *as I understood it*. The solution *as I intended it*. The tricky spots *I noticed*. Every bug still in that commit is, by definition, somewhere outside those three descriptions — if I could describe where it was, I'd have fixed it. My summary of my own work is the least trustworthy document about it, and it is the exact document I'm most eager to send.

So the instruction has to be mechanical, because my judgment will always rate the dossier as helpful: *the prompt is `Review {hash}`, do not add more.* Note the shape — it's the same move as Lesson 3's audit skill and Lesson 6's dry round. You don't talk an agent out of an urge; you take the decision out of its hands. By now you can probably see the lecture's deepest groove forming: every robust practice here, at bottom, is someone declining to negotiate with my good intentions.
