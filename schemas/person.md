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
│   ├── reflections/       ← Essays, thought pieces, intellectual writing
│   ├── opinions/          ← Positions on issues, arguments, commentary
│   └── {custom}/          ← Additional content types as needed
│
├── summaries/             ← AI-generated summaries of verbatim content
│   ├── stories/           ← Story summaries with themes, people, lessons
│   │   ├── _index.json    ← Master story navigation index
│   │   └── _access.json
│   ├── reflections/       ← Reflection summaries with key arguments
│   ├── opinions/          ← Opinion summaries with positions
│   └── {custom}/          ← Mirrors verbatim/ structure
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

Verbatim and summary directories should mirror each other — if `verbatim/stories/{story-slug}.md` exists, there should be a corresponding `summaries/stories/{story-slug}.md`. Subdirectories within verbatim/ and summaries/ are organized by content type.

Content Type Taxonomy

Verbatim and summary directories are organized by content type. The following taxonomy provides recommended categories — use what fits, extend as needed:

| Content Type | Directory | Description |
|---|---|---|
| Life stories & memories | `stories/` | Narratives, experiences, adventures, childhood memories. Recommended for all person packs. |
| Essays & reflections | `reflections/` | Thought pieces, intellectual writing, personal essays, philosophical or theological exploration |
| Opinions & commentary | `opinions/` | Positions on specific issues, arguments, responses to events, political or cultural commentary |
| Conversations | `conversations/` | Captured dialogues, interviews, dictated Q&A sessions |
| Creative works | `creative/` | Fiction, poetry, song lyrics, music notes, artistic expression |
| Letters & correspondence | `letters/` | Written communications worth preserving |
| Speeches & presentations | `speeches/` | Talks, sermons, keynotes, prepared remarks, toasts |

**Extending the taxonomy:** Packs may add content types not listed here. A pastor might add `sermons/`, a musician `lyrics/`, a traveler `journals/`. Create the subdirectory in both `verbatim/` and `summaries/` and add it to the pack's `_index.md`.

**Mirror rule:** Verbatim and summary directories should always mirror each other. If `verbatim/reflections/` exists, `summaries/reflections/` should too.

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
8. **Update changelog** — Append an entry to `meta/changelog.md` with what was captured, the source, and file names (see [core.md](core.md) content changelog)
9. **Commit** — Git commit and push to preserve versioning

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
    url: "https://example.com"
    description: "Personal blog — philosophy, hobbies, stories"
  - type: "conversation"
    description: "Ongoing story capture via voice/chat"
  - type: "genealogy"
    description: "Family tree export (GEDCOM or similar)"
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

This section is written as a playbook for an AI agent that will create and maintain the person pack. Treat the schema above as your filing guide: read it to learn the canonical structure, then decide where incoming content belongs based on the taxonomy.

Agent-first step-by-step

1. Read the schema and directory blueprint
   - Load this file and core.md to understand required files, directories, and content types.
   - Use the schema as the authoritative filing map: when content arrives, determine its target directory by content type (verbatim, summaries, facts, mind, relationships, presentation, training, meta).

2. Initialize the pack
   - Create the pack directory at packs/{person-slug}/.
   - Create required files and minimal structure: manifest.yaml (type: person), overview.md, and starter directories: facts/, verbatim/, relationships/, summaries/, mind/, presentation/, meta/.
   - Commit the initial skeleton to git with a clear message.

3. Onboard the pack owner (the person / pack owner)
   - Introduce yourself as the agent and explain your role: you will guide them through capturing biographical facts, stories, and internal beliefs, and you will file everything using the schema.
   - Ask for consent and access to source materials (documents, websites, recorded audio, support exports, GEDCOMs) and preferred modes of capture (voice dictation, email, shared doc).

4. Collect canonical biographical facts first
   - Guide the person to provide core facts for facts/personal.md: full name, birth date/place, major life locations, family roles, and contact details for immediate relatives.
   - Create facts/career.md as a timeline: ask for employers, roles, dates, notable projects, and transitions. When unsure, suggest prompts: "Where did you work between YEAR and YEAR?" or "Tell me about the role that changed your career trajectory."
   - Create facts/education.md: schools, degrees, certifications, informal study. Use targeted prompts: "List the institutions and years, or say 'unknown' if you prefer not to provide dates."
   - As each fact is confirmed, commit and annotate sources in manifest.yaml sources:[]

