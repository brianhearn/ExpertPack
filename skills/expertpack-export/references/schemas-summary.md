# ExpertPack Schema Summary for Export

Condensed reference for the export scripts. Full schemas at `schemas/` in the ExpertPack repo.

## Pack Types

| Type | Subtype | Purpose |
|------|---------|---------|
| person | (none) | Human knowledge — stories, mind, relationships, presentation |
| person | agent | AI agent identity — operational config, prescriptive mind, tools, safety |
| product | — | Product knowledge — concepts, workflows, interfaces, troubleshooting |
| process | — | Process knowledge — phases, decisions, checklists, gotchas |
| composite | — | Orchestration layer — wires packs together with roles and conflict rules |

## Agent Pack Structure (person, subtype: agent)

```
packs/{agent-slug}/
├── manifest.yaml          # type: person, subtype: agent
├── overview.md            # Identity, personality, vibe
├── MIGRATION.md           # How to hydrate a new instance
├── operational/
│   ├── tools.md           # Tool inventory (shape, not secrets)
│   ├── infrastructure.md  # Hosts, services, topology
│   ├── integrations.md    # Messaging channels, APIs, accounts
│   ├── routines.md        # Heartbeats, backups, cron schedules
│   └── safety.md          # Behavioral contracts, guardrails
├── mind/
│   ├── values.md          # Prescriptive operational principles
│   ├── skills.md          # Capabilities list
│   ├── relational.md      # Interaction rules
│   ├── preferences.md     # Learned formatting/behavior preferences
│   ├── reasoning.md       # Decision patterns
│   └── tensions.md        # Known limitations, failure modes
├── relationships/
│   └── people.md          # Primary user, contacts, peer agents
├── facts/
│   ├── personal.md        # Agent identity facts
│   └── timeline.md        # Significant events
├── presentation/
│   ├── speech-patterns.md # Communication style
│   └── modes.md           # Context-dependent voices
├── summaries/
│   └── lessons.md         # Patterns learned, failure post-mortems
├── meta/
│   └── privacy.md         # Export access tier rules
└── verbatim/              # Optional: significant decisions/conversations
```

## Person Pack Structure (standard)

```
packs/{person-slug}/
├── manifest.yaml          # type: person
├── overview.md
├── facts/                 # personal.md, career.md, education.md, timeline.md
├── relationships/people.md
├── mind/                  # 9 core files + optional reasoning, influences
├── preferences/           # (captured in mind/preferences.md)
├── presentation/          # speech-patterns.md, modes.md
└── meta/privacy.md
```

## Product Pack Structure (Schema v4.1)

```
packs/{product-slug}/
├── manifest.yaml          # type: product, schema_version: "4.1"
├── overview.md
├── concepts/              # Atomic-conceptual files: each carries its definition,
│                          # body, FAQs, related terms, and dependencies in one file
├── workflows/             # Step-by-step procedures (atomic retrieval)
├── interfaces/            # UI/API documentation
├── commercial/            # Pricing, deployment, security
├── troubleshooting/       # Errors, diagnostics, common mistakes
├── faq/                   # Cross-cutting questions only; per-concept FAQs live in concepts/
└── glossary.md            # (Optional) lean cross-cutting terms only
```

*Schema v4.1 (RFC-001) deprecated the `summaries/`, `propositions/`, and `sources/` directories and per-domain `glossary-{domain}.md` files for product packs — concept files are now self-contained retrieval units.*

## Process Pack Structure

```
packs/{process-slug}/
├── manifest.yaml          # type: process
├── overview.md
├── phases/                # Sequential steps
├── decisions/             # Decision points, criteria
├── checklists/            # Verification steps
└── gotchas/               # Common mistakes, edge cases
```

## Composite Manifest

```yaml
name: "Composite Name"
slug: "composite-slug"
type: "composite"
version: "1.0.0"
schema_version: "1.0"
entry_point: "overview.md"

packs:
  - path: "../packs/agent-slug"
    role: voice              # At most one voice pack
  - path: "../packs/person-slug"
    role: knowledge          # Multiple knowledge packs OK
  - path: "../packs/product-slug"
    role: knowledge

conflicts:
  priority: [agent-slug, person-slug, product-slug]
  strategy: "flag"
```

## Key Rules

1. **Markdown canonical** — all knowledge in .md files
2. **Atomic file sizing** — concept atoms target 400–800 tokens with a 1,000-token ceiling; one dominant topic per file
3. **## headers** at natural breaks for RAG chunking
4. **kebab-case** filenames and slugs
5. **No secrets** — never include API keys, tokens, passwords
6. **manifest.yaml required** for every pack
7. **overview.md required** for every pack
8. **Distill, don't copy** — compress raw state into structured knowledge
