#!/usr/bin/env python3
import os
import ast
import re
import argparse
from pathlib import Path

EXCLUDE_DIRS = {
    ".git", ".github", ".vscode", "node_modules", "venv", ".venv",
    "__pycache__", "dist", "build", "coverage", ".next", ".chroma", "graphify-out", ".agents"
}

EXCLUDE_FILES = {
    "package-lock.json", "yarn.lock", "uv.lock", "pnpm-lock.yaml"
}

def parse_python_ast(filepath: str) -> list[str]:
    """Extracts class and function signatures from a Python file using AST."""
    symbols = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols.append(f"class {node.name}:")
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Only include top-level functions or methods, not nested ones to save space
                if not hasattr(node, "is_nested"): 
                    args = [a.arg for a in node.args.args]
                    symbols.append(f"def {node.name}({', '.join(args)}):")
    except Exception:
        pass
    return symbols

def parse_typescript_regex(filepath: str) -> list[str]:
    """Extracts classes and functions from TS/JS using basic regex to save tokens."""
    symbols = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Match class definitions
        for match in re.finditer(r'^\s*(?:export\s+)?class\s+([A-Za-z0-9_]+)', content, re.MULTILINE):
            symbols.append(f"class {match.group(1)}")
            
        # Match function definitions
        for match in re.finditer(r'^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\(', content, re.MULTILINE):
            symbols.append(f"function {match.group(1)}()")
            
        # Match const arrow functions (top level mostly)
        for match in re.finditer(r'^\s*(?:export\s+)?const\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>', content, re.MULTILINE):
            symbols.append(f"const {match.group(1)} = () =>")
    except Exception:
        pass
    return symbols

def generate_tree(dir_path: str, prefix: str = "", is_last: bool = True) -> str:
    path = Path(dir_path)
    tree_str = ""
    
    if path.name in EXCLUDE_DIRS:
        return ""

    connector = "└── " if is_last else "├── "
    
    if path.is_file():
        if path.name in EXCLUDE_FILES:
            return ""
        tree_str += f"{prefix}{connector}{path.name}\n"
        
        # Add symbols for supported files
        symbols = []
        if path.suffix == ".py":
            symbols = parse_python_ast(str(path))
        elif path.suffix in [".ts", ".tsx", ".js", ".jsx"]:
            symbols = parse_typescript_regex(str(path))
            
        if symbols:
            sym_prefix = prefix + ("    " if is_last else "│   ")
            for i, sym in enumerate(symbols):
                sym_connector = "└── " if i == len(symbols) - 1 else "├── "
                # Truncate very long signatures
                if len(sym) > 80: sym = sym[:77] + "..."
                tree_str += f"{sym_prefix}{sym_connector}♦ {sym}\n"
                
    elif path.is_dir():
        tree_str += f"{prefix}{connector}{path.name}/\n"
        try:
            items = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
            # Filter excluded upfront to calculate is_last correctly
            items = [item for item in items if item.name not in EXCLUDE_DIRS and item.name not in EXCLUDE_FILES]
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, item in enumerate(items):
                item_is_last = (i == len(items) - 1)
                tree_str += generate_tree(str(item), new_prefix, item_is_last)
        except PermissionError:
            tree_str += f"{prefix}    └── [Permission Denied]\n"

    return tree_str

def main():
    parser = argparse.ArgumentParser(description="Generate a token-optimized project topology map.")
    parser.add_argument("path", nargs="?", default=".", help="Directory to map")
    parser.add_argument("--output", "-o", default=".repo_map", help="Output file name")
    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    print(f"Mapping topology for {root_path}...")
    
    tree_output = f"Topology Map for: {root_path.name}\n"
    tree_output += "=" * 50 + "\n"
    tree_output += generate_tree(str(root_path), is_last=True)
    
    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tree_output)
        
    print(f"Topology map saved to {out_path.absolute()}")

if __name__ == "__main__":
    main()
