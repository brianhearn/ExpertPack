# Interface Vocabulary Reference

*Standardized vocabularies for interface documentation in ExpertPack product packs. Use these in the `Region`, `Type`, `Location`, `Action`, and `State` fields of interface element tables. The full interface file template lives in [product.md](../product.md#interface-file-interfacesinterfacemd).*

---

### Region Taxonomy

Standardized region names for spatial attribution across all interface documents:

| Region ID | Name | Typical Location |
|-----------|------|-----------------|
| `header` | Header Bar | Top of screen, full width |
| `toolbar` | Toolbar | Below header, or within a panel |
| `panel-left` | Left Panel | Left side, collapsible |
| `panel-right` | Right Panel | Right side, collapsible |
| `panel-bottom` | Bottom Panel | Bottom of screen, collapsible |
| `canvas` | Canvas / Main Area | Center, behind panels |
| `overlay` | Overlay / Dialog | Centered modal or popup |
| `statusbar` | Status Bar | Bottom of screen, full width |
| `callout` | Callout / Tooltip | Floating, anchored to element |
| `context-menu` | Context Menu | Floating, anchored to click |

For sub-regions within panels, use hierarchical naming: `panel-left > shapes`, `panel-right > stats`.

### Element Type Vocabulary

Standardized types for the `Type` column in element tables:

| Type | Description |
|------|-------------|
| `icon-button` | Clickable icon (no visible text label) |
| `text-button` | Clickable button with text label |
| `link` | Text hyperlink |
| `icon-link` | Icon that behaves as a link |
| `dropdown` | Select/combo box |
| `text-field` | Text input |
| `search-field` | Text input with search behavior |
| `checkbox` | Toggle checkbox |
| `radio` | Radio button |
| `toggle` | Binary toggle (on/off) |
| `slider` | Range slider |
| `color-swatch` | Color picker/display |
| `label` | Static text label |
| `indicator` | Visual state indicator (highlight, underline, color change) |
| `drag-handle` | Draggable reorder control |
| `tab` | Tab switcher |
| `list-item` | Row in a list (often with its own action icons) |
| `table` | Data grid/table |
| `panel-control` | Panel expand/collapse/resize control |

### Spatial Descriptors

Use consistent language for the `Location` column within a region:

**Horizontal:** `left`, `center`, `right`, `1st`, `2nd`, `3rd` (for icon rows)
**Vertical:** `top`, `middle`, `bottom`, `below {element}`, `above {element}`
**Relative:** `next to {element}`, `inside {group}`, `per-row` (for list items)

For ordered icon/button rows, use ordinal position: "1st icon", "2nd icon", etc. — combined with the element name for clarity.

---

### Action Vocabulary

Use these verbs in the `Action` column so workflow steps and interface tables share a stable language:

| Action | Description |
|--------|-------------|
| `click` | Activate with mouse/tap |
| `select` | Choose an option from a list, menu, tab, or radio group |
| `type` | Enter text or numeric input |
| `toggle` | Switch an on/off control |
| `drag` | Move, resize, reorder, or pan by dragging |
| `hover` | Reveal a tooltip/callout or transient affordance |
| `open` | Opens a panel, dialog, menu, or route |
| `close` | Closes a panel, dialog, menu, or route |
| `submit` | Commits a form/action that may validate or persist data |
| `navigate` | Changes page, view, route, tab, or context |

### State Vocabulary

Use explicit conditions in the `State` column:

| State | Description |
|-------|-------------|
| `enabled` | Available for interaction |
| `disabled` | Visible but unavailable; document why |
| `selected` | Currently active choice/tab/tool |
| `hidden` | Not visible until a condition is met |
| `loading` | Waiting for data/action completion |
| `error` | Shows validation or failure state |
| `empty` | No data/content loaded |
| `dirty` | Unsaved changes exist |
| `readonly` | Visible but not editable |

### Required Element Table

Product interface files should use this element table shape so agents can connect screens to workflows and state changes:

| Element ID | Label | Type | Region | Location | Action | State | Opens/Changes | Used By Workflows | Notes |
|------------|-------|------|--------|----------|--------|-------|---------------|-------------------|-------|
| `{interface}.{element}` | Visible label or accessible name | Vocabulary type | Region ID | Spatial descriptor | Action verb | State + condition | Resulting UI/data change | `[[workflow]]` | Version/applicability/accessibility notes |

**Element ID rules:** stable, kebab-case, scoped to the interface file, and resilient to label-only changes.

**Accessibility notes:** when available, include accessible name, ARIA role, keyboard shortcut, and focus behavior in `Notes`.

**Version applicability:** if an element exists only in some product versions, put the version range in `Notes` and/or source frontmatter.

---

*Part of the ExpertPack schema. See [product.md](../product.md).*
