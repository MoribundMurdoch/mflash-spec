# Changelog

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