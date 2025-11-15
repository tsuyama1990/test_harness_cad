from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        DATABASE_URL: The URL for the application's database.
        KICAD_CLI_PATH: The full path to the kicad-cli executable.
    """

    DATABASE_URL: str = "sqlite:///./app/test.db"
    KICAD_CLI_PATH: str = "/usr/bin/kicad-cli"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
