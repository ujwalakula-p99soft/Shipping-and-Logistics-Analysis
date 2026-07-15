from __future__ import annotations

import json
from typing import Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger()


def get_secret() -> Dict[str, str]:

    logger.info("Retrieving Snowflake credentials from AWS Secrets Manager...")

    try:

        kwargs: dict = {
            "service_name": "secretsmanager",
            "region_name":  settings.AWS_REGION,
        }

        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            kwargs["aws_access_key_id"]     = settings.AWS_ACCESS_KEY_ID
            kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

        client = boto3.client(**kwargs)

        response = client.get_secret_value(SecretId=settings.AWS_SECRET_NAME)

        secret = json.loads(response["SecretString"])

        logger.info("Secrets retrieved successfully.")

        return secret

    except (ClientError, BotoCoreError) as error:

        logger.exception("Failed to retrieve secrets from AWS Secrets Manager.")

        raise RuntimeError("Unable to retrieve AWS Secrets.") from error
