# ExpertPack — Project Status

*Working context for the ExpertPack framework. Read this to know where we are.*

## Current State: Unified Framework with Schemas

### Major Restructure (2026-02-16)

The ExpertPack and BrianGPT repositories have been unified into a single ExpertPack repo with:
- **Shared schemas** — `schemas/core.md`, `schemas/person.md`, `schemas/product.md`, `schemas/process.md`
- **BrianGPT merged** — now lives at `packs/brian-gpt/` (person-type pack)
- **EZT Designer renamed** — from `packs/easyterritory-designer/` to `packs/ezt-designer/` (product-type pack)
- **Framework-level docs** — new `ARCHITECTURE.md` and `README.md` covering the whole framework
- **Old docs/ absorbed** — content moved into schemas/

### Packs

#### brian-gpt (Person Pack)
- **Status:** Active — content collection ongoing
- **Content:** 50+ verbatim stories, 21 philosophy essays, 5 politics essays, biographical facts, 28+ relationships, worldview content
- **What's done:** MD-canonical migration, RAG integration, section headers, two-tier content
- **What's not done:** More story collection, voice/style analysis, worldview files expansion
- **Source repo:** `/root/.openclaw/workspace/brian-gpt/` (kept intact, not deleted)

#### ezt-designer (Product Pack)
- **Status:** V1 ~70% complete
- **Content:** 14 concept files, 8 workflows, 5 commercial files, 1 FAQ, entities.json (20 entities)
- **What's done:** Full docs site crawl, concepts, workflows, commercial, FAQ
- **What's not done:** Troubleshooting, screens, tribal knowledge, expert review
- **Highest priority gap:** Troubleshooting section

### Schemas
All four schemas are defined and complete:
- `schemas/core.md` — Shared principles (MD-canonical, file size, RAG chunking, conflict resolution, etc.)
- `schemas/person.md` — Person-pack blueprint (verbatim, summaries, facts, relationships, legacy)
- `schemas/product.md` — Product-pack blueprint (concepts, workflows, troubleshooting, entities.json)
- `schemas/process.md` — Process-pack blueprint (phases, decisions, checklists, gotchas)

### Next Steps
1. Brian reviews the restructure and schemas
2. Content review of EZT Designer pack for accuracy
3. Begin troubleshooting section for EZT Designer
4. Continue BrianGPT content collection
5. Consider first process-type pack

### Open Questions
- Should the brian-gpt source repo be archived or deleted?
- Pack distribution strategy (git submodules, npm, etc.)?
- First process pack topic?

---
*Last updated: 2026-02-16*
