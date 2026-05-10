# mflash File Format v1 Specification

**Status:** Draft  
**Format version:** 1  
**Deck schema:** mflash v1  
**Raw deck extension:** `.mflash.json`  
**Packaged deck extension:** `.mflash`  
**Reference implementation:** MorFlash / Moribund Flash

---

## 1. Overview

mflash is a multilingual-friendly flashcard deck format designed for Moribund Flash and compatible tools.

Moribund Flash supports two related deck representations:

1. `.mflash.json` — a raw UTF-8 JSON deck file.
2. `.mflash` — a ZIP-style packaged deck archive containing `deck.json` and optional bundled media assets.

The deck data itself is UTF-8 JSON and uses the same mflash v1 deck schema in both representations.

Design goals:

- UTF-8 deck data with full Unicode support
- Unicode-native content, including CJK, Cyrillic, Greek, Georgian, IPA, emoji, and other scripts
- Per-card language metadata with deck-level defaults
- Optional card metadata such as phonetic text, part of speech, examples, notes, tags, hyperlinks, and media
- Human-editable raw JSON files for developers, deck builders, scripts, and Git repositories
- Portable packaged deck files for normal app use, sharing, importing, bundled media, and file-manager previews
- UI-agnostic and forward-compatible data shape

Unknown or unsupported fields SHOULD be ignored to allow forward compatibility with future versions.

---

## 2. Deck Representations

### 2.1 Raw developer format: `.mflash.json`

A `.mflash.json` file is a UTF-8 JSON document conforming to the mflash v1 deck schema.

Example filename:

```text
my-deck.mflash.json
```

A `.mflash.json` file is intended for:

- hand-editing
- scripts
- version control
- generated decks
- debugging
- direct schema inspection

A `.mflash.json` file MUST:

- be valid UTF-8
- contain exactly one JSON object at the top level
- include `"format": "mflash"`
- include `"version": 1`
- conform to the mflash v1 deck schema

### 2.2 Packaged user format: `.mflash`

A `.mflash` file is a ZIP-style archive containing a required `deck.json` file at the package root.

Example filename:

```text
my-deck.mflash
```

Example package layout:

```text
my-deck.mflash
├── deck.json
├── cover.png
└── media/
    ├── card-001-image.png
    ├── card-001-audio.mp3
    ├── card-002-video.mp4
    └── card-003-animation.gif
```

The `deck.json` file inside a `.mflash` package MUST:

- be valid UTF-8
- contain exactly one JSON object at the top level
- include `"format": "mflash"`
- include `"version": 1`
- conform to the same mflash v1 deck schema used by `.mflash.json` files

A `.mflash` package MUST contain a valid `deck.json` file at the package root.

A `.mflash` package MAY contain bundled media assets.

Readers MUST reject packages that do not contain a valid `deck.json` file.

Readers SHOULD treat `.mflash.json` and `.mflash` as equivalent after loading, producing the same normalized in-memory deck object.

---

## 3. Unicode and Encoding

All deck JSON data MUST be valid UTF-8.

All string fields MAY contain arbitrary Unicode text, including but not limited to:

- Latin
- Cyrillic
- Greek
- Georgian
- CJK scripts
- accents and diacritics
- IPA symbols
- emoji

Implementations MUST NOT assume ASCII-only content.

---

## 4. Deck Structure (`MflashDeck`)

The top-level JSON object represents a deck.

```jsonc
{
  "format": "mflash",
  "version": 1,

  "title": "Bad Hair Ahaha",
  "description": "A very serious multilingual deck about hair whatnot.",
  "snippet": "Hair, language, and assorted follicular situations.",

  "default_term_lang": "et",
  "default_def_lang": "en",

  "deck_tags": ["estonian", "english", "hair", "example-deck"],
  "cover_media": "cover.png",

  "cards": []
}
```

### 4.1 Required deck fields

#### `format`

Must be the string `"mflash"`.

#### `version`

Must be the integer `1`.

#### `title`

Human-readable deck name.

#### `cards`

Array of card objects.

### 4.2 Optional deck fields

#### `description`

Longer human-readable description of the deck.

#### `snippet`

Short preview text for UIs, deck lists, file pickers, and search results.

#### `default_term_lang`

Default language code for card terms when a card does not specify `term_lang`.

#### `default_def_lang`

Default language code for card definitions when a card does not specify `def_lang`.

Language codes SHOULD follow BCP-47, such as:

```text
en
et
fr
ja-JP
zh-Hans
```

#### `deck_tags`

Deck-level tags for categorization.

If absent, readers SHOULD treat this as an empty array.

