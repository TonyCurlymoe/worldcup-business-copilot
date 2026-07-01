from src.models.schemas import TeamBusinessValue

TEAMS = [
    TeamBusinessValue(team="Brazil", fifa_rank=5, marketability_index=96, social_reach_millions=255, sponsor_portfolio_value_musd=410, recent_form_points=13, business_value_score=94.2),
    TeamBusinessValue(team="France", fifa_rank=2, marketability_index=93, social_reach_millions=180, sponsor_portfolio_value_musd=385, recent_form_points=15, business_value_score=91.7),
    TeamBusinessValue(team="Argentina", fifa_rank=1, marketability_index=98, social_reach_millions=220, sponsor_portfolio_value_musd=390, recent_form_points=14, business_value_score=95.1),
    TeamBusinessValue(team="England", fifa_rank=4, marketability_index=94, social_reach_millions=170, sponsor_portfolio_value_musd=420, recent_form_points=12, business_value_score=90.4),
    TeamBusinessValue(team="United States", fifa_rank=11, marketability_index=88, social_reach_millions=95, sponsor_portfolio_value_musd=360, recent_form_points=10, business_value_score=84.6),
]

MATCHES = [
    {"home": "Brazil", "away": "France", "venue": "MetLife Stadium", "expected_viewers_millions": 145},
    {"home": "Argentina", "away": "England", "venue": "AT&T Stadium", "expected_viewers_millions": 138},
    {"home": "United States", "away": "Brazil", "venue": "SoFi Stadium", "expected_viewers_millions": 120},
]
