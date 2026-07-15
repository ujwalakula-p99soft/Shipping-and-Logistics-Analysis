from pathlib import Path

from snowflake.connector import SnowflakeConnection

from src.utils.logger import get_logger

logger = get_logger()

_STAGE = "SHIPPING_DB.BRONZE.RAW_STAGE"


def upload_to_stage(
    connection: SnowflakeConnection,
    file_path: Path,
) -> None:
    """Upload a single batch CSV file to the Snowflake internal stage."""

    resolved = file_path.resolve()
    path_str = resolved.as_posix()

    put_command = (
        f"PUT 'file://{path_str}' "
        f"@{_STAGE} "
        "AUTO_COMPRESS=TRUE "
        "OVERWRITE=TRUE"
    )

    cursor = connection.cursor()

    try:
        logger.info("Uploading {} to @{}...", file_path.name, _STAGE)
        cursor.execute(put_command)
        logger.info("Upload completed.")
    finally:
        cursor.close()
