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

## Directory Structure

```
packs/{process-slug}/
├── manifest.yaml          ← Pack identity and metadata (required)
├── overview.md            ← What this process is, who it's for (required)
│
├── phases/                ← Sequential stages of the process
│   ├── _index.md          ← Phase overview with sequence and dependencies
│   └── {phase}.md         ← One phase per file
│
├── decisions/             ← Key decision points with criteria and tradeoffs
│   ├── _index.md          ← Directory of all decision points
│   └── {decision}.md      ← One decision per file
│
├── checklists/            ← Actionable items per phase or milestone
│   ├── _index.md          ← Directory of all checklists
│   └── {checklist}.md     ← One checklist per file
│
├── resources/             ← Tools, vendors, materials, references
│   ├── _index.md          ← Directory of resources
│   └── {resource}.md      ← One resource category per file
│
├── examples/              ← Real-world case studies and lessons learned
│   ├── _index.md          ← Directory of examples
│   └── {example}.md       ← One case study per file
│
├── gotchas/               ← Things people miss, common mistakes, warnings
│   ├── _index.md          ← Directory of gotchas
│   └── {gotcha}.md        ← One gotcha per file
│
└── faq/                   ← Common questions grouped by topic
    └── {category}.md      ← One FAQ category per file
```

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
typical_duration: "12-18 months"    # How long the process typically takes
complexity: "high"                  # low | medium | high
cost_range: "$250K–$1M+"           # Approximate cost range (optional)
professional_required: true         # Whether professionals are typically needed
regions: ["US"]                     # Geographic relevance (if applicable)

# Sections included
sections:
  - phases
  - decisions
  - checklists
  - resources
  - examples
  - gotchas
  - faq
```

---

## Component Templates

### Overview (`overview.md`)

```markdown
# {Process Name}

## What This Process Is
One paragraph: what you're trying to accomplish, the end result.

## Who This Is For
Who benefits from this guide — first-time homebuilders, aspiring entrepreneurs, etc.

## How Long It Takes
Typical timeline from start to finish, with caveats.

## What It Costs
Rough cost range and the biggest cost drivers.

## The Big Picture
High-level flow: Phase 1 → Phase 2 → ... → Done.
What makes this process hard or where people typically struggle.

## When to Get Professional Help
Which parts can be DIY vs. where you need experts.
```

### Phases (`phases/{phase}.md`)

Phases are the backbone of a process pack. They represent sequential (or sometimes parallel) stages of the process.

```markdown
# Phase: {Phase Name}

## Overview
What this phase accomplishes and why it matters.

## When This Happens
Where this falls in the overall timeline. Prerequisites from prior phases.

## Duration
Typical time for this phase.

## Key Activities
- Activity 1 — what it involves
- Activity 2 — what it involves
- Activity 3 — what it involves

## Deliverables
What's produced or completed at the end of this phase.

## Key Decisions
- [Decision: {name}](../decisions/{decision}.md) — description
- [Decision: {name}](../decisions/{decision}.md) — description

## Common Mistakes
- Mistake 1 → See [Gotcha: {name}](../gotchas/{gotcha}.md)
- Mistake 2 — brief description

## Checklist
See [{Phase} Checklist](../checklists/{phase}-checklist.md)

## Next Phase
What triggers the transition to the next phase. What must be true before moving on.
```

### Phase Index (`phases/_index.md`)

The phase index is especially important because it captures the *sequence and dependencies* — not just a list.

```markdown
# Phases

Overview of the process phases in order.

## Sequence

1. [Planning](planning.md) — Define scope, budget, and timeline
2. [Design](design.md) — Create plans and specifications
3. [Permitting](permitting.md) — Obtain required approvals
4. [Construction](construction.md) — Build it
5. [Inspection](inspection.md) — Verify compliance and quality
6. [Completion](completion.md) — Final walkthrough and handoff

## Dependencies

- Phases 1–3 are strictly sequential
- Phase 4 may overlap with late Phase 3 (permit amendments)
- Phase 5 occurs at multiple points during Phase 4
```

### Decisions (`decisions/{decision}.md`)

Decision points are where the process branches. These capture the criteria, tradeoffs, and recommendations that an experienced practitioner would share.

```markdown
# Decision: {Decision Name}

## When This Decision Comes Up
What triggers this decision point in the process.

## The Options

### Option A: {Name}
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Best when:** {Circumstances where this is the right choice}

### Option B: {Name}
**Pros / Cons / Best when:** ...

### Option C: {Name} (if applicable)
...

## Recommendation
What an experienced practitioner would usually recommend, and why.

## Cost Impact
How this decision affects budget.

## Timeline Impact
How this decision affects schedule.

## Related
- [Phase: {name}](../phases/{phase}.md) — where this decision occurs
- [Gotcha: {name}](../gotchas/{gotcha}.md) — common mistake related to this decision
```

### Checklists (`checklists/{checklist}.md`)

Actionable, completable items. These are the "don't forget" lists.

```markdown
# Checklist: {Phase or Milestone Name}

