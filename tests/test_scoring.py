import pandas as pd
from src.worldcup_business_copilot.data import add_business_value_score


def test_business_value_score_exists():
    df = pd.DataFrame([
        {
            "market_size": 100,
            "star_power": 100,
            "social_media_heat": 100,
            "sponsor_exposure": 100,
            "performance_score": 100,
            "advancement_probability": 100,
        }
    ])
    result = add_business_value_score(df)
    assert result.loc[0, "business_value_score"] == 100
