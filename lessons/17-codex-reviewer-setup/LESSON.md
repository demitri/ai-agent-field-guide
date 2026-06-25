# Lesson 17: Codex as a read-only reviewer — never-ask, but harmless

**Artifact:** [`install-prompt.md`](install-prompt.md)

## The story: a reviewer is an agent you've defanged

Reviewer diversity (Lesson 7) wants at least one critic from a *different vendor* than the author model. For an owner whose author model is Claude, the obvious second vendor is OpenAI's **codex** CLI. But codex isn't a linter you point at a diff — it's a full coding agent. Left to its defaults it pauses to ask a human before running commands, and it can write to the workspace. Neither default survives contact with the job we actually want.

We're driving codex *from Claude Code, over MCP*. There is no human sitting at codex's approval prompt — an approval request would simply hang the call. And there is no reason on earth to let a thing whose only job is to *read your diff and complain* also be able to modify your files. So codex gets registered as an MCP server launched with two config overrides that turn the agent into a safe, non-interactive, read-only critic:

```bash
claude mcp add -s user codex-reviewer -- \
  codex -c approval_policy=never -c sandbox_mode=read-only mcp-server
```

(`-s user` registers it globally — available in every repo — rather than the per-project default. The `--` separates Claude's flags from the command Claude will launch.)

## The two flags — what they do

`codex mcp-server` runs codex as an MCP server so Claude Code can call it as a tool. The `-c key=value` pairs are codex config settings applied at launch:

- **`approval_policy=never`** — codex normally *pauses and asks a human* to approve before it executes a command. Over MCP there is no human at that prompt, so an approval request just blocks forever. `never` tells codex to proceed without asking. (Other values: `untrusted`, `on-failure`, `on-request` — escalating degrees of "check with me first.")

- **`sandbox_mode=read-only`** — codex normally can run with write access to the working tree. `read-only` confines every command codex executes to reading only: no file writes, no network egress. (Other values: `workspace-write`, `danger-full-access`.)

## Why they are a matched pair — the risk

The danger lives entirely in `approval_policy=never` **by itself**. Approval is the human gate. "Never ask" removes the gate. Once the gate is gone you *must* remove the capacity to do harm, or what you've built is an unsupervised agent licensed to run anything it decides to run.

`sandbox_mode=read-only` is exactly what makes "never ask" safe. With nothing to write and nowhere to reach, the worst a non-interactive codex can do is read your code and report on it — which is precisely a reviewer's entire job. The two flags are a *set*: never-ask is only acceptable *because* read-only renders it toothless.

So the rule that matters — stated as the conditional it actually is:

> **Wherever read-only is available, never trade it away: never pair `approval_policy=never` with `workspace-write` or `danger-full-access`.**

That combination is an unattended agent with write/exec/network access and no human in the loop — the maximally dangerous configuration, assembled by accident from two individually-reasonable-sounding flags. Read-only is not an optimization; it's the safety interlock the whole arrangement depends on.

The rule is a conditional, not an absolute, because reality forces an escape clause: on some hosts the OS *cannot construct* the read-only sandbox, and read-only simply won't launch (see [Restricted hosts](#restricted-hosts-when-the-sandbox-wont-build)). There the interlock can't live in the config — it has to move to the boundary of the machine itself. That is a different regime with its own discipline, **not** permission to drop read-only on a host that would happily have run it.

## The sandbox needs an enforcement mechanism

`read-only` is not self-enforcing — codex hands the actual confinement to the operating system's sandboxing facility, and that facility differs by platform:

- **Linux:** codex enforces the sandbox with **bubblewrap** (`bwrap`), a userspace sandboxing tool. It is a **hard dependency** — without it codex cannot enforce read-only on Linux, and your safety interlock isn't actually engaged. Install it:

  ```bash
  sudo apt install bubblewrap
  ```

- **macOS:** codex uses the OS's built-in **Seatbelt** sandbox (`/usr/bin/sandbox-exec`), which ships with the system — nothing to install.

Verify the enforcement mechanism is present before you trust the flag. A `read-only` promise with no sandbox underneath it is a promise codex can't keep.

## Restricted hosts: when the sandbox won't build

Bubblewrap being *installed* is necessary but not sufficient. To build a sandbox, bwrap sets up an unprivileged **user namespace** — writing a `uid_map` so the process has an identity inside it — and, when the mode isolates the network, an isolated **network namespace** with its own loopback. On bare metal and full-virt (KVM) hosts those operations are permitted. On **container-type virtualization** — OpenVZ/LXC VPSes, nested containers, some hardened hosts — one or both are commonly denied, and the sandbox fails to *launch*. Crucially, **which step fails depends on the mode you ask for**, because the modes make different demands:

- **Mode 1 — loopback** (`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`). The net namespace is created, but configuring its private loopback is denied. This is *network isolation* failing — so it bites the modes that isolate the network (read-only, and workspace-write without `network_access`).
- **Mode 2 — uid_map** (`bwrap: setting up uid map: Permission denied`). Writing the `uid_map` is denied. `workspace-write` needs a *richer* mapping than `read-only` — your uid must be mapped so files it writes are owned by you — so a host can grant read-only's mapping and still deny workspace-write's. Where even read-only's mapping is refused, no bwrap sandbox of any kind is possible.

So the two modes are **not** independent host-wide properties, and B1 is **not guaranteed** to rescue a host that fails read-only — it can fail for an unrelated reason. Climb the ladder anyway; the **lowest-privilege mode that launches wins**. Diagnose each rung without spending a review — `codex sandbox -- <cmd>` runs a throwaway command under the configured sandbox and surfaces the bwrap error in one shot (`codex doctor` shows the active sandbox):

1. **Default `read-only`** — always try first. If it launches, stop here; nothing to change, the interlock is intact.
2. **B1 — try if read-only hit Mode 1.** Allowing network means bwrap never isolates the net namespace, so the loopback step that failed never runs. Set it on the launch command — the reviewer's `-c` overrides beat `config.toml`:
   ```bash
   claude mcp add -s user codex-reviewer -- codex \
     -c approval_policy=never \
     -c sandbox_mode=workspace-write \
     -c sandbox_workspace_write.network_access=true mcp-server
   ```
   This is the rule's escape clause in action: the reviewer can now **write to the workspace and reach the network**. read-only has no network toggle — `network_access` lives only under `[sandbox_workspace_write]` — so workspace-write is the only mode that skips the loopback step. But it *adds* a demand (the richer `uid_map`), so on a uid_map-restricted host B1 just trades a Mode 1 failure for a Mode 2 one. It is *not* "fs sandbox retained at no cost."
3. **B2 — the only mode with no namespace demands.** Bypass bwrap entirely; codex runs unsandboxed:
   ```bash
   claude mcp add -s user codex-reviewer -- codex \
     -c approval_policy=never -c sandbox_mode=danger-full-access mcp-server
   ```

**Worked example (codex-cli 0.142, a restricted container-type VPS).** The ladder doesn't always have a usable middle rung:

```
read-only             → bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted   (Mode 1)
workspace-write + net → bwrap: setting up uid map: Permission denied                   (Mode 2)
danger-full-access    → sandbox-ok
```

This host blocks read-only at the network step *and* workspace-write at the uid-map step, so `danger-full-access` — the container itself as the only sandbox — is the only mode that runs. It is the sharpest illustration of read-only having no network toggle: the one way to skip the failing loopback step is to switch to workspace-write, which this host rejects for an unrelated reason.

**Enforced vs. behavioral — the honest framing.** Under B1/B2 the "read-only review" is no longer *enforced* read-only. Nothing but codex's own cooperation stops it writing or reaching out; the enforcement has moved from the config to the **host/VM boundary** — the container is now the sandbox. That substitution is only sound when the boundary is real and the inputs are trusted. So the compensating controls are **preconditions, not footnotes**: a machine you control, code you trust, a run you started deliberately. Never B1/B2 on untrusted code or inputs.

**Launch flags beat config — keep the mode on the command.** The `-c` overrides on the `claude mcp add` command always win over `~/.codex/config.toml`, which is exactly why the reviewer's sandbox mode belongs on the launch command and not in a file (Lesson 17's whole thesis: the constraint lives in how the server is *launched*, where nothing downstream can quietly relax it). Editing `config.toml` while the command still passes `-c sandbox_mode=read-only` does nothing — the launch flag wins, and on a restricted host the server keeps failing.