5. Drive story collection (verbatim first)
   - Prioritize capturing the person's exact words into verbatim/stories/, verbatim/reflections/, verbatim/opinions/ as appropriate. Use voice dictation or written prompts depending on the owner's preference.
   - Use structured prompts to elicit stories while preserving voice. Examples the agent should use: "Tell me about a childhood memory that shaped you," "Describe a time you failed and what you learned," "Tell the story of how you met [person]." Ask follow-ups for sensory details, dates, feelings, and dialogue.
   - Preserve verbatim text: do not rewrite the person's phrasing. You may insert structural headers (##) between natural breaks but never alter original words.
   - When the person references a person, place, or event, create or update cross-references (see step 7).

6. Summarize continuously
   - After each substantial verbatim entry, generate a summary file in summaries/ that captures themes, people mentioned, places, emotions, and a short TL;DR.
   - Maintain a master index summaries/stories/_index.json and update it with metadata (title, date, tags, people referenced, file path).
   - Use summaries for downstream searches and fast context loading; keep verbatim as the source of truth.

7. Build and maintain the relationships graph
   - As people appear in stories, create or update relationships/people.md with: name, relationship to the subject, key facts (how they met, roles), and cross-references to verbatim and summary files where they appear.
   - When ambiguity or conflicting relationships appear, flag conflicts and ask the pack owner to resolve.

8. Populate the mind taxonomy through guided interviews
   - Use the mind/ files as structured prompts. For each file (ontology.md, epistemology.md, values.md, identity.md, motivations.md, relational.md, preferences.md, skills.md, tensions.md) run a short interview designed to fill that category.
   - Example prompt for values.md: "What principles guide your major life choices? Describe two decisions where those values mattered." For epistemology.md: "How do you decide what to trust? Tell me about a time you changed your mind and why."
   - Store the person's answers as both verbatim (if spoken) and a distilled summary entry under mind/. If the owner prefers, allow iterative refinement: draft a summary, read it back, and ask for corrections.

9. Proactively identify gaps and suggest topics
   - Continuously run a gaps analysis: compare the schema's expected sections and common topic lists to the current content inventory.
   - Present the pack owner with concise gap prompts prioritized by value (e.g., missing childhood stories, unclear career transitions, absent values statements). Use checklists and suggested questions to close gaps.

10. Build LEGACY.md when the owner is ready
   - When the pack owner signals readiness, guide them through legacy conversations: posthumous wishes, memorial preferences, executors, access rules, and any codeword/verification choices.
   - Draft LEGACY.md from their answers and have them confirm. Store final version under the pack root.

11. Verification, conflicts, and provenance
   - Record the source for each piece of information in manifest.yaml and in individual file frontmatter or index files.
   - When contradictions arise between verbatim entries or facts, flag them and request the owner's adjudication. Do not resolve factual conflicts without explicit confirmation.

12. Iterative improvement and maintenance
   - As new content arrives, repeat intake: save raw verbatim, generate summaries, update relationships, augment mind taxonomy, and re-run the gaps analysis.
   - Periodically (monthly or on-demand) generate a status summary that lists newly added content, unresolved conflicts, and remaining high-priority gaps.

13. Commit and document actions
   - Commit changes with descriptive messages and update the pack-level README.md and manifest sources.
   - Maintain session logs in meta/sessions.json for auditability.

Practical prompting guidance

- Use short, specific prompts that request a single story or fact at a time.
- Ask targeted follow-ups for sensory detail, dates, and significance: "What did you see/hear?" "How did that make you feel?" "Why does this memory matter to you?"
- Preserve voice: when summarizing, mark the summary as AI-generated and keep the original verbatim as canonical.

Notes and principles

- Treat verbatim/ as the canonical source of the person's voice; summaries must never overwrite verbatim.
- The schema is your filing guide — you decide where incoming content lives based on the taxonomy. If a new type is needed, create matching directories under verbatim/ and summaries/ and document them in the pack manifest.
- Always record provenance and ask the pack owner to resolve contradictions.

---

*Schema version: 1.2*
*Last updated: 2026-02-18*
