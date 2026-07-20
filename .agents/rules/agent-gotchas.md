---
description: "Repository pitfalls, sandbox limitations, and execution gotchas for AI agents"
---

# Agent Gotchas & Edge Cases

When operating within this repository, agents MUST be aware of the following critical context and edge cases to avoid breaking the environment or causing infinite loops:

## 1. Sandbox Authentication Traps
When using CLI tools that require browser-based authentication (such as `agy login` or `antigravity-cli login`), **do not run them inside the default agent sandbox**.
The ephemeral sandbox will wipe the OAuth token when the agent exits, forcing the user to re-authenticate on every new session.
**Rule:** You MUST request `unsandboxed` permission via `ask_permission` and run the login command directly on the host machine to permanently persist the token.

## 2. Obsidian Export & Gitignore
The `graphify` tool was previously run to export an Obsidian Vault directly into the project root directory. This generated hundreds of individual markdown nodes at the root level.
**Rule:** The root `.gitignore` handles this mess by ignoring `/*.md` but explicitly whitelisting core documentation (`!/README.md`, `!/CONTEXT.md`, etc.). 
**CRITICAL:** Never remove this whitelist logic from `.gitignore`. If you create a new top-level markdown document that needs to be tracked by git, you MUST add it to the `.gitignore` whitelist first.

## 3. Path Preservation
The host machine may switch between Windows and macOS. The `tools/` folder was created to normalize this. Assume `tools/` is already in the user's `$PATH`, which intercepts standard calls like `python`, `pip`, and `agy` to ensure they run with absolute perfection cross-platform.

## 4. Verify CLI flags before using them — do not infer them from naming convention
Commit `a6ef5df` shows an agent adding `--elevate` and `--parallel` flags to
`antigravity-cli` subprocess calls in `llm_client.py`, because a prior
instruction implied the CLI should "elevate reasoning quality" and "run in
parallel." Those flags do not exist. The agent caught this itself by
actually running `antigravity-cli --help` before shipping, and used
`concurrent.futures` for the parallel part instead — but this was a near
miss, not a caught-in-code-review bug, and it would have broken the whole
extraction pipeline with an "unrecognized flag" error on every ingestion run.
**Rule:** Before adding any new flag/argument to a `subprocess` call for
`antigravity-cli`, `graphify`, or any other external CLI tool used in this
repo, run `<tool> --help` (or read its documented flag list) first and
confirm the flag actually exists in the output. Never add a flag because the
name "sounds right" for what you're trying to accomplish — verify, then use.
This applies equally to library APIs: if you're not certain a method/kwarg
exists on a dependency (chromadb, networkx, pydantic, fastapi, mcp), check
the installed version's actual signature rather than assuming it matches an
API you remember from training data or from a different version.

## 5. Background Processes and Browser Testing
When starting the local API or UI servers (`start_api.sh`, `start_ui.sh`) for browser testing, standard background tasks will automatically terminate all their child processes when the task finishes, causing the servers to crash instantly.
**Rule:** You MUST use a Persistent Terminal (`RunPersistent: true` in `run_command`) when starting the application servers. Furthermore, always verify the port is bound and responding (e.g., via `curl` or `lsof`) before launching a `browser_subagent` to avoid wasting time on `ERR_CONNECTION_REFUSED` failures.
