# Roadmap
## mflash v3 Roadmap

mflash v3 expands the format beyond basic term-definition cards.

### Format

- [x] JSON-first deck format
- [x] Packaged `.mflash` files as ZIP archives
- [x] `deck.json` at package root
- [x] `assets/` package layout
- [x] deck-level and card-level asset separation
- [x] typed cards using `kind`
- [x] structured media objects
- [x] structured deck cover object
- [x] polyglot language fallback rules
- [x] pronunciation audio roles
- [x] image occlusion object
- [x] extensions object for plugins and experiments
- [x] UUID-formatted IDs

#### Schema
- [x] Create `schema/mflash-v3-schema.json`
- [x] Preserve `schema/mflash-v2-schema.json`
- [ ] Keep `schema/mflash-schema.json` on stable v2 until v3 is stable
- [ ] Add package validator
- [ ] Add example validation workflow

#### Examples
- [x] v3 basic deck example
- [x] v3 image occlusion example
- [ ] v3 pronunciation audio example
- [ ] v3 media prompt example
- [ ] v3 polyglot deck example

#### Tooling
- [x] v2-to-v3 migration script
- [ ] package validation script
- [ ] asset existence checks
- [ ] UUID validation checks
- [ ] no absolute paths in packaged deck checks

#### App support
- [ ] Load v2 decks
- [ ] Load v3 decks
- [ ] Save v3 decks
- [ ] Migrate v2 decks to v3
- [ ] Deck cover editor uses v3 cover object
- [ ] Card editor supports `kind: basic`
- [ ] Card editor supports pronunciation audio
- [ ] Card editor supports image occlusion
## Current focus

- Define mflash v2.
- Keep v1 documented for migration.
- Separate study progress from deck content.
- Provide schemas, examples, and validation tools.

## Planned

- Better schema validation scripts.
- v1-to-v2 migration script.
- Packaged `.mflash` archive rules.
- Package manifest schema.
- Invalid examples for validator testing.
- Diagrams for loading and progress separation.

## Not standardized yet

- Specific spaced-repetition algorithms.
- Rich card layout systems.
- Plugin metadata conventions.
- Cloud sync behavior.
