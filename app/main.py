from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.pdf import router as pdf_router

app = FastAPI(title="Smart PDF Research Assistant")

app.include_router(health_router)
app.include_router(pdf_router)