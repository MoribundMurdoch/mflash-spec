# Raw `.mflash.json` vs Packaged `.mflash`

This diagram shows the two supported deck representations.

Raw `.mflash.json` files are best for development, scripts, Git, hand-editing, and debugging.

Packaged `.mflash` files are best for sharing, importing, bundled media, and user-facing app workflows.

```mermaid
flowchart TD
    A["Raw deck<br/>my-deck.mflash.json"] --> C["Parse JSON"]
    B["Packaged deck<br/>my-deck.mflash"] --> D["Open archive"]
    D --> E["Read root deck.json"]
    E --> C

    C --> F["Validate deck schema"]
    F --> G["Resolve media paths"]
    G --> H["Normalized deck object"]

    H --> I["Editor"]
    H --> J["Study mode"]
    H --> K["Export / package tools"]

    subgraph Raw_JSON["Raw .mflash.json"]
        A
    end

    subgraph Packaged["Packaged .mflash"]
        B
        D
        E
    end
Key rules
.mflash.json contains the deck JSON directly.
.mflash contains a root-level deck.json.
Both load into the same normalized deck object.
Study mode should not care which representation the deck came from.
