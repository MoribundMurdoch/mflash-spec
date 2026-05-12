#!/usr/bin/env python3

"""
Migrate an mflash v1 deck to mflash v2.

This script:
- changes version to 2
- adds a deck id if missing
- adds card ids if missing
- does NOT add created_at or updated_at unless --add-timestamps is used

By default, timestamps are intentionally omitted for privacy/anonymity.

Usage:
  python scripts/migrate_v1_to_v2.py examples/minimal-v1.mflash.json -o /tmp/minimal-v2.mflash.json
  python scripts/migrate_v1_to_v2.py examples/minimal-v1.mflash.json --in-place
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from normalize_deck import normalize_deck


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument(
        "--add-timestamps",
        action="store_true",
        help="Add created_at and updated_at if missing. Off by default for privacy.",
    )
    args = parser.parse_args()

    if args.output and args.in_place:
        print("Use either --output or --in-place, not both.", file=sys.stderr)
        return 2

    deck = load_json(args.input)

    old_version = deck.get("version")
    normalized = normalize_deck(deck)

    if args.add_timestamps:
        now = utc_now()
        normalized.setdefault("created_at", now)
        normalized.setdefault("updated_at", now)

    if args.in_place:
        output = args.input
    elif args.output:
        output = args.output
    else:
        json.dump(normalized, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    write_json(output, normalized)

    print(f"Migrated {args.input} -> {output}")
    print(f"Old version: {old_version}")
    print("New version: 2")
    print("Timestamps added:", "yes" if args.add_timestamps else "no")

    return 0


if __name__ == "__main__":
    sys.exit(main())
