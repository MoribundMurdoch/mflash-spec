# mflash Schemas

This directory contains JSON Schemas for mflash deck and progress files.

## Current schema

- `mflash-schema.json` — current/latest deck schema.
- `mflash-v2.schema.json` — explicit mflash v2 deck schema.

## Legacy schema

- `mflash-v1.schema.json` — legacy mflash v1 deck schema, kept for compatibility and migration.

## Progress schema

- `mflash-progress-v1.schema.json` — separate study progress format.

Applications SHOULD load v1 and v2 decks, but SHOULD save newly written decks as v2 by default.
