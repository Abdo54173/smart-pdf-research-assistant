from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_DB_DIR = DATA_DIR / "vectordb"

class Settings(BaseSettings):
    
    DEFAULT_CHUNK_SIZE: int = 500
    DEFAULT_CHUNK_OVERLAP: int = 50

    EMBEDDING_MODEL_NAME: str = "embed-english-v3.0"
    CHROMA_COLLECTION_NAME: str

    COHERE_API_KEY: str = ""

    LLM_PROVIDER: str = "groq"

    GROQ_API_KEY: str = ""
    GROQ_MODEL_NAME: str = "llama-3.1-8b-instant"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_NAME:str = "gpt-4.1-mini"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()