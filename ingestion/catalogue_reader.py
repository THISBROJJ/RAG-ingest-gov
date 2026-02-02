import yaml
import yamale
from yamale.validators import DefaultValidators
from pathlib import Path

"""
References:
- Yamale documentation: https://pypi.org/project/yamale/
    - yamale-6.1.0
    - schema = yamale.make_schema('path/to/schema.yaml')
    - data = yamale.make_data('path/to/data.yaml')
    - yamale.validate(schema, data)
- Pyyaml-6.0.3
    - yaml.safe_load() vs. yaml.load()

"""


CATALOGUE_PATH = Path("catalogue/data_catalogue.yaml")
SCHEMA_PATH = Path("catalogue/schema.yaml")


class CatalogueError(Exception):
    """Raised when the data catalog is invalid or inconsistent."""
    pass


def load_and_validate_catalog(catalogue_path=CATALOGUE_PATH, schema_path=SCHEMA_PATH) -> dict:
    """
    Loads and validates the data catalog using Yamale.
    Returns the parsed catalog as a Python dict.
    """
    if not catalogue_path.exists():
        raise CatalogueError(f"Catalog file not found: {catalogue_path}")

    if not schema_path.exists():
        raise CatalogueError(f"Schema file not found: {schema_path}")

    schema = yamale.make_schema(str(schema_path))
    data = yamale.make_data(str(catalogue_path))

    try:
        yamale.validate(schema, data)
    except yamale.YamaleError as e:
        raise CatalogueError(f"Catalog validation failed:\n{e}")

    with open(catalogue_path, "r") as f:
        return yaml.safe_load(f)


def get_dataset_metadata(dataset_name: str, catalogue_path=CATALOGUE_PATH, schema_path=SCHEMA_PATH) -> dict:
    """
    Retrieves metadata for a single dataset from the catalog.
    """
    catalog = load_and_validate_catalog(catalogue_path=catalogue_path, schema_path=schema_path)
    datasets = catalog.get("datasets", {})
    if dataset_name not in datasets:
        raise CatalogueError(f"Dataset '{dataset_name}' is not registered in the catalog")

    metadata = datasets[dataset_name]

    _validate_internal_consistency(dataset_name, metadata)

    return metadata


def _validate_internal_consistency(dataset_name: str, metadata: dict):
    """
    Cross-field validation beyond Yamale's schema checks.
    """
    classification = metadata["classification"]
    contains_pii = metadata["contains_pii"]
    llm_allowed = metadata["llm_policy"]["allowed"]

    if contains_pii and classification == "PUBLIC":
        raise CatalogueError(
            f"{dataset_name}: PUBLIC datasets cannot contain PII"
        )

    if classification == "CONFIDENTIAL" and llm_allowed:
        raise CatalogueError(
            f"{dataset_name}: CONFIDENTIAL datasets cannot be LLM-enabled"
        )

    if metadata["datatype"] not in {"Table", "Document", "Log"}:
        raise CatalogueError(
            f"{dataset_name}: Unsupported dataset type '{metadata['type']}'"
        )
