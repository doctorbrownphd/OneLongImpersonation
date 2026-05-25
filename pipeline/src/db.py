"""
One Long Impersonation -- SQLite Schema and Helpers
The working database for the data pipeline.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "rockhall.db")


def get_connection(db_path=None):
    """Return a connection to the SQLite database."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path=None):
    """Create all tables. Safe to call multiple times (IF NOT EXISTS)."""
    conn = get_connection(db_path)
    c = conn.cursor()

    # -----------------------------------------------------------
    # Artists -- the core table. Every eligible and inducted artist.
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            musicbrainz_id  TEXT,
            wikidata_id     TEXT,
            discogs_id      TEXT,

            -- Demographics (from Wikidata + manual review)
            gender          TEXT,          -- male / female / non-binary / group
            race            TEXT,          -- Black / white / Latino / Asian / multiracial / other
            race_source     TEXT,          -- wikidata / manual / documented-self-id
            race_notes      TEXT,          -- any ambiguity documented

            -- Genre classification
            genre_primary   TEXT,          -- from MusicBrainz + Discogs cross-reference
            genre_secondary TEXT,          -- JSON array of up to 3 secondary genres

            -- Career
            first_recording_year  INTEGER, -- year of first commercial recording
            last_active_year      INTEGER, -- year of last activity (or NULL if active)
            career_length_years   INTEGER, -- computed: last_active - first_recording

            -- Hall of Fame status
            eligible_year   INTEGER,       -- first_recording_year + 25
            is_eligible     INTEGER DEFAULT 0,  -- 1 if eligible and not inducted
            is_inducted     INTEGER DEFAULT 0,
            inducted_year   INTEGER,
            inducted_category TEXT,         -- Performer / Early Influence / Musical Excellence / etc.

            -- Catalog metrics
            studio_album_count    INTEGER,
            total_release_count   INTEGER,

            -- Commercial metrics
            riaa_certified_units  INTEGER,  -- total certified units (gold=500k, plat=1M, etc.)

            -- Criteria Compliance Score (computed by model)
            criteria_score        REAL,     -- 0-100 composite
            excellence_score      REAL,
            influence_score       REAL,
            career_length_score   REAL,
            catalog_depth_score   REAL,
            genre_contribution_score REAL,

            -- Rolling Stone Attention Score (computed from lists)
            rs_attention_score    REAL,

            -- Metadata
            created_at      TEXT DEFAULT (datetime('now')),
            updated_at      TEXT DEFAULT (datetime('now')),

            UNIQUE(name, first_recording_year)
        )
    """)

    # -----------------------------------------------------------
    # Inductions -- one row per induction event
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS inductions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id   INTEGER NOT NULL REFERENCES artists(id),
            year        INTEGER NOT NULL,
            category    TEXT NOT NULL,
            UNIQUE(artist_id, year, category)
        )
    """)

    # -----------------------------------------------------------
    # Nominations -- one row per nomination year
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS nominations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id   INTEGER NOT NULL REFERENCES artists(id),
            year        INTEGER NOT NULL,
            fan_vote_rank INTEGER,          -- rank in fan vote, if available
            UNIQUE(artist_id, year)
        )
    """)

    # -----------------------------------------------------------
    # Influence pairs -- teacher-student relationships
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS influence_pairs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id      INTEGER NOT NULL REFERENCES artists(id),
            student_id      INTEGER NOT NULL REFERENCES artists(id),
            source_type     TEXT NOT NULL,   -- musicbrainz / interview / liner_notes / biography / curated
            source_citation TEXT,            -- specific citation text
            source_url      TEXT,            -- URL if available
            confidence      TEXT DEFAULT 'documented',  -- documented / reported / estimated
            UNIQUE(teacher_id, student_id, source_type)
        )
    """)

    # -----------------------------------------------------------
    # RIAA certifications
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS certifications (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id       INTEGER NOT NULL REFERENCES artists(id),
            title           TEXT NOT NULL,
            certification   TEXT NOT NULL,   -- Gold / Platinum / Multi-Platinum / Diamond
            units           INTEGER,         -- certified units
            year            INTEGER,
            UNIQUE(artist_id, title, certification)
        )
    """)

    # -----------------------------------------------------------
    # Rolling Stone list appearances
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS rs_list_appearances (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id       INTEGER NOT NULL REFERENCES artists(id),
            list_name       TEXT NOT NULL,   -- 500 Greatest Albums / 100 Greatest Artists / etc.
            list_year       INTEGER,         -- year the list was published
            rank            INTEGER,         -- position on the list
            entry_title     TEXT,            -- album or song title if applicable
            UNIQUE(artist_id, list_name, list_year, entry_title)
        )
    """)

    # -----------------------------------------------------------
    # Nominating committee members (documented public record)
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS committee_members (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            role            TEXT,            -- member / chairman / etc.
            affiliation     TEXT,            -- Rolling Stone / Billboard / etc.
            year_start      INTEGER,
            year_end        INTEGER,
            source          TEXT NOT NULL,   -- public record citation
            UNIQUE(name, year_start)
        )
    """)

    # -----------------------------------------------------------
    # Model outputs -- survival analysis
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS survival_outputs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id       INTEGER NOT NULL REFERENCES artists(id),
            years_to_event  REAL,           -- years from eligibility to induction (or censoring)
            event_observed  INTEGER,         -- 1 = inducted, 0 = censored
            stratum         TEXT,            -- stratification group label
            predicted_survival REAL,         -- model-predicted survival probability
            UNIQUE(artist_id)
        )
    """)

    # -----------------------------------------------------------
    # Docket verdicts -- AI-generated briefs
    # -----------------------------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS docket_verdicts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id       INTEGER NOT NULL REFERENCES artists(id),
            verdict         TEXT NOT NULL,   -- STRONG_CASE / CASE / BORDERLINE / INSUFFICIENT
            confidence      REAL,           -- 0-1 confidence in verdict
            brief_json      TEXT,            -- full structured brief as JSON
            generated_at    TEXT,
            model_version   TEXT,            -- e.g. claude-sonnet-4-20250514
            human_reviewed  INTEGER DEFAULT 0,
            reviewer_name   TEXT,
            review_date     TEXT,
            UNIQUE(artist_id)
        )
    """)

    # -----------------------------------------------------------
    # Indexes for common queries
    # -----------------------------------------------------------
    c.execute("CREATE INDEX IF NOT EXISTS idx_artists_eligible ON artists(is_eligible)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_artists_inducted ON artists(is_inducted)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_artists_genre ON artists(genre_primary)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_artists_race ON artists(race)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_artists_criteria ON artists(criteria_score)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_influence_teacher ON influence_pairs(teacher_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_influence_student ON influence_pairs(student_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_nominations_artist ON nominations(artist_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_inductions_year ON inductions(year)")

    conn.commit()
    conn.close()
    return DB_PATH


def query(sql, params=None, db_path=None):
    """Execute a SELECT and return all rows as dicts."""
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute(sql, params or ())
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def execute(sql, params=None, db_path=None):
    """Execute an INSERT/UPDATE/DELETE and return lastrowid."""
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute(sql, params or ())
    conn.commit()
    lastid = c.lastrowid
    conn.close()
    return lastid


def executemany(sql, param_list, db_path=None):
    """Execute a batch INSERT/UPDATE."""
    conn = get_connection(db_path)
    c = conn.cursor()
    c.executemany(sql, param_list)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    path = init_db()
    print(f"Database initialized at {path}")

    # Verify tables
    conn = get_connection()
    tables = [r["name"] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    conn.close()
    print(f"Tables: {', '.join(tables)}")
