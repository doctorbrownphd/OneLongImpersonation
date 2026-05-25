"""
One Long Impersonation -- Wenner Coefficient Model
Model 5: Logistic regression measuring Rolling Stone editorial influence
on Hall of Fame induction probability.

The Wenner Coefficient = partial correlation between Rolling Stone
Attention Score and induction probability, AFTER controlling for
criteria-relevant variables (genre, era, commercial indicators).

This model documents CORRELATION, not CAUSATION.
The chapter says so explicitly. Multiple times.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query
from config import CURRENT_YEAR, CHAPTERS_DIR

try:
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from scipy import stats as scipy_stats
except ImportError:
    print("Required: pip install pandas numpy scikit-learn scipy")
    sys.exit(1)


def build_dataset():
    """
    Build the dataset for the Wenner Coefficient model.
    Uses inducted Performer artists with RS Attention Scores.
    """
    rows = query("""
        SELECT
            a.id, a.name, a.race, a.gender, a.genre_primary,
            a.first_recording_year, a.eligible_year,
            a.inducted_year, a.is_inducted,
            a.rs_attention_score,
            a.inducted_category
        FROM artists a
        WHERE a.inducted_category = 'P' OR a.inducted_category IS NULL
        ORDER BY a.name
    """)

    data = []
    for r in rows:
        rs_score = r["rs_attention_score"] or 0
        inducted = 1 if r["is_inducted"] else 0

        data.append({
            "name": r["name"],
            "inducted": inducted,
            "rs_attention_score": rs_score,
            "has_rs_coverage": 1 if rs_score > 0 else 0,
            "genre": r["genre_primary"] or "unknown",
            "race": r["race"] or "unknown",
            "gender": r["gender"] or "unknown",
            "eligible_year": r["eligible_year"],
        })

    df = pd.DataFrame(data)
    return df


def compute_wenner_coefficient(df):
    """
    Compute the Wenner Coefficient via logistic regression.

    We measure: how much does Rolling Stone coverage predict induction
    BEYOND what genre and era alone would predict?

    Since our current dataset is mostly inducted artists (we don't yet
    have the full eligible non-inducted population), we use a correlation
    approach: among inducted artists, does RS Attention Score predict
    SPEED of induction (wait time)?

    This is a preliminary analysis. The full model requires the eligible
    non-inducted population as controls.
    """
    # For now, compute the correlation between RS score and wait time
    # among inducted performers
    inducted = df[df["inducted"] == 1].copy()
    inducted = inducted[inducted["eligible_year"].notna()].copy()

    if "inducted_year" not in inducted.columns:
        # Compute from database
        for idx, row in inducted.iterrows():
            artist = query(
                "SELECT inducted_year FROM artists WHERE name = ? LIMIT 1",
                (row["name"],)
            )
            if artist:
                inducted.loc[idx, "inducted_year"] = artist[0]["inducted_year"]

    # Use RS attention score to predict whether artist was inducted quickly
    # (within 5 years of eligibility) vs slowly
    inducted["wait_time"] = inducted.apply(
        lambda r: query(
            "SELECT inducted_year FROM artists WHERE name = ? LIMIT 1",
            (r["name"],)
        )[0]["inducted_year"] - r["eligible_year"] if r["eligible_year"] else None,
        axis=1
    )

    inducted = inducted.dropna(subset=["wait_time"])
    inducted = inducted[inducted["wait_time"] >= 0]

    # Correlation: RS attention score vs wait time
    # Negative correlation = higher RS score -> shorter wait
    rs_scores = inducted["rs_attention_score"]
    wait_times = inducted["wait_time"]

    # Pearson correlation
    r_val, p_val = scipy_stats.pearsonr(rs_scores, wait_times)

    # Spearman (rank) correlation -- more robust
    rho, rho_p = scipy_stats.spearmanr(rs_scores, wait_times)

    # Split analysis: high RS vs low RS
    has_rs = inducted[inducted["rs_attention_score"] > 0]
    no_rs = inducted[inducted["rs_attention_score"] == 0]

    results = {
        "pearson_r": round(float(r_val), 4),
        "pearson_p": round(float(p_val), 6),
        "spearman_rho": round(float(rho), 4),
        "spearman_p": round(float(rho_p), 6),
        "n_with_rs": len(has_rs),
        "n_without_rs": len(no_rs),
        "median_wait_with_rs": round(float(has_rs["wait_time"].median()), 1),
        "median_wait_without_rs": round(float(no_rs["wait_time"].median()), 1),
        "mean_wait_with_rs": round(float(has_rs["wait_time"].mean()), 1),
        "mean_wait_without_rs": round(float(no_rs["wait_time"].mean()), 1),
    }

    return results, inducted


def build_scatter_data(inducted_df):
    """Build data points for the RS Attention vs Wait Time scatter plot."""
    points = []
    for _, row in inducted_df.iterrows():
        if pd.isna(row["wait_time"]):
            continue
        points.append({
            "name": row["name"],
            "rs_score": round(float(row["rs_attention_score"]), 2),
            "wait_time": int(row["wait_time"]),
            "genre": row["genre"],
            "race": row["race"],
        })

    # Sort by RS score for visual clarity
    points.sort(key=lambda p: p["rs_score"], reverse=True)
    return points


def committee_data():
    """
    Documented nominating committee composition.
    Sources: Billboard, published reports, Jann Wenner public statements.
    """
    return {
        "wenner_tenure": {
            "committee_member": "1986-2006",
            "chairman": "2006-2019",
            "board_removed": "September 2023",
            "removal_source": "New York Times interview, September 2023"
        },
        "documented_rs_connections": [
            {
                "name": "Jann Wenner",
                "role": "Founder, Rolling Stone; Chairman, Rock Hall Foundation",
                "years": "1986-2019",
                "source": "Rock Hall Foundation public records"
            },
            {
                "name": "John Sykes",
                "role": "Chairman (post-Wenner)",
                "years": "2020-present",
                "source": "Rock Hall Foundation announcement, 2019"
            }
        ],
        "wenner_quote_2023": {
            "quote": "Wenner told the New York Times that Black and female artists did not meet his 'historical standard.'",
            "source": "New York Times, David Marchese interview, September 15, 2023",
            "context": "Interview promoting Wenner's book 'The Masters.' Wenner was asked why no women or Black artists were featured."
        },
        "wenner_quote_2022": {
            "quote": "Foreigner, Boston, Styx, and 'that whole era' had simply 'never come up' in nominating committee discussions.",
            "source": "Podcast interview, 2022 (documented in Billboard reporting)",
            "context": "Wenner explaining why certain classic rock and arena rock bands were never nominated during his committee tenure."
        },
        "note": "All claims about named individuals are sourced to documented public statements. No motives are imputed."
    }


def export_results(results, scatter, committee):
    """Export Wenner Coefficient data to chapter file."""
    output_dir = os.path.join(CHAPTERS_DIR, "04-rolling-stone")
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "wenner_coefficient": results,
        "scatter_data": scatter,
        "committee": committee,
        "metadata": {
            "source": "Rolling Stone published lists (500 Greatest Albums, 100 Greatest Artists, etc.)",
            "method": "Pearson and Spearman correlation between RS Attention Score and induction wait time",
            "causation_caveat": "This analysis documents CORRELATION between Rolling Stone editorial "
                                "attention and Hall of Fame induction timing. It does NOT prove that "
                                "Rolling Stone coverage CAUSED faster induction. The correlation may "
                                "reflect shared aesthetic preferences rather than direct influence. "
                                "The chapter states this explicitly.",
            "rs_score_method": "Weighted composite of appearances across 4 major Rolling Stone lists. "
                               "Not a measure of artistic quality. A measure of editorial attention.",
            "limitation": "The full Wenner Coefficient model requires the eligible non-inducted "
                          "population as controls. This preliminary analysis uses induction wait "
                          "time as the outcome variable instead."
        }
    }

    js_path = os.path.join(output_dir, "wenner-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 04: The Rolling Stone Connection\n")
        f.write("// Wenner Coefficient data -- generated by pipeline\n")
        f.write("// CORRELATION, NOT CAUSATION. The chapter says so explicitly.\n\n")
        f.write("window.WENNER_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported to {js_path}")
    return js_path


def run():
    """Run the Wenner Coefficient analysis."""
    print("Building dataset...")
    df = build_dataset()
    print(f"  {len(df)} artists in dataset")

    print("\nComputing Wenner Coefficient...")
    results, inducted_df = compute_wenner_coefficient(df)

    print("\n" + "=" * 60)
    print("WENNER COEFFICIENT FINDINGS")
    print("=" * 60)
    print(f"Pearson r (RS score vs wait time): {results['pearson_r']} (p = {results['pearson_p']})")
    print(f"Spearman rho: {results['spearman_rho']} (p = {results['spearman_p']})")
    print(f"\nArtists with RS coverage: {results['n_with_rs']}")
    print(f"  Median wait: {results['median_wait_with_rs']} years")
    print(f"Artists without RS coverage: {results['n_without_rs']}")
    print(f"  Median wait: {results['median_wait_without_rs']} years")
    print(f"\nDifference: {results['median_wait_without_rs'] - results['median_wait_with_rs']} years longer wait without RS coverage")

    print("\nBuilding scatter data...")
    scatter = build_scatter_data(inducted_df)
    print(f"  {len(scatter)} data points")

    committee = committee_data()

    print("\nExporting...")
    export_results(results, scatter, committee)

    return results


if __name__ == "__main__":
    run()
