# mflash v4 Specification

## Status

Draft.

**v4 changes the transport layer to a Zstandard-compressed Protobuf file (`deck.pb`) instead of JSON, retaining the exact data structures and layout logic of v3.**

mflash v4 is a high-performance binary study deck format designed for typed study cards, organized packaged assets, polyglot learning, uploaded pronunciation audio, and image occlusion.

mflash v4 replaces the assumption that every card must be a term-definition flashcard. Basic term-definition cards remain supported, but they are now one card kind among several possible study card kinds.

---

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

## 3. Deck-Level Fields

### 3.1 Required deck fields

Every mflash v3 deck must include the following fields:

```json
{
  "format": "mflash",
  "version": 3,
  "id": "deck_001",
  "title": "Example Deck",
  "cards": []
}

```

Required fields:

* `format`
* `version`
* `id`
* `title`
* `cards`

**format**
The `format` field identifies the file as an mflash deck.
For mflash v3, it must be:

```json
"format": "mflash"

```

**version**
The `version` field identifies the mflash schema version.
For mflash v3, it must be:

```json
"version": 3

```

**id**
The `id` field is a stable deck identifier used for syncing, progress tracking, references, and app metadata.
The deck `id` should not contain personally identifying information.
Example:

```json
"id": "deck_21adb462"

```

**title**
The `title` field is the human-readable deck title.
Example:

```json
"title": "Human Anatomy"

```

**cards**
The `cards` field contains the deck's study cards.
It must be an array.
Example:

```json
"cards": []

```

### 3.2 Optional deck fields

mflash v3 decks may include the following optional fields:

* `description`
* `snippet`
* `created_at`
* `updated_at`
* `default_term_lang`
* `default_def_lang`
* `deck_tags`
* `cover`

**description**
A longer description of the deck.
Example:

```json
"description": "A deck for studying major bones, muscles, and organs."

```

**snippet**
A short summary of the deck, suitable for library views, search results, or previews.
Example:

```json
"snippet": "Study bones, muscles, organs, and anatomy diagrams."

```

**created_at**
An optional ISO 8601 timestamp for when the deck was created.
Example:

```json
"created_at": "2026-05-12T03:20:00Z"

```

Applications must not require this field.

**updated_at**
An optional ISO 8601 timestamp for when the deck content was last meaningfully updated.
Example:

```json
"updated_at": "2026-05-12T03:45:00Z"

```

Applications must not require this field.

**default_term_lang**
The default BCP 47 language tag for card terms when a card does not specify `term_lang`.
Example:

```json
"default_term_lang": "fr-FR"

```

**default_def_lang**
The default BCP 47 language tag for card definitions when a card does not specify `def_lang`.
Example:

```json
"default_def_lang": "en-US"

```

**deck_tags**
A list of tags describing the deck.
Example:

```json
"deck_tags": ["anatomy", "medicine", "biology"]

```

**cover**
A structured media object used as the deck's cover image.
Example:

```json
"cover": {
  "id": "cover_001",
  "type": "image",
  "role": "cover",
  "src": "assets/deck/cover.png",
  "alt": "Deck cover image"
}

```

### 3.3 Deck cover

mflash v3 replaces or supersedes the v2 `cover_media` string with a structured `cover` object.

v2 style:

```json
"cover_media": "media/cover.png"

```

v3 style:

```json
"cover": {
  "id": "cover_001",
  "type": "image",
  "role": "cover",
  "src": "assets/deck/cover.png",
  "alt": "Deck cover image"
}

```

The `cover` field uses the same media object shape used by card media.

Required cover media fields:

* `type`
* `src`

Recommended cover media fields:

* `id`
* `type`
* `role`
* `src`
* `alt`
* `description`

For deck covers, `type` should usually be:

```json
"type": "image"

```

For deck covers, `role` should usually be:

```json
"role": "cover"

```

### 3.4 Deck asset location

Deck-level assets should be stored under:

```text
assets/deck/

```

Recommended cover path:

```text
assets/deck/cover.png

```

Example package layout:

```text
deck.json
assets/
  deck/
    cover.png
  cards/
    card_001/
      pronunciation.mp3
      illustration.png

```

The deck cover is for deck identity, library display, thumbnails, storefront-style views, and file previews.
Card media is for study content.
Deck cover images should not be mixed into individual card asset folders.

## 4. Polyglot Language Support

mflash v3 preserves polyglot language support.

Decks may define default languages for terms and definitions. Individual cards may override those defaults. Media objects may also specify their own language when relevant, especially for pronunciation audio, listening cards, and example audio.

This allows a deck to define broad language behavior while still supporting mixed-language or multilingual cards.

---

### 4.1 Deck-level language defaults

A deck may define default languages for card terms and definitions.

Example:

```json
{
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US"
}
```

#### default_term_lang

The `default_term_lang` field defines the default BCP 47 language tag for card terms when a card does not specify `term_lang`.

Example:

```json
"default_term_lang": "fr-FR"
```

#### default_def_lang

The `default_def_lang` field defines the default BCP 47 language tag for card definitions when a card does not specify `def_lang`.

Example:

```json
"default_def_lang": "en-US"
```

Applications may use these fields for text-to-speech, language display, search, sorting, filtering, import/export behavior, and accessibility features.

---

### 4.2 Card-level language overrides

A card may override the deck-level language defaults.

Example:

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

#### term_lang

The `term_lang` field defines the BCP 47 language tag for the card's term.

If `term_lang` is present, it overrides the deck's `default_term_lang` for that card.

#### def_lang

The `def_lang` field defines the BCP 47 language tag for the card's definition.

If `def_lang` is present, it overrides the deck's `default_def_lang` for that card.

---

### 4.3 Media-level language

Media objects may define their own language with `lang`.

This is especially useful for pronunciation audio, listening prompts, spoken examples, explanation audio, and media where language-specific behavior matters.

Example:

```json
{
  "id": "audio_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/weltanschauung.mp3",
  "lang": "de-DE"
}
```

#### lang

The `lang` field defines the BCP 47 language tag for a media object.

If `lang` is present on a media object, it should be treated as the most specific language metadata for that media item.

---

### 4.4 Example language fields

Examples may continue to use language metadata.

Example:

```json
{
  "text": "Je voudrais du café.",
  "translation": "I would like some coffee.",
  "lang": "fr-FR",
  "translation_lang": "en-US"
}
```

#### lang

The `lang` field defines the language of the example text.

#### translation_lang

The `translation_lang` field defines the language of the example translation.

---

### 4.5 Language fallback order

Applications should use the most specific available language field.

General fallback order:

1. media `lang`
2. card language override
3. deck language default
4. application fallback

For term pronunciation:

1. `media.lang`
2. `card.term_lang`
3. `deck.default_term_lang`
4. application fallback

For definition pronunciation:

1. `media.lang`
2. `card.def_lang`
3. `deck.default_def_lang`
4. application fallback

For example text:

1. `example.lang`
2. `card.term_lang` or `card.def_lang`, depending on context
3. `deck.default_term_lang` or `deck.default_def_lang`, depending on context
4. application fallback

For example translation:

