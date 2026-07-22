import requests

from config import API_BASE_URL


def upload_pdf(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/pdf/upload",
        files=files,
    )

    response.raise_for_status()
    return response.json()


def ask_question(
    conversation_id: str,
    question: str,
):
    response = requests.post(
        f"{API_BASE_URL}/chat/ask",
        json={
            "conversation_id": conversation_id,
            "question": question,
        },
    )

    response.raise_for_status()
    return response.json()