#!/usr/bin/env python3
"""ep-migrate-3-to-4: ExpertPack schema v3 -> v4 migration planner.

Implements RFC-001 atomic-conceptual chunks migration. Scans an existing
schema v3 pack and produces either:
  - A human-readable migration plan (default, non-destructive)
  - A scaffold of v4 concept files in _schema-v4/ with supersedes: tracking
  - A full in-place migration (with --apply and explicit confirmation)

This tool does NOT auto-decide embed-vs-promote granularity calls. It flags
ambiguous cases for author review and always errs on the side of embedding.

Usage:
  python3 ep-migrate-3-to-4.py /path/to/pack [--plan | --scaffold | --apply]
                                             [--out _schema-v4]
                                             [--verbose]

Modes:
  --plan     (default) Print a migration plan to stdout / _migration-plan.md.
             Read-only. Safe.
  --scaffold Generate v4 concept files in --out directory. Source files
             untouched. Use to review the migration before committing.
  --apply    Apply the migration in place. Deletes deprecated directories,
             rewrites concept files, adds supersedes: frontmatter.
             REQUIRES: git clean working tree + --yes-really flag.

Schema v3 -> v4 mapping:
  summaries/              -> DELETE (opening paragraph of each concept replaces)
  propositions/           -> ABSORB into body prose or ## Key Propositions section
  faq/{cat}.md            -> SPLIT per-question into primary concepts' ## Frequently Asked
  glossary-{domain}.md    -> SPLIT: standalone terms -> promote, relative terms -> embed
  sources/                -> DELETE (already deprecated in v3.x)
  lead-summary blockquote -> REMOVE (opening paragraph IS the summary)

See schemas/rfcs/RFC-001-atomic-conceptual-chunks.md for the full spec
and schemas/references/granularity-guide.md for the embed-vs-promote rules.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ---------- Deprecated patterns (RFC-001) ----------

DEPRECATED_DIRS = ("summaries", "propositions", "sources")
DEPRECATED_FILE_GLOBS = ("glossary-*.md",)
DEPRECATED_FAQ_DIR = "faq"
LEAD_SUMMARY_BLOCKQUOTE_RE = re.compile(
    r"\A(\s*)>\s*\*\*Summary\*\*[:\s].*?(?=\n(?:\S|$))", re.DOTALL | re.IGNORECASE
)

# Size thresholds (RFC-001 §Size targets)
SIZE_SOFT_MAX = 900
SIZE_HARD_MAX = 1500
SIZE_PROMOTE_MIN = 200  # below this, prefer embedding over promoting

TOKEN_CHAR_RATIO = 4.0  # rough chars-per-token for token estimation


# ---------- Data model ----------


@dataclass
class FileRecord:
    path: Path
    rel: str
    size_chars: int
    est_tokens: int
    frontmatter: dict
    body: str
    heading_count: int
    has_lead_blockquote: bool


@dataclass
class MigrationPlan:
    pack_root: Path
    deprecations: list[str] = field(default_factory=list)  # files to delete
    faq_moves: list[tuple[str, str, str]] = field(default_factory=list)  # (faq_file, question, target_concept)
    glossary_reviews: list[tuple[str, str, str]] = field(default_factory=list)  # (term, source, suggested_home)
    lead_blockquote_removals: list[str] = field(default_factory=list)
    concept_renames: list[tuple[str, str]] = field(default_factory=list)  # (old, new)
    oversized_files: list[tuple[str, int]] = field(default_factory=list)
    orphan_terms: list[str] = field(default_factory=list)  # glossary terms with no clear home
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "deprecations": len(self.deprecations),
            "faq_moves": len(self.faq_moves),
            "glossary_reviews": len(self.glossary_reviews),
            "lead_blockquote_removals": len(self.lead_blockquote_removals),
            "concept_renames": len(self.concept_renames),
            "oversized_files": len(self.oversized_files),
            "orphan_terms": len(self.orphan_terms),
            "warnings": len(self.warnings),
        }


# ---------- Utilities ----------


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Empty dict if no frontmatter."""
    if not content.startswith("---\n"):
        return {}, content
    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[4:end]) or {}
    except yaml.YAMLError:
        fm = {}
    body = content[end + 5:]
    return fm, body


