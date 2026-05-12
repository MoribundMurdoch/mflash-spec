#!/usr/bin/env python3
import argparse
import json
import re
import sys
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


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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


def collect_errors_and_warnings(deck: Dict[str, Any], base_dir: Path | None = None) -> tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    card_ids: Set[str] = set()

    cards = deck.get("cards", [])
    if not isinstance(cards, list):
        errors.append("cards must be an array.")
        return errors, warnings

    cover = deck.get("cover")
    if isinstance(cover, dict):
        validate_media_path(
            media=cover,
            owner="deck.cover",
            errors=errors,
            warnings=warnings,
            base_dir=base_dir,
            expected_prefix="assets/deck/",
            require_exists=base_dir is not None,
        )
        warn_unknown_media_role(cover, "deck.cover", warnings)

    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            errors.append(f"cards[{index}] must be an object.")
            continue

        card_id = card.get("id")
        if isinstance(card_id, str):
            if card_id in card_ids:
                errors.append(f"Duplicate card id: {card_id}")
            card_ids.add(card_id)
        else:
            errors.append(f"cards[{index}].id must be a string.")

        kind = card.get("kind")
        if isinstance(kind, str) and kind not in OFFICIAL_CARD_KINDS:
            warnings.append(f"cards[{index}] has unknown card kind: {kind}")

        for media in iter_card_media(card):
            media_src = media.get("src")
            owner = f"card {card_id or index} media"

            validate_media_path(
                media=media,
                owner=owner,
                errors=errors,
                warnings=warnings,
                base_dir=base_dir,
                expected_prefix=f"assets/cards/{card_id}/" if isinstance(card_id, str) else "assets/cards/",
                require_exists=base_dir is not None,
            )
            warn_unknown_media_role(media, owner, warnings)

        validate_masks(card, card_id or str(index), errors)

    return errors, warnings


def warn_unknown_media_role(media: Dict[str, Any], owner: str, warnings: List[str]) -> None:
    role = media.get("role")
    if isinstance(role, str) and role not in OFFICIAL_MEDIA_ROLES:
        warnings.append(f"{owner} has unknown media role: {role}")


def validate_media_path(
    media: Dict[str, Any],
    owner: str,
    errors: List[str],
    warnings: List[str],
    base_dir: Path | None,
    expected_prefix: str,
    require_exists: bool,
) -> None:
    src = media.get("src")

    if not isinstance(src, str) or not src:
        errors.append(f"{owner} has missing or invalid src.")
        return

    if is_absolute_or_unsafe_path(src):
        errors.append(f"{owner} has absolute or unsafe src path: {src}")
        return

    normalized = src.replace("\\", "/")

    if not normalized.startswith("assets/"):
        errors.append(f"{owner} src must stay inside assets/: {src}")

    if expected_prefix and not normalized.startswith(expected_prefix):
        warnings.append(f"{owner} src is outside recommended path {expected_prefix}: {src}")

    if require_exists and base_dir is not None:
        asset_path = base_dir / normalized
        if not asset_path.exists():
            errors.append(f"{owner} src does not exist: {src}")


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an mflash deck JSON file.")
    parser.add_argument("deck_json", help="Path to deck.json or .mflash.json")
    parser.add_argument("schema_json", help="Path to mflash JSON Schema")
    parser.add_argument(
        "--check-assets",
        action="store_true",
        help="Check that referenced asset files exist relative to the deck JSON directory.",
    )
    args = parser.parse_args()

    deck_path = Path(args.deck_json)
    schema_path = Path(args.schema_json)

    deck = load_json(deck_path)
    schema = load_json(schema_path)

    schema_errors = validate_schema(deck, schema)

    base_dir = deck_path.parent if args.check_assets else None
    logical_errors, warnings = collect_errors_and_warnings(deck, base_dir=base_dir)

    all_errors = schema_errors + logical_errors

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {deck_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

