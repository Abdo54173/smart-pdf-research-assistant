from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self.model.encode(texts).tolist()