def estimate_tokens(text: str) -> int:
    return int(len(text) / TOKEN_CHAR_RATIO)


def scan_file(path: Path, pack_root: Path) -> FileRecord:
    raw = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(raw)
    heading_count = len(re.findall(r"^#{2,3}\s", body, re.MULTILINE))
    has_blockquote = bool(LEAD_SUMMARY_BLOCKQUOTE_RE.match(body.lstrip("\n")))
    return FileRecord(
        path=path,
        rel=str(path.relative_to(pack_root)),
        size_chars=len(raw),
        est_tokens=estimate_tokens(raw),
        frontmatter=fm,
        body=body,
        heading_count=heading_count,
        has_lead_blockquote=has_blockquote,
    )


def find_concept_files(pack_root: Path) -> list[FileRecord]:
    concepts_dir = pack_root / "concepts"
    if not concepts_dir.is_dir():
        return []
    files = []
    for p in sorted(concepts_dir.rglob("*.md")):
        if p.name == "_index.md":
            continue
        files.append(scan_file(p, pack_root))
    return files


def find_glossary_files(pack_root: Path) -> list[Path]:
    return sorted(p for p in pack_root.glob("glossary-*.md") if p.is_file())


def find_faq_files(pack_root: Path) -> list[Path]:
    faq_dir = pack_root / "faq"
    if not faq_dir.is_dir():
        return []
    return sorted(p for p in faq_dir.rglob("*.md") if p.name != "_index.md")


def find_deprecated_dirs(pack_root: Path) -> list[Path]:
    return [pack_root / d for d in DEPRECATED_DIRS if (pack_root / d).is_dir()]


# ---------- Matching heuristics ----------


