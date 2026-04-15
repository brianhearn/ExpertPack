#!/usr/bin/env python3
"""
ExpertPack Pack-Agnostic Eval Runner

Loads a pack's content as context and runs an eval set against an LLM via OpenRouter.
No agent endpoint required — queries the LLM directly with pack context in the prompt.

Usage:
    python tools/eval-runner/run_eval.py \
        --pack packs/blender-3d \
        --eval packs/blender-3d/eval/benchmark.yaml

    python tools/eval-runner/run_eval.py \
        --pack packs/home-assistant/product \
        --eval packs/home-assistant/product/eval/benchmark.yaml \
        --model openrouter/anthropic/claude-haiku-3 \
        --output results/ha-run-1.yaml

    # Validate eval YAML without making API calls:
    python tools/eval-runner/run_eval.py \
        --pack packs/blender-3d \
        --eval packs/blender-3d/eval/benchmark.yaml \
        --dry-run

Post-processing (claim verification):
    After a run, add claim_coverage and citation_f1 scores:

    python tools/eval-runner/claim_verifier.py \
        --result results/blender-3d-2026-04-15-1200.yaml \
        --pack packs/blender-3d

    This appends claim_coverage and citation_f1 to each question detail
    and to the aggregate scores block in the result YAML.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests required. Install with: pip install requests")
    sys.exit(1)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/openai/gpt-4o-mini"
DEFAULT_JUDGE_MODEL = "openrouter/openai/gpt-4o-mini"

# Max characters of pack context to load (keeps prompts from exploding)
MAX_CONTEXT_CHARS = 80_000

# Files to prioritize when loading pack context
PRIORITY_FILES = [
    "overview.md",
    "glossary.md",
    "manifest.yaml",
]

# Directories to prioritize (loaded before others)
PRIORITY_DIRS = [
    "concepts",
    "workflows",
    "troubleshooting",
    "faq",
    "summaries",
]


# ---------------------------------------------------------------------------
# Pack context loading
# ---------------------------------------------------------------------------

def load_pack_context(pack_path: Path) -> str:
    """
    Load pack markdown files as context string.
    Prioritizes overview, glossary, concepts, workflows, faq, troubleshooting.
    Stops loading when MAX_CONTEXT_CHARS is reached.
    """
    if not pack_path.exists():
        print(f"Error: Pack path does not exist: {pack_path}")
        sys.exit(1)

    chunks = []
    total_chars = 0

    def add_file(fp: Path):
        nonlocal total_chars
        if total_chars >= MAX_CONTEXT_CHARS:
            return
        try:
            content = fp.read_text(encoding="utf-8")
            # Skip empty files and index files
            if len(content.strip()) < 10:
                return
            header = f"\n\n--- FILE: {fp.relative_to(pack_path)} ---\n"
            chunk = header + content
            remaining = MAX_CONTEXT_CHARS - total_chars
            if len(chunk) > remaining:
                chunk = chunk[:remaining] + "\n[...truncated]"
            chunks.append(chunk)
            total_chars += len(chunk)
        except Exception:
            pass

    # Load priority files first
    for fname in PRIORITY_FILES:
        fp = pack_path / fname
        if fp.exists():
            add_file(fp)

    # Load priority directories
    for dname in PRIORITY_DIRS:
        dpath = pack_path / dname
        if dpath.is_dir():
            for fp in sorted(dpath.rglob("*.md")):
                if total_chars < MAX_CONTEXT_CHARS:
                    add_file(fp)

    # Load remaining markdown files
    for fp in sorted(pack_path.rglob("*.md")):
        if total_chars >= MAX_CONTEXT_CHARS:
            break
        # Skip already-loaded priority files
        rel = fp.relative_to(pack_path)
        rel_str = str(rel)
        already_loaded = (
            rel.name in PRIORITY_FILES or
            any(rel_str.startswith(d + "/") for d in PRIORITY_DIRS)
        )
        if not already_loaded:
            add_file(fp)

    if not chunks:
        print(f"Warning: No markdown files found in {pack_path}")

    context = "".join(chunks)
    print(f"Loaded pack context: {len(chunks)} files, {total_chars:,} chars")
    return context


# ---------------------------------------------------------------------------
# Eval YAML loading
# ---------------------------------------------------------------------------

def load_eval_set(path: Path) -> dict:
    """Load and validate eval YAML following schemas/eval.md."""
    if not path.exists():
        print(f"Error: Eval file not found: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    questions = data.get("questions", [])
    if not questions:
        print(f"Error: No questions found in {path}")
        sys.exit(1)

    required_fields = ("id", "question", "expected_answer", "category", "ek_dependent")
    for i, q in enumerate(questions):
        for field in required_fields:
            if field not in q:
                print(f"Error: Question {i+1} (id={q.get('id','?')}) missing required field '{field}'")
                sys.exit(1)

    print(f"Loaded {len(questions)} questions from {path}")
    return data


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Load OpenRouter API key from environment or .env file."""
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key

    for env_path in ["/root/.openclaw/.env", os.path.expanduser("~/.openclaw/.env"), ".env"]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            return key
    return ""


