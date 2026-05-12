# mflash Validation Rules

**Status:** Draft

## Overview

mflash validation happens at two levels:

1. JSON validation
2. Format/schema validation

For packaged `.mflash` files, validation has an additional package layer.

## Raw deck validation

A raw `.mflash.json` deck is valid when:

- the file is valid UTF-8
- the file contains one top-level JSON object
- the object contains `"format": "mflash"`
- the object declares a supported `version`
- the object conforms to the schema for that version

For mflash v2, the deck MUST include:

```text
format
version
id
title
cards

Each card MUST include:

id
term
definition
Packaged deck validation

A packaged .mflash deck is valid when:

the archive can be opened safely
the archive contains a root-level deck.json
deck.json is valid UTF-8
deck.json contains one top-level JSON object
deck.json conforms to the schema for its declared version
packaged media paths do not require unsafe absolute paths or path traversal
Progress validation

An mflash progress file is valid when it conforms to schema/mflash-progress-v1.schema.json.

A progress file MUST include:

format
version
deck_id
cards

The deck_id SHOULD match the id of the deck it belongs to.

Progress card keys SHOULD match card IDs from the deck.

Current schemas

Current/latest deck schema:

schema/mflash-schema.json

Explicit mflash v2 schema:

schema/mflash-v2.schema.json

Legacy mflash v1 schema:

schema/mflash-v1.schema.json

Progress schema:

schema/mflash-progress-v1.schema.json
Unknown fields

Readers SHOULD ignore unknown fields.

Writers SHOULD preserve unknown fields when practical.

Unknown fields SHOULD NOT make a deck invalid unless they conflict with required core fields.

Optional fields

Optional fields may be absent.

Applications MUST NOT require optional fields such as:

created_at
updated_at
description
snippet
cover_media
default_term_lang
default_def_lang
deck_tags
media
examples
notes
tags
hyperlink
Privacy validation

A deck with no created_at or updated_at is valid.

Anonymous sharing decks SHOULD be valid without timestamps.

Recommended validation commands

Check JSON syntax:

python -m json.tool schema/mflash-schema.json > /tmp/mflash-schema-check.json

Validate examples using the repository script:

python scripts/validate_examples.py

