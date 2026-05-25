"""
One Long Impersonation -- Load Curated Influence Pairs
Loads hand-verified teacher-student pairs from YAML into the database.
"""

import sys
import os
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import CURATED_DATA_DIR


def find_artist_id(name, conn):
    """Find artist ID by name. Returns None if not found."""
    row = conn.execute(
        "SELECT id FROM artists WHERE name = ? LIMIT 1",
        (name,)
    ).fetchone()
    return row[0] if row else None


def load_curated_pairs():
    """Load influence pairs from curated YAML file."""
    yaml_path = os.path.join(CURATED_DATA_DIR, "influence_pairs.yaml")

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    pairs = data.get("pairs", [])
    conn = get_connection()
    c = conn.cursor()

    loaded = 0
    skipped = 0
    missing = []

    for pair in pairs:
        teacher_name = pair["teacher"]
        student_name = pair["student"]

        teacher_id = find_artist_id(teacher_name, conn)
        student_id = find_artist_id(student_name, conn)

        if not teacher_id:
            # Teacher might not be in DB yet (not inducted)
            # Insert as eligible, non-inducted artist
            first_year = None  # Unknown for non-inducted
            c.execute("""
                INSERT OR IGNORE INTO artists (name, race_source)
                VALUES (?, 'unknown')
            """, (teacher_name,))
            conn.commit()
            teacher_id = find_artist_id(teacher_name, conn)
            if not teacher_id:
                missing.append(f"  Teacher not found: {teacher_name}")
                skipped += 1
                continue

        if not student_id:
            missing.append(f"  Student not found: {student_name}")
            skipped += 1
            continue

        c.execute("""
            INSERT OR IGNORE INTO influence_pairs
            (teacher_id, student_id, source_type, source_citation, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (
            teacher_id,
            student_id,
            pair.get("source_type", "curated"),
            pair.get("citation", ""),
            pair.get("confidence", "documented"),
        ))
        loaded += 1

    conn.commit()
    conn.close()

    print(f"Loaded {loaded} curated influence pairs, skipped {skipped}")
    if missing:
        print("Missing artists:")
        for m in missing:
            print(m)

    return loaded


if __name__ == "__main__":
    count = load_curated_pairs()

    # Show the pairs
    pairs = query("""
        SELECT t.name as teacher, s.name as student,
               ip.source_type, ip.confidence
        FROM influence_pairs ip
        JOIN artists t ON ip.teacher_id = t.id
        JOIN artists s ON ip.student_id = s.id
        ORDER BY t.name, s.name
    """)

    print(f"\n{len(pairs)} influence pairs in database:")
    for p in pairs:
        print(f"  {p['teacher']} -> {p['student']} [{p['source_type']}, {p['confidence']}]")