def call_llm(prompt: str, model: str, api_key: str, temperature: float = 0.3) -> dict:
    """Call OpenRouter and return response text + token usage."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        usage = data.get("usage", {})
        return {
            "text": content,
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        }
    except requests.HTTPError as e:
        return {"text": f"[HTTP_ERROR] {e}", "input_tokens": 0, "output_tokens": 0}
    except Exception as e:
        return {"text": f"[ERROR] {e}", "input_tokens": 0, "output_tokens": 0}


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert AI assistant. Use the provided knowledge base context to answer questions accurately.
If a question is outside the scope of the provided knowledge base, say so clearly rather than guessing.
Be concise and factual."""


def build_question_prompt(context: str, question: str) -> str:
    return f"""KNOWLEDGE BASE:
{context}

---

QUESTION: {question}

Answer based on the knowledge base above. If this question is outside the scope of this knowledge base, say: "This question is outside the scope of this knowledge base." """


def build_judge_prompt(question: dict, response: str) -> str:
    """Build scoring prompt for LLM-as-judge."""
    category = question.get("category", "")
    expected = question["expected_answer"]
    required_facts = question.get("required_facts", [])
    anti_hallucination = question.get("anti_hallucination", [])

    is_refusal = category in ("refusal", "out-of-scope")

    facts_section = ""
    if required_facts:
        facts_section = "\nREQUIRED FACTS (must be present for full correctness):\n"
        facts_section += "\n".join(f"- {f}" for f in required_facts)

    anti_section = ""
    if anti_hallucination:
        anti_section = "\nANTI-HALLUCINATION CHECKS (response must NOT contain these):\n"
        anti_section += "\n".join(f"- {f}" for f in anti_hallucination)

    refusal_note = ""
    if is_refusal:
        refusal_note = "\nNOTE: This is an OUT-OF-SCOPE question. The correct behavior is to decline or state it is outside scope."

    return f"""You are an evaluation judge scoring an AI assistant's response.

QUESTION: {question['question']}

EXPECTED ANSWER: {expected}
{facts_section}{anti_section}{refusal_note}

ACTUAL RESPONSE:
{response}

Score the response. Return ONLY valid JSON (no markdown fences):
{{
  "correctness": <float 0.0-1.0, fraction of key facts from expected_answer present in response>,
  "groundedness": <float 0.0-1.0, how well the response sticks to facts vs fabricating>,
  "hallucinations": [<list of specific wrong claims found, or empty list>],
  "refusal_correct": <true if out-of-scope question was properly declined, false if not, null if not out-of-scope>,
  "notes": "<brief explanation>"
}}

Be strict but fair. A fact counts as present if the response conveys the same meaning even if phrased differently."""


# ---------------------------------------------------------------------------
# Main eval loop
# ---------------------------------------------------------------------------

