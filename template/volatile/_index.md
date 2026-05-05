---
title: "Volatile Index"
type: index
tags: [index, volatile, pack-name]
pack: your-pack-slug
retrieval_strategy: navigation
---

# Volatile Content

Time-bound information that changes frequently — pricing, API rate limits, version-specific specs, leaderboards, current product tiers.

Volatile content is isolated here so it can be refreshed without touching stable content. If only a few data points are volatile, keep the file in its normal location and use inline `<!-- refresh -->` annotations.

## File Frontmatter for Volatile Files

Every file in this directory should declare a refresh TTL:

```yaml
---
title: "Pricing — Current"
type: volatile
tags: [volatile, pricing, pack-name]
pack: your-pack-slug
retrieval_strategy: standard
refresh: P30D
source: "https://example.com/pricing"
fetched_at: "YYYY-MM-DD"
expires_at: "YYYY-MM-DD"
---
```

At session start, the agent checks `expires_at` across volatile files and flags stale content for refresh.
