# ExpertPack Schema

## Overview

This document defines the structure of an ExpertPack — a knowledge package that gives AI agents deep product/domain expertise.

## Design Principles

1. **Markdown-first** — Human-readable, AI-consumable
2. **Modular** — Break into logical chunks (screens, workflows, concepts)
3. **Linkable** — Cross-reference between components
4. **Versionable** — Track product version compatibility

## Proposed Structure

```
packs/
└── {product-name}/
    ├── manifest.yaml          # Pack metadata
    ├── overview.md            # Product overview, positioning
    ├── concepts/              # Core concepts and terminology
    │   ├── _index.md
    │   └── {concept}.md
    ├── ui/                    # UI documentation
    │   ├── _index.md
    │   ├── screens/
    │   │   └── {screen}.md
    │   ├── dialogs/
    │   │   └── {dialog}.md
    │   └── components/
    │       └── {component}.md
    ├── workflows/             # Step-by-step procedures
    │   ├── _index.md
    │   └── {workflow}.md
    ├── decisions/             # Decision trees / troubleshooting
    │   ├── _index.md
    │   └── {decision}.md
    ├── verticals/             # Industry-specific context
    │   ├── _index.md
    │   └── {industry}.md
    ├── faq/                   # Q&A pairs
    │   ├── _index.md
    │   └── {category}.md
    └── glossary.md            # Terminology definitions
```

## Manifest Schema

```yaml
# manifest.yaml
name: "EasyTerritory Designer"
slug: "easyterritory-designer"
version: "1.0.0"
product_version: "2024.1+"
vendor: "EasyTerritory"
description: "Expert knowledge for EasyTerritory Territory Designer"
website: "https://www.easyterritory.com"

# What this pack covers
scope:
  - territory-design
  - capacity-planning
  - data-import
  - power-bi-integration

# Target use cases
use_cases:
  - customer-support
  - sales-engineering
  - user-training

# Dependencies (other packs required)
dependencies: []

# Pack structure for loaders
structure:
  entry_point: "overview.md"
  index_files: "_index.md"
```

## Component Templates

### Screen Documentation (`ui/screens/{screen}.md`)

```markdown
# {Screen Name}

## Purpose
What this screen is for.

## Access
How to navigate here.

## Layout
Description of major sections/areas.

## Fields/Controls
| Element | Type | Description | Validation |
|---------|------|-------------|------------|
| ... | ... | ... | ... |

## Actions
- **{Button/Action}**: What it does, when to use it

## Common Tasks
- Link to relevant workflows

## Gotchas
- Edge cases, common mistakes
```

### Workflow Documentation (`workflows/{workflow}.md`)

```markdown
# {Workflow Name}

## Goal
What the user is trying to accomplish.

## Prerequisites
- What's needed before starting

## Steps
1. Step one
   - Details, gotchas
2. Step two
   - Details, gotchas

## Variations
- Industry-specific or conditional paths

## Troubleshooting
- Common issues and solutions

## Related
- Links to screens, concepts, other workflows
```

### Decision Tree (`decisions/{decision}.md`)

```markdown
# {Decision/Troubleshooting Topic}

## Situation
When this decision tree applies.

## Questions

### Q1: {First question}
- **Yes** → {Action or next question}
- **No** → {Action or next question}

### Q2: {Second question}
...

## Outcomes
- **{Outcome A}**: What to do
- **{Outcome B}**: What to do
```

---

## UI Automation Layer

For packs that support autonomous agent operation (browser automation), add an `automation/` directory with element registries and executable workflows.

### Directory Structure

```
packs/
└── {product-name}/
    └── automation/
        ├── selectors.yaml       # Global selector conventions
        ├── elements/            # Element registries by screen
        │   └── {screen}.yaml
        └── playbooks/           # Executable workflow scripts
            └── {workflow}.yaml
```

### Selector Conventions (`automation/selectors.yaml`)

Define how elements are identified in the target application:

```yaml
# automation/selectors.yaml
conventions:
  # Primary selector strategy
  primary: "data-testid"
  
  # Attribute format: data-testid="{area}-{element}-{type}"
  # Example: data-testid="territory-list-save-btn"
  pattern: "{area}-{element}-{type}"
  
  # Fallback strategies (in order)
  fallbacks:
    - aria-label
    - id
    - text-content

  # Element type suffixes
  types:
    button: "btn"
    input: "input"
    select: "select"
    checkbox: "chk"
    grid: "grid"
    dialog: "dialog"
    link: "link"
    tab: "tab"
    panel: "panel"

# Framework-specific notes
framework:
  name: "Durandal (Knockout.js)"
  notes: |
    - Add data-testid to Knockout templates
    - Use data-bind alongside data-testid
    - Example: <button data-testid="save-btn" data-bind="click: save">Save</button>
```

