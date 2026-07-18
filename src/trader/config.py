import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    data_dir: Path = Path(os.getenv("TRADER_DATA_DIR", "data"))
    model_id: str = os.getenv("MODEL_ID", "gpt-4.1-mini")
    model_provider: str = os.getenv("MODEL_PROVIDER", "openai")
    aws_region: str = os.getenv("AWS_REGION", "us-west-2")
    storage_backend: str = os.getenv("STORAGE_BACKEND", "sqlite")
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE", "strands-trader-state")
    run_every_minutes: int = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
    run_when_closed: bool = os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "false").lower() == "true"
    massive_api_key: str | None = os.getenv("MASSIVE_API_KEY")
    tavily_api_key: str | None = os.getenv("TAVILY_API_KEY")
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID")

    @property
    def database_path(self) -> Path:
        return self.data_dir / "accounts.db"


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
