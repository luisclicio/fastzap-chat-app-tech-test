from django.conf import settings
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    "google/gemini-2.0-flash-exp:free",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
    ),
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
