"""
One Long Impersonation -- Criteria Compliance Model
Model 1: Operationalizes the Hall's five stated criteria into a 0-100 score.

The Hall's criteria:
1. Musical excellence -- proxied by RS Attention Score, Grammy-level recognition
2. Influence on other performers -- proxied by influence graph centrality
3. Length of career -- years active
4. Depth of catalog -- studio album count
5. Contributions to rock and roll -- genre pioneer status, first-mover

IMPORTANT: This model is a CONSTRUCT. Operationalizing "musical excellence" and
"influence" requires subjective weighting decisions. Those weights are documented.
The sensitivity of findings to weight changes is documented. The model is useful
and defensible, but it is not ground truth.

Weights from config.py:
  excellence: 0.25, influence: 0.25, career_length: 0.15,
  catalog_depth: 0.15, genre_contribution: 0.20
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import CURRENT_YEAR, CHAPTERS_DIR, CRITERIA_WEIGHTS

try:
    import numpy as np
except ImportError:
    print("numpy not installed. Run: pip install numpy")
    sys.exit(1)


def compute_excellence_score(artist):
    """
    Musical excellence proxy.
    Based on Rolling Stone Attention Score (0-100 normalized).
    In full pipeline: would also include AllMusic ratings, Grammy nominations.
    """
    rs = artist.get("rs_attention_score") or 0
    return min(rs, 100.0)


def compute_influence_score(artist_id):
    """
    Influence on other performers proxy.
    Based on number of documented influence relationships (as teacher).
    In full pipeline: would use PageRank centrality from full MusicBrainz graph.
    """
    pairs = query("""
        SELECT COUNT(*) as n FROM influence_pairs WHERE teacher_id = ?
    """, (artist_id,))
    outbound = pairs[0]["n"] if pairs else 0

    # Also count inbound (this artist was influenced by)
    inbound = query("""
        SELECT COUNT(*) as n FROM influence_pairs WHERE student_id = ?
    """, (artist_id,))[0]["n"]

    # Weight outbound (teacher) more than inbound (student)
    raw = outbound * 15 + inbound * 5
    return min(raw, 100.0)


def compute_career_length_score(artist):
    """
    Length of career proxy.
    Years from first recording to last active (or current year).
    Normalized: 50+ years = 100.
    """
    first = artist.get("first_recording_year")
    last = artist.get("last_active_year") or CURRENT_YEAR

    if not first:
        return 0.0

    years = last - first
    # Normalize: 50 years = 100, proportional below that
    return min(years / 50.0 * 100, 100.0)


def compute_catalog_score(artist):
    """
    Depth of catalog proxy.
    Studio album count.
    Normalized: 15+ albums = 100.
    """
    albums = artist.get("studio_album_count") or 0

    if albums == 0:
        # Estimate from career length if no catalog data
        first = artist.get("first_recording_year")
        if first:
            years = CURRENT_YEAR - first
            albums = max(1, years // 4)  # Rough estimate: 1 album per 4 years

    return min(albums / 15.0 * 100, 100.0)


def compute_genre_contribution_score(artist):
    """
    Contributions to rock and roll proxy.
    Based on genre pioneer status and era.
    Artists from earlier eras in foundational genres score higher.
    """
    genre = artist.get("genre_primary") or ""
    first = artist.get("first_recording_year") or 2000

    # Genre weight: foundational genres score higher
    genre_weights = {
        "Blues/Early": 1.0,
        "Soul/R&B": 0.9,
        "Classic Rock": 0.7,
        "Folk/Country": 0.6,
        "Heavy Metal": 0.8,  # Genre-defining contribution
        "Punk": 0.8,
        "Hip-Hop": 0.85,
        "Electronic": 0.85,
        "Disco/Dance": 0.6,
        "Pop": 0.5,
    }

    genre_w = genre_weights.get(genre, 0.5)

    # Era weight: earlier = more foundational
    if first < 1960:
        era_w = 1.0
    elif first < 1970:
        era_w = 0.85
    elif first < 1980:
        era_w = 0.7
    elif first < 1990:
        era_w = 0.55
    else:
        era_w = 0.4

    return min(genre_w * era_w * 100, 100.0)


def compute_criteria_score(artist):
    """
    Compute the full Criteria Compliance Score (0-100).
    Weighted composite of all five criteria proxies.
    """
    excellence = compute_excellence_score(artist)
    influence = compute_influence_score(artist["id"])
    career = compute_career_length_score(artist)
    catalog = compute_catalog_score(artist)
    genre_contrib = compute_genre_contribution_score(artist)

    w = CRITERIA_WEIGHTS
    composite = (
        w["excellence"] * excellence +
        w["influence"] * influence +
        w["career_length"] * career +
        w["catalog_depth"] * catalog +
        w["genre_contribution"] * genre_contrib
    )

    return {
        "composite": round(composite, 2),
        "excellence": round(excellence, 2),
        "influence": round(influence, 2),
        "career_length": round(career, 2),
        "catalog_depth": round(catalog, 2),
        "genre_contribution": round(genre_contrib, 2),
    }


def score_all_artists():
    """Compute and store criteria scores for all artists."""
    artists = query("SELECT * FROM artists ORDER BY name")
    conn = get_connection()
    c = conn.cursor()

    scored = 0
    for artist in artists:
        scores = compute_criteria_score(artist)

        c.execute("""
            UPDATE artists SET
                criteria_score = ?,
                excellence_score = ?,
                influence_score = ?,
                career_length_score = ?,
                catalog_depth_score = ?,
                genre_contribution_score = ?
            WHERE id = ?
        """, (
            scores["composite"],
            scores["excellence"],
            scores["influence"],
            scores["career_length"],
            scores["catalog_depth"],
            scores["genre_contribution"],
            artist["id"],
        ))
        scored += 1

    conn.commit()
    conn.close()
    return scored


def compute_violation_index():
    """
    Compute the Criteria Violation Index.
    For each eligible non-inducted artist, measure the gap between
    their criteria score and the average score of inducted artists.
    """
    inducted_scores = query("""
        SELECT criteria_score FROM artists
        WHERE is_inducted = 1 AND criteria_score IS NOT NULL
    """)
    inducted_avg = np.mean([r["criteria_score"] for r in inducted_scores])
    inducted_median = np.median([r["criteria_score"] for r in inducted_scores])

    violations = query("""
        SELECT name, criteria_score, genre_primary, eligible_year,
               (? - eligible_year) as wait_years
        FROM artists
        WHERE is_eligible = 1 AND criteria_score IS NOT NULL
        ORDER BY criteria_score DESC
    """, (CURRENT_YEAR,))

    results = []
    for v in violations:
        gap = v["criteria_score"] - inducted_median
        results.append({
            "name": v["name"],
            "criteria_score": v["criteria_score"],
            "genre": v["genre_primary"],
            "eligible_year": v["eligible_year"],
            "wait_years": v["wait_years"],
            "gap_vs_inducted_median": round(gap, 2),
            "above_inducted_median": bool(gap > 0),
        })

    return results, inducted_avg, inducted_median


def export_results(violations, inducted_avg, inducted_median):
    """Export criteria scores to chapter data files."""
    # Chapter 00 -- Opening (Criteria Violation Index)
    output_dir = os.path.join(CHAPTERS_DIR, "00-opening")
    os.makedirs(output_dir, exist_ok=True)

    # Top violators -- artists with highest criteria scores who are not inducted
    top_violations = [v for v in violations if v["above_inducted_median"]]

    data = {
        "violation_index": violations[:50],  # Top 50
        "inducted_average_score": round(inducted_avg, 2),
        "inducted_median_score": round(inducted_median, 2),
        "total_eligible": len(violations),
        "above_inducted_median": len(top_violations),
        "weights": CRITERIA_WEIGHTS,
        "metadata": {
            "source": "Criteria Compliance Model v1 (pipeline/src/models/criteria_compliance.py)",
            "method": "Weighted composite of 5 criteria proxies. See CLAUDE.md for weight documentation.",
            "note": "This model is a CONSTRUCT. The weights are documented, not derived. "
                    "Sensitivity analysis should be performed before publication.",
        }
    }

    js_path = os.path.join(output_dir, "criteria-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 00: The Criteria\n")
        f.write("// Criteria Compliance Model output -- generated by pipeline\n")
        f.write(f"// {len(violations)} eligible artists scored\n\n")
        f.write("window.CRITERIA_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported to {js_path}")

    # Also update the Docket data with real criteria scores
    docket_dir = os.path.join(CHAPTERS_DIR, "05-the-docket")
    docket_artists = []
    for v in violations:
        # Compute verdict from score percentiles
        inducted_scores = [r["criteria_score"] for r in
                           query("SELECT criteria_score FROM artists WHERE is_inducted=1 AND criteria_score IS NOT NULL")]
        p25 = np.percentile(inducted_scores, 25)
        p50 = np.percentile(inducted_scores, 50)
        p75 = np.percentile(inducted_scores, 75)

        if v["criteria_score"] >= p75:
            verdict = "STRONG_CASE"
        elif v["criteria_score"] >= p50:
            verdict = "CASE"
        elif v["criteria_score"] >= p25:
            verdict = "BORDERLINE"
        else:
            verdict = "INSUFFICIENT"

        docket_artists.append({
            "name": v["name"],
            "genre": v["genre"],
            "eligible_year": v["eligible_year"],
            "wait_years": v["wait_years"],
            "criteria_score": v["criteria_score"],
            "verdict": verdict,
        })

    from config import GENRE_COLORS
    docket_data = {
        "artists": docket_artists,
        "genre_colors": GENRE_COLORS,
        "current_year": CURRENT_YEAR,
        "total_eligible": len(docket_artists),
        "inducted_median_score": round(inducted_median, 2),
        "percentiles": {
            "p25": round(float(p25), 2),
            "p50": round(float(p50), 2),
            "p75": round(float(p75), 2),
        },
        "metadata": {
            "source": "Criteria Compliance Model v1",
            "verdict_method": "Based on criteria score percentiles relative to inducted artists",
        }
    }

    docket_js = os.path.join(docket_dir, "docket-data.js")
    with open(docket_js, "w") as f:
        f.write("// One Long Impersonation -- Chapter 05: The Docket\n")
        f.write("// Full docket with criteria scores -- generated by pipeline\n")
        f.write(f"// {len(docket_artists)} eligible artists\n\n")
        f.write("window.DOCKET_DATA = ")
        json.dump(docket_data, f, indent=2)
        f.write(";\n")

    print(f"Updated Docket: {docket_js}")

    return data


def run():
    """Run the full Criteria Compliance Model."""
    print("Scoring all artists...")
    scored = score_all_artists()
    print(f"  Scored {scored} artists")

    print("\nComputing Criteria Violation Index...")
    violations, inducted_avg, inducted_median = compute_violation_index()

    print(f"\n{'='*60}")
    print("CRITERIA COMPLIANCE MODEL RESULTS")
    print(f"{'='*60}")
    print(f"Inducted average score: {inducted_avg:.2f}")
    print(f"Inducted median score: {inducted_median:.2f}")
    print(f"Eligible artists scored: {len(violations)}")
    print(f"Eligible above inducted median: {len([v for v in violations if v['above_inducted_median']])}")

    print(f"\nTop 15 eligible artists by Criteria Score (STRONG CASE):")
    for v in violations[:15]:
        gap_str = f"+{v['gap_vs_inducted_median']:.1f}" if v['above_inducted_median'] else f"{v['gap_vs_inducted_median']:.1f}"
        print(f"  {v['criteria_score']:>6.2f}  {v['name']:<30} {v['genre']:<16} {v['wait_years']}y waiting  ({gap_str} vs median)")

    print(f"\nScore distribution of inducted artists:")
    inducted = query("SELECT criteria_score FROM artists WHERE is_inducted=1 AND criteria_score IS NOT NULL")
    scores = [r["criteria_score"] for r in inducted]
    print(f"  Min: {min(scores):.2f}")
    print(f"  25th: {np.percentile(scores, 25):.2f}")
    print(f"  Median: {np.median(scores):.2f}")
    print(f"  75th: {np.percentile(scores, 75):.2f}")
    print(f"  Max: {max(scores):.2f}")

    print("\nExporting results...")
    export_results(violations, inducted_avg, inducted_median)

    return violations


if __name__ == "__main__":
    run()
