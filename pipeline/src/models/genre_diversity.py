"""
One Long Impersonation -- Genre Diversity Analysis
Model 4: Simpson's Diversity Index and Genre Bias Scores.

Measures genre representation among inductees by year using
Simpson's Diversity Index (1 - sum(p_i^2)), the same metric
ecologists use to measure species diversity.

Genre Bias Score = (genre share among inductees) / (genre share among eligible).
Score of 1.0 = proportional representation. < 1.0 = underrepresented.

Compares Wenner era (1986-2019) to post-Wenner era (2020-2026).
"""

import sys
import os
import json
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query
from config import CURRENT_YEAR, CHAPTERS_DIR, GENRE_TAXONOMY, GENRE_COLORS


def get_inductions_by_year():
    """Get all Performer inductions grouped by year and genre."""
    rows = query("""
        SELECT i.year, a.genre_primary as genre, COUNT(*) as n
        FROM inductions i
        JOIN artists a ON i.artist_id = a.id
        WHERE i.category = 'P'
        GROUP BY i.year, a.genre_primary
        ORDER BY i.year, a.genre_primary
    """)

    # Build matrix: year -> {genre: count}
    years = sorted(set(r["year"] for r in rows))
    matrix = {}
    for year in years:
        matrix[year] = Counter()

    for r in rows:
        genre = r["genre"] or "unknown"
        matrix[r["year"]][genre] = r["n"]

    return matrix, years


def compute_simpson_index(genre_counts):
    """
    Compute Simpson's Diversity Index for a set of genre counts.
    D = 1 - sum(p_i^2) where p_i = proportion of inductees in genre i.
    0 = no diversity (all one genre), approaching 1 = maximum diversity.
    """
    total = sum(genre_counts.values())
    if total <= 1:
        return 0.0

    d = sum((n / total) ** 2 for n in genre_counts.values())
    return round(1.0 - d, 4)


def compute_genre_bias_scores(matrix, years):
    """
    Compute Genre Bias Scores for Wenner era (1986-2019) and post-Wenner (2020+).

    Bias Score = (genre share among inductees in era) / (genre share among ALL inductees).
    This is a simplified version -- the full model would use eligible population as denominator.
    """
    wenner_years = [y for y in years if y <= 2019]
    post_wenner_years = [y for y in years if y >= 2020]

    # Aggregate counts by era
    wenner_counts = Counter()
    post_wenner_counts = Counter()
    total_counts = Counter()

    for year, counts in matrix.items():
        for genre, n in counts.items():
            total_counts[genre] += n
            if year <= 2019:
                wenner_counts[genre] += n
            else:
                post_wenner_counts[genre] += n

    total_all = sum(total_counts.values())
    total_wenner = sum(wenner_counts.values())
    total_post = sum(post_wenner_counts.values())

    bias_scores = {}
    for genre in GENRE_TAXONOMY:
        overall_share = total_counts.get(genre, 0) / total_all if total_all > 0 else 0

        wenner_share = wenner_counts.get(genre, 0) / total_wenner if total_wenner > 0 else 0
        post_share = post_wenner_counts.get(genre, 0) / total_post if total_post > 0 else 0

        # Bias score relative to overall share (1.0 = proportional)
        if overall_share > 0:
            wenner_bias = round(wenner_share / overall_share, 2)
            post_bias = round(post_share / overall_share, 2)
        else:
            wenner_bias = 0
            post_bias = 0

        bias_scores[genre] = {
            "wenner_count": wenner_counts.get(genre, 0),
            "post_wenner_count": post_wenner_counts.get(genre, 0),
            "total_count": total_counts.get(genre, 0),
            "wenner_share": round(wenner_share, 4),
            "post_wenner_share": round(post_share, 4),
            "overall_share": round(overall_share, 4),
            "wenner_bias": wenner_bias,
            "post_wenner_bias": post_bias,
            "change": round(post_bias - wenner_bias, 2),
        }

    return bias_scores


def build_timeline_data(matrix, years):
    """Build the genre timeline data for the stacked bar visualization."""
    timeline = []
    simpson_series = []

    for year in years:
        counts = matrix[year]
        row = {"year": year}
        for genre in GENRE_TAXONOMY:
            row[genre] = counts.get(genre, 0)
        timeline.append(row)

        simpson = compute_simpson_index(counts)
        simpson_series.append({"year": year, "simpson": simpson})

    return timeline, simpson_series


def compute_era_simpson(matrix, years):
    """Compute aggregate Simpson's index for each era."""
    wenner_aggregate = Counter()
    post_aggregate = Counter()

    for year, counts in matrix.items():
        target = wenner_aggregate if year <= 2019 else post_aggregate
        for genre, n in counts.items():
            target[genre] += n

    wenner_simpson = compute_simpson_index(wenner_aggregate)
    post_simpson = compute_simpson_index(post_aggregate)

    return {
        "wenner_era": {"simpson": wenner_simpson, "years": "1986-2019"},
        "post_wenner": {"simpson": post_simpson, "years": "2020-2026"},
        "improvement_ratio": round(post_simpson / wenner_simpson, 2) if wenner_simpson > 0 else None,
    }


