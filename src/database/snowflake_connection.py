from __future__ import annotations

from contextlib import contextmanager

import snowflake.connector
from snowflake.connector.errors import Error

from src.utils.logger import get_logger
from src.utils.secrets_manager import get_secret

logger = get_logger()


@contextmanager
def get_connection():

    connection = None

    try:

        credentials = get_secret()

        logger.info("Connecting to Snowflake...")

        connection = snowflake.connector.connect(
            user=credentials["user"],
            password=credentials["password"],
            account=credentials["account"],
        )

        logger.info("Snowflake connection established.")

        yield connection

    except Error as error:

        logger.exception("Unable to connect to Snowflake.")

        raise RuntimeError(
            "Snowflake connection failed."
        ) from error

    finally:

        if connection:

            connection.close()

            logger.info("Snowflake connection closed.")
