#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from forensic_fincrime_companion.bootstrap import bootstrap_all


if __name__ == "__main__":
    bootstrap_all()
