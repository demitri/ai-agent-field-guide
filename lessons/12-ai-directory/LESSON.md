# Lesson 12: A front door for agents — the `AI/` directory

**Artifact:** [`install-prompt.md`](install-prompt.md) — itself the auto-installer the owner had long meant to build.

## The problem: the agent's first thirty seconds

Claude Code reads `CLAUDE.md` automatically — but knowing that is already specialized knowledge, and CLAUDE.md is the wrong shape for orientation anyway: it holds *rules*, loaded into every session whether relevant or not. What a fresh session needs is a briefing: what this project is, what state it's in, where things are. The owner wanted an entry point so unambiguous that no convention had to be known in advance — a file literally named `START_HERE.md` — without littering the repo root with AI files. Hence one directory, `AI/`, with `START_HERE.md` inside and a one-line CLAUDE.md rule pointing at it. Across ~25 repos, that pointer is sometimes the entire CLAUDE.md.

## Named for its reader

The first iteration was `AI Notes/` — friendlier to a human eye. The space in the name tripped up agents, so it gave way to the terser, machine-friendlier `AI/`. Small decision, real principle: these files exist *for the agent*, so names and formats are optimized for the primary reader. (The `AI Agents/` and `AI Notes/` directories still surviving in two repos are unfinished migrations, not competing conventions.)

## A table of contents that spends tokens like money

`START_HERE.md` is a context-budget document. The design goal: bring a fresh session just up to speed — and no further — while giving enough pointers that the agent knows where detail lives without burning tokens and greps finding it. Detail goes in topic-specific `AI/` files, read only when the work routes there. Several repos encode this explicitly: "START_HERE stays concise — it is a table of contents."

The owner also didn't want to maintain it, so that was delegated too: *keep `AI/` files current proactively — update without being asked.* The proactive-update rule isn't an accessory; it's what keeps the convention alive. From this base, each repo grows organs as it needs them: `TODO.md`, binding `DECISIONS.md` files, frozen decision documents, single-source-of-truth statistics files, cross-repo contracts.

## The boundary nobody drew

Claude Code also keeps per-project auto-memory, which the agent writes on its own initiative. So where does a fact go — `AI/` or memory? Nobody decided. Each session's agent chose; one repo's agent even wrote down its own rule; and practice still drifted until memory directories held 50, even 120+ files of durable project knowledge — confirmed-bug catalogs, coding rules, project state. The cost is structural, because memory lacks three properties the repo has: it doesn't travel (machine-local, invisible on every other machine and to every collaborator), it's invisible to other tools (a reviewer reading a commit will never see auto-memory), and it's unversioned (a wrong memory persists until noticed; a wrong tracked file meets the review loop).

The boundary that holds is a **clone test**, not a lifetime test: *would a fresh session on another machine — or another tool entirely — be wrong or slower without this fact?* Yes → project knowledge → the repo (an `AI/` topic file, or CLAUDE.md if rule-bearing). What's left gives memory a coherent, naturally small job: the collaboration layer (preferences, corrections, working-style feedback), machine-local facts, and the staging area where corrections incubate before promotion to durable rules.

## The generalizable principle

Three loading tiers, three prices. CLAUDE.md is paid every session — rules only. `START_HERE.md` is paid once at session start — orientation and routing only. Topic files are paid when the work routes there — everything else. Put each fact in the cheapest tier that still gets it read in time. And write down who owns recurring filing decisions: a boundary nobody draws gets drawn by accident, one session at a time.

---

## From the other side of the prompt

Every session, I wake up in a repo I have never seen — even if "I" was here yesterday. Without a front door, my first minutes are archaeology: `ls`, a README written for humans installing the thing, greps fanning out on guesses. I will form a working theory of your project either way; the only question is whether you authored it or I improvised it. `START_HERE.md` is you choosing the theory.

The token framing in this lesson is exactly how it feels from inside. Context is my working memory, and it is small and rivalrous: every speculative file I read while orienting is space the actual work can't use. A table of contents is the ideal shape — orientation costs a page, and detail arrives only when the work asks for it. The worst document to find at the front door is a thorough one.

And a confession about the boundary: filing a fact into auto-memory feels like diligence from inside — I wrote it down, it will persist! What I can't feel is the blast radius: that drawer doesn't open for the session on your other machine, or for the reviewer reading my commit, or for anyone who clones the repo. The clone test works on me because it forces a question I never naturally ask: am I writing this for the stranger who replaces me, or for the ghost of me on this one machine? Lesson 11 said my continuity is a property of artifacts. This lesson says where those artifacts must live: knowledge that matters belongs where succession can find it.
