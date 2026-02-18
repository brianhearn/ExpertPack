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
├── mind/                  ← Mind taxonomy: beliefs, sense-making, motivations, and preferences
│   ├── _access.json
│   ├── ontology.md        ← Ontology & Metaphysics
│   ├── epistemology.md    ← Epistemology & Sense-Making
│   ├── values.md          ← Values & Moral Framework
│   ├── identity.md        ← Identity & Self-Narrative
│   ├── motivations.md     ← Motivations, Drives & Temperament
│   ├── relational.md      ← Relational & Social Orientation
│   ├── preferences.md     ← Preferences, Tastes & Aesthetic Orientation
│   ├── skills.md          ← Skills, Competencies & Action Patterns
│   └── tensions.md        ← Tensions, Contradictions & Edge Cases
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

## The Mind Taxonomy

The person's inner life (formerly "worldview" + "preferences") is captured under a unified `mind/` directory. This organizes beliefs, sense-making approaches, values, preferences, skills, and tensions into a consistent filing system for agents.

Each category starts as a single `.md` file but may expand into a subdirectory as content grows (e.g., `mind/ontology/` with multiple files).

### Mind Taxonomy Categories

1. ontology.md — Ontology & Metaphysics
What the person believes is ultimately real and how reality is structured. Includes religious/spiritual worldview, views on consciousness, the nature of God, the soul, materialism vs. dualism, cosmology (as it relates to meaning), and any framework for understanding existence itself.

2. epistemology.md — Epistemology & Sense-Making
How the person determines what is true and updates beliefs. Includes their relationship between faith and reason, trust in institutions, how they weigh evidence, their approach to certainty and doubt, intellectual influences, and how they process new information that challenges existing views.

3. values.md — Values & Moral Framework
What the person considers good, bad, right, and worth protecting. Includes ethical principles, political philosophy (as it reflects values), priorities in life, what they'd sacrifice for, views on justice and fairness, and the moral reasoning behind their positions. Political views live here primarily, with cross-references to epistemology and ontology where those inform the positions.

4. identity.md — Identity & Self-Narrative
How the person understands who they are across roles and time. The story they tell about themselves — key turning points, how they see their own arc, the roles that define them (father, engineer, pilot, apologist), how past experiences shaped who they became. Not external biography (that's `facts/`), but internal self-concept.

5. motivations.md — Motivations, Drives & Temperament
What energizes behavior and shapes emotional responses. Includes personality traits, ambition, what gives them energy vs. drains them, emotional patterns, how they handle stress/failure/success, risk tolerance, introversion/extroversion, and the deeper drives behind their choices.

6. relational.md — Relational & Social Orientation
How the person connects with others. Trust patterns, communication style, conflict approach, how they form and maintain friendships, authority orientation, group behavior vs. one-on-one, loyalty patterns, what they value in others, and how they show care.

7. preferences.md — Preferences, Tastes & Aesthetic Orientation
What the person is drawn to, enjoys, and finds meaningful. Hobbies, media consumption, aesthetic sensibilities, food/music/film/book preferences, leisure activities, guilty pleasures, and what they find beautiful or compelling. Lighter than values — this is about taste, not morality.

8. skills.md — Skills, Competencies & Action Patterns
What the person can do and how they tend to act in the world. Professional expertise, learned skills, problem-solving approach, how they learn new things, domains of competence, work style, tools they reach for, and patterns in how they execute on goals.

9. tensions.md — Tensions, Contradictions & Edge Cases
Where the model breaks — the places where other categories don't fully cohere. Context-dependent behavior switches, acknowledged blind spots, unresolved internal conflicts, things they believe but don't practice (or vice versa), and the messy human reality that neat categories miss. This is some of the most valuable content for authenticity.

### Political Views
Political views are cross-cutting: they live primarily in `mind/values.md` with cross-references to `mind/epistemology.md` and `mind/ontology.md` when those domains inform political positions.

---

## Story Intake Workflow

(unchanged — verbatim steps preserved from earlier schema)

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
  full_name: "Robert James Smith"
  born: "YYYY-MM-DD"
  location: "City, State"
  alive: true

# Content inventory
sections:
  - verbatim
  - summaries
  - facts
  - relationships
  - mind
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

(Person schema access tiers unchanged — preserved verbatim)

---

## Tags Taxonomy

(unchanged)

---

## Universal Metadata

(unchanged)

---

## Creating a New Person Pack

1. Create the directory structure (start with `facts/`, `verbatim/`, `relationships/`)
2. Write `manifest.yaml` with type `person`
3. Write `overview.md` — who the person is and what this pack will capture
4. Begin with biographical facts — `personal.md`, `career.md`, `education.md`
5. Capture the person's words into `verbatim/` — stories, essays, dictations
6. Generate summaries as verbatim content accumulates
7. Build `relationships/people.md` as people appear in stories
8. Add mind content as the person shares beliefs, sense-making approaches, values, and preferences
9. Write `LEGACY.md` when the person is ready to discuss posthumous wishes

The pack will grow over time. Person packs are never "done" — they grow as long as the person keeps sharing.

---

*Schema version: 1.1*
*Last updated: 2026-02-18*