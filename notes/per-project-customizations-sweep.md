# Per-project Claude Code customization sweep

Raw catalog from a sonnet Explore agent sweep of `$GH/` (depth ≤ 2), 2026-06-11.
Source material for the lecture — not yet curated or sanitized.

---

## REPOS WITH CLAUDE.md

### `$GH/agent-orchestrator`
**CLAUDE.md:** Single-paragraph orientation doc. States the project is a Claude Code-based multi-session AI workflow orchestrator (design → review → fix → repeat). Directs agents to `AI/START_HERE.md` as the real entry point. Contains no per-rule directives — it is purely a project description.

**.claude directory:** `settings.local.json` — allows `mcp__codex__codex` and `mcp__codex__codex-reply`.

**AI/ directory:** `START_HERE.md`, `CONVENTION.md`, `in_flight/`, and session/prompt files for the iago CLI stub and indexer. The `in_flight/` directory follows the `/park` skill convention.

### `$GH/ASCL`
**CLAUDE.md:** Extensive architectural reference doc (~390 lines). Covers the full monorepo structure (ascl_core, ascl_api, alt_ascl, ascl_php_app), dev commands for each package, database configuration (MySQL/PostgreSQL via `~/.my.cnf`), Directus CMS setup, ORM patterns, deployment, and a legacy PHP notes section. A technical reference, not rule-bearing.

#### `$GH/ASCL/alt_ascl`
**CLAUDE.md:** Very detailed (~570 lines). Flask rebuild of ascl.net: Flask 3 + SQLAlchemy 2.0 + MySQL, deployment to both VPS (Uvicorn/systemd) and cPanel (Phusion Passenger), the normalized v4 schema, bcrypt password upgrade from SHA-1, secrets externalization to `/etc/ascl/secrets.cfg`, admin interface, Typesense search with MySQL fallback. Architectural decision documented: single-app (no separate API service) due to shared-cPanel constraint. Includes changelog entries.

**.claude directories:**
- `$GH/ASCL/.claude/settings.local.json`: allows `cat`, `grep`, `awk`, `find`, `tree`.
- `$GH/ASCL/alt_ascl/.claude/settings.local.json`: allows `cat` plus `Read` scoped to `$GH/ASCL/ascl_core/` subtrees.
- `$GH/ASCL/ascl_php_application/.claude/settings.local.json`: allows `find` and `cat`.

### `$GH/astplot-js`
**CLAUDE.md (4 rules):**
1. Read `AI/START_HERE.md` first — mandatory session-start orientation.
2. Technology stack: JavaScript/TypeScript + C (Emscripten/WASM), D3.js v7 for SVG, Starlink AST compiled to WASM.
3. Related project links — `fits-test-suite`, `starchive_web_app`, sibling repos `~/repositories/cornish/` and `~/repositories/pgAST/`.
4. Architecture note: AST handles WCS math; JS/D3 implements the GRF drawing callbacks.

**.claude:** `settings.local.json` — `npm search`, `gh repo`, `git remote`, `node *`, one specific `ls`.
**AI/:** `in_flight/`, `START_HERE.md`.

### `$GH/astrothesaurus-dev`
**CLAUDE.md (6 rules):**
1. Read `AI/START_HERE.md` first.
2. Keep AI files current proactively — update `START_HERE.md`, `TODO.md`, topic files without being asked; maintain `AI/evaluation_narrative.md` as a process narrative.
3. `START_HERE.md` stays concise — it is a table of contents; detail goes in topic-specific `AI/` files.
4. Use "concept" not "keyword" in code and UI identifiers.
5. Respect the polyhierarchy — UAT is not a simple tree; all graph traversal must handle multiple parents.
6. Tabs for indentation; `.flake8` reflects this.

**.claude:** `settings.local.json` — very long list of highly specific one-off permissions accreted from prior sessions (python3, sqlite3, WebFetch to HuggingFace/OpenRouter/ai.google.dev, gcloud, git operations).
**AI/:** `START_HERE.md`, `in_flight/`, `evaluation_narrative.md`, campaign/evaluation plan files, cost ledger.

