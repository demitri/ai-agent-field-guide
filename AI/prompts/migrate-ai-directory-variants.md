# One-time migration: consolidate `AI/` directory name variants

(Paste into a clean Claude Code session. Delete this file once both repos are migrated.)

---

Two repos under `$GH` use outdated names for the standard `AI/` agent-knowledge directory; migrate them. Work one repo at a time. For each: require a clean working tree before touching anything, use `git mv` so history follows, grep for stale references afterward, one commit per repo.

## 1. `$GH/openalex-local` — rename

The directory is `AI Agents/` (the space in the name trips up agents — the reason the standard is `AI/`). `git mv "AI Agents" AI`, then update the CLAUDE.md pointer and any other references (`grep -r "AI Agents"`).

## 2. `$GH/thehighlighter/tesseretica` — consolidate, not rename

Both `AI/` (current, rich, actively used) and `AI Notes/` (older seed material: Project Description, RAG aims, Coding Directions, May-era session docs) exist, each with its own `START_HERE.md`, and CLAUDE.md opens with `@AI Notes/START_HERE.md`.

1. Inspect both directories and diff the two `START_HERE.md` files before moving anything.
2. Decide per `AI Notes/` file: still-live → move into `AI/` (merge START_HERE content into `AI/START_HERE.md` — don't clobber); historical → `AI/_archive/`; superseded duplicate → flag and ask before deleting.
3. Update the CLAUDE.md `@AI Notes/START_HERE.md` include to `@AI/START_HERE.md`, and every other `AI Notes` reference (`grep -r "AI Notes"` — check scripts and docs too).
4. Tesseretica's Review & Commit Protocol applies: commit, `Review {hash}`, iterate to a dry round.