1. `example.translation_lang`
2. `deck.default_def_lang`
3. application fallback

---

### 4.6 TTS behavior

Applications that support text-to-speech should respect card-level overrides before deck-level defaults.

For a basic term-definition card:

```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "bonjour",
  "definition": "hello"
}
```

With deck defaults:

```json
{
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US"
}
```

The application should interpret:

- term language = `fr-FR`
- definition language = `en-US`

If the card overrides the term language:

```json
{
  "id": "card_002",
  "kind": "basic",
  "term": "Weltanschauung",
  "definition": "worldview",
  "term_lang": "de-DE"
}
```

The application should interpret:

- term language = `de-DE`
- definition language = `en-US`

When uploaded pronunciation audio exists, applications may prefer the uploaded audio file over generated TTS, depending on user settings.

Recommended playback order:

1. If file audio is enabled and matching pronunciation audio exists, play the file.
2. Otherwise, if TTS is enabled, speak using the language fallback rules.

---

### 4.7 BCP 47 language tags

Language fields should use BCP 47 language tags when possible.

Examples:

- `en`
- `en-US`
- `en-GB`
- `fr`
- `fr-FR`
- `de-DE`
- `ja-JP`
- `zh-CN`
- `es-MX`

Applications may accept common language names or aliases in their user interface, but saved mflash files should prefer BCP 47 tags.

---

### 4.8 Polyglot support checklist

- [x] Keep `default_term_lang` on deck.
- [x] Keep `default_def_lang` on deck.
- [x] Keep optional `term_lang` on cards.
- [x] Keep optional `def_lang` on cards.
- [x] Add optional `lang` to media objects.
- [x] Keep `lang` and `translation_lang` on examples.
- [x] Document fallback order: media lang > card lang > deck default.
- [x] Ensure TTS uses card override before deck default.

---

## 5. Summary of v3 Design Rules

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
* [x] Rename or supersede `cover_media` with `cover`.
* [x] Make `cover` use the same media object shape as card media.
* [x] Store deck cover files under `assets/deck/`.
* [x] Document that `cover` is for deck identity/library display.
* [x] Document that card media is for study content.

## 5. Redesign Cards Around `kind`

mflash v3 redesigns cards around a required `kind` field.

In mflash v2, every card was assumed to be a term-definition flashcard. In mflash v3, a card is a typed study item. Basic term-definition cards remain supported, but they are now represented as `kind: "basic"`.

---

### 5.1 Required card fields

Every mflash v3 card must include:

- `id`
- `kind`

**Example:**

```json
{
  "id": "card_001",
  "kind": "basic"
}
```

#### `id`
The `id` field is a stable identifier for the card.
- It may be used for progress tracking, syncing, media references, scheduling, review history, and app metadata.
- Card IDs should be unique within a deck.

**Example:** `"id": "card_001"`

#### `kind`
The `kind` field tells applications how to interpret, edit, and study the card.

**Example:** `"kind": "basic"`

Initial official card kinds include:
- `basic`
- `image_occlusion`
- `listening`
- `media_prompt`

Applications may support additional card kinds. If an application encounters an unknown card kind, it should preserve the card data when possible and show a useful fallback instead of deleting or corrupting the card.

---

### 5.2 `term` and `definition` are optional globally

In mflash v3, `term` and `definition` are no longer required on every card.

They are still normal fields for basic term-definition cards, but other card kinds may use different fields such as:
- `prompt`
- `answer`
- `media`
- `occlusion`

**Old v2 requirement:**
```json
"required": ["id", "term", "definition"]
```

**New v3 base card requirement:**
```json
"required": ["id", "kind"]
```

---

### 5.3 Basic cards

A basic card represents a traditional term-definition flashcard.

For `kind: "basic"`, applications should require:
- `id`
- `kind`
- `term`
- `definition`

**Example:**

```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as.",
  "media": []
}
```

Basic cards may also include:
- `term_lang`
- `def_lang`
- `phonetic`
- `part_of_speech`
- `notes`
- `tags`
- `examples`
- `media`

**Example with language metadata:**

```json
{
  "id": "card_002",
  "kind": "basic",
  "term": "Weltanschauung",
  "definition": "worldview",
  "term_lang": "de-DE",
  "def_lang": "en-US",
  "media": [
    {
      "id": "audio_001",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_002/weltanschauung.mp3",
      "lang": "de-DE"
    }
  ]
}
```

---

### 5.4 Non-basic cards

Non-basic cards do not need to use `term` and `definition`.

**Example: Image Occlusion Card**  
May use `prompt` and `occlusion`:

```json
{
  "id": "card_heart_001",
  "kind": "image_occlusion",
  "prompt": "Identify the hidden structure.",
  "occlusion": {
    "image": {
      "id": "heart_img",
      "type": "image",
      "role": "occlusion_image",
      "src": "assets/cards/card_heart_001/heart.png",
      "alt": "Diagram of the human heart"
    },
    "masks": []
  }
}
```

**Example: Listening Card**  
May use `prompt`, `media`, and `answer`:

```json
{
  "id": "card_listening_001",
  "kind": "listening",
  "prompt": "What word do you hear?",
  "answer": "bonjour",
  "media": [
    {
      "id": "audio_question_001",
      "type": "audio",
      "role": "question_audio",
      "src": "assets/cards/card_listening_001/bonjour.mp3",
      "lang": "fr-FR"
    }
  ]
}
```

**Example: Media Prompt Card**  
May use visual or video media:

```json
{
  "id": "card_media_001",
  "kind": "media_prompt",
  "prompt": "What process is shown here?",
  "answer": "Mitosis",
  "media": [
    {
      "id": "video_001",
      "type": "video",
      "role": "prompt_video",
      "src": "assets/cards/card_media_001/mitosis.mp4"
    }
  ]
}
```

---

### 5.5 Shared card fields

The following fields may be used across card kinds when relevant:
- `prompt`
- `answer`
- `term`
- `definition`
- `term_lang`
- `def_lang`
- `phonetic`
- `part_of_speech`
- `notes`
- `tags`
- `examples`
- `media`
- `occlusion`

#### `prompt`
A prompt shown to the learner.  
**Example:** `"prompt": "Identify the hidden structure."`

#### `answer`
An answer or expected response.  
**Example:** `"answer": "Aorta"`

#### `notes`
Additional notes for the card.  
**Example:** `"notes": "Often confused with the pulmonary artery."`

#### `tags`
Tags for organizing or filtering cards.  
**Example:** `"tags": ["anatomy", "heart"]`

#### `examples`
Example text, translations, or usage examples.  
**Example:**
```json
"examples": [
  {
    "text": "Je voudrais du café.",
    "translation": "I would like some coffee.",
    "lang": "fr-FR",
    "translation_lang": "en-US"
  }
]
```

#### `media`
A list of structured media objects attached to the card.  
**Example:**
```json
"media": [
  {
    "id": "img_001",
    "type": "image",
    "role": "illustration",
    "src": "assets/cards/card_001/image.png",
    "alt": "An illustration for the card"
  }
]
```

---

### 5.6 Kind-specific requirements

Each card kind defines its own required fields.

