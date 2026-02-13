# ARCHITECTURE.md — Design Rationale & Data Strategy

*Why ExpertPacks are structured the way they are, how agents consume them, and what we've learned building the first one.*

---

## The Problem

Frontier AI models know a lot about the world, but they know almost nothing about *your* product. Ask Claude or GPT about EasyTerritory and you'll get vague, outdated, or hallucinated answers. RAG helps — stuff some docs into a vector store — but raw documentation makes a poor expert. Docs are written for humans browsing, not for AI reasoning.

An AI support agent needs something different: structured knowledge that mirrors how a veteran support engineer thinks about the product — concepts, workflows, decision trees, edge cases, and the tribal knowledge that never makes it into docs.

That's what an ExpertPack is.

---

## Core Design Principles

### 1. Markdown-First
Every piece of knowledge is a Markdown file. This makes content human-readable, AI-consumable, git-versionable, and compatible with any RAG system. No proprietary formats, no databases, no lock-in.

### 2. Chunking by Design
Files are kept small (~1-3KB each) and focused on a single topic. Each file has `##` section headers at natural topic breaks. This is intentional — RAG chunkers split on ~400-token windows, and well-structured Markdown with headers produces high-quality, semantically coherent chunks. A file about "Capacity Planning" shouldn't also contain pricing information.

### 3. Layered Loading
Not every query needs the full pack. The structure supports three loading levels:

| Level | What to Load | When |
|-------|-------------|------|
| **Minimal** | `manifest.yaml` + `overview.md` | Product awareness, routing queries |
| **Topical** | Specific `concepts/`, `workflows/`, or `faq/` files | Answering a focused question |
| **Full** | Entire pack | Deep support session, complex troubleshooting |

This matters for token efficiency — a 50-file pack at full load burns context. Topical loading keeps costs down while maintaining depth.

### 4. Separation of Knowledge Types
Different types of knowledge serve different purposes and get queried differently:

| Directory | Knowledge Type | Query Example |
|-----------|---------------|---------------|
| `concepts/` | What things are, how they work | "What is capacity planning?" |
| `workflows/` | How to do things, step-by-step | "How do I import data?" |
| `troubleshooting/` | What went wrong, how to fix it | "Why can't I see my territories?" |
| `faq/` | Common questions, quick answers | "Does it work with Salesforce?" |
| `commercial/` | Pricing, deployment, security | "How much does it cost?" |

An agent answering a "how do I..." question should pull from `workflows/`. An agent answering a "what is..." question should pull from `concepts/`. This separation makes retrieval more precise.

### 5. Cross-Referencing via Links
Files reference each other with relative Markdown links. This creates a knowledge graph the agent can navigate:

```markdown
See [Territory Concepts](../concepts/territories.md) for background.
Related workflow: [Create Territory](../workflows/create-territory.md)
```

Index files (`_index.md`) in each directory serve as entry points — an agent can read the index to discover what's available before loading specific files.

---

## Pack Structure — What Each Part Does

```
packs/{product-name}/
├── manifest.yaml       ← Pack identity, version, scope, entry points
├── overview.md          ← Product summary — load this first, always
│
├── concepts/            ← The mental model
│   ├── _index.md        ← Directory of all concepts
│   └── {concept}.md     ← One concept per file
│
├── workflows/           ← Step-by-step procedures
│   ├── _index.md        ← Directory of all workflows
│   └── {workflow}.md    ← One task per file
│
├── troubleshooting/     ← Problem resolution (planned)
│   ├── errors/          ← Specific error messages + fixes
│   ├── diagnostics/     ← "Not working" decision trees
│   └── common-mistakes/ ← Gotchas and forgotten steps
│
├── faq/                 ← Common questions by category
│   └── {category}.md
│
└── commercial/          ← Business/sales information
    ├── _index.md
    ├── capabilities.md
    ├── pricing.md
    ├── deployment.md
    └── security.md
```

### Why These Categories?

These aren't arbitrary. They map to how support interactions actually flow:

1. **Customer asks a question** → Check `faq/` for a quick answer
2. **Customer needs to do something** → Load the relevant `workflow/`
3. **Customer doesn't understand something** → Load the relevant `concept/`
4. **Something went wrong** → Navigate `troubleshooting/` decision tree
5. **Prospect evaluating the product** → Load `commercial/` + `overview.md`

---

## How an Agent Consumes a Pack

### Discovery
The agent reads `manifest.yaml` to understand what the pack covers, then `overview.md` for product context. This gives enough awareness to route queries to the right section.

### Retrieval
For a specific question, the agent either:
- **Navigates:** Reads `_index.md` for the relevant section, picks the right file
- **Searches:** Uses RAG/vector search to find relevant chunks across all files
- **Both:** RAG finds candidates, agent reads the full file for context

