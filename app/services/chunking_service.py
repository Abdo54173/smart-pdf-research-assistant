import logging
from typing import List, Dict
import tiktoken
from app.core.config import settings

logger = logging.getLogger(__name__)

class ChunkingService:
    def __init__(self, encoding_name: str = "cl100k_base"):
        try:
            self.tokenizer = tiktoken.get_encoding(encoding_name)
        except Exception as e:
            logger.warning(f"Failed to load tiktoken encoding, falling back to default. Error: {e}")
            self.tokenizer = None

    def chunk_text(
        self,
        text: str,
        chunk_size: int = settings.DEFAULT_CHUNK_SIZE,  
        chunk_overlap: int = settings.DEFAULT_CHUNK_OVERLAP,
    ) -> List[str]:
        
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        if not text or not text.strip():
            return []

        if not self.tokenizer:
            return self._character_chunk_fallback(text, chunk_size * 4, chunk_overlap * 4)

        words = text.split()
        chunks = []
        current_words = []
        current_tokens = 0

        for word in words:

            word_tokens = len(self.tokenizer.encode(" " + word))
            
            if current_tokens + word_tokens > chunk_size:
                if current_words:
                    chunks.append(" ".join(current_words))
                
                overlap_words = []
                overlap_tokens = 0
                for w in reversed(current_words):
                    w_tokens = len(self.tokenizer.encode(" " + w))
                    if overlap_tokens + w_tokens <= chunk_overlap:
                        overlap_words.insert(0, w)
                        overlap_tokens += w_tokens
                    else:
                        break
                
                current_words = overlap_words + [word]
                current_tokens = overlap_tokens + word_tokens
            else:
                current_words.append(word)
                current_tokens += word_tokens

        if current_words:
            chunks.append(" ".join(current_words))

        return chunks

    def chunk_pages(
        self,
        pages: List[Dict],
        chunk_size: int = settings.DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = settings.DEFAULT_CHUNK_OVERLAP,
    ) -> List[Dict]:

        all_chunks = []
        global_chunk_id = 1

        for page in pages:
            page_number = page.get("page")
            page_text = page.get("text", "")

            if not page_text.strip():
                continue

            text_chunks = self.chunk_text(
                text=page_text,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                )

            for chunk_text in text_chunks:
                all_chunks.append(
                    {
                        "chunk_id": global_chunk_id,
                        "page": page_number,
                        "text": chunk_text,
                        "tokens_count": len(self.tokenizer.encode(chunk_text)) if self.tokenizer else len(chunk_text) // 4
                    }
                )
                global_chunk_id += 1
                
        return all_chunks

    def _character_chunk_fallback(self, text: str, size: int, overlap: int) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            start += size - overlap
        return chunks