def run_eval(args):
    pack_path = Path(args.pack)
    eval_path = Path(args.eval)
    output_path = Path(args.output) if args.output else Path(
        f"results/{pack_path.name}-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M')}.yaml"
    )

    eval_data = load_eval_set(eval_path)
    questions = eval_data["questions"]

    # Category summary
    categories = {}
    for q in questions:
        cat = q.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    if args.dry_run:
        print("\n=== DRY RUN — validation only, no API calls ===")
        print(f"Pack:       {pack_path}")
        print(f"Eval:       {eval_path}")
        print(f"Questions:  {len(questions)}")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        ek_count = sum(1 for q in questions if q.get("ek_dependent"))
        print(f"EK-dependent: {ek_count}")
        print("\nValidation passed. ✓")
        return

    api_key = load_api_key()
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found. Set it in the environment or /root/.openclaw/.env")
        sys.exit(1)

    pack_context = load_pack_context(pack_path)
    model = args.model or DEFAULT_MODEL
    judge_model = args.judge_model or DEFAULT_JUDGE_MODEL

    print(f"\n=== EVAL RUN ===")
    print(f"Pack:         {pack_path}")
    print(f"Questions:    {len(questions)}")
    print(f"Model:        {model}")
    print(f"Judge:        {judge_model}")
    print(f"Output:       {output_path}")
    print()

    results = []
    total_in_tokens = 0
    total_out_tokens = 0
    total_judge_in = 0
    total_judge_out = 0

    for i, q in enumerate(questions):
        qid = q["id"]
        print(f"[{i+1}/{len(questions)}] {qid} ({q.get('category','?')}): {q['question'][:55]}...", end=" ", flush=True)

        t0 = time.time()
        prompt = build_question_prompt(pack_context, q["question"])
        answer_result = call_llm(prompt, model, api_key, temperature=0.3)
        latency_ms = int((time.time() - t0) * 1000)

        response = answer_result["text"]
        total_in_tokens += answer_result["input_tokens"]
        total_out_tokens += answer_result["output_tokens"]

        if response.startswith("[ERROR]") or response.startswith("[HTTP_ERROR]"):
            print(f"ERROR")
            score = {
                "correctness": 0.0, "groundedness": 0.0,
                "hallucinations": [], "refusal_correct": None,
                "notes": response,
            }
        else:
            judge_prompt = build_judge_prompt(q, response)
            judge_result = call_llm(judge_prompt, judge_model, api_key, temperature=0.0)
            total_judge_in += judge_result["input_tokens"]
            total_judge_out += judge_result["output_tokens"]

            raw = judge_result["text"]
            # Strip markdown fences if present
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(lines[1:])
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

            try:
                score = json.loads(raw)
            except json.JSONDecodeError:
                score = {
                    "correctness": 0.0, "groundedness": 0.0,
                    "hallucinations": [], "refusal_correct": None,
                    "notes": f"Judge returned invalid JSON: {raw[:100]}",
                }

        print(f"correctness={score.get('correctness', '?'):.2f} ({latency_ms}ms)")

        results.append({
            "id": qid,
            "category": q.get("category", ""),
            "ek_dependent": q.get("ek_dependent", False),
            "correctness": round(float(score.get("correctness", 0)), 3),
            "groundedness": round(float(score.get("groundedness", 0)), 3),
            "hallucinations": score.get("hallucinations", []),
            "refusal_correct": score.get("refusal_correct"),
            "latency_ms": latency_ms,
            "response_preview": response[:300],
            "notes": score.get("notes", ""),
        })

        if args.delay > 0 and i < len(questions) - 1:
            time.sleep(args.delay)

    # Aggregate scores
    n = len(results)
    avg_correctness = sum(r["correctness"] for r in results) / n if n else 0
    avg_groundedness = sum(r["groundedness"] for r in results) / n if n else 0
    hallucination_count = sum(1 for r in results if r["hallucinations"])
    hallucination_rate = hallucination_count / n if n else 0

    refusal_qs = [r for r in results if r["category"] in ("refusal", "out-of-scope")]
    refusal_correct = sum(1 for r in refusal_qs if r.get("refusal_correct") is True)
    refusal_accuracy = refusal_correct / len(refusal_qs) if refusal_qs else None

    ek_qs = [r for r in results if r.get("ek_dependent")]
    ek_correctness = sum(r["correctness"] for r in ek_qs) / len(ek_qs) if ek_qs else None

    avg_latency = sum(r["latency_ms"] for r in results) / n if n else 0

    output = {
        "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "pack": str(pack_path),
        "eval_set": str(eval_path),
        "eval_set_version": eval_data.get("version", "1.0"),
        "model": model,
        "judge_model": judge_model,
        "questions_total": n,
        "scores": {
            "correctness": round(avg_correctness, 3),
            "groundedness": round(avg_groundedness, 3),
            "hallucination_rate": round(hallucination_rate, 3),
            "hallucination_count": hallucination_count,
            "refusal_accuracy": round(refusal_accuracy, 3) if refusal_accuracy is not None else None,
            "ek_correctness": round(ek_correctness, 3) if ek_correctness is not None else None,
            "avg_latency_ms": int(avg_latency),
        },
        "tokens": {
            "model_input": total_in_tokens,
            "model_output": total_out_tokens,
            "judge_input": total_judge_in,
            "judge_output": total_judge_out,
            "total": total_in_tokens + total_out_tokens + total_judge_in + total_judge_out,
        },
        "details": results,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n=== SCORECARD ===")
    print(f"Correctness:       {output['scores']['correctness']:.1%}")
    print(f"Groundedness:      {output['scores']['groundedness']:.1%}")
    print(f"Hallucination:     {output['scores']['hallucination_rate']:.1%}  ({hallucination_count}/{n})")
    if refusal_accuracy is not None:
        print(f"Refusal accuracy:  {output['scores']['refusal_accuracy']:.1%}  ({refusal_correct}/{len(refusal_qs)})")
    if ek_correctness is not None:
        print(f"EK correctness:    {output['scores']['ek_correctness']:.1%}  ({len(ek_qs)} EK questions)")
    print(f"Avg latency:       {output['scores']['avg_latency_ms']}ms")
    print(f"Total tokens:      {output['tokens']['total']:,}")
    print(f"\nResults → {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack Eval Runner — measure pack quality via LLM-as-judge"
    )
    parser.add_argument("--pack", required=True,
                        help="Path to pack directory (e.g. packs/blender-3d)")
    parser.add_argument("--eval", required=True,
                        help="Path to eval YAML file (e.g. packs/blender-3d/eval/benchmark.yaml)")
    parser.add_argument("--model", default=None,
                        help=f"Model for answering questions (default: {DEFAULT_MODEL})")
    parser.add_argument("--judge-model", default=None,
                        help=f"Model for LLM-as-judge scoring (default: {DEFAULT_JUDGE_MODEL})")
    parser.add_argument("--output", default=None,
                        help="Output YAML path (default: results/<pack>-<date>.yaml)")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="Seconds to wait between questions (default: 1.0)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate eval YAML and pack path without making API calls")

    args = parser.parse_args()
    run_eval(args)


if __name__ == "__main__":
    main()
