"""
One Long Impersonation -- Export Pipeline
Generates chapter data.js files from SQLite database.
This script generates the Docket data file for Chapter 05.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query
from config import CURRENT_YEAR, CHAPTERS_DIR, GENRE_COLORS

# Notable eligible non-inducted artists
# In the full pipeline, this would be computed from the complete eligible population.
# For now, this is curated from public nomination records and the spec.
NOTABLE_ELIGIBLE = [
    # Heavy Metal / Hard Rock
    {"name": "Motorhead", "genre": "Heavy Metal", "eligible_year": 2002, "note": "Musical Excellence 2020. Never Performer."},
    {"name": "Thin Lizzy", "genre": "Heavy Metal", "eligible_year": 1996, "note": "Phil Lynott died 1986. Never nominated."},
    {"name": "Soundgarden", "genre": "Heavy Metal", "eligible_year": 2016, "note": "Chris Cornell died 2017. Multiple nominations."},
    {"name": "Tool", "genre": "Heavy Metal", "eligible_year": 2018, "note": "Tops fan votes. Not inducted."},
    {"name": "System of a Down", "genre": "Heavy Metal", "eligible_year": 2023, "note": "Recently eligible."},
    {"name": "Pantera", "genre": "Heavy Metal", "eligible_year": 2008, "note": "Never nominated."},
    {"name": "Slayer", "genre": "Heavy Metal", "eligible_year": 2008, "note": "Never nominated."},
    {"name": "Iron Butterfly", "genre": "Heavy Metal", "eligible_year": 1993, "note": "Proto-metal. 33 years eligible."},
    {"name": "Megadeth", "genre": "Heavy Metal", "eligible_year": 2010, "note": "Never nominated."},

    # Punk / Post-Punk
    {"name": "Bad Brains", "genre": "Punk", "eligible_year": 2007, "note": "Black punk pioneers. Never nominated."},
    {"name": "Mission of Burma", "genre": "Punk", "eligible_year": 2006, "note": "Post-punk pioneers. Never nominated."},
    {"name": "The Replacements", "genre": "Punk", "eligible_year": 2006, "note": "Never nominated."},
    {"name": "Husker Du", "genre": "Punk", "eligible_year": 2009, "note": "Never nominated."},
    {"name": "Minor Threat", "genre": "Punk", "eligible_year": 2006, "note": "Hardcore pioneers. Never nominated."},

    # Electronic
    {"name": "Kraftwerk", "genre": "Electronic", "eligible_year": 1995, "note": "Invented electronic music. 31 years eligible."},
    {"name": "New Order", "genre": "Electronic", "eligible_year": 2008, "note": "Post-punk to electronic. Never nominated."},
    {"name": "Aphex Twin", "genre": "Electronic", "eligible_year": 2017, "note": "Most influential electronic artist. Never nominated."},
    {"name": "The Prodigy", "genre": "Electronic", "eligible_year": 2022, "note": "Keith Flint died 2019."},

    # Hip-Hop
    {"name": "OutKast", "genre": "Hip-Hop", "eligible_year": 2019, "note": "Multiple nominations."},
    {"name": "De La Soul", "genre": "Hip-Hop", "eligible_year": 2014, "note": "Never nominated. Posdnuos died 2023."},
    {"name": "Wu-Tang Clan", "genre": "Hip-Hop", "eligible_year": 2018, "note": "Never nominated."},
    {"name": "Nas", "genre": "Hip-Hop", "eligible_year": 2019, "note": "Never nominated."},

    # Soul / R&B / Funk
    {"name": "Chaka Khan", "genre": "Soul/R&B", "eligible_year": 2003, "note": "Multiple nominations. Never inducted."},
    {"name": "The Meters", "genre": "Soul/R&B", "eligible_year": 1994, "note": "Funk pioneers. Never nominated."},
    {"name": "War", "genre": "Soul/R&B", "eligible_year": 1994, "note": "Never nominated."},

    # Classic Rock / Pop
    {"name": "The Cranberries", "genre": "Classic Rock", "eligible_year": 2018, "note": "Dolores O'Riordan died 2018."},
    {"name": "Jethro Tull", "genre": "Classic Rock", "eligible_year": 1993, "note": "33 years eligible. Never nominated."},
    {"name": "The Smiths", "genre": "Classic Rock", "eligible_year": 2009, "note": "Multiple nominations."},
    {"name": "Bjork", "genre": "Electronic", "eligible_year": 2018, "note": "Never nominated."},
    {"name": "Sinead O'Connor", "genre": "Pop", "eligible_year": 2012, "note": "Died 2023. Never nominated."},

    # Blues / Early
    {"name": "Big Mama Thornton", "genre": "Blues/Early", "eligible_year": 1976, "note": "Wrote Hound Dog. Influenced Elvis, Janis Joplin. Never inducted as Performer."},
]


def generate_docket_data():
    """Generate the Docket data file for Chapter 05."""

    # Add computed fields
    for artist in NOTABLE_ELIGIBLE:
        artist["wait_years"] = CURRENT_YEAR - artist["eligible_year"]
        # Preliminary verdict (without full Criteria Compliance Model)
        wait = artist["wait_years"]
        if wait >= 25:
            artist["verdict"] = "STRONG_CASE"
        elif wait >= 15:
            artist["verdict"] = "CASE"
        elif wait >= 8:
            artist["verdict"] = "BORDERLINE"
        else:
            artist["verdict"] = "INSUFFICIENT"
        artist["criteria_score"] = None  # Will be computed when model is built

    # Sort by wait years descending
    sorted_artists = sorted(NOTABLE_ELIGIBLE, key=lambda a: a["wait_years"], reverse=True)

    data = {
        "artists": sorted_artists,
        "genre_colors": GENRE_COLORS,
        "current_year": CURRENT_YEAR,
        "total_eligible_estimate": "500-800",
        "metadata": {
            "source": "Curated from public nomination records, Future Rock Legends, and spec research",
            "note": "This is a preliminary docket of notable eligible artists. The full docket "
                    "requires the complete eligible artist population (est. 500-800 artists) "
                    "and Criteria Compliance Scores for all of them.",
            "verdict_method": "Preliminary: based on years waiting. Full: based on Criteria Compliance Score percentiles.",
            "ai_disclosure": "Full briefs will be generated by Claude API (claude-sonnet-4-20250514) "
                             "from structured prompts containing only pipeline data. Human-reviewed before publication.",
        }
    }

    output_dir = os.path.join(CHAPTERS_DIR, "05-the-docket")
    os.makedirs(output_dir, exist_ok=True)

    js_path = os.path.join(output_dir, "docket-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 05: The Docket\n")
        f.write("// Preliminary docket data -- notable eligible non-inducted artists\n")
        f.write(f"// {len(sorted_artists)} artists -- full docket will have 500-800\n\n")
        f.write("window.DOCKET_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported {len(sorted_artists)} artists to {js_path}")

    # Stats
    by_genre = {}
    by_verdict = {}
    for a in sorted_artists:
        by_genre[a["genre"]] = by_genre.get(a["genre"], 0) + 1
        by_verdict[a["verdict"]] = by_verdict.get(a["verdict"], 0) + 1

    print(f"\nBy genre: {by_genre}")
    print(f"By verdict: {by_verdict}")
    print(f"\nLongest waiting:")
    for a in sorted_artists[:10]:
        print(f"  {a['name']}: {a['wait_years']}y ({a['genre']}) -- {a['verdict']}")


if __name__ == "__main__":
    generate_docket_data()
