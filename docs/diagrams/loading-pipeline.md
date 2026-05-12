# mflash Loading Pipeline

This diagram shows how mflash-compatible tools should load decks.

```mermaid
flowchart TD
    A["Input file"] --> B{"Input type?"}

    B -->|".mflash.json"| C["Read UTF-8 JSON"]
    B -->|".mflash"| D["Open package archive"]
    B -->|"CSV / TSV / Anki / other"| E["Run importer"]

    D --> F["Find root deck.json"]
    F --> C

    E --> G["Convert to mflash-like deck object"]
    C --> H["Check format and version"]
    G --> H

    H --> I{"Version?"}

    I -->|"v1"| J["Load legacy v1"]
    J --> K["Normalize to current app model"]
    K --> L["Generate missing deck/card IDs in memory"]

    I -->|"v2"| M["Validate v2 required fields"]
    M --> N["Require deck.id"]
    M --> O["Require card.id"]

    L --> P["Resolve media paths"]
    N --> P
    O --> P

    P --> Q["Normalized deck object"]
    Q --> R["Editor"]
    Q --> S["Study mode"]
    Q --> T["Exporter"]

    S --> U["Load/save separate progress file"]
    T --> V["Write v2 by default"]
Compatibility rule

Readers should load v1 and v2.

Writers should save newly written or migrated decks as v2 by default.

Migration should add deck IDs and card IDs, but should not add timestamps unless explicitly requested.
