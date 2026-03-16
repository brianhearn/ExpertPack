---
name: expertpack
description: "Work with ExpertPacks — structured knowledge packs for AI agents. Use when: (1) Loading/consuming an ExpertPack as agent context, (2) Creating or hydrating a new ExpertPack from scratch, (3) Measuring EK (Esoteric Knowledge) ratio via blind probing, (4) Chunking a pack for RAG deployment, (5) Running quality evals against a pack-powered agent, (6) Backing up/exporting an OpenClaw agent's workspace into an ExpertPack. Triggers on: 'expertpack', 'expert pack', 'EK ratio', 'esoteric knowledge', 'knowledge pack', 'pack hydration', 'backup to expertpack', 'export agent knowledge'."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# ExpertPack

Structured knowledge packs for AI agents. Maximize the knowledge your AI is missing.

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack) · [Schema docs](https://expertpack.ai/#schemas)

**Full schemas:** `/path/to/ExpertPack/schemas/` in the repo (core.md, person.md, product.md, process.md, composite.md, eval.md)

## Pack Location

Default directory: `~/expertpacks/`. Check there first, fall back to current workspace. Users can override by specifying a path.

## Actions

### 1. Load / Consume a Pack

1. Read `manifest.yaml` — identify type, version, context tiers
2. Read `overview.md` — understand what the pack covers
3. Load all Tier 1 (always) files into session context
4. For queries: search Tier 2 (searchable) files via RAG or `_index.md` navigation
5. Load Tier 3 (on-demand) only on explicit request (verbatim transcripts, training data)

**OpenClaw RAG config** — add to `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["path/to/pack/.chunks"],
        "chunking": { "tokens": 500, "overlap": 0 },
        "query": {
          "hybrid": {
            "enabled": true,
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": false }
          }
        }
      }
    }
  }
}
```

For detailed platform integration (Cursor, Claude Code, custom APIs, direct context window): read `{skill_dir}/references/consumption.md`.

### 2. Create / Hydrate a Pack

1. Determine pack type: person, product, process, or composite
2. Read `{skill_dir}/references/schemas.md` for structural requirements
3. Scaffold the directory structure per the type schema
4. Create `manifest.yaml` and `overview.md` (both required)
5. Populate content using EK-aware hydration:
   - Blind-probe each extracted fact before filing
   - Full treatment for EK content (the model can't produce it)
   - Compressed scaffolding for GK content (the model already knows it)
   - Skip content with zero EK value
6. Add retrieval layers: `_index.md` per directory, `summaries/`, `propositions/`, `glossary.md`
7. Add `sources/_coverage.md` documenting what was researched

For full hydration methodology, EK triage process, and source prioritization: read `{skill_dir}/references/hydration.md`.

### 3. Measure EK Ratio

Run the blind-probing evaluator:

```bash
python3 {skill_dir}/scripts/eval-ek.py <pack-path> [--models model1,model2] [--sample N] [--output FILE]
```

- Defaults: GPT-4.1-mini, Claude Sonnet 4.6, Gemini 2.0 Flash via OpenRouter
- API key: auto-resolves from OpenClaw auth profiles or `OPENROUTER_API_KEY` env var
- Outputs YAML with per-proposition scores and aggregate EK ratio

**Interpretation:**

| EK Ratio | Meaning |
|----------|---------|
| 0.80+ | Exceptional — almost entirely esoteric |
| 0.60–0.79 | Strong — majority esoteric |
| 0.40–0.59 | Mixed — significant GK padding |
| 0.20–0.39 | Weak — most content already in weights |
| < 0.20 | Minimal value-add |

Add measured ratio to `manifest.yaml`:

```yaml
ek_ratio:
  value: 0.72
  measured: "2026-03-12"
  models: ["gpt-4.1-mini", "claude-sonnet-4-6", "gemini-2.0-flash"]
  propositions_tested: 142
```

### 4. Chunk for RAG

Run the schema-aware chunker:

```bash
python3 {skill_dir}/scripts/chunk.py --pack <pack-path> --output <pack-path>/.chunks
```

- Respects `##` headers, lead summaries, proposition groups, `<!-- refresh -->` metadata
- Each output file = one semantically coherent chunk
- Point OpenClaw RAG at `.chunks/` with overlap=0

**Why this matters:** Schema-aware chunking produced +9.4% correctness and -52% tokens vs. generic chunking in controlled experiments. It's the single highest-impact consumption optimization.

### 5. Run Quality Eval

```bash
python3 {skill_dir}/scripts/run-eval.py \
  --questions <eval-set.yaml> \
  --endpoint <ws://host:port/path> \
  --output <results.yaml> \
  --label "baseline"
```

- Build eval set: 30+ questions (basic, intermediate, advanced, out-of-scope)
- Fix one dimension at a time: structure → agent training → model
- Re-run after each change to verify improvement

Common failure patterns and the eval-driven improvement loop: read `{skill_dir}/references/consumption.md`.

### 6. Backup / Export OpenClaw → ExpertPack

Export an OpenClaw agent's accumulated knowledge into a structured ExpertPack composite.

**Step 1 — Scan:**

```bash
python3 {skill_dir}/scripts/scan.py --workspace <workspace-path> --output /tmp/ep-scan.json
```

Review the scan output with the user. It proposes pack assignments (agent, person, product, process) with confidence scores. Flag ambiguous classifications for user decision.

**Step 2 — Distill** (repeat per pack):

```bash
python3 {skill_dir}/scripts/distill.py \
  --scan /tmp/ep-scan.json \
  --pack <type:slug> \
  --output <export-dir>/packs/<slug>/
```

- Distill, don't copy — target 10-20% volume of raw state
- Strips secrets automatically (API keys, tokens, passwords)
- Deduplicates, prefers newest for conflicts

**Step 3 — Compose:**

```bash
python3 {skill_dir}/scripts/compose.py \
  --scan /tmp/ep-scan.json \
  --export-dir <export-dir>/
```

Generates composite manifest and overview.

**Step 4 — Validate:**

```bash
python3 {skill_dir}/scripts/validate.py --export-dir <export-dir>/
```

Checks: required files exist, manifest fields valid, no secrets leaked, file sizes within guidelines, cross-references resolve.

**Step 5 — Review & ship.** Present validation report to user. They decide whether to commit/push.

**Critical rules:**
- Never include secrets in the export
- Never modify the live workspace — all output goes to the export directory
- Flag personal information for access tier review
- Default user-specific content to `private` access
