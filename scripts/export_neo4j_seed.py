#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from forensic_fincrime_companion.bootstrap import export_neo4j_seed, init_sqlite_demo


if __name__ == "__main__":
    connection = init_sqlite_demo()
    try:
        export_neo4j_seed(connection)
    finally:
        connection.close()
