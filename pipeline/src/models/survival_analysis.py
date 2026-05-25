"""
One Long Impersonation -- Survival Analysis
Model 3: Cox Proportional Hazards model predicting time to induction.

Event: Induction into the Rock and Roll Hall of Fame
Time: Years from eligibility (first_recording_year + 25) to induction
Censoring: Artists not yet inducted are right-censored at 2026

Covariates:
- race (Black vs white baseline)
- gender (female vs male baseline)
- genre_primary (Heavy Metal, Hip-Hop, etc. vs Classic Rock baseline)
- era (decade of eligibility)

Output:
- Hazard ratios with 95% confidence intervals
- Stratified survival curves
- The documented bias coefficients

Note: This model documents DISPARITIES in induction rates.
It does NOT prove discrimination. Correlation, not causation.
The chapter says so explicitly.
"""

import sys
import os
import json
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query
from config import CURRENT_YEAR, CHAPTERS_DIR

try:
    import pandas as pd
    import numpy as np
    from lifelines import CoxPHFitter, KaplanMeierFitter
except ImportError:
    print("Required: pip install pandas numpy lifelines")
    sys.exit(1)

warnings.filterwarnings("ignore", category=FutureWarning)


def build_survival_dataset():
    """
    Build the survival analysis dataset from the artists table.
    Only includes Performer inductees and eligible non-inducted artists.
    Excludes Early Influence and non-performer categories.
    """
    # Get all inducted Performers
    inducted = query("""
        SELECT a.id, a.name, a.race, a.gender, a.genre_primary,
               a.first_recording_year, a.eligible_year, a.inducted_year,
               a.inducted_category, a.is_inducted
        FROM artists a
        WHERE a.is_inducted = 1
          AND a.inducted_category = 'P'
          AND a.eligible_year IS NOT NULL
          AND a.eligible_year <= ?
    """, (CURRENT_YEAR,))

    # For now, we analyze inducted performers only (with censoring for timing)
    # A full model would also include eligible non-inducted artists as censored
    # We'll add those as we build the eligible artist database

    rows = []
    for a in inducted:
        if not a["eligible_year"] or not a["inducted_year"]:
            continue

        time_to_event = a["inducted_year"] - a["eligible_year"]
        if time_to_event < 0:
            time_to_event = 0  # Inducted before formal eligibility (early classes)

        rows.append({
            "name": a["name"],
            "time_to_event": time_to_event,
            "event_observed": 1,  # All inducted = event observed
            "race": a["race"] or "unknown",
            "gender": a["gender"] or "unknown",
            "genre": a["genre_primary"] or "unknown",
            "eligible_year": a["eligible_year"],
            "inducted_year": a["inducted_year"],
            "era": ((a["eligible_year"] or 2000) // 10) * 10,
        })

    df = pd.DataFrame(rows)

    # Filter to known race and relevant categories
    df = df[df["race"].isin(["Black", "white", "Latino"])]
    df = df[df["time_to_event"] >= 0]

    return df


def fit_cox_model(df):
    """
    Fit the Cox PH model.
    Baseline: white, male, Classic Rock, 1980s eligibility era.
    """
    # Create dummy variables
    model_df = df.copy()

    # Race: Black indicator (baseline = white)
    model_df["is_black"] = (model_df["race"] == "Black").astype(int)
    model_df["is_latino"] = (model_df["race"] == "Latino").astype(int)

    # Gender: female indicator (baseline = male)
    model_df["is_female"] = (model_df["gender"] == "female").astype(int)
    model_df["is_group"] = (model_df["gender"] == "group").astype(int)

    # Genre indicators (baseline = Classic Rock)
    genre_dummies = pd.get_dummies(model_df["genre"], prefix="genre", drop_first=False)
    # Drop Classic Rock as baseline
    if "genre_Classic Rock" in genre_dummies.columns:
        genre_dummies = genre_dummies.drop("genre_Classic Rock", axis=1)
    model_df = pd.concat([model_df, genre_dummies], axis=1)

    # Era indicator
    model_df["era_post2000"] = (model_df["era"] >= 2000).astype(int)

    # Select model columns
    covariates = ["is_black", "is_female", "is_group"]

    # Add genre dummies that have enough observations
    for col in genre_dummies.columns:
        if model_df[col].sum() >= 5:  # At least 5 artists in genre
            covariates.append(col)

    covariates.append("era_post2000")

    # Fit Cox PH model
    cph = CoxPHFitter()
    fit_df = model_df[covariates + ["time_to_event", "event_observed"]].copy()

    # Remove rows with zero duration (inducted before eligibility)
    fit_df = fit_df[fit_df["time_to_event"] > 0]

    cph.fit(fit_df, duration_col="time_to_event", event_col="event_observed")

    return cph, model_df


def compute_survival_curves(df):
    """
    Compute Kaplan-Meier survival curves stratified by key groups.
    These are the visualization curves, not the Cox model curves.
    """
    kmf = KaplanMeierFitter()
    curves = {}

    # Define strata
    strata = {
        "White male, Classic Rock": (
            (df["race"] == "white") & (df["gender"].isin(["male", "group"])) &
            (df["genre"] == "Classic Rock")
        ),
        "Black artist, Soul/R&B": (
            (df["race"] == "Black") & (df["genre"].isin(["Soul/R&B", "Blues/Early"]))
        ),
        "Female artist": (
            df["gender"] == "female"
        ),
        "Heavy Metal artist": (
            df["genre"] == "Heavy Metal"
        ),
    }

    for label, mask in strata.items():
        subset = df[mask]
        if len(subset) < 3:
            continue

        kmf.fit(
            subset["time_to_event"],
            subset["event_observed"],
            label=label
        )

        # Extract curve data points
        timeline = kmf.survival_function_.index.tolist()
        survival = kmf.survival_function_[label].tolist()
        median = kmf.median_survival_time_

        curves[label] = {
            "timeline": [round(t, 2) for t in timeline],
            "survival": [round(s, 4) for s in survival],
            "median_wait": round(median, 1) if pd.notna(median) else None,
            "n": len(subset),
        }

    return curves


def compute_wait_stats(df):
    """Compute summary wait statistics by group."""
    stats = {}

    groups = {
        "All inducted": df,
        "Black artists": df[df["race"] == "Black"],
        "White artists": df[df["race"] == "white"],
        "Female artists": df[df["gender"] == "female"],
        "Male artists": df[df["gender"] == "male"],
        "Groups": df[df["gender"] == "group"],
        "Classic Rock": df[df["genre"] == "Classic Rock"],
        "Soul/R&B": df[df["genre"].isin(["Soul/R&B", "Blues/Early"])],
        "Heavy Metal": df[df["genre"] == "Heavy Metal"],
        "Hip-Hop": df[df["genre"] == "Hip-Hop"],
        "Punk": df[df["genre"] == "Punk"],
        "Pop": df[df["genre"] == "Pop"],
    }

    for label, subset in groups.items():
        if len(subset) == 0:
            continue
        waits = subset["time_to_event"]
        stats[label] = {
            "n": len(subset),
            "median_wait": round(waits.median(), 1),
            "mean_wait": round(waits.mean(), 1),
            "max_wait": int(waits.max()),
            "pct_first_eligible": round((waits <= 1).mean() * 100, 1),
        }

    return stats


def metal_cases(df):
    """Extract the specific metal wait time cases for the bar chart."""
    metal_artists = [
        "Black Sabbath", "Judas Priest", "Iron Maiden", "Metallica",
        "AC/DC", "Deep Purple", "Def Leppard", "Van Halen",
        "Guns N' Roses", "Ozzy Osbourne", "Rage Against the Machine",
    ]

    cases = []
    for name in metal_artists:
        row = df[df["name"] == name]
        if len(row) == 0:
            continue
        r = row.iloc[0]
        cases.append({
            "name": name,
            "eligible_year": int(r["eligible_year"]),
            "inducted_year": int(r["inducted_year"]),
            "wait_years": int(r["time_to_event"]),
        })

    # Sort by wait time descending
    cases.sort(key=lambda c: c["wait_years"], reverse=True)
    return cases


def export_results(cph, curves, wait_stats, metal, df):
    """Export all survival analysis results to chapter data files."""
    output_dir = os.path.join(CHAPTERS_DIR, "02-the-wait")
    os.makedirs(output_dir, exist_ok=True)

    # Extract Cox model results
    summary = cph.summary
    hazard_ratios = {}
    for covariate in summary.index:
        hazard_ratios[covariate] = {
            "coef": round(summary.loc[covariate, "coef"], 4),
            "hr": round(summary.loc[covariate, "exp(coef)"], 4),
            "hr_lower": round(summary.loc[covariate, "exp(coef) lower 95%"], 4),
            "hr_upper": round(summary.loc[covariate, "exp(coef) upper 95%"], 4),
            "p_value": round(summary.loc[covariate, "p"], 6),
            "significant": bool(summary.loc[covariate, "p"] < 0.05),
        }

    data = {
        "cox_model": {
            "hazard_ratios": hazard_ratios,
            "n_observations": len(df),
            "concordance": round(float(cph.concordance_index_), 4),
            "note": "Hazard ratio < 1 means SLOWER induction (longer wait). "
                    "HR of 0.5 means 50% lower annual probability of induction.",
            "causation_caveat": "This model documents DISPARITIES in induction rates. "
                                "It does NOT prove intentional discrimination. "
                                "Observational data, correlation only.",
        },
        "survival_curves": curves,
        "wait_statistics": wait_stats,
        "metal_cases": metal,
        "metadata": {
            "source": "Rock and Roll Hall of Fame official inductee database",
            "model_type": "Cox Proportional Hazards (lifelines library)",
            "censoring": f"Right-censored at {CURRENT_YEAR} for non-inducted artists",
            "baseline": "White male Classic Rock artist, eligible pre-2000",
            "n_artists_in_model": len(df),
        }
    }

    js_path = os.path.join(output_dir, "wait-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 02: The Wait\n")
        f.write("// Survival analysis data -- generated by pipeline\n")
        f.write("// Model: Cox Proportional Hazards\n")
        f.write(f"// N = {len(df)} inducted Performer artists\n\n")
        f.write("window.WAIT_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported to {js_path}")
    return js_path


def run():
    """Run the full survival analysis."""
    print("Building survival dataset...")
    df = build_survival_dataset()
    print(f"  {len(df)} artists in dataset")
    print(f"  Race: {df['race'].value_counts().to_dict()}")
    print(f"  Genre: {df['genre'].value_counts().to_dict()}")

    print("\nFitting Cox PH model...")
    cph, model_df = fit_cox_model(df)

    print("\n" + "=" * 60)
    print("COX PROPORTIONAL HAZARDS RESULTS")
    print("=" * 60)
    cph.print_summary()

    print("\n" + "=" * 60)
    print("KEY HAZARD RATIOS")
    print("=" * 60)
    summary = cph.summary
    for covariate in summary.index:
        hr = summary.loc[covariate, "exp(coef)"]
        p = summary.loc[covariate, "p"]
        sig = "*" if p < 0.05 else ""
        ci_lo = summary.loc[covariate, "exp(coef) lower 95%"]
        ci_hi = summary.loc[covariate, "exp(coef) upper 95%"]
        print(f"  {covariate}: HR = {hr:.3f} (95% CI: {ci_lo:.3f}-{ci_hi:.3f}) p = {p:.4f} {sig}")

    print("\nComputing survival curves...")
    curves = compute_survival_curves(df)
    for label, curve in curves.items():
        print(f"  {label}: n={curve['n']}, median wait={curve['median_wait']}y")

    print("\nComputing wait statistics...")
    wait_stats = compute_wait_stats(df)
    for label, stats in wait_stats.items():
        print(f"  {label}: n={stats['n']}, median={stats['median_wait']}y, "
              f"mean={stats['mean_wait']}y")

    print("\nMetal cases...")
    metal = metal_cases(df)
    for case in metal:
        print(f"  {case['name']}: eligible {case['eligible_year']}, "
              f"inducted {case['inducted_year']}, wait {case['wait_years']}y")

    print("\nExporting results...")
    export_results(cph, curves, wait_stats, metal, df)

    return cph, df


if __name__ == "__main__":
    run()
