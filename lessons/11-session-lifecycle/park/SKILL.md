---
name: park
description: Park the current session's in-progress work into AI/in_flight/ so a fresh session can resume it without hunting. Use when the user is closing a session mid-work ("park this session", "write the in-flight doc", "I'm closing sessions", "I need to reboot"). "/park list" prints a numbered inventory of parked sessions in the current repo; "/park list all" covers all repos; "/park resume <n>" resumes item n from the list.
---

# Park: write an in-flight resume doc for this session

The user is closing this session with work unfinished. Produce a detail file
+ registry entry so a fresh agent can resume exactly where this session
stopped — no file hunting, no re-derivation, no stale facts. This is a
compaction of the session, not a transcript.

**Why this exists:** the user works on many projects simultaneously, with
multiple sessions each. Open sessions accumulate and consume laptop RAM;
they stay open mainly because their final summary still needs the user's
attention; and once the server-side prompt cache expires, continuing an old
session is token-expensive anyway. The park doc replaces the session AS THE
RESUME ARTIFACT: it lets the user close it (reclaiming RAM) and return
later in a fresh session at low cost. The detail file's quality directly
sets that resume cost — this is why the "Last session output" section
reproduces the summary that needed the user's attention when one exists,
and why the pruning rules act as a deliberate
pseudo-compaction: a long session sheds its stale information at park time.

## Mode: `/park list` (read-only inventory)

If the argument is exactly `list` or `list all` (case-insensitive), do ONLY
this — write nothing, modify nothing (no creating, checking out, or fetching
while listing):

1. Find registries.
   - `list` (default): ONLY the current repo's `AI/in_flight/README.md`.
     If it doesn't exist, say there are no parked sessions in this repo and
     mention that `/park list all` scans every repo.
   - `list all`: the current repo's `AI/in_flight/README.md`, plus a
     bounded scan of the repositories root. The root is `$GH` if set;
     otherwise the platform default — macOS (Darwin):
     `~/Documents/Repositories/GitHub`; Linux: `~/repositories`; any other
     platform: skip the repositories-root scan unless `$GH` is set. Scan:
     `find <root> -maxdepth 5 -path '*/AI/in_flight/README.md' 2>/dev/null`
     (suppress inaccessible-path errors). If the root does not exist, skip
     the scan and say it was unavailable. Deduplicate registries by
     canonical absolute path before parsing (the current repo usually
     appears in both sources).
2. Parse each registry's entries (`## <name> — YYYY-MM-DD` headings); for
   each, capture the `**Pending:**` line plus continuation lines, stopping
   at the first blank line, next `## ` heading, or `→ Details:` line —
   normalized to one line. Also capture each entry's `→ Details:` link
   target when present; that exact target is what broken-link checks use.
   An entry with no Details link is itself an anomaly:
   `🔴 broken link — no detail link`. Do NOT read the detail files.
