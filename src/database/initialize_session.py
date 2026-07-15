from snowflake.connector import SnowflakeConnection
from snowflake.connector.errors import Error

from src.config.constants import (
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_ROLE,
    SNOWFLAKE_WAREHOUSE,
)
from src.utils.logger import get_logger

logger = get_logger()


def initialize_session(connection: SnowflakeConnection) -> None:
    """Set role, resume + use warehouse, and use database.
    No USE SCHEMA — all SQL uses fully qualified names."""

    logger.info("Initializing Snowflake session...")

    cursor = connection.cursor()

    try:
        cursor.execute(f"USE ROLE {SNOWFLAKE_ROLE}")
        logger.info("Role      : {}", SNOWFLAKE_ROLE)

        cursor.execute(f"ALTER WAREHOUSE {SNOWFLAKE_WAREHOUSE} RESUME IF SUSPENDED")
        cursor.execute(f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE}")
        logger.info("Warehouse : {}", SNOWFLAKE_WAREHOUSE)

        cursor.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
        logger.info("Database  : {}", SNOWFLAKE_DATABASE)

        logger.info("Snowflake session ready.")

    except Error as error:
        logger.exception("Failed to initialize Snowflake session.")
        raise RuntimeError("Snowflake session initialization failed.") from error

    finally:
        cursor.close()
