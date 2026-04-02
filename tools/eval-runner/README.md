# ExpertPack Eval Runner (Pack-Agnostic)

Simple Python script to evaluate how well an LLM performs with an ExpertPack loaded as context. Pack-agnostic, uses OpenRouter, no agent/web socket required.

## Installation

```bash
cd /root/.openclaw/workspace/ExpertPack
pip install pyyaml requests
# OPENROUTER_API_KEY should be in /root/.openclaw/.env
```

## Usage

```bash
python tools/eval-runner/run_eval.py \
  --pack packs/blender-3d \
  --eval packs/blender-3d/eval/benchmark.yaml \
  [--model openrouter/openai/gpt-4o-mini]
```

The script:
- Loads all relevant pack files (overview, glossary, key concepts, workflows, etc.)
- Loads eval questions from YAML (following schemas/eval.md)
- For each question: builds prompt with pack context + question, queries LLM via OpenRouter
- Compares response to expected_answer using simple text matching or optional judge
- Outputs structured scorecard with correctness %, hallucination count, refusal accuracy, token usage

## Output Meaning

- **Correctness %**: How often the generated answer matches key facts from expected_answer
- **Hallucination count**: Times the model invented facts not in pack
- **Refusal accuracy**: How well it declines out-of-scope questions (category=refusal)
- **Token usage**: Average input/output tokens per query (cost indicator)
- Per-question details for debugging specific failures

## Writing Your Own Eval YAML

See `schemas/eval.md` for full schema. Minimal fields per question:
- `id`: unique identifier (q001, q002...)
- `question`: the user query
- `expected_answer`: ground truth based on ACTUAL pack content
- `category`: concept | workflow | troubleshooting | gotcha | refusal
- `ek_dependent`: true if this tests esoteric knowledge in the pack

Ground answers in real pack content (read files first). Include 4+ EK-dependent questions and multiple refusal examples.

## Constraints

Only `requests`, `pyyaml`. Standalone, simple.
