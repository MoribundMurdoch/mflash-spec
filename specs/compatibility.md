# mflash Compatibility Rules

## Overview

mflash tools should be tolerant readers and careful writers.

The goal is to let old decks keep loading while new tools write cleaner v2 decks.

## Version support

Readers SHOULD support:

```text
mflash v1
mflash v2

Writers SHOULD save new or migrated decks as:

mflash v2
v1 behavior

mflash v1 decks may not contain:

deck id
card id

A v2-aware reader SHOULD still load v1 decks.

When normalizing a v1 deck, an application SHOULD generate missing IDs in memory.

When saving a migrated v1 deck, an application SHOULD save it as v2.

v2 behavior

mflash v2 requires:

top-level id
card-level id

Applications SHOULD reject v2 decks that are missing required IDs.

Optional timestamps

created_at and updated_at are optional.

Readers MUST NOT require them.

Writers MAY add them for local deck management, but SHOULD provide a way to omit or strip them for anonymous sharing.

Migration tools SHOULD NOT add timestamps unless explicitly requested.

Unknown fields

Readers SHOULD ignore unknown fields.

Writers SHOULD preserve unknown fields when practical.

This supports future versions, plugins, and third-party tools.

Media compatibility

Readers MAY support legacy string media values:

"media": "media/card_001.png"

Readers SHOULD support structured media arrays:

"media": [
  {
    "type": "image",
    "src": "media/card_001.png"
  }
]

Writers SHOULD prefer structured media arrays for new decks.

Example compatibility flow
Open v1 deck
  -> parse JSON
  -> generate missing deck ID in memory
  -> generate missing card IDs in memory
  -> normalize to current app model
  -> save as mflash v2 when written
Open v2 deck
  -> parse JSON
  -> verify deck ID exists
  -> verify card IDs exist
  -> normalize to current app model
Application guidance

Study apps SHOULD not care whether a deck came from:

.mflash.json
packaged .mflash
CSV importer
TSV importer
Anki importer

Importers should convert input into a normalized mflash-compatible deck object before study mode receives it.
