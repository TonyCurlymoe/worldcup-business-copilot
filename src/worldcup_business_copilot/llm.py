from openai import OpenAI
from .config import settings


def generate_ai_report(team: dict) -> str:
    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
        return fallback_report(team)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
You are a sports business analyst.

Analyze this World Cup team using the data below:
{team}

Please include:
1. Team performance summary
2. Business value analysis
3. Sponsor and brand impact
4. Risk factors
5. Next match outlook

Use clear, simple business English. Do not invent exact facts not shown in the data.
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are a professional sports business analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response.choices[0].message.content or "No report generated."


def fallback_report(team: dict) -> str:
    return f"""
### AI Report Preview: {team['team']}

**Performance Summary:** {team['team']} has a performance score of {team['performance_score']} and an advancement probability of {team['advancement_probability']}%.

**Business Value:** Its business value score is {team['business_value_score']:.1f}. This reflects market size, star power, social media heat, sponsor exposure, performance, and tournament outlook.

**Sponsor Impact:** Sponsor exposure is {team['sponsor_exposure']}, which suggests the team can create meaningful brand visibility during the tournament.

**Risk Factors:** Main risks include early elimination, weak match performance, injury to star players, or reduced media attention.

**Next Outlook:** Recent result: {team.get('recent_result', 'N/A')}. If the team continues to advance, its commercial value is likely to increase.

_Add OPENAI_API_KEY to .env to generate a richer AI report._
"""
