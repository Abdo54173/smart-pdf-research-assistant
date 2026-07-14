from groq import Groq

from app.core.config import settings
from app.llms.base import BaseLLM

class GroqLLM(BaseLLM):

    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )
    
    def generate(
        self,
        messages: list[dict],
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL_NAME,
            messages=messages,
            temperature=0,
        )

        return response.choices[0].message.content 