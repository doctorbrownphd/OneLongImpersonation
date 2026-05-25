# One Long Impersonation -- Pipeline Orchestration
# Usage: make <target>

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: setup clean ingest models export all

# -----------------------------------------------
# Setup
# -----------------------------------------------

setup: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(PYTHON) src/db.py
	@echo "Pipeline ready. Database initialized."

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

# -----------------------------------------------
# Data Ingestion (Phase 1)
# -----------------------------------------------

ingest: ingest-rockhall ingest-wikidata ingest-musicbrainz ingest-rs-lists

ingest-rockhall:
	$(PYTHON) src/ingest/rockhall.py

ingest-wikidata:
	$(PYTHON) src/ingest/wikidata.py

ingest-musicbrainz:
	$(PYTHON) src/ingest/musicbrainz.py

ingest-discogs:
	$(PYTHON) src/ingest/discogs.py

ingest-riaa:
	$(PYTHON) src/ingest/riaa.py

ingest-rs-lists:
	$(PYTHON) src/ingest/rolling_stone.py

ingest-frl:
	$(PYTHON) src/ingest/future_rock_legends.py

# -----------------------------------------------
# ML Models (Phase 2)
# -----------------------------------------------

models: model-criteria model-network model-survival model-genre model-wenner

model-criteria:
	$(PYTHON) src/models/criteria_compliance.py

model-network:
	$(PYTHON) src/models/teacher_student_network.py

model-survival:
	$(PYTHON) src/models/survival_analysis.py

model-genre:
	$(PYTHON) src/models/genre_diversity.py

model-wenner:
	$(PYTHON) src/models/wenner_coefficient.py

# -----------------------------------------------
# Docket Generation (Phase 3)
# -----------------------------------------------

docket:
	$(PYTHON) src/docket/batch_generate.py

# -----------------------------------------------
# Export to Chapter Data Files
# -----------------------------------------------

export:
	$(PYTHON) src/export/to_chapter_data.py

# -----------------------------------------------
# Full Pipeline
# -----------------------------------------------

all: setup ingest models export
	@echo "Full pipeline complete."

# -----------------------------------------------
# Cleanup
# -----------------------------------------------

clean:
	rm -f rockhall.db
	rm -rf data/processed/*
	@echo "Cleaned."

nuke: clean
	rm -rf $(VENV)
	@echo "Nuked venv."
