from src.business_value import METRICS, build_ranked_team_records, generate_business_report


def test_team_records_contain_required_teams():
    teams = build_ranked_team_records()
    assert {team["team"] for team in teams} == {"Argentina", "Brazil", "France", "England", "USA", "Mexico", "Germany", "Portugal"}


def test_business_value_score_is_metric_average():
    teams = build_ranked_team_records()
    argentina = next(team for team in teams if team["team"] == "Argentina")
    expected = round(sum(argentina[metric] for metric in METRICS) / len(METRICS), 1)
    assert argentina["business_value_score"] == expected


def test_business_report_is_template_generated():
    team = build_ranked_team_records()[0]
    report = generate_business_report(team)
    assert team["team"] in report
    assert "Recommended actions" in report
