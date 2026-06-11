<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will install the /endsession and /park skills (payloads in
     endsession/ and park/ alongside this file). Background: LESSON.md. -->

# Setup task: install the session-lifecycle skills

You (Claude) are installing two skills that ritualize how sessions end: `/endsession` (audit before a clean close) and `/park` (suspend mid-work into a resume document).

## Steps

1. **Ask about their working style first.** These skills earn their keep for people running multiple concurrent sessions/projects. If the user runs one session at a time to completion, `/endsession` alone may be all they need — say so.

2. **Install `/endsession`.** Copy `endsession/SKILL.md` (alongside this prompt) to `~/.claude/skills/endsession/SKILL.md`. It is fully general — no adaptation needed.

3. **Install `/park` — with adaptation.** Copy `park/SKILL.md` to `~/.claude/skills/park/SKILL.md`, then check its conventions against this user's world:
   - Park docs land in an `AI/in_flight/` directory at repo root. Ask whether they have (or want) that convention; adapt the path in the skill if they keep agent files elsewhere.
   - The skill assumes git repos. If they work outside repos, ask where parked-session docs should live.

4. **Explain the usage rhythm:** `/endsession` when wrapping up ("anything to close out?"); `/park` when closing mid-work ("I need to reboot", "park this session"); `/park list` to inventory parked work; `/park resume <n>` to pick one up in a fresh session.

5. **Set expectations for park-doc quality** — it's a succession document, not a log: what was done, enough detail for a future agent to retrace, and the verbatim final summary the user hasn't dealt with yet. The pruning is deliberate: a long session sheds its stale information at park time.
