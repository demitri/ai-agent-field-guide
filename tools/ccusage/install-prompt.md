<!-- Human: paste this file into a Claude Code session (or @-reference it) and
     Claude will install the ccusage SQLite sync and plotting tools on your
     machine. To do it by hand instead: copy the three scripts alongside this
     file to ~/bin/, make them executable, add the two crontab entries from
     the Cron section below, and run the initial sync. -->

# Setup task: ccusage → SQLite sync + plotting

You (Claude) are installing two tools that work together:

- **`ccusage_sync.py`** — reads `npx ccusage --json` output and upserts it
  into a local SQLite database idempotently (primary key: date + model). Runs
  daily via cron and sends a Pushover alert if data goes stale.
- **`ccusage_plot.py`** — reads `npx ccusage --json` directly and produces a
  two-panel matplotlib figure: daily cost per model (color = provider,
  linestyle = model variant) and daily token volume by provider.

The scripts are in the same directory as this file. Copy them to the user's
machine; do not modify them during install. Inspect first, show before writing,
ask one question at a time, merge — never clobber.

---

## Step 1 — Inspect

Before asking anything:

1. **Check for an existing install**: look for `ccusage_sync.py` in `~/bin/`
   and `~/.local/bin/`; check `crontab -l` for any existing ccusage entries;
   check for `~/.ccusage/usage.db`.
2. **Check prerequisites** (stop if any are missing — name the tool and what
   it's for; do not degrade):
   - `python3` with `matplotlib` and `numpy`: `python3 -c "import matplotlib, numpy"`
   - `npx ccusage --json` — run it and confirm it returns valid JSON. If npx
     isn't on PATH, check for nvm: `[ -s "$HOME/.nvm/nvm.sh" ]`. If nvm is
     present, note that the cron wrapper handles this automatically; if npx is
     absent entirely, stop.
   - `pushover` (for staleness alerts): `which pushover`. If absent, note it
     and ask whether to proceed without staleness alerts or to install it first
     (don't install it yourself).
3. Identify `python3` path: `which python3`.

Report what you found in one compact block, then proceed to the interview.

---

## Step 2 — Interview (one question at a time)

Ask only what inspection didn't answer:

1. **Bin directory**: where should the scripts live? Default: `~/bin/` (suggest
   `~/.local/bin/` on Linux). Confirm the directory exists and is on PATH.
2. **Database path**: where should the SQLite DB live? Default:
   `~/.ccusage/usage.db`.
3. **Stale-days threshold**: how many days before a Pushover alert fires?
   Default: 5. (Explain: the daily sync cron fires this alert if the newest
   record is older than N days — catches pruned session logs.)
4. **Node/nvm situation**: if nvm is present, confirm the default alias
   (`cat ~/.nvm/alias/default`) — the cron wrapper calls `nvm use default`.
   If node is installed system-wide (no nvm), note that the cron wrapper can
   be simplified and ask whether to do so.

---

## Step 3 — Show, then install

### 3a. Scripts

Copy the three scripts from this directory to the chosen bin directory. If any
of them already exist, show a diff (`diff <existing> <new>`) and ask before
overwriting.

```bash
cp ccusage_sync.py      <bin>/ccusage_sync.py
cp ccusage_sync_cron.sh <bin>/ccusage_sync_cron.sh
cp ccusage_plot.py      <bin>/ccusage_plot.py
chmod +x <bin>/ccusage_sync.py <bin>/ccusage_sync_cron.sh <bin>/ccusage_plot.py
```

If the stale-days threshold differs from the default (5), edit `ccusage_sync.py`
to update the `STALE_DAYS` constant before copying — show the proposed edit.

If the database path differs from the default, edit `ccusage_sync.py` to update
`DB_PATH` before copying.

If node is installed system-wide (no nvm), simplify `ccusage_sync_cron.sh` to
remove the nvm lines and call npx directly — show the proposed text.

### 3b. Cron entries

Pass `--db` and `--stale-days` as cron arguments rather than editing the
source constants. `ccusage_sync_cron.sh` forwards all its arguments to
`ccusage_sync.py`, so both the sync and watchdog lines can override defaults
without modifying source.

Show the two proposed crontab lines before installing:

```
# ccusage — sync AI usage data daily
37 8 * * * <bin>/ccusage_sync_cron.sh --db <db_path> --stale-days <N> >> <log_path> 2>&1
# ccusage — staleness watchdog (fires pushover if sync cron fails)
5 9 * * * <python3> <bin>/ccusage_sync.py --check-only --db <db_path> --stale-days <N> >> <log_path> 2>&1
```

Where:
- `<bin>` = chosen bin directory (full path, not `~/`)
- `<python3>` = full path from `which python3`
- `<db_path>` = chosen database path (full path)
- `<N>` = stale-days threshold
- `<log_path>` = DB directory + `/sync.log`

If DB path and stale-days match their defaults (`~/.ccusage/usage.db`, `5`),
omit those flags for cleaner cron lines.

Install by reading the existing crontab, appending the new lines, and writing
back. Never overwrite the full crontab blindly — merge.

```bash
( crontab -l 2>/dev/null; echo ""; echo "# ccusage entries"; echo "<line1>"; echo "<line2>" ) | crontab -
```

If ccusage crontab entries already exist, show the diff and ask before replacing.

---

## Step 4 — Initial sync and verify

Run the initial sync (npx will be available in the terminal even if cron needs
the wrapper):

```bash
npx ccusage --json | python3 <bin>/ccusage_sync.py
```

Then verify:

```bash
sqlite3 <db_path> "SELECT COUNT(*) AS rows, MIN(date) AS earliest, MAX(date) AS latest, ROUND(SUM(cost),2) AS total_cost FROM usage;"
```

Show the output. If it looks wrong (zero rows, or an error), stop and surface it.

Run `--check-only` to confirm the watchdog path works:

```bash
python3 <bin>/ccusage_sync.py --check-only
```

Expected: `ok  latest=<date>  stale=<N>d`

---

## Step 5 — Finish

Summarise what was installed:

- Scripts installed to: `<path>`
- Database: `<path>`
- Cron: sync at 8:37am daily, watchdog at 9:05am daily
- Stale-days threshold: N
- Log: `<path>`
- Initial sync result: N model-day rows, date range, total cost

Note: the cron runs while the machine is on. If the machine is off for more
than `<stale-days>` consecutive days, the next successful cron run will send a
Pushover alert.