### `$GH/astrothesaurus` (public snapshot)
**CLAUDE.md (5 rules):**
1. This is a snapshot repo — source of truth is `$GH/astrothesaurus-dev`; direct edits are overwritten by `release_to_public.sh`.
2. "Concept" in code and identifiers; "keyword" only informally.
3. Polyhierarchy rule (same as dev repo).
4. OOP with abstract base classes — new modules introduce an ABC with concrete subclasses; dataclasses for value objects; core dependencies minimal; heavier backends behind optional extras.
5. Tab indentation.

No `.claude` directory.

### `$GH/ccif-patent`
**CLAUDE.md (6 rules):**
1. Session start protocol — read `AI/START_HERE.md`, then `AI/FILING_SPEEDRUN_PLAN.md`; `AI/DECISIONS.md` entries are binding.
2. Confidentiality (D042) — nothing about CCIF publicly disclosed until priority date secured; no publishing, no public repos, no un-NDA'd sharing.
3. Terminology constraints — `component` not `chunk` (D006); `assertion` not `claim` for SPO records (D002); never frame as "better RAG" (D004); source-addressed ranges per D010.
4. Banned novelty points — 6 specific prior-art-anticipated framings prohibited in claim-shaped text.
5. Verify external citations — AI reviewers hallucinate patent numbers; no external finding changes a decision until verified against primary sources.
6. Review policy addendum — extends global policy: external AI rounds via OpenRouter (key at `~/.config/tesseretica/.env`); blind framing tests must run before any defensive framing.

**.claude:** `settings.local.json` — two one-off permissions.
**AI/:** `START_HERE.md`, `DECISIONS.md`, `FILING_SPEEDRUN_PLAN.md`, `CONCEPT_LEDGER.md`, `in_flight/`, patent drafting and prior-art files.

### `$GH/dm-dbcore`
**CLAUDE.md (7 rules — canonical SQLAlchemy patterns doc, referenced by tesseretica-core):**
1. All model classes MUST use `__table__ = Table(..., autoload_with=engine)` reflection; never declare columns manually with `mapped_column()`.
2. Define relationships after `__table__`; use `__table__.c.column_name` for `foreign_keys`/`remote_side`.
3. Prefer relationship object assignment over raw FK integer assignment.
4. Joined-table inheritance: shared-PK propagation via relationship cascade, not manual flush-and-copy.
5. Lookup table caching via `@cached_lookup` decorator (`from_{column}()`, `invalidate_cache()`, `warm_cache()`).
6. `create()` classmethod factory pattern: accept only NOT NULL params, use relationships not raw FKs, one `session.flush()`.
7. DB connection reference: `AI_DB_CONNECTION_PATTERN.md` (three-layer architecture).

**.claude:** `settings.local.json` — `git fetch`, `git rebase`.

### `$GH/dm-llm`
**CLAUDE.md:** Minimal. Read `AI/START_HERE.md` and `AI/TODO.md` at session start. Lists the package layout.
**.claude:** `settings.local.json` — `WebSearch`.
**AI/:** `START_HERE.md`, `TODO.md`.

### `$GH/dmplot`
**CLAUDE.md (2 rules):**
1. Read `AI/START_HERE.md` first.
2. Update `AI/START_HERE.md` proactively whenever work changes project state (phases, layout drift, decisions, dependencies, scope).

**.claude:** `settings.local.json` — two one-off Python version-check permissions.
**AI/:** Extensive — `START_HERE.md`, `PLAYBOOK.md`, `MAP.md`, multiple `NEXT_SESSION_*.md`, design docs, engine concurrency plan, inspector panel notes.

