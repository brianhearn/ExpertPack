# Product Pack Schema

*Blueprint for ExpertPacks that capture deep knowledge about a product or platform — concepts, workflows, troubleshooting, and the tribal knowledge that lives in support teams' heads. Applicable to software, hardware, medical devices, consumer products, or any product with enough complexity to benefit from structured expert knowledge. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

A product pack gives an AI agent the same depth of knowledge as a veteran product expert. Unlike generic RAG over documentation (which is written for humans browsing, not AI reasoning), a product pack structures knowledge around how support interactions actually flow — what things are, how to do things, what went wrong, and what the product costs.

**V1 Goal:** An agent that can *guide humans* through the product — answering questions, walking through workflows, and troubleshooting issues.

---

## Directory Structure

```
packs/{product-slug}/
├── manifest.yaml          ← Pack identity and metadata (required)
├── overview.md            ← Product summary — load first, always (required)
├── entities.json          ← Entity cross-reference index (recommended)
│
├── concepts/              ← The mental model
│   ├── _index.md          ← Directory of all concepts
│   └── {concept}.md       ← One concept per file
│
├── workflows/             ← Step-by-step procedures
│   ├── _index.md          ← Directory of all workflows
│   └── {workflow}.md      ← One task per file
│
├── interfaces/            ← Interface documentation (UI screens, panels, endpoints, or physical controls)
│   ├── _index.md          ← Directory of all interfaces
│   └── {interface}.md     ← One interface per file (include variant notes where applicable)
│
├── specifications/        ← Technical specs, requirements, compliance (optional)
│   ├── _index.md
│   └── {spec}.md          ← One spec category per file
│
├── troubleshooting/       ← Problem resolution
│   ├── errors/            ← Specific error messages + fixes
│   │   └── {error}.md
│   ├── diagnostics/       ← "Not working" decision trees
│   │   └── {issue}.md
│   └── common-mistakes/   ← Gotchas and forgotten steps
│       └── {mistake}.md
│
├── faq/                   ← Common questions by category
│   └── {category}.md
│
├── sources/               ← Ingestion artifacts and source indexes (optional)
│   ├── _index.md          ← Directory of all source materials
│   └── {source}.md        ← One index per source (video, doc set, interview)
│
└── commercial/            ← Business/sales information (optional)
    ├── _index.md
    ├── capabilities.md
    ├── pricing.md
    ├── deployment.md
    └── security.md
```

**Required:** `manifest.yaml`, `overview.md`
**Recommended:** `entities.json`, at least one of `concepts/`, `workflows/`, or `faq/`
**Optional:** Everything else, based on pack focus and available content

---

## Why These Categories?

These aren't arbitrary. They map to how support interactions actually flow:

1. **Customer asks a question** → Check `faq/` for a quick answer
2. **Customer needs to do something** → Load the relevant `workflows/` file
3. **Customer doesn't understand something** → Load the relevant `concepts/` file
4. **Something went wrong** → Navigate `troubleshooting/` decision trees
5. **Prospect evaluating the product** → Load `commercial/` + `overview.md`

An agent answering a "how do I..." question should pull from `workflows/`. An agent answering a "what is..." question should pull from `concepts/`. This separation makes retrieval more precise.

---

## Content Templates

### overview.md

```markdown
# {Product Name}

## What It Is
One paragraph: what the product does, who it's for.

## Key Capabilities
- Capability 1
- Capability 2
- Capability 3

## How It Fits
Where this product sits in the broader ecosystem.

## Getting Started
How to access the product, first steps.
```

### Concept File (concepts/{concept}.md)

Mental model, terminology, how things work.

```markdown
# {Concept Name}

## What It Is
Clear explanation of the concept.

## Why It Matters
When/why users encounter this concept.

## How It Works
Mechanics, rules, behavior.

## Example
Concrete example to illustrate.

## Related
- [Other Concept](other-concept.md)
- [Relevant Workflow](../workflows/relevant-workflow.md)
```

### Workflow File (workflows/{workflow}.md)

Step-by-step procedures for accomplishing tasks. The Steps section adapts to the product type — for software this may describe screens and UI interactions; for hardware or physical products it may describe physical operations, adjustments, or checks; for APIs it may describe request sequences and expected responses.

