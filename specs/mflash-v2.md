# mflash Deck Format v2

**Status:** Draft  
**Format version:** 2  
**Schema:** `schema/mflash-v2.schema.json`  
**Raw deck extension:** `.mflash.json`  
**Packaged deck extension:** `.mflash`

## Overview

mflash v2 is the current deck format for mflash-compatible tools.

A deck is reusable flashcard content. It contains terms, definitions, examples, media references, notes, tags, and language metadata.

Study progress is not stored in the deck file. Progress belongs in a separate `mflash-progress` file.

## Required deck fields

A valid mflash v2 deck MUST include:

```json
{
  "format": "mflash",
  "version": 2,
  "id": "deck_example",
  "title": "Example Deck",
  "cards": []
}
format

MUST be:

"mflash"
version

MUST be:

2
id

Stable deck identifier.

Deck IDs are used for progress files, syncing, app metadata, and external references.

Deck IDs SHOULD NOT contain personally identifying information such as usernames, email addresses, machine names, real names, or timestamps.

title

Human-readable deck title.

cards

Array of card objects.

Optional deck fields
description

Longer human-readable description.

snippet

Short preview text for deck libraries, search results, file pickers, and OS integrations.

created_at

Optional ISO 8601 timestamp for when the deck was created.

Applications MUST NOT require this field.

updated_at

Optional ISO 8601 timestamp for when the deck content was last meaningfully updated.

Applications MUST NOT require this field.

default_term_lang

Default language tag for card terms.

Language tags SHOULD follow BCP 47, such as:

en
fr
et
ja-JP
zh-Hans
default_def_lang

Default language tag for card definitions.

deck_tags

Array of deck-level tags.

If absent, readers SHOULD treat this as an empty array.

cover_media

Path or reference to a cover image or preview media item.

For packaged .mflash decks, this SHOULD be a relative package path.

Required card fields

Each card MUST include:

{
  "id": "card_001",
  "term": "bonjour",
  "definition": "hello"
}
id

Stable card identifier.

Card IDs are used for progress tracking, media references, syncing, review history, and app metadata.

Card IDs SHOULD NOT contain personally identifying information.

term

Prompt, front-side text, source-language item, or thing to remember.

definition

Answer, back-side text, target-language item, or explanation.

Optional card fields
term_lang

Language tag for the term.

If absent, readers SHOULD use default_term_lang when available.

def_lang

Language tag for the definition.

If absent, readers SHOULD use default_def_lang when available.

phonetic

Pronunciation, IPA, romanization, reading helper, or phonetic spelling.

part_of_speech

Grammatical category such as noun, verb, adjective, interjection, phrase, or idiom.

notes

Extra explanation, mnemonic, usage note, or warning.

hyperlink

Optional URL associated with the card.

tags

Array of card-level tags.

If absent, readers SHOULD treat this as an empty array.

examples

Examples MAY be strings or structured objects.

String example:

"examples": [
  "Bonjour, comment ça va ? → Hello, how are you?"
]

Structured example:

"examples": [
  {
    "text": "Bonjour, comment ça va ?",
    "translation": "Hello, how are you?",
    "lang": "fr",
    "translation_lang": "en"
  }
]
media

Media MAY be a string path or an array of structured media objects.

Legacy/simple media:

"media": "media/card_001.png"

Preferred structured media:

"media": [
  {
    "type": "image",
    "src": "media/card_001.png",
    "alt": "A greeting card illustration."
  }
]

Supported media types:

image
audio
video
gif
other
Unknown fields

Readers SHOULD ignore unknown fields.

Writers SHOULD preserve unknown fields when practical.

This allows forward compatibility and tool-specific metadata without breaking the core format.

Minimal valid v2 deck
{
  "format": "mflash",
  "version": 2,
  "id": "deck_minimal_v2",
  "title": "Minimal mflash v2 Deck",
  "cards": [
    {
      "id": "card_001",
      "term": "bonjour",
      "definition": "hello"
    }
  ]
}

