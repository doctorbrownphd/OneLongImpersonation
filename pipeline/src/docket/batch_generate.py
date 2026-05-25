"""
One Long Impersonation -- Docket Brief Batch Generator
Generates structured legal briefs for eligible non-inducted artists
using the Claude API.

Each brief is generated from the artist's pipeline data record ONLY.
The prompt contains documented facts, not open-ended generation.

Verdict classification is computed from criteria score percentiles,
not from Claude's judgment.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CHAPTERS_DIR, CURRENT_YEAR
from docket.prompt_builder import build_prompt, build_data_record, classify_verdict, SYSTEM_PROMPT

try:
    import anthropic
    import numpy as np
except ImportError:
    print("Required: pip install anthropic numpy")
    sys.exit(1)


def get_inducted_score_distribution():
    """Get criteria score distribution of inducted artists for verdict classification."""
    scores = query("""
        SELECT criteria_score FROM artists
        WHERE is_inducted = 1 AND criteria_score IS NOT NULL
    """)
    return [r["criteria_score"] for r in scores]


def generate_brief(client, artist, inducted_scores):
    """Generate a single artist brief via Claude API."""
    verdict, confidence = classify_verdict(
        artist.get("criteria_score"), inducted_scores
    )

    prompt = build_prompt(artist, verdict, confidence)

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        brief_text = response.content[0].text

        return {
            "artist_name": artist["name"],
            "artist_id": artist["id"],
            "verdict": verdict,
            "confidence": confidence,
            "criteria_score": artist.get("criteria_score"),
            "brief_text": brief_text,
            "model_version": CLAUDE_MODEL,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "human_reviewed": False,
            "data_record": build_data_record(artist),
        }
    except Exception as e:
        print(f"  ERROR generating brief for {artist['name']}: {e}")
        return None


def store_brief(brief, db_path=None):
    """Store a generated brief in the database and as a JSON file."""
    if not brief:
        return

    conn = get_connection(db_path)
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO docket_verdicts
        (artist_id, verdict, confidence, brief_json, generated_at,
         model_version, human_reviewed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        brief["artist_id"],
        brief["verdict"],
        brief["confidence"],
        json.dumps(brief),
        brief["generated_at"],
        brief["model_version"],
        0,
    ))

    conn.commit()
    conn.close()

    # Also save as individual JSON file
    briefs_dir = os.path.join(CHAPTERS_DIR, "05-the-docket", "briefs")
    os.makedirs(briefs_dir, exist_ok=True)

    slug = brief["artist_name"].lower().replace(" ", "-").replace("'", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    filepath = os.path.join(briefs_dir, f"{slug}.json")

    with open(filepath, "w") as f:
        json.dump(brief, f, indent=2)

    return filepath


def run(limit=None, top_only=False):
    """Generate briefs for eligible non-inducted artists."""

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set. Set it to generate briefs.")
        print("Export: export ANTHROPIC_API_KEY=your-key-here")
        print("\nGenerating sample brief structure instead...")
        generate_sample()
        return

    client = anthropic.Anthropic(api_key=api_key)
    inducted_scores = get_inducted_score_distribution()

    # Get eligible artists sorted by criteria score (highest first)
    if top_only:
        artists = query("""
            SELECT * FROM artists
            WHERE is_eligible = 1 AND criteria_score IS NOT NULL
            ORDER BY criteria_score DESC
            LIMIT 10
        """)
    else:
        artists = query("""
            SELECT * FROM artists
            WHERE is_eligible = 1 AND criteria_score IS NOT NULL
            ORDER BY criteria_score DESC
        """)

    if limit:
        artists = artists[:limit]

    print(f"Generating briefs for {len(artists)} artists...")
    generated = 0

    for i, artist in enumerate(artists):
        print(f"  [{i+1}/{len(artists)}] {artist['name']} (score: {artist.get('criteria_score', 'N/A')})...")

        brief = generate_brief(client, artist, inducted_scores)
        if brief:
            filepath = store_brief(brief)
            generated += 1
            print(f"    -> {brief['verdict']} (confidence: {brief['confidence']:.0%})")
            if filepath:
                print(f"    -> Saved: {filepath}")

        # Rate limit
        time.sleep(1)

    print(f"\nGenerated {generated}/{len(artists)} briefs")
    return generated


def generate_sample():
    """Generate a sample brief structure without calling the API."""
    inducted_scores = get_inducted_score_distribution()

    # Get top 5 eligible artists
    artists = query("""
        SELECT * FROM artists
        WHERE is_eligible = 1 AND criteria_score IS NOT NULL
        ORDER BY criteria_score DESC
        LIMIT 5
    """)

    print(f"\nSample briefs (structure only, no API call):")
    for artist in artists:
        verdict, confidence = classify_verdict(
            artist.get("criteria_score"), inducted_scores
        )
        record = build_data_record(artist)

        print(f"\n{'='*60}")
        print(f"ARTIST: {artist['name']}")
        print(f"VERDICT: {verdict} (confidence: {confidence:.0%})")
        print(f"CRITERIA SCORE: {artist.get('criteria_score', 'N/A')}")
        print(f"DATA RECORD:\n{record}")

        # Save sample structure
        sample = {
            "artist_name": artist["name"],
            "artist_id": artist["id"],
            "verdict": verdict,
            "confidence": confidence,
            "criteria_score": artist.get("criteria_score"),
            "brief_text": "[Brief would be generated by Claude API]",
            "model_version": CLAUDE_MODEL,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "human_reviewed": False,
            "data_record": record,
        }
        store_brief(sample)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="Generate only N briefs")
    parser.add_argument("--top-only", action="store_true", help="Top 10 by criteria score only")
    args = parser.parse_args()

    run(limit=args.limit, top_only=args.top_only)
