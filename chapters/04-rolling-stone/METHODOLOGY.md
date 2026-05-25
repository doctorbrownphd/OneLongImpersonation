# The Rolling Stone Connection -- Methodology
## onelongimpersonation.report/chapters/rolling-stone/

**Version:** 1.0
**Published:** May 2026
**Reviewed by:** Elias (statistical methodology) / Rosetta (historical grounding / legal standard)

---

## What This Chapter Does

Measures the correlation between Rolling Stone editorial attention and Rock Hall induction timing. Documents that artists with RS coverage waited a median 4 years; artists without waited 13. Documents committee composition from public records. Quotes named individuals from documented public sources only.

---

## Rolling Stone Attention Score

**Method:** Weighted composite of appearances across published RS lists:
- 100 Greatest Artists (weight: 10)
- 500 Greatest Albums (weight: 5)
- 100 Greatest Guitarists (weight: 3)
- 200 Greatest Singers (weight: 3)

Normalized to 0-100. This is a measure of EDITORIAL ATTENTION, not artistic quality.

---

## Wenner Coefficient

**Method:** Spearman rank correlation between RS Attention Score and induction wait time.
**Result:** rho = -0.43, p < 0.001
**Interpretation:** Strong negative correlation: higher RS attention correlates with shorter wait.

**CAUSATION CAVEAT:** This analysis documents CORRELATION. It does NOT prove that Rolling Stone coverage CAUSED faster induction. The correlation may reflect shared aesthetic preferences, overlapping social networks, or other confounders. The chapter states this explicitly. Multiple times.

---

## Named Individuals

All claims about Jann Wenner and other named individuals are sourced to:
- Documented public statements (interviews, podcasts, published articles)
- Public records (committee membership, board positions)
- Published reporting (Billboard, New York Times)

No motives are imputed. Documented facts are stated. The reader draws conclusions.

**Key sources:**
- Wenner NY Times interview: David Marchese, September 15, 2023
- Wenner podcast quote (Foreigner/Boston/Styx): 2022, documented in Billboard reporting
- Committee composition: Last fully disclosed 2015, supplemented by published reporting

---

## Reproducibility

```bash
cd pipeline
python src/ingest/rolling_stone.py
python src/models/wenner_coefficient.py
```

Output: `chapters/04-rolling-stone/wenner-data.js`
