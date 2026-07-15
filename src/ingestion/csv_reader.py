from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger()


def read_csv(file_path: Path) -> pd.DataFrame:
    """Read a single batch CSV and normalise column names."""

    logger.info("Reading source CSV: {}", file_path)

    if not file_path.exists():
        logger.error("CSV file not found: {}", file_path)
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        dataframe = pd.read_csv(file_path)
        dataframe.columns = (
            dataframe.columns
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
            .str.replace(".", "_")
        )

        logger.info(
            "CSV loaded | rows={} | columns={}",
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe

    except Exception as error:
        logger.exception("Failed to read CSV file.")
        raise RuntimeError("Unable to read source CSV.") from error