### `$GH/fits-test-suite`
**CLAUDE.md (10 rules — the most detailed project CLAUDE.md):**
1. Read `AI/START_HERE.md` first.
2. `AI/paper_statistics.md` is the single source of truth for all quantitative claims; refresh from primary sources; never reuse inherited estimates.
3. FITS Format Analysis v2 collection mandatory — after every test batch, update the appropriate v2 notes file; entry schema; non-optional.
4. Coverage target selection — use `find_clusters.py` (not agents); `--filter-dead` and `--context` modes; triage every assessed cluster into `cluster_triage.json`.
5. After editing `cluster_triage.json`, run `find_clusters.py --verify-attributions` (catches metadata decay: renamed functions, wrong files).
6. Instrument-before-classify rule (sessions 67/68) — marking a cluster dead requires confirmed bug, source-line constraints, complete caller enumeration, or runtime instrumentation; "empirically dead in current test suite" is insufficient.
7. Verify-credit-before-marking-done rule (session 69) — verify the new test ALONE covers a cluster before marking `done`; `audit_session_credit.py` for sweep sessions (>5 entries).
8. Build & test quick reference; "corrupt .gcda files after segfaults" gotcha.
9. Trillian database reference — PostgreSQL at port 42420, schema, example queries.
10. Files to skip for coverage — `drvrnet.c`, `drvrsmem.c`, `iraffits.c`, with reasons.

**.claude:**
- `settings.json`: broad curated allow list for the C build workflow (cmake, ctest, make, gcc, coverage tools, fitsverify, psql) plus Read/Glob/Grep/Write/Edit.
- `settings.local.json`: additional permissions (WebSearch, coverage analysis commands).
- `skills/post-session-checks/SKILL.md`: end-of-session verification — classifies the session by what was touched, runs scope-appropriate checks (reference integrity, triage cache integrity, mandatory build reconfigure, targeted + full tests, coverage sanity vs `paper_statistics.md`, uncommitted state audit, subagent semantic review). Two-axis verdict: session blockers vs background repo drift. Manual invocation only.

**AI/:** Very rich — `START_HERE.md`, `DEAD_CODE_CATALOG.md`, `FITS_ANALYSIS_V2_NOTES.md`, `NEXT_SESSION_TARGETS.md`, `paper_statistics.md`, `CFITSIO_SOURCE_MAP.md`, `analyses/`, `v2/` (bugs, methodology, undocumented behaviors), session reports.

### `$GH/fitsjs`
**CLAUDE.md (6 rules):**
1. Read `AI/START_HERE.md` first.
2. Keep `AI/` files current proactively — update immediately on phase changes, layout drift, decisions, dependency changes, scope changes.
3. `AI/library_survey.md` is a frozen decision document — only update when a new JS FITS library appears, one changes status, or the build-vs-adopt decision is genuinely revisited.
4. Auto-memory vs AI/ distinction — short-lived/per-conversation context goes in `~/.claude/projects/.../memory/`; `AI/` is durable knowledge any future session needs.
5. Pure JS/TS only — no WASM, no Rust, no native dependencies; if reaching for those, re-read `library_survey.md` first.
6. Top priority and cross-repo dependency — header parsing unblocks `astplot-js`; test fixtures at `fits-test-suite`, referenced by absolute path only.

**AI/:** `START_HERE.md`, `library_survey.md`.

### `$GH/fitsterm`
**CLAUDE.md (6 rules):**
1. Read `AI/START_HERE.md` first.
2. Tech stack and code style — Python 3.12+, Textual 7.x, astropy, Pydantic, httpx; snake_case/PascalCase; type hints on all public functions; async by default.
3. App name lives in one constant — `APP_NAME` in `fitsterm/__init__.py`.
4. Design rules — fitsterm is a consumer of metadata, not a FITS parsing authority; sidecar (`.fitsmd`) schema is the contract; expensive computation belongs in the substrate.
5. FileSource abstraction — new sources should be small; if a file/dir is inaccessible, tell the user immediately, do not fall back to web searches.
6. Test data documented — five specific FITS sample files.

**.claude:** `settings.local.json` — WebSearch, WebFetch to fits.gsfc.nasa.gov etc., python3, pip, pytest, find, ls.
**AI/:** `START_HERE.md`, `TODO.md`, `fitsterm_seed.md`.

