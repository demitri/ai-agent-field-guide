<!-- A template for directing `/compact` on a session that has become an
     orchestrator. Copy the block below the line, fill the {{slots}}, delete any
     tier — or any single item — that doesn't apply, and pass it as the argument to /compact:
     `/compact <this text>`. The goal is never "make it shorter" — it is
     "preserve the orchestrator's function." The NET TEST is what keeps it
     honest; don't drop it. Background: LESSON.md. -->

---

COMPACTION GUIDANCE — this session's value is as an ORCHESTRATOR of
{{the program: what multi-session work this session coordinates}}, not the
per-item execution detail. Preserve the operating state and procedure in HIGH
FIDELITY; compress the blow-by-blow. {{the durable record — e.g. the git repo,
a queue/state file, a changelog}} is the canonical record; anything captured
there can be summarized to a pointer.

KEEP IN HIGH FIDELITY (verbatim-level):
1. The orchestration loop — {{who does what; the exact per-item procedure from
   "item landed" to "next item recommended + prompted"; any single-editor or
   safety discipline that prevents a known failure}}.
2. The exact invariants — {{the gate commands / checks that must pass, verbatim}}.
3. Current program state, LATEST values only — {{counts, current HEAD, what's
   done, what's next, what's handed off but not yet landed, any prerequisites}}.
4. Operating conventions — {{the rules this session runs by: generation
   discipline, review rotation, naming, model strategy}}.
5. Durable lessons established this session — {{what was learned here that must
   survive}}.
6. Open / owed — {{anything unresolved or disclosed that must not be
   rediscovered later as a mystery}}.

COMPRESS TO ONE-LINERS (drop the detail; it lives in the durable record):
- {{full text of each finding / report / bug — keep "what it found + where it lives"}}
- {{every review round's findings and edit diffs — keep only the net outcome}}
- {{the consumed start-prompts — keep which items were prompted and whether landed}}
- {{intermediate commit hashes — keep only current HEAD (and, if it's a git workflow, that origin is in sync with local)}}
- {{resolved investigations — one line each at most}}

DROP ENTIRELY:
- raw tool output (greps, file reads, gate/test logs)
- setup / handoff detail already committed to a file
- exploratory tangents that didn't change a decision

NET TEST: after compaction I should still be able to {{the orchestrator's job in
one sentence — e.g. take "item X landed", integrate it correctly, and recommend
+ prompt the next item}} — without re-reading this session.
