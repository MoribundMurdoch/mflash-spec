# mflash File Format v1 Specification

**Status:** Draft  
**Format version:** 1  
**Container:** UTF-8 JSON text file ending in `.mflash`  
**Reference implementation:** MorFlash (Rust)

---

# 1. Overview

mflash is a human-readable, multilingual-friendly flashcard format.

- UTF-8 text (full Unicode)
- Per-card language metadata
- Media support via relative paths
- Tags, notes, examples, hyperlinks
- Deck-level defaults with per-card overrides

---

# 2. Encoding

A `.mflash` file MUST:

- Be valid UTF-8  
- Contain a single JSON object  
- Have `"format": "mflash"`  
- Have `"version": 1`

All strings may contain:

- Cyrillic  
- CJK (Chinese, Japanese, Korean)  
- Greek  
- Georgian  
- Emoji  
- Accents, IPA  
- Any Unicode codepoints

---

# 3. Deck Structure (MflashDeck)

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
