from dataclasses import dataclass, field
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:

    PROJECT_ROOT: Path = PROJECT_ROOT

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEV")

    AWS_REGION:             str = os.getenv("AWS_REGION",             "")
    AWS_SECRET_NAME:        str = os.getenv("AWS_SECRET_NAME",        "")
    AWS_ACCESS_KEY_ID:      str = os.getenv("AWS_ACCESS_KEY_ID",      "")
    AWS_SECRET_ACCESS_KEY:  str = os.getenv("AWS_SECRET_ACCESS_KEY",  "")

    RAW_DATA_DIR:  Path = PROJECT_ROOT / "data" / "raw"

    LOG_DIRECTORY: Path = PROJECT_ROOT / "logs"
    APPLICATION_LOG: Path = PROJECT_ROOT / os.getenv("APPLICATION_LOG", "logs/application.log")
    QUALITY_LOG:     Path = PROJECT_ROOT / os.getenv("QUALITY_LOG",     "logs/quality.log")

    LOG_LEVEL:     str = os.getenv("LOG_LEVEL",     "INFO")
    LOG_ROTATION:  str = os.getenv("LOG_ROTATION",  "10 MB")
    LOG_RETENTION: str = os.getenv("LOG_RETENTION", "30 days")


settings = Settings()
