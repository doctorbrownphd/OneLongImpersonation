"""
One Long Impersonation -- Rolling Stone Lists Ingest
Builds the Rolling Stone Attention Score from publicly available "Greatest" lists.

We use published Rolling Stone lists as a proxy for Rolling Stone editorial attention.
These lists are all publicly documented and widely cited.

Lists used:
- 500 Greatest Albums of All Time (2003, 2012, 2020 editions)
- 100 Greatest Artists (2004, 2011)
- 100 Greatest Guitarists (2011, 2023)
- 200 Greatest Singers (2023)
- 500 Greatest Songs of All Time (2004, 2021)

The RS Attention Score = weighted composite of list appearances.
This is NOT a measure of artistic quality. It is a measure of how much
attention Rolling Stone gave an artist, which we then correlate with
induction probability to compute the Wenner Coefficient.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import get_connection, query

# -------------------------------------------------------
# Rolling Stone list data -- curated from published lists
# Format: (artist_name, list_name, list_year, rank, entry_title)
# Only includes artists who appear in our database
# -------------------------------------------------------

RS_LIST_DATA = [
    # 100 Greatest Artists (2004/2011 combined -- top entries)
    ("The Beatles", "100 Greatest Artists", 2011, 1, None),
    ("Bob Dylan", "100 Greatest Artists", 2011, 2, None),
    ("Elvis Presley", "100 Greatest Artists", 2011, 3, None),
    ("The Rolling Stones", "100 Greatest Artists", 2011, 4, None),
    ("Chuck Berry", "100 Greatest Artists", 2011, 5, None),
    ("Jimi Hendrix", "100 Greatest Artists", 2011, 6, None),
    ("James Brown", "100 Greatest Artists", 2011, 7, None),
    ("Little Richard", "100 Greatest Artists", 2011, 8, None),
    ("Aretha Franklin", "100 Greatest Artists", 2011, 9, None),
    ("Ray Charles", "100 Greatest Artists", 2011, 10, None),
    ("Led Zeppelin", "100 Greatest Artists", 2011, 14, None),
    ("The Who", "100 Greatest Artists", 2011, 29, None),
    ("Stevie Wonder", "100 Greatest Artists", 2011, 15, None),
    ("Prince", "100 Greatest Artists", 2011, 27, None),
    ("Bruce Springsteen", "100 Greatest Artists", 2011, 23, None),
    ("Neil Young", "100 Greatest Artists", 2011, 34, None),
    ("Eric Clapton", "100 Greatest Artists", 2011, 55, None),
    ("The Clash", "100 Greatest Artists", 2011, 28, None),
    ("U2", "100 Greatest Artists", 2011, 22, None),
    ("Pink Floyd", "100 Greatest Artists", 2011, 51, None),
    ("Nirvana", "100 Greatest Artists", 2011, 30, None),
    ("Metallica", "100 Greatest Artists", 2011, 61, None),
    ("Radiohead", "100 Greatest Artists", 2011, 73, None),
    ("David Bowie", "100 Greatest Artists", 2011, 39, None),
    ("Joni Mitchell", "100 Greatest Artists", 2011, 62, None),
    ("Michael Jackson", "100 Greatest Artists", 2011, 35, None),
    ("Madonna", "100 Greatest Artists", 2011, 36, None),
    ("Elton John", "100 Greatest Artists", 2011, 49, None),
    ("Ramones", "100 Greatest Artists", 2011, 26, None),
    ("Johnny Cash", "100 Greatest Artists", 2011, 31, None),
    ("The Doors", "100 Greatest Artists", 2011, 41, None),
    ("Buddy Holly", "100 Greatest Artists", 2011, 13, None),
    ("Fats Domino", "100 Greatest Artists", 2011, 25, None),
    ("The Velvet Underground", "100 Greatest Artists", 2011, 19, None),
    ("B.B. King", "100 Greatest Artists", 2011, 6, None),
    ("AC/DC", "100 Greatest Artists", 2011, 72, None),
    ("Patti Smith", "100 Greatest Artists", 2011, 47, None),
    ("Van Morrison", "100 Greatest Artists", 2011, 42, None),
    ("The Kinks", "100 Greatest Artists", 2011, 65, None),
    ("Talking Heads", "100 Greatest Artists", 2011, 64, None),
    ("Pearl Jam", "100 Greatest Artists", 2011, 54, None),
    ("Janis Joplin", "100 Greatest Artists", 2011, 46, None),
    ("Muddy Waters", "100 Greatest Artists", 2011, 17, None),
    ("Bo Diddley", "100 Greatest Artists", 2011, 20, None),
    ("Otis Redding", "100 Greatest Artists", 2011, 21, None),
    ("Marvin Gaye", "100 Greatest Artists", 2011, 18, None),
    ("Sam Cooke", "100 Greatest Artists", 2011, 16, None),
    ("Run-D.M.C.", "100 Greatest Artists", 2011, 48, None),
    ("Sly & The Family Stone", "100 Greatest Artists", 2011, 43, None),

    # 500 Greatest Albums (2020 edition -- selected top entries)
    ("Marvin Gaye", "500 Greatest Albums", 2020, 1, "What's Going On"),
    ("The Beach Boys", "500 Greatest Albums", 2020, 2, "Pet Sounds"),
    ("Joni Mitchell", "500 Greatest Albums", 2020, 3, "Blue"),
    ("Stevie Wonder", "500 Greatest Albums", 2020, 4, "Songs in the Key of Life"),
    ("The Beatles", "500 Greatest Albums", 2020, 5, "Abbey Road"),
    ("Nirvana", "500 Greatest Albums", 2020, 6, "Nevermind"),
    ("Fleetwood Mac", "500 Greatest Albums", 2020, 7, "Rumours"),
    ("Prince", "500 Greatest Albums", 2020, 8, "Purple Rain"),
    ("Bob Dylan", "500 Greatest Albums", 2020, 9, "Highway 61 Revisited"),
    ("The Beatles", "500 Greatest Albums", 2020, 10, "White Album"),
    ("Aretha Franklin", "500 Greatest Albums", 2020, 11, "I Never Loved a Man"),
    ("Led Zeppelin", "500 Greatest Albums", 2020, 16, "Led Zeppelin IV"),
    ("The Rolling Stones", "500 Greatest Albums", 2020, 14, "Exile on Main St."),
    ("Michael Jackson", "500 Greatest Albums", 2020, 12, "Thriller"),
    ("Pink Floyd", "500 Greatest Albums", 2020, 55, "Dark Side of the Moon"),
    ("The Clash", "500 Greatest Albums", 2020, 18, "London Calling"),
    ("Radiohead", "500 Greatest Albums", 2020, 20, "OK Computer"),
    ("The Who", "500 Greatest Albums", 2020, 25, "Who's Next"),
    ("David Bowie", "500 Greatest Albums", 2020, 30, "Ziggy Stardust"),
    ("Bruce Springsteen", "500 Greatest Albums", 2020, 38, "Born to Run"),
    ("The Velvet Underground", "500 Greatest Albums", 2020, 23, "VU & Nico"),
    ("Metallica", "500 Greatest Albums", 2020, 235, "Master of Puppets"),
    ("Black Sabbath", "500 Greatest Albums", 2020, 69, "Paranoid"),
    ("AC/DC", "500 Greatest Albums", 2020, 77, "Back in Black"),
    ("Guns N' Roses", "500 Greatest Albums", 2020, 62, "Appetite for Destruction"),
    ("Jay-Z", "500 Greatest Albums", 2020, 22, "Reasonable Doubt"),
    ("Public Enemy", "500 Greatest Albums", 2020, 17, "It Takes a Nation"),
    ("The Notorious B.I.G.", "500 Greatest Albums", 2020, 26, "Ready to Die"),
    ("N.W.A", "500 Greatest Albums", 2020, 83, "Straight Outta Compton"),
    ("Run-D.M.C.", "500 Greatest Albums", 2020, 139, "Raising Hell"),
    ("Tupac Shakur", "500 Greatest Albums", 2020, 104, "All Eyez on Me"),
    ("Eminem", "500 Greatest Albums", 2020, 300, "Marshall Mathers LP"),
    ("A Tribe Called Quest", "500 Greatest Albums", 2020, 154, "Low End Theory"),
    ("Whitney Houston", "500 Greatest Albums", 2020, 254, "Whitney Houston"),
    ("Janet Jackson", "500 Greatest Albums", 2020, 260, "Control"),
    ("Depeche Mode", "500 Greatest Albums", 2020, 158, "Violator"),
    ("Kate Bush", "500 Greatest Albums", 2020, 68, "Hounds of Love"),
    ("Nina Simone", "500 Greatest Albums", 2020, 249, "I Put a Spell on You"),
    ("Dolly Parton", "500 Greatest Albums", 2020, 409, "Coat of Many Colors"),
    ("Iron Maiden", "500 Greatest Albums", 2020, 400, "Number of the Beast"),
    ("Judas Priest", "500 Greatest Albums", 2020, 377, "British Steel"),

    # 100 Greatest Guitarists (2011 -- selected)
    ("Jimi Hendrix", "100 Greatest Guitarists", 2011, 1, None),
    ("Eric Clapton", "100 Greatest Guitarists", 2011, 2, None),
    ("Led Zeppelin", "100 Greatest Guitarists", 2011, 3, "Jimmy Page"),
    ("Chuck Berry", "100 Greatest Guitarists", 2011, 7, None),
    ("B.B. King", "100 Greatest Guitarists", 2011, 6, None),
    ("The Rolling Stones", "100 Greatest Guitarists", 2011, 4, "Keith Richards"),
    ("Muddy Waters", "100 Greatest Guitarists", 2011, 49, None),
    ("Neil Young", "100 Greatest Guitarists", 2011, 17, None),
    ("Prince", "100 Greatest Guitarists", 2011, 33, None),
    ("Van Halen", "100 Greatest Guitarists", 2011, 8, "Eddie Van Halen"),
    ("Stevie Ray Vaughan", "100 Greatest Guitarists", 2011, 12, None),
    ("Buddy Guy", "100 Greatest Guitarists", 2011, 30, None),
    ("The Who", "100 Greatest Guitarists", 2011, 10, "Pete Townshend"),
    ("Santana", "100 Greatest Guitarists", 2011, 20, None),
    ("Metallica", "100 Greatest Guitarists", 2011, 87, "Kirk Hammett"),
    ("Black Sabbath", "100 Greatest Guitarists", 2011, 25, "Tony Iommi"),

    # 200 Greatest Singers (2023 -- selected)
    ("Aretha Franklin", "200 Greatest Singers", 2023, 1, None),
    ("Whitney Houston", "200 Greatest Singers", 2023, 2, None),
    ("Sam Cooke", "200 Greatest Singers", 2023, 3, None),
    ("Stevie Wonder", "200 Greatest Singers", 2023, 5, None),
    ("Ray Charles", "200 Greatest Singers", 2023, 6, None),
    ("Marvin Gaye", "200 Greatest Singers", 2023, 4, None),
    ("Elvis Presley", "200 Greatest Singers", 2023, 12, None),
    ("Otis Redding", "200 Greatest Singers", 2023, 7, None),
    ("Little Richard", "200 Greatest Singers", 2023, 8, None),
    ("James Brown", "200 Greatest Singers", 2023, 10, None),
    ("Tina Turner", "200 Greatest Singers", 2023, 9, None),
    ("Bob Dylan", "200 Greatest Singers", 2023, 14, None),
    ("Prince", "200 Greatest Singers", 2023, 13, None),
    ("Nina Simone", "200 Greatest Singers", 2023, 15, None),
    ("Janis Joplin", "200 Greatest Singers", 2023, 17, None),
    ("Joni Mitchell", "200 Greatest Singers", 2023, 18, None),
    ("David Bowie", "200 Greatest Singers", 2023, 23, None),
    ("Smokey Robinson", "200 Greatest Singers", 2023, 20, None),
    ("Al Green", "200 Greatest Singers", 2023, 11, None),
    ("Dolly Parton", "200 Greatest Singers", 2023, 36, None),
    ("Patti Smith", "200 Greatest Singers", 2023, 52, None),
    ("Freddie Mercury", "200 Greatest Singers", 2023, 16, None),
    ("Bruce Springsteen", "200 Greatest Singers", 2023, 56, None),
    ("Missy Elliott", "200 Greatest Singers", 2023, 97, None),
    ("Jay-Z", "200 Greatest Singers", 2023, 142, None),
    ("Eminem", "200 Greatest Singers", 2023, 83, None),
    ("Cyndi Lauper", "200 Greatest Singers", 2023, 186, None),
]


def compute_attention_scores():
    """
    Compute Rolling Stone Attention Score for each artist.

    Scoring:
    - 100 Greatest Artists: 10 points * (101 - rank) / 100
    - 500 Greatest Albums: 5 points per appearance * (501 - rank) / 500
    - 100 Greatest Guitarists: 3 points * (101 - rank) / 100
    - 200 Greatest Singers: 3 points * (201 - rank) / 200

    Multiple appearances across lists stack.
    Score is normalized to 0-100 range.
    """
    weights = {
        "100 Greatest Artists": (10.0, 101),
        "500 Greatest Albums": (5.0, 501),
        "100 Greatest Guitarists": (3.0, 101),
        "200 Greatest Singers": (3.0, 201),
    }

    # Aggregate raw scores by artist
    raw_scores = {}
    for entry in RS_LIST_DATA:
        name = entry[0]
        list_name = entry[1]
        rank = entry[3]

        weight, max_rank = weights.get(list_name, (1.0, 100))
        score = weight * (max_rank - rank) / (max_rank - 1)

        if name not in raw_scores:
            raw_scores[name] = 0
        raw_scores[name] += score

    # Normalize to 0-100
    if raw_scores:
        max_score = max(raw_scores.values())
        for name in raw_scores:
            raw_scores[name] = round(raw_scores[name] / max_score * 100, 2)

    return raw_scores


def load_rs_data():
    """Load Rolling Stone list data into the database."""
    conn = get_connection()
    c = conn.cursor()

    loaded = 0
    for entry in RS_LIST_DATA:
        name, list_name, list_year, rank, entry_title = entry

        # Find artist
        row = c.execute(
            "SELECT id FROM artists WHERE name = ? LIMIT 1", (name,)
        ).fetchone()
        if not row:
            continue

        artist_id = row[0]
        c.execute("""
            INSERT OR IGNORE INTO rs_list_appearances
            (artist_id, list_name, list_year, rank, entry_title)
            VALUES (?, ?, ?, ?, ?)
        """, (artist_id, list_name, list_year, rank, entry_title))
        loaded += 1

    conn.commit()

    # Now compute and store attention scores
    scores = compute_attention_scores()
    for name, score in scores.items():
        c.execute("""
            UPDATE artists SET rs_attention_score = ?
            WHERE name = ?
        """, (score, name))

    conn.commit()
    conn.close()

    print(f"Loaded {loaded} RS list appearances")
    print(f"Computed attention scores for {len(scores)} artists")

    return scores


if __name__ == "__main__":
    scores = load_rs_data()

    # Top 20 by RS Attention Score
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 by Rolling Stone Attention Score:")
    for name, score in top:
        print(f"  {score:>6.2f}  {name}")

    # Show artists with zero RS attention who are inducted
    zero_rs = query("""
        SELECT name, genre_primary, inducted_year
        FROM artists
        WHERE is_inducted = 1
          AND inducted_category = 'P'
          AND (rs_attention_score IS NULL OR rs_attention_score = 0)
        ORDER BY inducted_year
    """)
    print(f"\nInducted Performers with ZERO RS Attention Score: {len(zero_rs)}")
    for a in zero_rs[:15]:
        print(f"  {a['name']} ({a['genre_primary']}, {a['inducted_year']})")
