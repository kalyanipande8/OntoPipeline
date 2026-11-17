"""Real dictionary-based entity extraction: matches surface-form
synonyms in free text against the ontology's known forms (case-
insensitive substring match), mapping each text entry to a
structured ontology-ID record -- the real ETL transform step."""
from __future__ import annotations

from .simulate_text_corpus import ONTOLOGY


def extract_entity(text: str) -> str | None:
    text_lower = text.lower()
    for onto_id, surface_forms in ONTOLOGY.items():
        for form in surface_forms:
            if form.lower() in text_lower:
                return onto_id
    return None


def build_structured_records(raw_entries: list) -> list:
    records = []
    for entry in raw_entries:
        extracted_id = extract_entity(entry["text"])
        records.append({"entry_id": entry["entry_id"], "text": entry["text"],
                         "true_ontology_id": entry["true_ontology_id"], "extracted_ontology_id": extracted_id})
    return records
