#!/usr/bin/env python3

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema")
    print("Install it with:")
    print("  python -m pip install jsonschema")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_V1 = ROOT / "schema" / "mflash-v1.schema.json"
SCHEMA_V2 = ROOT / "schema" / "mflash-v2.schema.json"
SCHEMA_PROGRESS = ROOT / "schema" / "mflash-progress-v1.schema.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(path: Path, schema: dict) -> None:
    data = load_json(path)
    jsonschema.Draft202012Validator(schema).validate(data)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    failed = False

    schema_v1 = load_json(SCHEMA_V1)
    schema_v2 = load_json(SCHEMA_V2)
    schema_progress = load_json(SCHEMA_PROGRESS)

    print("Checking schemas are valid JSON Schemas...")
    for schema_path in sorted((ROOT / "schema").glob("*.json")):
        try:
            schema_data = load_json(schema_path)
            jsonschema.Draft202012Validator.check_schema(schema_data)
            print(f"OK   {rel(schema_path)}")
        except Exception as e:
            failed = True
            print(f"FAIL {rel(schema_path)}: {e}")

    print()
    print("Checking valid deck examples...")

    valid_deck_examples = [
        ROOT / "examples" / "minimal-v1.mflash.json",
        ROOT / "examples" / "minimal-v2.mflash.json",
        ROOT / "examples" / "anonymous-share-v2.mflash.json",
        ROOT / "examples" / "maximal-v2.mflash.json",
        ROOT / "examples" / "multilingual-v2.mflash.json"
    ]

    for path in valid_deck_examples:
        try:
            data = load_json(path)
            version = data.get("version")

            if version == 1:
                jsonschema.Draft202012Validator(schema_v1).validate(data)
            elif version == 2:
                jsonschema.Draft202012Validator(schema_v2).validate(data)
            else:
                raise ValueError(f"Unsupported mflash version in valid example: {version}")

            print(f"OK   {rel(path)}")
        except Exception as e:
            failed = True
            print(f"FAIL {rel(path)}: {e}")

    print()
    print("Checking progress examples...")

    progress_examples = sorted((ROOT / "examples" / "progress").glob("*.json"))

    for path in progress_examples:
        try:
            validate_file(path, schema_progress)
            print(f"OK   {rel(path)}")
        except Exception as e:
            failed = True
            print(f"FAIL {rel(path)}: {e}")

    print()
    print("Checking invalid examples fail as expected...")

    invalid_examples = sorted((ROOT / "examples" / "invalid").glob("*.json"))

    for path in invalid_examples:
        try:
            validate_file(path, schema_v2)
            failed = True
            print(f"FAIL {rel(path)}: unexpectedly passed validation")
        except Exception:
            print(f"OK   {rel(path)} failed validation as expected")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