def never_inducted_notable():
    """List notable never-inducted artists by genre."""
    # These are documented from Future Rock Legends and public nomination records
    # In a full pipeline, this would come from the eligible artist database
    notable = [
        {"name": "Motorhead", "genre": "Heavy Metal", "eligible_year": 2002,
         "note": "Lemmy died 2015. Musical Excellence 2020 (not Performer)."},
        {"name": "Thin Lizzy", "genre": "Heavy Metal", "eligible_year": 1996,
         "note": "Phil Lynott died 1986. Never nominated."},
        {"name": "Soundgarden", "genre": "Heavy Metal", "eligible_year": 2016,
         "note": "Chris Cornell died 2017. Multiple nominations, never inducted."},
        {"name": "Tool", "genre": "Heavy Metal", "eligible_year": 2018,
         "note": "Consistently tops fan votes. Not inducted."},
        {"name": "System of a Down", "genre": "Heavy Metal", "eligible_year": 2023,
         "note": "Recently eligible. Not yet nominated."},
        {"name": "Bad Brains", "genre": "Punk", "eligible_year": 2007,
         "note": "Black punk pioneers. Never nominated."},
        {"name": "Kraftwerk", "genre": "Electronic", "eligible_year": 1995,
         "note": "Invented electronic music. Never inducted."},
        {"name": "New Order", "genre": "Electronic", "eligible_year": 2008,
         "note": "Bridged post-punk and electronic. Never nominated."},
        {"name": "Aphex Twin", "genre": "Electronic", "eligible_year": 2017,
         "note": "Most influential electronic artist. Never nominated."},
        {"name": "Iron Butterfly", "genre": "Heavy Metal", "eligible_year": 1993,
         "note": "Proto-metal pioneers. Never nominated."},
    ]
    return notable


def export_results(timeline, simpson_series, bias_scores, era_simpson, notable):
    """Export genre diversity results to chapter data file."""
    output_dir = os.path.join(CHAPTERS_DIR, "03-genre")
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "genre_timeline": timeline,
        "simpson_index": simpson_series,
        "genre_bias_scores": bias_scores,
        "era_comparison": era_simpson,
        "never_inducted_notable": notable,
        "genre_colors": GENRE_COLORS,
        "genre_taxonomy": GENRE_TAXONOMY,
        "metadata": {
            "source": "Rock and Roll Hall of Fame official inductee database",
            "method": "Simpson's Diversity Index (1 - sum(p_i^2))",
            "bias_method": "Genre Bias Score = era genre share / overall genre share",
            "wenner_era": "1986-2019 (Wenner on nominating committee or as Chairman)",
            "post_wenner_era": "2020-2026 (John Sykes era)",
            "note": "Performer category only. Early Influence and Musical Excellence excluded.",
        }
    }

    js_path = os.path.join(output_dir, "genre-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 03: Genre Desertification\n")
        f.write("// Genre diversity data -- generated by pipeline\n")
        f.write("// Method: Simpson's Diversity Index + Genre Bias Scores\n\n")
        f.write("window.GENRE_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported to {js_path}")
    return js_path


def run():
    """Run the full genre diversity analysis."""
    print("Building induction matrix...")
    matrix, years = get_inductions_by_year()
    print(f"  {len(years)} years of inductions ({years[0]}-{years[-1]})")

    print("\nBuilding timeline data...")
    timeline, simpson_series = build_timeline_data(matrix, years)

    print("\nComputing Genre Bias Scores...")
    bias_scores = compute_genre_bias_scores(matrix, years)

    print("\n" + "=" * 60)
    print("GENRE BIAS SCORES")
    print("=" * 60)
    print(f"{'Genre':<18} {'Wenner':<10} {'Post-W':<10} {'Change':<10}")
    print("-" * 48)
    for genre in GENRE_TAXONOMY:
        s = bias_scores[genre]
        print(f"{genre:<18} {s['wenner_bias']:<10} {s['post_wenner_bias']:<10} {s['change']:+.2f}")

    print("\nEra-level Simpson's Diversity Index...")
    era_simpson = compute_era_simpson(matrix, years)
    print(f"  Wenner era (1986-2019): {era_simpson['wenner_era']['simpson']}")
    print(f"  Post-Wenner (2020-2026): {era_simpson['post_wenner']['simpson']}")
    print(f"  Improvement ratio: {era_simpson['improvement_ratio']}x")

    print("\nSimpson's index by year (selected):")
    for s in simpson_series:
        if s["year"] in [1986, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2023, 2026]:
            print(f"  {s['year']}: {s['simpson']}")

    notable = never_inducted_notable()

    print("\nExporting results...")
    export_results(timeline, simpson_series, bias_scores, era_simpson, notable)

    return bias_scores, era_simpson


if __name__ == "__main__":
    run()
