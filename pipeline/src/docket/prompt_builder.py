"""
One Long Impersonation -- Docket Prompt Builder
Constructs structured prompts for Claude API verdict generation.

Each artist's brief is generated from their documented data record,
NOT from the model's training data. The prompt contains ONLY facts
from the pipeline database. The model applies the Hall's criteria
to the facts provided.

Verdict classification is computed from criteria score thresholds,
not from Claude's judgment:
- STRONG CASE: score > 75th percentile of inducted artists
- CASE: score > 50th percentile
- BORDERLINE: score > 25th percentile
- INSUFFICIENT: below 25th percentile
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query


SYSTEM_PROMPT = """You are a legal clerk preparing case briefs for a data journalism platform
called One Long Impersonation, which examines Rock and Roll Hall of Fame induction patterns.

Your task: apply the Rock and Roll Hall of Fame's five stated induction criteria to the
documented facts provided about an artist. Structure your response as a legal brief.

RULES:
1. Cite ONLY the facts provided in the data record. Do not add facts from your training data.
2. If the data record is missing information for a criterion, state "Insufficient data in record."
3. Do not speculate about the Hall's motivations or intentions.
4. Do not assert that the artist "should" be inducted. Present the evidence.
5. Use the confidence vocabulary: Documented, Verified, Reported, Estimated, Modeled.
6. Never use em dashes. Use commas, colons, or restructure."""

BRIEF_TEMPLATE = """Generate a structured legal brief for the following artist's case
for Rock and Roll Hall of Fame induction.

ARTIST DATA RECORD:
{data_record}

THE HALL'S FIVE STATED CRITERIA:
1. Musical excellence
2. Influence on other performers
3. Length of career
4. Depth of catalog
5. Contributions to rock and roll

REQUIRED STRUCTURE:

## Findings of Fact
[Summarize the documented career facts from the data record above. Only cite facts provided.]

## Application of Criteria
[Apply each of the five criteria to the documented facts. For each criterion, state what
the evidence shows and what evidence is missing.]

## The Gap
[State the difference between this artist's documented qualifications and the average
qualifications of inducted artists in their era and genre. Use the criteria score provided.]

## The Verdict
[State the verdict classification provided: {verdict}. Explain what the evidence supports.
End with a single sentence summary of the case.]

Note: This verdict is computed from the artist's Criteria Compliance Score relative to
inducted artists, not from your judgment. The classification is: {verdict} (confidence: {confidence})."""


def build_data_record(artist):
    """Build a structured data record string from an artist's database entry."""
    lines = [
        f"Name: {artist['name']}",
        f"Genre: {artist['genre_primary'] or 'Not classified'}",
        f"First commercial recording: {artist['first_recording_year'] or 'Unknown'}",
        f"Eligible for induction since: {artist['eligible_year'] or 'Unknown'}",
        f"Years since eligibility: {2026 - artist['eligible_year'] if artist['eligible_year'] else 'Unknown'}",
    ]

    if artist.get("studio_album_count"):
        lines.append(f"Studio albums: {artist['studio_album_count']}")
    if artist.get("riaa_certified_units"):
        lines.append(f"RIAA certified units: {artist['riaa_certified_units']:,}")

    # RS Attention Score
    rs = artist.get("rs_attention_score", 0)
    lines.append(f"Rolling Stone Attention Score: {rs or 0}")

    # Influence relationships
    teacher_pairs = query("""
        SELECT s.name as student_name
        FROM influence_pairs ip
        JOIN artists s ON ip.student_id = s.id
        WHERE ip.teacher_id = ?
    """, (artist["id"],))

    student_pairs = query("""
        SELECT t.name as teacher_name
        FROM influence_pairs ip
        JOIN artists t ON ip.teacher_id = t.id
        WHERE ip.student_id = ?
    """, (artist["id"],))

    if teacher_pairs:
        lines.append(f"Documented influence on: {', '.join(p['student_name'] for p in teacher_pairs)}")
    if student_pairs:
        lines.append(f"Documented influences from: {', '.join(p['teacher_name'] for p in student_pairs)}")

    # Nomination history
    noms = query(
        "SELECT year FROM nominations WHERE artist_id = ? ORDER BY year",
        (artist["id"],)
    )
    if noms:
        lines.append(f"Nomination years: {', '.join(str(n['year']) for n in noms)}")
    else:
        lines.append("Nomination history: No documented nominations")

    return "\n".join(lines)


def classify_verdict(criteria_score, inducted_scores):
    """Classify verdict based on criteria score percentiles."""
    if not criteria_score or not inducted_scores:
        return "INSUFFICIENT", 0.0

    import numpy as np
    p25 = np.percentile(inducted_scores, 25)
    p50 = np.percentile(inducted_scores, 50)
    p75 = np.percentile(inducted_scores, 75)

    if criteria_score >= p75:
        return "STRONG_CASE", 0.9
    elif criteria_score >= p50:
        return "CASE", 0.7
    elif criteria_score >= p25:
        return "BORDERLINE", 0.5
    else:
        return "INSUFFICIENT", 0.3


def build_prompt(artist, verdict, confidence):
    """Build the full prompt for Claude API."""
    data_record = build_data_record(artist)

    return BRIEF_TEMPLATE.format(
        data_record=data_record,
        verdict=verdict,
        confidence=f"{confidence:.0%}",
    )


if __name__ == "__main__":
    # Test with a sample artist
    from db import init_db
    test = query("SELECT * FROM artists WHERE name = 'Big Mama Thornton' LIMIT 1")
    if test:
        record = build_data_record(test[0])
        print("=== Sample Data Record ===")
        print(record)
        print("\n=== Sample Prompt ===")
        print(build_prompt(test[0], "STRONG_CASE", 0.9)[:500])
