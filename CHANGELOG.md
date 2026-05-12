# Changelog
## mflash v3 - Draft

### Breaking changes

- Introduces `version: 3`.
- Deck and card IDs now use UUID format.
- Cards now require a `kind` field.
- `term` and `definition` are no longer globally required for every card.
- Basic term-definition cards are represented with `kind: "basic"`.
- `cover_media` is replaced or superseded by a structured `cover` object.
- Card `media` is now always an array of structured media objects.
- Bare media strings are deprecated for v3-authored decks.
- Packaged assets should live under `assets/`.
- Deck-level assets should live under `assets/deck/`.
- Card-level assets should live under `assets/cards/<card_id>/`.

### Added

- `schema/mflash-v3-schema.json`.
- Typed card kinds:
  - `basic`
  - `image_occlusion`
  - `listening`
  - `media_prompt`
- Structured media objects with:
  - `id`
  - `type`
  - `role`
  - `src`
  - `alt`
  - `description`
  - `lang`
- Structured deck cover metadata.
- Pronunciation audio roles:
  - `term_pronunciation`
  - `definition_pronunciation`
  - `example_audio`
  - `question_audio`
- Image occlusion support.
- Normalized occlusion mask coordinates.
- Rect, ellipse, and polygon mask definitions.
- Lexical metadata object for etymology and morphology.
- Namespaced `extensions` object for plugins and experimental metadata.
- v2-to-v3 migration script.

### Compatibility

- mflash v2 schema and documentation remain available.
- v2 cards may be migrated to v3 as `kind: "basic"`.
- Existing deck language defaults remain supported.
- Existing card language overrides remain supported.
- Unknown extra fields may be preserved for forward compatibility.

## mflash v3 - Draft

### Breaking changes

- Introduces `version: 3`.
- Cards now use a required `kind` field.
- `term` and `definition` are no longer globally required for every card.
- Basic term-definition cards are now represented as `kind: "basic"`.
- Deck cover metadata is moving from `cover_media` toward a structured `cover` object.
- Media objects are standardized for deck covers, card images, pronunciation audio, videos, gifs, and occlusion images.
- Packaged `.mflash` assets should now live under `assets/`.
- Deck-level assets should live under `assets/deck/`.
- Card-level assets should live under `assets/cards/<card_id>/`.

### Compatibility

- mflash v2 schemas and documentation remain available.
- v2 cards can be migrated to v3 as `kind: "basic"`.
- Polyglot deck defaults and card-level language overrides remain supported.

## mflash v2 draft

- Require top-level deck `id`.
- Require card `id`.
- Keep `created_at` and `updated_at` optional for privacy and anonymous sharing.
- Define separate `mflash-progress` format for study progress.
- Preserve v1 as legacy/migration format.

## mflash v1

- Initial raw `.mflash.json` and packaged `.mflash` deck format.
- Basic multilingual card metadata.
- Optional media, examples, notes, tags, and hyperlinks.