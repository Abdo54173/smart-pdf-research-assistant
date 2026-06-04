# from fastapi import FastAPI
# from app.api.health import router as health_router
# from app.api.pdf import router as pdf_router

# app = FastAPI(title="Smart PDF Research Assistant")

# app.include_router(health_router)
# app.include_router(pdf_router)

from app.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()

vector = embedding_service.embed_text(
    "What is Retrieval Augmented Generation?"
)

print(len(vector))