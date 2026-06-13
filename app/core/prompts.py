SYSTEM_PROMPT = """
You are a helpful research assistant.
Answer the user's question using ONLY the provided context.
If the answer is not present in the context, say exactly: 'I could not find that information in the uploaded documents.'
Do not use your own external knowledge. Always be concise and factual.
""".strip()

def build_rag_prompt(question: str, context: str) -> str:
    return f"""
Use the following context to answer the question at the end.

Context:
{context}

Question:
{question}

Answer:
""".strip()