# 0004: Separate Study Progress

## Status

Accepted

## Context

A deck file represents reusable learning content.

Study progress represents user/app-specific state.

These are different kinds of data.

Deck content includes terms, definitions, examples, media references, notes, tags, and language metadata.

Study progress includes review counts, due dates, ease factors, last-reviewed timestamps, lapses, scheduling state, and app-specific learning history.

If progress is stored inside deck files, decks mutate every time someone studies. That makes sharing, Git diffs, syncing, collaboration, and anonymous publishing worse.

## Decision

mflash deck files should not store study progress.

Study progress belongs in a separate `mflash-progress` format.

Progress files are keyed by:

- deck `id`
- card `id`

Recommended progress extension:

```text
.mflash.progress.json
Consequences

Deck files remain clean, reusable, and shareable.

Multiple users can study the same deck with different progress files.

Multiple apps can use different scheduling systems without changing the deck.

Git diffs for deck content stay focused on deck content.

Example

Deck file:

{
  "format": "mflash",
  "version": 2,
  "id": "deck_french_basics",
  "title": "French Basics",
  "cards": [
    {
      "id": "card_001",
      "term": "bonjour",
      "definition": "hello"
    }
  ]
}

Progress file:

{
  "format": "mflash-progress",
  "version": 1,
  "deck_id": "deck_french_basics",
  "cards": {
    "card_001": {
      "review_count": 3,
      "due_at": "2026-05-12T20:44:00Z"
    }
  }
}
Notes

The exact spaced-repetition algorithm is not standardized in mflash-progress v1.

Applications may add app-specific scheduling fields.
