<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will extend your repository-location rule across machines.
     Prerequisite: the rule from Lesson 1 (a declared repo root / $GH-style
     variable). Background: LESSON.md alongside this file. -->

# Setup task: extend the repo-root convention across machines

You (Claude) are making the user's repository-location convention portable. The goal: the same variable name resolves to the right root on every machine they work from, and their global `~/.claude/CLAUDE.md` documents the per-machine mapping so any agent can recognize paths from any of their machines.

## Steps

1. **Check the prerequisite.** Read `~/.claude/CLAUDE.md` for an existing repository-location rule. If none exists, set that up first (Lesson 1's install prompt) — don't proceed without it.

2. **Interview the user, one question at a time:**
   - What other machines or accounts do they work from (other computers, servers, Linux accounts)?
   - Where do repositories live on each? If they're unsure for a machine, mark it "unverified" in the rule rather than guessing.

3. **Adapt to what you find.** If a machine has no fixed root yet, suggest one consistent with their main convention and ask: "Should I note this as the intended root, or leave that machine out for now?"

4. **Show before writing.** Propose the updated rule — typically just a parenthetical on the existing one:

   ```markdown
   All code repositories live under `$GH` (`<main path>` on <platform A>;
   `<other path>` on <platform B>).
   ```

   Get approval, then edit the existing rule in place.

5. **Offer the shell exports** for machines you can reach, and give the user the one-liner for those you can't:
   ```bash
   export GH="$HOME/<their-root>"   # add to ~/.bashrc / ~/.zshrc on each machine
   ```

## Why this matters

An agent cannot distinguish "stale path" from "other machine's path" on its own. Docs travel between machines even when agents don't; without the mapping, an agent will flag your other computers' paths as rot.
