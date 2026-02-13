# ExpertPack Schema (V1)

## Overview

This document defines the structure of an ExpertPack — a knowledge package that gives AI agents deep product expertise.

**V1 Focus:** Enable agents to *guide humans* through a product (support, sales, training).

---

## Design Principles

1. **Markdown-first** — Human-readable, AI-consumable
2. **Modular** — Break into logical chunks for efficient context loading
3. **Flexible** — One schema, optional sections based on pack focus
4. **Linkable** — Cross-reference between components
5. **Versionable** — Track product version compatibility

---

## Directory Structure

```
packs/
└── {product-name}/
    ├── manifest.yaml          # Pack metadata (required)
    ├── overview.md            # Product overview (required)
    ├── entities.json          # Entity cross-reference index (recommended)
    │
    ├── concepts/              # Mental model, terminology
    │   ├── _index.md
    │   └── {concept}.md
    │
    ├── screens/               # UI documentation
    │   ├── _index.md
    │   └── {screen}.md
    │
    ├── workflows/             # Step-by-step procedures
    │   ├── _index.md
    │   └── {workflow}.md
    │
    ├── troubleshooting/       # Problem resolution
    │   ├── errors/            # Explicit error messages
    │   │   └── {error}.md
    │   ├── diagnostics/       # "Not working as expected" trees
    │   │   └── {issue}.md
    │   └── common-mistakes/   # Gotchas, forgotten steps
    │       └── {mistake}.md
    │
    ├── faq/                   # Common questions
    │   └── {category}.md
    │
    └── commercial/            # Sales/business info (optional)
        ├── pricing.md
        ├── deployment.md
        ├── security.md
        └── capabilities.md
```

**Required:** `manifest.yaml`, `overview.md`
**Everything else:** Optional, based on pack focus

---

## Manifest Schema

```yaml
# manifest.yaml

# Identity
name: "EasyTerritory Designer"
slug: "easyterritory-designer"
version: "1.0.0"
product_version: "2024.1+"
vendor: "EasyTerritory"
website: "https://www.easyterritory.com"
description: "Expert knowledge for EasyTerritory Territory Designer"

# What personas this pack serves
focus:
  - support      # Customer support scenarios
  - sales        # Sales/marketing scenarios
  # - training   # Internal training (future)

# What sections are included (for consumers to know what to expect)
sections:
  - concepts
  - screens
  - workflows
  - troubleshooting
  - faq
  - commercial    # Only if sales focus

# What topics/features are covered
scope:
  - territory-design
  - capacity-planning
  - data-import
  - routing
  - power-bi-integration

# Entry points
entry_point: "overview.md"
index_files: "_index.md"

# Dependencies (other packs required)
dependencies: []
```

---

## Component Templates

### Overview (`overview.md`)

```markdown
# {Product Name}

## What It Is
One paragraph: what the product does, who it's for.

## Key Capabilities
- Capability 1
- Capability 2
- Capability 3

## How It Fits
Where this product sits in the broader ecosystem (other tools, integrations).

## Getting Started
How to access the product, first steps.
```

---

### Concepts (`concepts/{concept}.md`)

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
- [Relevant Screen](../screens/relevant-screen.md)
```

---

### Screens (`screens/{screen}.md`)

Every screen in the product.

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
| {Label} | Dropdown | {What choices, what they mean} |
| {Label} | Grid | {What data it shows} |

### {Another Section}
...

## Common Tasks
- [Create a Territory](../workflows/create-territory.md)
- [Import Data](../workflows/import-data.md)

## Tips
- Helpful hints for this screen
- Things users often miss
```

**Element detail guidelines:**
- **Buttons:** What it does, any prerequisites, what happens after
- **Text fields:** What data, required/optional, validation (length, format), examples
- **Dropdowns:** What choices exist, what each means, default
- **Checkboxes/toggles:** What setting it controls, default state, implications
- **Grids:** What columns, what row actions are available

---

### Workflows (`workflows/{workflow}.md`)

Step-by-step procedures.

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
- **{Problem}:** {Solution}

## Variations
- {Alternative path or option}

