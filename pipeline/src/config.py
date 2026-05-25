"""
One Long Impersonation -- Pipeline Configuration
"""

import os

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PIPELINE_ROOT = os.path.join(PROJECT_ROOT, "pipeline")
DB_PATH = os.path.join(PIPELINE_ROOT, "rockhall.db")
RAW_DATA_DIR = os.path.join(PIPELINE_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PIPELINE_ROOT, "data", "processed")
CURATED_DATA_DIR = os.path.join(PIPELINE_ROOT, "data", "curated")
CHAPTERS_DIR = os.path.join(PROJECT_ROOT, "chapters")

# MusicBrainz API
MUSICBRAINZ_APP_NAME = "OneLongImpersonation"
MUSICBRAINZ_APP_VERSION = "0.1"
MUSICBRAINZ_CONTACT = "jeremy@onelongimpersonation.report"
MUSICBRAINZ_RATE_LIMIT = 1.0  # seconds between requests

# Wikidata SPARQL
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
WIKIDATA_USER_AGENT = "OneLongImpersonation/0.1 (data journalism; CC0 output)"

# Rock and Roll Hall of Fame
ROCKHALL_BASE_URL = "https://www.rockhall.com"

# Claude API (for Docket generation)
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 4096

# Hall eligibility rule
ELIGIBILITY_YEARS_AFTER_FIRST_RECORDING = 25

# Current year (for censoring in survival analysis)
CURRENT_YEAR = 2026

# Criteria Compliance Model weights (documented, sensitivity-tested)
CRITERIA_WEIGHTS = {
    "excellence": 0.25,       # critical reception + Grammy nominations
    "influence": 0.25,        # network centrality + inbound citations
    "career_length": 0.15,    # years active
    "catalog_depth": 0.15,    # album count + release count
    "genre_contribution": 0.20,  # first-mover + genre centrality
}

# Genre taxonomy -- primary genre labels used across the platform
GENRE_TAXONOMY = [
    "Classic Rock",
    "Soul/R&B",
    "Pop",
    "Folk/Country",
    "Hip-Hop",
    "Heavy Metal",
    "Punk",
    "Electronic",
    "Blues/Early",
    "Disco/Dance",
]

# Genre color mapping (matches shared/design-tokens.css)
GENRE_COLORS = {
    "Classic Rock":  "#d4a017",
    "Soul/R&B":      "#b03434",
    "Pop":           "#c47a3a",
    "Folk/Country":  "#8a7d48",
    "Hip-Hop":       "#5a6f8a",
    "Heavy Metal":   "#3d4a5c",
    "Punk":          "#7a4a8a",
    "Electronic":    "#5f7d56",
    "Blues/Early":   "#5c3a2a",
    "Disco/Dance":   "#8a5a6f",
}
