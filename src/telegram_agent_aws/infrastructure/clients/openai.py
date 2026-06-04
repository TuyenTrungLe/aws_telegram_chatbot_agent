from functools import lru_cache

from openai import OpenAI

from telegram_agent_aws.config import settings


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """
    Get or create an OpenAI-compatible client singleton.
    The client is created once and cached for subsequent calls.
    """
    return OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