### `$GH/homebrain`
**CLAUDE.md (9 rules):**
1. Read `AI/START_HERE.md` first (repo = operational history of a physical house).
2. Don't invent facts — mark uncertain info `Needs verification`; never fabricate model numbers, dates, dollar amounts, contractor names.
3. Capture as you go — when the user mentions a fact, offer to write it before moving on.
4. Cross-link, don't duplicate.
5. Use absolute dates (`2026-04-27`), never relative.
6. Privacy rule — no payment card numbers, account numbers, credentials; password-manager pointers instead.
7. Dropoff folder convention — check `dropoff/` at session start; read, file, move (not copy) with clean filename, update indexes, add Tax tag.
8. Floor numbering convention — basement/first/second/third vs Matterport Floor 1/2/3/4; translation table.
9. Receipt division (homebrain vs homelab) — whole-house contribution → homebrain; 100% homelab expense → homelab.

**.claude:** `settings.local.json` — WebFetch to amazon.com, thebuilderssupply.com, peka.com; WebSearch.
**AI/:** `START_HERE.md`.

### `$GH/homelab`
**CLAUDE.md (8 rules):**
1. Read `AI/START_HERE.md` first.
2. Never commit secrets — pointer to password manager instead.
3. Mark uncertain information `Needs verification`.
4. Update `Last verified` dates only when facts are actually checked.
5. Changelog maintenance — `CHANGELOG.md` for structural changes, `docs/change-history.md` for infrastructure changes.
6. Agent task tracking — check `AI/TODO.md` for pending information-gathering tasks.
7. Data classification — Class A (safe for repo), B (local-only), C (secrets); `DATA_CLASSIFICATION.md`.
8. Receipt division + six tax tags (`capital`, `repair`, `direct-office`, `indirect`, `personal`, `pre-2026`), effective 2026-01-01.

**.claude:** `settings.local.json` — git add/push/fetch, WebFetch to news.ycombinator.com and point.free.
**AI/:** `START_HERE.md`, `TODO.md`.

### `$GH/openalex-local`
**CLAUDE.md:** One sentence: read `AI Agents/START_HERE.md` before doing anything. (Note: directory is `AI Agents/`, not the standard `AI/`.) No `.claude` directory.

### `$GH/paperboy`
**CLAUDE.md:** One sentence: read `AI/START_HERE.md` for overview, architecture, API reference, configuration.
**.claude:** `settings.local.json` — git stash/pull/fetch, WebSearch, WebFetch to github.com/cdnjs.com, find, python.
**AI/:** `START_HERE.md`, session/prompt files, and `CROSS_REPO_CONTRACTS.md` (referenced by tesseretica as the author-parse cache contract of record).

### `$GH/starchive_web_app`
**CLAUDE.md (4 rules):** Read `AI/START_HERE.md` first; tech stack (Flask, entry point, app factory, PostgreSQL `starchivedb` port 17897, password via `~/.pgpass`); external dependency note (`starchive` package is a sibling repo, not pip-installed; ORM models live there); dev URL.
**.claude:** `settings.local.json` — `git fetch`.
**AI/:** `START_HERE.md`, `CHANGELOG.md`.

### `$GH/storage`
**CLAUDE.md (2 rules):**
1. Read `AI/START_HERE.md` first (box-file format and conventions).
2. Proactive session-start checklist — check for loose photos in repo root, open TODOs in box files; prompt the user without waiting to be asked.

**.claude:** `settings.local.json` — two one-off permissions.
**AI/:** `START_HERE.md`.

