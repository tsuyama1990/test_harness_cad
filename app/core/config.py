import yaml
from pathlib import Path
from typing import Any, Dict, Tuple

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

# Define paths
CONFIG_DIR = Path(__file__).parent
APP_DIR = CONFIG_DIR.parent
ROOT_DIR = APP_DIR.parent
CONFIG_YAML_FILE = CONFIG_DIR / "config.yaml"


def yaml_config_settings_source() -> Dict[str, Any]:
    """
    A settings source that loads configuration from a YAML file.
    """
    if CONFIG_YAML_FILE.exists():
        with open(CONFIG_YAML_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


class KiCadSettings(BaseModel):
    cli_command: str
    default_connector: Dict[str, str]


class APISettings(BaseModel):
    default_filenames: Dict[str, str]


class Settings(BaseSettings):
    """
    Main settings object for the application.
    It loads settings from multiple sources:
    1. YAML configuration file (`config.yaml`)
    2. Environment variables (and .env file)
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Environment-specific settings
    PROJECT_NAME: str = "KiCad Harness SaaS"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./test.db"

    # Static settings from YAML
    kicad: KiCadSettings
    api: APISettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            yaml_config_settings_source,
            file_secret_settings,
        )


settings = Settings()
