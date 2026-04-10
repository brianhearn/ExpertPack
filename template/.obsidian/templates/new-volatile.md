---
title: "<% tp.file.title %>"
type: volatile
tags: [volatile, <% tp.file.title.toLowerCase().replace(/ /g, '-') %>]
pack: your-pack-slug
retrieval_strategy: standard
id: "your-pack-slug/volatile/<% tp.file.title.toLowerCase().replace(/ /g, '-') %>"
refresh: P30D
source: ""
fetched_at: "<% tp.date.now('YYYY-MM-DD') %>"
expires_at: "<% tp.date.now('YYYY-MM-DD', 30) %>"
verified_at: "<% tp.date.now('YYYY-MM-DD') %>"
verified_by: "agent"
---

# <% tp.file.title %>

> **⚠️ Volatile content** — expires <% tp.date.now('YYYY-MM-DD', 30) %>. Refresh from: 

