from pydantic import BaseModel, Field


class FaqItem(BaseModel):
    id: str
    category: str
    question: str
    answer: str


class FaqListResponse(BaseModel):
    count: int
    categories: list[str]
    items: list[FaqItem]


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class AskResponse(BaseModel):
    answer: str
    matched_question: str | None = None
    category: str | None = None
    confidence: float
    escalate: bool
    suggestions: list[str] = Field(default_factory=list)
