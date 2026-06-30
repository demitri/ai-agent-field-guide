#!/usr/bin/env python3
"""
ccusage_sync.py — sync ccusage --json output to SQLite idempotently.

Usage (stdin):
    npx ccusage --json | python3 ~/bin/ccusage_sync.py

Usage (auto, when npx is on PATH):
    python3 ~/bin/ccusage_sync.py --auto

Cron: use ccusage_sync_cron.sh which loads nvm first.
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

DB_PATH    = Path.home() / ".ccusage" / "usage.db"
STALE_DAYS = 5   # ping via pushover when newest record is this many days old


def infer_provider(model: str) -> str:
    if model.startswith("claude"):
        return "Claude"
    if model.startswith(("gpt", "o1", "o3", "o4", "codex")):
        return "OpenAI"
    if model.startswith("gemini"):
        return "Gemini"
    return "Other"


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usage (
            date                TEXT NOT NULL,
            model               TEXT NOT NULL,
            provider            TEXT NOT NULL,
            input_tokens        INTEGER NOT NULL DEFAULT 0,
            output_tokens       INTEGER NOT NULL DEFAULT 0,
            cache_read_tokens   INTEGER NOT NULL DEFAULT 0,
            cache_create_tokens INTEGER NOT NULL DEFAULT 0,
            cost                REAL    NOT NULL DEFAULT 0.0,
            first_seen          TEXT    NOT NULL,
            last_updated        TEXT    NOT NULL,
            PRIMARY KEY (date, model)
        );

        CREATE TABLE IF NOT EXISTS sync_log (
            synced_at     TEXT    PRIMARY KEY,
            rows_upserted INTEGER NOT NULL,
            latest_date   TEXT    NOT NULL
        );
    """)
    conn.commit()


def sync(conn: sqlite3.Connection, data: dict) -> tuple[int, str]:
    now = datetime.now(timezone.utc).isoformat()
    upserted   = 0
    latest_date = ""

    for entry in data.get("daily", []):
        day = entry["period"]
        if day > latest_date:
            latest_date = day

        for mb in entry.get("modelBreakdowns", []):
            model    = mb["modelName"]
            provider = infer_provider(model)

            conn.execute("""
                INSERT INTO usage
                    (date, model, provider,
                     input_tokens, output_tokens, cache_read_tokens, cache_create_tokens,
                     cost, first_seen, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date, model) DO UPDATE SET
                    provider            = excluded.provider,
                    input_tokens        = excluded.input_tokens,
                    output_tokens       = excluded.output_tokens,
                    cache_read_tokens   = excluded.cache_read_tokens,
                    cache_create_tokens = excluded.cache_create_tokens,
                    cost                = excluded.cost,
                    last_updated        = excluded.last_updated
            """, (
                day, model, provider,
                mb.get("inputTokens", 0),
                mb.get("outputTokens", 0),
                mb.get("cacheReadTokens", 0),
                mb.get("cacheCreationTokens", 0),
                mb.get("cost", 0.0),
                now, now,
            ))
            upserted += 1

    conn.execute(
        "INSERT OR REPLACE INTO sync_log (synced_at, rows_upserted, latest_date) VALUES (?, ?, ?)",
        (now, upserted, latest_date),
    )
    conn.commit()
    return upserted, latest_date


def days_stale(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT MAX(date) FROM usage").fetchone()
    if not row or not row[0]:
        return -1
    return (date.today() - date.fromisoformat(row[0])).days


def pushover(message: str) -> None:
    try:
        subprocess.run(["pushover", message], check=True, timeout=10)
    except Exception as e:
        print(f"pushover failed: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync ccusage --json to SQLite")
    parser.add_argument("--db", default=str(DB_PATH), metavar="PATH",
                        help="SQLite database path (default: %(default)s)")
    parser.add_argument("--auto", action="store_true",
                        help="Run 'npx ccusage --json' automatically (npx must be on PATH)")
    parser.add_argument("--check-only", action="store_true",
                        help="Skip sync; just check staleness and alert if needed")
    parser.add_argument("--stale-days", type=int, default=STALE_DAYS, metavar="N",
                        help="Pushover alert threshold in days (default: %(default)s)")
    args = parser.parse_args()

    db_path = Path(args.db)

    if args.check_only:
        if not db_path.exists():
            pushover("ccusage DB missing — sync cron may not be running")
            sys.exit(0)
        conn = sqlite3.connect(db_path)
        stale = days_stale(conn)
        latest = conn.execute("SELECT MAX(date) FROM usage").fetchone()[0] or "none"
        conn.close()
        if stale < 0:
            msg = "ccusage DB is empty — initial sync may not have run"
            print(f"WARNING: {msg}", file=sys.stderr)
            pushover(msg)
        elif stale > args.stale_days:
            msg = (f"ccusage data is {stale} days stale (latest: {latest}). "
                   f"Sync cron may have failed.")
            print(f"WARNING: {msg}", file=sys.stderr)
            pushover(msg)
        else:
            print(f"ok  latest={latest}  stale={stale}d")
        return

    db_path.parent.mkdir(parents=True, exist_ok=True)

    if args.auto:
        result = subprocess.run(
            ["npx", "ccusage", "--json"],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(result.stdout)
    elif not sys.stdin.isatty():
        data = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    init_db(conn)
    upserted, latest_date = sync(conn, data)
    stale = days_stale(conn)
    conn.close()

    print(f"synced {upserted} model-day rows  latest={latest_date}  db={db_path}")

    if stale < 0:
        msg = "ccusage sync produced no rows — ccusage output may be empty or malformed"
        print(f"WARNING: {msg}", file=sys.stderr)
        pushover(msg)
    elif stale > args.stale_days:
        msg = (f"ccusage data is {stale} days stale (latest: {latest_date}). "
               f"Claude session logs may have been pruned.")
        print(f"WARNING: {msg}", file=sys.stderr)
        pushover(msg)


if __name__ == "__main__":
    main()
