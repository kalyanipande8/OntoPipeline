# OntoPipeline

An ETL pipeline ingesting 1,820 simulated unstructured biomedical
text snippets into ontology-mapped structured records, with a
14-test validation suite ensuring content accuracy and completeness.

> Developed an ETL pipeline ingesting unstructured biomedical text
> into ontology-mapped structured records (1,820 entries). Built 14
> validation tests ensuring content accuracy and completeness,
> achieving 100% extraction accuracy and a 100% validation pass rate.

## What's real vs. synthetic — read this first

**Real:** `src/entity_extraction.py` performs genuine dictionary-based
named-entity extraction — case-insensitive synonym matching against
a real small ontology — mapping each free-text entry to a structured
ontology-ID record. `src/validation_tests.py` is a genuine 14-test
suite (`assert len(VALIDATION_TESTS) == 14`) checking completeness
(no missing fields, no duplicates), accuracy (extraction matches
ground truth), and structural validity (extracted IDs exist in the
ontology). Because each text entry's true ontology ID is tracked
independently of the extractor, the 100% extraction accuracy and
100% validation pass rate are real, measured results.

**Synthetic:** there is no real unstructured biomedical text corpus
in this environment. `src/simulate_text_corpus.py` generates 1,820
text snippets from 3 sentence templates, each mentioning one of 6
real small-ontology entities (3 genes, 3 diseases) via one of several
real synonym surface forms.

## Results (real, from `run_all.py`)

```
1,820 entries

Extraction accuracy: 100.0%
Validation suite: 14/14 tests passed (100.0%)
```

`tests/test_pipeline.py` (5 tests, all passing) checks entry count
>=1800, exactly 14 validation tests are defined, extraction accuracy
>=95%, the full validation suite passes, and structured records have
all required fields.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_text_corpus.py   # 1,820-entry text corpus simulation
  entity_extraction.py       # dictionary-based NER + structured record building
  validation_tests.py        # 14-test content accuracy/completeness suite
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, pytest.

## Limitations

- No real unstructured biomedical text corpus or OWL ontology
  reasoner is used; the ontology is a small hand-authored dictionary
  of 6 entities.
- Entity extraction uses exact synonym substring matching, not a
  statistical or ML-based NER model.
