#!/usr/bin/env python3
"""
Claim-to-span verifier for ExpertPack eval runs.

Post-retrieval step: for each answer in a completed eval result YAML,
extract the claims made, then check each claim against the retrieved
pack context spans to compute:

  - claim_coverage  (fraction of claims supported by a retrieved span)
  - citation_f1     (precision * recall on citation-to-span alignment)

Usage:
    # Verify a completed eval result file against the pack used to generate it:
    python tools/eval-runner/claim_verifier.py \
        --result results/ezt-designer-2026-04-15.yaml \
        --pack ExpertPacks/ezt-designer

    # Limit to a specific question id:
    python tools/eval-runner/claim_verifier.py \
        --result results/... \
        --pack ... \
        --question-id q001

Output:
    Appends claim_coverage and citation_f1 to each question's detail record,
    adds aggregate scores to the YAML, and prints a summary scorecard.
    Saves an updated result file (overwrites in place, or --output to specify).

Notes:
    - Uses the same OPENROUTER_API_KEY as run_eval.py
    - Claim extraction and span-matching are both LLM-as-judge calls
    - Designed as a standalone post-processor; does not re-run the full eval
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests required. pip install requests")
    sys.exit(1)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_VERIFIER_MODEL = "openai/gpt-4o-mini"

# How many characters of pack context to load per verification call.
# Smaller than the full eval context — we're checking claim support, not answering.
MAX_SPAN_CHARS = 120_000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_api_key() -> str:
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


def call_llm(prompt: str, model: str, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[ERROR] {e}"


def strip_fences(raw: str) -> str:
    """Remove markdown code fences from LLM JSON output."""
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
        if raw.endswith("```"):
            raw = raw[:-3]
    return raw.strip()


def load_pack_spans(pack_path: Path) -> str:
    """Load pack content as a flat string for span matching (truncated)."""
    chunks = []
    total = 0
    for fp in sorted(pack_path.rglob("*.md")):
        if total >= MAX_SPAN_CHARS:
            break
        try:
            content = fp.read_text(encoding="utf-8").strip()
            if len(content) < 10:
                continue
            header = f"\n\n--- {fp.relative_to(pack_path)} ---\n"
            chunk = header + content
            remaining = MAX_SPAN_CHARS - total
            if len(chunk) > remaining:
                chunk = chunk[:remaining] + "\n[truncated]"
            chunks.append(chunk)
            total += len(chunk)
        except Exception:
            pass
    return "".join(chunks)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

EXTRACT_CLAIMS_PROMPT = """\
Extract the distinct factual claims made in the following AI assistant response.
A claim is a single assertable statement of fact (not a question, not a disclaimer).
Skip hedges like "I don't know" or "outside the scope".

Response:
{response}

Return ONLY a JSON array of short claim strings (no markdown fences):
["claim 1", "claim 2", ...]

If the response makes no factual claims (e.g. it only declines), return: []"""


VERIFY_CLAIM_PROMPT = """\
You are checking whether a factual claim is supported by the provided knowledge base spans.

CLAIM: {claim}

KNOWLEDGE BASE SPANS:
{spans}

