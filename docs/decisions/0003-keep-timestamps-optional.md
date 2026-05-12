# 0003: Keep Timestamps Optional

## Status

Accepted

## Context

Timestamps such as `created_at` and `updated_at` are useful for local libraries, sorting, sync, backups, and app-managed workflows.

However, timestamps can leak metadata.

For anonymous deck sharing, users may not want to reveal when a deck was created, edited, exported, or maintained.

mflash should not force timestamp metadata into every shared deck.

## Decision

mflash v2 keeps `created_at` and `updated_at` optional.

Applications MAY add timestamps for local deck management.

Applications MUST NOT require timestamps to load or validate a deck.

Migration tools SHOULD NOT add timestamps unless explicitly requested.

Anonymous export tools SHOULD remove timestamps and other nonessential metadata when the user requests a privacy-preserving export.

## Consequences

A valid mflash v2 deck can omit timestamps entirely.

This makes anonymous sharing easier and avoids unnecessary metadata leakage.

Applications that want timestamps can still use them.

## Example

Valid anonymous/shareable deck:

```json
{
  "format": "mflash",
  "version": 2,
  "id": "deck_anonymous_french_basics",
  "title": "French Basics",
  "cards": [
    {
      "id": "card_001",
      "term": "bonjour",
      "definition": "hello"
    }
  ]
}
Notes

Deck and card IDs remain required because they are structural identifiers.

Timestamps are optional because they are descriptive metadata.