**Recommended initial requirements:**
- **`basic`:** `id`, `kind`, `term`, `definition`
- **`image_occlusion`:** `id`, `kind`, `occlusion`
- **`listening`:** `id`, `kind`, `media`, `answer`
- **`media_prompt`:** `id`, `kind`, `media`, `answer`

Applications should validate card-kind-specific requirements when possible.

Applications may allow incomplete cards while editing, but exported or released decks should satisfy the requirements for each card kind.

---

### 5.7 Migration from v2 cards

When migrating v2 cards to v3, applications should treat old term-definition cards as `kind: "basic"`.

**v2 card:**
```json
{
  "id": "card_001",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}
```

**v3 migrated card:**
```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as."
}
```

If a v2 card has `media`, `tags`, `notes`, `examples`, or language fields, those fields should be preserved during migration.

---

### 5.8 Card kind checklist

- [x] Add `kind` to every v3 card.
- [x] Make `term` optional globally.
- [x] Make `definition` optional globally.
- [x] For `kind: "basic"`, require `term` and `definition`.
- [x] For other kinds, require fields appropriate to that kind.
- [x] Keep `notes`, `tags`, `examples`, `media` available across card kinds.

## 6. Official Card Kinds

mflash v3 defines a small initial set of official card kinds.

The initial official card kinds are:
- `basic`
- `image_occlusion`
- `listening`
- `media_prompt`

Applications may support additional card kinds, but these four kinds form the first stable v3 baseline.

---

### 6.1 `basic`

A basic card is a traditional term-definition flashcard.

Use `basic` for vocabulary, concepts, definitions, names, facts, and ordinary two-sided flashcards.

**Required fields:**
- `id`
- `kind`
- `term`
- `definition`

**Example:**
```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as.",
  "media": []
}
```

A basic card may also include:
- `term_lang`
- `def_lang`
- `phonetic`
- `part_of_speech`
- `notes`
- `tags`
- `examples`
- `media`

**Example with pronunciation audio:**
```json
{
  "id": "card_002",
  "kind": "basic",
  "term": "Weltanschauung",
  "definition": "worldview",
  "term_lang": "de-DE",
  "def_lang": "en-US",
  "media": [
    {
      "id": "audio_term_001",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_002/weltanschauung.mp3",
      "lang": "de-DE"
    }
  ]
}
```

---

### 6.2 `image_occlusion`

An `image_occlusion` card hides one or more regions of an image and asks the learner to identify the hidden content.

Use `image_occlusion` for anatomy, maps, diagrams, machinery, art history, biological structures, charts, labels, and visual memorization.

**Required fields:**
- `id`
- `kind`
- `occlusion`

**Recommended fields:**
- `prompt`
- `tags`
- `notes`

**Example:**
```json
{
  "id": "card_heart_001",
  "kind": "image_occlusion",
  "prompt": "Identify the hidden structure.",
  "occlusion": {
    "image": {
      "id": "heart_img",
      "type": "image",
      "role": "occlusion_image",
      "src": "assets/cards/card_heart_001/heart.png",
      "alt": "Diagram of the human heart"
    },
    "masks": [
      {
        "id": "mask_001",
        "shape": "rect",
        "x": 0.42,
        "y": 0.31,
        "w": 0.18,
        "h": 0.08,
        "answer": "Aorta",
        "hint": "Main artery leaving the heart"
      }
    ]
  },
  "tags": ["anatomy", "heart"]
}
```

Image occlusion coordinates should be normalized from `0.0` to `1.0` relative to the image dimensions.

**Example:**
```json
{
  "x": 0.42,
  "y": 0.31,
  "w": 0.18,
  "h": 0.08
}
```

This allows occlusion masks to work even when the image is displayed at different sizes.

---

### 6.3 `listening`

A `listening` card is an audio-first prompt/answer card.

Use `listening` for language listening practice, dictation, pronunciation recognition, music identification, sound identification, or any study card where the primary prompt is audio.

**Required fields:**
- `id`
- `kind`
- `media`
- `answer`

**Recommended fields:**
- `prompt`
- `notes`
- `tags`

**Example:**
```json
{
  "id": "card_listening_001",
  "kind": "listening",
  "prompt": "What word do you hear?",
  "answer": "bonjour",
  "media": [
    {
      "id": "audio_question_001",
      "type": "audio",
      "role": "question_audio",
      "src": "assets/cards/card_listening_001/bonjour.mp3",
      "lang": "fr-FR"
    }
  ],
  "tags": ["french", "listening"]
}
```

A listening card may also include answer audio:
```json
{
  "id": "audio_answer_001",
  "type": "audio",
  "role": "answer_audio",
  "src": "assets/cards/card_listening_001/bonjour-answer.mp3",
  "lang": "fr-FR"
}
```

---

### 6.4 `media_prompt`

A `media_prompt` card uses image, gif, video, or other media as the main prompt.

Use `media_prompt` for identifying images, interpreting diagrams, recognizing scenes, studying historical images, analyzing video clips, or answering questions based on visual media.

**Required fields:**
- `id`
- `kind`
- `media`
- `answer`

**Recommended fields:**
- `prompt`
- `notes`
- `tags`

**Example:**
```json
{
  "id": "card_media_001",
  "kind": "media_prompt",
  "prompt": "What process is shown here?",
  "answer": "Mitosis",
  "media": [
    {
      "id": "video_001",
      "type": "video",
      "role": "prompt_video",
      "src": "assets/cards/card_media_001/mitosis.mp4",
      "description": "A short clip showing cell division."
    }
  ],
  "tags": ["biology", "cell division"]
}
```

A media prompt may use an image:
```json
{
  "id": "image_prompt_001",
  "type": "image",
  "role": "prompt_image",
  "src": "assets/cards/card_media_001/painting.png",
  "alt": "A historical painting"
}
```

or a gif:
```json
{
  "id": "gif_prompt_001",
  "type": "gif",
  "role": "prompt_animation",
  "src": "assets/cards/card_media_001/process.gif",
  "alt": "Animated process diagram"
}
```

---

### 6.5 Unknown or extension card kinds

Applications may encounter card kinds outside the official v3 set.

**Example:**
```json
{
  "id": "card_custom_001",
  "kind": "multiple_choice",
  "prompt": "Which answer is correct?",
  "choices": ["A", "B", "C", "D"],
  "answer": "B"
}
```

If an application does not support a card kind, it should:
- Preserve the card data
- Avoid deleting unknown fields
- Show a useful fallback message
- Avoid silently converting the card to another kind

**Recommended fallback message:**
> This card kind is not supported by this application.

Applications may still show raw JSON or limited metadata for unsupported cards.

---

### 6.6 Later candidate card kinds

The following card kinds are candidates for future versions or extensions:

- **`cloze`**  
  A fill-in-the-blank card.  
  *Potential use:* Language learning, quotes, formulas, definitions, memorized passages.

- **`multiple_choice`**  
  A prompt with predefined answer options.  
  *Potential use:* Quizzes, exam prep, recognition practice.

- **`typing`**  
  A card that requires the learner to type the answer.  
  *Potential use:* Spelling, language production, formulas, exact recall.