```markdown
# {Task Name}

## Goal
What the user is trying to accomplish.

## Prerequisites
- What must be true before starting
- What they need to have ready

## Steps

### 1. {First Step}
{Action to take}

- **Where:** {Screen, panel, component, or area}
- **What to do:** {Specific action — click, adjust, connect, configure}
- **You should see/hear/feel:** {Expected result}

### 2. {Second Step}
...

## Completion
How to know it worked. What they should observe when done.

## Common Issues
- **{Problem}:** {Solution}

## Related
- [Relevant Concept](../concepts/relevant-concept.md)
- [Related Workflow](related-workflow.md)
```

### Interface File (interfaces/{interface}.md)

Documentation for an interface — UI screen, physical panel, API endpoint, or other interaction surface.

```markdown
# {Interface Name}

## Purpose
What this interface is for, when users interact with it.

## How to Access
Navigation path(s), physical location, or endpoint URL to reach this interface.

## Variants
Notes about platform-specific or model-specific differences (desktop vs mobile, firmware revision, API version).

## Layout / Contract
For UI / physical interfaces: describe sections and elements. For APIs: describe request/response contract.

### {Section or Operation}
Description of this area or operation.

**Elements / Fields / Controls:**
| Name | Type | Purpose |
|------|------|---------|
| {Label} | Button | {What it does} |
| {Label} | Text field | {What data, validation rules} |
| {Field} | JSON body | {Request/response field description} |

## Common Tasks
- [Create a Project](../workflows/create-project.md)

## Tips
- Helpful hints for using this interface
```

**Element detail guidelines:**
- **Buttons / Controls:** What it does, prerequisites, what happens after
- **Fields / Parameters:** What data, required/optional, validation, examples
- **States:** Normal, loading, error states and how to detect them
- **Variants:** Platform or model differences to be aware of

### Error File (troubleshooting/errors/{error}.md)

```markdown
# {Error Message or Code}

## When It Appears
What action triggers this error.

## What It Means
Why this error occurs.

## How to Fix
Step-by-step resolution.

## Prevention
How to avoid this error in the future.
```

### Diagnostic File (troubleshooting/diagnostics/{issue}.md)

```markdown
# {Problem Description}

*"I'm trying to {action} but {unexpected result}."*

## Expected Behavior
What should happen when everything is working correctly.

## Diagnostic Questions

### What are you seeing?
- **{Symptom A}** → [Check X](#check-x)
- **{Symptom B}** → [Check Y](#check-y)

### Check X
{Diagnostic step}
- **If {result}:** {Resolution}
- **If not:** [Check Y](#check-y)

## Common Causes
1. {Cause} — {Quick fix}
2. {Cause} — {Quick fix}
```

### Common Mistake File (troubleshooting/common-mistakes/{mistake}.md)

```markdown
# {Mistake Description}

## Symptom
What the user experiences.

## The Mistake
What they did (or didn't do).

## The Fix
How to correct it.

## How to Avoid
What to remember for next time.
```

### FAQ File (faq/{category}.md)

```markdown
# {Category} FAQ

## {Question 1}
{Answer}

## {Question 2}
{Answer}
```

### Commercial Files (commercial/)

Business information for sales scenarios. See individual templates:

- **pricing.md** — Pricing model, tiers, what affects cost
- **deployment.md** — Architecture, requirements, data residency, or installation/unboxing and site requirements for hardware
- **security.md** — Certifications, data protection, authentication
- **capabilities.md** — What it can do, limitations, roadmap

---

## Specifications Directory (specifications/)

Optional directory for technical specifications, requirements, and compliance information. Use when the product has formal specs, regulatory constraints, or technical compatibility matrices.

- **Software:** System requirements, API specifications, browser compatibility, performance benchmarks
- **Hardware:** Dimensions, materials, electrical ratings, operating conditions, safety certifications
- **Any product:** Compliance standards, regulatory certifications, compatibility matrices

Template for specifications/{spec}.md:

```markdown
# {Specification Name}

## Summary
One-paragraph summary of what this specification covers.

## Scope
What components, models, or versions this spec applies to.

## Details
Technical parameters, tolerances, compliance statements, or API contracts.

## Related
- [Related Specification](../specifications/other-spec.md)
- [Related Concept](../concepts/related-concept.md)
```

