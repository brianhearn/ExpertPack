# Interface Vocabulary Reference

*Standardized vocabularies for interface documentation in ExpertPack product packs. Use these in the `Region`, `Type`, and `Location` fields of interface element tables.*

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

---

*Part of the ExpertPack schema. See [product.md](../product.md).*