## Before Starting
- [ ] Prerequisite 1
- [ ] Prerequisite 2

## During This Phase
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

## Before Moving to Next Phase
- [ ] Verification step 1
- [ ] Sign-off or approval
- [ ] Documentation complete
```

### Resources (`resources/{resource}.md`)

Tools, vendors, materials, and reference information.

```markdown
# Resources: {Category}

## Tools
| Tool | Purpose | Notes |
|------|---------|-------|
| Tool 1 | What it's for | Cost, availability |
| Tool 2 | What it's for | Alternatives |

## Professionals
| Role | When Needed | How to Find | Typical Cost |
|------|-------------|-------------|--------------|
| Architect | Phase 2 | AIA directory | $X–$Y |

## Materials / References
- [Resource 1](url) — description
- [Resource 2](url) — description

## Tips for Choosing
Advice on selecting vendors, tools, or materials.
```

### Examples (`examples/{example}.md`)

Real-world case studies that illustrate the process in action.

```markdown
# Example: {Case Study Title}

## Context
Who did this, when, and what they were trying to accomplish.

## What They Did
How they went through the process — what went well, what didn't.

## Key Decisions
What choices they made and why.

## Lessons Learned
- Lesson 1
- Lesson 2

## What They'd Do Differently
Hindsight insights.

## Timeline & Cost
Actual vs. planned timeline and budget.
```

### Gotchas (`gotchas/{gotcha}.md`)

The hard-won wisdom that separates experience from ignorance. These are the highest-value content in a process pack.

```markdown
# Gotcha: {Short Description}

## The Mistake
What people commonly do wrong.

## Why It Happens
Why this mistake is so common — what makes it non-obvious.

## The Consequence
What goes wrong when you make this mistake.

## How to Avoid It
What to do instead.

## How to Recover
If you've already made the mistake, how to fix it (or can you?).

## Phase
This typically occurs during [Phase: {name}](../phases/{phase}.md).
```

---

## How an Agent Consumes a Process Pack

### Query Routing

| User Question | Where to Look |
|---------------|---------------|
| "What are the steps to...?" | `phases/_index.md` → relevant phase |
| "Should I choose X or Y?" | `decisions/` |
| "What do I need before...?" | `checklists/` |
| "Who should I hire for...?" | `resources/` |
| "What usually goes wrong with...?" | `gotchas/` |
| "Has anyone done this before?" | `examples/` |
| "How long does X take?" | `phases/` (duration section) or `overview.md` |

### Navigation Flow

1. **Start with overview.md** — understand the big picture
2. **Check phases/_index.md** — see the full sequence and where the user is
3. **Load the relevant phase** — get details on current activities
4. **Follow cross-references** — decisions, gotchas, and checklists linked from the phase
5. **Pull resources as needed** — tools, vendors, materials

---

## Process vs. Product vs. Person

| Aspect | Process Pack | Product Pack | Person Pack |
|--------|-------------|-------------|-------------|
| **Organized by** | Sequential phases | Knowledge type (concepts, workflows) | Content type (verbatim, summaries) |
| **Primary dimension** | Time / sequence | Topic / feature | Life domain / theme |
| **Key content** | Decisions, gotchas | Troubleshooting, concepts | Stories, beliefs |
| **Navigation** | Phase → activities → decisions | Feature → concept → workflow | Theme → story → people |
| **Updates** | Process evolves slowly | Product updates frequently | Content grows over time |

---

## Content Sourcing

| Source | Quality | Best For |
|--------|---------|----------|
| Practitioner interviews | Highest — captures real decisions and gotchas | Decisions, gotchas, examples |
| How-to books and guides | Good — structured, comprehensive | Phases, checklists |
| Forum discussions | Medium — real problems, noisy | Gotchas, FAQ |
| Professional association docs | Good — authoritative | Resources, checklists |
| Personal experience | Highest — authentic, specific | Examples, gotchas |
| Regulatory / government docs | Authoritative — dry | Checklists, resources (permits, codes) |

---

## Lessons Learned

### Phases Need Crisp Boundaries
A phase should have a clear entry condition ("you've completed X") and exit condition ("you now have Y"). Without these, the process feels like one continuous blob rather than manageable stages.

### Decisions Are the Highest-Value Content
Anyone can list the steps. What makes a process pack valuable is capturing *why* an experienced person would choose option A over option B. These decisions are where cost, quality, and timeline are won or lost.

### Gotchas Are Hard to Source
People who've been through a process often forget what was hard about it — survivorship bias. The best gotchas come from asking "what surprised you?" rather than "what advice would you give?"

### Checklists Should Be Actionable, Not Aspirational
Each item should be something you can actually check off. "Understand the zoning requirements" is vague. "Download zoning map from county website and verify your parcel's classification" is actionable.

---

*Schema version: 1.0*
*Last updated: 2026-02-16*