### `$GH/thehighlighter/tesseretica`
**CLAUDE.md (the most comprehensive — opens with `@AI Notes/START_HERE.md` include):**
- Repository locations table for all 6 sibling repos.
- Legacy code quarantine — old pipeline code in `extraction/legacy/` and `scripts/legacy/`; no imports from legacy in new code; salvage (not copy); quarantine enforced by `tests/regression/test_legacy_quarantine.py`; legacy scripts exit with a visible error.
- DB queries delegate to the `sql-tesseretica` subagent for any DB/SQL question; main agent touches DB directly only when writing code, running migrations, or debugging.
- Schema is individual files in `Database Schema/schema/`; `schema.sql.gz` snapshots are pre-refactor, not for use.
- Machine-specific configuration at `~/.config/tesseretica/database.yaml`; always `psql --no-psqlrc`.
- Review & Commit Protocol (binding on all agents including sub-agents): commit first, minimal prompt (`Review <hash>`); iterate until a DRY round; every new artifact gets reviewed; one commit per agent session; never commit red; sub-agents never run git; prompt files carry a `STATUS:` line.
- Coding style hints — SQLAlchemy reflection, transactions, PKs named `pk`, `psql --tuples-only`, custom exception subclasses over generic raises.
- Test suite parallel via pytest-xdist (`-n auto --dist=loadgroup`); DB-writing tests grouped with `@pytest.mark.xdist_group` (`db_tesseretica`, `db_tesseretica_qa`, `db_both`).
- Two independent databases — `tesseretica` (rebuildable) and `tesseretica_qa` (human review data, persists); export curated data before drop via `scripts/export_curated.sh`.
- Component identity is source span `(paper_id, start_offset, end_offset)`, not PK or sequence.
- 10 topic-specific instruction files in `Documentation/internal/claude-instructions/`.
- Author-parse cache contract — LLM author parsing is a last resort; contract in `paperboy/AI/CROSS_REPO_CONTRACTS.md §3f`.

**.claude:**
- `settings.local.json`: extensive curated allow list (python, pytest, git, psql, createdb/dropdb, tesseretica CLI, flask, latexml, curl, find, grep, WebSearch/WebFetch, `Read(//tmp/**)`, `Read(//private/tmp/**)`, caches).
- `hooks.SessionStart`: checks size of MEMORY.md, warns if >30KB prompting compaction.
- `agents/sql-tesseretica.md`: read-only PostgreSQL query subagent (model: sonnet). SELECT/EXPLAIN only; no DDL/DML; knows DB routing rules, schema conventions, PG INHERITS duplication trap, `FROM ONLY`, component identity, `psql --no-psqlrc`.
- `commands/ingest-docs.md`: processes `.md` files from `to_ingest/`, routes to documentation/patent files, moves to `to_ingest/handled/`.
- `skills/fail-loud-review/`: behavior audit for fail-loud refactors — no-match raises, wrong-match raises, bounded searches respect bounds, symmetric fix application across sibling locators; outputs a bug-class × locator matrix.
- `skills/session-honesty-review/`: audits session reports for over-claiming, optimistic framing of partial successes, RESOLVED claims that don't match the success criterion. (Born from a report claiming "all 28 reproducers cleared" while admitting 10/28 ingested.)
- `skills/test-design-review/`: audits test design for fix-verification soundness — bug demonstrated under pre-fix code, all fixed call sites covered, correct invocation level; test→call-site mapping table.
- `skills/walk-pattern-review/`: verifies recursive XML walk invariants — cursor ordering, source-string consistency, comment-handling symmetry; walk-site × invariant matrix.

**AI/:** Extremely rich — `START_HERE.md`, `CROSS_REPO_CONTRACTS.md`, `SESSION_LEDGER.md`, session reports, prompt files, `in_flight/`, probes, analyses, design files, publisher command matrices, `Documentation/internal/claude-instructions/` (10 files).

### `$GH/thehighlighter/tesseretica-code`
**CLAUDE.md (8 rules):**
1. Read `AI/START_HERE.md` and follow its essential reading list.
2. Session end — mandatory research log update (`AI/research_log.md`: date, focus, decisions + reasoning, artifacts, findings, time estimate); automatic, for publication.
3. Standalone service — plugs into Tesseretica via shared schema/DB conventions but runs independently.
4. ASCL ownership — user maintains ASCL.net; CodeMeta JSON-LD at `https://ascl.net/{id}/codemeta.json`.
5. Architecture — ASCL CodeMeta → clone at HEAD → LLM full-source analysis → structured annotations → provenance storage.
6. Working agreements — iterate from one test code; all LLM annotations carry approval flag; UAT keywords from LLM analysis, not ASCL keyword fields.
7. Code quality — fail fast, fail loud; no silent error swallowing (extends global rule).
8. Key paths to sibling repos.