- **`ordering`**  
  A card where the learner orders items correctly.  
  *Potential use:* Processes, timelines, taxonomies, steps.

- **`matching`**  
  A card where the learner matches related items.  
  *Potential use:* Vocabulary pairs, names and dates, images and labels.

- **`reverse`**  
  A card designed to generate or represent reverse-direction practice.  
  *Potential use:* Definition-to-term review, translation reversal, bidirectional vocabulary.

These candidates are not part of the required v3 baseline unless formally added to the official card kind list.

---

### 6.7 Official card kind checklist

- [x] `basic`
- [x] `image_occlusion`
- [x] `listening`
- [x] `media_prompt`

**Later candidates:**
- [ ] `cloze`
- [ ] `multiple_choice`
- [ ] `typing`
- [ ] `ordering`
- [ ] `matching`
- [ ] `reverse`

## 7. Standardize Media Objects

mflash v3 uses one standard media object shape for deck covers, card images, audio, video, gifs, documents, pronunciation files, prompt media, answer media, and occlusion images.

In mflash v2, media could be represented inconsistently, including as a bare string in some cases. In mflash v3, media should be represented as structured objects.

---

### 7.1 Media object shape

Every media item should use this general shape:

```json
{
  "id": "media_001",
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/image.png",
  "alt": "A diagram",
  "description": "Optional longer description",
  "lang": "en-US"
}
```

**Required fields:**
- `type`
- `src`

**Optional fields:**
- `id`
- `role`
- `alt`
- `description`
- `lang`

---

### 7.2 Required media fields

#### `type`
The `type` field describes what kind of media file this is.

**Example:**
```json
"type": "image"
```

**Recommended media types:**
- `image`
- `audio`
- `video`
- `gif`
- `document`
- `other`

Applications should use `other` for media that does not fit the official type list.

#### `src`
The `src` field points to the media file.

For packaged `.mflash` decks, `src` should be a relative path inside the package.

**Example:**
```json
"src": "assets/cards/card_001/image.png"
```

Packaged v3 decks should **not** store absolute local filesystem paths such as:
```text
/home/user/Pictures/image.png
C:\Users\User\Pictures\image.png
```

Applications may temporarily use absolute paths while editing, but saved packaged decks should ingest the file and rewrite `src` to a relative package path.

---

### 7.3 Optional media fields

#### `id`
The `id` field is an optional stable identifier for the media item.

**Example:** `"id": "audio_term_001"`

Media IDs should be unique within the object that owns them, such as a card's media array.

#### `role`
The `role` field describes how the media is used.

**Example:** `"role": "term_pronunciation"`

The media type says what the file is. The media role says what the file is for.

For example, both of these are audio files but have different study behavior:
```json
{
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/term.mp3"
}
```
```json
{
  "type": "audio",
  "role": "question_audio",
  "src": "assets/cards/card_002/question.mp3"
}
```

#### `alt`
The `alt` field provides short alternative text for visual media.

**Example:** `"alt": "Diagram of the human heart"`

Applications should use `alt` for accessibility, search, exports, and fallback display when an image cannot be shown.

#### `description`
The `description` field provides a longer description of the media item.

**Example:** `"description": "A labeled diagram showing the major chambers and vessels of the heart."`

#### `lang`
The `lang` field defines the BCP 47 language tag for the media item when language is relevant.

**Example:** `"lang": "fr-FR"`

This is especially useful for:
- Term pronunciation audio
- Definition pronunciation audio
- Question audio
- Answer audio
- Example audio
- Spoken explanations
- Videos with spoken language

---

### 7.4 Card media is always an array

In mflash v3, card media should always be an array of media objects.

**Valid:**
```json
"media": []
```

**Valid:**
```json
"media": [
  {
    "id": "img_001",
    "type": "image",
    "role": "illustration",
    "src": "assets/cards/card_001/image.png",
    "alt": "A diagram"
  }
]
```

**Deprecated v2-style media string:**
```json
"media": "image.png"
```

Applications may support bare media strings when importing or migrating older decks, but v3-authored decks should use media arrays.

---

### 7.5 Recommended media types

mflash v3 defines the following recommended media types:

#### `image`
Use for still images.  
**File examples:** `png`, `jpg`, `jpeg`, `webp`, `svg`

```json
{
  "id": "img_001",
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/image.png",
  "alt": "An illustration"
}
```

#### `audio`
Use for audio files.  
**File examples:** `mp3`, `wav`, `ogg`, `flac`, `m4a`

```json
{
  "id": "audio_term_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/pronunciation.mp3",
  "lang": "en-US"
}
```

#### `video`
Use for video files.  
**File examples:** `mp4`, `webm`, `mov`, `mkv`

```json
{
  "id": "video_001",
  "type": "video",
  "role": "prompt_video",
  "src": "assets/cards/card_001/clip.mp4",
  "description": "A short video prompt."
}
```

#### `gif`
Use for animated gifs when the file should be treated as a gif rather than a generic image.

```json
{
  "id": "gif_001",
  "type": "gif",
  "role": "prompt_animation",
  "src": "assets/cards/card_001/process.gif",
  "alt": "Animated process diagram"
}
```

#### `document`
Use for attached documents.  
**File examples:** `pdf`, `txt`, `html`, `md`

```json
{
  "id": "doc_001",
  "type": "document",
  "role": "source_document",
  "src": "assets/cards/card_001/source.pdf",
  "description": "A source document for the card."
}
```

#### `other`
Use when none of the official media types apply.

```json
{
  "id": "file_001",
  "type": "other",
  "role": "supplement",
  "src": "assets/cards/card_001/file.bin"
}
```

---

### 7.6 Recommended media roles

mflash v3 defines the following recommended media roles:

- `cover`
- `illustration`
- `prompt_image`
- `answer_image`
- `prompt_video`
- `answer_video`
- `prompt_animation`
- `answer_animation`
- `term_pronunciation`
- `definition_pronunciation`
- `question_audio`
- `answer_audio`
- `example_audio`
- `explanation_audio`
- `occlusion_image`
- `source_document`
- `supplement`

**Initial recommended role set:**
- `cover`
- `illustration`
- `prompt_image`
- `answer_image`
- `term_pronunciation`
- `definition_pronunciation`
- `question_audio`
- `answer_audio`
- `example_audio`
- `explanation_audio`
- `occlusion_image`

---

### 7.7 Role descriptions

#### `cover`
Use for a deck cover image.
```json
{
  "id": "cover_001",
  "type": "image",
  "role": "cover",
  "src": "assets/deck/cover.png",
  "alt": "Deck cover image"
}
```

#### `illustration`
Use for supporting card imagery.
```json
{
  "id": "img_001",
  "type": "image",
  "role": "illustration",
  "src": "assets/cards/card_001/illustration.png",
  "alt": "A supporting illustration"
}
```

#### `prompt_image`
Use when an image is the question or prompt.
```json
{
  "id": "prompt_img_001",
  "type": "image",
  "role": "prompt_image",
  "src": "assets/cards/card_001/prompt.png",
  "alt": "Image prompt"
}
```

