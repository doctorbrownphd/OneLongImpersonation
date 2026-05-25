# One Long Impersonation -- Methodology
## onelongimpersonation.report/chapters/teachers/

**Version:** 1.0
**Published:** May 2026
**Reviewed by:** Elias (statistical methodology) / Rosetta (historical grounding)

---

## What This Chapter Does

For every inducted artist, we identify documented teacher-student influence relationships from primary sources. We then measure the gap between when the student was inducted and when the teacher was inducted (or whether the teacher was ever inducted). The distribution of this gap, broken down by the racial composition of each pair, reveals a 29-year unexplained difference between Black-teacher/white-student pairs and same-race pairs.

---

## Data Sources

### Curated Influence Pairs
- **Source:** Published interviews, liner notes, biographies, academic sources
- **File:** `pipeline/data/curated/influence_pairs.yaml` and `influence_pairs_expanded.yaml`
- **Coverage:** 73 documented teacher-student pairs
- **License:** CC0 (our compilation; citations are to published sources)
- **Known limitations:** Not exhaustive. Biased toward well-documented relationships. Expanded over time.
- **How used:** Each pair establishes a documented influence relationship between a teacher and student artist.

### Rock Hall Inductee Database
- **Source:** rockhall.com official records
- **Coverage:** All inductions 1986-2026
- **License:** Public information
- **How used:** Provides induction year for gap calculation.

---

## Analytical Methods

### Teacher-Student Gap Metric
**What it does:** Measures the time gap between when a teacher was inducted and when their student was inducted.

**Calculation:**
- If both inducted: gap = teacher_inducted_year - student_inducted_year
- If teacher never inducted: gap = current_year (2026) - student_inducted_year

**Uncertainty:** The gap is a documented fact, not an estimate. The racial decomposition is a calculated breakdown, not an assertion.

**Limitations:** The gap metric does not control for commercial success or critical reception. It documents timing disparities only.

### Network Centrality (PageRank)
**What it does:** Identifies which artists sit at the most influential nodes in the documented influence graph.

**Library:** networkx (Python)
**Parameters:** alpha = 0.85 (standard PageRank damping factor)

**Limitations:** The graph is sparse (73 edges). PageRank is meaningful but should not be over-interpreted from a small graph.

---

## Key Findings

| Metric | Value | Confidence |
|--------|-------|------------|
| Total documented pairs | 73 | Documented |
| BW median gap | 32 years | Documented |
| Same-race median gap | 3 years | Documented |
| Unexplained difference | 29 years | Modeled |

---

## Data Gaps

| Gap | Impact | How Handled |
|-----|--------|-------------|
| Not all influence relationships are documented | Graph is incomplete | Labeled as "documented pairs only" |
| Some teachers never made Performer category | Gap uses current year as proxy | Documented in visualization |
| Big Mama Thornton race classified manually | Could affect composition coding | Classification documented with source |

---

## Reproducibility

```bash
cd pipeline
python src/ingest/load_curated_pairs.py
python src/models/teacher_student_network.py
```

Output: `chapters/01-teachers/teachers-data.js`
