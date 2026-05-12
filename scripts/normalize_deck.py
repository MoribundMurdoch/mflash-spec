#!/usr/bin/env python3

"""
Normalize an mflash deck to mflash v2 shape.

This script:
- sets format to "mflash"
- sets version to 2
- adds a deck id if missing
- adds card ids if missing
- does NOT add created_at or updated_at

Usage:
  python scripts/normalize_deck.py input.mflash.json
  python scripts/normalize_deck.py input.mflash.json -o output.mflash.json
  python scripts/normalize_deck.py input.mflash.json --in-place
"""

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or fallback


def unique_id(base: str, used: set[str]) -> str:
    candidate = base
    counter = 2

    while candidate in used:
        candidate = f"{base}_{counter}"
        counter += 1

    used.add(candidate)
    return candidate


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def normalize_deck(deck: dict) -> dict:
    if not isinstance(deck, dict):
        raise ValueError("Deck must be a JSON object.")

    deck["format"] = "mflash"
    deck["version"] = 2

    title = str(deck.get("title") or "untitled_deck")
    if not deck.get("id"):
        deck["id"] = f"deck_{slugify(title, 'untitled_deck')}"

    cards = deck.get("cards")

    if cards is None:
        deck["cards"] = []
        cards = deck["cards"]

    if not isinstance(cards, list):
        raise ValueError("Deck field 'cards' must be an array.")

    used_card_ids = {
        str(card.get("id"))
        for card in cards
        if isinstance(card, dict) and card.get("id")
    }

    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            raise ValueError(f"Card at index {index - 1} must be an object.")

        if not card.get("id"):
            term = str(card.get("term") or f"card_{index:03d}")
            base = f"card_{slugify(term, f'{index:03d}')}"
            card["id"] = unique_id(base, used_card_ids)

    return deck


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        print("Use either --output or --in-place, not both.", file=sys.stderr)
        return 2

    deck = load_json(args.input)
    normalized = normalize_deck(deck)

    if args.in_place:
        output = args.input
    elif args.output:
        output = args.output
    else:
        json.dump(normalized, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    write_json(output, normalized)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
