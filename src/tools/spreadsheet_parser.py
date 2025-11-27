# src/tools/spreadsheet_parser.py

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

class SpreadsheetTool:
    """
    Tool for reading CSV files into a pandas DataFrame.
    Agents can use this to analyze business data.
    """

    def read_csv(self, file_path: str) -> pd.DataFrame:
        """
        Reads a CSV file and returns a pandas DataFrame.
        """

        path = Path(file_path)
        logger.info("Reading CSV file: %s", path)

        if not path.exists():
            logger.error("CSV file not found: %s", path)
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(path)

        if df.empty:
            logger.warning("CSV file is empty: %s", path)
            raise ValueError(f"CSV file is empty: {file_path}")

        logger.info("CSV read successfully with %d rows and %d columns", *df.shape)
        return df
