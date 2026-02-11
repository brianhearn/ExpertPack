# ExpertPack

AI Agent training datasets for instant domain specialization.

## What is an ExpertPack?

An ExpertPack is a structured knowledge package that gives AI agents deep expertise in a specific product or domain — the kind of expertise that frontier models don't have because it's not in their training data.

Unlike generic RAG (stuffing docs into vectors), ExpertPacks capture:
- **UI knowledge** — every screen, form, dialog, and action
- **Workflows** — step-by-step procedures for common tasks
- **Decision trees** — conditional logic ("if X, then Y")
- **Industry context** — how the product is used in different verticals
- **Tribal knowledge** — the stuff that lives in support teams' heads

## Repository Structure

```
ExpertPack/
├── docs/                    # Requirements, guides, specs
│   ├── REQUIREMENTS.md      # Project requirements
│   └── SCHEMA.md            # Schema documentation
├── schema/                  # Schema definitions
│   └── expertpack.schema.json
└── packs/                   # Actual ExpertPacks
    └── easyterritory-designer/
```

## Status

🚧 **Early development** — defining requirements and schema.

## License

TBD
