# mflash Privacy Notes

mflash v2 treats privacy as part of the file format design.

## Optional timestamps

`created_at` and `updated_at` are optional.

Applications MAY add them for local sorting, sync, backup, or library management, but they MUST NOT require them for loading or validating a deck.

Anonymous export tools SHOULD remove timestamps unless the user explicitly chooses to keep them.

## Structural IDs

Deck IDs and card IDs are structural identifiers.

They SHOULD NOT contain:

- usernames
- email addresses
- machine names
- real names
- timestamps
- private project names

Good IDs are boring, stable, and non-identifying.

## Study progress

Study progress SHOULD be stored outside the deck file.

Deck files are shareable learning content. Progress files are user/app-specific state.
