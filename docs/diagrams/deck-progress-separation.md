# Deck and Progress Separation

mflash deck files store reusable learning content.

mflash progress files store user/app-specific study state.

```mermaid
flowchart TD
    A["mflash deck<br/>format: mflash<br/>version: 2"] --> B["Deck ID<br/>deck.id"]
    A --> C["Cards"]
    C --> D["Card ID<br/>card.id"]
    C --> E["Term"]
    C --> F["Definition"]
    C --> G["Examples / media / notes / tags"]

    H["mflash progress file<br/>format: mflash-progress<br/>version: 1"] --> I["deck_id"]
    H --> J["cards object"]
    J --> K["card_id key"]
    K --> L["review_count"]
    K --> M["due_at"]
    K --> N["ease"]
    K --> O["last_reviewed_at"]

    B -. "matches" .-> I
    D -. "keys progress entry" .-> K
Why separate them?

Deck content is shareable. Progress is personal.

Keeping them separate makes it easier to:

share decks anonymously
keep clean Git diffs
support multiple users studying the same deck
support multiple scheduling systems
avoid mutating deck files every time someone studies