#### `cover_media`

Path or reference to a deck cover image or preview media item.

For `.mflash.json` files, `cover_media` MAY be a relative path, absolute path, or URL, depending on loader support.

For `.mflash` packages, `cover_media` SHOULD be a relative package path, such as:

```json
"cover_media": "cover.png"
```

or:

```json
"cover_media": "media/cover.png"
```

Absolute filesystem paths SHOULD NOT be used inside packaged decks.

---

## 5. Card Structure (`MflashCard`)

Each item in `cards` represents one flashcard.

```jsonc
{
  "id": "card-001",
  "term": "halb soeng",
  "definition": "Bad hair; a follicular situation.",
  "term_lang": "et",
  "def_lang": "en",
  "phonetic": "HAHLB soh-eng",
  "part_of_speech": "noun phrase",
  "notes": "A useful phrase for describing a hair situation.",
  "hyperlink": "https://en.wiktionary.org/wiki/soeng",
  "examples": [
    {
      "text": "Mul on täna halb soeng.",
      "translation": "I have bad hair today.",
      "lang": "et",
      "translation_lang": "en"
    }
  ],
  "media": [
    {
      "type": "image",
      "src": "media/card-001-image.png",
      "alt": "A blue-tinted illustration of chaotic bad hair."
    }
  ],
  "tags": ["hair", "appearance", "estonian"]
}
```

### 5.1 Required card fields

#### `term`

The prompt, front-side text, or source-language item.

#### `definition`

The answer, back-side text, explanation, or target-language item.

### 5.2 Optional card fields

#### `id`

Stable card identifier.

Card IDs are useful for media naming, progress tracking, syncing, and future review history.

#### `term_lang`

Language code for the term.

If absent, readers SHOULD use the deck-level `default_term_lang` when available.

#### `def_lang`

Language code for the definition.

If absent, readers SHOULD use the deck-level `default_def_lang` when available.

#### `phonetic`

Optional pronunciation, phonetic spelling, IPA, romanization, or reading helper.

Examples:

```json
"phonetic": "HAHLB soh-eng"
```

```json
"phonetic": "/ˈhælb ˈsoʊ.eŋ/"
```

#### `part_of_speech`

Optional grammatical label, such as:

```text
noun
verb
adjective
interjection
noun phrase
idiom
```

#### `notes`

Optional longer note, usage explanation, warning, or mnemonic.

#### `hyperlink`

Optional URL associated with the card.

#### `examples`

Optional array of examples.

Readers SHOULD support legacy string examples:

```json
"examples": [
  "Tere! Kuidas läheb? → Hello! How is it going?"
]
```

Readers SHOULD also support structured example objects:

```json
"examples": [
  {
    "text": "Mul on täna halb soeng.",
    "translation": "I have bad hair today.",
    "lang": "et",
    "translation_lang": "en"
  }
]
```

Structured example object fields:

- `text`: example sentence or phrase
- `translation`: optional translation
- `lang`: optional language code for the example text
- `translation_lang`: optional language code for the translation

#### `media`

Optional media reference or array of media objects.

For backwards compatibility, readers MAY support a single string media path:

```json
"media": "media/card-001-image.png"
```

Preferred structured media format:

```json
"media": [
  {
    "type": "image",
    "src": "media/card-001-image.png",
    "alt": "A blue-tinted illustration of chaotic bad hair."
  }
]
```

Supported media object fields:

- `type`: media type
- `src`: media path or URL
- `alt`: optional alt text for visual media
- `description`: optional description for audio, video, or other media

Recommended media type values:

```text
image
audio
video
gif
other
```

#### `tags`

Optional card-level tags.

If absent, readers SHOULD treat this as an empty array.

---

## 6. Optional Field Behavior

Deck readers SHOULD tolerate missing optional fields.

If an optional field is absent, empty, or unsupported by the current app view, the reader SHOULD continue loading the deck and the UI SHOULD simply display nothing for that field.

Common optional card fields include:

```text
id
term_lang
def_lang
phonetic
part_of_speech
notes
examples
media
tags
hyperlink
```

Common optional deck fields include:

```text
description
snippet
default_term_lang
default_def_lang
deck_tags
cover_media
```

---

## 7. Media Path Rules

Media paths are interpreted differently depending on deck representation.

### 7.1 Media paths in `.mflash.json`

For raw `.mflash.json` files, media paths MAY be:

- relative paths resolved from the `.mflash.json` file location
- absolute filesystem paths, if supported by the application
- URLs, if supported by the application

Applications SHOULD prefer relative paths for portability.

### 7.2 Media paths in `.mflash`