## Related
- [Relevant Screen](../screens/relevant-screen.md)
- [Related Workflow](related-workflow.md)
```

---

### Troubleshooting: Errors (`troubleshooting/errors/{error}.md`)

Explicit error messages with resolutions.

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

---

### Troubleshooting: Diagnostics (`troubleshooting/diagnostics/{issue}.md`)

"Not working as expected" decision trees.

```markdown
# {Problem Description}

*"I'm trying to {action} but {unexpected result}."*

## Expected Behavior
What *should* happen when everything is working correctly.

## Diagnostic Questions

### What are you seeing?
- **{Symptom A}** → [Check X](#check-x)
- **{Symptom B}** → [Check Y](#check-y)
- **{Symptom C}** → [Check Z](#check-z)

### Check X
{Diagnostic step}

- **If {result}:** {Resolution or next step}
- **If not:** [Check Y](#check-y)

### Check Y
...

## Common Causes
1. {Cause} — {Quick fix}
2. {Cause} — {Quick fix}

## Still Not Working?
Escalation path or contact info.
```

---

### Troubleshooting: Common Mistakes (`troubleshooting/common-mistakes/{mistake}.md`)

Gotchas, forgotten steps, easy-to-miss things.

```markdown
# {Mistake Description}

## Symptom
What the user experiences when they make this mistake.

## The Mistake
What they did (or didn't do).

## The Fix
How to correct it.

## How to Avoid
What to remember for next time.
```

---

### FAQ (`faq/{category}.md`)

Common questions grouped by topic.

```markdown
# {Category} FAQ

## {Question 1}
{Answer}

## {Question 2}
{Answer}

## {Question 3}
{Answer}
```

---

### Commercial (`commercial/`)

Business information for sales scenarios. Optional section.

#### `pricing.md`
```markdown
# Pricing

## Model
How pricing works (per user, per tier, etc.)

## Tiers
| Tier | Includes | Price |
|------|----------|-------|
| ... | ... | ... |

## What Affects Cost
- Factor 1
- Factor 2

## Common Questions
- Q: ...
- A: ...
```

#### `deployment.md`
```markdown
# Deployment

## Architecture
How the product is deployed (cloud, on-prem, hybrid).

## Requirements
What's needed to run it.

## Data Residency
Where data is stored.

## Integration
How it connects to other systems.
```

#### `security.md`
```markdown
# Security

## Certifications
- SOC 2, ISO 27001, etc.

## Data Protection
How data is secured (encryption, access control).

## Authentication
SSO, MFA, etc.

## Compliance
GDPR, HIPAA, etc.
```

#### `capabilities.md`
```markdown
# Capabilities

## What It Can Do
| Capability | Details |
|------------|---------|
| ... | ... |

## What It Can't Do (Yet)
- Limitation 1
- Limitation 2

## Roadmap Highlights
Upcoming features (if public).
```

---

## Cross-Referencing

Use relative markdown links to connect content:

```markdown
See [Territory Screen](../screens/territory-list.md) for details.
Related workflow: [Create Territory](../workflows/create-territory.md)
```

Index files (`_index.md`) in each folder list and link to all items in that section.

---

## Context Loading Strategy

Packs should be loadable in layers:

1. **Minimal:** `manifest.yaml` + `overview.md` (product awareness)
2. **Topical:** Add specific sections based on query (screens, workflows, etc.)
3. **Full:** Entire pack (comprehensive expertise)

Keep individual files focused and reasonably sized (<2KB each recommended) so loaders can pull just what's needed.

---

## V2: Automation Layer (Future)

V2 adds browser automation capabilities on top of V1 knowledge:

```
packs/
└── {product-name}/
    └── automation/           # V2 addition
        ├── selectors.yaml    # Element selector registry
        ├── elements/         # Per-screen element mappings
        └── playbooks/        # Executable workflows
```

**V2 adds:**
- CSS selectors / data-testid mappings
- Executable playbooks (Playwright/Puppeteer)
- State verification and assertions
- Visual anchors for fallback detection

V2 schema will be defined when we reach that phase.

---

*Last updated: 2026-02-12*
