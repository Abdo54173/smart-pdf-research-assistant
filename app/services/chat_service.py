from app.core.prompts import SYSTEM_PROMPT, build_rag_prompt
from app.services.retriever_service import RetrieverService
from app.services.conversation_service import ConversationService
from app.llms.base import BaseLLM

class ChatService:

    def __init__(
        self,
        retriever_service: RetrieverService,
        conversation_service: ConversationService,
        llm: BaseLLM,
    ) -> None:

        self.retriever_service = retriever_service
        self.conversation_service = conversation_service
        self.llm = llm

    async def ask(
        self,
        conversation_id: str | None,
        document_ids: list[str] | None,
        question: str,
        top_k: int = 5,
    ) -> dict:
        
        if conversation_id is None:

            conversation = await self.conversation_service.create_conversation(
                title="New Conversation",
                document_ids=document_ids,
            )

            conversation_id = conversation.id
        
        if not question.strip():
            raise ValueError("Question cannot be empty.")
        
        history = await self.conversation_service.get_history(
            conversation_id
        )

        history_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in history
        ]

        document_ids = await self.conversation_service.get_document_ids(
            conversation_id
        )

        retrieval_result = await self.retriever_service.retrieve(
            document_ids=document_ids,
            query=question,
            top_k=top_k,
        )

        if not retrieval_result:
            return {
                "answer": "I could not find that information in the uploaded documents.",
                "sources": [],
            }

        documents = [item["text"] for item in retrieval_result]

        seen = set()
        metadatas = []

        for item in retrieval_result:
            metadata = item["metadata"]

            key = (
                metadata["document_id"],
                metadata["page"],
            )

            if key not in seen:
                seen.add(key)
                metadatas.append(metadata)

        context = "\n\n".join(documents)

        await self.conversation_service.add_message(
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *history_messages,
            {
                "role": "user",
                "content": build_rag_prompt(
                    question=question,
                    context=context,
                ),
            },
        ]

        try:
            answer = self.llm.generate(messages)

        except Exception as e:
            raise RuntimeError(
                f"Failed to generate answer: {e}"
            )

        await self.conversation_service.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        return {
            "conversation_id": conversation_id,
            "answer": answer,
            "sources": [
                {
                    "document_name": metadata["document_name"],
                    "page": metadata["page"],
                }
                for metadata in metadatas
            ],
        }