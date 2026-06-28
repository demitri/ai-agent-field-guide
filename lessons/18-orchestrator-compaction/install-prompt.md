<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will set you up to do directed compaction on orchestrator-shaped
     sessions, adapting the template (alongside this prompt as
     compaction-template.md) to your projects. To do it by hand: copy
     compaction-template.md, fill the {{slots}} for your session, and pass it as
     the argument to /compact. Background: LESSON.md. -->

# Setup task: install directed compaction for orchestrator sessions

You (Claude) are helping the user compact long sessions that have become
*orchestrators* — sessions whose value is the live, multi-session operating
state, not the per-item detail. Inspect first, ask one question at a time, show
proposed text before writing, merge — never clobber.

## Steps

1. **Check the shape fits.** Ask whether the user runs sessions that evolve into
   orchestrators: a session that ends up generating prompts for clean sessions
   and integrating their results back to decide what's next. If they never do,
   this lesson doesn't apply — say so. (Related: Lesson 11 for parking/closing
   sessions at their boundary; Lesson 13 for why long sessions get expensive to
   keep alive.)

2. **Explain the failure mode** that default `/compact` falls into: it's
   content-blind and compresses everything at one rate, smearing the
   irreplaceable orchestration state at the same ratio as detail that's already
   safe in the repo.

3. **Establish the clone-test discriminator.** Ask where this user's durable
   record lives for the work they orchestrate (a git repo, a queue/state file, a
   changelog). That answer is the dividing line: anything recoverable from there
   compresses to a pointer; anything that exists only in the session stays
   verbatim.

4. **Place the template.** The fill-in template is `compaction-template.md`,
   alongside this prompt. If this prompt was @-referenced, the file is on disk;
   if it was pasted as text, ask the user for the path to their copy of the
   lesson directory first. Offer to put the template where they can reach it
   quickly — options, in order: a project `AI/` file they @-reference; a global
   snippet; or, if they want it as a command, wrapped as a
   `/compact-orchestrator` skill that prints the filled template. Ask which, then
   adapt the durable-record name from step 3 and any paths to this user's world.

5. **Set the quality bar.** The compaction is a succession document for the
   session's own future context (Lesson 11, written in place). The hard part is
   the NET TEST: name the orchestrator's one-sentence job and require the result
   to preserve the ability to do it. Without that test it degrades back into
   "just make it shorter," which is what smooths the orchestration loop away.

6. **Show everything before writing**, then write.
