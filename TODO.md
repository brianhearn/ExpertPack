# ExpertPack Framework — TODO

## Guides

- [ ] **Consumption guide** (`guides/consumption-methods.md`) — How an AI agent should load, navigate, and reason over an ExpertPack at query time. Chunking strategy, context window management, entity graph navigation, tier-based loading, when to drill into sources vs. stay at summary level. **BLOCKED: write after deploying a consumer agent on a real pack** (don't speculate — document what we learn). Prerequisite: deploy EZT Designer pack with a consumer agent and collect real observations.

- [ ] **Research: optimal models for pack consumption** — Survey OpenRouter models suited for agent-style pack consumption. Goals: fast, inexpensive, good at structured document reasoning and instruction-following. Opus 4.6 is overkill for a deployed consumer agent. Evaluate candidates on: cost/token, speed, context window, instruction adherence, structured output quality. Consider separate recommendations for different consumption patterns (simple Q&A vs. multi-step troubleshooting vs. workflow guidance).

## Population

- [x] **Population methods guide** (`guides/population-methods.md`) — DONE (2026-02-28). Consolidated all ingestion/population methodology into one guide, removed duplication from schemas (product.md 1.4→1.5, person.md 1.3→1.4, process.md 1.2→1.3).
