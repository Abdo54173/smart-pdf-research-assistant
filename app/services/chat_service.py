from groq import Groq
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT, build_rag_prompt
from app.services.retriever_service import RetrieverService

class ChatService:

    def __init__(
        self,
        retriever_service: RetrieverService,
    ) -> None:

        self.retriever_service = retriever_service

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def ask(
        self,
        file_id: str,
        question: str,
        top_k: int = 5,
    ) -> dict:
        
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        retrieval_result = self.retriever_service.retrieve(
            file_id=file_id,
            query=question,
            top_k=top_k,
        )

        if not retrieval_result.get("documents") or not retrieval_result["documents"][0]:
            return {
                "answer": "I could not find that information in the uploaded documents.",
                "sources": []
            }

        documents = retrieval_result["documents"][0]
        metadatas = retrieval_result["metadatas"][0]

        context = "\n\n".join(documents)

        prompt = build_rag_prompt(
            question=question,
            context=context,
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to generate answer: {e}"
            )

        return {
            "answer": response.choices[0].message.content,
            "sources": metadatas,
        }