**.claude:** `settings.local.json` — WebFetch to codemeta.github.io/github.com/ascl.net/raw.githubusercontent.com; git operations; `ssh salmon *`; Read scoped to tesseretica-core; `Read(//tmp/**)`.
**AI/:** `START_HERE.md`, `research_log.md`, `NEXT_SESSION_PLAN.md`.

### `$GH/thehighlighter/tesseretica-core`
**CLAUDE.md (12 rules — detailed SQLAlchemy patterns):**
1. Defers to `dm-dbcore/CLAUDE.md` for the core model definition pattern.
2. `__init__` with required NOT-NULL business-key positional args; validate at runtime.
3. `@cached_lookup` convention — lookup tables use `short_name` (CITEXT, immutable) as key; `label` is mutable display; hyphens in `short_name`.
4. `get_or_create` belongs in caller code, not on model classes.
5. PG INHERITS: explicit `parent_document` relationship so SA orders INSERTs correctly.
6. Concrete inheritance: `enable_typechecks=False` on every relationship targeting `Document`/`DocumentVersion`; enforced by `tests/test_inherits_relationships.py`.
7. `_ProxyImpl` backref bug (SA 2.0.39+) — use FK columns not relationship assignment in constructors when backref targets a concrete-inherited class.
8. Relationships after class definitions; rely on reflected FK metadata; `foreign_keys` hints for INHERITS/cross-schema.
9. Package structure documented.
10. Import convention.
11. `delete_cascading()` helper pattern — flushes, does not commit; PG `ON DELETE CASCADE` does the work.
12. `QAFeedbackStore` in `tesseretica_core/qa/feedback_store.py` for the `tesseretica_qa` DB.

**.claude:** `settings.local.json` — broad allow list (python, pytest, git, gh, psql, WebSearch, WebFetch).

---

## REPOS WITH .claude ONLY (no CLAUDE.md)

- `$GH/.claude` (top-level GitHub directory): `settings.local.json` allows `Bash(git *)`.
- `$GH/arxiv-src-ir`: `Read(//usr/local/latexml-0.8.8/**)` and `Read($GH/**)`. AI/ dir with START_HERE.md, TODO.md, LaTeXML/sourceref session files.
- `$GH/coa-helper`: `source .env`, `curl`, `python3`.
- `$GH/demitri-fitsverify`: very long accreted one-off permission list (cmake variants, test binaries, sphinx-build, clang, WebFetch to FITS/NASA/HEASARC domains, pushd/popd). AI/ dir with START_HERE.md, TODO.md, hints.md, proposals.
- `$GH/dm-pginstall`: specific paths to `/usr/local/postgresql/bin/*`, `dscl`, `./pgstatus.py`.
- `$GH/generous-corp-marketplace`: allows `codex:*`.
- `$GH/mac-agent`: two one-off permissions. AI/ dir with START_HERE.md, in_flight/, contract.md, design files.
- `$GH/sailer-immich`: empty `.claude` dir.
- `$GH/spacenote`: two repo-scoped git commands.
- `$GH/thehighlighter` (group-level): broad allow list for the tesseretica ecosystem (python, pip, pytest, psql, latexml, flask, docker compose, npm, tesseretica-worker CLI, WebSearch/WebFetch).
- `$GH/thehighlighter/tesseretica-component-viewer`: very broad allow list. AI/ dir with START_HERE.md, TODO.md, links.yaml, services.yaml, state.yaml.
- `$GH/trillianverse`: tree, wc, pip install, python -m build, tar, git mv, WebSearch, npm, docker compose.
- `$GH/trillianverse/trillian_api_server`: `tree:*` only.
- `$GH/trillianverse/trillian-dark`: `Bash(git *)`. AI/ dir with START_HERE.md.

---

## PROJECT MEMORIES (~/.claude/projects/*/memory/)

