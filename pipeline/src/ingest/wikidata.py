"""
One Long Impersonation -- Wikidata Demographics Ingest
Semi-automated extraction of race/gender/nationality via SPARQL.

Source: Wikidata (CC0)
Method: Match artists by name, extract P172 (ethnic group), P21 (sex/gender),
        P27 (citizenship). Manual review pass required afterward.

Known limitations:
- P172 (ethnic group) coverage is ~40-60% for musicians
- Some artists have no Wikidata entry at all
- Group demographics require looking at individual members
- Race is complex; we document methodology transparently
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import WIKIDATA_ENDPOINT, WIKIDATA_USER_AGENT

try:
    from SPARQLWrapper import SPARQLWrapper, JSON as SPARQL_JSON
except ImportError:
    print("SPARQLWrapper not installed. Run: pip install SPARQLWrapper")
    sys.exit(1)


# Wikidata property IDs
P_ETHNIC_GROUP = "P172"
P_SEX_GENDER = "P21"
P_COUNTRY_CITIZENSHIP = "P27"
P_MUSICBRAINZ_ARTIST_ID = "P434"

# Map Wikidata ethnic group QIDs to our race taxonomy
ETHNIC_GROUP_MAP = {
    "Q49085": "Black",           # African Americans
    "Q190168": "Black",          # African-American culture (sometimes used)
    "Q170984": "Latino",         # Hispanic and Latino Americans
    "Q160016": "Asian",          # Asian Americans
    "Q539051": "white",          # European Americans
    "Q127885": "white",          # White Americans
    "Q678551": "multiracial",    # Multiracial Americans
    "Q1075293": "Black",         # Afro-Caribbean
    "Q988343": "Black",          # Black British
    "Q2325516": "Black",         # African diaspora
}

# Map Wikidata gender QIDs
GENDER_MAP = {
    "Q6581097": "male",
    "Q6581072": "female",
    "Q1052281": "male",          # transgender male
    "Q1097630": "female",        # transgender female
    "Q48270": "non-binary",
}


def sparql_query(query_str):
    """Execute a SPARQL query against Wikidata."""
    sparql = SPARQLWrapper(WIKIDATA_ENDPOINT)
    sparql.setQuery(query_str)
    sparql.setReturnFormat(SPARQL_JSON)
    sparql.addCustomHttpHeader("User-Agent", WIKIDATA_USER_AGENT)

    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"  SPARQL error: {e}")
        return []


def search_artist(name):
    """Search Wikidata for a musician by name. Returns QID and labels."""
    # Escape quotes in name
    safe_name = name.replace('"', '\\"')

    q = f"""
    SELECT ?item ?itemLabel ?genderLabel ?ethnicGroupLabel ?ethnicGroup ?gender
    WHERE {{
      ?item rdfs:label "{safe_name}"@en .
      ?item wdt:P31/wdt:P279* wd:Q5 .  # instance of human (or subclass)

      OPTIONAL {{ ?item wdt:{P_SEX_GENDER} ?gender . }}
      OPTIONAL {{ ?item wdt:{P_ETHNIC_GROUP} ?ethnicGroup . }}

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
    }}
    LIMIT 5
    """

    return sparql_query(q)


def search_band(name):
    """Search Wikidata for a band/group by name. Returns QID and member info."""
    safe_name = name.replace('"', '\\"')

    q = f"""
    SELECT ?item ?itemLabel
    WHERE {{
      ?item rdfs:label "{safe_name}"@en .
      ?item wdt:P31/wdt:P279* wd:Q215380 .  # instance of musical group

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
    }}
    LIMIT 3
    """

    return sparql_query(q)


def get_value(binding, key):
    """Extract a value from a SPARQL binding."""
    if key in binding:
        return binding[key]["value"]
    return None


def get_qid(uri):
    """Extract QID from a Wikidata URI."""
    if uri and "wikidata.org" in uri:
        return uri.split("/")[-1]
    return None


def enrich_artist(artist_row):
    """Look up demographics for a single artist from Wikidata."""
    name = artist_row["name"]
    gender = artist_row["gender"]
    is_group = gender == "group"

    result = {
        "wikidata_id": None,
        "gender_wd": None,
        "race_wd": None,
        "race_source": None,
    }

    if is_group:
        # For groups, search as band
        bindings = search_band(name)
        if bindings:
            qid = get_qid(get_value(bindings[0], "item"))
            result["wikidata_id"] = qid
        # Group demographics come from curated data, not Wikidata
        return result

    # Search as individual
    bindings = search_artist(name)
    if not bindings:
        return result

    # Take first human result
    for b in bindings:
        qid = get_qid(get_value(b, "item"))
        result["wikidata_id"] = qid

        # Gender
        gender_qid = get_qid(get_value(b, "gender"))
        if gender_qid and gender_qid in GENDER_MAP:
            result["gender_wd"] = GENDER_MAP[gender_qid]

        # Ethnic group
        ethnic_qid = get_qid(get_value(b, "ethnicGroup"))
        if ethnic_qid and ethnic_qid in ETHNIC_GROUP_MAP:
            result["race_wd"] = ETHNIC_GROUP_MAP[ethnic_qid]
            result["race_source"] = "wikidata"

        if result["race_wd"]:
            break

    return result


def run_enrichment(limit=None, dry_run=False):
    """
    Enrich all artists in the database with Wikidata demographics.
    Only updates artists where race_source is 'curated' (from Rock Hall ingestion).
    Does NOT overwrite manually reviewed demographics.
    """
    artists = query("""
        SELECT id, name, gender, race, race_source
        FROM artists
        WHERE gender != 'group'
        ORDER BY name
    """)

    if limit:
        artists = artists[:limit]

    print(f"Enriching {len(artists)} solo artists from Wikidata...")
    enriched = 0
    found_race = 0
    found_wikidata = 0

    for i, artist in enumerate(artists):
        if i > 0 and i % 10 == 0:
            print(f"  Processed {i}/{len(artists)}...")

        result = enrich_artist(artist)
        time.sleep(1.5)  # Rate limit: be polite to Wikidata

        if result["wikidata_id"]:
            found_wikidata += 1

        if result["race_wd"]:
            found_race += 1

        if dry_run:
            if result["wikidata_id"] or result["race_wd"]:
                print(f"  {artist['name']}: QID={result['wikidata_id']}, "
                      f"race_wd={result['race_wd']}, gender_wd={result['gender_wd']}")
            continue

        # Update database
        conn = get_connection()
        c = conn.cursor()

        updates = []
        params = []

        if result["wikidata_id"]:
            updates.append("wikidata_id = ?")
            params.append(result["wikidata_id"])

        # Only update race if Wikidata has data AND current source is 'curated'
        # (don't overwrite manual reviews)
        if result["race_wd"] and artist["race_source"] == "curated":
            # Verify against existing race -- flag conflicts
            if artist["race"] and artist["race"] != result["race_wd"]:
                print(f"  CONFLICT: {artist['name']} -- "
                      f"curated={artist['race']}, wikidata={result['race_wd']}")
                updates.append("race_notes = ?")
                params.append(f"Wikidata says {result['race_wd']}, curated says {artist['race']}")
            else:
                updates.append("race_source = 'wikidata'")

        if updates:
            sql = f"UPDATE artists SET {', '.join(updates)} WHERE id = ?"
            params.append(artist["id"])
            c.execute(sql, params)
            enriched += 1

        conn.commit()
        conn.close()

    print(f"\nResults:")
    print(f"  Artists processed: {len(artists)}")
    print(f"  Wikidata entries found: {found_wikidata}")
    print(f"  Race data from Wikidata: {found_race}")
    print(f"  Database records updated: {enriched}")

    return enriched


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Enrich artist demographics from Wikidata")
    parser.add_argument("--limit", type=int, help="Process only N artists")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing")
    args = parser.parse_args()

    run_enrichment(limit=args.limit, dry_run=args.dry_run)
