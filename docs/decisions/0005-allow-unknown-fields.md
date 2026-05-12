# 0005: Allow Unknown Fields

## Status

Accepted

## Context

mflash is intended to be used by multiple tools, apps, scripts, importers, exporters, and future versions of the format.

The format needs room for forward compatibility and tool-specific metadata.

Strictly rejecting every unknown field would make experimentation and future extension harder.

However, too much looseness can make typos harder to catch.

## Decision

mflash schemas allow unknown fields with `additionalProperties: true`.

Readers SHOULD ignore unknown fields.

Writers SHOULD preserve unknown fields when practical.

Core required fields are still validated by the schema.

## Consequences

Future versions and third-party tools can add metadata without immediately breaking older readers.

Plugin/app-specific fields can exist without requiring every tool to understand them.

Writers that preserve unknown fields can avoid destructive round-tripping.

The tradeoff is that some typo fields may not be rejected by schema validation.

## Example

A reader should load this card even if it does not understand `custom_hint`:

```json
{
  "id": "card_001",
  "term": "bonjour",
  "definition": "hello",
  "custom_hint": "Used during the day."
}
Guidance

Important standardized behavior should eventually move into the official schema.

Experimental or app-specific behavior may use unknown fields, but tools should avoid depending on undocumented fields for core interoperability.

Notes

This decision favors forward compatibility over strict typo detection.

Validation scripts and linters may later add optional warnings for suspicious unknown fields.
