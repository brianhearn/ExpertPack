# ARCHITECTURE.md — ExpertPack Framework

*What ExpertPacks are, how they work, and why they're structured this way.*

---

## The Problem

Frontier AI models know a lot about the world, but they know almost nothing about *your* product, *your* life, or *your* process. Ask an LLM about your company's software and you'll get vague, outdated, or hallucinated answers. Ask it about your grandfather and it has nothing. Ask it how to build a custom home and you'll get generic advice that misses the gotchas.

RAG helps — stuff some documents into a vector store — but raw documentation makes a poor expert. Docs are written for humans browsing, not for AI reasoning. An expert system needs something different: structured knowledge that mirrors how a veteran practitioner thinks.

That's what an ExpertPack is.

---

## What is an ExpertPack?

An ExpertPack is a structured knowledge package that gives an AI agent deep expertise in a specific domain. It's a portable, git-native, Markdown-first knowledge base designed to be consumed by AI agents and readable by humans.

ExpertPacks come in three types:

| Type | What It Captures | Example |
|------|-----------------|---------|
| **Person** | A human being — stories, mind, beliefs, relationships, voice | BobGPT — a father's life archive for his family |
| **Product** | A product or platform — concepts, workflows, troubleshooting, tribal knowledge | AcmeHQ — expert knowledge for a project management platform |
| **Process** | A complex endeavor — phases, decisions, checklists, gotchas | Building a custom home, starting a business, landscape design |

Each type follows a type-specific schema that defines its directory structure and content patterns. All types share a common set of core principles.

---

## Core Principles

These apply to every ExpertPack. See [schemas/core.md](schemas/core.md) for the full specification.

| Principle | Rule |
|-----------|------|
| **MD-Canonical** | Markdown is the source of truth for all content; JSON is navigation only |
| **One Source of Truth** | Each fact lives in exactly one place |
| **Small Files** | 1–3KB per content file, one topic per file |
| **RAG-Optimized** | `##` section headers at natural topic breaks for quality chunking |
| **Layered Loading** | Minimal → topical → full context loading |
| **Cross-Referenced** | Relative markdown links between related files |
| **Git-Native** | Version controlled, diffable, collaborative |
| **Never Overwrite** | Contradictions are flagged for human resolution |

---

## How Schemas Work

The schema system has two layers:

### Core Schema ([schemas/core.md](schemas/core.md))
Shared principles and conventions that apply to every ExpertPack:
- The MD-canonical principle
- Required files (`manifest.yaml`, `overview.md`)
- Directory conventions (`_index.md`, `_access.json`)
- File structure rules (size, naming, headers)
- Cross-referencing patterns
- Layered loading strategy
- Conflict resolution
- Agent consumption patterns

### Type-Specific Schemas
Each pack type has its own schema that extends core with domain-specific structure:

- **[schemas/person.md](schemas/person.md)** — Mind taxonomy (9 universal categories), verbatim content, summaries, biographical facts, relationships, legacy/memorial mode, presentation (voice, appearance)
- **[schemas/product.md](schemas/product.md)** — Concepts, workflows, troubleshooting (errors, diagnostics, common mistakes), screens, FAQ, commercial info, entity cross-references
- **[schemas/process.md](schemas/process.md)** — Phases, decisions, checklists, resources, examples, gotchas

A pack declares its type in `manifest.yaml`, which determines which type-specific schema applies.

---

## Packs Are Instances

A pack is an instantiation of a schema — a concrete knowledge base about a specific person, product, or process.

```
ExpertPack/
├── schemas/               ← The blueprints
│   ├── core.md
│   ├── person.md
│   ├── product.md
│   └── process.md
│
└── packs/                 ← The instances
    ├── bob-gpt/           ← Person pack: BobGPT
    └── acme-hq/           ← Product pack: AcmeHQ
```

Creating a new pack means:
1. Choose the type (person, product, or process)
2. Create a directory under `packs/`
3. Add `manifest.yaml` and `overview.md` (required)
4. Populate directories per the type-specific schema
5. Follow core principles for all content

