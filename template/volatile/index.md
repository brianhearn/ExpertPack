---
title: "Volatile Content"
type: index
tags: [index, volatile, pack-name]
pack: your-pack-slug
retrieval_strategy: standard
---

# Volatile Content

Time-bound information that changes frequently — pricing, API rate limits, version-specific specs, leaderboards, current product tiers. Isolated here so it can be refreshed without touching the stable content.

**Rule:** If more than ~50% of a file's facts are time-sensitive, put it here with a TTL. If only a few data points are volatile, keep the file in its normal location and use inline `<!-- refresh -->` annotations.

## File Frontmatter for Volatile Files

Every file in this directory should declare a refresh TTL:

```yaml
---
title: "Pricing — Current"
type: volatile
tags: [volatile, pricing, pack-name]
pack: your-pack-slug
retrieval_strategy: standard
refresh: P30D          # ISO 8601 duration — refresh every 30 days
source: "https://example.com/pricing"
fetched_at: "YYYY-MM-DD"
expires_at: "YYYY-MM-DD"
---
```

At session start, the agent checks `expires_at` across all volatile files and flags stale content for refresh.
