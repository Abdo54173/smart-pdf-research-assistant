from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT, build_rag_prompt
from app.services.retriever_service import RetrieverService
from app.llms.factory import LLMFactory

class ChatService:

    def __init__(
        self,
        retriever_service: RetrieverService,
    ) -> None:

        self.retriever_service = retriever_service
        self.llm = LLMFactory.create()

    def ask(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
    ) -> dict:
        
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        retrieval_result = self.retriever_service.retrieve(
            document_id=document_id,
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
            answer = self.llm.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to generate answer: {e}"
            )

        return {
            "answer": answer,
            "sources": metadatas,
        }