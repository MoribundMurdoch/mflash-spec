#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    *ROOT.glob("schema/*.json"),
    *ROOT.glob("examples/**/*.json"),
]

def main() -> int:
    failed = False

    for path in sorted(JSON_FILES):
        try:
            with path.open("r", encoding="utf-8") as f:
                json.load(f)
            print(f"OK   {path.relative_to(ROOT)}")
        except Exception as e:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)}: {e}")

    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
