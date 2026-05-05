# ExpertPack Ontology Suggest

`ep-ontology-suggest.py` proposes a lightweight ontology from an existing ExpertPack. It is **review-first**: output is suggestions only, not authoritative schema changes.

The tool uses the compact AKS projection from pack Markdown plus existing `requires:` / `related` edges to propose:

- category nodes by content role (`concept`, `workflow`, `failure-mode`, etc.)
- repeated candidate entities/terms with evidence records
- explicit graph edges already present in frontmatter or `_graph.yaml`

## Usage

```bash
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack
python tools/ontology-suggest/ep-ontology-suggest.py /path/to/pack --format json --output suggestions.json
```

Default output is `ontology-suggestions.yaml` in the pack root.

## Review Workflow

1. Run `ep-validate.py --aks` first so the compact projection is complete enough.
2. Run ontology suggest.
3. Review candidate entities and categories.
4. Accept useful entities into a maintained ontology/entity registry.
5. Reject generic tags or accidental capitalized phrases.

Do not ingest suggestions automatically into production retrieval without owner review.
