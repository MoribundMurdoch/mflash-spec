# mflash Progress Format v1

**Status:** Draft  
**Format:** `mflash-progress`  
**Version:** 1  
**Schema:** `schema/mflash-progress-v1.schema.json`  
**Recommended extension:** `.mflash.progress.json`

## Overview

mflash progress files store user/app-specific study state separately from reusable deck content.

Deck files SHOULD remain shareable learning material.

Progress files MAY contain review counts, due dates, ease factors, and other scheduling metadata.

## Why progress is separate

Study progress is personal state. It should not be mixed into a deck that may be shared, copied, published, or edited collaboratively.

Separating progress from decks allows:

- anonymous deck sharing
- multiple users studying the same deck
- multiple apps using their own scheduling systems
- clean Git diffs for deck content
- safer syncing and backup workflows

## Required fields

A valid mflash progress file MUST include:

```json
{
  "format": "mflash-progress",
  "version": 1,
  "deck_id": "deck_example",
  "cards": {}
}
format

MUST be:

"mflash-progress"
version

MUST be:

1
deck_id

The ID of the deck this progress file belongs to.

This MUST match the deck-level id in an mflash v2 deck.

cards

Object keyed by card ID.

Each key SHOULD match a card id from the deck.

Optional top-level fields
created_at

Optional ISO 8601 timestamp for when this progress file was created.

updated_at

Optional ISO 8601 timestamp for when this progress file was last updated.

Card progress fields

Each card progress object MAY include:

review_count

Number of times the card has been reviewed.

correct_count

Number of correct reviews.

incorrect_count

Number of incorrect reviews.

last_reviewed_at

ISO 8601 timestamp for the last review.

due_at

ISO 8601 timestamp for when the card is next due.

ease

Numeric ease factor or scheduling weight.

The exact spaced-repetition algorithm is not standardized in mflash progress v1.

Example
{
  "format": "mflash-progress",
  "version": 1,
  "deck_id": "deck_minimal_v2",
  "cards": {
    "card_001": {
      "review_count": 3,
      "correct_count": 2,
      "incorrect_count": 1,
      "last_reviewed_at": "2026-05-11T20:44:00Z",
      "due_at": "2026-05-12T20:44:00Z",
      "ease": 2.5
    }
  }
}
Reader behavior

Readers SHOULD tolerate missing card progress entries.

If a card has no progress entry, applications SHOULD treat it as new/unreviewed.

Readers SHOULD ignore progress entries for card IDs that no longer exist in the deck.

Writer behavior

Writers SHOULD preserve unknown fields when practical.

Applications MAY add app-specific scheduling metadata, but SHOULD avoid placing reusable deck content inside progress files.
