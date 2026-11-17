import json
import os

from src.simulate_text_corpus import simulate
from src.entity_extraction import build_structured_records
from src.validation_tests import run_validation_tests


def main():
    raw_entries = simulate()
    records = build_structured_records(raw_entries)
    validation = run_validation_tests(records)

    correct = sum(1 for r in records if r["extracted_ontology_id"] == r["true_ontology_id"])
    accuracy = round(100 * correct / len(records), 2)

    summary = {"n_entries": len(records), "extraction_accuracy_pct": accuracy, "validation": validation}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
