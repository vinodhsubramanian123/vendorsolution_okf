# Vendorsolution OKF

> First time here? See **[SETUP.md](SETUP.md)** for install, environment
> variables, seeding the knowledge repository, and running the app/tests.
> This doc covers the cross-platform CLI toolchain only.

> Current architecture/runtime truth lives in
> **[IKP/standards/11_CURRENT_IMPLEMENTATION_STACK.md](IKP/standards/11_CURRENT_IMPLEMENTATION_STACK.md)**.

## Cross-Platform Toolchain Setup

> [!NOTE]
> For detailed setup instructions, database seeding, and tests, see **[SETUP.md](SETUP.md)**.
> For architecture standards, see `IKP/standards/`.
To completely prevent path, alias, and virtual environment issues when developing across Windows, macOS, and Linux, we have shipped a `tools/` directory inside this repository.

### 1. Add `tools/` to your PATH
Add the absolute path of the `tools/` folder to your system `PATH`. 
By doing this, you instantly get access to the following project-safe aliases across all operating systems:

- **`python`**: Safely redirects to `uv run python`. You can run `python script.py` anywhere in this project and it will always use the correct virtual environment!
- **`pip`**: Safely redirects to `uv pip`.
- **`agy`**: Properly aliases the Antigravity CLI (`antigravity-cli`), fixing the 'command not found' errors.
- **`graphify`**: Standardized command for the graphify extractor.

*(If you don't want to modify your PATH, you can simply run them like `./tools/python`, `./tools/agy`, etc.)*

### 2. Frontend (ikp_web)
The frontend uses standard Node/Vite tools. Run scripts via npm:
```bash
cd ikp_web
npm install
npm run dev
npm run build
```

For normal full-stack local work, prefer the project start scripts:

```bash
./scripts/start_api.sh
./scripts/start_ui.sh
```

Defaults are API `8000` and UI `5173`. The scripts normalize accidental
leading-`1` five-digit local ports, for example `15173` to `5173`.

## Agent Configuration
AI coding assistants (like Antigravity, Cursor, etc.) will automatically read the `.agents/rules/toolchain.md` file in this repository to enforce these aliases natively, preventing agentic headaches.

## Architecture & Capabilities

| Capability | Status | Description |
|---|---|---|
| **Graph Bootstrap** | Implemented | Bi-directional sync between Markdown files and NetworkX graph. |
| **PDF Ingestion** | Implemented | Extracts components via vendor-agnostic adapter framework (e.g., HPE QuickSpecs). |
| **Reasoning Engine** | Implemented | Deterministic evaluation of rule triggers (`REQUIRES`, `INCOMPATIBLE_WITH`). |
| **BOQ Validation** | Implemented | Fuzzy matching, typo learning loop, and graph-based validation. |
| **Partner Portal API** | Planned | Placeholder in LangGraph; currently acts as a stub for live vendor validation. |
| **MCP / Obsidian** | Optional | MCP integration is optional and may not be available in all environments. |

*Note: The generated OKF files are placed in `repository/`. Fallback human-in-the-loop review files go to `needs_review/`. Typo learning deltas persist in `history/`.*

Do not treat older blueprint wording as proof that a capability is live.
Check the current implementation stack doc and code before promising a
behavior.