---

## Sources Directory (sources/)

Optional directory for ingestion artifacts — indexes of source materials used to build the pack. These files document *where content came from* and help builder agents trace pack content back to original materials for updates, verification, or gap analysis.

**This is not content.** Sources files are metadata about the ingestion process. They complement the per-file provenance frontmatter defined in [core.md](core.md) by providing a bird's-eye view of all source materials and what was extracted from each.

**Context tier:** Tier 3 (on-demand). Only loaded during pack maintenance, content audits, or update workflows.

### Source Index File (sources/{source}.md)

One file per major source material. For a video, this is a scene-by-scene index with timestamps and extracted artifacts. For a documentation site, this is a page inventory with extraction status.

**Video source template:**

```markdown
---
source_type: video
title: "{Video Title}"
duration: "MM:SS"
file: "{filename or URL}"
ingested: "YYYY-MM-DD"
---

# {Video Title}

## Overview
What this video covers, target audience, product version shown.

## Scene Index

| Timestamp | Scene | Entities | Extracted To |
|-----------|-------|----------|-------------|
| 00:00-01:30 | Introduction and login | authentication, dashboard | concepts/authentication.md |
| 01:30-03:45 | Creating a new project | projects, templates | workflows/create-project.md |
| 03:45-05:20 | Configuring settings | settings-panel, user-roles | interfaces/settings-panel.md |
| 05:20-06:00 | Common error: permissions | permission-denied | troubleshooting/errors/permission-denied.md |

## Extraction Status
- **Workflows extracted:** 3 of 5 identified
- **Interfaces documented:** 2 of 4 screens shown
- **Gaps:** Settings sub-panels not yet documented, error at 07:15 not captured
```

**Documentation source template:**

```markdown
---
source_type: documentation
url: "{base URL}"
pages_total: {N}
ingested: "YYYY-MM-DD"
---

# {Documentation Source Name}

## Pages Indexed

| Page | Status | Extracted To |
|------|--------|-------------|
| Getting Started | ✅ Complete | workflows/getting-started.md |
| API Reference | ✅ Complete | specifications/api.md |
| Troubleshooting | ⏳ Partial | troubleshooting/errors/ |
| Release Notes | ❌ Not started | — |
```

**Interview source template:**

```markdown
---
source_type: interview
with: "{Person Name}"
role: "{Their role}"
date: "YYYY-MM-DD"
duration: "MM:SS"
---

# Interview: {Person Name}

## Topics Covered

| Timestamp | Topic | Extracted To |
|-----------|-------|-------------|
| 00:00-05:30 | Common new-user mistakes | troubleshooting/common-mistakes/ |
| 05:30-12:00 | Undocumented feature: bulk import | workflows/bulk-import.md |
| 12:00-15:45 | Edge case: large datasets | faq/performance.md |

## Key Insights
- Bullet-point summary of tribal knowledge captured
- Things that surprised the interviewer or contradicted documentation

## Follow-up Needed
- Topics mentioned but not fully explored
- References to other people who know more
```

### Maintenance

Update source index files when:
- New content is extracted from an existing source
- A gap is filled that was previously noted
- The source material is updated (new product version, revised documentation)

Source indexes make re-ingestion efficient: when a product ships a new version, the builder agent can review source indexes to identify which videos/docs need re-processing and which pack files may be affected.

---

## Entity Cross-Reference (entities.json)

`entities.json` is a manually maintained cross-reference index at the pack root. It tells an agent *where to look* when a topic comes up.

### What It Solves

When new information arrives (e.g., "user roles now support custom permissions"), the agent needs to:
1. Know that `user-roles` is a documented entity
2. Find all files that discuss it — concept, workflows, FAQ mentions
3. Update all relevant files, not just one

Without a cross-reference, the agent would have to search every file — slow, error-prone, and likely to miss mentions in unexpected places.

### Structure

**Example** `entities.json` entry:

```json
{
  "entities": [
    {
      "id": "user-roles",
      "name": "User Roles",
      "type": "core-feature",
      "description": "Permission levels that control what users can see and do",
      "related": ["teams", "access-control"],
      "files": {
        "concept": "concepts/user-roles.md",
        "workflows": ["workflows/assign-role.md"],
        "mentions": ["overview.md", "faq/general.md"]
      }
    }
  ]
}
```

### Entity Types

| Type | Examples |
|------|---------|
| `core-feature` | Key capabilities, primary functions |
| `component` | Sub-systems, modules, physical parts |
| `integration` | Third-party connections, accessories, companion products |
| `infrastructure` | Underlying systems the product depends on |
| `category` | Umbrella groupings |
| `specification` | Technical specs, compliance standards, certifications |

### Maintenance

Update `entities.json` whenever:
- A new concept, workflow, or feature file is added
- A new entity is introduced in the product
- Cross-references change (a feature is mentioned in a new file)

This is a navigation index — structured data that helps agents *find* content, not content itself. The knowledge lives in `.md` files; `entities.json` just tells you where to look.

---

## Product-Specific Manifest Fields

Beyond the core manifest fields defined in [core.md](core.md):

```yaml
# Required
name: "Product Name"
slug: "product-slug"
type: "product"
version: "1.0.0"
description: "Expert knowledge for {product}"
entry_point: "overview.md"

# Product-specific
product_version: "2024.1+"
vendor: "Company Name"
website: "https://example.com"

# What personas this pack serves
focus:
  - support      # Customer support scenarios
  - sales        # Sales/marketing scenarios
  # - training   # Internal training

# What sections are included
sections:
  - concepts
  - workflows
  - troubleshooting
  - faq
  - commercial

# What topics/features are covered
scope:
  - feature-1
  - feature-2
  - integration-1

# Entry points
index_files: "_index.md"

# Dependencies (other packs required)
dependencies: []
```

---

## Agent Consumption Patterns

### Support Scenario
1. Load `manifest.yaml` + `overview.md` — understand the product
2. Classify the question: concept / how-to / troubleshooting / pricing
3. Load the relevant `_index.md` for the target section
4. Load the specific file that answers the question
5. Cross-reference related files via markdown links
6. Synthesize an answer that cites specific content

### Sales Scenario
1. Load `overview.md` + `commercial/capabilities.md`
2. Pull from `commercial/pricing.md`, `commercial/deployment.md`, or `commercial/security.md` as needed
3. Reference `concepts/` for technical depth

### Update Scenario
1. New product information arrives
2. Load `entities.json` — identify affected entities
3. Find all files via entity cross-reference
4. Update Markdown files (following conflict resolution rules from [core.md](core.md))
5. Update `entities.json` if new entities or file references were created

---

## Pack Creation Process

### Input Sources

| Source | What It Provides | Quality | Effort |
|--------|------------------|---------|--------|
| **Product documentation** | Concepts, features, basic procedures | Medium — written for browsing | Low — restructure |
| **Video tutorials / demos** | Real usage, step-by-step procedures | High — shows actual product | Medium — transcribe and extract |
| **Product imagery** | Interface layouts, component locations | High — visual ground truth | Medium — requires analysis |
| **Expert walkthroughs** | Edge cases, tribal knowledge | Highest — captures what docs miss | High — requires expert time |
| **Support tickets / forums** | Real user problems, FAQ content | High — real pain points | Medium — requires curation |
| **Technical specifications** | Specs, compliance, requirements | High — authoritative | Low — reformat |

### The Crawl → Structure → Refine Pipeline

1. **Crawl** — Scrape product documentation (help sites, docs)
2. **Ingest video/media** — Process video tutorials and demos (see Video Source Ingestion below)
3. **Structure** — Reorganize all extracted content into pack format (concepts, workflows, commercial, FAQ)
4. **Add headers** — Ensure every file chunks well for RAG
5. **Cross-reference** — Link related concepts and workflows
6. **Build entities.json** — Map entities to their files
7. **Identify gaps** — Screens, troubleshooting, and tribal knowledge are usually missing

This gets you ~70% of V1. The remaining 30% — edge cases, tribal knowledge, undocumented behavior — requires guided walkthroughs with product experts.

### Video Source Ingestion