3. Print one ITEM per parked session. Blank lines separate ITEMS only —
   no blank line between an item's header and its description:
   - **Line 1** (header): starts with the status dot, no list bullet:
     `<dot> [<n>] <repo> · YYYY-MM-DD · **<session name>** · <status>`,
     where `<n>` is the item's 1-based position in the sorted order —
     this is the number `/park resume <n>` accepts. The
     dot+status pair is derived from the pending step: `🟡` + `awaiting
     decision` if it is a question waiting on the user, `🟢` + `ready to
     resume` otherwise. Status text is italic (`*ready to resume*`), never
     bold; only the session name is bold.
     In plain `list` mode OMIT `<repo>` — it is invariant (the current
     repo). In `list all` mode include it: the path relative to the
     repositories root when possible, otherwise the absolute git-root
     path; if no git root resolves, use the grandparent of the
     `in_flight/` directory (the `AI/` folder's parent).
   - **Line 2+** (description): the pending step, plus the summary when it
     adds signal, rendered as a blockquote (`> …`) directly under the
     header line so the whole description — including wrapped lines — is
     indented and visually subordinate.
   Sort by date descending; for equal dates, by registry file modification
   time descending, then repo path ascending.
4. Flag anomalies as their own items in the same format, with a `🔴` dot
   and the anomaly as the status. Detail files are `YYYY-MM-DD-*.md` in
   the same `AI/in_flight/` directory, excluding `README.md`. Report
   detail files not referenced by their registry (`🔴 … orphaned — not in
   registry`) and registry entries whose detail file is missing (`🔴 …
   broken link — detail file missing`).
5. After the items, print a horizontal rule and a **Next:**
   recommendation: which session to resume first and why, in 1–3
   sentences. Derive it ONLY from registry text (list mode never reads
   detail files) — it is a heuristic ranking: time-sensitive / in-flight
   work first (background runs that may have finished or stalled),
   umbrella/coordination sessions last, 🟡 decision-blocked sessions
   ranked by how much they gate other work. End with the one-line resume
   prompt for the recommended session in a blockquote:
   `Read AI/in_flight/README.md in <repo> and resume the <name> session.`
6. If there are no valid registry entries and no anomalies, say exactly
   that and skip the recommendation. If only anomalies exist, print the
   anomalies instead.

## Mode: `/park resume <n>` (resume by item number)

If the argument matches `resume <n>` or `resume <n> all` (case-insensitive,
`<n>` a positive integer), resume the n-th parked session instead of
parking:

1. Re-derive the sorted entry list EXACTLY as `list` does (registry
   discovery, parsing, and sort order) — `resume <n>` uses the plain
   `list` scope (current repo); `resume <n> all` uses the `list all`
   scope. The number is recomputed at resume time, so it matches the most
   recent `/park list` output only if no registry changed in between —
   echo the resolved item's header line back to the user before doing
   anything, so a drifted number is caught immediately.
2. If `<n>` is out of range, the registry is missing, or item `<n>` is an
   anomaly (broken link, orphan), do NOT guess: print the current numbered
   list and stop.
3. Otherwise act as the resuming agent for that entry: read ONLY its
   detail file (the registry's Details link target), follow its "First
   actions on resume", and proceed with the work. Honor the detail file's
   cleanup rule when the work completes.

Because `list`, `list all`, and `resume <n>` are reserved, a session
cannot be labeled with any of them; if the user genuinely wants such a
label, they must pass a longer one (e.g. `list-cleanup session`).

Any other argument (or none) means normal parking, below.

If the user passed an argument, use it as the label for this session.
- **Label rule** (display text in headings/summaries): one line only, trim
  whitespace, replace any newlines with spaces; treat it as plain text, not
  markdown (no links/headings from it). The label never becomes a filename.
- **Slug rule** (the only filename input): lowercase ASCII, replace
  non-alphanumeric runs with `-`, trim leading/trailing `-`, max 60 chars.
  If no argument was given or the result is empty, derive the slug from the
  task summary. Never include `/`, `..`, spaces, or shell metacharacters.

## 0. Is parking actually the right move?

Park is for work a future session must RESUME. If it is already clear from
the current context that the work is actually at a finished seam (nothing
meaningful to resume; what's left is close-out: loose ends, git cleanup,
capture of decisions), **STOP before doing any park work** and tell the
user: this looks like an end-of-session situation, `/endsession` is
probably what they want, and ask them to confirm whether to park anyway
or switch. Do not write the detail file, touch the registry, or run the
safety sweep until the user answers — those steps assume parking is the
right call, and writing a residual park entry pollutes the registry with
something that immediately needs deletion. Recommend only, never invoke
`/endsession` automatically; the user decides.

Only after the user confirms "park anyway" (or any answer that isn't
"switch to /endsession") do you proceed to step 1. Even then, park's job
is to PRESERVE state, not resolve it: don't run a close-out audit as part
of parking — unresolved items get recorded in the detail doc and handled
on resume.

## 1. Locate the home repo

Default: the git repo root of the current working directory. BUT first check
where this session's work actually lives — if the session's primary
artifacts, branches, or boot documents are in a different repo than cwd, ask
the user one question (which repo to park in) rather than guessing.

- If cwd is not inside a git repo, ask the user where to park.
- If cwd is inside a submodule or nested repo, treat that inner repo as the
  default only if the session's work is inside it; otherwise ask one
  question.

## 2. Pre-park safety sweep

- If background work from this session is still running, STOP and tell the
  user — park means "cleanly interrupted", not abandoned. Check at minimum:
  background shell commands started by this agent, running dev/test
  commands, known background agent/task/workflow IDs, and external processes
  explicitly launched this session (CI runs, remote jobs). If a category
  cannot be inspected, say so in the detail doc rather than claiming nothing
  is running. Either wait for them, stop them, or — if the user says leave
  them — record their IDs and how to check on them in the detail doc.
- Capture `git status --short` (plus `git diff --stat` if dirty) for every
  repo this session touched: any repo where files were read or edited,
  commands were run, branches were inspected, or artifacts were generated
  during the visible session. If unsure whether a repo was touched, list it
  under an explicit "Possibly touched / not verified" note rather than
  omitting it. Dirty state is recorded verbatim in the detail doc so nothing
  is silently lost or misattributed to a later session.
- NEVER commit, stage, revert, or stash anything as part of parking.

## 3. Write the detail file FIRST

The detail file is created before the registry entry, so the registry always
points at the exact final filename.

Path: `AI/in_flight/YYYY-MM-DD-<slug>.md`. Immediately before writing, list
the folder: if the filename already exists (another same-day session),
suffix `-2`, `-3`, … and re-check. Use a create-only write — never an
overwrite of an existing file. If create-only semantics are unavailable in
the write tool, do NOT write to a predictable filename with an
overwrite-capable tool: make the filename unique before writing by adding
`-HHMMSS` (or a short random suffix). Never overwrite an existing detail
file.

Fixed section order:

```markdown
# <High-level task, one sentence — what this session is FOR>

Parked: YYYY-MM-DD HH:MM <timezone>   (e.g. 2026-06-05 14:37 America/New_York)

STATUS: <1–2 sentences: what has been done, what has NOT. Be explicit about
not-done; never overclaim. "Zero execution" is a valid and useful status.>

## Last session output (verbatim)

<ONLY if an actual prior assistant end-of-work summary/report exists in the
visible conversation: reproduce it EXACTLY, unedited, in a blockquote or
fence. The park confirmation itself does NOT count as the last session
output. If no such summary exists, write a fresh closing summary here and
label it clearly: "(written at park time — no end-of-work summary existed)".
Never pass off a synthesized summary as reproduced.>

## Resume context

<The compaction. Everything a fresh agent needs and NOTHING it doesn't:>
- Boot documents: every file the resuming agent must read, with exact paths —
  and exact commands if any live only in git or on another machine
  (e.g. `git show <hash>:<path>`).
- Binding rules and gates in effect (approval gates, human-only actions,
  review conventions, batching constraints).
- Environment facts established this session, EACH tagged `[stable]` or
  `[re-verify]` (service states, branch/commit positions, tool availability —
  these go stale).
- Findings already established, marked "done — do not redo".
- The work plan as it stands, including alternatives still open.
- Pending user decisions: reproduce the question and its options VERBATIM if
  the session stopped mid-decision.

Pruning rules — DROP: superseded findings, resolved questions, dead ends,
anything re-derivable from git history or the code itself, and narrative of
how the session got here. KEEP only what is needed going forward.

## Working tree state at park

<`git status --short` per touched repo, verbatim. "clean" if clean. Include
the "Possibly touched / not verified" list here if any.>

## First actions on resume

<Numbered checklist: re-verify each `[re-verify]` fact, re-ask the pending
question, then proceed. End with the cleanup rule: when the resumed session
COMPLETES the work, remove ONLY the registry entry whose Details link
exactly matches this file's name, then delete this file. If the work was
SUPERSEDED or ABANDONED rather than completed, do NOT silently delete:
either keep this file with an updated STATUS and update the registry entry
to match, or ask the user before deleting.>
```

## 4. Bootstrap or update the registry

Path: `<repo>/AI/in_flight/README.md`. Done AFTER the detail file exists;
the entry's Details link must be the exact filename created in step 3.

If the detail file is written but the registry update FAILS, do not pretend
parking succeeded: tell the user the detail file is orphaned (resume starts
from README.md, so an unregistered file is invisible), give its exact path,
and either retry, ask the user to update manually, or record an explicit
failure note — in the detail file if it can be safely updated, otherwise in
the final user confirmation.

If the folder or file does not exist, create the file starting with EXACTLY
this header:

```markdown
# In-flight sessions — resume registry

Each entry below is ONE interrupted session: a short summary plus a pointer
to its detail file. Entries are newest-first. **New agents: read ONLY the
detail file for the session you are resuming — do not read the other detail
files.** When a session is resumed and closed out, delete its entry and its
detail file.

---
```

If it exists:

- **Insert the new entry immediately after the `---` separator** (registry
  order is newest-first). Preserve all existing entries below it unchanged —
  never modify or delete them.
- **Re-read the file immediately before writing**, and AFTER writing verify
  that every entry from your last read survived; if external changes are
  observed at any point, merge them in and re-verify. This CANNOT detect
  every parallel write without locking or compare-and-swap (a write landing
  between your re-read and your write is invisible to this check) —
  concurrency safety here is best-effort only, and should be reported as
  such if it matters. Never overwrite a version you did not just read.
- If the file exists but is malformed — no `---` separator, a different
  header, a divergent convention — do NOT rewrite or normalize it. If a
  prior "Parked sessions added by park skill" block already exists, insert
  the new normal entry immediately below that block heading, before any
  older entries in that block; otherwise append exactly this at the end of
  the file:

  ```markdown
  ---
  ## Parked sessions added by park skill

  <normal entry format>
  ```

Entry format:

```markdown
## <Session name> — YYYY-MM-DD

<1–2 line summary of what the session is.>
**Pending:** <the single next step, so the user can pick a session to resume
by scanning this registry alone>

→ Details: [`YYYY-MM-DD-<slug>.md`](YYYY-MM-DD-<slug>.md)
```

## 5. Confirm back to the user

- The two file paths written, and whether each is tracked, untracked, or
  gitignored — determined precisely: tracked only if `git ls-files --
  <path>` returns it; gitignored only if `git check-ignore -- <path>`
  matches; otherwise untracked. (A new file under a tracked directory is
  NOT tracked until added to the index.)
- The one-line resume prompt: `Read AI/in_flight/README.md in <repo> and
  resume the <name> session.`
- An explicit statement that nothing was left mid-execution — or, if
  something was, exactly what is still running and where that is recorded.

## Conventions

- Tracked vs untracked: determine the repo's convention by checking whether
  existing `AI/` (or similar planning-doc) files are tracked and whether
  `.gitignore` covers them. Do not stage anything either way. When the
  convention is undeterminable, leave the new files untracked and say so.
- Concurrent parking: detail-file-first ordering, create-only writes, the
  re-read-before-write rule, and the verify-after-write check together make
  parallel parking best-effort safe. Do not skip them; if a verification
  step finds lost content, restore it before finishing.
