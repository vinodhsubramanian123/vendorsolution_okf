# Vendorsolution OKF

> First time here? See **[SETUP.md](SETUP.md)** for install, environment
> variables, seeding the knowledge repository, and running the app/tests.
> This doc covers the cross-platform CLI toolchain only.

## Cross-Platform Toolchain Setup
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

## Agent Configuration
AI coding assistants (like Antigravity, Cursor, etc.) will automatically read the `.agents/rules/toolchain.md` file in this repository to enforce these aliases natively, preventing agentic headaches.
