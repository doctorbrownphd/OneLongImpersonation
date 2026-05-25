# One Long Impersonation

> *"My whole career has been one long Sister Rosetta Tharpe impersonation."*
> -- Chuck Berry, Rock and Roll Hall of Fame induction ceremony, 1986

A data-driven prosecution of the Rock and Roll Hall of Fame using their own stated criteria as the instrument of indictment.

**Domain:** onelongimpersonation.report
**Standard:** Museum quality. Legally defensible. Citable.
**License:** MIT (code) / CC0 (data)

---

## The Platform

Seven chapters organized as a legal prosecution. Every finding sourced. Every verdict rendered by the data. The reader is the jury.

| Chapter | Title | Model |
|---------|-------|-------|
| 00 | The Criteria | Criteria Compliance Score |
| 01 | One Long Impersonation | Teacher-Student Network (networkx) |
| 02 | The Wait | Cox Proportional Hazards (lifelines) |
| 03 | The Genre Desertification | Simpson's Diversity Index |
| 04 | The Rolling Stone Connection | Wenner Coefficient (correlation) |
| 05 | The Docket | AI Verdict Engine (Claude API) |
| 06 | The Other Side | Post-2019 improvement analysis |

---

## Key Findings

| Finding | Value |
|---------|-------|
| Teacher-student gap (Black teacher, white student) | **32 years** median |
| Teacher-student gap (same-race pairs) | **3 years** median |
| Unexplained difference | **29 years** |
| RS coverage vs wait time (Spearman) | **rho = -0.43** |
| Wait with RS coverage | **4 years** median |
| Wait without RS coverage | **13 years** median |
| Heavy Metal bias (Wenner era) | **0.47** |
| Heavy Metal bias (post-Wenner) | **4.15** |
| Genre diversity improvement | **1.19x** post-2019 |

---

## Data Pipeline

```bash
cd pipeline
make setup    # Create venv, install deps, initialize SQLite
make ingest   # Ingest from all sources
make models   # Run all 5 ML models
make export   # Export to chapter data files
```

Database: 402 artists, 73 documented influence pairs, 132 RS list appearances, 113 eligible non-inducted artists with criteria scores.

---

## Tech Stack

Vanilla HTML/CSS/JS + D3.js. No framework. No build step. Static files.

Python data pipeline: pandas, lifelines, networkx, scikit-learn, musicbrainzngs.

---

## Sibling Project

[The Other Box Score](https://theotherboxscore.org) -- the same mission, different institution. A museum-quality data journalism platform dedicated to the Negro Leagues.

---

## Agent Team

Five agents review every chapter before it ships:

- **Rosetta** -- Music history accuracy (named for Sister Rosetta Tharpe)
- **Elias** -- Statistical methodology
- **Vera** -- Visualization and assets
- **Ida** -- Project coherence
- **Gates** -- Final QA gate

---

*They built a hall of fame for the music. They forgot who built the music.*
