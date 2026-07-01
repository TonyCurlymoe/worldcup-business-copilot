from openai import OpenAI

from src.core.config import Settings
from src.models.schemas import AnalysisResponse


class OpenAIAnalysisService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def analyze(self, prompt: str) -> AnalysisResponse:
        if not self.client:
            return AnalysisResponse(
                summary=f"Demo analysis: {prompt[:180]}",
                risks=["Live AI analysis requires OPENAI_API_KEY.", "Forecasts should be validated against current match and market data."],
                opportunities=["Use audience segmentation to optimize sponsor placements.", "Compare team momentum with brand exposure benchmarks."],
                confidence=0.72,
            )
        response = self.client.responses.create(
            model=self.settings.openai_model,
            input=(
                "Return concise executive business intelligence for World Cup stakeholders. "
                f"Include risks and opportunities. Prompt: {prompt}"
            ),
        )
        return AnalysisResponse(
            summary=response.output_text,
            risks=["Model output requires human review before commercial decisions."],
            opportunities=["Operationalize insights in sponsorship and media planning workflows."],
            confidence=0.86,
        )
