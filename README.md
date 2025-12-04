# mflash

Rust library for reading and writing **.mflash** flashcard deck files.

The `.mflash` format is:

- UTF-8 JSON
- Unicode-native (CJK, Cyrillic, Georgian, emoji, etc.)
- Designed for multilingual decks with per-card language metadata

This crate follows the [`mflash-spec`](https://github.com/your-user-or-org/mflash-spec) v1 specification.

## Example

```rust
use mflash::{read_from_path, write_to_path, MflashDeck, MflashCard};

fn main() -> mflash::Result<()> {
    // Load a deck
    let mut deck = read_from_path("examples/multiscript-demo.mflash")?;
    println!("Loaded deck: {} ({} cards)", deck.title, deck.cards.len());

    // Add a new card
    deck.cards.push(MflashCard {
        term: "Hello".into(),
        definition: "გამარჯობა".into(),
        term_lang: Some("en".into()),
        def_lang: Some("ka".into()),
        hyperlink: None,
        media: None,
        tags: vec!["greeting".into()],
        examples: vec!["Hello → გამარჯობა".into()],
        notes: None,
    });

    // Save it back out
    write_to_path(&deck, "examples/multiscript-demo-updated.mflash")?;
    Ok(())
}
