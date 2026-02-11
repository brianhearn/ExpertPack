# ExpertPack Schema

## Overview

This document defines the structure of an ExpertPack — a knowledge package that gives AI agents deep product/domain expertise.

## Design Principles

1. **Markdown-first** — Human-readable, AI-consumable
2. **Modular** — Break into logical chunks (screens, workflows, concepts)
3. **Linkable** — Cross-reference between components
4. **Versionable** — Track product version compatibility

## Proposed Structure

```
packs/
└── {product-name}/
    ├── manifest.yaml          # Pack metadata
    ├── overview.md            # Product overview, positioning
    ├── concepts/              # Core concepts and terminology
    │   ├── _index.md
    │   └── {concept}.md
    ├── ui/                    # UI documentation
    │   ├── _index.md
    │   ├── screens/
    │   │   └── {screen}.md
    │   ├── dialogs/
    │   │   └── {dialog}.md
    │   └── components/
    │       └── {component}.md
    ├── workflows/             # Step-by-step procedures
    │   ├── _index.md
    │   └── {workflow}.md
    ├── decisions/             # Decision trees / troubleshooting
    │   ├── _index.md
    │   └── {decision}.md
    ├── verticals/             # Industry-specific context
    │   ├── _index.md
    │   └── {industry}.md
    ├── faq/                   # Q&A pairs
    │   ├── _index.md
    │   └── {category}.md
    └── glossary.md            # Terminology definitions
```

## Manifest Schema

```yaml
# manifest.yaml
name: "EasyTerritory Designer"
slug: "easyterritory-designer"
version: "1.0.0"
product_version: "2024.1+"
vendor: "EasyTerritory"
description: "Expert knowledge for EasyTerritory Territory Designer"
website: "https://www.easyterritory.com"

# What this pack covers
scope:
  - territory-design
  - capacity-planning
  - data-import
  - power-bi-integration

# Target use cases
use_cases:
  - customer-support
  - sales-engineering
  - user-training

# Dependencies (other packs required)
dependencies: []

# Pack structure for loaders
structure:
  entry_point: "overview.md"
  index_files: "_index.md"
```

## Component Templates

### Screen Documentation (`ui/screens/{screen}.md`)

```markdown
# {Screen Name}

## Purpose
What this screen is for.

## Access
How to navigate here.

## Layout
Description of major sections/areas.

## Fields/Controls
| Element | Type | Description | Validation |
|---------|------|-------------|------------|
| ... | ... | ... | ... |

## Actions
- **{Button/Action}**: What it does, when to use it

## Common Tasks
- Link to relevant workflows

## Gotchas
- Edge cases, common mistakes
```

### Workflow Documentation (`workflows/{workflow}.md`)

```markdown
# {Workflow Name}

## Goal
What the user is trying to accomplish.

## Prerequisites
- What's needed before starting

## Steps
1. Step one
   - Details, gotchas
2. Step two
   - Details, gotchas

## Variations
- Industry-specific or conditional paths

## Troubleshooting
- Common issues and solutions

## Related
- Links to screens, concepts, other workflows
```

### Decision Tree (`decisions/{decision}.md`)

```markdown
# {Decision/Troubleshooting Topic}

## Situation
When this decision tree applies.

## Questions

### Q1: {First question}
- **Yes** → {Action or next question}
- **No** → {Action or next question}

### Q2: {Second question}
...

## Outcomes
- **{Outcome A}**: What to do
- **{Outcome B}**: What to do
```

---

## Open Items

- [ ] Finalize manifest schema
- [ ] Define linking/cross-reference syntax
- [ ] Define chunking hints for RAG
- [ ] Create validation tooling

---

*Last updated: 2026-02-11*
