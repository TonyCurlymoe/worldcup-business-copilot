"""Business value model for the Streamlit MVP."""

from __future__ import annotations

from typing import Any

METRICS = [
    "market_size",
    "star_power",
    "social_media_heat",
    "sponsor_exposure",
    "performance_score",
    "advancement_probability",
]

TEAM_DATA: list[dict[str, Any]] = [
    {"team": "Argentina", "region": "CONMEBOL", "market_size": 87, "star_power": 98, "social_media_heat": 96, "sponsor_exposure": 92, "performance_score": 95, "advancement_probability": 88, "profile": "Defending champion brand equity, elite global stars, and a massive international fan base."},
    {"team": "Brazil", "region": "CONMEBOL", "market_size": 92, "star_power": 96, "social_media_heat": 97, "sponsor_exposure": 94, "performance_score": 90, "advancement_probability": 86, "profile": "Iconic football identity with premium sponsor fit and consistently high global attention."},
    {"team": "France", "region": "UEFA", "market_size": 88, "star_power": 95, "social_media_heat": 90, "sponsor_exposure": 91, "performance_score": 93, "advancement_probability": 87, "profile": "Deep squad quality and luxury-market alignment create strong commercial upside."},
    {"team": "England", "region": "UEFA", "market_size": 94, "star_power": 91, "social_media_heat": 89, "sponsor_exposure": 93, "performance_score": 88, "advancement_probability": 82, "profile": "High-value media market, strong league halo effect, and broad sponsor demand."},
    {"team": "USA", "region": "CONCACAF", "market_size": 96, "star_power": 78, "social_media_heat": 84, "sponsor_exposure": 90, "performance_score": 76, "advancement_probability": 68, "profile": "Host-market scale and brand-safe sponsorship inventory make the USA a business growth story."},
    {"team": "Mexico", "region": "CONCACAF", "market_size": 86, "star_power": 76, "social_media_heat": 88, "sponsor_exposure": 85, "performance_score": 74, "advancement_probability": 64, "profile": "Passionate cross-border fan base and reliable merchandise demand support strong activations."},
    {"team": "Germany", "region": "UEFA", "market_size": 90, "star_power": 82, "social_media_heat": 80, "sponsor_exposure": 88, "performance_score": 84, "advancement_probability": 75, "profile": "Premium economy, heritage brand, and disciplined performance profile attract blue-chip partners."},
    {"team": "Portugal", "region": "UEFA", "market_size": 78, "star_power": 94, "social_media_heat": 93, "sponsor_exposure": 86, "performance_score": 85, "advancement_probability": 77, "profile": "Star-led attention and high digital engagement create outsized value relative to market size."},
]


def calculate_business_value_score(team: dict[str, Any]) -> float:
    """Calculate the transparent MVP business value score as an average of six metrics."""
    return round(sum(float(team[metric]) for metric in METRICS) / len(METRICS), 1)


def build_ranked_team_records() -> list[dict[str, Any]]:
    """Return sample teams with business scores and ranks."""
    scored = [{**team, "business_value_score": calculate_business_value_score(team)} for team in TEAM_DATA]
    scored.sort(key=lambda team: team["business_value_score"], reverse=True)
    for index, team in enumerate(scored, start=1):
        team["rank"] = index
    return scored


def generate_business_report(team: dict[str, Any]) -> str:
    """Generate an AI-style business report without external AI dependencies."""
    strongest_metric = max(METRICS, key=lambda metric: team[metric])
    weakest_metric = min(METRICS, key=lambda metric: team[metric])
    return f"""
### AI-Style Business Report: {team['team']}

**Executive summary:** {team['team']} has a business value score of **{team['business_value_score']}**,
placing it at rank **#{team['rank']}** in this MVP model. The team is strongest in
**{strongest_metric.replace('_', ' ')}** and has the most room to improve in
**{weakest_metric.replace('_', ' ')}**.

**Commercial outlook:** {team['profile']} Sponsors should prioritize campaigns that connect fan passion,
player storytelling, and matchday momentum. If the team advances deeper into the tournament, brand exposure,
earned media, and retail conversion are likely to increase.

**Recommended actions:**
- Build short-form content around star players and national identity.
- Reserve flexible media budget for knockout-stage acceleration.
- Pair local market activations with global social campaigns.
- Track weekly movement in sponsor exposure and advancement probability.
"""