#### `answer_image`
Use when an image is part of the answer.
```json
{
  "id": "answer_img_001",
  "type": "image",
  "role": "answer_image",
  "src": "assets/cards/card_001/answer.png",
  "alt": "Answer image"
}
```

#### `term_pronunciation`
Use for uploaded pronunciation audio for a card's term.
```json
{
  "id": "audio_term_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/term.mp3",
  "lang": "fr-FR"
}
```

#### `definition_pronunciation`
Use for uploaded pronunciation audio for a card's definition.
```json
{
  "id": "audio_def_001",
  "type": "audio",
  "role": "definition_pronunciation",
  "src": "assets/cards/card_001/definition.mp3",
  "lang": "en-US"
}
```

#### `question_audio`
Use when audio is the main question or prompt.
```json
{
  "id": "audio_question_001",
  "type": "audio",
  "role": "question_audio",
  "src": "assets/cards/card_001/question.mp3",
  "lang": "fr-FR"
}
```

#### `answer_audio`
Use when audio is part of the answer.
```json
{
  "id": "audio_answer_001",
  "type": "audio",
  "role": "answer_audio",
  "src": "assets/cards/card_001/answer.mp3",
  "lang": "fr-FR"
}
```

#### `example_audio`
Use for audio attached to an example sentence or usage example.
```json
{
  "id": "audio_example_001",
  "type": "audio",
  "role": "example_audio",
  "src": "assets/cards/card_001/example.mp3",
  "lang": "fr-FR"
}
```

#### `explanation_audio`
Use for spoken explanations.
```json
{
  "id": "audio_explanation_001",
  "type": "audio",
  "role": "explanation_audio",
  "src": "assets/cards/card_001/explanation.mp3",
  "lang": "en-US"
}
```

#### `occlusion_image`
Use for the base image in an image occlusion card.
```json
{
  "id": "heart_img",
  "type": "image",
  "role": "occlusion_image",
  "src": "assets/cards/card_heart_001/heart.png",
  "alt": "Diagram of the human heart"
}
```

---

### 7.8 Media path rules

In packaged `.mflash` decks, media paths should be relative to the package root.

**Valid:**
```text
assets/deck/cover.png
assets/cards/card_001/image.png
assets/cards/card_001/pronunciation.mp3
```

**Invalid for released packaged decks:**
```text
/home/user/Pictures/image.png
C:\Users\User\Pictures\image.png
../outside-folder/image.png
```

Media paths should not escape the package root. Applications should reject or sanitize path traversal patterns such as:
- `../`
- `..\`

---

### 7.9 Media ownership

**Deck-level media** belongs under:
```text
assets/deck/
```

**Card-level media** belongs under:
```text
assets/cards/<card_id>/
```

**Example structure:**
```text
deck.json
assets/
  deck/
    cover.png
  cards/
    card_001/
      lative.mp3
      illustration.png
