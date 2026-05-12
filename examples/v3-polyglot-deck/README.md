# mflash v3 Polyglot Example

This example demonstrates language fallback behavior.

It covers:

- deck-level `default_term_lang`
- deck-level `default_def_lang`
- card-level `term_lang`
- card-level `def_lang`
- media-level `lang`
- example `lang`
- example `translation_lang`

The first card inherits the deck languages:

```text
term language: fr-FR
definition language: en-US

The second card overrides the term language:

term language: de-DE
definition language: en-US

Referenced audio paths:

assets/cards/550e8400-e29b-41d4-a716-446655480001/bonjour.mp3
assets/cards/550e8400-e29b-41d4-a716-446655480002/weltanschauung.mp3

A real package should include those files.
