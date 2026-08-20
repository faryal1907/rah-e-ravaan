from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://rah_e_ravaan:password@postgres:5432/rah_e_ravaan",
        description="PostgreSQL database connection URL"
    )
    postgres_user: str = Field(default="rah_e_ravaan", description="PostgreSQL username")
    postgres_password: str = Field(default="password", description="PostgreSQL password")
    postgres_db: str = Field(default="rah_e_ravaan", description="PostgreSQL database name")
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://redis:6379/0",
        description="Redis connection URL"
    )
    
    # Qdrant Configuration
    qdrant_url: str = Field(
        default="http://qdrant:6333",
        description="Qdrant vector database URL"
    )
    qdrant_api_key: Optional[str] = Field(
        default=None,
        description="Qdrant API key (optional)"
    )
    
    # Backend Configuration
    debug: bool = Field(default=True, description="Debug mode")
    
    # Add backend host and port for docker-compose compatibility
    backend_host: str = Field(default="0.0.0.0", description="Backend host")
    backend_port: int = Field(default=8000, description="Backend port")
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for cryptographic operations"
    )
    
    # API Keys
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    # Optional Configuration
    log_level: str = Field(default="info", description="Logging level")
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="CORS allowed origins (comma-separated)"
    )
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate that secret key is not the default in production."""
        # This validator will be called after all fields are set
        # We'll check the actual instance value in a model_validator instead
        return v
    
    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Validate settings that are critical for production."""
        # Only validate if explicitly in production mode
        if not self.debug and self.secret_key == "dev-secret-key-change-in-production":
            raise ValueError(
                "SECRET_KEY must be changed from the default value in production"
            )
        return self
    

    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the application settings instance."""
    return settings