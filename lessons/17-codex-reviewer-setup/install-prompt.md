<!-- Human: paste this file into a Claude Code session (or @-reference it)
     and Claude will register codex as a read-only, non-interactive reviewer,
     adapted to your machine. Prerequisite: the review panel from Lesson 7.
     Background — what the flags do and why they're a matched pair: LESSON.md. -->

# Setup task: register codex as a read-only reviewer (MCP)

You (Claude) are registering OpenAI's codex CLI as a cross-vendor reviewer that
the user can invoke over MCP. It must be **non-interactive** (no human at its
approval prompt) and **read-only** (a reviewer never mutates the tree). Do not
proceed past any step that fails — surface it and ask.

## Steps

1. **Check codex is installed.** Run `codex --version`. If it's missing, stop
   and tell the user — codex is the prerequisite; don't try to install it
   yourself unless they ask (installation routes are their policy).

2. **Check the sandbox enforcement mechanism** for their platform — `read-only`
   is enforced by the OS, and without the mechanism the flag is an empty promise:
   - **Linux:** `which bwrap`. If absent, tell the user to run
     `sudo apt install bubblewrap` (a hard dependency) before continuing.
   - **macOS:** `which sandbox-exec` — built in at `/usr/bin/sandbox-exec`,
     nothing to install. Confirm it's present.

2a. **On Linux, confirm the sandbox actually *constructs*** — bwrap being
   installed is necessary but not sufficient on container-type VPSes (OpenVZ/LXC,
   nested containers). Test it cheaply, without a review:

   ```bash
   codex sandbox -- echo sandbox-ok      # default (read-only)
   ```

   - Prints `sandbox-ok` → read-only works; keep it, go to step 3.
   - `bwrap: loopback: Failed RTM_NEWADDR …` → Mode 1. Re-test with B1:
     `codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- echo sandbox-ok`.
   - `uid_map` / userns error even under B1 → Mode 2; only `danger-full-access`
     will launch.

   If you land on B1 or B2, **stop and get explicit confirmation**: those modes
   give the reviewer write and/or network access, so the enforcement has moved to
   the host/VM boundary. Confirm this is a machine they control, the code is
   trusted, and the run is deliberate — never on untrusted inputs. Then carry the
   chosen mode's `-c` flags **into the step-4 registration command** — they
   override `config.toml`, so the launch command (not a config file) is what
   actually governs the reviewer:
   - **B1:** `-c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true`
   - **B2:** `-c sandbox_mode=danger-full-access`

3. **Confirm codex auth exists.** Look for `~/.codex/auth.json`. If it's missing,
   tell the user to run `codex login` first — auth is per-machine and does not
   travel with the MCP registration.

4. **Register the MCP server**, non-interactive, with the sandbox mode resolved
   above. Default to user scope (`-s user`) so it's available in every repo;
   confirm that's what they want first. Use `read-only` unless step 2a forced
   B1/B2:

   ```bash
   claude mcp add -s user codex-reviewer -- \
     codex -c approval_policy=never -c sandbox_mode=read-only mcp-server
   ```

   On a restricted host, **swap the `-c sandbox_mode=read-only`** for the B1 or B2
   flags from step 2a — the launch command's `-c` overrides are what start the
   server, so editing `config.toml` won't help while the command sets `-c
   sandbox_mode`.

   Before running it, explain the two flags in one line each, and the rule:
   `approval_policy=never` is only safe **because** `sandbox_mode=read-only`
   removes its teeth — never pair `never` with `workspace-write` or
   `danger-full-access` *unless the host left no read-only option* (see LESSON.md,
   Restricted hosts).

5. **Verify** with `claude mcp list` — expect `codex-reviewer ... ✔ Connected`.

6. **Note the ChatGPT-account gotcha** if relevant: when invoking the codex tool,
   don't pass explicit model ids — they return HTTP 400 on a ChatGPT account.
   Use the account default.

## What you've built

A reviewer that can read the repo and report, but cannot write to it, reach the
network, or block waiting for an approval no human will give — the three
properties that make a general-purpose coding agent safe to drive from another
agent. Slot it into the panel from Lesson 7 as the cross-vendor lens.
