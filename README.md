# ExpertPack

Structured knowledge packages that turn AI agents into domain experts — for products, people, and processes. Feed an agent your docs, websites, data, or just talk to it. The schema handles the rest.

---

## What Is ExpertPack?

ExpertPack is an open framework for building knowledge packs that AI agents consume to become instant domain experts. Point an agent at the schema, feed it your raw materials — documents, websites, conversations, data exports — and it organizes everything into a structured pack that any AI system can use.

Unlike generic RAG (stuffing docs into a vector store and hoping for the best), ExpertPacks are structured around how experts actually think — concepts, workflows, decision trees, edge cases, and the tribal knowledge that never makes it into documentation.

**The token problem:** Dumping all your content into one big context pool bloats every conversation with irrelevant material, burns tokens on content the agent doesn't need for this turn, and dilutes retrieval quality. ExpertPack solves this with a [three-tier context strategy](schemas/core.md#context-strategy) — core identity loads every session, knowledge loads on topic match, and heavy content loads only on demand. Your agent gets the right information at the right time, not everything all the time.

Every ExpertPack is:
- **Markdown-first** — human-readable, AI-consumable, git-versionable
- **AI-built** — agents create packs from conversations, websites, documents, and data exports
- **Token-efficient** — three-tier context strategy loads only what's needed per conversation
- **Structured for retrieval** — small files, section headers, cross-references optimized for RAG
- **Composable** — combine person, product, and process packs into unified deployments
- **Type-aware** — person, product, and process packs each have their own schema
- **Agent-agnostic** — works with any AI system that can read Markdown files

## Pack Types

### 🧑 Person Packs
Capture a person — stories, beliefs, relationships, voice, and legacy.

**Use cases:** Personal AI assistant, family archive, memorial AI, digital legacy, founder knowledge capture

**Example:** *BobGPT* — a father captures his life stories, beliefs, and family history so his kids and grandkids can talk to an AI that actually knows him.

### 📦 Product Packs
Capture deep knowledge about a product or platform — concepts, workflows, troubleshooting.

**Use cases:** AI support agent, sales assistant, training tool, onboarding guide, product documentation

**Example:** *AcmeHQ* — a project management company packages their product knowledge so an AI agent can handle tier-1 support, walk new users through onboarding, and answer sales questions. Works equally well for software platforms, hardware products, medical devices, or any product with enough complexity to warrant expert knowledge.

### 🔄 Process Packs
Capture complex multi-phase processes — phases, decisions, checklists, gotchas.

**Use cases:** Guided navigation of home building, business formation, project management, certification processes

**Example:** *Custom Home Build* — a veteran builder captures every phase, decision point, and gotcha from 30 years of building homes, so first-time homebuilders get expert guidance without a consultant.

### 🔗 Composites
Combine multiple packs into a single deployment. A CEO agent needs to sound like the founder (person pack), know the product (product pack), and follow the sales methodology (process pack). Composites wire them together with role assignments, context tier overrides, and cross-pack conflict resolution.

**Use cases:** Founder AI assistant, multi-product support bot, company knowledge base, personal legacy AI

