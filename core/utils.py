from django.conf import settings
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

model = GeminiModel(
    settings.AI_MODEL, provider=GoogleGLAProvider(api_key=settings.AI_API_KEY)
)


class ContentSafetyResponse(BaseModel):
    is_safe: bool


def is_safe_content(content):
    """
    Returns a boolean indicating if the content is safe.
    """
    agent = Agent(
        model,
        output_type=ContentSafetyResponse,
        system_prompt="You are a content safety model. Your task is to determine if the content is safe or not.",
    )
    response = agent.run_sync(content)
    return response.output.is_safe
