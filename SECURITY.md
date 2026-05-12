# Security and Privacy

mflash files may contain user-generated text, media paths, URLs, and packaged media assets.

## Privacy

`created_at` and `updated_at` are optional. Anonymous export tools SHOULD remove timestamps and other nonessential metadata when requested.

Deck IDs and card IDs SHOULD NOT contain usernames, emails, machine names, timestamps, or other personally identifying information.

## Packaged decks

Applications that read packaged `.mflash` archives MUST protect against archive path traversal.

Readers SHOULD reject or sanitize paths such as:

- `../outside-file`
- absolute filesystem paths
- platform-specific unsafe paths

## Remote URLs

Decks may reference remote URLs. Applications SHOULD avoid fetching remote content automatically without user consent.

## Media files

Applications SHOULD treat bundled media as untrusted input.
