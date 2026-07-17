from typing import Any, Mapping

from openai import OpenAI

from .config import settings


def _investment_rating(score: float) -> tuple[int, str]:
    """Convert the business value score into a five-star rating."""

    if score >= 90:
        return 5, "Excellent"
    if score >= 85:
        return 4, "Strong"
    if score >= 75:
        return 3, "Moderate"
    if score >= 65:
        return 2, "Cautious"

    return 1, "High Risk"


def _recommended_sectors(team: Mapping[str, Any]) -> list[str]:
    """Recommend sponsorship sectors based on the team profile."""

    sectors = []

    if team["market_size"] >= 90:
        sectors.extend(
            [
                "Global consumer brands",
                "Financial services",
                "Airlines and travel",
            ]
        )

    if team["star_power"] >= 90:
        sectors.extend(
            [
                "Luxury brands",
                "Sportswear",
                "Premium automobiles",
            ]
        )

    if team["social_media_heat"] >= 90:
        sectors.extend(
            [
                "Technology",
                "Gaming",
                "Digital media",
            ]
        )

    if team["sponsor_exposure"] >= 90:
        sectors.extend(
            [
                "Payment platforms",
                "Telecommunications",
                "International retail",
            ]
        )

    if not sectors:
        sectors = [
            "Regional retail",
            "Sportswear",
            "Local media",
        ]

    # Remove duplicates while preserving the original order.
    return list(dict.fromkeys(sectors))


def _commercial_risks(team: Mapping[str, Any]) -> list[str]:
    """Generate commercial risks from the team metrics."""

    risks = []

    if team["advancement_probability"] < 70:
        risks.append(
            "Tournament elimination could reduce media exposure and campaign duration."
        )

    if team["social_media_heat"] < 80:
        risks.append(
            "Digital fan engagement is below the leading commercial teams."
        )

    if team["sponsor_exposure"] < 80:
        risks.append(
            "Current sponsorship visibility may limit short-term brand reach."
        )

    if team["performance_score"] < 80:
        risks.append(
            "Inconsistent sporting performance could create brand-value volatility."
        )

    if not risks:
        risks.append(
            "The team currently has a relatively low commercial-risk profile, "
            "although tournament performance should still be monitored."
        )

    return risks


def generate_ai_report(team: Mapping[str, Any]) -> str:
    """
    Generate an offline, rule-based business report.

    The function name is retained so the application can later replace
    the internal logic with an AI API without changing app.py.
    """

    business_score = float(team["business_value_score"])
    rating, rating_label = _investment_rating(business_score)
    stars = "★" * rating + "☆" * (5 - rating)

    sectors = _recommended_sectors(team)
    risks = _commercial_risks(team)

    strengths = sorted(
        [
            ("Market size", float(team["market_size"])),
            ("Star power", float(team["star_power"])),
            ("Social media heat", float(team["social_media_heat"])),
            ("Sponsor exposure", float(team["sponsor_exposure"])),
            ("Performance", float(team["performance_score"])),
            (
                "Advancement probability",
                float(team["advancement_probability"]),
            ),
        ],
        key=lambda item: item[1],
        reverse=True,
    )[:3]

    strength_lines = "\n".join(
        f"- **{name}:** {value:.0f}" for name, value in strengths
    )

    sector_lines = "\n".join(f"- {sector}" for sector in sectors[:6])
    risk_lines = "\n".join(f"- {risk}" for risk in risks)

    return f"""
# {team["team"]} Commercial Intelligence Report

## Executive Summary

{team["team"]} has a business value score of **{business_score:.1f}**.
Its commercial position is supported by market reach, player recognition,
sponsorship exposure, digital engagement, tournament performance, and an
advancement probability of **{team["advancement_probability"]}%**.

The team's most recent recorded result is **{team["recent_result"]}**.

## Investment Rating

**{stars} — {rating_label}**

## Key Commercial Strengths

{strength_lines}

## Sponsorship Opportunities

The following sectors appear most aligned with the team's current profile:

{sector_lines}

## Fan Engagement Strategy

- Build short-form campaigns around the team's most recognizable players.
- Use match results and tournament milestones for real-time social content.
- Develop multilingual campaigns for high-value international markets.
- Combine sponsor promotions with interactive fan experiences.
- Track social engagement and tournament progress throughout the competition.

## Commercial Risks

{risk_lines}

## Recommended Action

{"Prioritize the team for major multinational sponsorship campaigns."
if rating >= 4
else "Consider a targeted or regional sponsorship strategy with controlled investment."}

This report was generated locally from the dashboard's scoring rules and
currently does not use a paid external AI API.
""".strip()


