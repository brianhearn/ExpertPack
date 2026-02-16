# Person Pack Schema

*Blueprint for ExpertPacks that capture a person — their stories, mind, beliefs, relationships, and voice. This schema extends [core.md](core.md); all shared principles apply.*

---

## Purpose

A person pack creates a structured digital archive of a human being. It serves two primary purposes:

1. **While alive:** A personal AI that knows the person deeply — can retell their stories, represent their views accurately, and serve as a living archive they and their family can interact with.
2. **After death:** A memorial AI that preserves the person's authentic voice and wisdom for future generations.

The system must be good enough that someone talking to the pack's avatar feels like they're getting *that person* — not a generic AI with some facts about them.

---

## Directory Structure

```
packs/{person-slug}/
├── manifest.yaml          ← Pack identity (required — see below)
├── overview.md            ← Who this person is (required)
├── README.md              ← Project documentation
├── SCHEMA.md              ← Points to this schema
├── LEGACY.md              ← Posthumous wishes, executor chain, memorial mode
│
├── verbatim/              ← The person's actual words (source of truth)
│   ├── stories/           ← Life stories, childhood memories, adventures
│   │   └── _access.json
│   ├── philosophy/        ← Essays, thought pieces
│   └── politics/          ← Political writing
│
├── summaries/             ← AI-generated summaries of verbatim content
│   ├── stories/           ← Story summaries with themes, people, lessons
│   │   ├── _index.json    ← Master story navigation index
│   │   └── _access.json
│   ├── philosophy/        ← Philosophy summaries with key arguments
│   └── politics/          ← Politics summaries with positions
│
├── facts/                 ← Biographical data (Markdown — canonical)
│   ├── _access.json
│   ├── personal.md        ← Birth, family structure, locations, bio
│   ├── family_tree.md     ← Full genealogy in narrative format
│   ├── career.md          ← Work history timeline
│   └── education.md       ← Schools, degrees, self-taught subjects
│
├── relationships/         ← The people graph
│   ├── _access.json
│   └── people.md          ← Everyone mentioned: family, friends, mentors
│
├── worldview/             ← Beliefs, values, opinions
│   ├── _access.json
│   ├── beliefs.md         ← Core theological/philosophical beliefs
│   ├── values.md          ← What matters most
│   ├── politics.md        ← Political positions
│   └── ai-predictions.md  ← Views on AI and technology
│
├── preferences/           ← Likes, dislikes, habits, communication style
│   ├── _access.json
│   └── preferences.md     ← Preferences in Markdown (canonical)
│
├── presentation/          ← How the avatar should sound and look
│   ├── _access.json
│   ├── speech_patterns.md ← Verbal style, humor, storytelling mode
│   ├── voice/             ← Voice profile for TTS/synthesis
│   └── appearance/        ← Visual appearance for avatar rendering
│
├── training/              ← Fine-tuning data (experimental)
│   ├── _access.json
│   ├── config.json        ← Format spec
│   ├── qa_pairs.jsonl     ← Direct Q&A from the person
│   └── conversations.jsonl← Conversation examples
│
└── meta/                  ← System metadata
    ├── _access.json
    ├── status.json        ← Alive/memorial mode flag
    ├── access.json        ← Access tier definitions
    ├── verification.json  ← Codeword verification rules
    ├── interaction.md     ← Interaction guidelines
    └── sessions.json      ← Capture session log
```

Not every directory is required from day one. Start with `facts/`, `verbatim/`, and `relationships/`, then expand as content is collected.

---

## The Two-Tier Content System

Every piece of the person's writing or dictation exists in two forms:

| Layer | Directory | Purpose | Token Cost | When to Use |
|-------|-----------|---------|------------|-------------|
| **Verbatim** | `verbatim/` | Person's exact words | High | Retelling stories, exact quotes, avatar performance, fine-tuning |
| **Summary** | `summaries/` | Structured distillation | Low | Context loading, search results, quick reference, theme analysis |

### Why Both?

An AI retelling a person's story needs their actual words — the humor, the pacing, the details only they would include. But an AI answering "what themes run through their childhood?" just needs the summary. The two-tier system optimizes for both use cases without burning tokens.

### Priority

**Verbatim first, summaries second.** The person's actual words are the source of truth. Summaries are generated from verbatim content. If a summary and verbatim disagree, the verbatim wins.

### Organizing Verbatim and Summary Content

Verbatim and summary directories should mirror each other — if `verbatim/stories/nina-street.md` exists, there should be a corresponding `summaries/stories/nina-street.md`. Subdirectories within verbatim/ and summaries/ are organized by content type:

