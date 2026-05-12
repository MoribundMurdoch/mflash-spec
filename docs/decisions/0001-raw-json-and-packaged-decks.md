# 0001: Raw JSON and Packaged Decks

## Status

Accepted

## Context

mflash needs to support two different workflows:

1. Developer/editable workflows where decks are easy to inspect, diff, generate, and modify.
2. User/shareable workflows where decks can bundle media and behave like portable files.

A single representation does not serve both cases equally well.

Raw JSON is excellent for editing, scripts, Git repositories, and debugging.

Packaged archives are better for normal app use, media bundling, importing, sharing, and future OS integrations such as thumbnails and MIME handling.

## Decision

mflash supports two related deck representations:

- `.mflash.json` — raw UTF-8 JSON deck file.
- `.mflash` — packaged archive containing a root-level `deck.json` and optional bundled assets.

Both representations use the same deck object after loading.

A packaged `.mflash` archive MUST contain a valid root-level `deck.json`.

## Consequences

Applications should normalize both `.mflash.json` and `.mflash` into the same in-memory deck model.

Study mode should not care whether the deck came from raw JSON, a packaged archive, or an importer.

Raw `.mflash.json` remains the preferred format for development, scripts, tests, generated decks, and Git.

Packaged `.mflash` remains the preferred format for sharing, importing, media bundling, and user-facing app workflows.

## Notes

This decision lets mflash be both human-editable and user-friendly without forcing one file representation to do every job badly.
