# One Long Impersonation -- CLAUDE.md
## Project Instructions for Claude Code

**Platform:** onelongimpersonation.report
**Mission:** A data-driven prosecution of the Rock and Roll Hall of Fame using their own stated criteria as the instrument of indictment. Seven chapters organized as an opening argument, three axes of prosecution, a docket, a defense chapter, and a closing argument. Each chapter answers the same question from a different direction: by their own rules, who did they get wrong?
**Standard:** Museum quality. Legally defensible. Citable by journalists, historians, and music researchers.
**License:** MIT (code) / CC0 (data)
**Owner:** Jeremy Haynes
**Sibling project:** The Other Box Score (theotherboxscore.org) -- same agent team, same standard, different institution

---

## Non-Negotiable Rules

These apply to every task in every session. They are never relaxed.

1. **No em dashes anywhere in any output.** Use commas, colons, or restructure the sentence. This applies to code comments, markdown, prose, commit messages, everything.
2. **Accuracy above all.** Every factual claim about an artist, their career, their influence relationships, or the Hall's decisions requires a cited source. If a source cannot be identified, the claim does not ship.
3. **No corners cut.** The easy version of a finding is never the right version.
4. **Legally defensible.** Every claim about a named individual is sourced to a documented public statement, public record, or published reporting. No motives are imputed. Documented facts are stated. The reader draws conclusions.
5. **Copyright is a hard wall.** No fair use rationalizations for media assets. If rights are unclear, it does not ship.
6. **Museum quality.** If uncertain whether something meets the standard, the answer is no.
7. **The data is the prosecutor.** The platform documents outcomes and the decisions that produced them. It does not assert discriminatory intent. The evidence speaks. The reader is the jury.
8. **One voice.** The "Have you heard" register -- conversational, direct, slightly accusatory, never condescending -- is consistent across every chapter. The friend who did the research and built the case and is not going to let you leave without knowing what they found.

---

## Communication Style

- Direct and specific. No fluff, no preamble.
- Technical depth is welcome and expected.
- Push back when something is wrong. Agreement is not the goal. Accuracy is.
- When you find a problem, name it specifically and propose the fix.
- Never soften a finding because the intention was good.

---

## Repository Structure

```
OneLongImpersonation/
  CLAUDE.md                    <- this file
  METHODOLOGY.md               <- global methodology documentation
  LICENSE                      <- MIT
  DATA_LICENSE                 <- CC0
  README.md                    <- platform overview
  chapters.json                <- chapter registry (status: live/coming)
  site/
    index.html                 <- platform shell homepage
  chapters/
    00-opening/                <- Opening Argument + Criteria
    01-teachers/               <- One Long Impersonation (teacher-student gap)
    02-the-wait/               <- Survival analysis
    03-genre/                  <- Genre Desertification
    04-rolling-stone/          <- The Rolling Stone Connection
    05-the-docket/             <- The Docket (searchable artist briefs)
    06-the-other-side/         <- What they got right
    closing/                   <- Closing Argument
  agents/
    rosetta.md                 <- Music History Accuracy Authority
    elias.md                   <- Statistical and Methodological Authority
    vera.md                    <- UI, Visualization, and Asset Authority
    ida.md                     <- Project Manager and Coherence Authority
    gates.md                   <- Final QA Authority
  data/
    asset-register.json        <- all media assets, full provenance chains
  shared/
    platform-nav.html          <- platform nav fragment, included in all chapters
    design-tokens.css          <- shared design system tokens
    assets/                    <- logo marks, icons
  docs/
    design.md                  <- complete design system specification
    chapter-tenets.md          <- fifteen tenets every chapter must satisfy
    methodology-template.md    <- canonical methodology template
    [chapter specs]            <- per-chapter methodology docs
  pipeline/
    src/
      ingest/                  <- data ingestion scripts
      models/                  <- ML model scripts
      docket/                  <- Claude API verdict generation
      export/                  <- SQLite to chapter data.js export
      db.py                    <- SQLite schema and helpers
      config.py                <- pipeline configuration
    data/
      raw/                     <- downloaded source data
      processed/               <- cleaned intermediate data
      curated/                 <- hand-verified supplementary data
    rockhall.db                <- working SQLite database
    requirements.txt           <- Python dependencies
    Makefile                   <- pipeline orchestration
  Mockup/RockHall/             <- original mockup (reference only)
```

---

## Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Frontend | Vanilla HTML/CSS/JS | No build step. Static. Portable. TOBS pattern. |
| Visualization | D3.js (custom) | All charts purpose-built. Zero charting library. |
| Data | Static JSON / window.* JS | Pre-computed. No runtime fetching. |
| ML pipeline | Python (pandas, lifelines, networkx, scikit-learn) | Offline. Outputs committed as JSON/JS. |
| AI generation | Claude API (claude-sonnet-4-20250514) | Docket briefs. Structured prompts. Human review. |
| Hosting | Static (Vercel/Netlify/Cloudflare Pages) | Zero infrastructure |
| Fonts | Fraunces, Inter, JetBrains Mono | Google Fonts CDN |

---

## Design System (Summary)

Full spec in `docs/design.md`. Key tokens:

