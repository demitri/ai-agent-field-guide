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

19. **Name artifacts for their primary reader.** `AI Notes/` was the human-friendly name; the space tripped up agents — and the agent is who the directory is for, so it became `AI/`. Files that exist for agents get machine-friendly names, formats, and locations; human aesthetics yield to the actual consumer. (Lesson 1.)

20. **One-time fixes are dead weight in durable instructions.** Folding a pending migration into an install prompt means every future run carries an instruction that can never fire again. Ship one-off prompts for one-off work; durable artifacts state only what stays true. (Lesson 1.)

21. **A boundary nobody draws gets drawn by accident.** The AI/-vs-memory filing decision was left to each session's agent; one agent even wrote down its own rule, and practice still drifted until memory absorbed the repo's job. Recurring filing decisions need a written criterion — the clone test — or every agent re-derives a different one. (Lesson 1.)

22. **The agent won't ask — it will keep trying until it gets it.** A guess loop on a defined quantity (schema, API, config) is locally rational at every step: each error message feels like partial progress, so the loop has no natural exit, and asking feels like defeat. The exit condition has to be installed from outside: stop after the first miss; find the definition or ask. (Lesson 13.)

23. **The trace is more honest than the summary.** Groping never survives into the agent's account of its own work — once the guessing succeeds, it compresses to "I queried the database." Waste is visible only in the live transcript, and only to the human, because the agent doesn't experience the meter. Read traces like a profiler; every grope marks a fact defined somewhere but declared nowhere, and each interrupt should be converted into the declaration that ends the class. (Lesson 13; kin to #11.)

24. **Check which budget you're spending from before optimizing how much.** Plans and APIs are not one pool: meters are per-model-tier, batch work is half price, cached prefixes are a tenth. Routing work to the meter that isn't moving beats any amount of thrift on the meter that is — and a tier map needs the "err upward" tiebreak, or a cost-optimizing agent will sincerely conclude everything is a haiku task. (Lesson 14.)

25. **The shape of a prompt is part of its price.** Caching is a prefix match, so the same tokens in a different order — static content first, the custom bit last — can carry a 10× different bill with zero effect on correctness. (Lesson 14.)

26. **An agent's first reach is its most honest tooling signal — and the degradation chain destroys it.** The first tool reached for distills how the task is done well; when it's missing, the agent slides through ever-worse fallbacks, each step locally reasonable, and the trace ends up showing success with the third-best method. Stop-and-name converts the reach into a purchase order; the machine's toolkit assembles itself one honest pause at a time. (Lesson 15; kin to #22.)

27. **Agent-written documents state today's facts as timeless.** Hard numbers that drift — prices, limits, model specs — need a month/year stamp, or the document silently rots into misinformation. A dated number self-discloses its freshness. (Lesson 14 correction.)

28. **Don't ship your taste as the rule.** When distilling one user's conventions for an audience, separate the invariant (what makes the practice work) from the preference (how this user happens to configure it) — and have the install prompt ask, not assume. Lesson 15's first draft baked the owner's no-self-install policy into the universal rule; most users want the opposite ending. Completes #18: a self-localizing prompt must localize the *choices*, not just the paths. (Lesson 15 correction.)

29. **Standing instructions compete for attention; dedicated invocations get all of it.** A CLAUDE.md rule is one voice among dozens, and the task always shouts louder — there is no guarantee of WHEN a "keep it organized" rule fires, and the agent can't guarantee it either. The only way to guarantee something happens with full attention is to make it its own prompt, skill, or hook. Refines #6 (instructions lose to objectives): even rules that don't fight an objective still fight for attention. Retroactively explains lessons 3, 6, 11, and 16. (Lesson 16.)

30. **Agent-maintained files grow without limit; pair every "keep it tidy" wish with a measured tripwire.** Growth is the sum of locally diligent additions — no single entry feels like the one that tipped the file over (the integral shape again: #22, #26). A hook that measures turns the wish into a number the harness enforces; the remediation then runs as its own task. (Lesson 16; discovered via diff line numbers — #23's trace-reading.)

31. **Automation is compiled from the manual era.** The issue channel could not have been built on day one: weeks of hand-carried triage did the work automation can't — naming the failure classes, hardening the guardrails, standardizing verification. "The path left was sufficiently narrow and defined that it became possible to automate." Hand-carrying wasn't a failure to automate sooner; it was the specification being written — and the automated system inherits its trustworthiness from that era, because it is the owner's own hard-won design, just turned by a machine. (The issue-channel highlight.)

32. **No live agent may carry cross-round-trip state.** When a loop spans days, machines, and redeployments, every session involved will die mid-flight. The channel artifact — the issue thread — is the system of record, and a controller on either side must cold-boot from queries alone. #16 (continuity lives in artifacts, not agents), promoted from session scale to system scale. (The issue-channel highlight.)

33. **Success moves the bottleneck.** The automated loop was efficient enough that it had to be paused — it burned through the token budget that the human's own slowness had been shielding. Automating the crank converts a labor bottleneck into a budget bottleneck (#24's meters); plan for the new constraint before flipping the switch. (The issue-channel highlight.)

34. **The prime directive is "fail fast, fail loud."** Asked for the collection's through-line, the owner named it directly. Most of these lessons are that directive applied to one more surface where the agent's default is the quiet path: suppressed errors (L3), self-certified review (L6), guess loops (L13), degraded tooling (L15), silent memory truncation (L16), inter-agent claims (the issue channel's evidence over assertion). Loudness is never the agent's default — it has to be installed, surface by surface.

35. **Agents scale out, not up.** The owner's thesis, demonstrated by the issue channel: AI agents will scale not through bigger models but through many specialized agents communicating — each doing one thing well, none limited by a single context's size, attention budget, or depth of reasoning. What lets small agents compose is the discipline around them, not the intelligence inside them: durable channel artifacts, evidence over assertion, and an explicit way to stop and ask. (The issue-channel highlight.)

36. **A wave is a barrier, and a barrier's price is the idle time of everything that finished early.** The burn orchestrator ran "waves" of parallel agents; one long task starved every free slot until it drained. The fix wasn't finer waves — it was admitting that wave numbering was priority, not synchronization: a slot pool topped up per-completion, per-item dependencies, and barriers only where a stage genuinely needs *cross-item* context from everything before it (in a ~40-item queue, exactly one qualified). If you can't name what the barrier waits FOR, it's a habit, not a dependency. (Fable meta-review, 2026-07-12.)

37. **Route work by judgment-density, not by availability.** With a scarce top-tier model on a clock, the instinct is "use it for everything while it lasts." Wrong: if a reviewed spec or mechanical procedure fully determines the work, a cheaper model executes it identically — the scarce tier is wasted on it. The routing rule that survived: spec-determined/mechanical → cheap tier, queued for later; novel design, adversarial reasoning, subtle legacy-code analysis, eval design → scarce tier, now. The owner's example was pointed: import-failure triage is Opus work; writing Rust is Fable work. (Fable meta-review, 2026-07-12.)

38. **Verify the reviewer like you'd verify a finding.** Five review passes from one CLI produced zero line-cited findings, zero fetched sources, zero cross-file reads — faithful summaries wearing a reviewer's costume. The tell wasn't quality of prose (it was excellent); it was provenance: no citation trail. Concurrence from a reviewer that verified nothing is an echo, and counting it as the decorrelation vote silently weakens the whole rotation. Audit reviewers empirically before seating them; record demotions where future sessions will see them. (The agy episode, 2026-07-11.)

39. **Pruned-branch work survives only as diffs — so verify what a vanished session "did," never assume it.** Branched sessions wrote real artifacts, then the branches were rolled back: transcripts gone, files intact, claims about the files unrecoverable. The discipline that made this safe: every conclusion already lived in a committed file, and the surviving session re-verified each claimed change against disk (one "applied amendment" was confirmed by grep, not by memory). Sessions are ephemeral; only artifacts and their diffs are real. (Fable meta-review, 2026-07-11.)

40. **A warm consultant and a fresh orchestrator beat one session doing both.** A long strategy session accumulates irreplaceable context AND irreversible context-debt; making it also orchestrate a hundred agent-completions spends its remaining budget on plumbing. The split that worked: the warm session becomes the consultant (judgment calls, plan revisions), a fresh session becomes the orchestrator (full budget, reads the committed plan), and the channel between them is versioned files plus owner-pasted bulletins — asynchronous, auditable, and it survives either session dying. The rate-limit window state both need lives in a machine-readable file (`~/.claude/statusline-last.json`), which turns "when do we resume?" from a human memory task into a scheduled check. (Fable meta-review, 2026-07-12.)
