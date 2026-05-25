"""
One Long Impersonation -- Eligible Non-Inducted Artist Population
Builds the complete list of artists who are eligible for induction
but have not been inducted.

Eligibility rule: 25 years after first commercial recording.
An artist with a first recording in 1990 became eligible in 2015.

Sources:
- Future Rock Legends (futurerockhall.com) -- community-maintained
  comprehensive nomination tracking database
- Wikipedia "Rock and Roll Hall of Fame" article -- lists notable
  nominees who were not inducted
- Published reporting on nominees (Billboard, Rolling Stone)

This is the most labor-intensive data task. The full population
is estimated at 500-800 artists. We build it in stages:
1. Artists documented as nominees (from Future Rock Legends)
2. Notable eligible artists from the spec and public discourse
3. Expansion via MusicBrainz genre/era queries

For the initial build, we use a curated list of ~200 notable
eligible artists covering the most important prosecution cases.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query
from config import CURRENT_YEAR, ELIGIBILITY_YEARS_AFTER_FIRST_RECORDING

# Curated eligible non-inducted artists
# Format: (name, first_recording_year, genre, gender, race)
# Sources: Future Rock Legends, Wikipedia, Billboard, published reporting
ELIGIBLE_ARTISTS = [
    # Heavy Metal / Hard Rock -- the genre exclusion case
    ("Motorhead", 1977, "Heavy Metal", "group", "white"),
    ("Thin Lizzy", 1971, "Heavy Metal", "group", "Black"),
    ("Soundgarden", 1988, "Heavy Metal", "group", "white"),
    ("Tool", 1993, "Heavy Metal", "group", "white"),
    ("System of a Down", 1998, "Heavy Metal", "group", "white"),
    ("Pantera", 1983, "Heavy Metal", "group", "white"),
    ("Slayer", 1983, "Heavy Metal", "group", "white"),
    ("Iron Butterfly", 1968, "Heavy Metal", "group", "white"),
    ("Megadeth", 1985, "Heavy Metal", "group", "white"),
    ("Anthrax", 1984, "Heavy Metal", "group", "white"),
    ("Type O Negative", 1991, "Heavy Metal", "group", "white"),
    ("Sepultura", 1986, "Heavy Metal", "group", "Latino"),
    ("Dio", 1983, "Heavy Metal", "group", "white"),
    ("Scorpions", 1972, "Heavy Metal", "group", "white"),
    ("Queensryche", 1983, "Heavy Metal", "group", "white"),
    ("Dream Theater", 1989, "Heavy Metal", "group", "white"),
    ("Mastodon", 2000, "Heavy Metal", "group", "white"),
    ("Lamb of God", 2000, "Heavy Metal", "group", "white"),
    ("White Zombie", 1987, "Heavy Metal", "group", "white"),
    ("King Diamond", 1986, "Heavy Metal", "group", "white"),

    # Punk / Post-Punk / Hardcore
    ("Bad Brains", 1982, "Punk", "group", "Black"),
    ("Mission of Burma", 1981, "Punk", "group", "white"),
    ("The Replacements", 1981, "Punk", "group", "white"),
    ("Husker Du", 1981, "Punk", "group", "white"),
    ("Minor Threat", 1981, "Punk", "group", "white"),
    ("Dead Kennedys", 1979, "Punk", "group", "white"),
    ("Fugazi", 1988, "Punk", "group", "white"),
    ("Sonic Youth", 1982, "Punk", "group", "white"),
    ("Bauhaus", 1979, "Punk", "group", "white"),
    ("Wire", 1977, "Punk", "group", "white"),
    ("The Damned", 1976, "Punk", "group", "white"),
    ("Siouxsie and the Banshees", 1978, "Punk", "group", "white"),
    ("Joy Division", 1978, "Punk", "group", "white"),
    ("The Fall", 1978, "Punk", "group", "white"),
    ("Descendents", 1979, "Punk", "group", "white"),
    ("Social Distortion", 1981, "Punk", "group", "white"),
    ("The Misfits", 1977, "Punk", "group", "white"),
    ("Pixies", 1987, "Punk", "group", "white"),
    ("Dinosaur Jr.", 1985, "Punk", "group", "white"),

    # Electronic / Dance
    ("Kraftwerk", 1970, "Electronic", "group", "white"),
    ("New Order", 1981, "Electronic", "group", "white"),
    ("Aphex Twin", 1992, "Electronic", "male", "white"),
    ("The Prodigy", 1991, "Electronic", "group", "white"),
    ("Massive Attack", 1988, "Electronic", "group", "Black"),
    ("Portishead", 1994, "Electronic", "group", "white"),
    ("The Chemical Brothers", 1992, "Electronic", "group", "white"),
    ("Underworld", 1988, "Electronic", "group", "white"),
    ("Tangerine Dream", 1967, "Electronic", "group", "white"),
    ("Brian Eno", 1973, "Electronic", "male", "white"),
    ("Bjork", 1977, "Electronic", "female", "white"),
    ("Daft Punk", 1994, "Electronic", "group", "white"),

    # Hip-Hop
    ("OutKast", 1994, "Hip-Hop", "group", "Black"),
    ("De La Soul", 1989, "Hip-Hop", "group", "Black"),
    ("Wu-Tang Clan", 1993, "Hip-Hop", "group", "Black"),
    ("Nas", 1994, "Hip-Hop", "male", "Black"),
    ("Snoop Dogg", 1993, "Hip-Hop", "male", "Black"),
    ("LL Cool J", 1985, "Hip-Hop", "male", "Black"),
    ("Ice Cube", 1990, "Hip-Hop", "male", "Black"),
    ("Cypress Hill", 1991, "Hip-Hop", "group", "Latino"),
    ("Lil Wayne", 1999, "Hip-Hop", "male", "Black"),
    ("Kanye West", 2001, "Hip-Hop", "male", "Black"),
    ("Lauryn Hill", 1998, "Hip-Hop", "female", "Black"),
    ("Salt-N-Pepa", 1986, "Hip-Hop", "group", "Black"),
    ("DMX", 1998, "Hip-Hop", "male", "Black"),
    ("Busta Rhymes", 1996, "Hip-Hop", "male", "Black"),

    # Soul / R&B / Funk
    ("Chaka Khan", 1973, "Soul/R&B", "female", "Black"),
    ("The Meters", 1969, "Soul/R&B", "group", "Black"),
    ("War", 1969, "Soul/R&B", "group", "Black"),
    ("Rufus featuring Chaka Khan", 1973, "Soul/R&B", "group", "Black"),
    ("The Commodores", 1974, "Soul/R&B", "group", "Black"),
    ("New Edition", 1983, "Soul/R&B", "group", "Black"),
    ("Boyz II Men", 1991, "Soul/R&B", "group", "Black"),
    ("TLC", 1992, "Soul/R&B", "group", "Black"),
    ("Erykah Badu", 1997, "Soul/R&B", "female", "Black"),
    ("D'Angelo", 1995, "Soul/R&B", "male", "Black"),
    ("Sade", 1984, "Soul/R&B", "group", "Black"),
    ("Anita Baker", 1983, "Soul/R&B", "female", "Black"),
    ("Luther Vandross", 1981, "Soul/R&B", "male", "Black"),
    ("Teena Marie", 1979, "Soul/R&B", "female", "white"),
    ("Rick James", 1978, "Soul/R&B", "male", "Black"),

    # Classic Rock / Pop / Alt
    ("The Smiths", 1984, "Classic Rock", "group", "white"),
    ("Jethro Tull", 1968, "Classic Rock", "group", "white"),
    ("The Cranberries", 1993, "Classic Rock", "group", "white"),
    ("Phish", 1988, "Classic Rock", "group", "white"),
    ("Jane's Addiction", 1987, "Classic Rock", "group", "white"),
    ("Oingo Boingo", 1979, "Classic Rock", "group", "white"),
    ("King Crimson", 1969, "Classic Rock", "group", "white"),
    ("Emerson Lake & Palmer", 1970, "Classic Rock", "group", "white"),
    ("The Moody Blues", 1964, "Classic Rock", "group", "white"),  # already inducted 2018
    ("Styx", 1972, "Classic Rock", "group", "white"),
    ("Boston", 1976, "Classic Rock", "group", "white"),
    ("Foreigner", 1977, "Classic Rock", "group", "white"),  # inducted 2024
    ("REO Speedwagon", 1971, "Classic Rock", "group", "white"),
    ("Toad the Wet Sprocket", 1989, "Classic Rock", "group", "white"),
    ("The Dave Clark Five", 1963, "Classic Rock", "group", "white"),  # inducted 2008
    ("Sinead O'Connor", 1987, "Pop", "female", "white"),
    ("Peter Gabriel", 1977, "Classic Rock", "male", "white"),  # inducted 2014
    ("Kate Bush", 1978, "Pop", "female", "white"),  # inducted 2023
    ("Mariah Carey", 1990, "Pop", "female", "multiracial"),
    ("Backstreet Boys", 1996, "Pop", "group", "white"),
    ("No Doubt", 1992, "Pop", "group", "white"),

    # Blues / Early -- the forgotten teachers
    ("Big Mama Thornton", 1951, "Blues/Early", "female", "Black"),
    ("The Ink Spots", 1934, "Soul/R&B", "group", "Black"),  # inducted EI 1989
    ("Rosetta Tharpe", 1938, "Blues/Early", "female", "Black"),  # inducted EI 2018
    ("Mississippi John Hurt", 1928, "Blues/Early", "male", "Black"),
    ("Blind Willie McTell", 1927, "Blues/Early", "male", "Black"),
    ("Lonnie Johnson", 1925, "Blues/Early", "male", "Black"),
    ("Tampa Red", 1928, "Blues/Early", "male", "Black"),
    ("Big Bill Broonzy", 1927, "Blues/Early", "male", "Black"),
    ("Son House", 1930, "Blues/Early", "male", "Black"),  # inducted EI 2023 pending

    # Folk / Country
    ("The Kingston Trio", 1958, "Folk/Country", "group", "white"),
    ("Gordon Lightfoot", 1966, "Folk/Country", "male", "white"),
    ("Townes Van Zandt", 1968, "Folk/Country", "male", "white"),
    ("Lucinda Williams", 1979, "Folk/Country", "female", "white"),
    ("Emmylou Harris", 1969, "Folk/Country", "female", "white"),
    ("John Prine", 1971, "Folk/Country", "male", "white"),

    # Disco / Dance
    ("Gloria Gaynor", 1965, "Disco/Dance", "female", "Black"),
    ("KC and the Sunshine Band", 1973, "Disco/Dance", "group", "white"),
    ("Chic", 1977, "Disco/Dance", "group", "Black"),
    ("The Pointer Sisters", 1973, "Disco/Dance", "group", "Black"),
]


def load_eligible_population():
    """Load eligible non-inducted artists into the database."""
    conn = get_connection()
    c = conn.cursor()

    loaded = 0
    skipped = 0
    already_inducted = 0

    for row in ELIGIBLE_ARTISTS:
        name, first_rec, genre, gender, race = row
        eligible_year = first_rec + ELIGIBILITY_YEARS_AFTER_FIRST_RECORDING

        # Check if already in database (might be inducted under different name/category)
        existing = c.execute(
            "SELECT id, is_inducted, inducted_category FROM artists WHERE name = ?",
            (name,)
        ).fetchone()

        if existing:
            if existing[1]:  # Already inducted
                already_inducted += 1
                # Still update eligible_year if missing
                c.execute("""
                    UPDATE artists SET eligible_year = COALESCE(eligible_year, ?)
                    WHERE id = ?
                """, (eligible_year, existing[0]))
            else:
                skipped += 1
            continue

        # Insert new eligible artist
        c.execute("""
            INSERT OR IGNORE INTO artists
            (name, first_recording_year, genre_primary, gender, race,
             race_source, eligible_year, is_eligible, is_inducted)
            VALUES (?, ?, ?, ?, ?, 'curated', ?, 1, 0)
        """, (name, first_rec, genre, gender, race, eligible_year))
        loaded += 1

    conn.commit()
    conn.close()

    print(f"Loaded {loaded} new eligible artists")
    print(f"Skipped {skipped} (already in DB as non-inducted)")
    print(f"Already inducted: {already_inducted}")
    return loaded


if __name__ == "__main__":
    count = load_eligible_population()

    # Summary
    total = query("SELECT COUNT(*) as n FROM artists")[0]["n"]
    inducted = query("SELECT COUNT(*) as n FROM artists WHERE is_inducted = 1")[0]["n"]
    eligible = query("SELECT COUNT(*) as n FROM artists WHERE is_eligible = 1")[0]["n"]

    print(f"\nDatabase totals:")
    print(f"  Total artists: {total}")
    print(f"  Inducted: {inducted}")
    print(f"  Eligible (non-inducted): {eligible}")

    # By genre
    by_genre = query("""
        SELECT genre_primary, COUNT(*) as n
        FROM artists WHERE is_eligible = 1
        GROUP BY genre_primary ORDER BY n DESC
    """)
    print(f"\nEligible by genre:")
    for g in by_genre:
        print(f"  {g['genre_primary']}: {g['n']}")

    # By race
    by_race = query("""
        SELECT race, COUNT(*) as n
        FROM artists WHERE is_eligible = 1
        GROUP BY race ORDER BY n DESC
    """)
    print(f"\nEligible by race:")
    for r in by_race:
        print(f"  {r['race']}: {r['n']}")

    # Longest waiting
    longest = query("""
        SELECT name, eligible_year, genre_primary,
               (? - eligible_year) as wait_years
        FROM artists
        WHERE is_eligible = 1 AND eligible_year IS NOT NULL
        ORDER BY eligible_year ASC
        LIMIT 15
    """, (CURRENT_YEAR,))
    print(f"\nLongest waiting eligible artists:")
    for a in longest:
        print(f"  {a['name']}: {a['wait_years']}y ({a['genre_primary']}, eligible {a['eligible_year']})")
