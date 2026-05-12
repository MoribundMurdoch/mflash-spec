#!/usr/bin/env python3
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


def stable_or_new_uuid(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        raw = value.strip()
        try:
            return str(uuid.UUID(raw))
        except ValueError:
            return str(uuid.uuid5(uuid.NAMESPACE_URL, f"mflash:{raw}"))

    return str(uuid.uuid4())


def guess_media_type(src: str) -> str:
    ext = Path(src).suffix.lower().lstrip(".")

    if ext in {"png", "jpg", "jpeg", "webp", "svg"}:
        return "image"
    if ext == "gif":
        return "gif"
    if ext in {"mp3", "wav", "ogg", "flac", "m4a"}:
        return "audio"
    if ext in {"mp4", "webm", "mov", "mkv"}:
        return "video"
    if ext in {"pdf", "txt", "md", "html"}:
        return "document"

    return "other"


def default_role_for_type(media_type: str) -> str:
    if media_type in {"image", "gif"}:
        return "illustration"
    if media_type == "audio":
        return "supplement"
    if media_type == "video":
        return "prompt_video"
    if media_type == "document":
        return "source_document"
    return "supplement"


def migrate_media_item(item: Any) -> Dict[str, Any]:
    if isinstance(item, str):
        src = item.strip()
        media_type = guess_media_type(src)
        return {
            "id": str(uuid.uuid4()),
            "type": media_type,
            "role": default_role_for_type(media_type),
            "src": src
        }

    if isinstance(item, dict):
        src = item.get("src") or item.get("path") or item.get("file") or ""
        media_type = item.get("type") or guess_media_type(src)

        migrated: Dict[str, Any] = {
            "id": stable_or_new_uuid(item.get("id")),
            "type": media_type,
            "src": src
        }

        migrated["role"] = item.get("role") or default_role_for_type(media_type)

        for key in ["alt", "description", "lang"]:
            if key in item and item[key] is not None:
                migrated[key] = item[key]

        known = {"id", "type", "role", "src", "path", "file", "alt", "description", "lang"}
        for key, value in item.items():
            if key not in known:
                migrated[key] = value

        return migrated

    return {
        "id": str(uuid.uuid4()),
        "type": "other",
        "role": "supplement",
        "src": "",
        "original_value": item
    }


def migrate_media(media: Any) -> List[Dict[str, Any]]:
    if media is None:
        return []

    if isinstance(media, list):
        return [migrate_media_item(item) for item in media]

    return [migrate_media_item(media)]


def migrate_examples(examples: Any) -> List[Any]:
    if not isinstance(examples, list):
        return []

    migrated = []

    for example in examples:
        if isinstance(example, str):
            migrated.append({
                "id": str(uuid.uuid4()),
                "text": example
            })
        elif isinstance(example, dict):
            new_example = dict(example)
            new_example["id"] = stable_or_new_uuid(new_example.get("id"))
            migrated.append(new_example)

    return migrated


def migrate_card(card: Dict[str, Any]) -> Dict[str, Any]:
    new_id = stable_or_new_uuid(card.get("id"))

    migrated: Dict[str, Any] = {
        "id": new_id,
        "kind": card.get("kind", "basic")
    }

    field_map = [
        "term",
        "definition",
        "prompt",
        "answer",
        "term_lang",
        "def_lang",
        "phonetic",
        "part_of_speech",
        "notes",
        "hyperlink"
    ]

    for key in field_map:
        if key in card and card[key] is not None:
            migrated[key] = card[key]

    migrated["media"] = migrate_media(card.get("media"))
    migrated["tags"] = card.get("tags", []) if isinstance(card.get("tags", []), list) else []
    migrated["examples"] = migrate_examples(card.get("examples", []))

    known = {
        "id",
        "kind",
        "term",
        "definition",
        "prompt",
        "answer",
        "term_lang",
        "def_lang",
        "phonetic",
        "part_of_speech",
        "notes",
        "hyperlink",
        "media",
        "tags",
        "examples"
    }

    for key, value in card.items():
        if key not in known:
            migrated[key] = value

    return migrated


def migrate_deck(v2: Dict[str, Any]) -> Dict[str, Any]:
    migrated: Dict[str, Any] = {
        "format": "mflash",
        "version": 3,
        "id": stable_or_new_uuid(v2.get("id")),
        "title": v2.get("title", "Untitled mflash Deck"),
        "cards": []
    }

    for key in [
        "description",
        "snippet",
        "created_at",
        "updated_at",
        "default_term_lang",
        "default_def_lang"
    ]:
        if key in v2 and v2[key] is not None:
            migrated[key] = v2[key]

    if isinstance(v2.get("deck_tags"), list):
        migrated["deck_tags"] = v2["deck_tags"]

    if isinstance(v2.get("cover"), dict):
        migrated["cover"] = migrate_media_item(v2["cover"])
        migrated["cover"]["role"] = "cover"
    elif isinstance(v2.get("cover_media"), str) and v2["cover_media"].strip():
        src = v2["cover_media"].strip()
        migrated["cover"] = {
            "id": str(uuid.uuid4()),
            "type": guess_media_type(src),
            "role": "cover",
            "src": src,
            "alt": "Deck cover image"
        }

    cards = v2.get("cards", [])
    if isinstance(cards, list):
        migrated["cards"] = [
            migrate_card(card)
            for card in cards
            if isinstance(card, dict)
        ]

    known = {
        "format",
        "version",
        "id",
        "title",
        "description",
        "snippet",
        "created_at",
        "updated_at",
        "default_term_lang",
        "default_def_lang",
        "deck_tags",
        "cover",
        "cover_media",
        "cards"
    }

    for key, value in v2.items():
        if key not in known:
            migrated[key] = value

    return migrated


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Migrate mflash v2 JSON to mflash v3 JSON.")
    parser.add_argument("input", help="Path to v2 deck.json or .mflash.json")
    parser.add_argument("output", help="Path to write v3 deck.json")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        v2 = json.load(f)

    v3 = migrate_deck(v2)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(v3, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
