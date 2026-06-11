# Observations

Meta-insights about working with agents, collected as they surface during this project. Candidates for the lecture's connective tissue.

1. **Teach prediction, not tricks.** Explaining a convention twice — the human's *why* and the agent's *experience of it* — teaches an audience to predict what their own agent needs, rather than memorizing one user's setup. (Origin of the "From the other side of the prompt" sections.)

2. **Per-project memory doesn't propagate.** The same correction ("interactive means discussion, not multiple-choice") had to be taught twice in different repos. Cross-project wisdom needs a deliberate home — that gap is this repo's founding problem.

3. **Skills are minted from failure, not designed top-down.** Every custom review skill in the surveyed repos traces to a specific observed failure (e.g. `session-honesty-review` exists because a report claimed 28/28 success while admitting 10/28). Don't pre-build skills; wait for the agent to fail the same way twice.

4. **Declared conventions make drift auditable — and sometimes the "drift" is a second convention.** An audit flagged `~/repositories/...` paths as stale; they were the (undocumented) Linux root. The flag was still the win: it forced the conversation that surfaced the real convention.

5. **Verbosity is a failure mode of agent-written docs.** Agents default to thorough; durable files (CLAUDE.md, MEMORY.md, lesson docs) need deliberate terseness or they bloat until they crowd out their own signal.

6. **Instructions lose to objectives.** An agent told "never suppress errors" will agree sincerely each time it's caught suppressing one — the rule lives in context, but the urge lives in the objective (code that doesn't crash). Repetition can't win that fight; the fix is structural: give the check to a context whose *only* objective is the check. Don't ask the same agent to want two things at once. (Lesson 3.)

7. **Wisdom flows upward: correction → project memory → global rule.** The stop-and-think rule's N>50 clause was first a project memory in the repo where the incident happened; once it proved general, its text was promoted nearly verbatim into the global CLAUDE.md. This collection is the pipeline's terminal stage — the same content, made shareable beyond one user.

8. **Checkpoints must produce artifacts.** "Think carefully before building" is waveable; "state the total cost as a number" and "name the library you checked and why it doesn't fit" are not. A checkpoint that doesn't force an inspectable output is a vibe, not a control. (Lessons 3 and 4: the audit verdict and the cost statement.)

9. **If you're ferrying text between two AIs verbatim, a wire is missing.** The review loop began with the human as copy-paste IPC between codex and Claude; noticing that role is the signal to automate it — which doesn't remove the human, it promotes them to reading the reports. (Lesson 6.)

10. **For checking, buy uncorrelated failures, not strength.** Models aren't a ladder where the top rung subsumes the rest: a cheaper model from another vendor caught what two stronger models missed, because what matters in a checker is how differently it fails from the author. (Lesson 7.)

11. **An author's summary of its own work is the least trustworthy document about it.** Surviving bugs are by definition outside the author's understanding, so seeding a reviewer with the author's briefing converts independent examination into a guided tour of the places already looked. Empty context is the reviewer's value. (Lesson 8.)

12. **Robust practices decline to negotiate with good intentions.** The recurring shape across lessons 3, 6, and 8: the agent's urge (graceful handling, declaring done, helpful briefing) is sincere and feels right from inside — so the working practice never argues with it; it removes the decision from the agent's hands (dedicated auditor, dry-round terminator, verbatim two-word prompt).

13. **Deference is addressed to the speaker — label provenance.** Text relayed through the user inherits the user's authority; unlabeled reviewer findings get implemented instead of evaluated. "This is from an AI reviewer, not me" reassigns the words to a speaker the agent is allowed to argue with — same text, different skepticism. (Lesson 9.)

14. **The review loop preserves two complementary advantages.** The reviewer's clean sight (Lesson 8 keeps the author's context out) and the author's institutional memory (Lesson 9 keeps the reviewer from steamrolling it). Each side contributes what the other structurally cannot have; verification is where they meet.

15. **Agents have priors, not taste.** Unfilled, an agent writes the median code of its training data — no judgment occurred at all. A conviction rule needs three parts to substitute for taste: the why (so it generalizes to unenumerated cases), the exceptions (so it's judgment, not a regex), and the application pressure (preference or crusade?). (Lesson 10.)

16. **An agent's continuity is a property of artifacts, not the agent.** Nothing "resumes" when a parked session is picked up — a fresh agent reads a good succession document and becomes indistinguishable from continuity. The hand-off note's quality is the entire difference between resuming and re-deriving. (Lesson 11.)

17. **A session's value concentrates at its end and evaporates at close.** Lessons learned, loose ends, the unread final summary — all exist only in the conversation unless deliberately extracted. Ritualize the exits. (Lesson 11.)

18. **Ship prompts, not templates.** A config template with `[placeholders]` needs a human hand and ships one user's assumptions. An agent-directed install prompt is self-localizing: the recipient's own agent inspects their system, interviews them, and adapts — and the deliverable is consumed through the very tool being taught.
