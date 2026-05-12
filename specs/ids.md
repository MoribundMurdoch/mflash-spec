# mflash ID Guidelines

## Overview

mflash v2 requires stable IDs for decks and cards.

IDs make it possible to track progress, sync edits, reference media, preserve review history, and migrate decks without relying on array position.

Array position is not a stable identity.

## Required IDs in mflash v2

Decks MUST include:

```json
"id": "deck_example"

Cards MUST include:

"id": "card_001"
Deck IDs

Deck IDs identify a deck across files, app libraries, progress files, and sync systems.

Good deck IDs:

deck_french_basics
deck_bad_hair_ahaha
deck_01hx_example

Bad deck IDs:

john-smith-french-deck
moribundmurdoch-laptop-2026-05-11
my-email@example.com

Deck IDs SHOULD NOT contain personally identifying information.

Card IDs

Card IDs identify a card within a deck.

Good card IDs:

card_001
card_bonjour
card_01hx9s7a

Card IDs MUST be stable once created.

If a card is edited, keep the same ID.

If a card is duplicated, the duplicate needs a new ID.

If a card is deleted, its ID SHOULD NOT be reused in the same deck.

Progress IDs

Progress files use deck IDs and card IDs to connect study state to deck content.

Example:

{
  "deck_id": "deck_french_basics",
  "cards": {
    "card_001": {
      "review_count": 3
    }
  }
}
Generated IDs

Applications MAY generate IDs automatically.

Generated IDs SHOULD be:

stable after creation
unique within the relevant deck
privacy-safe
free of usernames, emails, machine names, and timestamps
Anonymous export

Anonymous export tools MAY regenerate deck IDs and card IDs.

If card IDs are regenerated, associated progress files may no longer match unless they are migrated too.

Anonymous export tools SHOULD remove optional timestamps and other nonessential metadata when requested.

ID format

The schema only requires IDs to be non-empty strings.

Recommended characters:

A-Z
a-z
0-9
_
-

Recommended style:

deck_example
card_001
media_001

Avoid spaces when possible.
