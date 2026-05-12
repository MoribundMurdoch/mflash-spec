# mflash v3 Specification

## Status

Draft.

mflash v3 is a JSON-first study deck format designed for typed study cards, organized packaged assets, polyglot learning, uploaded pronunciation audio, and image occlusion.

mflash v3 replaces the assumption that every card must be a term-definition flashcard. Basic term-definition cards remain supported, but they are now one card kind among several possible study card kinds.

---

## 1. Core Design Rules

### 1.1 JSON-first format

mflash v3 decks are JSON-first.

The canonical deck data is stored in a `deck.json` file. Applications may expose visual editors, raw JSON editors, importers, exporters, or package tools, but the source of truth for a deck is the JSON deck object.

A raw unpackaged deck may exist as:

```text
example.mflash.json

A packaged deck must contain:

deck.json

at the archive root.

1.2 Packaged .mflash files are ZIP archives

A packaged .mflash file is a ZIP archive with a required deck.json file at the archive root.

Required packaged layout:

deck.json

Recommended packaged layout:

deck.json
assets/
  deck/
  cards/

Applications should treat .mflash as a package, not as a single flat JSON file.

1.3 deck.json must live at the archive root

In packaged .mflash archives, deck.json must be located at the root of the ZIP archive.

Valid:

deck.json
assets/deck/cover.png
assets/cards/card_001/image.png

Invalid:

data/deck.json
mflash/deck.json
assets/deck.json
1.4 Assets live under assets/

All packaged media and supporting files should live under the assets/ directory.

Recommended:

assets/deck/
assets/cards/

Applications should write new packaged assets into assets/.

Applications may preserve older or unknown files elsewhere in the package for compatibility, but v3-authored packages should use assets/.

1.5 Deck assets and card assets are separated

Deck-level assets belong under:

assets/deck/

Card-level assets belong under:

assets/cards/<card_id>/

Example:

deck.json
assets/
  deck/
    cover.png
  cards/
    card_001/
      pronunciation.mp3
      illustration.png
    card_002/
      heart-diagram.png

Deck-level assets are used to represent the deck as a whole, such as cover images or deck branding.

Card-level assets are used as study material for individual cards, such as illustrations, pronunciation audio, diagrams, videos, or occlusion images.

1.6 Cards have a kind

Every v3 card must declare a kind.

Example:

{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}

The kind field tells applications how to interpret and present the card.

Initial official card kinds:

basic
image_occlusion
listening
media_prompt

Applications may support additional card kinds, but unknown kinds should not automatically make the entire deck invalid. Applications that cannot render a card kind should preserve the card data and show a useful fallback message.

1.7 term and definition are not globally required

In mflash v3, term and definition are no longer required on every card.

They remain normal fields for kind: "basic" cards, but other card kinds may use fields such as prompt, answer, media, or occlusion.

Valid basic card:

{
  "id": "card_001",
  "kind": "basic",
  "term": "Clavicle",
  "definition": "The collarbone."
}

Valid image occlusion card:

{
  "id": "card_002",
  "kind": "image_occlusion",
  "prompt": "Identify the hidden structure.",
  "occlusion": {
    "image": {
      "type": "image",
      "role": "occlusion_image",
      "src": "assets/cards/card_002/heart.png"
    },
    "masks": []
  }
}
1.8 Each card kind defines its own required fields

All cards require:

id
kind

Individual card kinds define additional requirements.

Recommended requirements:

basic:
  id
  kind
  term
  definition

image_occlusion:
  id
  kind
  occlusion

listening:
  id
  kind
  media
  answer

media_prompt:
  id
  kind
  media
  answer

Applications should validate card-kind-specific requirements when possible.

1.9 Media objects are structured and reusable

mflash v3 uses structured media objects instead of bare strings.

Recommended media object:

{
  "id": "media_001",
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/image.png",
  "alt": "A diagram",
  "description": "Optional longer description.",
  "lang": "en-US"
}

Required media fields:

type
src

Optional media fields:

id
role
alt
description
lang

Media objects may be used for:

deck covers
card illustrations
pronunciation audio
question audio
answer audio
videos
gifs
image occlusion base images
1.10 Polyglot language support remains

mflash v3 keeps deck-level language defaults and card-level language overrides.

Deck-level language defaults:

{
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US"
}

Card-level overrides:

{
  "id": "card_001",
  "kind": "basic",
  "term": "Weltanschauung",
  "definition": "worldview",
  "term_lang": "de-DE",
  "def_lang": "en-US"
}

Media-level language metadata:

{
  "id": "audio_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/weltanschauung.mp3",
  "lang": "de-DE"
}

Language fallback order:

media lang, when relevant
card term_lang or def_lang
deck default_term_lang or default_def_lang
application fallback

For term pronunciation, applications should use:

media.lang
card.term_lang
deck.default_term_lang
application fallback

For definition pronunciation, applications should use:

media.lang
card.def_lang
deck.default_def_lang
application fallback
1.11 Unknown extra fields may be preserved

mflash v3 allows forward-compatible extension.

Decks, cards, media objects, examples, and occlusion masks may contain unknown extra fields.

Applications should preserve unknown fields when reading and writing whenever practical.

Applications may ignore unknown fields they do not understand.

Unknown fields should not override the meaning of official fields.

2. Summary of v3 Design Rules
[x] mflash v3 decks are still JSON-first.
[x] Packaged .mflash files are ZIP archives.
[x] deck.json must live at the archive root.
[x] Assets live under assets/.
[x] Deck assets and card assets are separated.
[x] Cards have a kind/type.
[x] term and definition are not globally required anymore.
[x] Each card kind defines its own required fields.
[x] Media objects are structured and reusable.
[x] Polyglot deck/card/media language support remains.
[x] Unknown extra fields may be preserved for forward compatibility.
