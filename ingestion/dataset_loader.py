""" 
Load data after catalogue_reader.py has 
validated it's existence and structure.


Base on type in catalogue: Table, Document, Log
check if data source is reachable and data structure is as expected
(e.g., columns for Table, text for Document, patterns for Log).

Triggers lineage tracking on successful data load.

Returns data in a format ready for further processing.
"""