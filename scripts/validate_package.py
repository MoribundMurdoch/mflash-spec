#!/usr/bin/env python3
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

from jsonschema import Draft202012Validator, FormatChecker


OFFICIAL_CARD_KINDS = {
    "basic",
    "image_occlusion",
    "listening",
    "media_prompt",
}

OFFICIAL_MEDIA_ROLES = {
    "cover",
    "illustration",
    "prompt_image",
    "answer_image",
    "prompt_video",
    "answer_video",
    "prompt_animation",
    "answer_animation",
    "term_pronunciation",
    "definition_pronunciation",
    "question_audio",
    "answer_audio",
    "example_audio",
    "explanation_audio",
    "occlusion_image",
    "source_document",
    "supplement",
}


def is_absolute_or_unsafe_path(src: str) -> bool:
    if src.startswith("/") or src.startswith("\\"):
        return True

    if re.match(r"^[A-Za-z]:[\\/]", src):
        return True

    parts = src.replace("\\", "/").split("/")
    return ".." in parts


def iter_card_media(card: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    media = card.get("media", [])
    if isinstance(media, list):
        for item in media:
            if isinstance(item, dict):
                yield item

    occlusion = card.get("occlusion")
    if isinstance(occlusion, dict):
        image = occlusion.get("image")
        if isinstance(image, dict):
            yield image

    examples = card.get("examples", [])
    if isinstance(examples, list):
        for example in examples:
            if not isinstance(example, dict):
                continue
            example_media = example.get("media", [])
            if isinstance(example_media, list):
                for item in example_media:
                    if isinstance(item, dict):
                        yield item


def validate_schema(deck: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(deck), key=lambda e: list(e.path))

    messages = []
    for error in errors:
        path = ".".join(str(part) for part in error.path)
        if path:
            messages.append(f"{path}: {error.message}")
        else:
            messages.append(error.message)

    return messages


def validate_media_path(
    media: Dict[str, Any],
    owner: str,
    archive_names: Set[str],
    errors: List[str],
    warnings: List[str],
    expected_prefix: str,
) -> None:
    src = media.get("src")

    if not isinstance(src, str) or not src:
        errors.append(f"{owner} has missing or invalid src.")
        return

    normalized = src.replace("\\", "/")

    if is_absolute_or_unsafe_path(src):
        errors.append(f"{owner} has absolute or unsafe src path: {src}")
        return

    if not normalized.startswith("assets/"):
        errors.append(f"{owner} src must stay inside assets/: {src}")

    if expected_prefix and not normalized.startswith(expected_prefix):
        warnings.append(f"{owner} src is outside recommended path {expected_prefix}: {src}")

    if normalized not in archive_names:
        errors.append(f"{owner} src missing from package: {src}")


def warn_unknown_media_role(media: Dict[str, Any], owner: str, warnings: List[str]) -> None:
    role = media.get("role")
    if isinstance(role, str) and role not in OFFICIAL_MEDIA_ROLES:
        warnings.append(f"{owner} has unknown media role: {role}")


def validate_masks(card: Dict[str, Any], card_id: str, errors: List[str]) -> None:
    occlusion = card.get("occlusion")
    if not isinstance(occlusion, dict):
        return

    masks = occlusion.get("masks", [])
    if not isinstance(masks, list):
        errors.append(f"card {card_id} occlusion.masks must be an array.")
        return

    seen: Set[str] = set()

    for index, mask in enumerate(masks):
        if not isinstance(mask, dict):
            errors.append(f"card {card_id} mask[{index}] must be an object.")
            continue

        mask_id = mask.get("id")
        if not isinstance(mask_id, str):
            errors.append(f"card {card_id} mask[{index}].id must be a string.")
            continue

        if mask_id in seen:
            errors.append(f"card {card_id} has duplicate mask id: {mask_id}")

        seen.add(mask_id)


def validate_deck_logic(deck: Dict[str, Any], archive_names: Set[str]) -> tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    cover = deck.get("cover")
    if isinstance(cover, dict):
        validate_media_path(
            media=cover,
            owner="deck.cover",
            archive_names=archive_names,
            errors=errors,
            warnings=warnings,
            expected_prefix="assets/deck/",
        )
        warn_unknown_media_role(cover, "deck.cover", warnings)

    card_ids: Set[str] = set()
    cards = deck.get("cards", [])

    if not isinstance(cards, list):
        errors.append("cards must be an array.")
        return errors, warnings

    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            errors.append(f"cards[{index}] must be an object.")
            continue

        card_id = card.get("id")
        if not isinstance(card_id, str):
            errors.append(f"cards[{index}].id must be a string.")
            continue

        if card_id in card_ids:
            errors.append(f"Duplicate card id: {card_id}")
        card_ids.add(card_id)

        kind = card.get("kind")
        if isinstance(kind, str) and kind not in OFFICIAL_CARD_KINDS:
            warnings.append(f"card {card_id} has unknown card kind: {kind}")

        for media in iter_card_media(card):
            owner = f"card {card_id} media"
            validate_media_path(
                media=media,
                owner=owner,
                archive_names=archive_names,
                errors=errors,
                warnings=warnings,
                expected_prefix=f"assets/cards/{card_id}/",
            )
            warn_unknown_media_role(media, owner, warnings)

        validate_masks(card, card_id, errors)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a packaged .mflash file.")
    parser.add_argument("package", help="Path to .mflash ZIP package")
    parser.add_argument(
        "--schema",
        default="schema/mflash-v3-schema.json",
        help="Path to mflash v3 schema. Default: schema/mflash-v3-schema.json",
    )
    args = parser.parse_args()

    package_path = Path(args.package)
    schema_path = Path(args.schema)

    if not package_path.exists():
        print(f"ERROR: package does not exist: {package_path}", file=sys.stderr)
        return 1

    if not schema_path.exists():
        print(f"ERROR: schema does not exist: {schema_path}", file=sys.stderr)
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    errors: List[str] = []
    warnings: List[str] = []

    try:
        with zipfile.ZipFile(package_path, "r") as archive:
            archive_names = set(archive.namelist())

            if "deck.json" not in archive_names:
                errors.append("deck.json is required at package root.")
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1

            with archive.open("deck.json") as f:
                deck = json.loads(f.read().decode("utf-8"))

            errors.extend(validate_schema(deck, schema))

            logical_errors, logical_warnings = validate_deck_logic(deck, archive_names)
            errors.extend(logical_errors)
            warnings.extend(logical_warnings)

    except zipfile.BadZipFile:
        print(f"ERROR: not a valid ZIP/.mflash package: {package_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: deck.json is not valid JSON: {e}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {package_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
