from pydantic import BaseModel, Field


class TeamBusinessValue(BaseModel):
    team: str
    fifa_rank: int = Field(ge=1)
    marketability_index: float = Field(ge=0, le=100)
    social_reach_millions: float = Field(ge=0)
    sponsor_portfolio_value_musd: float = Field(ge=0)
    recent_form_points: int = Field(ge=0)
    business_value_score: float = Field(ge=0, le=100)


class MatchAnalysisRequest(BaseModel):
    home_team: str
    away_team: str
    context: str | None = None


class SponsorImpactRequest(BaseModel):
    sponsor: str
    team: str
    campaign_budget_musd: float = Field(gt=0)


class AnalysisResponse(BaseModel):
    summary: str
    risks: list[str]
    opportunities: list[str]
    confidence: float = Field(ge=0, le=1)


class NewsArticle(BaseModel):
    title: str
    source: str
    url: str
    summary: str