### Answering
The agent synthesizes an answer from the retrieved content, cross-referencing related files as needed. Good answers cite specific workflows or concepts rather than paraphrasing vaguely.

---

## The Creation Process

### Where Pack Content Comes From

| Source | Quality | Coverage | Effort |
|--------|---------|----------|--------|
| **Web docs / help sites** | Medium — written for browsing, not AI | Good for concepts, basic workflows | Low — can be crawled and restructured |
| **Video tutorials** | High — shows actual UI flow | Great for workflows, screen knowledge | Medium — requires transcription + extraction |
| **Screenshots** | High — visual ground truth | Screens, element locations | Medium — requires analysis |
| **Guided walkthroughs** | Highest — captures tribal knowledge | Edge cases, gotchas, undocumented behavior | High — requires expert time |
| **Support tickets** | High — real user problems | Troubleshooting, FAQ | Medium — requires curation |

### The Crawl → Structure → Refine Pipeline

For the EasyTerritory Designer pack, we:

1. **Crawled** the docs site (`/docs-sitemap.xml`) — 68 pages of product documentation
2. **Structured** the raw content into pack format — concepts, workflows, commercial, FAQ
3. **Added section headers** — ensuring every file chunks well for RAG
4. **Cross-referenced** — linked related concepts and workflows
5. **Identified gaps** — screens and troubleshooting sections not yet populated

This gets you ~70% of V1. The remaining 30% — edge cases, tribal knowledge, undocumented behavior — requires guided walkthroughs with product experts.

---

## Version Strategy

### V1: Knowledge Layer (Current)
The agent can **guide humans** through the product. It knows what things are, how to do tasks, and what can go wrong. It cannot operate the product autonomously.

**Success criteria:** Agent with ExpertPack answers support questions better than agent with raw docs alone.

### V2: Automation Layer (Future)
The agent can **operate the product** via browser automation — clicking, typing, navigating. This adds an `automation/` directory with CSS selectors, executable playbooks, and state verification.

**V2 builds on V1** — all knowledge layer content remains; automation hooks are layered on top.

---

## Lessons Learned

### Docs ≠ Knowledge
Product documentation is written for a human who can see the screen and click around. An AI agent needs explicit information that docs assume — navigation paths, element names, what "success" looks like after completing a step. Restructuring docs into ExpertPack format forces this explicitness.

### File Size Matters for RAG
Large files produce poor search results. A 20KB file about "everything the product does" will match almost any query with mediocre relevance. Small, focused files (1-3KB) with clear headers produce high-relevance matches. One concept per file, one workflow per file.

### Section Headers Are Infrastructure
Without `##` headers, RAG chunkers produce arbitrary ~400-token slices that split mid-thought. With headers, chunks align to semantic boundaries. This is cheap to do and has outsized impact on retrieval quality. Every file should have descriptive section headers.

### Index Files Are Navigation
`_index.md` files serve two purposes: (1) they let an agent discover what's available without loading every file, and (2) they provide a table of contents that RAG can match against broad queries like "what workflows are documented?"

### The Two Hardest Things to Capture
1. **What the UI actually looks like** — Docs describe features, not screens. Screen documentation (`screens/`) requires screenshots or live app access.
2. **What goes wrong** — Troubleshooting knowledge lives in support engineers' heads. It's the highest-value content and the hardest to extract.

---

## Relationship to Other Projects

### BrianGPT
BrianGPT uses a similar markdown-first, RAG-optimized approach to capture a *person's* knowledge and identity. The structural patterns overlap (verbatim content + summaries, section headers for chunking, JSON for structured data), but the domains are fundamentally different. A person's life story and a SaaS product's knowledge base have different shapes — keeping them separate preserves clarity of purpose.

### OpenClaw
ExpertPacks are designed to be loadable by any AI agent system. OpenClaw's `memorySearch` can index pack files via `extraPaths` for RAG-based retrieval, but packs are not OpenClaw-specific. Any system that can read Markdown files can consume an ExpertPack.

---

## Open Questions

1. **Validation methodology** — How do we systematically verify pack accuracy against the live product?
2. **Automated generation** — Can we crawl + restructure docs into pack format with minimal human intervention?
3. **Pack distribution** — How should packs be shared/installed? (npm package, git submodule, download)
4. **Licensing** — Open source? Per-pack licensing? Vendor-created vs community-created?
5. **Multi-version support** — How to handle packs for different product versions simultaneously?

---

## Revision History

| Date | Changed By | Notes |
|------|-----------|-------|
| 2026-02-13 | EasyBot | Initial draft — documenting decisions from first pack build |

---

*This is a living document. Update it as the approach evolves.*
