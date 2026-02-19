# Process Pack Schema

*Blueprint for ExpertPacks that capture a complex process — multi-phase endeavors like building a home, starting a business, or designing a landscape. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

A process pack turns an AI agent into an expert guide for a complex, multi-phase process. Unlike a product pack (which documents a specific tool) or a person pack (which captures a human), a process pack captures the *how-to* of a significant real-world endeavor — the phases, decisions, gotchas, and tribal knowledge that separate experienced practitioners from beginners.

The target user is someone undertaking a process for the first (or second) time who needs structured guidance without hiring a full-time consultant.

**Examples:**
- Architecting and building a new home
- Starting and incorporating a new business
- Creating a professional landscape design
- Planning and executing a kitchen renovation
- Setting up a home recording studio
- Navigating the private pilot certification process

---

## High-level design goals

1. Capture the sequential flow (phases) and the decision points that cause branches.
2. Surface the hard-won heuristics (gotchas) and examples that make novices competent quickly.
3. Provide the operational artifacts people actually need: checklists, templates, budgets, schedules, and regulatory references.
4. Keep files small and focused so RAG retrieves precise chunks (1–3KB per file guideline).
5. Make the pack discoverable via `_index.md` files and manifest-declared context tiers.

---

## Directory Structure (recommended)

```
packs/{process-slug}/
├── manifest.yaml          ← Pack identity and metadata (required)
├── overview.md            ← What this process is, who it's for (required)
│
├── fundamentals/          ← Core concepts & domain knowledge required before starting
├── glossary/              ← Terminology and short definitions (searchable)
├── phases/                ← Sequential stages of the process (backbone)
├── decisions/             ← Key decision points with criteria and tradeoffs
├── checklists/            ← Actionable, phase-aligned checklists
├── scheduling/           ← Timelines, dependencies, lead times, seasonal constraints
├── budget/                ← Cost breakdowns, financing, templates, cost drivers
├── roles/                 ← Stakeholders, responsibilities, how to work with them
├── regulations/           ← Permits, codes, licensing, compliance & region notes
├── templates/             ← Document templates, contracts, applications, forms
├── resources/             ← Tools, vendors, materials, buying guides
├── examples/              ← Case studies and post-mortems
├── gotchas/               ← Common mistakes, traps, and recovery patterns
└── faq/                   ← Frequently asked questions by category
```

Notes:
- Each directory should include `_index.md` describing contents and links to files.
- Files should be named kebab-case and kept focused (one topic per file).
- `fundamentals/` and `glossary/` help novices build mental models before they act.

---

## Manifest Extensions

Process packs extend the [core manifest](core.md) with these fields:

```yaml
# Required
name: "Building a Custom Home"
slug: "custom-home-build"
type: "process"
version: "1.0.0"
description: "Complete guide to architecting and building a custom home"
entry_point: "overview.md"

# Process-specific fields
domain: "construction"              # High-level domain (construction, business, creative, etc.)
typical_duration: "12-18 months"    # Typical timeline
complexity: "high"                  # low | medium | high
cost_range: "$250K–$1M+"           # Approximate cost range (optional)
professional_required: true          # Whether professionals are typically needed
regions: ["US"]                     # Geographic relevance (if applicable)

# Sections included (manifest-driven inventory)
sections:
  - fundamentals
  - glossary
  - phases
  - decisions
  - checklists
  - scheduling
  - budget
  - roles
  - regulations
  - templates
  - resources
  - examples
  - gotchas
  - faq

# Recommended context strategy (manifest context block supported by core.md)
context:
  always:
    - overview.md
    - manifest.yaml
  searchable:
    - fundamentals/
    - glossary/
    - phases/
    - decisions/
    - checklists/
    - resources/
    - roles/
    - regulations/
    - examples/
    - gotchas/
    - faq/
  on_demand:
    - templates/
    - budget/
    - scheduling/
```

---

## Component Templates (high-level)

Below are templates and guidance for the most important directories.

### Overview (`overview.md`)

Keep this short and always-loadable. The agent should load this on every session to understand the pack's scope.

```markdown
# {Process Name}

## What This Process Is
One paragraph describing the end result and who benefits.

## Who This Is For
Primary audience and skill level.

## Typical Duration & Cost
High-level ranges and major cost drivers.

## The Big Picture
Phase sequence and where the tricky bits are.

## When to Get Professional Help
Which parts typically require external experts.
```

### Fundamentals (`fundamentals/{topic}.md`)

Conceptual material that helps the user understand *why* steps exist.

```markdown
# Fundamentals: {Topic}

## What It Is
Short definition and why it matters.

## How It Works
High-level mechanics and mental models.

## Where It Shows Up
Links to phases/decisions where this concept matters.

## Further Reading
Links to deeper resources.
```

### Glossary (`glossary/{term}.md`)

Short, plain-English definitions for domain terms. Useful for RAG when users ask "what is X?".

### Phases (`phases/{phase}.md`)

Phases remain the backbone but now explicitly reference scheduling and budget artifacts.

```markdown
# Phase: {Phase Name}

## Overview
What this phase accomplishes and why it matters.

## When This Happens
Prerequisites and triggers.

## Duration & Lead Times
Typical duration and items with long lead times (e.g., windows, custom cabinets).

## Key Activities
- Activity 1
- Activity 2

## Deliverables
Artifacts produced at the end of the phase.

## Budget Items
Summarize the major budget lines relevant to this phase and link to budget files.

## Checklist
Link to `checklists/{phase}-checklist.md`.

## Common Mistakes
Link to gotchas.
```

### Decisions (`decisions/{decision}.md`)

Decision templates unchanged — emphasize cost, schedule, and risk tradeoffs. Always link to phases and budget impact.

### Checklists (`checklists/{checklist}.md`)

Actionable items with verification steps and sign-off criteria.

### Scheduling (`scheduling/{schedule}.md`)

Guidance on sequencing, parallel work, seasonal constraints, and a few example Gantt templates. Include notes on lead times and supplier SLAs.

### Budget (`budget/{budget-template}.md`)

Breakdowns and templates for estimating and tracking costs. Include example spreadsheets or CSV snippets for ingestion.

### Roles (`roles/{role}.md`)

Define stakeholder roles, scope, how to hire/contract them, typical costs, and what good looks like.

### Regulations (`regulations/{topic}.md`)

Permits, codes, licenses. Include jurisdiction notes and links to authoritative sources. Mark sensitive legal content as guidance, not legal advice.

### Templates (`templates/{template}.md`)

Contracts, purchase orders, RFIs, permit application checklists. Prefer short, editable templates.

### Resources, Examples, Gotchas, FAQ

Keep these as before but follow the small-file guideline. Cross-link heavily.

---

## Agent Consumption Patterns

- Start with `overview.md` (Tier 1) to route the user's question.
- Use `_index.md` files to identify candidate files.
- Prefer `fundamentals/` and `glossary/` for conceptual questions.
- Use `phases/` for step-by-step guidance and `checklists/` for action items.
- Use `decisions/` for tradeoff reasoning and `budget/` and `scheduling/` for planning tasks.
- Load `templates/` and full `budget/` spreadsheets on demand (Tier 3).

---

## Sourcing Guidance

Prioritize practitioner interviews for decisions and gotchas. Use authoritative sources for regulations. Capture real timelines and budgets from case studies in `examples/`.

---

*Schema version: 1.1*
*Last updated: 2026-02-19*
