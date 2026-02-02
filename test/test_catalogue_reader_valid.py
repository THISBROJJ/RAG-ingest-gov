from ingestion.catalogue_reader import get_dataset_metadata
from pathlib import Path


EXAMPLE = Path("test/examples/datasets_valid.yaml")
SCHEMA = Path("catalogue/schema.yaml")

def test_valid_catalog_loads():
    metadata = get_dataset_metadata(
        "hr_employees",
        catalogue_path=EXAMPLE,
        schema_path=SCHEMA
    )

    assert metadata["classification"] == "CONFIDENTIAL"
    assert metadata["contains_pii"] is True
    assert metadata["llm_policy"]["allowed"] is False
