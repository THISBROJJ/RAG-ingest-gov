"""

Handles tracking of data lineage during ingestion.
Tracks the origin, movement, and transformation of data as it 
flows through the ingestion pipeline via. appending to a lineage log
object (in my lineage folder) or database.

Is triggered by dataset_loader.py upon successful data load.

Resources to consider:
- OpenLineage (https://openlineage.io/)

"""