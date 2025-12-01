"""Configuration management for the summarization agent."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # Ollama settings
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_K_M")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Langfuse settings
    LANGFUSE_PUBLIC_KEY: Optional[str] = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: Optional[str] = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        missing = []
        if not cls.LANGFUSE_PUBLIC_KEY:
            missing.append("LANGFUSE_PUBLIC_KEY")
        if not cls.LANGFUSE_SECRET_KEY:
            missing.append("LANGFUSE_SECRET_KEY")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Please set them in your .env file or environment."
            )


# Global config instance
config = Config()

