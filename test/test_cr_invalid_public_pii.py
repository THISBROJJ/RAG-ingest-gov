from ingestion.catalogue_reader import CatalogueError, get_dataset_metadata
from pathlib import Path
import pytest


EXAMPLE = Path("test/examples/datasets_public_w_pii.yaml")
SCHEMA = Path("catalogue/schema.yaml")


def test_missing_dataset_fails():
    with pytest.raises(CatalogueError):
        get_dataset_metadata(
            "bad_public_pii_dataset",
            catalogue_path=EXAMPLE,
            schema_path=SCHEMA
        )

def test_confidential_dataset_llm_enabled_fails():
    with pytest.raises(CatalogueError):
        get_dataset_metadata(
            "bad_public_pii_dataset",
            catalogue_path=EXAMPLE,
            schema_path=SCHEMA
        )
