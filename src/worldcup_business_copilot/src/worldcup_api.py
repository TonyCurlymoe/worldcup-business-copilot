import pandas as pd


def fetch_worldcup_matches():
    """
    Temporary stable match dataset for MVP v2.
    Later we will replace this with a real football API.
    """
    matches = [
        {
            "date": "2026-06-22",
            "team_a": "Argentina",
            "team_b": "Austria",
            "score": "2-0",
            "winner": "Argentina",
            "stage": "Group J",
        },
        {
            "date": "2026-06-22",
            "team_a": "France",
            "team_b": "Iraq",
            "score": "3-0",
            "winner": "France",
            "stage": "Group I",
        },
        {
            "date": "2026-06-23",
            "team_a": "Portugal",
            "team_b": "Uzbekistan",
            "score": "5-0",
            "winner": "Portugal",
            "stage": "Group K",
        },
        {
            "date": "2026-06-21",
            "team_a": "Spain",
            "team_b": "Saudi Arabia",
            "score": "4-0",
            "winner": "Spain",
            "stage": "Group H",
        },
    ]

    return pd.DataFrame(matches)