Does any span in the knowledge base directly support this claim?
Answer with ONLY one of: "supported" or "unsupported"
(supported = the KB contains text that clearly backs the claim;
 unsupported = the claim goes beyond or contradicts what the KB says)"""


# ---------------------------------------------------------------------------
# Core verification
# ---------------------------------------------------------------------------

def verify_question(
    question_result: dict,
    pack_spans: str,
    model: str,
    api_key: str,
    delay: float = 0.5,
) -> dict:
    """Run claim extraction + span verification for a single question result.

    Returns a dict with:
        claims          list[str]
        supported       list[str]
        unsupported     list[str]
        claim_coverage  float  (0.0 – 1.0)
        citation_f1     float  (0.0 – 1.0)
        error           str | None
    """
    # Support both run_eval.py format (response_preview) and legacy format (response)
    response = question_result.get("response_preview") or question_result.get("response", "")
    if not response or response.startswith("[ERROR]") or response.startswith("[HTTP_ERROR]"):
        return {
            "claims": [], "supported": [], "unsupported": [],
            "claim_coverage": None, "citation_f1": None, "error": "no_response",
        }

    # 1. Extract claims
    extract_prompt = EXTRACT_CLAIMS_PROMPT.format(response=response)
    raw_claims = call_llm(extract_prompt, model, api_key)
    if raw_claims.startswith("[ERROR]"):
        return {
            "claims": [], "supported": [], "unsupported": [],
            "claim_coverage": None, "citation_f1": None, "error": raw_claims,
        }

    try:
        claims = json.loads(strip_fences(raw_claims))
        if not isinstance(claims, list):
            claims = []
    except json.JSONDecodeError:
        claims = []

    if not claims:
        # Refusal or no claims — not an error; skip coverage
        return {
            "claims": [], "supported": [], "unsupported": [],
            "claim_coverage": None, "citation_f1": None, "error": None,
        }

    # 2. Verify each claim against spans
    supported = []
    unsupported = []

    for claim in claims:
        time.sleep(delay)
        verify_prompt = VERIFY_CLAIM_PROMPT.format(
            claim=claim,
            spans=pack_spans[:MAX_SPAN_CHARS],
        )
        verdict = call_llm(verify_prompt, model, api_key).lower().strip()
        if "supported" in verdict and "unsupported" not in verdict:
            supported.append(claim)
        else:
            unsupported.append(claim)

    total = len(claims)
    n_supported = len(supported)

    # claim_coverage = fraction of claims supported by a span
    claim_coverage = n_supported / total if total > 0 else None

    # citation_f1:
    #   precision = supported / total claims made  (how much of what we said is grounded)
    #   recall    = supported / total expected facts (how much ground truth we covered)
    # Since we don't have ground-truth citation spans yet, we approximate:
    #   recall ≈ correctness score from the existing judge (proxy for fact coverage)
    #   precision = claim_coverage
    # F1 = 2 * precision * recall / (precision + recall)
    correctness = question_result.get("correctness", 0.0) or 0.0
    precision = claim_coverage if claim_coverage is not None else 0.0
    recall = float(correctness)
    if precision + recall > 0:
        citation_f1 = round(2 * precision * recall / (precision + recall), 3)
    else:
        citation_f1 = 0.0

    return {
        "claims": claims,
        "supported": supported,
        "unsupported": unsupported,
        "claim_coverage": round(claim_coverage, 3) if claim_coverage is not None else None,
        "citation_f1": citation_f1,
        "error": None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_verifier(args):
    result_path = Path(args.result)
    pack_path = Path(args.pack)
    output_path = Path(args.output) if args.output else result_path
    model = args.model or DEFAULT_VERIFIER_MODEL
    question_filter = args.question_id

    if not result_path.exists():
        print(f"Error: result file not found: {result_path}")
        sys.exit(1)
    if not pack_path.exists():
        print(f"Error: pack path not found: {pack_path}")
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found.")
        sys.exit(1)

    with open(result_path) as f:
        result_data = yaml.safe_load(f)

    questions = result_data.get("details", [])
    if not questions:
        print("Error: no question details found in result file.")
        sys.exit(1)

    if question_filter:
        questions = [q for q in questions if q.get("id") == question_filter]
        if not questions:
            print(f"Error: question id '{question_filter}' not found.")
            sys.exit(1)

    print(f"Loading pack spans from {pack_path}...")
    pack_spans = load_pack_spans(pack_path)
    print(f"Loaded {len(pack_spans):,} chars of pack content.")
    print(f"\nVerifier model: {model}")
    print(f"Questions to verify: {len(questions)}\n")

    all_coverages = []
    all_f1s = []

    for i, q in enumerate(questions):
        qid = q.get("id", f"q{i+1}")
        cat = q.get("category", "?")
        print(f"[{i+1}/{len(questions)}] {qid} ({cat})...", end=" ", flush=True)

        vr = verify_question(q, pack_spans, model, api_key, delay=args.delay)

        q["claim_coverage"] = vr["claim_coverage"]
        q["citation_f1"] = vr["citation_f1"]
        q["claims_extracted"] = vr["claims"]
        q["claims_unsupported"] = vr["unsupported"]
        q["verifier_error"] = vr["error"]

        if vr["claim_coverage"] is not None:
            all_coverages.append(vr["claim_coverage"])
        if vr["citation_f1"] is not None and vr["citation_f1"] > 0:
            all_f1s.append(vr["citation_f1"])

        status = (
            f"coverage={vr['claim_coverage']:.2f} f1={vr['citation_f1']:.2f} "
            f"({len(vr['supported'])}/{len(vr['claims'])} claims supported)"
            if vr["claim_coverage"] is not None
            else f"skipped ({vr['error'] or 'no claims'})"
        )
        print(status)

    # Aggregate
    avg_coverage = sum(all_coverages) / len(all_coverages) if all_coverages else None
    avg_f1 = sum(all_f1s) / len(all_f1s) if all_f1s else None

    if "scores" not in result_data:
        result_data["scores"] = {}
    result_data["scores"]["claim_coverage"] = round(avg_coverage, 3) if avg_coverage is not None else None
    result_data["scores"]["citation_f1"] = round(avg_f1, 3) if avg_f1 is not None else None
    result_data["scores"]["verifier_model"] = model

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(result_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n=== CLAIM VERIFICATION SCORECARD ===")
    if avg_coverage is not None:
        print(f"Claim coverage:  {avg_coverage:.1%}  (fraction of claims supported by pack spans)")
    else:
        print("Claim coverage:  n/a (no verifiable responses)")
    if avg_f1 is not None:
        print(f"Citation F1:     {avg_f1:.1%}  (harmonic mean of coverage + correctness)")
    else:
        print("Citation F1:     n/a")
    print(f"\nUpdated result → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack claim-to-span verifier — add claim_coverage and citation_f1 to eval results"
    )
    parser.add_argument("--result", required=True,
                        help="Path to completed eval result YAML (from run_eval.py)")
    parser.add_argument("--pack", required=True,
                        help="Path to the pack used in the eval run")
    parser.add_argument("--model", default=None,
                        help=f"Verifier model (default: {DEFAULT_VERIFIER_MODEL})")
    parser.add_argument("--output", default=None,
                        help="Output path (default: overwrites --result)")
    parser.add_argument("--question-id", default=None,
                        help="Only verify a single question by id")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Seconds between claim verification calls (default: 0.5)")
    args = parser.parse_args()
    run_verifier(args)


if __name__ == "__main__":
    main()