```

A card should not normally reference another card's asset directory.

**Discouraged:**
```json
{
  "id": "card_002",
  "kind": "basic",
  "media": [
    {
      "type": "image",
      "src": "assets/cards/card_001/image.png"
    }
  ]
}
```

Shared assets may be supported later with an explicit shared asset directory, but the initial v3 convention is card-local media.

---

### 7.10 Migration from v2 media

v2 media may appear as a bare string or older object shape.

**v2-style bare string:**
```json
"media": "image.png"
```

**v3 migrated form:**
```json
"media": [
  {
    "type": "image",
    "role": "illustration",
    "src": "assets/cards/card_001/image.png"
  }
]
```

**v2-style card image:**
```json
"media": {
  "type": "image",
  "path": "image.png",
  "alt": "An image"
}
```

**v3 migrated form:**
```json
"media": [
  {
    "type": "image",
    "role": "illustration",
    "src": "assets/cards/card_001/image.png",
    "alt": "An image"
  }
]
```

**When migrating from v2 to v3:**
- `path` should become `src`
- Bare strings should become media objects
- Card media should become an array
- Deck `cover_media` should become `deck.cover`

---

### 7.11 Media object checklist

- [x] Media object requires `type` and `src`.
- [x] Media object may have `id`.
- [x] Media object may have `role`.
- [x] Media object may have `alt`.
- [x] Media object may have `description`.
- [x] Media object may have `lang`.
- [x] Card media is always an array.
- [x] Remove or deprecate media as a bare string.

**Recommended media types:**
- [x] `image`
- [x] `audio`
- [x] `video`
- [x] `gif`
- [x] `document`
- [x] `other`

**Recommended media roles:**
- [x] `cover`
- [x] `illustration`
- [x] `prompt_image`
- [x] `answer_image`
- [x] `term_pronunciation`
- [x] `definition_pronunciation`
- [x] `question_audio`
- [x] `answer_audio`
- [x] `example_audio`
- [x] `explanation_audio`
- [x] `occlusion_image`

## 8. Pronunciation Audio Support

mflash v3 officially supports uploaded pronunciation audio.

Pronunciation audio allows a deck author to attach recorded or generated audio files to cards. Applications may use these files instead of generated text-to-speech when studying, reviewing, or previewing cards.

Pronunciation audio is represented using standard media objects with `type: "audio"` and a pronunciation-specific `role`.

---

### 8.1 Term pronunciation audio

Use `role: "term_pronunciation"` for audio that pronounces a card's term.

**Example:**
```json
{
  "id": "audio_term_001",
  "type": "audio",
  "role": "term_pronunciation",
  "src": "assets/cards/card_001/lative.mp3",
  "lang": "en-US"
}
```

**Recommended use:**
- Vocabulary words
- Names
- Technical terms
- Foreign-language terms
- Phonetic drills

**For a basic card:**
```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as.",
  "term_lang": "en-US",
  "media": [
    {
      "id": "audio_term_001",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_001/lative.mp3",
      "lang": "en-US"
    }
  ]
}
```

---

### 8.2 Definition pronunciation audio

Use `role: "definition_pronunciation"` for audio that pronounces a card's definition.

**Example:**
```json
{
  "id": "audio_definition_001",
  "type": "audio",
  "role": "definition_pronunciation",
  "src": "assets/cards/card_001/definition.mp3",
  "lang": "en-US"
}
```

**This is useful for:**
- Accessibility
- Language-learning definitions
- Spoken explanations
- Hands-free study

**Example:**
```json
{
  "id": "card_002",
  "kind": "basic",
  "term": "bonjour",
  "definition": "hello",
  "term_lang": "fr-FR",
  "def_lang": "en-US",
  "media": [
    {
      "id": "audio_term_001",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_002/bonjour.mp3",
      "lang": "fr-FR"
    },
    {
      "id": "audio_def_001",
      "type": "audio",
      "role": "definition_pronunciation",
      "src": "assets/cards/card_002/hello.mp3",
      "lang": "en-US"
    }
  ]
}
```

---

### 8.3 Example audio

Use `role: "example_audio"` for audio attached to an example sentence or usage example.

**Example:**
```json
{
  "id": "audio_example_001",
  "type": "audio",
  "role": "example_audio",
  "src": "assets/cards/card_001/example.mp3",
  "lang": "fr-FR"
}
```

If an application needs to associate audio with a specific example, it may use an extension field such as `example_id` or place the audio reference inside a structured example object.

**Example with `example_id`:**
```json
{
  "id": "audio_example_001",
  "type": "audio",
  "role": "example_audio",
  "src": "assets/cards/card_001/example_001.mp3",
  "lang": "fr-FR",
  "example_id": "example_001"
}
```

**Example structured example:**
```json
{
  "id": "example_001",
  "text": "Je voudrais du café.",
  "translation": "I would like some coffee.",
  "lang": "fr-FR",
  "translation_lang": "en-US",
  "media": [
    {
      "id": "audio_example_001",
      "type": "audio",
      "role": "example_audio",
      "src": "assets/cards/card_001/example_001.mp3",
      "lang": "fr-FR"
    }
  ]
}
```

Applications may support either pattern. The shared media object shape remains the same.

---

### 8.4 Question audio for listening cards

Use `role: "question_audio"` for audio that acts as the main prompt in a listening card.

**Example:**
```json
{
  "id": "audio_question_001",
  "type": "audio",
  "role": "question_audio",
  "src": "assets/cards/card_listening_001/bonjour.mp3",
  "lang": "fr-FR"
}
```

**Listening card example:**
```json
{
  "id": "card_listening_001",
  "kind": "listening",
  "prompt": "What word do you hear?",
  "answer": "bonjour",
  "media": [
    {
      "id": "audio_question_001",
      "type": "audio",
      "role": "question_audio",
      "src": "assets/cards/card_listening_001/bonjour.mp3",
      "lang": "fr-FR"
    }
  ],
  "tags": ["french", "listening"]
}
```

---

### 8.5 File audio and TTS fallback

Applications may support both uploaded audio files and generated text-to-speech (TTS).

**Recommended behavior:**
1. Prefer uploaded audio when file audio is enabled and matching audio exists.
2. Fall back to TTS when uploaded audio is missing, disabled, or cannot be played.
3. Use mflash language fallback rules when generating TTS.

This allows users to choose between recorded pronunciation and generated speech.

**Example app controls:**
- File audio: `enabled` / `disabled`
- TTS: `enabled` / `disabled`

---

### 8.6 Suggested playback order for basic cards

For a basic card with `term` and `definition`, the recommended playback order is:

1. If file audio is enabled and `term_pronunciation` exists, play that file.
2. Else if TTS is enabled, speak `term` using the term language fallback.
3. If file audio is enabled and `definition_pronunciation` exists, play that file.
4. Else if TTS is enabled, speak `definition` using the definition language fallback.

**Term language fallback chain:**
1. `term` pronunciation media `lang`
2. `card.term_lang`
3. `deck.default_term_lang`
4. Application fallback

**Definition language fallback chain:**
1. `definition` pronunciation media `lang`
2. `card.def_lang`
3. `deck.default_def_lang`
4. Application fallback

---

### 8.7 Multiple pronunciation files

A card may include multiple pronunciation files when useful.

**Examples:**
- Different speakers
- Different accents
- Slow pronunciation
- Natural pronunciation
- Regional variants

**Example:**
```json
{
  "id": "card_003",
  "kind": "basic",
  "term": "tomato",
  "definition": "A red edible fruit often used as a vegetable.",
  "term_lang": "en-US",
  "media": [
    {
      "id": "audio_term_us",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_003/tomato-us.mp3",
      "lang": "en-US",
      "variant": "US"
    },
    {
      "id": "audio_term_uk",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_003/tomato-uk.mp3",
      "lang": "en-GB",
      "variant": "UK"
    }
  ]
}
```

Applications may choose the best matching audio by language, user preference, order in the media array, or app-specific settings.

---

### 8.8 Audio file location

Card pronunciation audio should be stored under the card's asset directory:
```text
assets/cards/<card_id>/
```

**Example paths:**
```text
assets/cards/card_001/lative.mp3
assets/cards/card_001/definition.mp3
assets/cards/card_001/example_001.mp3
```

In packaged `.mflash` decks, audio `src` paths should be relative package paths.

**Valid:**
```text
assets/cards/card_001/lative.mp3
```

**Invalid for released packaged decks:**
```text
/home/user/Audio/lative.mp3
C:\Users\User\Audio\lative.mp3
../outside-folder/lative.mp3
```

---

### 8.9 Audio support checklist

- [x] Add `term_pronunciation` media role.
- [x] Add `definition_pronunciation` media role.
- [x] Add `example_audio` media role.
- [x] Add `question_audio` media role for listening cards.
- [x] Document file audio vs TTS fallback.
- [x] App should prefer uploaded pronunciation if enabled.
- [x] App should fall back to TTS if no uploaded audio exists.

**Suggested playback order:**
- [x] If file audio enabled and `term_pronunciation` exists, play file.
- [x] Else if TTS enabled, speak term using card/deck language.
- [x] If file audio enabled and `definition_pronunciation` exists, play file.
- [x] Else if TTS enabled, speak definition using card/deck language.

## 9. Image Occlusion Support

mflash v3 supports image occlusion as a first-class card kind.

Image occlusion cards hide one or more regions of an image and ask the learner to identify the hidden content. This is useful for anatomy, maps, diagrams, machinery, art history, biology, geography, charts, labels, and visual memorization.

Image occlusion cards use:
```text
kind: "image_occlusion"
```

---

### 9.1 Basic image occlusion card

**Example:**
```json
{
  "id": "card_heart_001",
  "kind": "image_occlusion",
  "prompt": "Identify the hidden structure.",
  "occlusion": {
    "image": {
      "id": "heart_img",
      "type": "image",
      "role": "occlusion_image",
      "src": "assets/cards/card_heart_001/heart.png",
      "alt": "Diagram of the human heart"
    },
    "masks": [
      {
        "id": "mask_001",
        "shape": "rect",
        "x": 0.42,
        "y": 0.31,
        "w": 0.18,
        "h": 0.08,
        "answer": "Aorta",
        "hint": "Main artery leaving the heart"
      }
    ]
  }
}
```

**Required fields for an image occlusion card:**
- `id`
- `kind`
- `occlusion`

**Recommended fields:**
- `prompt`
- `tags`
- `notes`

---

### 9.2 Occlusion object

The `occlusion` object contains the base image and the masks used to hide parts of that image.

**Required occlusion fields:**
- `image`
- `masks`

**Example:**
```json
"occlusion": {
  "image": {
    "id": "heart_img",
    "type": "image",
    "role": "occlusion_image",
    "src": "assets/cards/card_heart_001/heart.png",
    "alt": "Diagram of the human heart"
  },
  "masks": []
}
```

---

### 9.3 Occlusion image

The `occlusion.image` field is a standard mflash media object.

It should use:
- `"type": "image"`
- and usually: `"role": "occlusion_image"`

**Example:**
```json
{
  "id": "skeleton_img",
  "type": "image",
  "role": "occlusion_image",
  "src": "assets/cards/card_skeleton_001/skeleton.png",
  "alt": "Diagram of the human skeleton"
}
```

The image file should be stored under the card's asset directory:
```text
assets/cards/<card_id>/
```

**Example:**
```text
assets/cards/card_skeleton_001/skeleton.png
```

---

### 9.4 Masks array

The `masks` field is an array of occlusion mask objects. Each mask represents one hidden region on the image.

**Example:**
```json
"masks": [
  {
    "id": "mask_001",
    "shape": "rect",
    "x": 0.42,
    "y": 0.31,
    "w": 0.18,
    "h": 0.08,
    "answer": "Aorta",
    "hint": "Main artery leaving the heart"
  }
]
```

**Each mask should have:**
- `id`
- `shape`
- `answer`

Shape-specific coordinate fields are also required depending on the mask shape.

---

### 9.5 Normalized coordinates

Image occlusion coordinates should use normalized values from `0.0` to `1.0`.

This means coordinates are relative to the image dimensions, not absolute pixels.

**Example:**
```json
{
  "x": 0.42,
  "y": 0.31,
  "w": 0.18,
  "h": 0.08
}
```

This allows masks to keep working when the image is resized.

**For rectangular and elliptical masks:**
| Coordinate | Description |
|------------|-------------|
| `x` | Horizontal position from the left edge of the image |
| `y` | Vertical position from the top edge of the image |
| `w` | Mask width relative to image width |
| `h` | Mask height relative to image height |

Applications should clamp or reject invalid coordinate values outside the `0.0` to `1.0` range.

---

### 9.6 Rectangular masks

Rectangular masks use:
```json
"shape": "rect"
```

**Required fields:**
- `id`
- `shape`
- `x`
- `y`
- `w`
- `h`
- `answer`

**Example:**
```json
{
  "id": "mask_001",
  "shape": "rect",
  "x": 0.42,
  "y": 0.31,
  "w": 0.18,
  "h": 0.08,
  "answer": "Aorta",
  "hint": "Main artery leaving the heart"
}
```

Applications should support rectangular masks first.

---

### 9.7 Ellipse masks

Ellipse masks use:
```json
"shape": "ellipse"
```

**Required fields:**
- `id`
- `shape`
- `x`
- `y`
- `w`
- `h`
- `answer`

**Example:**
```json
{
  "id": "mask_002",
  "shape": "ellipse",
  "x": 0.55,
  "y": 0.44,
  "w": 0.14,
  "h": 0.10,
  "answer": "Left atrium",
  "hint": "Upper chamber on the viewer's right side of the diagram"
}
```

For ellipse masks, `x`, `y`, `w`, and `h` describe the bounding box of the ellipse.

---

### 9.8 Polygon masks

Polygon masks use:
```json
"shape": "polygon"
```

**Required fields:**
- `id`
- `shape`
- `points`
- `answer`

The `points` field is an array of normalized coordinate pairs.

**Example:**
```json
{
  "id": "mask_003",
  "shape": "polygon",
  "points": [
    { "x": 0.20, "y": 0.30 },
    { "x": 0.32, "y": 0.34 },
    { "x": 0.28, "y": 0.47 },
    { "x": 0.18, "y": 0.42 }
  ],
  "answer": "Scapula",
  "hint": "Shoulder blade"
}
```

Polygon points should also use normalized coordinates from `0.0` to `1.0`.

---

### 9.9 Mask answer, hint, and explanation

Each mask should include an `answer`.

**Example:**
```json
"answer": "Aorta"
```

A mask may include a `hint`.

**Example:**
```json
"hint": "Main artery leaving the heart"
```

A mask may include an `explanation`.

**Example:**
```json
"explanation": "The aorta carries oxygenated blood from the left ventricle to the body."
```

**Recommended mask fields:**
- `id`
- `shape`
- `answer`
- `hint` (optional)
- `explanation` (optional)

---

### 9.10 Multiple masks

A single image occlusion card may contain multiple masks.

**Example:**
```json
{
  "id": "card_heart_001",
  "kind": "image_occlusion",
  "prompt": "Identify the hidden structures.",
  "occlusion": {
    "image": {
      "id": "heart_img",
      "type": "image",
      "role": "occlusion_image",
      "src": "assets/cards/card_heart_001/heart.png",
      "alt": "Diagram of the human heart"
    },
    "masks": [
      {
        "id": "mask_001",
        "shape": "rect",
        "x": 0.42,
        "y": 0.31,
        "w": 0.18,
        "h": 0.08,
        "answer": "Aorta"
      },
      {
        "id": "mask_002",
        "shape": "ellipse",
        "x": 0.58,
        "y": 0.44,
        "w": 0.14,
        "h": 0.10,
        "answer": "Left atrium"
      }
    ]
  }
}
```

Applications may choose to study all masks at once or generate separate review prompts for each mask.

---

### 9.11 One-card versus generated-card behavior

An image occlusion card may be treated in two ways:

| Mode | Description |
|------|-------------|
| **single-card mode** | The card is reviewed as one card with multiple hidden regions. |
| **generated-card mode** | An application may generate separate review items from each mask. |

For example, one image occlusion card with three masks may become three study prompts during review.

Applications should preserve the source card and mask IDs so progress systems can track review history consistently.

**Recommended generated review identifier pattern:**
```text
<card_id>#<mask_id>
```

**Example:**
```text
card_heart_001#mask_001
```

---

### 9.12 Image occlusion asset location

Image occlusion base images should live under the card's asset directory.

**Recommended layout:**
```text
deck.json
assets/
  cards/
    card_heart_001/
      heart.png