Video tutorials, product demos, and recorded walkthroughs are high-value sources — they show the actual product in use, capture real workflows, and reveal UI details that documentation often omits. However, video requires a different ingestion strategy than text documentation.

**Key principle: the pack is the chunking layer.** A consuming agent never needs to process video — it reads small, topic-scoped Markdown files. The chunking happens during pack *creation*, not consumption. You do not need to create smaller video files.

#### The Video Ingestion Pipeline

1. **Keep the master video intact.** Do not split it into smaller video files. The original recording stays as-is for reference and re-processing.

2. **Build a scene index.** Watch or process the video and produce `sources/{video-slug}.md` — a timestamped inventory of what happens in the video. Each scene entry captures:
   - Timestamp range (`MM:SS-MM:SS`)
   - What's happening (action, screen shown, concept explained)
   - Entities referenced (features, UI elements, settings)
   - Target pack file (where this content will be extracted to)

3. **Extract pack artifacts from timestamp ranges.** For each identified scene, create or update the appropriate pack file:
   - **UI walkthrough scenes** → `workflows/{task}.md` with timestamped steps
   - **Screen/panel tours** → `interfaces/{screen}.md` with layout details
   - **Conceptual explanations** → `concepts/{concept}.md`
   - **Error demonstrations** → `troubleshooting/errors/{error}.md`
   - **Tips and gotchas** → `troubleshooting/common-mistakes/{mistake}.md`

4. **Add provenance frontmatter** to every extracted file (see [core.md](core.md) Source Provenance):
   ```markdown
   ---
   sources:
     - type: video
       title: "Territory Designer Overview"
       ref: "03:12-04:05"
   ---
   ```

5. **Update cross-references.** Add new entities to `entities.json`, update `_index.md` files, and link related content.

6. **Track extraction status** in the source index file. Mark which scenes have been fully extracted, which are partial, and what gaps remain.

#### Chunking Strategy for Video

Even when using large-context models that can accept full video, UI walkthroughs benefit from focused processing:

- **Process by interaction moments**, not arbitrary time windows. A "moment" is a cluster of related actions: navigating to a screen, filling fields, clicking submit, observing the result. These map naturally to workflow steps.
- **Target 30–90 second segments** as a practical default. Short enough for accurate extraction, long enough to capture a complete interaction.
- **Extract frames at key moments** when visual detail matters — screen layouts, error dialogs, configuration panels. Reference these in interface files if the agent's platform supports image context.
- **Transcribe narration** for conceptual content. The speaker's explanation of *why* something works a certain way is often more valuable than the UI actions themselves — this becomes concept file content.

#### Multiple Videos for One Product

When building a pack from multiple videos (e.g., a training series):
- Create one `sources/{video-slug}.md` per video
- Use `sources/_index.md` to inventory all video sources with their coverage areas
- Cross-reference between source indexes when videos cover overlapping topics (note which video has the more authoritative/current treatment)
- Deduplicate: if two videos show the same workflow, extract from the better source and note the alternative in provenance

---

## Creating a New Product Pack

This section is a playbook for an AI agent creating and maintaining a product pack. Read the schema and use it as your filing map: determine where incoming documentation, expert input, and support data belong and file them accordingly.

Agent-first step-by-step

1. Read the schema and product blueprint
   - Load this file and core.md to understand required sections, expected files, and recommended data structures (entities.json, _index.md files).
   - Treat the schema as the authoritative navigation map for filing content.

2. Initialize the pack
   - Create packs/{product-slug}/ and the minimal required files: manifest.yaml (type: product) and overview.md. Create directories: concepts/, workflows/, interfaces/, troubleshooting/, faq/, commercial/, and a placeholder entities.json.
   - Commit the initial skeleton and record sources and creation notes in manifest.yaml.

3. Crawl and ingest existing documentation
   - Harvest official docs, help sites, API specs, manuals, and public support articles. Prioritize canonical sources listed by the domain expert.
   - For each source, extract sections and restructure them into concept or workflow files. Chunk large text into RAG-friendly sections by adding `##` headers without changing technical meaning.
   - Record provenance (source URL, scrape date) for every ingested file in frontmatter or manifest sources.
   - Create `sources/{doc-source}.md` for each documentation source with page inventory and extraction status.

