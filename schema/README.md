# mflash Schemas

This folder contains JSON Schemas for mflash deck files.

## Versioned schemas

mflash-v2-schema.json
mflash-v3-schema.json

Versioned schemas are stable references for specific mflash versions.

Generic schema
mflash-schema.json

The generic schema may point to the latest stable mflash version.

While mflash v3 is in draft, mflash-schema.json may continue to represent the latest stable v2 schema. Once v3 is stable, it may be updated to mirror or reference mflash-v3-schema.json.

mflash v3

mflash v3 introduces:

- version: 3
- UUID-based deck/card/media/example/mask ids
- typed cards using kind
- structured deck cover metadata
- standardized media objects
- lexical metadata for etymology and morphology
- pronunciation audio roles
- image occlusion cards
- package assets under assets/
- namespaced extensions objects for plugins and experiments

## 11.5 Add v3 examples

Create a basic deck example:

{
  "format": "mflash",
  "version": 3,
  "id": "6ac16ce2-e1bf-4cc7-9a3e-575dd9462c3b",
  "title": "Philological & Lexicographical Sample Deck",
  "description": "A showcase of mflash v3 features including lexical metadata, UUIDs, and namespaced extensions.",
  "snippet": "Exploring Latin neologisms and suckless philosophy.",
  "created_at": "2026-05-12T09:33:11.609598Z",
  "updated_at": "2026-05-12T09:33:11.609876Z",
  "default_term_lang": "la-Latn",
  "default_def_lang": "en-US",
  "deck_tags": [
    "linguistics",
    "latin",
    "minimalism"
  ],
  "cards": [
    {
      "id": "47904746-c70e-45a0-ace0-3281ada93389",
      "kind": "basic",
      "term": "mendaciarium",
      "definition": "A treasury or collection of lies; a place where lies are kept.",
      "term_lang": "la-Latn",
      "def_lang": "en-US",
      "phonetic": "/men.da.ki.'a\u02d0.ri.um/",
      "part_of_speech": "noun",
      "lexical": {
        "etymology": "Derived from Latin 'mendax' (liar) + '-arium' (receptacle/place for).",
        "morphology": [
          {
            "form": "mendax",
            "type": "root",
            "meaning": "lying, false",
            "lang": "la-Latn"
          },
          {
            "form": "-arium",
            "type": "suffix",
            "meaning": "place for, collection of",
            "lang": "la-Latn"
          }
        ],
        "ipa": "/mendaki\u02c8a\u02d0rium/",
        "register": "literary/neologism",
        "usage_note": "Commonly used in philosophical contexts to describe structured misinformation."
      },
      "media": [
        {
          "id": "f938e0b3-a481-49a5-bf7d-e912edce4d3a",
          "type": "audio",
          "role": "term_pronunciation",
          "src": "assets/audio/mendaciarium_pron.mp3",
          "lang": "la-Latn"
        }
      ],
      "examples": [
        {
          "id": "9ada495c-2141-47e0-b2e9-174cc7e7487a",
          "text": "In hoc mendaciario nihil veri invenies.",
          "translation": "In this treasury of lies, you will find nothing of the truth.",
          "lang": "la-Latn",
          "translation_lang": "en-US"
        }
      ],
      "extensions": {
        "dev.mflash.philology": {
          "certainty_score": 0.95,
          "attestation": "Classical hypothetical"
        }
      }
    },
    {
      "id": "d478e055-7ecb-44fb-8a19-13cf921b6d68",
      "kind": "basic",
      "term": "Suckless",
      "definition": "A philosophy of software development that values simplicity, clarity, and frugality.",
      "term_lang": "en-US",
      "def_lang": "en-US",
      "tags": [
        "software",
        "philosophy"
      ],
      "notes": "Think 'dwm', 'st', and minimalist C code.",
      "extensions": {
        "com.example.plugin": {
          "priority_level": "high",
          "render_mode": "compact"
        }
      }
    }
  ],
  "extensions": {
    "org.mflash.app": {
      "last_viewed_card": null,
      "custom_theme": "gruvbox-dark"
    }
  }
}
Validation

Validate a raw v3 deck JSON file:

```bash
python scripts/validate.py examples/v3-basic-deck/deck.json schema/mflash-v3-schema.json

Validate a raw v3 deck and check referenced assets exist:

python scripts/validate.py examples/v3-basic-deck/deck.json schema/mflash-v3-schema.json --check-assets

Validate a packaged .mflash file:

python scripts/validate_package.py path/to/deck.mflash

Validate all v3 examples:

python scripts/validate_examples.py