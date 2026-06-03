from pydantic import BaseModel


class PageContent(BaseModel):
    page: int
    text: str