- `stories/` — Life stories, childhood memories, adventures
- `philosophy/` — Essays, thought pieces, intellectual writing
- `politics/` — Political writing and commentary

Additional subdirectories can be added as content warrants (e.g., `humor/`, `travel/`, `career-stories/`).

---

## Story Intake Workflow

When the person dictates a new story or memory:

1. **Capture** — Record verbatim text from voice dictation or written input into `verbatim/stories/`
2. **Structure** — Add `##` section headers at natural topic breaks (never change the person's words — only insert structural markers between existing paragraphs)
3. **Summarize** — Generate a summary in `summaries/stories/` with themes, people, places, emotions
4. **Cross-reference** — Search existing content for related people, places, events
5. **Update relationships** — Check `relationships/people.md` for new or updated people; add entries
6. **Update index** — Add entry to `summaries/stories/_index.json`
7. **Contradiction check** — Flag any conflicts with existing data for the person to resolve (see [core.md](core.md) conflict resolution rules)
8. **Commit** — Git commit and push to preserve versioning

### Voice Dictation Notes

When content arrives via voice dictation, the transcription will be imperfect but authentic. Clean up obvious transcription errors but preserve the person's phrasing, tangents, and style. The goal is *their voice*, not polished prose.

---

## Biographical Data Patterns

### facts/personal.md
Birth date, family structure, locations lived, basic biographical data. Use `##` headers to organize by life period or topic.

### facts/family_tree.md
Full genealogy in narrative Markdown format. This is the canonical version — if a JSON genealogy file exists (e.g., GEDCOM-derived), it is archival only.

### facts/career.md
Work history as a timeline with highlights, key roles, and transitions.

### facts/education.md
Schools, degrees, certifications, and self-taught subjects.

### relationships/people.md
Every person mentioned across the pack: family, friends, mentors, colleagues. Each entry should include:
- Relationship to the person
- Key facts (how they met, shared experiences)
- Cross-references to stories or content where they appear

---

## Worldview & Preferences

### Worldview Files

`worldview/` captures the person's beliefs, values, and opinions. Each file uses free-form Markdown with `##` headers for categories:

```markdown
# Beliefs

## On Faith
What they believe and why...

## On Science
How they view the relationship between faith and science...

## On Human Nature
Their view of people...
```

### Opinions

For well-developed opinions or essays, use individual files:

```markdown
# Opinion: {Topic}

**Stance:** One-line position
**Strength:** strong | moderate | tentative
**Last updated:** YYYY-MM-DD

## Position
Full explanation...

## Why I Think This
Background, reasoning...

## What Could Change My Mind
...
```

### Preferences

`preferences/preferences.md` captures likes, dislikes, habits, and communication style. Organized by category (food, music, movies, communication style, pet peeves, guilty pleasures, etc.).

---

## Presentation Layer

The `presentation/` directory defines how a person-pack avatar should behave:

### speech_patterns.md
Verbal style, humor type, storytelling mode, common phrases, how they start and end stories, what makes their communication distinctive.

### voice/
Voice profile data for TTS synthesis. May include voice samples, ElevenLabs voice IDs, prosody notes, or other synthesis parameters.

### appearance/
Visual appearance data for avatar rendering. Physical description, reference photo metadata, avatar generation parameters.

---

## Legacy / Memorial Mode

Person packs include a `LEGACY.md` file that documents the person's wishes for how the pack should function after their death. This is a critical document — it captures:

### Executor Chain
Who has authority over the pack after death, in order of succession. Executor powers and limitations.

### Memorial Mode Activation
What changes when the person dies:
- Update `meta/status.json` with death date and memorial mode flag
- Avatar behavioral changes (past tense, acknowledging memorial status)
- Content access changes (some content opens up, some stays sealed)

### Content Decisions
- **Open up after death:** Content that becomes available to family or public
- **Seal forever:** Content that should never be shared
- **Time-locked:** Content that unlocks at specific conditions (grandchild turns 18, 5 years after death, etc.)

### Long-Term Continuity
Hosting wishes, technology upgrade preferences, conditions for sunset.

---

## Person-Specific Manifest Fields

Beyond the core manifest fields defined in [core.md](core.md):

```yaml
# Required
name: "Person's Full Name"
slug: "person-slug"
type: "person"
version: "1.0.0"
description: "What this pack captures"
entry_point: "overview.md"

# Person-specific
subject:
  full_name: "Brian Franklin Hearn"
  born: "YYYY-MM-DD"
  location: "City, State"
  alive: true

# Content inventory
sections:
  - verbatim
  - summaries
  - facts
  - relationships
  - worldview
  - preferences
  - presentation
  - training
  - meta

# Data sources
sources:
  - type: "website"
    url: "https://bfhearn.com"
    description: "Personal blog — philosophy, politics, stories"
  - type: "voice-dictation"
    description: "Ongoing story capture via Telegram"
  - type: "genealogy"
    description: "Ancestry.com GEDCOM export"
```

---

## Access Tiers

Person packs use a four-tier access model, enforced via `_access.json` files at the directory level:

| Tier | Who Can Access | Examples |
|------|----------------|---------|
| **public** | Anyone | Published essays, public bio, general stories |
| **friends** | Known associates | Casual stories, opinions, some personal details |
| **family** | Family members | Private stories, family history, personal reflections |
| **self** | The person only (or executor) | Truly private content, credentials, sealed memories |

### How Access Works

Each content directory can have an `_access.json` file:

```json
{
  "default_access": "family",
  "overrides": {
    "private-reflection.md": "self",
    "published-essay.md": "public"
  }
}
```

Access tiers can change posthumously as defined in `LEGACY.md` — some `friends` content may open to `family`, some `self` content may be sealed forever.

### Verification

Access can be verified via codewords defined in `meta/verification.json`. Each tier has its own codeword or verification method.

---

## Tags Taxonomy

Person packs use a consistent tagging system for stories and content, stored in `summaries/stories/_index.json`:

### Life Domains
`career` · `family` · `health` · `education` · `social` · `hobbies` · `travel` · `finance`

### Story Themes
`turning-point` · `lesson-learned` · `funny` · `challenge` · `failure` · `success` · `relationship` · `origin`

### Emotions
`proud` · `happy` · `grateful` · `excited` · `scared` · `anxious` · `uncertain` · `sad` · `regretful` · `disappointed` · `angry` · `frustrated` · `amused` · `surprised` · `peaceful` · `content`

### Usage in _index.json

```json
{
  "stories": [
    {
      "id": "nina-street-shed",
      "title": "The Shed on Nina Street",
      "date": "circa-1975",
      "date_precision": "approximate",
      "summary": "Building a hideout in the backyard shed",
      "themes": ["funny", "origin"],
      "people": ["sam"],
      "places": ["Brooksville, FL"],
      "emotions": ["amused", "proud"],
      "file": "nina-street-shed.md"
    }
  ]
}
```

---

## Universal Metadata

When applicable, content items can carry metadata:

```json
{
  "id": "unique-slug-identifier",
  "created": "2026-02-07T22:40:00Z",
  "updated": "2026-02-07T22:40:00Z",
  "source": "telegram|voice|interview|document|memory",
  "confidence": "certain|likely|approximate|uncertain",
  "tags": ["tag1", "tag2"],
  "related": ["other-id-1", "other-id-2"]
}
```

This metadata lives in JSON index files, not in the Markdown content itself (following the MD-canonical principle).

---

## Data Sources for Person Packs

| Source | Quality | Coverage | Effort |
|--------|---------|----------|--------|
| **Personal blog/website** | High — person's own words | Philosophy, stories, opinions | Low — scrape and structure |
| **Voice dictation** | High — authentic but needs cleanup | Stories, memories, opinions | Medium — transcribe and structure |
| **Direct Q&A sessions** | High — targeted content | Preferences, beliefs, specific facts | Medium — guided conversation |
| **Genealogy exports** | Structured — good for family tree | Family relationships | Low — parse and convert |
| **"Tell Me Your Story" books** | High — prompted memories | Childhood, life milestones | Medium — use prompts as starting points |
| **Social media archives** | Variable — may need curation | Opinions, interests, relationships | High — filter signal from noise |

---

## Creating a New Person Pack

1. Create the directory structure (start with `facts/`, `verbatim/`, `relationships/`)
2. Write `manifest.yaml` with type `person`
3. Write `overview.md` — who the person is and what this pack will capture
4. Begin with biographical facts — `personal.md`, `career.md`, `education.md`
5. Capture the person's words into `verbatim/` — stories, essays, dictations
6. Generate summaries as verbatim content accumulates
7. Build `relationships/people.md` as people appear in stories
8. Add worldview content as the person shares beliefs and opinions
9. Write `LEGACY.md` when the person is ready to discuss posthumous wishes

The pack will grow over time. Person packs are never "done" — they grow as long as the person keeps sharing.

---

*Schema version: 1.0*
*Last updated: 2026-02-16*
