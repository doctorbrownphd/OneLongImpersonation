# The Genre Desertification -- Methodology
## onelongimpersonation.report/chapters/genre/

**Version:** 1.0
**Published:** May 2026
**Reviewed by:** Elias (statistical methodology) / Rosetta (historical grounding)

---

## What This Chapter Does

Measures genre representation among inductees by year using Simpson's Diversity Index, the same metric ecologists use to measure species diversity. Compares the Wenner era (1986-2019) to the post-Wenner era (2020-2026). Documents which genres were systematically under-inducted relative to the eligible population.

---

## Analytical Methods

### Simpson's Diversity Index
**Formula:** D = 1 - sum(p_i^2) where p_i = proportion of inductees in genre i
**Range:** 0 (no diversity) to approaching 1 (maximum diversity)
**Computed:** Per induction year and aggregated by era

### Genre Bias Score
**Formula:** (genre share among inductees in era) / (genre share among ALL inductees)
**Interpretation:** 1.0 = proportional. < 1.0 = underrepresented. > 1.0 = overrepresented.
**Limitation:** Uses all-time inductee share as denominator, not eligible population share. Full model would use eligible population.

---

## Key Findings

| Finding | Value |
|---------|-------|
| Simpson's (Wenner era) | 0.67 |
| Simpson's (post-Wenner) | 0.80 |
| Improvement | 1.19x |
| Heavy Metal bias (Wenner) | 0.47 |
| Heavy Metal bias (post) | 4.15 |
| Electronic (Wenner) | 0.00 |
| Electronic (post) | 6.92 |

---

## Reproducibility

```bash
cd pipeline
python src/models/genre_diversity.py
```

Output: `chapters/03-genre/genre-data.js`