**Example:** *AcmeCEO* — combines a person pack (founder's voice and stories), a product pack (AcmeHQ platform), and a process pack (enterprise sales methodology) into a single agent that sounds like the CEO and knows everything about the business.

---

## Quick Start

### Creating a New Pack

ExpertPacks are designed to be built by AI agents, not manually. You provide the knowledge — the AI reads the schema, asks the right questions, and handles all the structuring, file creation, and organization.

**What you need:**
- An AI agent with file access (OpenClaw, Cursor, Claude Code, etc.)
- A decision: person, product, or process pack

**The workflow:**

1. **Point your AI agent at this repo** and tell it to read the schema for your pack type:
   - Person → [schemas/person.md](schemas/person.md)
   - Product → [schemas/product.md](schemas/product.md)
   - Process → [schemas/process.md](schemas/process.md)
   - Composite → [schemas/composite.md](schemas/composite.md)
   - All types → [schemas/core.md](schemas/core.md)

2. **Feed it knowledge.** The agent structures everything — you just supply the raw material. Multiple sources work:

   - **Conversation** — Talk to the agent. It asks questions based on the schema, captures your answers, and files them. Great for stories, opinions, tribal knowledge, and anything in your head that's never been written down.
   - **Websites** — Point the agent at a URL. It scrapes and restructures the content into pack-formatted files. Ideal for product docs, company sites, personal blogs, or wikis.
   - **Existing documents** — Drop in PDFs, Word docs, spreadsheets, slide decks, or plain text. The agent reads them, extracts the knowledge, and organizes it according to the schema.
   - **Data exports** — CRM exports, support ticket archives, FAQ databases, knowledge bases. Anything structured or semi-structured that the agent can parse.
   - **Combination** — Most packs use a mix. Scrape the website for the basics, ingest the docs for depth, then fill the gaps through conversation.

3. **Review what it built.** The agent creates the `manifest.yaml`, `overview.md`, directory structure, and all content files. You review, correct, and iterate.

The schema is the agent's blueprint. You supply the raw expertise in whatever form you have it. The agent does the filing.

### Using an Existing Pack

A completed ExpertPack is a folder of Markdown files — ready to plug into any AI agent that supports file-based context or RAG. Clone (or copy) the pack into your agent's workspace, point the agent at it, and it becomes a domain expert immediately.

**Steps:**

1. **Get the pack** into your agent's workspace:
   ```bash
   # Clone directly, or copy a pack folder from an existing ExpertPack repo
   git clone https://github.com/someone/their-expertpack.git
   ```

2. **Tell your agent where it is.** How you do this depends on your platform:

   | Platform | Integration |
   |----------|-------------|
   | **OpenClaw** | Add the pack path to `memorySearch.extraPaths` in your config. The agent's RAG indexes all `.md` files automatically. |
   | **Cursor** | Place the pack in your project. Cursor indexes workspace files for context. |
   | **Claude Code** | Place the pack in your project. Reference it from `CLAUDE.md` or let the agent discover it. |
   | **Custom / API** | Feed the `.md` files into your vector store or context window. The small-file structure (1–3KB each) is optimized for chunked retrieval. |

3. **Start asking questions.** The agent now has deep, structured expertise. No prompt engineering required — the pack's structure (entry point, cross-references, focused files) guides retrieval naturally.

**Why it works:** ExpertPacks aren't just document dumps. Every file is sized for precise retrieval, cross-referenced for context, and organized around how experts actually think. Your agent doesn't need special instructions — it just needs access to the files.

---

## Agent Packs — Export Your AI Agent as an ExpertPack

**New in v1.6/1.7:** AI agents can now export themselves as ExpertPacks using the `agent` subtype of the person schema. An agent pack captures everything an AI agent has learned and become — identity, personality, operational knowledge, tool expertise, behavioral patterns, and relationships — in a format that can bootstrap a new instance to near-equivalent capability.

### What Agent Packs Enable

- **Backup & restore** — your agent dies; a new one boots from its EP and is immediately competent
- **Migration** — move an agent from one platform to another, bringing its knowledge along
- **Collaboration** — share an agent's domain expertise with another agent via composite
- **Marketplace** — distribute a well-trained agent configuration as a portable pack

### Auto-Discovery Export

The included `expertpack-export` skill can scan a running agent's workspace, auto-discover knowledge domains, and generate a complete composite EP:

```
Agent workspace (438KB raw state)
    ↓ scan → discover → classify
Proposed composite:
    - 1 agent pack (identity, tools, safety, routines)
    - 1 person pack (user knowledge)
    - N product/process packs (domain expertise)
    ↓ distill → compress → validate
Composite EP (31KB structured knowledge, 7% of raw)
```

See [schemas/person.md — Agent Extension](schemas/person.md#agent-extension-subtype-agent) for the full spec, and `skills/expertpack-export/` for the automation tooling.

---

## Featured Packs

These example packs demonstrate the ExpertPack format in action. Each is built from real source material — official documentation, community forums, source code analysis, and practitioner knowledge.

| Pack | Type | Description | Files | Size |
|------|------|-------------|-------|------|
| [**Blender 3D**](packs/blender-3d/) | Product | The free, open-source **3D modeling, animation, and rendering software** (blender.org). Covers polygon modeling, sculpting, PBR materials, Cycles/EEVEE rendering, Geometry Nodes, and more. Deep practitioner knowledge for artists and technical users. | 13 | ~120 KB |
| [**Home Assistant**](packs/home-assistant/) | Product | The open-source **home automation platform**. Covers smart home protocols (Zigbee/Z-Wave/Matter), automation patterns, presence detection, YAML configuration, ESPHome, dashboards, voice assistant, energy management, and security monitoring. | 27 | ~289 KB |

> 💡 These packs are open-source examples — not toy demos. Each contains substantive, practitioner-level content that a domain expert would recognize as valuable. Browse them to see what a well-built ExpertPack looks like.

---

## Repository Structure

```
ExpertPack/
├── ARCHITECTURE.md          ← Framework design philosophy
├── ROADMAP.md               ← Improvement project tracker
├── README.md                ← This file
├── LICENSE                  ← Apache 2.0
│
├── schemas/                 ← Pack blueprints
│   ├── core.md              ← Shared principles for all pack types (v1.7)
│   ├── person.md            ← Person-pack schema (v1.6) — includes agent subtype
│   ├── product.md           ← Product-pack schema (v1.8)
│   ├── process.md           ← Process-pack schema (v1.4)
│   ├── composite.md         ← Composite schema (v1.1) — auto-discovery & export
│   └── eval.md              ← Evaluation framework for measuring pack quality
│
├── skills/                  ← Agent skills
│   └── expertpack-export/   ← Auto-discover & export an agent instance to EP
│
├── guides/                  ← Practical how-to guides
│   └── population-methods.md ← How to populate packs from various sources
│
├── tools/                   ← Tooling for pack development
│   └── eval-runner/         ← Eval runner script for automated quality scoring
│
└── packs/                   ← Pack instances (example packs included)
    ├── blender-3d/          ← Blender 3D software — modeling, animation, rendering
    ├── home-assistant/      ← Home Assistant — home automation platform
    └── ...                  ← Your packs here
```

---

## Retrieval Optimization

ExpertPacks go beyond basic RAG with a multi-layer retrieval system designed to maximize precision and minimize wasted tokens. These layers work together — each compensates for what the others can't do alone.

### Summaries (`summaries/`)
Section-level summaries that enable hierarchical retrieval. Broad questions ("what can this product do?") match summaries first with high relevance. The agent drills into detail files for follow-ups. Follows the RAPTOR pattern — recursive summarization into a retrieval tree.

### Propositions (`propositions/`)
Atomic factual statements extracted from content files. When a user asks a specific factual question, the RAG system matches an exact proposition rather than a paragraph that happens to contain the answer. High-precision retrieval for factual queries.

### Lead Summaries
A 1–3 sentence blockquote at the top of high-traffic content files that directly answers the most likely query. Ensures the first RAG chunk contains the core answer, not a table of contents or preamble.

### Glossary (`glossary.md`)
Maps common user language to precise technical terms. Users say "stuck ZIP codes" when the pack documents "locked territories." The glossary bridges this vocabulary gap so RAG retrieval finds the right content regardless of how users phrase their questions.

### File Splitting + Three-Layer Approach
When content files grow beyond 1–3KB, split them — but never split without also generating summaries and propositions. Naive splitting loses cross-topic context. The three-layer approach (split files + summaries + propositions) consistently outperforms any single optimization.

See [schemas/core.md](schemas/core.md) for the full retrieval optimization spec.

---

## Schema Versioning

Every pack type schema carries a semantic version (`MAJOR.MINOR`). Major bumps indicate breaking structural changes; minor bumps are additive and backwards-compatible.

Every pack's `manifest.yaml` declares which schema version it targets:

```yaml
schema_version: "1.6"  # Version of the type-specific schema this pack conforms to
```

Current schema versions:
- Core: **1.7** — subtypes, retrieval optimization (summaries, propositions, lead summaries, glossary)
- Person: **1.6** — agent subtype, story cards, timeline, provenance, privacy modes, reasoning, conflicts
- Product: **1.8** — timeline, decisions, customers, limitations, landscape, mental model, lead summaries, glossary
- Process: **1.4** — exceptions, variants, enhanced phases/roles/overview
- Composite: **1.1** — auto-discovery & export, multi-pack deployments with role assignments and conflict resolution
- Eval: **1.0** — evaluation framework for measuring and tracking pack quality

---

## Source Provenance

Every content file can track where its information came from using frontmatter:

```markdown
---
sources:
  - type: video
    title: "Product Overview Walkthrough"
    ref: "03:12-04:05"
  - type: documentation
    url: "https://docs.example.com/feature-x"
    date: "2026-01-15"
---
```

Supported source types: `video`, `documentation`, `interview`, `support`, `conversation`. Provenance is especially important for packs built from multiple sources where content may need later verification or updating.

---

## Evaluation

Every ExpertPack can include an eval suite to measure and track quality. The eval framework ([schemas/eval.md](schemas/eval.md)) defines:

- **Response quality** — correctness, completeness, hallucination rate, refusal accuracy
- **Retrieval quality** — hit rate, precision
- **Efficiency** — tokens per query, latency, cost
- **Pack health** — structural conformance to schema

Build an eval set (10–20 test questions), run it with the [eval runner](tools/eval-runner/), and use results to guide optimization. Eval-driven improvement beats guessing.

---

## Key Principles

- **Markdown is content** — all knowledge lives in `.md` files
- **JSON is navigation** — indexes help agents find content, they're not content themselves
- **One source of truth** — each fact lives in exactly one place
- **Small focused files** — 1–3KB per file for precise RAG retrieval
- **Tiered context loading** — always/searchable/on-demand tiers minimize token cost per conversation
- **Retrieval-optimized** — summaries, propositions, lead summaries, and glossary for multi-layer retrieval
- **Source-tracked** — provenance frontmatter traces content back to its origin
- **Composable** — combine packs with role assignments, context overrides, and conflict resolution
- **Eval-driven** — measurable quality with automated scoring and baselines
- **Schema-versioned** — type schemas carry semantic versions; packs declare their target version
- **Never overwrite** — flag contradictions, let the human resolve

See [schemas/core.md](schemas/core.md) for the full set of principles.

---

## Status

🚧 **Active development** — schemas maturing, retrieval optimization and eval framework in place, tooling expanding.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

The ExpertPack framework (schemas, architecture, tooling) is open source. Individual pack instances contain original content and can be licensed independently by their creators.