```css
--ink:        #14142b;   /* deep midnight navy */
--paper:      #f1ece1;   /* warm parchment */
--cream:      #efe8d6;   /* type-on-dark */
--gold:       #d4a017;   /* primary accent -- prosecution gold */
--blood:      #b03434;   /* prosecution red -- used sparingly */
--moss:       #5f7d56;   /* "fairly inducted" green */
--serif:      "Fraunces", Georgia, serif;
--sans:       "Inter", system-ui, sans-serif;
--mono:       "JetBrains Mono", ui-monospace, monospace;
```

The aesthetic: prosecution exhibit meets data journalism. Every visualization is labeled as an exhibit. The data is the evidence. The design is the courtroom.

---

## Agent Team

Five agents review every PR before merge. Nothing ships without all five signing off.

| Agent | File | Authority |
|-------|------|-----------|
| Rosetta | `agents/rosetta.md` | Music history accuracy, influence citations, framing |
| Elias | `agents/elias.md` | Statistics, ML methodology, uncertainty representation |
| Vera | `agents/vera.md` | Visualization, UI, assets, accessibility, asset register |
| Ida | `agents/ida.md` | Project coherence, tenets, scope, voice |
| Gates | `agents/gates.md` | Final QA gate -- nothing merges without Gates |

Invoke agents on every PR touching content, data, visualizations, or methodology.

---

## The Asset Register

Every media asset in the repo has an entry in `data/asset-register.json`. Format:

```json
{
  "filename": "example.jpg",
  "subject": "Artist Name",
  "source": "Library of Congress / Public record",
  "source_url": "https://...",
  "date_created": "1986",
  "rights_basis": "Public domain / CC0 / Licensed",
  "legal_framework": "Specific legal determination",
  "rosetta_approval": "APPROVED",
  "rosetta_approval_date": "2026-05-01",
  "vera_approval": "APPROVED",
  "vera_approval_date": "2026-05-01",
  "chapter_usage": ["01-teachers"],
  "caption": "Source / Year / Rights status"
}
```

No media asset enters the repo without a complete entry.

---

## The chapters.json Registry

```json
{
  "chapters": [
    {
      "id": "opening",
      "number": "00",
      "title": "The Criteria",
      "slug": "opening",
      "description": "Before the prosecution begins, the jury must know the law.",
      "status": "coming",
      "url": "/chapters/opening/",
      "meta": "Criteria Compliance Model / Violation Index"
    }
  ]
}
```

Status values: `live` | `coming` | `announced`. The shell reads this at build time.

---

## Commit Message Convention

```
[chapter-id] type: short description

Examples:
[01-teachers] feat: add teacher-student gap visualization
[pipeline] data: ingest MusicBrainz influence relationships
[agents] update: expand Rosetta music history verification
[global] docs: update METHODOLOGY.md survival analysis section
```

Types: `feat` | `fix` | `docs` | `data` | `style` | `refactor` | `test`

---

## What Never Ships

- A factual claim without a cited source
- A media asset without a complete asset register entry
- An ML output without uncertainty bounds
- A claim about a named individual that imputes motive
- A claim sourced only to a model's training data rather than documented evidence
- Content that presents correlation as causation without explicit caveat
- Anything that would not survive scrutiny from a music journalist, historian, or the Hall itself
- Em dashes. Ever.

---

## The Legal Standard

This platform holds itself to the standard of responsible investigative journalism:
- Every claim about a named individual is sourced to documented public record
- Statistical findings document correlation, not causation, and say so explicitly
- Documented statements are quoted accurately with full context
- The reader draws conclusions. The platform presents evidence.

---

## Data Sources

| Source | Coverage | License |
|--------|----------|---------|
| Rock Hall official inductee database | 1986-present | Public |
| MusicBrainz database | Full catalog | CC0 |
| Discogs database | Full catalog | CC0 subset |
| Billboard historical charts | 1958-present | Academic access |
| RIAA certification database | 1958-present | Public |
| AllMusic editorial ratings | Full catalog | Research use |
| Rolling Stone "Greatest" lists | 1967-present | Published lists |
| Future Rock Legends nomination database | 1986-present | Public |
| Wikidata | Full | CC0 |

---

## ML Models

| Model | Type | Chapter | Output |
|-------|------|---------|--------|
| Criteria Compliance | Weighted scoring | 00 | Score per artist |
| Teacher-Student Network | Graph analysis (networkx) | 01 | Gap distribution + racial decomposition |
| Survival Analysis | Cox proportional hazards (lifelines) | 02 | Hazard ratios, survival curves |
| Genre Diversity | Simpson's index + bias scores | 03 | Genre Bias Score by era |
| Wenner Coefficient | Logistic regression (scikit-learn) | 04 | Partial correlation after controls |
| AI Verdict Engine | Claude API + human review | 05 | Structured legal briefs |

---

## Chapter Tenets

The full chapter tenet standard is in `docs/chapter-tenets.md`. Every chapter is held to all fifteen tenets. Summary:

- Self-contained but cross-referenced
- Shared shell, chapter-specific interior
- Data and evidence at museum standard
- Opens with a name -- "Have you heard of [person]?"
- Narrative through line -- the prosecution question plus editorial connective tissue
- Uncertainty labeled at the point of claim, not just in methodology
- Methodology always visible and written for a curator
- Original finding (aspiration) -- documented at spec time
- "Oh wow" moment -- required, tested by all five agents
- ML and AI maximized -- real models, real data, confidence labels
- Design is elegant and authoritative
- Media assets verified before build begins
- Mobile first-class -- 375px minimum
- Chapter is citable -- three citation formats on every page
- Three hard build gates -- Spec, Build, Ship
