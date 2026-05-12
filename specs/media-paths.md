# mflash Media Path Rules

**Status:** Draft  
**Applies to:** Raw `.mflash.json` decks and packaged `.mflash` decks

## Overview

mflash decks may reference media such as images, audio, video, GIFs, and other assets.

Media path behavior depends on whether the deck is a raw `.mflash.json` file or a packaged `.mflash` archive.

## Media in raw `.mflash.json` files

In raw `.mflash.json` files, media paths MAY be:

- relative paths
- absolute filesystem paths, if the application supports them
- URLs, if the application supports them

Applications SHOULD prefer relative paths for portability.

Example:

```json
{
  "type": "image",
  "src": "media/card_001.png",
  "alt": "An example image."
}

Relative paths SHOULD be resolved relative to the .mflash.json file location.

Media in packaged .mflash files

In packaged .mflash files, media paths SHOULD be relative package paths.

Example:

{
  "type": "audio",
  "src": "media/card_001-audio.mp3",
  "description": "Pronunciation audio."
}

Packaged decks SHOULD NOT use absolute filesystem paths.

Readers SHOULD resolve packaged media paths relative to the package root.

Cover media

Raw deck example:

"cover_media": "cover.png"

Packaged deck example:

"cover_media": "media/cover.png"
URL media

Applications MAY support remote media URLs.

Applications SHOULD NOT fetch remote media automatically without user consent.

Remote media may affect privacy by revealing when a deck is opened or studied.

Legacy string media

Readers MAY support legacy/simple string media:

"media": "media/card_001.png"

Writers SHOULD prefer structured media arrays:

"media": [
  {
    "type": "image",
    "src": "media/card_001.png",
    "alt": "An example image."
  }
]
Media type values

Recommended media type values:

image
audio
video
gif
other
Path safety

Readers MUST treat media paths as untrusted input.

Readers MUST protect against:

path traversal
unsafe absolute paths
unexpected archive extraction paths
remote URL fetching without user consent
Missing media

Readers SHOULD continue loading a deck even if optional media is missing.

The UI SHOULD display a graceful placeholder, warning, or nothing, depending on application design.

Missing media SHOULD NOT make an otherwise valid deck unloadable.
