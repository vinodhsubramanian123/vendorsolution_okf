---
name: Agent Lifecycle Operations
description: Standard operational commands for agents working on the IKP project to ensure OS-agnostic command execution.
---

# Agent Lifecycle Operations

To prevent OS-specific command failures or dependency guessing, ALWAYS use the provided `Makefile` commands from the root of the repository `/home/vinodh/vendorsolution_okf`. Do not manually run `pip install` or `npm install` inside bash scripts unless strictly necessary.

## Python Backend (IKP Platform)

*   **Install Dependencies**: `make install` (This uses `uv sync --extra dev` behind the scenes, ensuring the lockfile is respected).
*   **Run Tests**: `make test` (Executes the full pytest suite in a hermetic environment).
*   **Run Linter**: `make lint` (Runs Ruff and Mypy).
*   **Clean Cache**: `make clean` (Cleans `__pycache__`, `.pytest_cache`, etc.).
*   **Run API**: `make run` (Starts the FastAPI server).

## Frontend UI (IKP Web)

*   **Install Dependencies**: `make ui-install` (Runs `npm install` within `ikp_web`).
*   **Run E2E Tests**: `make ui-test` (Executes Playwright tests via `npm run test:e2e`).
*   **Run Dev Server**: `make ui-dev` (Starts the Vite development server).

By wrapping these inside `Makefile` targets, you abstract away the specific underlying package manager arguments and OS paths, ensuring that execution works seamlessly across Ubuntu, Linux Mint, MacOS, or Windows WSL.