```

The corresponding JSON should use:
```json
"src": "assets/cards/card_heart_001/heart.png"
```

---

### 9.13 Image occlusion checklist

- [x] Add `image_occlusion` card kind.
- [x] Add `occlusion` object.
- [x] Add `occlusion.image` media object.
- [x] Add `masks` array.
- [x] Use normalized coordinates from `0.0` to `1.0`.
- [x] Support `rect` masks first.
- [x] Define `ellipse` masks.
- [x] Define `polygon` masks.
- [x] Each mask has `id`.
- [x] Each mask has `shape`.
- [x] Each mask has `answer`.
- [x] Optional `hint` per mask.
- [x] Optional `explanation` per mask.

**Mask shape checklist:**
- [x] `rect`: `x`, `y`, `w`, `h`
- [x] `ellipse`: `x`, `y`, `w`, `h`
- [x] `polygon`: `points` array

## 10. Package Asset Rules

mflash v3 defines a standard package layout for `.mflash` archives.

A packaged `.mflash` file is a ZIP archive. The deck data lives in `deck.json` at the archive root. Media and other supporting files live under `assets/`.

---

## 10. Package Asset Rules

mflash v3 defines a standard package layout for `.mflash` archives.

A packaged `.mflash` file is a ZIP archive. The deck data lives in `deck.json` at the archive root. Media and other supporting files live under `assets/`.

---

### 10.1 Official v3 package layout

Official v3 package layout:
```text
deck.json
assets/
  deck/
  cards/
    <card_id>/
```

**Example:**
```text
deck.json
assets/
  deck/
    cover.png
  cards/
    card_001/
      lative.mp3
      illustration.png
    card_002/
      heart.png
