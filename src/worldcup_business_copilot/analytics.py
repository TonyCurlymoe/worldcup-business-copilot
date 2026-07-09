def generate_business_summary(team: dict) -> str:
    score = team["business_value_score"]
    if score >= 90:
        level = "elite global commercial value"
    elif score >= 80:
        level = "strong commercial value"
    elif score >= 70:
        level = "solid commercial potential"
    else:
        level = "developing commercial potential"

    return (
        f"{team['team']} currently has a business value score of {score:.1f}, which indicates "
        f"{level}. The score is driven by market size, star power, social media heat, sponsor "
        f"exposure, team performance, and advancement probability. Recent result: "
        f"{team.get('recent_result', 'N/A')}."
    )


def identify_strengths(team: dict) -> list[str]:
    metrics = {
        "Market size": team["market_size"],
        "Star power": team["star_power"],
        "Social media heat": team["social_media_heat"],
        "Sponsor exposure": team["sponsor_exposure"],
        "Performance": team["performance_score"],
        "Advancement probability": team["advancement_probability"],
    }
    return [name for name, value in sorted(metrics.items(), key=lambda item: item[1], reverse=True)[:3]]