---

## How Agents Consume Packs

### Discovery
1. Read `manifest.yaml` — understand what the pack covers, its type, and scope
2. Read `overview.md` — get enough context to route queries
3. This is the **minimal** loading level — enough for pack awareness

### Retrieval
For a specific question:
- **Navigate:** Read `_index.md` for the relevant directory → pick the right file
- **Search:** Use RAG/vector search across all `.md` files for semantic matching
- **Both:** RAG finds candidates, agent reads full files for complete context

### Update
When adding or changing content:
1. Identify the canonical file
2. Check for contradictions
3. Edit the Markdown file
4. Update any affected JSON indexes
5. Commit with a descriptive message

---

## Content Creation

ExpertPacks are intended to be created and maintained by AI agents. The creation pipeline below is written as an agent-operated workflow — the agent is the operator, the human is the pack owner or domain expert who supplies knowledge and approvals.

### Where Pack Content Comes From

| Source | Quality | Coverage |
|--------|---------|----------|
| **Expert interviews / dictation** | Highest — captures tribal knowledge | Decisions, gotchas, real experience |
| **Existing documentation** | Medium — written for human browsing | Concepts, basic workflows |
| **Video tutorials / walkthroughs** | High — shows actual usage | Workflows, screen knowledge |
| **Support tickets / forums** | High — real problems | Troubleshooting, FAQ |
| **Personal experience** | Highest — authentic, specific | Stories, beliefs, examples |

### Agent-operated Creation Pipeline

1. Schema read-in
   - The agent loads type-specific and core schemas and uses them as the filing guide.
2. Skeleton initialization
   - The agent creates the pack skeleton (manifest.yaml, overview.md, starter directories) and commits it.
3. Crawl & ingest
   - The agent ingests authorized docs, transcribes media, and chunks text with `##` headers for RAG.
4. Expert interviews
   - The agent conducts structured interviews with the pack owner to capture tribal knowledge, edge cases, and decisions. Capture verbatim and distilled forms.
5. Structure & cross-reference
   - The agent files content into the schema taxonomy, adds cross-links, and updates `_index.md` and JSON indexes.
6. Troubleshooting & gotchas
   - The agent synthesizes recurring failures from tickets/forums and expert input into troubleshooting and gotchas files.
7. Gap analysis
   - The agent compares actual content to schema expectations and produces a prioritized gap report for the pack owner.
8. Validation & provenance
   - The agent requests confirmation for ambiguous facts, records provenance, and flags contradictions for human adjudication.
9. Commit & reporting
   - The agent commits changes with descriptive messages and produces status summaries of new content and remaining gaps.
10. Ongoing maintenance
   - The agent monitors new sources, ingests updates, and repeats the pipeline under human supervision.

Practical prompting guidance for agents

- Ask one focused question per prompt during interviews and request concrete examples or steps.
- Present clarifying choices when uncertain and ask the pack owner to pick or correct.
- Frame gap reports as short checklists with suggested interview prompts.

Notes

- The agent is responsible for structuring and filing content; humans are responsible for providing knowledge and resolving conflicts.
- Record provenance for every file; prefer human confirmation before making authoritative edits.

---

## Future Directions

- **Pack distribution** — How should packs be shared? npm packages, git submodules, downloads?
- **Community packs** — Can anyone create an ExpertPack? What's the quality bar?
- **Licensing** — Open framework, per-pack licensing for commercial packs?
- **Multi-version support** — Product packs for different product versions
- **Validation** — Systematic testing that pack content matches reality
- **Pack marketplace** — A hub for discovering and sharing ExpertPacks

---

## Revision History

| Date | Changed By | Notes |
|------|-----------|-------|
| 2026-02-13 | EasyBot | Initial ARCHITECTURE.md |
| 2026-02-16 | EasyBot | Unified framework — three pack types, shared schemas |
| 2026-02-18 | EasyBot | Person schema: mind taxonomy (9 categories); removed project-specific references |

---

*This is a living document. Update it as the framework evolves.*
