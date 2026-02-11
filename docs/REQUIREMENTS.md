# ExpertPack Requirements

## Vision

Enable AI agents to become instant experts in complex products/domains by loading structured knowledge packs — no fine-tuning required.

**Long-term goal:** An AI agent that can operate the application autonomously, as well as a trained human user.

## Goals

1. **Instant specialization** — Load a pack, agent becomes an expert
2. **Platform-agnostic** — Works with OpenClaw, LangChain, custom agents, etc.
3. **Maintainable** — Easy to update as products evolve
4. **Comprehensive** — Goes beyond docs to capture real expertise
5. **Automation-ready** — Structured for eventual autonomous operation

---

## Development Phases

### Phase 1: Knowledge Layer (Current)
**Goal:** Agent can understand and guide humans through the product.

- Semantic documentation of screens, concepts, workflows
- Natural language descriptions of UI and purpose
- Decision trees for troubleshooting
- Q&A pairs for common questions

**Agent capability:** "Let me explain how to create a territory..." / "Go to the Territory List screen and click New Territory..."

### Phase 2: UI Mapping Layer
**Goal:** Agent knows exactly what elements exist and where.

- Element registry with stable selectors (data-testid)
- Field metadata: purpose, validation, expected values
- Screen state awareness (what's visible when)
- Navigation maps (how to get from A to B)

**Agent capability:** "The Territory Name field accepts alphanumeric characters, max 100 chars. It's required."

### Phase 3: Execution Layer
**Goal:** Agent can perform actions via browser automation.

- Executable playbooks (Playwright/Puppeteer integration)
- Input/output contracts for workflows
- Error detection and recovery
- State verification (did the action succeed?)

**Agent capability:** "I'll create that territory for you now..." *[performs clicks and inputs]*

### Phase 4: Vision & Adaptation Layer
**Goal:** Agent can operate even when UI changes or selectors break.

- Visual anchors (screenshots, region descriptions)
- Vision model integration for element detection
- Self-healing selectors (fallback strategies)
- Anomaly detection ("this screen looks different than expected")

**Agent capability:** *[UI changed after update]* "I notice the button moved, but I can still find it..."

---

## Use Cases

### Primary: Customer Support Agent
- Answer product questions with deep accuracy
- Guide users through complex workflows
- Troubleshoot issues using decision trees
- Know every screen, field, and edge case

### Secondary: Sales Engineering
- Demo assistance with accurate product knowledge
- Answer technical questions during sales calls
- Provide industry-specific use case examples

### Tertiary: Internal Training
- Onboard new employees faster
- Consistent knowledge transfer
- Living documentation that stays current

### Future: Autonomous Operator
- Perform routine tasks on behalf of users
- Data entry and bulk operations
- Scheduled maintenance workflows
- "Do this for me" delegation

---

## Requirements

### Functional

#### Core Knowledge (Phase 1)
- [ ] **FR-1**: Schema supports UI element documentation (screens, forms, dialogs)
- [ ] **FR-2**: Schema supports workflow definitions (multi-step procedures)
- [ ] **FR-3**: Schema supports decision trees (conditional guidance)
- [ ] **FR-4**: Schema supports industry/vertical context
- [ ] **FR-5**: Schema supports Q&A pairs (common questions with verified answers)
- [ ] **FR-6**: Schema supports versioning (product version ↔ pack version)

#### Element Semantics (Phase 1-2)
- [ ] **FR-7**: All interactive elements documented (not just buttons)
- [ ] **FR-8**: Input fields include: purpose, data type, validation rules, examples
- [ ] **FR-9**: Select/dropdown fields include: purpose, available options, defaults
- [ ] **FR-10**: Grids/tables include: columns, data types, sort/filter capabilities, row actions
- [ ] **FR-11**: Checkboxes/toggles include: what they control, default state, implications
- [ ] **FR-12**: Required vs optional clearly marked
- [ ] **FR-13**: Field dependencies documented (field B only visible when field A = X)

#### Automation (Phase 2-3)
- [ ] **FR-14**: Stable selectors for all interactive elements
- [ ] **FR-15**: Executable playbooks with inputs, steps, assertions
- [ ] **FR-16**: Error handling and recovery paths
- [ ] **FR-17**: State verification (success/failure detection)

#### Vision (Phase 4)
- [ ] **FR-18**: Visual anchors for key elements
- [ ] **FR-19**: Fallback selector strategies
- [ ] **FR-20**: Screen change detection

### Non-Functional

- [ ] **NFR-1**: Human-readable format (YAML/Markdown preferred over pure JSON)
- [ ] **NFR-2**: Diffable — changes trackable in git
- [ ] **NFR-3**: Reasonable context size — prioritize density over verbosity
- [ ] **NFR-4**: Extensible — custom fields for domain-specific needs
- [ ] **NFR-5**: Packs can be loaded as context without preprocessing
- [ ] **NFR-6**: Packs can be chunked for RAG if needed

---

## Element Documentation Requirements

Every interactive element should capture:

### Buttons/Actions
| Field | Description |
|-------|-------------|
| id | Unique identifier |
| label | Display text |
| purpose | What it does (semantic) |
| when_to_use | Guidance on appropriate use |
| prerequisites | What must be true before clicking |
| outcome | What happens after clicking |
| selector | CSS selector for automation |

### Input Fields (Text, Number, Date, etc.)
| Field | Description |
|-------|-------------|
| id | Unique identifier |
| label | Display label |
| purpose | What data this captures and why |
| data_type | string, number, date, email, etc. |
| required | true/false |
| validation | Rules (min/max length, pattern, range) |
| default | Default value if any |
| examples | Example valid values |
| depends_on | Other fields that affect this one |
| selector | CSS selector for automation |

### Select/Dropdown Fields
| Field | Description |
|-------|-------------|
| id | Unique identifier |
| label | Display label |
| purpose | What choice this represents |
| options | List of available values with descriptions |
| default | Default selection |
| multi_select | Can select multiple? |
| depends_on | Other fields that affect options |
| selector | CSS selector for automation |

### Checkboxes/Toggles
| Field | Description |
|-------|-------------|
| id | Unique identifier |
| label | Display label |
| purpose | What setting this controls |
| default | Default state (true/false) |
| implications | What changes when toggled |
| selector | CSS selector for automation |

### Grids/Tables
| Field | Description |
|-------|-------------|
| id | Unique identifier |
| purpose | What data this displays |
| columns | Column definitions (name, type, sortable, filterable) |
| row_actions | Actions available per row |
| bulk_actions | Actions for multiple selected rows |
| pagination | How paging works |
| selector | CSS selector for automation |

---

## Open Questions

1. **Format**: YAML for structured data, Markdown for prose — hybrid approach?
2. **Chunking strategy**: How to break large packs for RAG?
3. **Validation**: How to verify pack accuracy against actual app?
4. **Generation**: Manual authoring vs. automated extraction from UI/code?
5. **Licensing**: Open packs vs. proprietary?
6. **Sync**: How to keep pack in sync as product evolves?

---

## Success Metrics

### Phase 1
- Agent with ExpertPack answers product questions more accurately than agent with just docs
- Time-to-expertise reduced from weeks to minutes

### Phase 2-3
- Agent can successfully execute common workflows via automation
- Error rate < 5% on supported playbooks

### Phase 4
- Agent recovers from minor UI changes without pack updates
- Autonomous task completion rate > 90%

---

*Last updated: 2026-02-11*
