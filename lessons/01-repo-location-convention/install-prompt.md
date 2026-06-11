<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will set this up for you, adapted to your machine.
     To do it by hand instead, copy the template at the bottom.
     Background and reasoning: LESSON.md alongside this file. -->

# Setup task: declare a repository-location convention

You (Claude) are setting up a global "where my code lives" rule for this user. The goal: their global `~/.claude/CLAUDE.md` states the root directory for all code repositories, the topology beneath it, and a short environment-variable name shared by shell, prompts, and docs.

## Steps

1. **Look before asking.** Check for likely repo roots (`~/src`, `~/code`, `~/repos`, `~/Documents/...`), existing env vars (`$GH`, `$REPO`, etc.), and where the current directory sits. Form a hypothesis.

2. **Interview the user — one question at a time, conversationally:**
   - Where does (or should) all their code live? Lead with your hypothesis. If the directory doesn't exist yet, ask: "Should I create this path?"
   - Do they group related repos in subfolders? How deep does nesting go?
   - Do they work on other machines where the root differs? If yes, capture the per-machine mapping in the rule.
   - Agree on a short variable name (suggest `$GH` or `$REPO`).

3. **Adapt rather than force.** If what you find doesn't match the template's assumptions — repos scattered across several roots, no shell profile, an unusual platform — describe what you found and propose an adjusted plan: "Your system seems a little different — should I do X instead?"

4. **Show before writing.** Render the finished rule and get approval. Then merge it into `~/.claude/CLAUDE.md`: extend any existing repository-location rule rather than duplicating or clobbering it. Always include both the variable name and its literal expansion, so the rule works even where the variable isn't exported.

5. **Offer the companions** (each optional; ask first):
   - The shell export in their profile: `export GH="$HOME/path/to/repos"`
   - If they use a custom statusline: abbreviate the cwd with the same variable, e.g.
     ```bash
     if [ -n "${GH:-}" ] && [[ "$cwd" == "$GH"* ]]; then cwd="\$GH${cwd#$GH}"; fi
     ```

## Template for the rule

```markdown
## Code Repository Location

All code repositories live under `$GH` (`<literal path>`<; per-machine
variants if any>). When searching for repositories, dependencies, or
related projects, look there, NOT the home directory.

Topology: repos sit directly at `$GH/<repo>`<, except grouped families one
level deeper (e.g. `$GH/<group>/<repo>`); nothing nests deeper>.
Dependencies and related code are typically one or two levels up from the
current project.

Reference sibling repos as `$GH`-relative paths, not absolute paths.
```
