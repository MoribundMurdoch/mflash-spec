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

## Card kind

A card kind describes how a card should be interpreted, edited, and studied.

Examples:

```text
basic
image_occlusion
listening
media_prompt

In mflash v3, every card requires a kind.

Basic card

A traditional term-definition flashcard.

Example:

{
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}
Media object

A structured object describing an attached file.

Example:

{
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/image.png"
}

The type describes what the file is.

The role describes what the file is for.

Media role

The purpose of a media object.

Examples:

cover
illustration
term_pronunciation
definition_pronunciation
question_audio
occlusion_image
Asset path

A path to a file inside a packaged .mflash archive.

In mflash v3, packaged asset paths should be relative to the package root.

Examples:

assets/deck/cover.png
assets/cards/<card_id>/pronunciation.mp3
Deck asset

An asset that belongs to the deck as a whole.

Deck assets live under:

assets/deck/

Example:

assets/deck/cover.png
Card asset

An asset that belongs to an individual card.

Card assets live under:

assets/cards/<card_id>/

Example:

assets/cards/<card_id>/illustration.png
Image occlusion

A study card type that hides one or more regions of an image and asks the learner to identify the hidden content.

Used for anatomy, maps, diagrams, art history, machinery, biology, and visual memorization.

Occlusion mask

A shape used to hide part of an image in an image occlusion card.

Supported mask shapes:

rect
ellipse
polygon

Masks use normalized coordinates from 0.0 to 1.0.

Normalized coordinates

Coordinates expressed relative to an image’s dimensions instead of absolute pixels.

Example:

{
  "x": 0.42,
  "y": 0.31,
  "w": 0.18,
  "h": 0.08
}

This allows masks to work even when images are resized.

Lexical metadata

Structured linguistic information attached to a card.

Examples:

etymology
morphology
ipa
romanization
register
usage_note
related_terms
Extension object

A namespaced object for plugin, experimental, or application-specific metadata.

Example:

"extensions": {
  "mflash-studio-rs": {
    "collapsed_sections": ["media"]
  }
}

Extensions should not override the meaning of official mflash fields.
