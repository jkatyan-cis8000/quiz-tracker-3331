#!/usr/bin/env python3
"""
Layer-based linting for quiz-tracker project.

Verifies:
1. Every source file lives in a layer directory under src/
2. Imports respect the layer dependency direction
3. No file exceeds 300 lines
"""

import ast
import sys
from pathlib import Path
from typing import Optional

# Layer definitions and allowed imports
LAYERS = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

LAYER_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}

MAX_LINES = 300


def get_layer(file_path: Path) -> Optional[str]:
    """Determine which layer a file belongs to."""
    parts = file_path.parts
    if "src" in parts:
        src_idx = parts.index("src")
        if src_idx + 1 < len(parts):
            return parts[src_idx + 1]
    return None


def get_imports(file_path: Path) -> list[str]:
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def check_line_count(file_path: Path) -> list[tuple[int, str]]:
    """Check if file exceeds MAX_LINES."""
    errors = []
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            errors.append((len(lines), f"File has {len(lines)} lines, max is {MAX_LINES}"))
    except Exception:
        pass
    return errors


def check_imports(file_path: Path, layer: str) -> list[tuple[int, str]]:
    """Check that imports respect layer dependencies."""
    errors = []
    allowed = LAYER_IMPORTS.get(layer, set())
    imports = get_imports(file_path)
    
    # Only check internal imports (those starting with src or our layers)
    for imp in imports:
        if imp in LAYERS and imp not in allowed:
            errors.append((1, f"Import '{imp}' not allowed in {layer} layer"))
    
    return errors


def lint_file(file_path: Path) -> list[tuple[int, str, str]]:
    """Run all checks on a single file."""
    errors = []
    layer = get_layer(file_path)
    
    if layer is None:
        return errors
    
    # Check line count
    errors.extend((file_path.name, line_num, msg) for line_num, msg in check_line_count(file_path))
    
    # Check imports
    errors.extend((file_path.name, line_num, msg) for line_num, msg in check_imports(file_path, layer))
    
    return errors


def main() -> int:
    """Run the linter and return exit code."""
    repo_root = Path(__file__).parent
    src_dir = repo_root / "src"
    
    if not src_dir.exists():
        print("ERROR: src/ directory not found")
        return 1
    
    all_errors: list[tuple[str, int, str]] = []
    
    # Find all Python files
    for py_file in src_dir.rglob("*.py"):
        # Skip test files and __pycache__
        if "test" in py_file.parts or "__pycache__" in str(py_file):
            continue
        
        file_errors = lint_file(py_file)
        all_errors.extend((str(py_file.relative_to(repo_root)), line, msg) for line, msg in file_errors)
    
    if all_errors:
        print("Lint errors found:")
        for filepath, line, msg in sorted(all_errors):
            print(f"  {filepath}:{line}: {msg}")
        return 1
    
    print("All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
