import httpx

from src.core.config import Settings
from src.models.schemas import NewsArticle

DEMO_NEWS = [
    NewsArticle(title="Sponsors prepare global activations for expanded tournament", source="Demo Wire", url="https://example.com/sponsors", summary="Brands are planning multi-market campaigns around stadium, digital, and fan-zone inventory."),
    NewsArticle(title="Host cities forecast tourism and retail lift", source="Demo Business", url="https://example.com/host-cities", summary="Local businesses expect demand spikes across hospitality, transportation, and merchandise."),
]


class NewsRetrievalService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def search(self, query: str) -> list[NewsArticle]:
        if not self.settings.news_api_key:
            return DEMO_NEWS
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.get(
                f"{self.settings.news_api_base_url}/everything",
                params={"q": query, "language": "en", "sortBy": "publishedAt", "apiKey": self.settings.news_api_key},
            )
            response.raise_for_status()
        return [
            NewsArticle(
                title=item.get("title") or "Untitled",
                source=(item.get("source") or {}).get("name") or "Unknown",
                url=item.get("url") or "",
                summary=item.get("description") or item.get("content") or "No summary available.",
            )
            for item in response.json().get("articles", [])[:10]
        ]
