# ExpertPack Requirements

## Vision

Enable AI agents to become instant experts in complex software products by loading structured knowledge packs — no fine-tuning required.

**End goal:** An AI agent that knows a product as well as a veteran support engineer.

---

## Version Scope

### V1: Knowledge Layer (Current Focus)

Agent becomes an expert who can **guide humans** through the product.

**Capabilities:**
- Answer product questions with deep accuracy
- Walk users through workflows step-by-step ("click X, enter Y, expect Z")
- Troubleshoot issues using decision trees
- Know every screen, field, button, and edge case
- Explain concepts and suggest best practices

**Use cases:**
- Customer support chatbot
- Sales demo assistance (human drives, agent guides)
- Internal training / onboarding
- Self-service help

**What V1 includes:**
- Product concepts and mental model
- Screen catalog with navigation paths
- UI element documentation (labels, purpose, location, behavior)
- Step-by-step workflows
- Decision trees for troubleshooting
- Common questions and gotchas
- Error messages and resolutions

**What V1 does NOT include:**
- CSS selectors / automation hooks
- Executable playbooks
- Visual anchors / screenshots for vision models
- Self-healing selector logic

---

### V2: Automation Layer (Future)

Agent can **operate the product** via browser automation.

**Capabilities:**
- Execute workflows autonomously (clicks, inputs, navigation)
- Perform live demos without human driving
- Complete routine tasks on behalf of users
- Recover from minor UI changes

**Additional requirements for V2:**
- Stable selectors (data-testid preferred)
- Executable playbooks (Playwright/Puppeteer)
- State verification (success/failure detection)
- Visual anchors for fallback element detection
- Error recovery paths

**V2 builds on V1** — all knowledge layer content remains, automation hooks are added.

---

## Pack Schema

The schema defines the structure of an ExpertPack. See [SCHEMA.md](SCHEMA.md) for detailed specifications.

### Core Components

| Component | Purpose |
|-----------|---------|
| `manifest.yaml` | Pack metadata, version, product info |
| `concepts/` | Mental model, terminology, how things work |
| `screens/` | Every screen in the product |
| `workflows/` | Step-by-step procedures |
| `troubleshooting/` | Decision trees, error resolution |
| `faq/` | Common questions with verified answers |

### Screen Documentation

Each screen captures:
- **Identity**: Name, purpose, how to navigate there
- **Layout**: Sections, regions, what's where
- **Elements**: Every interactive element (buttons, fields, grids, etc.)
- **States**: Different modes/views the screen can be in

### Element Documentation

Every interactive element captures:
- **Label**: What it's called in the UI
- **Purpose**: What it does (semantic description)
- **Location**: Where to find it on screen
- **Behavior**: What happens when you interact
- **Validation**: Rules, constraints, requirements (for inputs)
- **Dependencies**: Other elements that affect it

### Workflow Documentation

Each workflow captures:
- **Goal**: What the user is trying to accomplish
- **Prerequisites**: What must be true before starting
- **Steps**: Ordered sequence with:
  - Action ("Click X", "Enter Y")
  - Location (which screen, which element)
  - Expected result
- **Completion**: How to know it succeeded
- **Common issues**: What can go wrong and how to fix it

---

## Pack Creation Process

### Input Sources

| Source | What it provides |
|--------|------------------|
| **Web docs** | Concepts, feature descriptions, basic workflows |
| **Videos** | UI flow, step-by-step procedures, visual context |
| **Screenshots** | Screen layouts, element locations, visual reference |
| **Guided walkthroughs** | Detailed procedures, edge cases, expert knowledge |
| **Live app** | Verification, discovering undocumented behavior |
| **Support tickets** | Common questions, real user pain points |

### Creation Methods

#### 1. Document Ingestion
Process existing documentation to extract structured knowledge.

**Input:** Web docs, help articles, user guides
**Output:** Concepts, basic screen info, feature descriptions
**Process:** 
- Agent reads docs
- Extracts and restructures into pack format
- Human reviews for accuracy

#### 2. Video Processing
Extract workflows and UI knowledge from demo/tutorial videos.

**Input:** Video files or URLs
**Output:** Step-by-step workflows, screen sequences
**Process:**
- Transcribe narration
- Capture key frames
- Extract procedure steps
- Human validates against live app

#### 3. Screenshot Analysis
Understand screen layouts and element locations.

**Input:** Screenshots of each screen/state
**Output:** Screen documentation, element inventory
**Process:**
- Agent analyzes screenshot
- Identifies and documents visible elements
- Human provides missing context (purpose, behavior)

#### 4. Guided Walkthrough (Primary Method)
Human expert walks agent through scenarios interactively.

**Input:** Human narration + live app access
**Output:** Detailed workflows, expert knowledge, edge cases
**Process:**
1. Human describes a scenario/task
2. Human walks through steps, describing what they see and do
3. Agent asks clarifying questions
4. Agent drafts structured documentation
5. Human reviews and corrects
6. Agent commits to pack

This is the highest-fidelity method — captures tribal knowledge that docs miss.

#### 5. Validation
Verify pack accuracy against live product.

**Input:** Completed pack sections + live app
**Output:** Corrections, missing information
**Process:**
- Agent (or human) follows pack instructions in live app
- Notes discrepancies
- Updates pack

### Creation Workflow

```
┌─────────────────┐
│  Gather Sources │  (docs, videos, screenshots)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Initial Ingest │  (process docs, analyze media)
└────────┬────────┘
         ▼
┌─────────────────┐
│ Guided Sessions │  (human walks through scenarios)
└────────┬────────┘
         ▼
┌─────────────────┐
│   Validation    │  (verify against live app)
└────────┬────────┘
         ▼
┌─────────────────┐
│    Publish      │  (version, release)
└─────────────────┘
```

### Maintenance

Packs need updates when the product changes:
- **Version tagging**: Pack version tied to product version
- **Change detection**: Compare pack against new release
- **Incremental updates**: Guided sessions for new/changed features

---

## Success Criteria

### V1 Complete When:
- [ ] Agent with ExpertPack answers support questions better than agent with raw docs
- [ ] Agent can walk a user through any documented workflow accurately
- [ ] Pack covers all screens and major workflows
- [ ] Validation pass against live app with <5% error rate

### V2 Complete When:
- [ ] Agent can execute documented workflows via browser automation
- [ ] Automation success rate >90% on supported workflows
- [ ] Agent recovers from minor UI changes without pack updates

---

## First Pack: EasyTerritory Designer

**Product:** Territory Designer web application
**Goal:** Full V1 coverage for support chatbot use case

**Milestones:**
1. [ ] Schema finalized
2. [ ] Core concepts documented
3. [ ] All screens cataloged
4. [ ] Primary workflows documented (create territory, import data, etc.)
5. [ ] Troubleshooting trees for common issues
6. [ ] Validation pass
7. [ ] Integration test with OpenClaw chatbot

---

*Last updated: 2026-02-12*
