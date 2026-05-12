# mflash Package Layout

**Status:** Draft  
**Applies to:** Packaged `.mflash` decks

## Overview

A packaged `.mflash` file is a ZIP-style archive containing a required `deck.json` file and optional bundled assets.

The packaged format is intended for sharing, importing, bundled media, file-manager previews, and normal application use.

Raw `.mflash.json` files remain the preferred format for hand-editing, scripts, Git repositories, and debugging.

## Required package contents

A packaged `.mflash` archive MUST contain:

```text
deck.json

deck.json MUST be located at the package root.

deck.json MUST be valid UTF-8 JSON.

deck.json MUST conform to the current mflash deck schema for its declared version.

For mflash v2, deck.json MUST include:

{
  "format": "mflash",
  "version": 2,
  "id": "deck_example",
  "title": "Example Deck",
  "cards": []
}
Optional package contents

A packaged .mflash archive MAY contain:

manifest.json
cover.png
media/

Example package:

my-deck.mflash
├── deck.json
├── manifest.json
├── cover.png
└── media/
    ├── card_001-image.png
    ├── card_001-audio.mp3
    └── card_002-video.mp4
manifest.json

manifest.json is optional.

When present, it SHOULD contain package-level metadata about the archive itself, not deck content.

Deck content belongs in deck.json.

Study progress belongs in a separate progress file, not inside the packaged deck by default.

Media directory

Bundled media SHOULD be placed under:

media/

This is recommended, not required.

Deck media references SHOULD use relative package paths:

"src": "media/card_001-audio.mp3"
Cover media

If deck.json includes cover_media, it SHOULD reference a relative package path:

"cover_media": "cover.png"

or:

"cover_media": "media/cover.png"
Path safety

Packaged decks MUST NOT rely on absolute filesystem paths.

Readers MUST protect against path traversal.

Readers MUST reject or sanitize unsafe paths such as:

../outside-file
../../secret
/home/user/file.png
C:\Users\Name\file.png

Package extraction MUST NOT write files outside the intended extraction directory.

Reader behavior

Readers MUST reject packages that do not contain a valid root-level deck.json.

Readers SHOULD ignore unknown package files.

Readers SHOULD load .mflash.json and .mflash into the same normalized in-memory deck object.

Writer behavior

Writers SHOULD create packages with a root-level deck.json.

Writers SHOULD use relative paths for bundled assets.

Writers SHOULD avoid including user-specific progress, local cache files, or private app state in packaged decks.
