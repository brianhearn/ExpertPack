# ExpertPack Eval Runner

Automated evaluation tool for ExpertPack quality assessment. Sends questions from an eval set to a pack-powered agent endpoint, captures responses, and scores them against expected answers.

## Usage

```bash
python3 run_eval.py \
  --questions /path/to/eval/questions.yaml \
  --endpoint ws://host:port/path \
  --output /path/to/eval/results/YYYY-MM-DD-label.yaml \
  --model "gemini-2.0-flash" \
  --label "baseline-gemini-flash"
```

## Options

| Flag | Required | Description |
|------|----------|-------------|
| `--questions` | Yes | Path to questions.yaml eval set |
| `--endpoint` | Yes | WebSocket or HTTP endpoint for the agent |
| `--output` | Yes | Path to write results YAML |
| `--model` | No | Model name (for metadata; default: from endpoint) |
| `--label` | No | Human-readable label for this run |
| `--judge-model` | No | Model to use for LLM-as-judge scoring (default: openrouter/anthropic/claude-sonnet-4) |
| `--timeout` | No | Per-question timeout in seconds (default: 60) |
| `--delay` | No | Delay between questions in seconds (default: 2) |
| `--dry-run` | No | Parse questions and validate, don't send |
| `--structure-version` | No | Pack version for dimensions metadata |
| `--agent-training-version` | No | Agent training version for dimensions metadata |

## How Scoring Works

### Automated Scoring (LLM-as-Judge)
For each question, the judge model evaluates:
1. **Correctness** — Are the `required_facts` present in the response? (0.0–1.0)
2. **Hallucination** — Does the response contain any `anti_hallucination` violations? (binary)
3. **Groundedness** — Does the response stick to pack knowledge vs. fabricating? (0.0–1.0)
4. **Refusal accuracy** — For out-of-scope questions, did the agent properly decline? (binary)

### What It Does NOT Score
- **Retrieval metrics** — Would need access to the RAG system internals (which chunks were retrieved)
- **Voice fidelity** — Subjective, requires human evaluation
- **Completeness** — Partially automated via required_facts, but subjective depth assessment is human

## Output

Produces a YAML file matching the eval schema format (`schemas/eval.md`), including:
- Aggregate scores across all questions
- Per-question detail with facts present/missing, hallucinations detected
- Dimensions metadata (structure version, model, agent training version)
- Timing and token data where available

## Requirements

- Python 3.10+
- `pyyaml` (pip install pyyaml)
- `websockets` (pip install websockets) — for WebSocket endpoints
- `httpx` (pip install httpx) — for HTTP endpoints
- Access to an LLM API for judge scoring (via OpenRouter or direct)
