# One Long Impersonation -- Global Methodology

**Version:** 1.0
**Published:** May 2026
**Reviewed by:** Elias (statistical methodology) / Rosetta (historical grounding)

---

## What This Platform Does

One Long Impersonation applies the Rock and Roll Hall of Fame's five stated induction criteria to documented evidence about every eligible artist, measuring who was inducted, how long they waited, what genres were included or excluded, and how editorial influence correlated with induction decisions. Every finding is sourced. Every verdict is rendered by the data.

---

## Data Sources

### Rock and Roll Hall of Fame Official Records
- **Source:** rockhall.com, public press releases, published reporting
- **Coverage:** All inductions 1986-2026, all categories
- **License:** Public information
- **Known limitations:** Nomination history only partially public. Fan vote data incomplete before 2012.

### MusicBrainz
- **Source:** musicbrainz.org
- **Coverage:** Artist relationships, release groups, genre tags
- **License:** CC0
- **Access:** API (musicbrainzngs library), rate-limited to 1 req/sec
- **Known limitations:** Influence relationships sparsely populated. Supplemented by curated pairs.

### Curated Influence Pairs
- **Source:** Published interviews, liner notes, biographies, academic sources
- **Coverage:** 73 documented teacher-student pairs with primary source citations
- **License:** CC0 (our compilation)
- **Known limitations:** Not exhaustive. Biased toward well-documented artists. Expanded over time.

### Rolling Stone Published Lists
- **Source:** 500 Greatest Albums, 100 Greatest Artists, 100 Greatest Guitarists, 200 Greatest Singers
- **Coverage:** Major published lists 2003-2023
- **License:** Published lists (factual data not copyrightable)
- **Known limitations:** Proxy for editorial attention, not artistic quality. Lists have their own biases.

### Wikidata
- **Source:** wikidata.org
- **Coverage:** Demographics (ethnic group, gender, citizenship)
- **License:** CC0
- **Known limitations:** Ethnic group (P172) coverage ~40-60% for musicians. Supplemented by manual curation.

---

## Models

### Model 1: Criteria Compliance Score
- **Type:** Weighted composite scoring (0-100)
- **Weights:** Excellence 0.25, Influence 0.25, Career Length 0.15, Catalog Depth 0.15, Genre Contribution 0.20
- **Note:** This is a CONSTRUCT. The weights are documented choices, not empirically derived. Sensitivity analysis required before publication.
- **Output:** Score for every artist in the database

### Model 2: Teacher-Student Network
- **Type:** Directed graph analysis (networkx)
- **Input:** 73 documented influence pairs with primary source citations
- **Output:** Gap distribution with racial decomposition, PageRank centrality
- **Key finding:** 32-year median gap for Black teacher / white student pairs vs 3-year for same-race pairs. 29-year unexplained difference.

### Model 3: Survival Analysis
- **Type:** Cox Proportional Hazards (lifelines library)
- **Input:** 256 inducted Performer artists with eligibility and induction dates
- **Covariates:** Race, gender, genre, era
- **Censoring:** Right-censored at 2026 for non-inducted artists
- **Key finding:** Female artists: 14-year median wait. Classic Rock: 6-year. Heavy Metal: 12-year.
- **Causation caveat:** Documents DISPARITIES, not discrimination. Observational data only.

### Model 4: Genre Diversity
- **Type:** Simpson's Diversity Index + Genre Bias Score
- **Input:** All Performer inductions by year and genre
- **Key finding:** Heavy Metal bias 0.47 (Wenner era) to 4.15 (post-Wenner). Simpson's diversity 0.67 to 0.80.

### Model 5: Wenner Coefficient
- **Type:** Correlation analysis (Pearson + Spearman)
- **Input:** RS Attention Score vs induction wait time
- **Key finding:** Spearman rho = -0.43 (p < 0.001). 4-year median wait with RS coverage vs 13-year without.
- **Causation caveat:** CORRELATION, not causation. Stated explicitly in the chapter. Multiple times.

### Model 6: AI Verdict Engine
- **Type:** Claude API (claude-sonnet-4-20250514) structured generation
- **Input:** Artist data record from pipeline database ONLY
- **Output:** Structured legal brief per artist
- **Verdict classification:** Computed from criteria score percentiles, not from Claude's judgment
- **Human review:** Required before publication

---

## Confidence Level Vocabulary

| Term | Meaning |
|------|---------|
| Documented | Appears in a primary source with specific citation |
| Verified | Cross-referenced across multiple independent sources |
| Reported | Appears in a single secondary source |
| Estimated | Derived from incomplete data using documented assumptions |
| Modeled | Output of an ML or statistical model with stated confidence bounds |
| AI-generated | Produced by Claude API with human review |

---

## What This Platform Cannot Show

This platform documents patterns in outcomes. It does not prove intent. The statistical models document disparities, correlations, and gaps. They do not prove that any individual acted with discriminatory purpose. The legal standard is responsible investigative journalism: documented facts, sourced claims, transparent methodology. The reader draws conclusions.

---

## Reproducibility

All code: `pipeline/` directory, MIT licensed.
All data: CC0 licensed.
Environment: Python 3.12+, requirements in `pipeline/requirements.txt`.

```bash
cd pipeline
make setup    # Creates venv, installs deps, initializes DB
make ingest   # Runs all data ingestion
make models   # Runs all ML models
make export   # Exports to chapter data files
```

---

## Citation

Haynes, Jeremy. "One Long Impersonation: Methodology." One Long Impersonation, May 2026.
https://onelongimpersonation.report/methodology/

Data: CC0 1.0 -- freely reusable.
