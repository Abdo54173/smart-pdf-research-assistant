from app.core.config import settings
from app.llms.base import BaseLLM
from app.llms.groq_llm import GroqLLM
from app.llms.openai_llm import OpenAILLM


class LLMFactory:

    @staticmethod
    def create() -> BaseLLM:

        provider = settings.LLM_PROVIDER.lower()

        if provider == "groq":
            return GroqLLM()

        if provider == "openai":
            return OpenAILLM()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )