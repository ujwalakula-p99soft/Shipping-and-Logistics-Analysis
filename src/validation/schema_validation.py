from __future__ import annotations

import pandas as pd

from src.config.constants import REQUIRED_COLUMNS
from src.utils.logger import (
    get_logger,
    get_quality_logger,
)

logger = get_logger()
quality_logger = get_quality_logger()


def validate_schema(dataframe: pd.DataFrame) -> bool:

    logger.info("Starting schema validation.")

    if dataframe.empty:

        logger.error("Dataset is empty.")

        raise ValueError("Dataset is empty.")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:

        logger.error(
            "Missing required columns: {}",
            ", ".join(missing_columns),
        )

        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("Schema validation completed successfully.")

    quality_logger.info("Schema Validation : PASSED")

    return True
