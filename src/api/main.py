from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import Settings, get_settings
from src.models.schemas import AnalysisResponse, MatchAnalysisRequest, SponsorImpactRequest
from src.services.football_data import FootballDataService
from src.services.news import NewsRetrievalService
from src.services.openai_service import OpenAIAnalysisService

app = FastAPI(title="World Cup Business Intelligence Copilot", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def football_service(settings: Settings = Depends(get_settings)) -> FootballDataService:
    return FootballDataService(settings)


@app.get("/health")
def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/dashboard")
async def dashboard(service: FootballDataService = Depends(football_service)) -> dict:
    return {"teams": [team.model_dump() for team in await service.teams()], "matches": await service.matches()}


@app.post("/analysis/match", response_model=AnalysisResponse)
def match_analysis(request: MatchAnalysisRequest, settings: Settings = Depends(get_settings)) -> AnalysisResponse:
    prompt = f"Analyze {request.home_team} vs {request.away_team}. Context: {request.context or 'World Cup commercial impact.'}"
    return OpenAIAnalysisService(settings).analyze(prompt)


@app.post("/analysis/sponsor", response_model=AnalysisResponse)
def sponsor_analysis(request: SponsorImpactRequest, settings: Settings = Depends(get_settings)) -> AnalysisResponse:
    prompt = f"Sponsor {request.sponsor} invests ${request.campaign_budget_musd}M with {request.team}. Estimate brand, media, and downside impact."
    return OpenAIAnalysisService(settings).analyze(prompt)


@app.get("/news")
async def news(query: str = "World Cup business sponsors", settings: Settings = Depends(get_settings)):
    return [article.model_dump() for article in await NewsRetrievalService(settings).search(query)]
