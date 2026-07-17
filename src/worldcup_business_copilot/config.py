from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5")
    ai_enabled: bool = bool(os.getenv("OPENAI_API_KEY"))
    data_path: str = os.getenv("TEAM_DATA_PATH", "data/teams.csv")
    historical_data_path: str = os.getenv(
        "HISTORICAL_DATA_PATH",
        "data/historical_world_cup.csv",
    )


settings = Settings()
