---
title: "Pack Dashboard"
type: meta
tags: [dashboard, meta]
pack: your-pack-slug
retrieval_strategy: standard
---

# Pack Dashboard

Live view of your ExpertPack content. Powered by [Dataview](https://github.com/blacksmithgu/obsidian-dataview) — install it from Community Plugins if queries show as code blocks.

---

## 📊 Content by Type

```dataview
TABLE rows.file.link AS Files, length(rows) AS Count
FROM ""
WHERE type != null AND type != "meta" AND type != "index"
GROUP BY type
SORT length(rows) DESC
```

---

## ⚠️ Files Missing Frontmatter

```dataview
LIST
FROM ""
WHERE type = null
AND file.name != "Dashboard"
```

---

## 🔴 Volatile Content — Expiring Soon

```dataview
TABLE title, expires_at, source
FROM "volatile"
WHERE type = "volatile"
SORT expires_at ASC
```

---

## ⚛️ Atomic Files (Workflows + Troubleshooting)

```dataview
TABLE title, type
FROM ""
WHERE retrieval_strategy = "atomic"
SORT type ASC
```

---

## 🏷️ All Tags in Pack

```dataview
TABLE rows.file.link AS Files
FROM ""
WHERE type != null
FLATTEN tags AS tag
GROUP BY tag
SORT tag ASC
```

---

## 📈 EK Scores (where measured)

```dataview
TABLE title, ek_score, type
FROM ""
WHERE ek_score != null
SORT ek_score DESC
```

---

## 📁 File Count by Directory

```dataview
TABLE length(rows) AS Files
FROM ""
WHERE type != null
GROUP BY file.folder
SORT file.folder ASC
```

---

*Dashboard is for authoring visibility only — not loaded as AI context (type: meta).*