4. Ingest video and media sources
   - For each video tutorial, demo, or recorded walkthrough, follow the Video Source Ingestion pipeline (see above).
   - Build `sources/{video-slug}.md` with the scene index, timestamps, and entity mapping.
   - Extract pack artifacts (workflows, interfaces, concepts, troubleshooting) from identified scenes.
   - Add provenance frontmatter to all video-derived files per the convention in [core.md](core.md).
   - Track extraction completeness in the source index — note gaps for follow-up.

5. Build concepts/ and workflows/ from all ingested sources
   - Convert conceptual explanations into concepts/{concept}.md with the template fields (What It Is, Why It Matters, How It Works, Example, Related).
   - Convert step-by-step procedures into workflows/{workflow}.md with Goal, Prerequisites, Steps, Completion, and Common Issues.
   - Merge content from multiple sources (docs + video + interviews) into single canonical files — use provenance frontmatter to track all contributing sources.
   - Add cross-links between related concept and workflow files.

6. Extract interfaces and specifications
   - From screenshots, UI docs, API contracts, device manuals, and video frame captures, create interfaces/{interface}.md and specifications/{spec}.md as appropriate. Include navigation paths, field-level details, and variant notes.
   - Video-derived interface files are often richer than documentation because they show real UI state — prioritize video sources for interface content when available.

7. Build entities.json as the knowledge graph emerges
   - As concepts, workflows, or interfaces are added, create entity entries with id, name, type, description, related entities, and file references.
   - Use entities.json to speed updates: when new information arrives, consult entities.json to find all affected files.

8. Gather tribal knowledge via expert interviews
   - Schedule and run structured interviews with the domain expert (the pack owner or SME). Ask targeted questions to elicit edge cases, recent gotchas, and undocumented behaviors: "What do new users get wrong first?" "Describe a time something failed and how you fixed it."
   - Record experts' verbatim answers and then distill them into concepts, workflows, or troubleshooting entries. Mark those entries as expert-sourced.
   - Create `sources/{interview-slug}.md` with timestamp index of topics covered.

9. Build troubleshooting/ from support data
   - Ingest support tickets, forum threads, and incident reports. Extract recurring failure modes, errors, and diagnostic steps into troubleshooting/errors/ and diagnostics/ files.
   - Link these troubleshooting files to workflows and concepts where relevant.

10. Compile FAQ and commercial content
    - Derive FAQ entries from common support questions and expert interviews. Organize by persona or category in faq/.
    - If the pack supports sales or go-to-market scenarios, populate commercial/ with capabilities.md, pricing.md, deployment.md, and security.md using a combination of documentation and conversations with product management.

11. Identify gaps and report them
    - Run an automated gaps analysis: compare expected sections (interfaces, troubleshooting decision trees, workflows for critical tasks) to the current inventory.
    - Cross-reference `sources/` indexes against pack content — identify scenes/pages that were indexed but not yet extracted.
    - Produce a prioritized gap report for the domain expert: what needs expert walkthroughs, missing screens, undocumented error states, or incomplete specs.

12. Maintain entities and cross-references
    - Whenever files are added or updated, update entities.json and relevant _index.md files.
    - Use entities.json for targeted updates when new product info arrives (release notes, patch fixes).

13. Commit, document provenance, and create status reports
    - Commit changes with descriptive messages, including source references.
    - Maintain a pack-level README with guidance for future updates and a changelog of significant content additions.
    - Periodically generate a status summary showing new content, resolved gaps, and outstanding high-priority items.

Practical prompting guidance

- Use concise, task-focused prompts during expert interviews: one question per turn, with specific examples and requests for steps, error messages, or screenshots.
- When extracting from docs, ask for clarifications from the domain expert for ambiguous behavior or undocumented edge cases.
- Present the gap report as a short checklist the expert can act on.

Notes and principles

- The schema is your filing guide — decide where content belongs; create new directories when a new content type is needed and document the change in the manifest.
- Record provenance for every file and never overwrite expert-verified content without reconfirmation.
- Prioritize building troubleshooting/ and interfaces/ early for support readiness; these are high-value for user-facing agents.

---

*Schema version: 1.2*
*Last updated: 2026-02-20*
