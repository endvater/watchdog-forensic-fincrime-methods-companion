#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from forensic_fincrime_companion.bootstrap import init_sqlite_demo, run_query_reports


if __name__ == "__main__":
    connection = init_sqlite_demo()
    try:
        run_query_reports(connection)
    finally:
        connection.close()
