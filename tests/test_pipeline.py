import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_text_corpus import simulate
from src.entity_extraction import build_structured_records
from src.validation_tests import run_validation_tests, VALIDATION_TESTS


def test_at_least_1800_entries():
    raw = simulate()
    assert len(raw) >= 1800


def test_exactly_14_validation_tests():
    assert len(VALIDATION_TESTS) == 14


def test_extraction_is_highly_accurate():
    raw = simulate()
    records = build_structured_records(raw)
    correct = sum(1 for r in records if r["extracted_ontology_id"] == r["true_ontology_id"])
    assert correct / len(records) >= 0.95


def test_validation_suite_passes_all_tests():
    raw = simulate()
    records = build_structured_records(raw)
    validation = run_validation_tests(records)
    assert validation["pass_rate_pct"] == 100.0


def test_structured_records_have_required_fields():
    raw = simulate()
    records = build_structured_records(raw)
    for r in records[:20]:
        assert "entry_id" in r and "extracted_ontology_id" in r