def answer_business_question(
    team: Mapping[str, Any],
    question: str,
) -> str:
    """Answer common business questions without using an external AI API."""

    question_lower = question.strip().lower()
    team_name = str(team["team"])
    business_score = float(team["business_value_score"])
    sponsor_exposure = float(team["sponsor_exposure"])
    star_power = float(team["star_power"])
    social_heat = float(team["social_media_heat"])
    performance = float(team["performance_score"])
    advancement = float(team["advancement_probability"])

    if not question_lower:
        return "Please enter a business question."

    if any(
        word in question_lower
        for word in ["sponsor", "sponsorship", "brand", "adidas", "nike"]
    ):
        if sponsor_exposure >= 90 and business_score >= 85:
            return (
                f"{team_name} is a strong sponsorship candidate. "
                f"Its sponsor exposure score is {sponsor_exposure:.0f}, "
                f"and its overall business value score is {business_score:.1f}. "
                "A multinational sponsorship campaign could focus on global "
                "visibility, star players, match-day content, and digital fan engagement."
            )

        return (
            f"{team_name} may be better suited to a targeted sponsorship strategy. "
            "The sponsor should begin with regional or digital campaigns and expand "
            "investment if tournament exposure and fan engagement improve."
        )

    if any(
        phrase in question_lower
        for phrase in ["how valuable", "business value", "commercial value", "worth"]
    ):
        return (
            f"{team_name} has a business value score of {business_score:.1f}. "
            f"Its main commercial drivers include star power ({star_power:.0f}), "
            f"sponsor exposure ({sponsor_exposure:.0f}), social media heat "
            f"({social_heat:.0f}), and performance ({performance:.0f})."
        )

    if any(
        phrase in question_lower
        for phrase in ["risk", "weakness", "concern", "problem"]
    ):
        risks = []

        if advancement < 70:
            risks.append("a meaningful risk of early tournament elimination")
        if social_heat < 80:
            risks.append("weaker digital fan engagement")
        if sponsor_exposure < 80:
            risks.append("limited current sponsorship visibility")
        if performance < 80:
            risks.append("performance-related brand volatility")

        if not risks:
            return (
                f"{team_name} currently has a relatively low commercial-risk profile. "
                "The main remaining uncertainty is how tournament results may affect "
                "media exposure and sponsor returns."
            )

        return (
            f"The main commercial concerns for {team_name} are "
            + ", ".join(risks)
            + "."
        )

    if any(
        phrase in question_lower
        for phrase in ["social media", "fan engagement", "digital", "fans"]
    ):
        return (
            f"{team_name} has a social media heat score of {social_heat:.0f}. "
            "Recommended actions include short-form player content, multilingual "
            "campaigns, live match reactions, sponsor-linked fan challenges, and "
            "interactive voting or prediction features."
        )

    if any(
        phrase in question_lower
        for phrase in ["investment", "invest", "recommend"]
    ):
        if business_score >= 90:
            recommendation = "a high-priority commercial investment"
        elif business_score >= 85:
            recommendation = "a strong investment opportunity"
        elif business_score >= 75:
            recommendation = "a selective investment opportunity"
        else:
            recommendation = "a higher-risk commercial opportunity"

        return (
            f"{team_name} is currently {recommendation}. "
            f"The business value score is {business_score:.1f}, and the advancement "
            f"probability is {advancement:.0f}%. Investment size should still be "
            "adjusted as tournament performance changes."
        )

    if any(
        phrase in question_lower
        for phrase in ["strength", "best", "advantage"]
    ):
        metrics = {
            "market size": float(team["market_size"]),
            "star power": star_power,
            "social media heat": social_heat,
            "sponsor exposure": sponsor_exposure,
            "performance": performance,
            "advancement probability": advancement,
        }

        top_metrics = sorted(
            metrics.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:3]

        formatted = ", ".join(
            f"{name} ({value:.0f})"
            for name, value in top_metrics
        )

        return f"{team_name}'s strongest commercial drivers are {formatted}."

    return (
        f"Based on the current dashboard data, {team_name} has a business value "
        f"score of {business_score:.1f}, sponsor exposure of "
        f"{sponsor_exposure:.0f}, and an advancement probability of "
        f"{advancement:.0f}%. Try asking about sponsorship, risks, investment, "
        "fan engagement, strengths, or commercial value."
    )

def answer_business_question_with_ai(
    team: Mapping[str, Any],
    question: str,
) -> tuple[str, str]:
    """
    Answer with OpenAI when an API key is available.

    Returns:
        A tuple containing the answer and the mode used:
        ("answer text", "AI") or ("answer text", "Offline")
    """

    if not settings.openai_api_key:
        return answer_business_question(team, question), "Offline"

    team_context = f"""
Team: {team["team"]}
Region: {team["region"]}
Business value score: {float(team["business_value_score"]):.1f}
Market size: {float(team["market_size"]):.0f}
Star power: {float(team["star_power"]):.0f}
Social media heat: {float(team["social_media_heat"]):.0f}
Sponsor exposure: {float(team["sponsor_exposure"]):.0f}
Performance score: {float(team["performance_score"]):.0f}
Advancement probability: {float(team["advancement_probability"]):.0f}%
Recent result: {team["recent_result"]}
""".strip()

    instructions = """
You are a World Cup business intelligence consultant.

Answer the user's question using only the supplied team data.

Focus on:
- sponsorship potential
- commercial value
- fan engagement
- brand exposure
- investment risk
- tournament-performance risk

Requirements:
- Use a professional but readable tone.
- Be concise.
- Explain the recommendation with evidence from the metrics.
- Do not invent players, financial values, contracts, or match results.
- Clearly distinguish facts from recommendations.
""".strip()

    prompt = f"""
Team data:
{team_context}

User question:
{question}
""".strip()

    try:
        client = OpenAI(api_key=settings.openai_api_key)

        response = client.responses.create(
            model=settings.openai_model,
            instructions=instructions,
            input=prompt,
            store=False,
        )

        answer = response.output_text.strip()

        if not answer:
            raise ValueError("The AI response was empty.")

        return answer, "AI"

    except Exception:
        fallback = answer_business_question(team, question)

        return (
            fallback
            + "\n\n"
            + "_AI mode was unavailable, so this answer was generated "
            + "using the offline business rules._"
        ), "Offline"