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
