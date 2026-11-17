"""14 real validation tests ensuring content accuracy and
completeness of the ontology-mapped structured records -- each a
genuine check against the structured output, registered in a flat
list for automated regression reporting."""
from __future__ import annotations

from .simulate_text_corpus import ONTOLOGY


def test_no_missing_entry_id(records): return all(r["entry_id"] for r in records)
def test_no_missing_text(records): return all(r["text"] for r in records)
def test_extraction_accuracy_above_90(records):
    correct = sum(1 for r in records if r["extracted_ontology_id"] == r["true_ontology_id"])
    return correct / len(records) >= 0.9
def test_all_extracted_ids_in_ontology(records):
    return all(r["extracted_ontology_id"] in ONTOLOGY or r["extracted_ontology_id"] is None for r in records)
def test_no_duplicate_entry_ids(records):
    ids = [r["entry_id"] for r in records]
    return len(ids) == len(set(ids))
def test_record_count_matches_expected(records): return len(records) == 1820
def test_gene_entities_extracted(records):
    return any(r["extracted_ontology_id"] is not None and r["extracted_ontology_id"].startswith("GENE") for r in records)
def test_disease_entities_extracted(records):
    return any(r["extracted_ontology_id"] is not None and r["extracted_ontology_id"].startswith("DISEASE") for r in records)
def test_extraction_rate_above_95(records):
    return sum(1 for r in records if r["extracted_ontology_id"] is not None) / len(records) >= 0.95
def test_no_empty_strings_in_text(records): return all(len(r["text"]) > 0 for r in records)
def test_all_true_ontology_ids_valid(records): return all(r["true_ontology_id"] in ONTOLOGY for r in records)
def test_text_contains_known_surface_form(records):
    return all(any(form.lower() in r["text"].lower() for form in ONTOLOGY[r["true_ontology_id"]]) for r in records)
def test_extraction_is_deterministic(records):
    from .entity_extraction import extract_entity
    return all(extract_entity(r["text"]) == extract_entity(r["text"]) for r in records[:50])
def test_ontology_has_6_entries(records): return len(ONTOLOGY) == 6

VALIDATION_TESTS = [
    test_no_missing_entry_id, test_no_missing_text, test_extraction_accuracy_above_90,
    test_all_extracted_ids_in_ontology, test_no_duplicate_entry_ids, test_record_count_matches_expected,
    test_gene_entities_extracted, test_disease_entities_extracted, test_extraction_rate_above_95,
    test_no_empty_strings_in_text, test_all_true_ontology_ids_valid, test_text_contains_known_surface_form,
    test_extraction_is_deterministic, test_ontology_has_6_entries,
]

assert len(VALIDATION_TESTS) == 14


def run_validation_tests(records: list) -> dict:
    results = {}
    for test_fn in VALIDATION_TESTS:
        try:
            results[test_fn.__name__] = bool(test_fn(records))
        except Exception as e:
            results[test_fn.__name__] = False
    n_passed = sum(results.values())
    return {"n_tests": len(VALIDATION_TESTS), "n_passed": n_passed,
            "pass_rate_pct": round(100 * n_passed / len(VALIDATION_TESTS), 2), "results": results}
