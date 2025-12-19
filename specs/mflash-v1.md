# mflash File Format v1 Specification

**Status:** Draft  
**Format version:** 1  
**Container:** UTF-8 JSON text file ending in `.mflash`  
**Reference implementation:** MorFlash (Rust)

---

## 1. Overview

mflash is a human-readable, multilingual-friendly flashcard file format.

Design goals:

- UTF-8 text with full Unicode support
- Per-card language metadata with deck-level defaults
- Media references via relative paths (no embedded binaries)
- Optional tags, examples, hyperlinks, and notes
- Simple JSON structure suitable for manual editing and version control

The format is intended to be UI-agnostic and forward-compatible.

---

## 2. File Encoding and Container

A `.mflash` file MUST:

- Be valid UTF-8
- Contain exactly one JSON object at the top level
- Include `"format": "mflash"`
- Include `"version": 1`

All string fields MAY contain arbitrary Unicode text, including (but not limited to):

- Latin, Cyrillic, Greek, Georgian
- CJK scripts (Chinese, Japanese, Korean)
- Accents, IPA symbols
- Emoji

Implementations MUST NOT assume ASCII-only content.

Unknown or unsupported fields SHOULD be ignored to allow forward compatibility with future versions.

---

## 3. Deck Structure (`MflashDeck`)

The top-level JSON object represents a deck.

```jsonc
{
  "format": "mflash",
  "version": 1,

  "title": "Demo Deck",
  "description": "Multilingual sample deck.",
  "snippet": "A demonstration of mflash v1.",

  "default_term_lang": "en",
  "default_def_lang": "fr",

  "deck_tags": ["languages", "demo"],
  "cover_media": "cover.png",

  "cards": []
}
````

### Field semantics

* `title`
  Human-readable deck name.

* `description`
  Optional longer description of the deck.

* `snippet`
  Optional short preview text for UIs (file pickers, lists).

* `default_term_lang`, `default_def_lang`
  Optional language codes applied when a card does not specify its own language.
  Language codes SHOULD follow BCP-47 (e.g. `en`, `fr`, `ja-JP`, `zh-Hans`).

* `deck_tags`
  Optional deck-level tags for categorization.

* `cover_media`
  Optional relative path to a cover or thumbnail image.

* `cards`
  Array of card objects (`MflashCard`).

If a card omits `term_lang` or `def_lang`, the corresponding deck-level default is used.