For packaged `.mflash` files, media paths SHOULD be relative package paths.

Examples:

```json
"cover_media": "cover.png"
```

```json
"src": "media/card-001-image.png"
```

Absolute filesystem paths SHOULD NOT be used inside packaged decks.

Readers SHOULD resolve packaged media paths relative to the package root.

---

## 8. Loading Behavior

Applications SHOULD load both deck representations into the same normalized deck object.

```text
Open .mflash.json
  -> parse JSON
  -> resolve external media paths relative to file location
  -> normalize deck

Open .mflash
  -> open package archive
  -> parse deck.json
  -> resolve media paths inside package
  -> normalize deck
```

After loading, study mode SHOULD NOT care where the deck came from.

```text
Study screen receives normalized deck object.
Study screen does not care whether the source was .mflash, .mflash.json, CSV, TSV, Anki, or another imported format.
```

Importers for CSV, TSV, Anki, or other formats SHOULD be separate from study mode.

---

## 9. Maximal Example

This example intentionally enables most common optional fields.

Real decks do not need to fill out every field.

Missing optional fields should simply display nothing in the app.

```json
{
  "format": "mflash",
  "version": 1,
  "title": "Bad Hair Ahaha",
  "description": "A very serious multilingual deck about hair whatnot.",
  "snippet": "Hair, language, and assorted follicular situations.",
  "default_term_lang": "et",
  "default_def_lang": "en",
  "deck_tags": ["estonian", "english", "hair", "example-deck"],
  "cover_media": "cover.png",
  "cards": [
    {
      "id": "card-001",
      "term": "halb soeng",
      "definition": "Bad hair; a follicular situation.",
      "term_lang": "et",
      "def_lang": "en",
      "phonetic": "HAHLB soh-eng",
      "part_of_speech": "noun phrase",
      "notes": "A useful phrase for describing the sort of hair situation that has become everybody else's business.",
      "hyperlink": "https://en.wiktionary.org/wiki/soeng",
      "examples": [
        {
          "text": "Mul on täna halb soeng.",
          "translation": "I have bad hair today.",
          "lang": "et",
          "translation_lang": "en"
        }
      ],
      "media": [
        {
          "type": "image",
          "src": "media/card-001-image.png",
          "alt": "A blue-tinted illustration of chaotic bad hair."
        },
        {
          "type": "audio",
          "src": "media/card-001-audio.mp3",
          "description": "Pronunciation audio for halb soeng."
        }
      ],
      "tags": ["hair", "appearance", "estonian"]
    },
    {
      "id": "card-002",
      "term": "juuksed",
      "definition": "Hair.",
      "term_lang": "et",
      "def_lang": "en",
      "phonetic": "YOO-ksehd",
      "part_of_speech": "noun",
      "notes": "General word for hair.",
      "examples": [
        {
          "text": "Tema juuksed on pikad.",
          "translation": "Their hair is long.",
          "lang": "et",
          "translation_lang": "en"
        }
      ],
      "media": [
        {
          "type": "video",
          "src": "media/card-002-video.mp4",
          "description": "Short video showing hair movement."
        }
      ],
      "tags": ["body", "estonian"]
    },
    {
      "id": "card-003",
      "term": "soeng",
      "definition": "Hairstyle.",
      "term_lang": "et",
      "def_lang": "en",
      "phonetic": "SOH-eng",
      "part_of_speech": "noun",
      "notes": "Useful for talking about styled hair rather than hair in general.",
      "examples": [
        {
          "text": "See soeng on väga dramaatiline.",
          "translation": "This hairstyle is very dramatic.",
          "lang": "et",
          "translation_lang": "en"
        }
      ],
      "media": [
        {
          "type": "gif",
          "src": "media/card-003-animation.gif",
          "alt": "Animated hairstyle transformation."
        }
      ],
      "tags": ["hair", "style", "estonian"]
    }
  ]
}
```

---

## 10. Validation

The canonical schema for mflash v1 deck JSON is `schema/mflash-schema.json`.

The schema applies to:

- raw `.mflash.json` files
- `deck.json` inside packaged `.mflash` files

A packaged `.mflash` file itself is validated in two layers:

1. Package validation: the archive contains a valid root-level `deck.json`.
2. Deck validation: `deck.json` conforms to the mflash v1 JSON schema.

---

## 11. Forward Compatibility

Readers SHOULD ignore unknown fields.

Writers SHOULD preserve unknown fields when practical.

Future versions MAY add additional fields, media metadata, scheduling metadata, study history, card types, or richer layout hints.

A v1 reader MUST NOT require optional fields to be present.