```

---

### 10.2 `deck.json` is required at root

Every packaged `.mflash` archive must contain `deck.json` at the archive root.

**Valid:**
```text
deck.json
assets/deck/cover.png
assets/cards/card_001/image.png
```

**Invalid:**
```text
data/deck.json
mflash/deck.json
assets/deck.json
```

Applications should reject packaged decks that do not contain root-level `deck.json`.

---

### 10.3 `assets/` is the standard asset folder

All v3 packaged assets should live under:
```text
assets/
```

This includes:
- Deck cover images
- Card images
- Pronunciation audio
- Question audio
- Answer audio
- Example audio
- Videos
- GIFs
- Image occlusion base images
- Documents
- Supplementary files

Applications may preserve unknown legacy files outside `assets/`, but v3-authored packages should place new assets under `assets/`.

---

### 10.4 Deck-level assets

Deck-level assets should live under:
```text
assets/deck/
```

Use this folder for files that belong to the deck itself rather than to a specific card.

**Recommended examples:**
- `assets/deck/cover.png`
- `assets/deck/banner.png`
- `assets/deck/icon.png`

The most common deck-level asset is the deck cover:
```json
"cover": {
  "id": "cover_001",
  "type": "image",
  "role": "cover",
  "src": "assets/deck/cover.png",
  "alt": "Deck cover image"
}
```

Deck-level assets are for deck identity, library display, thumbnails, file previews, and app presentation.

---

### 10.5 Card-level assets

Card-level assets should live under:
```text
assets/cards/<card_id>/
```

**Example paths:**
- `assets/cards/card_001/lative.mp3`
- `assets/cards/card_001/illustration.png`
- `assets/cards/card_002/heart.png`

Card-level assets are study content attached to a specific card. Examples include:
- Term pronunciation audio
- Definition pronunciation audio
- Illustrations
- Prompt images
- Answer images
- Videos
- GIFs
- Image occlusion base images
- Example audio

**Example card media:**
```json
{
  "id": "card_001",
  "kind": "basic",
  "term": "Lative",
  "definition": "Indicating motion up to or as far as.",
  "media": [
    {
      "id": "audio_term_001",
      "type": "audio",
      "role": "term_pronunciation",
      "src": "assets/cards/card_001/lative.mp3",
      "lang": "en-US"
    },
    {
      "id": "img_001",
      "type": "image",
      "role": "illustration",
      "src": "assets/cards/card_001/illustration.png",
      "alt": "Illustration for the term"
    }
  ]
}
```

---

### 10.6 Relative packaged paths

In packaged `.mflash` decks, all `src` paths should be relative to the package root.

**Valid:**
```text
assets/deck/cover.png
assets/cards/card_001/lative.mp3
assets/cards/card_001/illustration.png
assets/cards/card_002/heart.png
```

**Invalid for released packaged decks:**
```text
/home/user/Pictures/cover.png
/home/user/Audio/lative.mp3
C:\Users\User\Pictures\cover.png
../outside-folder/image.png
```

Applications should not save absolute local filesystem paths into released packaged `.mflash` decks.

---

### 10.7 Editing paths versus packaged paths

Applications may temporarily use absolute local filesystem paths while editing.

**Example temporary editing path:**
```text
/home/user/Pictures/cover.png
```

But when saving or exporting a packaged `.mflash`, the application should:
1. Copy the file into the package under `assets/`.
2. Rewrite the media `src` to a relative package path.
3. Save the updated `deck.json`.

**Example rewrite:**
```text
/home/user/Pictures/cover.png → assets/deck/cover.png
/home/user/Audio/lative.mp3 → assets/cards/card_001/lative.mp3
```

---

### 10.8 Save/export ingest behavior

When saving or exporting a packaged `.mflash`, applications should ingest external asset files.

**Recommended behavior:**
- [ ] Detect absolute local asset paths.
- [ ] Copy deck-level assets into `assets/deck/`.
- [ ] Copy card-level assets into `assets/cards/<card_id>/`.
- [ ] Rewrite all `src` paths to relative package paths.
- [ ] Write `deck.json` at the archive root.
- [ ] Preserve existing package files when practical.
- [ ] Avoid duplicate filenames or safely rename duplicates.
- [ ] Prevent path traversal outside the package.

**Example:**

*Before save:*
```json
{
  "cover": {
    "type": "image",
    "role": "cover",
    "src": "/home/user/Pictures/anatomy-cover.png"
  },
  "cards": [
    {
      "id": "card_001",
      "kind": "basic",
      "term": "Clavicle",
      "definition": "The collarbone.",
      "media": [
        {
          "type": "audio",
          "role": "term_pronunciation",
          "src": "/home/user/Audio/clavicle.mp3"
        }
      ]
    }
  ]
}
```

*After save:*
```json
{
  "cover": {
    "type": "image",
    "role": "cover",
    "src": "assets/deck/anatomy-cover.png"
  },
  "cards": [
    {
      "id": "card_001",
      "kind": "basic",
      "term": "Clavicle",
      "definition": "The collarbone.",
      "media": [
        {
          "type": "audio",
          "role": "term_pronunciation",
          "src": "assets/cards/card_001/clavicle.mp3"
        }
      ]
    }
  ]
}
```

---

### 10.9 Duplicate filenames

Applications should avoid asset collisions.

For example, if two cards both import a file named `image.png`, they can safely coexist because card assets are stored in card-specific folders:
```text
assets/cards/card_001/image.png
assets/cards/card_002/image.png
```

If multiple files with the same name are imported into the same card directory, applications should rename them safely.

**Example:**
```text
assets/cards/card_001/image.png
assets/cards/card_001/image_2.png
assets/cards/card_001/image_3.png
```

Applications should update the corresponding `src` values after renaming.

---

### 10.10 Path safety

Applications should prevent package paths from escaping the archive.

**Invalid path patterns:**
- `../`
- `..\`
- `/absolute/path`
- `C:\absolute\path`

**Invalid examples:**
- `../secrets.txt`
- `../../image.png`
- `/home/user/image.png`
- `C:\Users\User\image.png`

Applications should reject, sanitize, or rewrite unsafe paths during save/export.

---

### 10.11 Shared assets

The initial v3 convention is:
- Deck assets go under `assets/deck/`
- Card assets go under `assets/cards/<card_id>/`

A future version may define a shared asset folder, such as:
```text
assets/shared/
```

For v3, card-local assets are preferred because they make ownership clear and simplify export, deletion, copying, and editing.

Applications may preserve an existing `assets/shared/` folder if encountered, but v3 does not require shared asset support.

---

### 10.12 Package asset checklist

- [x] `deck.json` is required at root.
- [x] `assets/` is the standard asset folder.
- [x] `assets/deck/` stores cover and deck-level assets.
- [x] `assets/cards/<card_id>/` stores card-level assets.
- [x] All packaged `src` paths should be relative.
- [x] Packaged decks should not store absolute local paths.
- [x] App may temporarily use absolute paths while editing.
- [x] Save/export should ingest files and rewrite paths.

**Recommended examples:**
- [x] `assets/deck/cover.png`
- [x] `assets/cards/card_001/lative.mp3`
- [x] `assets/cards/card_001/illustration.png`
- [x] `assets/cards/card_002/heart.png`

