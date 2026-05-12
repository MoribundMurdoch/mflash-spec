# 0002: Require Stable IDs

## Status

Accepted

## Context

mflash v1 allowed cards without IDs.

That made simple decks easy, but it also meant applications had to rely on array position or card text to track identity.

Array position is unstable. Cards can be reordered, inserted, deleted, duplicated, imported, or merged.

Without stable IDs, features like study progress, sync, undo/redo, media references, review history, and card-level metadata become fragile.

## Decision

mflash v2 requires:

- a top-level deck `id`
- a card-level `id` for every card

Deck IDs identify decks across files, libraries, progress files, and sync systems.

Card IDs identify cards within decks.

## Consequences

mflash v2 decks are slightly more verbose than v1 decks.

In exchange, applications get stable references for progress, media, syncing, migration, and editing.

v1 decks can still be loaded by v2-aware tools, but missing IDs should be generated during normalization or migration.

When a v1 deck is saved by a v2-aware writer, it should be saved as v2 with required IDs.

## Privacy

IDs should be structural, not personal.

IDs SHOULD NOT contain:

- usernames
- email addresses
- real names
- machine names
- timestamps
- private project names

Good IDs are boring, stable, and non-identifying.

## Notes

A card ID should remain stable when a card is edited.

A duplicated card should receive a new ID.

A deleted card ID should not be reused within the same deck.
