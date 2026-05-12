# Glossary

## mflash

The flashcard deck format used by Moribund Flash and related tools.

## Deck

A collection of flashcards and deck-level metadata.

## Card

A single flashcard containing at minimum an `id`, `term`, and `definition` in mflash v2.

## Term

The prompt, front-side text, or source-language item.

## Definition

The answer, back-side text, explanation, or target-language item.

## Raw deck

A UTF-8 JSON deck file using the `.mflash.json` extension.

## Packaged deck

A portable `.mflash` archive containing `deck.json` and optional bundled media assets.

## Progress file

A separate file containing user/app-specific study progress, keyed by deck ID and card ID.

## Stable ID

An identifier that remains stable across edits so apps can track cards, progress, media, and sync state.
