from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router
from app.api.health import router as health_router
from app.api.pdf import router as pdf_router

app = FastAPI(
    title="Smart PDF Research Assistant",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(pdf_router)
app.include_router(chat_router)
app.include_router(conversation_router)


@app.get("/")
async def root():
    return {
        "message": "Smart PDF Research Assistant API is running"
    }