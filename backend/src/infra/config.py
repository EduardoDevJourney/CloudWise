from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    database_url: str = "sqlite:///./cloudwise.db"
    secret_key: str = ""
    azure_subscription_id: str = ""
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_client_secret: str = ""
    pulumi_stack: str = "dev"
    pulumi_state_dir: str = "infra/pulumi/.pulumi"
    pulumi_config_passphrase: str = ""
    admin_emails: str = ""  # comma-separated emails
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @model_validator(mode="after")
    def _require_secrets_outside_development(self) -> "Settings":
        if self.app_env == "development":
            self.secret_key = self.secret_key or "dev-secret-key"
            self.pulumi_config_passphrase = self.pulumi_config_passphrase or "cloudwise-dev"
            return self
        for name in ("secret_key", "pulumi_config_passphrase"):
            value = getattr(self, name)
            if not value or value.startswith("change-me"):
                raise ValueError(f"{name.upper()} must be set via environment when APP_ENV != development")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
