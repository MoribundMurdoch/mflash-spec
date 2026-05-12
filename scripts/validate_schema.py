#!/usr/bin/env python3

"""
Validate all JSON Schema files in schema/.

This checks:
- the file is valid JSON
- the file is a valid Draft 2020-12 JSON Schema

Requires:
  python -m pip install jsonschema

On Arch Linux, prefer a venv:
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install jsonschema
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema")
    print()
    print("Recommended setup:")
    print("  python -m venv .venv")
    print("  source .venv/bin/activate")
    print("  python -m pip install jsonschema")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    failed = False

    schema_files = sorted(SCHEMA_DIR.glob("*.json"))

    if not schema_files:
        print("No schema files found.")
        return 1

    for path in schema_files:
        try:
            data = load_json(path)
            jsonschema.Draft202012Validator.check_schema(data)
            print(f"OK   {rel(path)}")
        except Exception as e:
            failed = True
            print(f"FAIL {rel(path)}: {e}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
