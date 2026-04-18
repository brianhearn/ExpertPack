---
id: your-pack-slug/concepts/example-concept
title: "Example Concept"
type: concept
tags: [example-concept, your-domain]
pack: your-pack-slug
retrieval_strategy: standard
concept_scope: single
schema_version: "4.0"
verified_at: "YYYY-MM-DD"
verified_by: agent
related:
  - other-concept.md
  - related-workflow.md
---

# Example Concept

An example concept is a self-contained unit of knowledge in an ExpertPack — it carries its definition, body, FAQs, related terms, and key propositions in a single retrieval-ready file. This opening paragraph IS the summary: retriever-anchored, reader-useful, no throat-clearing. Write it to answer the most likely query about this concept directly.

## How It Works

Explain the concept clearly. Assume the reader knows the domain but not the specifics. Target 500–900 tokens for the whole file; hard ceiling 1,500. Use `##` section headers at natural topic breaks — the EP MCP chunker splits on these boundaries, so each section becomes its own coherent sub-chunk.

## Why It Matters

What does understanding this concept unlock? What mistakes does it prevent? This is often where esoteric knowledge (EK) lives — the things a general-purpose LLM gets wrong without the pack.

## Frequently Asked

### How is this concept different from [sibling-concept]?
Phrase questions the way users actually ask them. Each H3 becomes its own sub-chunk with a strong natural-language match surface.

### When should I use this concept vs. [alternative]?
Keep answers tight and directly applicable. FAQ answers should not re-explain the whole concept — assume the reader has the opening paragraph.

## Related Terms

- **Relative term 1:** Definition that only makes sense in context of this concept. If a term has its own definition, properties, and relationships, it earns its own concept file instead — don't embed it here.
- **Relative term 2:** Short, concrete, 1–2 sentences.

## Key Propositions

- Axiomatic statement 1 — a hard rule, invariant, or formal property.
- Axiomatic statement 2.

*(Omit this section when the concept's truth is adequately carried by body prose.)*

## Related Concepts

- [[other-concept]]
- [[related-workflow]]
