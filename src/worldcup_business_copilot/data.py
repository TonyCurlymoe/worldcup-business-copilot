from pathlib import Path
import pandas as pd

WEIGHTS = {
    "market_size": 0.20,
    "star_power": 0.20,
    "social_media_heat": 0.20,
    "sponsor_exposure": 0.20,
    "performance_score": 0.10,
    "advancement_probability": 0.10,
}


def load_team_data(path: str = "data/teams.csv") -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Cannot find data file: {csv_path}")

    df = pd.read_csv(csv_path)
    return add_business_value_score(df)


def add_business_value_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    score = 0
    for col, weight in WEIGHTS.items():
        score += df[col] * weight
    df["business_value_score"] = score.round(1)
    return df


def get_team_profile(df: pd.DataFrame, team: str) -> dict:
    matched = df[df["team"] == team]
    if matched.empty:
        raise ValueError(f"Team not found: {team}")
    return matched.iloc[0].to_dict()

def load_historical_world_cup_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)