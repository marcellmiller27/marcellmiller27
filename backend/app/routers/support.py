from typing import Annotated

from fastapi import APIRouter, Query

from app.support_models import AskRequest, AskResponse, FaqListResponse
from app.support_services import SupportService

router = APIRouter(prefix="/support", tags=["support"])
service = SupportService()


@router.get("/faq", response_model=FaqListResponse)
def faq(
    category: Annotated[str | None, Query(description="Optional category filter.")] = None,
) -> FaqListResponse:
    return service.faqs(category)


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    return service.ask(payload.question)
