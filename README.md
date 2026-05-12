# mflash

Rust library for reading and writing **mflash** flashcard deck files.

Moribund Flash supports two related deck representations:

1. `.mflash.json` — a raw UTF-8 JSON deck file.
2. `.mflash` — a packaged deck archive containing `deck.json` and optional bundled media assets.

A `.mflash.json` file is the source/editable/plain representation of a deck. It is intended for developers, deck builders, Git repositories, scripts, and direct editing.

A `.mflash` file is the portable packaged representation of a deck. It is intended for sharing, importing, bundled media, cover previews, and normal application use.

The deck data itself remains:

- UTF-8 JSON
- Unicode-native (CJK, Cyrillic, Georgian, emoji, etc.)
- Designed for multilingual decks with per-card language metadata
- Flexible enough to omit unused optional fields

In raw form, the deck JSON is stored directly in a `.mflash.json` file.

In packaged form, the deck JSON is stored as `deck.json` inside a `.mflash` archive.

This crate follows the [`mflash-spec`](https://github.com/your-user-or-org/mflash-spec) v1 specification.

## mflash v3 Draft

mflash v3 is the next major version of the mflash study deck format.

It expands mflash from a term-definition flashcard format into a more versatile study deck format with typed cards, organized packaged assets, polyglot language metadata, pronunciation audio, and image occlusion.

Core v3 changes:

```text
- Decks still use deck.json as the source of truth.
- Packaged .mflash files are ZIP archives.
- deck.json lives at the archive root.
- Assets live under assets/.
- Deck assets live under assets/deck/.
- Card assets live under assets/cards/<card_id>/.
- Cards now require kind.
- term and definition are no longer globally required for every card.
- Basic flashcards use kind: "basic".
- Media objects are structured and reusable.
- Deck cover metadata uses a structured cover object.
- Pronunciation audio is supported through media roles.
- Image occlusion is supported through kind: "image_occlusion".
- Polyglot deck/card/media language support remains.
- Unknown extra fields and extensions may be preserved for forward compatibility.
```

Example v3 deck header:

```json
{
  "format": "mflash",
  "version": 3,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Example Deck",
  "cards": []
}
```

See:

- `specs/mflash-v3.md`
- `schema/mflash-v3-schema.json`
- `examples/v3-basic-deck/`
- `examples/v3-image-occlusion/`

mflash v3 is currently draft unless otherwise noted.

## Deck representations

### Raw developer format

```text
my-deck.mflash.json
```

A `.mflash.json` file is a UTF-8 JSON document conforming to the mflash deck schema.

This format is good for hand-editing, scripts, version control, generated decks, and debugging.

### Packaged user format

```text
my-deck.mflash
```

A `.mflash` file is a ZIP-style archive with a required `deck.json` file at the package root.

Example package layout:

```text
my-deck.mflash
├── deck.json
├── cover.png
└── media/
    ├── card-001-image.png
    ├── card-002-video.mp4
    ├── card-003-animation.gif
    └── card-004-audio.mp3
```

The `deck.json` file inside a `.mflash` package MUST conform to the same mflash deck schema used by `.mflash.json` files.

Readers SHOULD treat `.mflash.json` and `.mflash` as equivalent after loading, producing the same normalized in-memory deck object.

## Maximal deck example

This example intentionally enables most common optional fields.

Real decks do not need to fill out every field. Missing optional fields should simply display nothing in the app.

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
      "examples": [
        {
          "text": "Mul on täna halb soeng.",
          "translation": "I have bad hair today.",
          "lang": "et"
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
          "src": "media/card-004-audio.mp3",
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
          "lang": "et"
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
          "lang": "et"
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

## Optional fields

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

## Media paths

The `cover_media` field identifies the deck cover image or media item used for deck previews.

For `.mflash.json` files, `cover_media` MAY be a relative path, absolute path, or URL, depending on loader support.

For `.mflash` packages, `cover_media` SHOULD be a relative package path, such as:

```json
"cover_media": "cover.png"
```

or:

```json
"cover_media": "media/cover.png"
```

All media paths inside a `.mflash` package SHOULD be relative package paths.

Absolute filesystem paths SHOULD NOT be used inside packaged decks.

## Loading behavior

The app should load both formats into the same normalized deck object.

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

After loading, the study screen should not care where the deck came from.

```text
Study screen receives normalized deck object.
Study screen does not care whether the source was .mflash, .mflash.json, CSV, TSV, Anki, or another imported format.
```

## Rust example

```rust
use mflash::{read_from_path, write_to_path, MflashDeck, MflashCard, MflashMedia};

fn main() -> mflash::Result<()> {
    // Load a packaged deck
    let mut deck = read_from_path("examples/multiscript-demo.mflash")?;
    println!("Loaded deck: {} ({} cards)", deck.title, deck.cards.len());

    // Add a new card
    deck.cards.push(MflashCard {
        id: Some("card-004".into()),
        term: "Tere".into(),
        definition: "Hello".into(),
        term_lang: Some("et".into()),
        def_lang: Some("en".into()),
        phonetic: Some("TEH-reh".into()),
        part_of_speech: Some("interjection".into()),
        hyperlink: None,
        media: vec![
            MflashMedia {
                media_type: "audio".into(),
                src: "media/card-004-audio.mp3".into(),
                alt: None,
                description: Some("Pronunciation audio for Tere.".into()),
            }
        ],
        tags: vec!["greeting".into(), "estonian".into()],
        examples: vec!["Tere! Kuidas läheb? → Hello! How is it going?".into()],
        notes: Some("Basic Estonian greeting.".into()),
    });

    // Save it back out
    write_to_path(&deck, "examples/multiscript-demo-updated.mflash")?;
    Ok(())
}
```

> Note: the Rust structs should track the schema. If `phonetic`, `part_of_speech`, `id`, or structured media fields are not implemented yet, add them to the Rust model before using this exact example as compiling code.

## Current format status

mflash v2 is the current deck format.

mflash v1 remains documented as a legacy format for compatibility and migration. Applications SHOULD be able to load v1 decks, normalize them, and save newly written decks as v2.

mflash v2 requires stable deck and card IDs:

- deck-level `id`
- card-level `id`

`created_at` and `updated_at` are optional so decks can be shared anonymously without unnecessary timestamp metadata.

Study progress is stored separately using the `mflash-progress` format.

## Key specs

- `specs/mflash-v3.md` — draft format
- `specs/mflash-v2.md` — current deck format
- `specs/mflash-progress-v1.md` — separate study progress format
- `specs/ids.md` — deck and card ID guidance
- `specs/compatibility.md` — reader/writer compatibility behavior
- `specs/package-layout.md` — packaged `.mflash` archive layout
- `specs/media-paths.md` — raw and packaged media path rules
- `specs/validation.md` — validation behavior

## Key schemas

- `schema/mflash-schema.json` — current/latest deck schema
- `schema/mflash-v3-schema.json` — draft mflash v3 deck schema
- `schema/mflash-v2.schema.json` — explicit mflash v2 deck schema
- `schema/mflash-v1.schema.json` — legacy mflash v1 deck schema
- `schema/mflash-progress-v1.schema.json` — progress file schema
- `schema/mflash-package-manifest-v1.schema.json` — optional package manifest schema