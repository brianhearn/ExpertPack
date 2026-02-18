# ExpertPack

Structured knowledge packages that give AI agents deep expertise — in products, people, and processes.

---

## What Is ExpertPack?

ExpertPack is a framework for building knowledge packs that AI agents can consume to become instant domain experts. Unlike generic RAG (stuffing docs into a vector store), ExpertPacks are structured around how experts actually think — concepts, workflows, decision trees, edge cases, and the tribal knowledge that never makes it into documentation.

Every ExpertPack is:
- **Markdown-first** — human-readable, AI-consumable, git-versionable
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

1. **Choose your type:** person, product, or process

2. **Create the directory:**
   ```
   packs/my-pack/
   ```

3. **Add required files:**
   ```yaml
   # manifest.yaml
   name: "My Pack"
   slug: "my-pack"
   type: "product"  # or "person" or "process"
   version: "1.0.0"
   description: "What this pack contains"
   entry_point: "overview.md"
   ```

   ```markdown
   # overview.md
   What this pack is about and who it's for.
   ```

4. **Follow the schema** for your pack type:
   - Person → [schemas/person.md](schemas/person.md)
   - Product → [schemas/product.md](schemas/product.md)
   - Process → [schemas/process.md](schemas/process.md)

5. **Read the core rules** that apply to all packs: [schemas/core.md](schemas/core.md)

---

## Repository Structure

```
ExpertPack/
├── ARCHITECTURE.md          ← Framework design philosophy
├── README.md                ← This file
├── LICENSE.md               ← License (TBD)
│
├── schemas/                 ← Pack blueprints
│   ├── core.md              ← Shared principles for all pack types
│   ├── person.md            ← Person-pack schema
│   ├── product.md           ← Product-pack schema
│   └── process.md           ← Process-pack schema
│
└── packs/                   ← Pack instances
    ├── bob-gpt/             ← Example: Person pack
    └── acme-hq/             ← Example: Product pack
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

TBD
