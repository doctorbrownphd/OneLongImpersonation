"""
One Long Impersonation -- MusicBrainz Bulk Ingest
Fetches artist relationships (influence links), release groups (catalog depth),
and genre tags from MusicBrainz for all artists in the database.

Source: MusicBrainz (CC0)
API: musicbrainzngs library, rate-limited to 1 req/sec
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import (
    MUSICBRAINZ_APP_NAME, MUSICBRAINZ_APP_VERSION,
    MUSICBRAINZ_CONTACT, MUSICBRAINZ_RATE_LIMIT
)

try:
    import musicbrainzngs as mb
except ImportError:
    print("musicbrainzngs not installed. Run: pip install musicbrainzngs")
    sys.exit(1)

mb.set_useragent(MUSICBRAINZ_APP_NAME, MUSICBRAINZ_APP_VERSION, MUSICBRAINZ_CONTACT)


def search_artist(name):
    """Search MusicBrainz for an artist by name. Returns best match MBID."""
    try:
        result = mb.search_artists(artist=name, limit=5)
        artists = result.get("artist-list", [])
        if not artists:
            return None

        # Try exact match first
        for a in artists:
            if a.get("name", "").lower() == name.lower():
                return a["id"]

        # Fall back to first result if score is high
        if artists and int(artists[0].get("ext:score", 0)) >= 90:
            return artists[0]["id"]

        return None
    except Exception as e:
        print(f"  Search error for '{name}': {e}")
        return None


def get_artist_relations(mbid):
    """Get influence relationships for an artist from MusicBrainz."""
    try:
        result = mb.get_artist_by_id(mbid, includes=["artist-rels"])
        relations = result.get("artist", {}).get("artist-relation-list", [])

        influences = []
        for rel in relations:
            rel_type = rel.get("type", "")
            target = rel.get("artist", {})
            target_name = target.get("name", "")
            target_id = target.get("id", "")
            direction = rel.get("direction", "")

            # We want "influenced by" relationships
            # In MB: type="influenced by", direction="backward" means this artist influenced the target
            #         type="influenced by", direction="forward" means the target influenced this artist
            if rel_type in ("influenced by", "influenced"):
                influences.append({
                    "target_name": target_name,
                    "target_mbid": target_id,
                    "type": rel_type,
                    "direction": direction,
                })

        return influences
    except Exception as e:
        print(f"  Relations error for {mbid}: {e}")
        return []


def get_artist_releases(mbid):
    """Get release group count (studio albums) for an artist."""
    try:
        result = mb.browse_release_groups(artist=mbid, release_type=["album"], limit=100)
        count = result.get("release-group-count", 0)
        return count
    except Exception as e:
        print(f"  Release error for {mbid}: {e}")
        return 0


def get_artist_tags(mbid):
    """Get genre tags for an artist from MusicBrainz."""
    try:
        result = mb.get_artist_by_id(mbid, includes=["tags"])
        tags = result.get("artist", {}).get("tag-list", [])
        # Sort by count descending
        tags.sort(key=lambda t: int(t.get("count", 0)), reverse=True)
        return [t.get("name", "") for t in tags[:10]]
    except Exception as e:
        print(f"  Tags error for {mbid}: {e}")
        return []


def resolve_mbids():
    """Find MusicBrainz IDs for all artists in the database."""
    artists = query("""
        SELECT id, name, musicbrainz_id
        FROM artists
        WHERE musicbrainz_id IS NULL
        ORDER BY name
    """)

    print(f"Resolving MBIDs for {len(artists)} artists...")
    conn = get_connection()
    found = 0

    for i, artist in enumerate(artists):
        if i > 0 and i % 20 == 0:
            print(f"  {i}/{len(artists)} processed, {found} found...")

        mbid = search_artist(artist["name"])
        time.sleep(MUSICBRAINZ_RATE_LIMIT)

        if mbid:
            conn.execute(
                "UPDATE artists SET musicbrainz_id = ? WHERE id = ?",
                (mbid, artist["id"])
            )
            found += 1

    conn.commit()
    conn.close()
    print(f"Resolved {found}/{len(artists)} MBIDs")
    return found


def fetch_influence_relations():
    """Fetch influence relationships for all artists with MBIDs."""
    artists = query("""
        SELECT id, name, musicbrainz_id
        FROM artists
        WHERE musicbrainz_id IS NOT NULL
        ORDER BY name
    """)

    print(f"\nFetching influence relations for {len(artists)} artists...")
    conn = get_connection()
    c = conn.cursor()
    total_new = 0

    # Build name-to-id lookup for matching
    all_artists = query("SELECT id, name FROM artists")
    name_lookup = {a["name"].lower(): a["id"] for a in all_artists}

    for i, artist in enumerate(artists):
        if i > 0 and i % 20 == 0:
            print(f"  {i}/{len(artists)} processed, {total_new} new pairs...")

        relations = get_artist_relations(artist["musicbrainz_id"])
        time.sleep(MUSICBRAINZ_RATE_LIMIT)

        for rel in relations:
            target_name = rel["target_name"]
            target_id_in_db = name_lookup.get(target_name.lower())

            if not target_id_in_db:
                continue  # Target artist not in our database

            # Determine teacher/student
            if rel["direction"] == "forward":
                # "influenced by" forward = target influenced this artist
                teacher_id = target_id_in_db
                student_id = artist["id"]
            else:
                # "influenced by" backward = this artist influenced target
                teacher_id = artist["id"]
                student_id = target_id_in_db

            # Skip self-references
            if teacher_id == student_id:
                continue

            try:
                c.execute("""
                    INSERT OR IGNORE INTO influence_pairs
                    (teacher_id, student_id, source_type, source_citation, confidence)
                    VALUES (?, ?, 'musicbrainz', ?, 'documented')
                """, (teacher_id, student_id,
                      f"MusicBrainz artist relationship: {rel['type']} ({rel['direction']})"))
                if c.rowcount > 0:
                    total_new += 1
            except Exception:
                pass

    conn.commit()
    conn.close()
    print(f"Added {total_new} new influence pairs from MusicBrainz")
    return total_new


def fetch_catalog_data():
    """Fetch studio album counts for all artists with MBIDs."""
    artists = query("""
        SELECT id, name, musicbrainz_id
        FROM artists
        WHERE musicbrainz_id IS NOT NULL
          AND studio_album_count IS NULL
        ORDER BY name
    """)

    print(f"\nFetching catalog data for {len(artists)} artists...")
    conn = get_connection()
    updated = 0

    for i, artist in enumerate(artists):
        if i > 0 and i % 20 == 0:
            print(f"  {i}/{len(artists)} processed...")

        count = get_artist_releases(artist["musicbrainz_id"])
        time.sleep(MUSICBRAINZ_RATE_LIMIT)

        if count > 0:
            conn.execute(
                "UPDATE artists SET studio_album_count = ? WHERE id = ?",
                (count, artist["id"])
            )
            updated += 1

    conn.commit()
    conn.close()
    print(f"Updated catalog data for {updated} artists")
    return updated


def run(skip_mbid_resolve=False, skip_relations=False, skip_catalog=False):
    """Run the full MusicBrainz ingestion pipeline."""

    if not skip_mbid_resolve:
        resolve_mbids()

    if not skip_relations:
        fetch_influence_relations()

    if not skip_catalog:
        fetch_catalog_data()

    # Summary
    stats = query("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN musicbrainz_id IS NOT NULL THEN 1 ELSE 0 END) as with_mbid,
            SUM(CASE WHEN studio_album_count IS NOT NULL THEN 1 ELSE 0 END) as with_catalog
        FROM artists
    """)[0]

    pairs = query("SELECT COUNT(*) as n FROM influence_pairs")[0]["n"]
    mb_pairs = query("SELECT COUNT(*) as n FROM influence_pairs WHERE source_type = 'musicbrainz'")[0]["n"]

    print(f"\n{'='*60}")
    print("MUSICBRAINZ INGEST SUMMARY")
    print(f"{'='*60}")
    print(f"Artists with MBID: {stats['with_mbid']}/{stats['total']}")
    print(f"Artists with catalog data: {stats['with_catalog']}/{stats['total']}")
    print(f"Total influence pairs: {pairs} ({mb_pairs} from MusicBrainz)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-mbid", action="store_true", help="Skip MBID resolution")
    parser.add_argument("--skip-relations", action="store_true", help="Skip influence relations")
    parser.add_argument("--skip-catalog", action="store_true", help="Skip catalog data")
    parser.add_argument("--limit", type=int, help="Process only N artists")
    args = parser.parse_args()

    run(
        skip_mbid_resolve=args.skip_mbid,
        skip_relations=args.skip_relations,
        skip_catalog=args.skip_catalog,
    )
