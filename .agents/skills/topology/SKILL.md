---
name: topology
description: "Generates a highly condensed, token-saving repository map of the project, including file hierarchy and class/function signatures. Use this skill when you need to understand where code is located without reading entire files."
---

# /topology

This is an Atomic Skill designed to save context tokens. It generates a structural map of the codebase by recursively walking the directory and parsing python ASTs and typescript regexes to extract classes and function names.

## Usage

When invoked by the user, or when you determine you need a high-level view of the repository to locate code, run the python script:

```bash
python3 .agents/skills/topology/topology_mapper.py .
```

You can optionally specify a target directory to map a subset of the project:

```bash
python3 .agents/skills/topology/topology_mapper.py ikp_platform/core
```

## What it Does
1. Traverses the directory (ignoring `.git`, `.venv`, `node_modules`, etc.).
2. Extracts `class` and `def` names from Python files.
3. Extracts `class` and `function` / `const = () =>` names from JS/TS files.
4. Outputs the combined hierarchy to a `.repo_map` file in the root directory.

## What You Must Do When Invoked
1. Ensure the script is executable (e.g. `chmod +x .agents/skills/topology/topology_mapper.py` if necessary, though `python3` works directly).
2. Execute the script via the `run_command` tool.
3. Read the resulting `.repo_map` file using the `view_file` tool to ingest the project structure into your context.
4. If the map answers the user's question, respond based on it. If you need deeper implementation details, use the map to pinpoint exactly which file to read next.
