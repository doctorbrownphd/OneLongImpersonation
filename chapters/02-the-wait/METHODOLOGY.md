# The Wait -- Methodology
## onelongimpersonation.report/chapters/the-wait/

**Version:** 1.0
**Published:** May 2026
**Reviewed by:** Elias (statistical methodology) / Rosetta (historical grounding)

---

## What This Chapter Does

We fit a Cox Proportional Hazards survival model predicting time from eligibility to induction, controlling for race, gender, genre, and era. The model documents disparities in induction rates. It does NOT prove intentional discrimination. The distinction matters legally and scientifically.

---

## Data Sources

### Rock Hall Inductee Database
- **Coverage:** 256 inducted Performer artists with eligibility and induction dates
- **License:** Public information

---

## Model: Cox Proportional Hazards

**Library:** lifelines 0.29+ (Python)
**Event:** Induction. **Time:** Years from eligibility to induction.
**Censoring:** Right-censored at 2026 for non-inducted artists.
**Baseline:** White male Classic Rock artist, eligible pre-2000.

**Covariates:**
- `is_black`: Black artist indicator
- `is_female`: Female artist indicator
- `is_group`: Group indicator
- Genre dummies (baseline: Classic Rock)
- `era_post2000`: Eligible after 2000

**Interpretation:** Hazard ratio < 1 means SLOWER induction. HR of 0.5 = 50% lower annual induction probability.

**Concordance index:** 0.63 (moderate discriminative ability)

---

## Kaplan-Meier Survival Curves

Four strata computed independently:
1. White male, Classic Rock (n=112, median wait: 6y)
2. Black artist, Soul/R&B (n=66, median wait: 12y)
3. Female artist (n=31, median wait: 14y)
4. Heavy Metal artist (n=5, median wait: 12y)

---

## Causation Caveat

This model documents DISPARITIES in induction rates after controlling for observable characteristics. It does NOT prove that these disparities were caused by intentional discrimination. The data is observational. Unmeasured confounders may exist. The chapter states this explicitly.

---

## Reproducibility

```bash
cd pipeline
python src/models/survival_analysis.py
```

Output: `chapters/02-the-wait/wait-data.js`
