# ExpertPack Schema Registry

The schema registry defines the **canonical micro-record format** for ExpertPack content — a compact, machine-readable representation of any pack file that can be consumed by triple stores, search indexes, and downstream tools without losing provenance or semantic context.

## Files

| File | Purpose |
|---|---|
| `micro-record.schema.yaml` | Canonical field definitions for a micro-record |
| `micro-record.jsonld.json` | JSON-LD context for micro-records (stable URIs) |
| `types.yaml` | Registry of all declared content types with descriptions |
| `edge-kinds.yaml` | Registry of all declared graph edge kinds |
| `examples/concept-record.json` | Example micro-record for a concept file |
| `examples/workflow-record.json` | Example micro-record for a workflow file |
| `examples/faq-record.json` | Example micro-record for an FAQ entry |

## What Is a Micro-Record?

A micro-record is a minimal, canonical representation of a single ExpertPack file. It contains:

- **Stable identity** — `id` and `source_span_uri` for deterministic lookups
- **Canonical statement** — one sentence that is the primary claim of the file
- **Provenance** — when verified, by whom, from what source
- **Semantic context** — type, tags, related IDs, pack slug

Micro-records are designed to be generated from pack files (see `tools/micro-record-exporter/`) and fed into triple stores, vector indexes, or any tool that needs to reference EP content by ID rather than by free text.

## Design Goals

1. **Deterministic lookups** — any tool can reference a piece of knowledge by its stable `id`
2. **Compact** — one record per file, minimal fields, no narrative duplication
3. **Portable** — valid JSON-LD, importable into any triple store or knowledge graph
4. **Traceable** — every record links back to its source file via `source_span_uri`

## Relation to Graphiti / KG Patterns

This format is inspired by the temporal context graph pattern (Graphiti, 2026-04-15) but adapted for EP's static-curated model:
- Where Graphiti tracks `valid_from`/`valid_to` for dynamic facts, EP uses `valid_from`/`recorded_at` for versioned expertise
- Where Graphiti auto-extracts triples from episodes, EP micro-records are authored (or auto-generated from frontmatter) with human curation
- The `source_span_uri` field enables claim-to-span traceability (feeds `claim_verifier.py`)
