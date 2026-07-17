---
description: "Cross-platform tool aliases and environment standards"
---

# Cross-Platform Toolchain Standards

To prevent cross-platform path and alias issues (Windows/macOS/Linux) and to avoid agentic headaches, ALWAYS strictly adhere to the following command patterns when interacting with this repository.

## Python Execution
Do not invoke `python`, `python3`, or `py` directly, as this leads to virtual environment resolution errors across OSes.
**Rule:** Always prefix python script execution with `uv run`.
- Correct: `uv run python script.py`
- Correct: `uv run pytest tests/`
- Incorrect: `python3 script.py`

## Antigravity CLI
**Rule:** Always use the alias `agy` for the Antigravity CLI. Do not use `antigravity-cli` or any other alias.
- Correct: `agy run ...`

## Graphify
**Rule:** Always use `graphify` directly (installed globally via `uv tool install graphifyy`). 
- Correct: `graphify extract ./src`

## Node / Frontend (ikp_web)
**Rule:** Use `npm run <script>` to execute frontend scripts (e.g. `npm run dev`, `npm run build`, `npm run lint`). 

## Package Management
- For python packages: Use `uv pip install <package>` or `uv add <package>` instead of `pip install`.
- For node packages: Use `npm install` inside the `ikp_web` directory.

## The `tools/` Directory
The `tools/` folder in the project root contains wrappers for `python`, `pip`, `agy`, and `graphify` that automatically implement the rules above. The user has this directory in their `PATH`, meaning the commands are natively intercepted and corrected. Do not remove or alter these scripts.