### Element Registry (`automation/elements/{screen}.yaml`)

Map semantic elements to selectors:

```yaml
# automation/elements/territory-list.yaml
screen:
  name: "Territory List"
  path: "/territories"
  
elements:
  # Toolbar
  - id: new-territory-btn
    type: button
    label: "New Territory"
    description: "Opens dialog to create a new territory"
    selector:
      primary: "[data-testid='territory-new-btn']"
      fallback: "button:contains('New Territory')"
    action:
      type: opens
      target: territory-create-dialog
      
  - id: import-btn
    type: button
    label: "Import"
    description: "Opens import wizard for bulk territory upload"
    selector:
      primary: "[data-testid='territory-import-btn']"
      
  # Data Grid
  - id: territory-grid
    type: grid
    label: "Territory List"
    description: "Main grid showing all territories"
    selector:
      primary: "[data-testid='territory-grid']"
    columns:
      - name: name
        label: "Territory Name"
        sortable: true
        filterable: true
      - name: assignee
        label: "Assigned Rep"
        sortable: true
        filterable: true
      - name: account_count
        label: "Accounts"
        sortable: true
      - name: revenue
        label: "Revenue"
        sortable: true
        format: currency
    row_actions:
      - id: edit
        label: "Edit"
        selector: "[data-testid='territory-edit-btn']"
      - id: delete
        label: "Delete"
        selector: "[data-testid='territory-delete-btn']"
        confirmation: true

# Visual anchors (for vision-based automation)
visual_anchors:
  - element: new-territory-btn
    region: "top-right toolbar"
    appearance: "Blue primary button"
  - element: territory-grid
    region: "main content area"
    appearance: "Data table with sortable column headers"
```

### Executable Playbooks (`automation/playbooks/{workflow}.yaml`)

Turn workflows into executable scripts:

```yaml
# automation/playbooks/create-territory.yaml
playbook:
  name: "Create Territory"
  description: "Create a new geography-based territory"
  
inputs:
  - name: territory_name
    type: string
    required: true
  - name: geography_type
    type: enum
    options: [postal_code, county, state, country]
    default: postal_code
  - name: geographies
    type: array
    description: "List of geography codes to include"
    required: true
  - name: assignee
    type: string
    required: false

preconditions:
  - screen: territory-list
    description: "Must be on Territory List screen"

steps:
  - id: open-dialog
    action: click
    target: new-territory-btn
    wait_for: territory-create-dialog
    
  - id: enter-name
    action: fill
    target: territory-name-input
    value: "{{territory_name}}"
    
  - id: select-geo-type
    action: select
    target: geography-type-select
    value: "{{geography_type}}"
    
  - id: add-geographies
    action: multi-select
    target: geography-picker
    values: "{{geographies}}"
    
  - id: set-assignee
    action: fill
    target: assignee-input
    value: "{{assignee}}"
    condition: "assignee is not null"
    
  - id: save
    action: click
    target: save-btn
    wait_for:
      type: toast
      message: "Territory created"

postconditions:
  - screen: territory-list
  - assertion: "Territory '{{territory_name}}' appears in grid"

error_handling:
  - condition: "validation error"
    action: capture-screenshot
    then: abort
  - condition: "timeout"
    action: retry
    max_attempts: 2
```

### Adding Selectors to Your Application

For applications without existing test selectors, add `data-testid` attributes to interactive elements:

**Knockout.js (Durandal) Example:**

```html
<!-- Before -->
<button class="btn btn-primary" data-bind="click: createTerritory">
  New Territory
</button>

<!-- After -->
<button class="btn btn-primary" 
        data-testid="territory-new-btn"
        data-bind="click: createTerritory">
  New Territory
</button>
```

**Naming Convention:**
```
{area}-{element}-{type}

Examples:
- territory-new-btn
- territory-name-input  
- territory-grid
- import-wizard-dialog
- settings-save-btn
```

**Priority Elements to Tag:**
1. Primary action buttons (Save, Create, Delete, Submit)
2. Navigation elements (tabs, menu items, breadcrumbs)
3. Form inputs (especially those referenced in workflows)
4. Data grids and their row actions
5. Dialogs and modals
6. Error/success message containers

---

## Open Items

- [ ] Finalize manifest schema
- [ ] Define linking/cross-reference syntax
- [ ] Define chunking hints for RAG
- [ ] Create validation tooling
- [ ] Build playbook executor (Playwright integration)
- [ ] Define visual anchor format for vision-based automation

---

*Last updated: 2026-02-11*