def extract_glossary_terms(path: Path) -> list[tuple[str, str]]:
    """Parse a glossary file, return list of (term, definition_text).

    Handles three common glossary formats:
      - Markdown tables with **Term** in the first column
      - Bulleted lists (`- **Term**: definition`)
      - H3 heading per term
    """
    raw = path.read_text(encoding="utf-8", errors="replace")
    _, body = parse_frontmatter(raw)
    terms: list[tuple[str, str]] = []

    # Table rows: | **Term** | Definition | ... |
    table_re = re.compile(
        r"^\|\s*\*\*([^*|]+?)\*\*\s*\|\s*([^|]+?)\s*\|",
        re.MULTILINE,
    )
    for m in table_re.finditer(body):
        term = m.group(1).strip()
        defn = m.group(2).strip()
        # Skip the header separator row (all dashes)
        if re.match(r"^[-:]+$", defn):
            continue
        terms.append((term, defn))

    # Bullet-list entries: - **Term**: definition
    bullet_re = re.compile(
        r"^\s*[-*]\s+\*\*([^*]+?)\*\*\s*[:\u2014–-]\s*(.+?)(?=\n\s*[-*]|\n\n|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    for m in bullet_re.finditer(body):
        terms.append((m.group(1).strip(), m.group(2).strip()))

    # H3 headings: ### Term\ndefinition
    heading_re = re.compile(r"^###\s+(.+?)\n(.+?)(?=\n###|\Z)", re.DOTALL | re.MULTILINE)
    for m in heading_re.finditer(body):
        terms.append((m.group(1).strip(), m.group(2).strip()))

    # Deduplicate by term (keep longest definition)
    by_term: dict[str, str] = {}
    for t, d in terms:
        if t not in by_term or len(d) > len(by_term[t]):
            by_term[t] = d
    return list(by_term.items())


def extract_faq_questions(path: Path) -> list[tuple[str, str]]:
    """Parse an FAQ file, return list of (question, answer_text)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    _, body = parse_frontmatter(raw)
    out = []
    # Pattern: ## Question or ### Question followed by answer text
    q_re = re.compile(r"^#{2,3}\s+(.+?)\n(.+?)(?=\n#{2,3}\s|\Z)", re.DOTALL | re.MULTILINE)
    for m in q_re.finditer(body):
        q = m.group(1).strip()
        a = m.group(2).strip()
        # Skip non-question headings (no "?" and doesn't start with common Q-words)
        if "?" not in q and not re.match(r"(how|what|why|when|where|who|which|can|does|do|is|are|should)\b",
                                          q, re.IGNORECASE):
            continue
        out.append((q, a))
    return out


def suggest_concept_home(term_or_question: str, answer_or_def: str,
                          concepts: list[FileRecord]) -> Optional[str]:
    """Heuristic: pick the concept file whose title or tags most overlap."""
    text = (term_or_question + " " + answer_or_def).lower()
    best: tuple[int, Optional[str]] = (0, None)
    for c in concepts:
        title = str(c.frontmatter.get("title", "")).lower()
        tags = [str(t).lower() for t in (c.frontmatter.get("tags") or [])]
        slug = c.path.stem.lower().lstrip("con-")
        score = 0
        for tok in re.findall(r"\b\w{4,}\b", title):
            if tok in text:
                score += 3
        for tag in tags:
            if tag in text:
                score += 2
        for tok in slug.replace("-", " ").split():
            if len(tok) >= 4 and tok in text:
                score += 1
        if score > best[0]:
            best = (score, c.path.stem)
    return best[1] if best[0] >= 3 else None


def is_standalone_term(term: str, definition: str) -> bool:
    """Very rough heuristic for whether a glossary term earns its own concept.
    Conservative: defaults to False (embed). Only promotes if the definition
    is long and self-contained.
    """
    if len(definition) < 300:
        return False
    # References to a parent concept suggest relative definition
    relative_markers = [" in the context of", " within ", " of a territory", " of a partition"]
    if any(m in definition.lower() for m in relative_markers):
        return False
    return len(definition) >= 500


# ---------- Plan construction ----------


def build_plan(pack_root: Path) -> MigrationPlan:
    plan = MigrationPlan(pack_root=pack_root)

    # 1. Deprecated directories
    for d in find_deprecated_dirs(pack_root):
        for p in sorted(d.rglob("*.md")):
            plan.deprecations.append(str(p.relative_to(pack_root)))

    concepts = find_concept_files(pack_root)

    # 2. FAQ moves
    for faq_path in find_faq_files(pack_root):
        qs = extract_faq_questions(faq_path)
        if not qs:
            plan.warnings.append(f"FAQ file {faq_path.relative_to(pack_root)} has no parseable Q/A pairs")
            continue
        for q, a in qs:
            target = suggest_concept_home(q, a, concepts)
            if target:
                plan.faq_moves.append((str(faq_path.relative_to(pack_root)), q, target))
            else:
                plan.faq_moves.append((str(faq_path.relative_to(pack_root)), q, "<UNMATCHED>"))

    # 3. Glossary terms
    for gloss_path in find_glossary_files(pack_root):
        terms = extract_glossary_terms(gloss_path)
        if not terms:
            plan.warnings.append(f"Glossary {gloss_path.name} has no parseable terms")
            continue
        for term, defn in terms:
            if is_standalone_term(term, defn):
                # Suggest a new concept file
                slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
                plan.glossary_reviews.append(
                    (term, str(gloss_path.relative_to(pack_root)), f"PROMOTE -> concepts/{slug}.md")
                )
            else:
                home = suggest_concept_home(term, defn, concepts)
                if home:
                    plan.glossary_reviews.append(
                        (term, str(gloss_path.relative_to(pack_root)),
                         f"EMBED -> concepts/{home}.md ## Related Terms")
                    )
                else:
                    plan.orphan_terms.append(f"{term} (from {gloss_path.name})")

    # 4. Lead blockquote removals + oversized concepts
    for c in concepts:
        if c.has_lead_blockquote:
            plan.lead_blockquote_removals.append(c.rel)
        if c.est_tokens > SIZE_HARD_MAX:
            plan.oversized_files.append((c.rel, c.est_tokens))

    # 5. Concept file renames (drop con- prefix per v4 convention)
    for c in concepts:
        stem = c.path.stem
        if stem.startswith("con-"):
            new_stem = stem[4:]
            plan.concept_renames.append((c.rel, f"concepts/{new_stem}.md"))

    return plan


# ---------- Plan rendering ----------


def render_plan_md(plan: MigrationPlan) -> str:
    s = plan.summary()
    lines = [
        "# Schema v3 -> v4 Migration Plan",
        "",
        f"Pack root: `{plan.pack_root}`",
        "",
        "## Summary",
        "",
        f"- {s['deprecations']} files in deprecated directories (summaries/, propositions/, sources/)",
        f"- {s['faq_moves']} FAQ Q/A pairs to relocate into concept files",
        f"- {s['glossary_reviews']} glossary terms needing embed/promote decisions",
        f"- {s['lead_blockquote_removals']} files with lead-summary blockquotes to remove",
        f"- {s['concept_renames']} concept files to rename (drop `con-` prefix)",
        f"- {s['oversized_files']} concept files above 1,500 token ceiling",
        f"- {s['orphan_terms']} glossary terms with no clear concept home",
        f"- {s['warnings']} warnings",
        "",
        "---",
        "",
        "## 1. Deprecated directories (DELETE)",
        "",
    ]
    if plan.deprecations:
        lines.append("The following files will be deleted when --apply is run. Their knowledge")
        lines.append("either already lives in concept files, or should be absorbed before deletion.")
        lines.append("")
        for rel in plan.deprecations[:50]:
            lines.append(f"- `{rel}`")
        if len(plan.deprecations) > 50:
            lines.append(f"- ...and {len(plan.deprecations) - 50} more")
    else:
        lines.append("_None found._")

    lines.extend(["", "## 2. FAQ relocations", ""])
    if plan.faq_moves:
        lines.append("Each Q/A should move into the primary concept file's `## Frequently Asked` section.")
        lines.append("Review the `<UNMATCHED>` rows manually \u2014 those need author judgment.")
        lines.append("")
        by_target: dict[str, list[tuple[str, str]]] = {}
        for src, q, target in plan.faq_moves:
            by_target.setdefault(target, []).append((src, q))
        for target in sorted(by_target.keys()):
            lines.append(f"### -> {target}")
            for src, q in by_target[target]:
                lines.append(f"- from `{src}`: {q}")
            lines.append("")
    else:
        lines.append("_No FAQ files found._")

    lines.extend(["", "## 3. Glossary term decisions", ""])
    if plan.glossary_reviews:
        lines.append("Each term needs an embed-vs-promote decision. Heuristic suggestions below;")
        lines.append("override per the granularity guide if needed.")
        lines.append("")
        promotes = [r for r in plan.glossary_reviews if r[2].startswith("PROMOTE")]
        embeds = [r for r in plan.glossary_reviews if r[2].startswith("EMBED")]
        if promotes:
            lines.append("### Suggested promotions (standalone concepts)")
            for term, src, action in promotes:
                lines.append(f"- **{term}** (from `{src}`) -> {action}")
            lines.append("")
        if embeds:
            lines.append("### Suggested embeds (related terms)")
            for term, src, action in embeds:
                lines.append(f"- **{term}** (from `{src}`) -> {action}")
            lines.append("")
    else:
        lines.append("_No glossary files found._")

    if plan.orphan_terms:
        lines.extend(["## 4. Orphan glossary terms (need manual homing)", ""])
        for t in plan.orphan_terms:
            lines.append(f"- {t}")
        lines.append("")

    if plan.lead_blockquote_removals:
        lines.extend(["## 5. Lead-summary blockquote removals", "",
                      "These concept files have a `> **Summary:**` blockquote at the top that should be",
                      "replaced by a retriever-friendly opening paragraph.", ""])
        for rel in plan.lead_blockquote_removals:
            lines.append(f"- `{rel}`")
        lines.append("")

    if plan.concept_renames:
        lines.extend(["## 6. Concept file renames (drop `con-` prefix)", "",
                      "Schema v4 drops the `con-` directory prefix on concept files",
                      "(filename uniqueness is already enforced by the pack-level prefix registry).", ""])
        for old, new in plan.concept_renames[:30]:
            lines.append(f"- `{old}` -> `{new}`")
        if len(plan.concept_renames) > 30:
            lines.append(f"- ...and {len(plan.concept_renames) - 30} more")
        lines.append("")

    if plan.oversized_files:
        lines.extend(["## 7. Oversized concept files (above 1,500 token ceiling)", "",
                      "These exceed the hard ceiling and must be split at `##` boundaries",
                      "or decomposed into parent+child concepts via `concept_scope: composite`.", ""])
        for rel, tokens in plan.oversized_files:
            lines.append(f"- `{rel}` (~{tokens} tokens)")
        lines.append("")

    if plan.warnings:
        lines.extend(["## Warnings", ""])
        for w in plan.warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Next steps",
        "",
        "1. **Review** this plan end-to-end. Resolve `<UNMATCHED>` FAQ rows and orphan terms.",
        "2. **Override** any embed/promote suggestions you disagree with.",
        "3. Run with `--scaffold` to generate v4 files in `_schema-v4/` for side-by-side review.",
        "4. Once satisfied, run with `--apply --yes-really` on a clean git working tree.",
        "5. Run `ep-validate` on the migrated pack to catch residual issues.",
        "",
        "See [RFC-001](../../schemas/rfcs/RFC-001-atomic-conceptual-chunks.md) and the",
        "[granularity guide](../../schemas/references/granularity-guide.md) for full context.",
        "",
    ])

    return "\n".join(lines)


# ---------- Main ----------


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack", type=Path, help="Path to the ExpertPack root")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", default=True, help="Produce a migration plan (default, read-only)")
    mode.add_argument("--scaffold", action="store_true", help="Generate v4 files in --out (not yet implemented)")
    mode.add_argument("--apply", action="store_true", help="Apply migration in place (not yet implemented)")
    ap.add_argument("--out", type=Path, default=None, help="Output directory for --scaffold (default: <pack>/_schema-v4)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--yes-really", action="store_true", help="Required for --apply")
    args = ap.parse_args()

    pack_root = args.pack.resolve()
    if not pack_root.is_dir():
        print(f"ERROR: pack path is not a directory: {pack_root}", file=sys.stderr)
        sys.exit(2)
    if not (pack_root / "manifest.yaml").is_file():
        print(f"ERROR: no manifest.yaml at {pack_root} - is this an ExpertPack?", file=sys.stderr)
        sys.exit(2)

    plan = build_plan(pack_root)

    if args.scaffold:
        print("ERROR: --scaffold is not yet implemented. Use --plan for now, then refactor manually",
              file=sys.stderr)
        print("       per the plan. Scaffolding will land in a follow-up once the plan format stabilizes.",
              file=sys.stderr)
        sys.exit(3)

    if args.apply:
        print("ERROR: --apply is not yet implemented. Review the plan, refactor manually,",
              file=sys.stderr)
        print("       and run ep-validate on the result. Bulk --apply will land after the",
              file=sys.stderr)
        print("       first real migration proves out the plan format.", file=sys.stderr)
        sys.exit(3)

    # Default: render plan
    md = render_plan_md(plan)
    out_path = pack_root / "_migration-plan.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote migration plan to: {out_path}")
    print()
    print("Summary:")
    for k, v in plan.summary().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
