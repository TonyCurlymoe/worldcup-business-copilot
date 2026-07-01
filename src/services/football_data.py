import httpx

from src.core.config import Settings
from src.services.data import MATCHES, TEAMS


class FootballDataService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def teams(self):
        return TEAMS

    async def matches(self):
        if not self.settings.football_data_api_key:
            return MATCHES
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.get(
                f"{self.settings.football_data_base_url}/competitions/WC/matches",
                headers={"X-Auth-Token": self.settings.football_data_api_key},
            )
            response.raise_for_status()
            return response.json().get("matches", [])
