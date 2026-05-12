# mflash v3 Basic Deck Example

This example demonstrates a basic mflash v3 term-definition deck.

It covers:

- `version: 3`
- `kind: "basic"`
- deck-level language defaults
- card-level term and definition fields
- lexical metadata
- deck cover metadata using `cover`
- deck assets under `assets/deck/`

The referenced cover image path is:

```text
assets/deck/cover.png

A real package should include that file.


---

# 13.2 `examples/v3-pronunciation-audio/`

Create:

```bash
mkdir -p examples/v3-pronunciation-audio/assets/deck
mkdir -p examples/v3-pronunciation-audio/assets/cards/550e8400-e29b-41d4-a716-446655450001
nano examples/v3-pronunciation-audio/deck.json

Paste:

{
  "format": "mflash",
  "version": 3,
  "id": "550e8400-e29b-41d4-a716-446655450000",
  "title": "mflash v3 Pronunciation Audio Example",
  "description": "A deck showing uploaded pronunciation audio for a basic card.",
  "snippet": "Pronunciation audio example.",
  "default_term_lang": "fr-FR",
  "default_def_lang": "en-US",
  "deck_tags": ["example", "audio", "pronunciation", "french"],
  "cover": {
    "id": "550e8400-e29b-41d4-a716-446655450010",
    "type": "image",
    "role": "cover",
    "src": "assets/deck/cover.png",
    "alt": "Pronunciation audio example cover"
  },
  "cards": [
    {
      "id": "550e8400-e29b-41d4-a716-446655450001",
      "kind": "basic",
      "term": "bonjour",
      "definition": "hello",
      "term_lang": "fr-FR",
      "def_lang": "en-US",
      "media": [
        {
          "id": "550e8400-e29b-41d4-a716-446655450020",
          "type": "audio",
          "role": "term_pronunciation",
          "src": "assets/cards/550e8400-e29b-41d4-a716-446655450001/bonjour.mp3",
          "lang": "fr-FR"
        },
        {
          "id": "550e8400-e29b-41d4-a716-446655450021",
          "type": "audio",
          "role": "definition_pronunciation",
          "src": "assets/cards/550e8400-e29b-41d4-a716-446655450001/hello.mp3",
          "lang": "en-US"
        }
      ],
      "examples": [
        {
          "id": "550e8400-e29b-41d4-a716-446655450030",
          "text": "Bonjour, comment ça va ?",
          "translation": "Hello, how are you?",
          "lang": "fr-FR",
          "translation_lang": "en-US",
          "media": [
            {
              "id": "550e8400-e29b-41d4-a716-446655450031",
              "type": "audio",
              "role": "example_audio",
              "src": "assets/cards/550e8400-e29b-41d4-a716-446655450001/example_001.mp3",
              "lang": "fr-FR"
            }
          ]
        }
      ]
    }
  ]
}
