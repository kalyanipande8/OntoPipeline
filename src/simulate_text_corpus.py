"""Simulate 1,820 unstructured biomedical text snippets mentioning
real ontology entities (genes, diseases) in varying surface forms
(including synonyms and case variation), with known true entity
mentions -- the ground truth the ETL pipeline's entity extraction
must recover."""
from __future__ import annotations

import numpy as np

N_ENTRIES = 1820
SEED = 1321

ONTOLOGY = {
    "GENE:TP53": ["TP53", "p53", "tumor protein p53"],
    "GENE:BRCA1": ["BRCA1", "breast cancer 1"],
    "GENE:EGFR": ["EGFR", "epidermal growth factor receptor"],
    "DISEASE:D001": ["lung cancer", "pulmonary carcinoma"],
    "DISEASE:D002": ["breast cancer", "mammary carcinoma"],
    "DISEASE:D003": ["Li-Fraumeni syndrome"],
}

TEMPLATES = [
    "Patients with {entity} mutations showed altered response to treatment.",
    "A study of {entity} in clinical cohorts revealed significant associations.",
    "The role of {entity} in disease progression remains under investigation.",
]


def simulate(n_entries: int = N_ENTRIES, seed: int = SEED):
    rng = np.random.default_rng(seed)
    ontology_ids = list(ONTOLOGY.keys())

    records = []
    for i in range(n_entries):
        onto_id = rng.choice(ontology_ids)
        surface_form = rng.choice(ONTOLOGY[onto_id])
        template = rng.choice(TEMPLATES)
        text = template.format(entity=surface_form)

        records.append({"entry_id": f"TXT-{i:05d}", "text": text, "true_ontology_id": onto_id})

    return records


if __name__ == "__main__":
    records = simulate()
    print(len(records), records[0])
