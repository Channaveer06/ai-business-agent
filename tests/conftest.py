# tests/conftest.py

"""
Pytest configuration file.

We add the 'src' directory to sys.path so that imports like
'from agents.report_agent import ReportAgent' work correctly.

This is a common pattern for projects using a 'src' layout.
"""

import sys
from pathlib import Path

# Resolve the project root (one level above 'tests')
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add 'src' to sys.path if it's not already there
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
