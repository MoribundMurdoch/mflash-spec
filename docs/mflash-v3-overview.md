# mflash v3 Overview

mflash v3 is a draft major version of the mflash study deck format.

It expands mflash from basic term-definition flashcards into typed study cards.

## Main ideas

```text
deck.json remains the source of truth
.mflash packages are ZIP archives
assets live under assets/
cards have kind
media objects are structured
languages remain first-class
pronunciation audio is supported
image occlusion is supported
Minimal deck
{
  "format": "mflash",
  "version": 3,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Example Deck",
  "cards": []
}
Package layout
deck.json
assets/
  deck/
  cards/
    <card_id>/
Card kinds
basic
image_occlusion
listening
media_prompt
