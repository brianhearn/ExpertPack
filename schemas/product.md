# Product Pack Schema

*Blueprint for ExpertPacks that capture deep knowledge about a product or platform — concepts, workflows, troubleshooting, and the tribal knowledge that lives in support teams' heads. Applicable to software, hardware, medical devices, consumer products, or any product with enough complexity to benefit from structured expert knowledge. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

A product pack gives an AI agent the same depth of knowledge as a veteran support engineer. Unlike generic RAG over documentation (which is written for humans browsing, not AI reasoning), a product pack structures knowledge around how support interactions actually flow — what things are, how to do things, what went wrong, and what the product costs.

**V1 Goal:** An agent that can *guide humans* through the product — answering questions, walking through workflows, and troubleshooting issues.

**V2 Goal (Future):** An agent that can *operate the product* via browser automation.

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
├── screens/               ← UI documentation (V1+)
│   ├── _index.md          ← Directory of all screens
│   └── {screen}.md        ← One screen per file
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

Step-by-step procedures for accomplishing tasks.

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

- **Where:** {Screen or location}
- **What to click/enter:** {Specific element and value}
- **You should see:** {Expected result}

### 2. {Second Step}
...

## Completion
How to know it worked. What they should see when done.

## Common Issues
- **{Problem}:** {Solution}

## Related
- [Relevant Concept](../concepts/relevant-concept.md)
- [Related Workflow](related-workflow.md)
```

### Screen File (screens/{screen}.md)

UI documentation — every screen in the product.

```markdown
# {Screen Name}

## Purpose
What this screen is for, when users come here.

## How to Get Here
Navigation path(s) to reach this screen.

## Layout

### {Section Name}
Description of this area of the screen.

**Elements:**
| Element | Type | Purpose |
|---------|------|---------|
| {Label} | Button | {What it does} |
| {Label} | Text field | {What data, validation rules} |
| {Label} | Dropdown | {Choices and their meanings} |

## Common Tasks
- [Create a Territory](../workflows/create-territory.md)

## Tips
- Helpful hints for this screen
```

**Element detail guidelines:**
- **Buttons:** What it does, prerequisites, what happens after
- **Text fields:** What data, required/optional, validation, examples
- **Dropdowns:** Choices, what each means, default
- **Checkboxes/toggles:** What it controls, default state, implications
- **Grids:** Columns, row actions available

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
- **deployment.md** — Architecture, requirements, data residency
- **security.md** — Certifications, data protection, authentication
- **capabilities.md** — What it can do, limitations, roadmap

---

## Entity Cross-Reference (entities.json)

`entities.json` is a manually maintained cross-reference index at the pack root. It tells an agent *where to look* when a topic comes up.

### What It Solves

When new information arrives ("capacity planning now supports shift-based scheduling"), the agent needs to:
1. Know that `capacity-planning` is a documented entity
2. Find all files that discuss it — concept, workflows, FAQ mentions
3. Update all relevant files, not just one

Without a cross-reference, the agent would have to search every file — slow, error-prone, and likely to miss mentions in unexpected places.

### Structure

```json
{
  "entities": [
    {
      "id": "capacity-planning",
      "name": "Capacity Planning",
      "type": "core-feature",
      "description": "Modeling workloads and rep capacity to balance territories",
      "related": ["scheduling", "workload-partitioning"],
      "files": {
        "concept": "concepts/capacity-planning.md",
        "workflows": ["workflows/capacity-planning.md"],
        "mentions": ["overview.md", "faq/general.md"]
      }
    }
  ]
}
```

### Entity Types

| Type | Examples |
|------|---------|
| `core-feature` | Territories, Capacity Planning, Routing |
| `integration` | Dynamics 365, Salesforce, Power BI |
| `product` | Sub-products or components |
| `infrastructure` | Authentication, hosting, map providers |
| `category` | Umbrella groupings (e.g., "CRM Integrations") |

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
| **Web docs / help sites** | Concepts, features, basic workflows | Medium — written for browsing, not AI | Low — crawl and restructure |
| **Video tutorials** | UI flow, step-by-step procedures | High — shows actual UI | Medium — transcribe and extract |
| **Screenshots** | Screen layouts, element locations | High — visual ground truth | Medium — requires analysis |
| **Guided walkthroughs** | Edge cases, tribal knowledge | Highest — captures what docs miss | High — requires expert time |
| **Support tickets** | Real user problems, FAQ content | High — real pain points | Medium — requires curation |

### The Crawl → Structure → Refine Pipeline

1. **Crawl** — Scrape product documentation (help sites, docs)
2. **Structure** — Reorganize into pack format (concepts, workflows, commercial, FAQ)
3. **Add headers** — Ensure every file chunks well for RAG
4. **Cross-reference** — Link related concepts and workflows
5. **Build entities.json** — Map entities to their files
6. **Identify gaps** — Screens, troubleshooting, and tribal knowledge are usually missing

This gets you ~70% of V1. The remaining 30% — edge cases, tribal knowledge, undocumented behavior — requires guided walkthroughs with product experts.

---

## Version Roadmap

### V1: Knowledge Layer (Current)

The agent can **guide humans** through the product. It knows what things are, how to do tasks, and what can go wrong. It cannot operate the product autonomously.

**V1 includes:** Concepts, workflows, screens, troubleshooting, FAQ, commercial.

**Success criteria:** Agent with ExpertPack answers support questions better than agent with raw docs alone.

### V2: Automation Layer (Future)

The agent can **operate the product** via browser automation — clicking, typing, navigating. This adds an `automation/` directory:

```
automation/
├── selectors.yaml    ← Element selector registry
├── elements/         ← Per-screen element mappings
└── playbooks/        ← Executable workflows
```

**V2 adds:** CSS selectors, executable playbooks (Playwright/Puppeteer), state verification, visual anchors for fallback detection.

**V2 builds on V1** — all knowledge layer content remains; automation hooks are layered on top.

---

## Creating a New Product Pack

1. Create the directory structure
2. Write `manifest.yaml` with type `product` and the product-specific fields
3. Write `overview.md` — what the product does, who it's for, key capabilities
4. Crawl existing documentation and restructure into `concepts/` and `workflows/`
5. Add `##` section headers to every file for RAG chunking
6. Build `entities.json` as entities emerge
7. Write `_index.md` files for each content directory
8. Add `faq/` from common support questions
9. Add `commercial/` if the pack serves sales scenarios
10. Identify gaps — `troubleshooting/` and `screens/` usually need expert walkthroughs

---

*Schema version: 1.0*
*Last updated: 2026-02-16*
