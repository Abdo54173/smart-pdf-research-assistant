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
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )

        return response.choices[0].message.content 