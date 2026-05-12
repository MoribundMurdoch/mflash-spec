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
