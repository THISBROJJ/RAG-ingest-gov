import pytest
from ingestion.catalogue_reader import get_dataset_metadata, CatalogueError
from pathlib import Path

EXAMPLE = Path("tests/examples/datasets_valid.yaml")
SCHEMA = Path("catalogue/schema.yaml")

def test_missing_dataset_fails():
    with pytest.raises(CatalogueError):
        get_dataset_metadata(
            "does_not_exist",
            catalogue_path=EXAMPLE,
            schema_path=SCHEMA
        )
