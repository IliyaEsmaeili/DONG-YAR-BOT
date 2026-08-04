from repositories import execute_query
from pathlib import Path
execute_query(Path("schema.sql").read_text() , None)