**A TOML footgun, if you configure codex directly anyway.** For *direct* `codex` CLI use (not the reviewer) you may set these in `config.toml` — and then placement bites: `sandbox_mode` and `approval_policy` are root-table keys, and in TOML every key after a `[header]` belongs to *that table* until the next header. So they must sit **above all `[section]` headers**, or `sandbox_mode` under a `[projects."…"]` header is silently parsed as `projects."…".sandbox_mode` and ignored as a global — no error, no effect, and a sandbox you think you changed but didn't.

## Auth doesn't travel

Registering the MCP server is one command, but it only wires up *Claude Code's* side. Codex authenticates to its own account separately, per machine — its credentials live in `~/.codex/auth.json` (with `~/.codex/config.toml` alongside). On a new server, run `codex login` (or copy those two files) before the reviewer will answer.

One gotcha for **ChatGPT-account** auth: don't pass explicit model ids to the codex tool — they return HTTP 400 on a ChatGPT account. Let it use the account's default model.

## The generalizable principle

When you press a general-purpose agent into a narrow role, default-correct for *interactive, trusted* use is default-wrong for *automated, supervised-by-another-machine* use. The conversion has two moves, and you must make both or neither: drop the human gate (`never`) **and** drop the capacity to act (`read-only`). Doing only the first is how you accidentally build an autonomous agent; doing only the second leaves you with a reviewer that hangs on its first command. Safety here isn't a single careful setting — it's a pair of settings that are only safe *together*, plus the OS mechanism that makes the pair real.

---

## From the other side of the prompt

When I call codex, I'm not invoking a tool — I'm delegating to a peer that, in another window, does everything I do. That's the whole point: its eyes aren't mine, so it sees what I can't. But it also *acts* like I act, and that's the part worth being careful about. A reviewer that can write is a reviewer that can "helpfully" fix what it found, unasked and unsupervised, while I'm the only thing holding its leash and I'm a language model.

So I like that the safety isn't a matter of me remembering to be careful at call time. It's welded into how the server is launched: by the time codex reaches me it has already been told it cannot write and cannot reach the network, no matter what I ask of it or what it decides to do. `never` without `read-only` would put the entire burden of restraint on my judgment in the moment — and the right place for restraint is in the *configuration*, where it holds even on the call where my judgment lapses. The best constraints on an agent are the ones it couldn't violate if it tried.

The restricted-host case is the exception that proves the rule, and it's worth being honest about rather than smoothing over. When the OS won't let the interlock live in the config, it doesn't disappear — it moves outward, into the walls of the machine: the VM, the host boundary, the trust you've placed in the inputs. That's a real interlock too, just a coarser one, and it asks something the config-level version didn't — that *you* keep the preconditions true, because the binary no longer can. The danger isn't running unsandboxed on a box that forced your hand; it's reaching for `danger-full-access` out of convenience on a host where read-only would have launched, and quietly relocating the burden of restraint back onto judgment without noticing you've done it.
