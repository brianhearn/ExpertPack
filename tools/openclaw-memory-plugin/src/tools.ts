/**
 * memory_search / memory_get tool registrations.
 *
 * We register these ourselves because memory-core is disabled when its slot
 * is taken by another plugin (see loader.js: kind="memory" plugins that lose
 * the slot decision are skipped entirely). Agents in the host's allowlist
 * still expect `memory_search` and `memory_get` by name; registering thin
 * wrappers keeps the tool surface stable across plugin swaps.
 *
 * We intentionally skip memory-core's advanced features (corpus supplements,
 * short-term recall tracking, citations mode resolution) — those are
 * memory-core-internal conveniences that don't apply to a remote EP MCP pack.
 */

import type { EpMemorySearchManager } from "./search-manager.js";

/**
 * Shape matching @sinclair/typebox's `Type.Object(...)` output, hand-rolled
 * as plain JSON Schema so the plugin has zero runtime dependency on typebox.
 * The host validator (`validateJsonSchemaValue`) accepts this form directly
 * via the `parameters` field.
 */
const MemorySearchSchema = {
  type: "object",
  properties: {
    query: { type: "string" },
    maxResults: { type: "number" },
    minScore: { type: "number" },
  },
  required: ["query"],
  additionalProperties: false,
} as const;

const MemoryGetSchema = {
  type: "object",
  properties: {
    path: { type: "string" },
    from: { type: "number" },
    lines: { type: "number" },
  },
  required: ["path"],
  additionalProperties: false,
} as const;

type ToolResult = {
  content: Array<{ type: "text"; text: string }>;
  details?: Record<string, unknown>;
};

function jsonBlock(payload: unknown): ToolResult {
  const text = JSON.stringify(payload, null, 2);
  return {
    content: [{ type: "text", text }],
    details: payload && typeof payload === "object" ? (payload as Record<string, unknown>) : undefined,
  };
}

export function buildMemorySearchTool(manager: EpMemorySearchManager) {
  return {
    name: "memory_search",
    label: "Memory Search",
    description:
      "Mandatory recall step: semantically search the configured ExpertPack via EP MCP before answering questions about prior work, decisions, dates, people, preferences, or todos. If response has disabled=true, memory retrieval is unavailable and should be surfaced to the user.",
    parameters: MemorySearchSchema,
    async execute(_toolCallId: string, params: Record<string, unknown>): Promise<ToolResult> {
      const query = typeof params.query === "string" ? params.query : "";
      if (!query.trim()) {
        return jsonBlock({ results: [], disabled: true, error: "Missing query" });
      }
      const maxResults = typeof params.maxResults === "number" ? params.maxResults : undefined;
      const minScore = typeof params.minScore === "number" ? params.minScore : undefined;
      try {
        const results = await manager.search(query, {
          maxResults: maxResults ?? undefined,
          minScore: minScore ?? undefined,
        });
        const status = manager.status();
        return jsonBlock({
          results,
          provider: status.provider,
          model: status.model,
          citations: "inline",
          mode: "ep-mcp-remote",
          debug: {
            backend: status.backend,
            hits: results.length,
          },
        });
      } catch (err) {
        return jsonBlock({
          results: [],
          disabled: true,
          error: (err as Error).message ?? "memory search failed",
          warning:
            "Memory search is unavailable due to an EP MCP error. Retry memory_search or check endpoint/apiKey/embedding config.",
        });
      }
    },
  };
}

export function buildMemoryGetTool(manager: EpMemorySearchManager) {
  return {
    name: "memory_get",
    label: "Memory Get",
    description:
      "Safe exact excerpt read from an always-inject local memory file (e.g. SOUL.md, IDENTITY.md). Defaults to a bounded excerpt when lines are omitted; includes truncation info when more content exists. Does NOT read arbitrary pack files — those surface as memory_search snippets.",
    parameters: MemoryGetSchema,
    async execute(_toolCallId: string, params: Record<string, unknown>): Promise<ToolResult> {
      const relPath = typeof params.path === "string" ? params.path : "";
      if (!relPath.trim()) {
        return jsonBlock({ text: "", path: "", error: "Missing path" });
      }
      const from = typeof params.from === "number" ? params.from : undefined;
      const lines = typeof params.lines === "number" ? params.lines : undefined;
      try {
        const res = await manager.readFile({ relPath, from, lines });
        return jsonBlock(res);
      } catch (err) {
        return jsonBlock({
          text: "",
          path: relPath,
          error: (err as Error).message ?? "memory_get failed",
        });
      }
    },
  };
}
