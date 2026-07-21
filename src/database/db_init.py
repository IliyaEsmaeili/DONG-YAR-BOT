from repositories import *
from pathlib import Path
execute_query(Path("schema.sql").read_text() , None)