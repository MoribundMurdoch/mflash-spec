# Contributing to mflash-spec

Thank you for your interest in improving the **mflash** file format!  
This repository defines the *official specification* for `.mflash`, including the formal spec, examples, and JSON schema.

All contributions are welcome: issues, proposals, improvements, and discussions.

---

## 📘 How to Contribute

### 1. File an Issue First (Recommended)
Before submitting a pull request for significant changes:

- Open an **Issue** describing the change you’d like to make.
- Explain *why* it improves the `.mflash` format.
- Include examples if applicable.

This helps maintain a clean, consistent format evolution.

---

## 🧩 Types of Contributions

You can help by contributing:

### ✔ Specification improvements  
Clarifying behavior, fixing typos, adjusting field definitions.

### ✔ Examples  
Adding more `.mflash` examples, including:
- Multilingual decks  
- Edge cases  
- Media usage  
- Language overrides  

### ✔ Schema updates  
Updating or enhancing `mflash-schema.json` to better reflect the spec.

### ✔ Discussions (Issues)  
Proposals for future versions (v2, v3…)  
e.g., ZIP container format, SRS metadata, RTL support, plugins, etc.

---

## 🛑 Breaking Changes

### The `.mflash` format is versioned.
The current spec describes:

- `"format": "mflash"`
- `"version": 1`

If a change **breaks compatibility**, it *must* be discussed thoroughly and may require:

- A formal **version bump** (e.g., v2)
- Backward-compatibility considerations
- Migration guidelines in the spec

Do **not** break v1 behavior without a discussion.

---

## 🧪 Validating Examples

Any `.mflash` example in the `examples/` folder should:

- Be valid UTF-8 JSON  
- Pass schema validation using the included `schema/mflash-schema.json`

## Why validate .mflash examples?
- Consistency: All files in the examples/ folder behave the same way. Tools that read .mflash can rely on the structure.

- Error prevention: Catches missing fields, wrong data types, or invalid values before they cause bugs.

- Future compatibility: When the format evolves (v2, v3…), validation helps distinguish which files follow which spec version.

(Optional but recommended):

```bash
npm install -g ajv-cli
ajv validate -s schema/mflash-schema.json -d "examples/*.mflash"
```

## Alternative validation methods
You don't have to use ajv. Any JSON Schema validator works:

- Online tools – paste your schema and JSON into websites like jsonschemavalidator.net

- Editor plugins – VS Code, IntelliJ, etc. can validate live if you add "$schema": "path/to/mflash-schema.json" inside your .mflash file.

- Other CLI tools – check-jsonschema, speclate, or custom scripts.