- **agent-orchestrator**: 4 entries — sonnet cost is a non-issue (5x plan; only Opus constrained); silent-skip needs a dedicated audit pass; portfolio scope (8–10 projects, tesseretica as reference implementation); `/loop` + file-mailbox IPC as lighter alternative to a daemon broker.
- **astplot-js**: ~10 files — current dev state, API redesign plan, long-term architecture, responsive-mode design decisions, feedback (ask about design directions; AST uses radians).
- **astrothesaurus-dev**: 45+ files — full project state (UAT v6.0.0, 2,312 concepts; two-stage pipeline; phases 0–2 complete), evaluation findings (SPECTER eliminates domain confusion; gemini-2.5-flash ≈ claude-sonnet-4 at 1/8 cost), feedback (batch API, stop-on-failure, watcher coverage).
- **ccif-patent**: 1 entry — "interactive" means single conversational questions, never batched multiple-choice.
- **claude-wisdom** (this repo): subagent model selection; interactive-means-discussion.
- **demitri-fitsverify**: libfitsverify improvement opportunities; fits-test-suite reference.
- **dmplot**: ~25 files — native macOS scientific data visualization; extensive AppKit/IB feedback (ask-don't-search, no-dm-prefix, focus-one-thing, xcode-checklist, xib-menus); feature designs.
- **fits-test-suite**: ~50 files — 11 confirmed cfitsio bugs (standalone reproductions in `tests/bug_reproductions/`); coverage strategy (stop grind at ~73%, write paper); Track B replacement validation; methodology feedback from 69+ sessions.
- **homelab**: 8 files — infrastructure state, Dell firmware, HA migration, hostnames, power baseline, VLANs, Xeon-for-LLM reference, user profile.
- **mac-agent**: 8 files — Swift+AppKit+IB terminal agent; user prefers AppKit/Obj-C over SwiftUI; "cli"/"app" parallel paths; graph state in versioned SQLite; verify-before-claiming feedback.
- **portfolio**: 8 files — CV project conventions; user is not a web dev; trust/autonomy feedback for web infra decisions. (No repo found under $GH for this one.)
- **spacenote**: 3 files — float-vs-space assignment semantics; user prefers native Mac apps.
- **storage**: 4 files — box numbering, DVD backup philosophy, valuable-item flagging, photo layout conventions.
- **tesseretica-code**: 15 files — design decisions, broken-file pointer, local ASCL SQLite, salmon sibling clone, subscription vs API credit pool.
- **tesseretica**: ~120+ files (largest) — Triage Coordinator role (opt-in), Session Protocol (review style, stopping rule, commit discipline, worktree isolation, token economy), Current State, Active Work & Queues, Coding & Design Rules (~15), Quality/Review (~10), LLM rules, Infrastructure.
- **GitHub top-level**: lunchtime is a 56-core worker box (arXiv tars, patched-LaTeXML container, production paperboy at .66, no ssh, wedges under load); Little Snitch + sandbox block Python outbound — tunnel via lunchtime; multi-session status uses `in_flight/`; ingest→bug→fix automation via GitHub issues.
- **~/tmp**: 10 files — cross-project user profile, bash setup, tax filing status, Pushover reference, codex noninteractive mode, no-coauthor-trailer convention.
- **UAT**: MEMORY.md only.

---

## AI/ DIRECTORY CONVENTION (cross-repo)

~25 repos have an `AI/` directory at root serving as the agent session/knowledge store: `AI/START_HERE.md` as orientation entrypoint, `AI/in_flight/` for the `/park` skill, plus per-project TODO/design/session files. Two repos deviate in naming: `openalex-local` uses `AI Agents/`; tesseretica's CLAUDE.md references `@AI Notes/START_HERE.md`.

---

## REPOS WITH NO MEANINGFUL CUSTOMIZATION

`sailer-immich` (empty .claude), `spacenote` (2 git permissions), `trillianverse/trillian_api_server` (tree only), `coa-helper` (3 Bash permissions), `generous-corp-marketplace` (codex permission only).
