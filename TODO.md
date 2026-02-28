# ExpertPack Framework — TODO

## Guides

- [ ] **Consumption guide** (`guides/consumption-methods.md`) — How an AI agent should load, navigate, and reason over an ExpertPack at query time. Chunking strategy, context window management, entity graph navigation, tier-based loading, when to drill into sources vs. stay at summary level. Capture lessons as we learn them from real deployments.

- [ ] **Research: optimal models for pack consumption** — Survey OpenRouter models suited for agent-style pack consumption. Goals: fast, inexpensive, good at structured document reasoning and instruction-following. Opus 4.6 is overkill for a deployed consumer agent. Evaluate candidates on: cost/token, speed, context window, instruction adherence, structured output quality. Consider separate recommendations for different consumption patterns (simple Q&A vs. multi-step troubleshooting vs. workflow guidance).

## Population

- [ ] **Population methods guide** (`guides/population-methods.md`) — IN PROGRESS. Consolidate all ingestion/population methodology into one guide, remove duplication from schemas.
