# ExpertPack

Structured knowledge packages that turn AI agents into domain experts — for products, people, and processes. Feed an agent your docs, websites, data, or just talk to it. The schema handles the rest.

---

## What Is ExpertPack?

ExpertPack is an open framework for building knowledge packs that AI agents consume to become instant domain experts. Point an agent at the schema, feed it your raw materials — documents, websites, conversations, data exports — and it organizes everything into a structured pack that any AI system can use.

Unlike generic RAG (stuffing docs into a vector store), ExpertPacks are structured around how experts actually think — concepts, workflows, decision trees, edge cases, and the tribal knowledge that never makes it into documentation.

Every ExpertPack is:
- **Markdown-first** — human-readable, AI-consumable, git-versionable
- **AI-built** — agents create packs from conversations, websites, documents, and data exports
- **Structured for retrieval** — small files, section headers, cross-references optimized for RAG
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

## Repository Structure

```
ExpertPack/
├── ARCHITECTURE.md          ← Framework design philosophy
├── README.md                ← This file
├── LICENSE                  ← Apache 2.0
│
├── schemas/                 ← Pack blueprints
│   ├── core.md              ← Shared principles for all pack types
│   ├── person.md            ← Person-pack schema
│   ├── product.md           ← Product-pack schema
│   └── process.md           ← Process-pack schema
│
└── packs/                   ← Pack instances
    ├── your-person-pack/    ← e.g., a founder's knowledge & stories
    └── your-product-pack/   ← e.g., a product's docs & workflows
```

---

## Key Principles

- **Markdown is content** — all knowledge lives in `.md` files
- **JSON is navigation** — indexes help agents find content, they're not content themselves
- **One source of truth** — each fact lives in exactly one place
- **Small focused files** — 1–3KB per file for precise RAG retrieval
- **Never overwrite** — flag contradictions, let the human resolve

See [schemas/core.md](schemas/core.md) for the full set of principles.

---

## Status

🚧 **Active development** — schemas defined, framework stabilizing.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

The ExpertPack framework (schemas, architecture, tooling) is open source. Individual pack instances contain original content and can be licensed independently by their creators.
