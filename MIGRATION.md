# mflash Migration Guide

## v1 to v2

mflash v2 adds stable required IDs.

A v1 deck can be migrated to v2 by:

1. Set `"version": 2`.
2. Add a top-level deck `"id"` if missing.
3. Add an `"id"` to every card if missing.
4. Do not add `created_at` or `updated_at` unless explicitly requested.
5. Keep study progress outside the deck file.

## Reader behavior

Applications SHOULD load v1 and v2 decks.

When saving a migrated deck, applications SHOULD save as v2 by default.

## Writer behavior

Writers SHOULD produce v2 decks.

Writers SHOULD preserve unknown fields when practical.

---

## Migrating from mflash v2 to mflash v3

mflash v3 is a major format update.

The biggest change is that mflash is no longer limited to term-definition flashcards. In v3, every card has a `kind`, and different card kinds may require different fields.

Basic term-definition cards are still supported as:

```json
{
  "kind": "basic"
}
v2 to v3 migration checklist
[x] v2 version: 2 becomes v3 version: 3.

[x] v2 cover_media becomes v3 cover object.

[x] v2 card with no kind becomes kind: basic.

[x] v2 term/definition cards remain valid as basic cards.

[x] v2 card media string becomes media array.

[x] v2 media paths move toward assets/cards/<card_id>/.

[x] v2 deck cover moves toward assets/deck/.

[x] v2 default_term_lang/default_def_lang remain unchanged.

[x] v2 term_lang/def_lang remain unchanged.

Version
v2:

JSON
{
  "format": "mflash",
  "version": 2
}
v3:

JSON
{
  "format": "mflash",
  "version": 3
}
During migration:

version: 2 -> version: 3

The format field remains: "format": "mflash"

IDs
mflash v3 uses UUID-formatted IDs for stable syncing across devices.

If a v2 deck or card already uses UUIDs, migration tools should preserve them.

If a v2 deck or card uses a non-UUID ID, migration tools should convert it to a UUID.

Recommended behavior:

existing UUID -> preserve

non-UUID string -> deterministic UUIDv5 generated from old ID

missing ID -> new UUIDv4

Example v2 ID:

JSON
"id": "card_001"
Possible v3 migrated ID:

JSON
"id": "550e8400-e29b-41d4-a716-446655440001"
Applications may keep a legacy ID in an extension field if needed:

JSON
"extensions": {
  "mflash.migration": {
    "legacy_id": "card_001"
  }
}
Deck cover
mflash v2 used cover_media as a string:

JSON
{
  "cover_media": "media/cover.png"
}
mflash v3 uses a structured cover media object:

JSON
{
  "cover": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "type": "image",
    "role": "cover",
    "src": "assets/deck/cover.png",
    "alt": "Deck cover image"
  }
}
During migration:

cover_media -> cover.src

cover.type -> image, gif, or other based on file extension

cover.role -> cover

Deck cover assets should move toward: assets/deck/
Recommended path: assets/deck/cover.png

Cards
In mflash v2, cards were assumed to be term-definition cards.

v2 card:

JSON
{
  "id": "card_001",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}
In mflash v3, this becomes a basic card:

JSON
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}
Migration rule: card.kind missing -> kind: basic

Fields that should be preserved when present:

term

definition

term_lang

def_lang

phonetic

part_of_speech

notes

hyperlink

tags

examples

media

Term and definition
mflash v2 required every card to have:

term

definition

mflash v3 does not require term and definition globally, but kind: "basic" cards still require them. So ordinary v2 cards remain valid as v3 basic cards after adding: "kind": "basic"

Language fields
Existing polyglot language fields remain supported.

Deck-level defaults remain unchanged:

JSON
{
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US"
}
Card-level overrides remain unchanged:

JSON
{
  "term_lang": "de-DE",
  "def_lang": "en-US"
}
Migration rules:

default_term_lang -> default_term_lang

default_def_lang -> default_def_lang

term_lang -> term_lang

def_lang -> def_lang

No language migration is required unless an application wants to normalize language names into BCP 47 tags.

Media
mflash v2 allowed looser media shapes.

Possible v2 media string:

JSON
{
  "media": "image.png"
}
Possible v2 media object:

JSON
{
  "media": {
    "type": "image",
    "path": "image.png",
    "alt": "An image"
  }
}
mflash v3 card media is always an array of structured media objects:

JSON
{
  "media": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440011",
      "type": "image",
      "role": "illustration",
      "src": "assets/cards/550e8400-e29b-41d4-a716-446655440001/image.png",
      "alt": "An image"
    }
  ]
}
Migration rules:

media string -> media array with one media object

media object -> media array with one media object

media array -> media array

path -> src

missing role -> inferred role

missing id -> generated UUID

Recommended role inference:

image -> illustration

gif -> illustration or prompt_animation

audio -> supplement unless clearly pronunciation

video -> prompt_video

document -> source_document

other -> supplement

Asset paths
mflash v3 packaged decks should use:

Plaintext
deck.json
assets/
  deck/
  cards/
    <card_id>/
Deck covers should move toward: assets/deck/

Card media should move toward: assets/cards/<card_id>/

Example path migration:

media/cover.png -> assets/deck/cover.png

media/lative.mp3 -> assets/cards/<card_id>/lative.mp3

image.png -> assets/cards/<card_id>/image.png

Applications may temporarily preserve old paths while converting JSON, but packaged v3 exports should ingest assets and rewrite paths to the v3 layout.

Examples
Minimal v2 deck

JSON
{
  "format": "mflash",
  "version": 2,
  "id": "deck_001",
  "title": "Example Deck",
  "cover_media": "media/cover.png",
  "cards": [
    {
      "id": "card_001",
      "term": "Lative",
      "definition": "Indicating motion up to or as far as."
    }
  ]
}
Migrated v3 deck

JSON
{
  "format": "mflash",
  "version": 3,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Example Deck",
  "cover": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "type": "image",
    "role": "cover",
    "src": "assets/deck/cover.png",
    "alt": "Deck cover image"
  },
  "cards": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "kind": "basic",
      "term": "Lative",
      "definition": "Indicating motion up to or as far as."
    }
  ]
}
Migration script
A migration script is provided at: scripts/migrate_v2_to_v3.py

Usage:

Bash
python scripts/migrate_v2_to_v3.py old-deck.json new-deck.json
The migration script should:

Read a v2 deck JSON file.

Set format to mflash.

Set version to 3.

Convert deck/card/media IDs to UUIDs.

Convert cover_media to cover.

Add kind: basic to v2 cards.

Convert media strings or objects into media arrays.

Preserve language fields.

Preserve unknown extra fields when practical.

Write a v3 deck JSON file.

Compatibility notes
mflash v3 readers should not assume all cards have term and definition.

mflash v2 readers may not understand v3 cards.

Applications that support both versions should parse by version:

version: 2 -> parse as mflash v2

version: 3 -> parse as mflash v3

Applications may offer an explicit migration/export command rather than silently rewriting v2 decks.