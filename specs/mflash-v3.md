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

```

A packaged deck must contain:

```text
deck.json

```

at the archive root.

### 1.2 Packaged .mflash files are ZIP archives

A packaged .mflash file is a ZIP archive with a required `deck.json` file at the archive root.

Required packaged layout:

```text
deck.json

```

Recommended packaged layout:

```text
deck.json
assets/
  deck/
  cards/

```

Applications should treat .mflash as a package, not as a single flat JSON file.

### 1.3 deck.json must live at the archive root

In packaged .mflash archives, `deck.json` must be located at the root of the ZIP archive.

Valid:

```text
deck.json
assets/deck/cover.png
assets/cards/card_001/image.png

```

Invalid:

```text
data/deck.json
mflash/deck.json
assets/deck.json

```

### 1.4 Assets live under assets/

All packaged media and supporting files should live under the `assets/` directory.

Recommended:

```text
assets/deck/
assets/cards/

```

Applications should write new packaged assets into `assets/`.

Applications may preserve older or unknown files elsewhere in the package for compatibility, but v3-authored packages should use `assets/`.

### 1.5 Deck assets and card assets are separated

Deck-level assets belong under:

```text
assets/deck/

```

Card-level assets belong under:

```text
assets/cards/<card_id>/

```

Example:

```text
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

```

Deck-level assets are used to represent the deck as a whole, such as cover images or deck branding.

Card-level assets are used as study material for individual cards, such as illustrations, pronunciation audio, diagrams, videos, or occlusion images.

### 1.6 Cards have a kind

Every v3 card must declare a `kind`.

Example:

```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}

```

The `kind` field tells applications how to interpret and present the card.

Initial official card kinds:

* `basic`
* `image_occlusion`
* `listening`
* `media_prompt`

Applications may support additional card kinds, but unknown kinds should not automatically make the entire deck invalid. Applications that cannot render a card kind should preserve the card data and show a useful fallback message.

### 1.7 term and definition are not globally required

In mflash v3, `term` and `definition` are no longer required on every card.

They remain normal fields for `kind: "basic"` cards, but other card kinds may use fields such as `prompt`, `answer`, `media`, or `occlusion`.

Valid basic card:

```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Clavicle",
  "definition": "The collarbone."
}

```

Valid image occlusion card:

```json
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

```

### 1.8 Each card kind defines its own required fields

All cards require:

* `id`
* `kind`

Individual card kinds define additional requirements.

Recommended requirements:

**basic:**

* `id`
* `kind`
* `term`
* `definition`

**image_occlusion:**

* `id`
* `kind`
* `occlusion`

**listening:**

* `id`
* `kind`
* `media`
* `answer`

**media_prompt:**

* `id`
* `kind`
* `media`
* `answer`

Applications should validate card-kind-specific requirements when possible.

### 1.9 Media objects are structured and reusable

mflash v3 uses structured media objects instead of bare strings.

Recommended media object:

```json
{
  "id": "media_001",
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/image.png",
  "alt": "A diagram",
  "description": "Optional longer description.",
  "lang": "en-US"
}

```

Required media fields:

* `type`
* `src`

Optional media fields:

* `id`
* `role`
* `alt`
* `description`
* `lang`

Media objects may be used for:

* deck covers
* card illustrations
* pronunciation audio
* question audio
* answer audio
* videos
* gifs
* image occlusion base images

### 1.10 Polyglot language support remains

mflash v3 keeps deck-level language defaults and card-level language overrides.

Deck-level language defaults:

```json
{
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US"
}

```

Card-level overrides:

```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Weltanschauung",
  "definition": "worldview",
  "term_lang": "de-DE",
  "def_lang": "en-US"
}

```

Media-level language metadata:

```json
{
  "id": "audio_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/weltanschauung.mp3",
  "lang": "de-DE"
}

```

Language fallback order:

1. `media` lang, when relevant
2. card `term_lang` or `def_lang`
3. deck `default_term_lang` or `default_def_lang`
4. application fallback

For term pronunciation, applications should use:

1. `media.lang`
2. `card.term_lang`
3. `deck.default_term_lang`
4. application fallback

For definition pronunciation, applications should use:

1. `media.lang`
2. `card.def_lang`
3. `deck.default_def_lang`
4. application fallback

### 1.11 Unknown extra fields may be preserved

mflash v3 allows forward-compatible extension.

Decks, cards, media objects, examples, and occlusion masks may contain unknown extra fields.

Applications should preserve unknown fields when reading and writing whenever practical.

Applications may ignore unknown fields they do not understand.

Unknown fields should not override the meaning of official fields.

---

## 2. Versioning

### 2.1 Format identifier

Every mflash v3 deck must identify itself with:

```json
{
  "format": "mflash",
  "version": 3
}

```

The `format` field identifies the file as an mflash deck.
The `version` field identifies the deck schema version.

### 2.2 v3 is a new major format version

mflash v3 is a major version update.
It changes the card model from term-definition-only cards to typed study cards. In v3, cards have a `kind`, and `term` and `definition` are no longer globally required for every card.
This is a breaking change from mflash v2.

### 2.3 v2 compatibility

mflash v2 schemas, examples, and documentation should remain available for compatibility.
Applications may continue to read v2 decks.
Applications that support both v2 and v3 should detect the version field and parse accordingly:

* `version: 2` -> parse as mflash v2
* `version: 3` -> parse as mflash v3

If an older v2-style deck is migrated to v3, applications should normally treat v2 cards as:

```json
{
  "kind": "basic"
}

```

and preserve the existing `term` and `definition` fields.

### 2.4 Schema files

mflash v3 should use a new schema file rather than overwriting the v2 schema.
Recommended schema files:

* `schema/mflash-v2-schema.json`
* `schema/mflash-v3-schema.json`
* `schema/mflash-schema.json`

The version-specific schemas should remain stable references:

* `schema/mflash-v2-schema.json`
* `schema/mflash-v3-schema.json`

The generic schema file may point to the latest stable format version:

* `schema/mflash-schema.json`

Once v3 is stable, `schema/mflash-schema.json` may mirror or reference the v3 schema.

### 2.5 Changelog requirement

The changelog must document the breaking changes introduced in mflash v3.
Required changelog notes:

* mflash v3 uses `version: 3`.
* Cards now require `kind`.
* `term` and `definition` are no longer globally required on all cards.
* Basic term-definition cards remain supported as `kind: "basic"`.
* `cover_media` is replaced or superseded by structured cover metadata.
* Media objects are standardized.
* Packaged assets should live under `assets/`.
* Deck assets and card assets are separated.
* Polyglot deck/card/media language support remains.

---

## 3. Summary of v3 Design Rules

* [x] mflash v3 decks are still JSON-first.
* [x] Packaged .mflash files are ZIP archives.
* [x] deck.json must live at the archive root.
* [x] Assets live under assets/.
* [x] Deck assets and card assets are separated.
* [x] Cards have a kind/type.
* [x] term and definition are not globally required anymore.
* [x] Each card kind defines its own required fields.
* [x] Media objects are structured and reusable.
* [x] Polyglot deck/card/media language support remains.
* [x] Unknown extra fields may be preserved for forward compatibility.