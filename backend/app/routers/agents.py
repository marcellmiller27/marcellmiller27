# JHI-SIG: 69M2705M | Support & AI Agents | John Henry Investments (proprietary)
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents_models import AgentMessageRequest, AgentReply, AgentRoster, TicketRead
from app.agents_services import AgentService
from app.database import get_db
from app.dependencies import get_current_principal
from app.foundation_models import Principal

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=AgentRoster)
def roster() -> AgentRoster:
    return AgentService().roster()


@router.post("/message", response_model=AgentReply)
def message(
    payload: AgentMessageRequest,
    db: Annotated[Session, Depends(get_db)],
) -> AgentReply:
    return AgentService(db).handle(payload.message, payload.user_email)


@router.get("/tickets", response_model=list[TicketRead])
def tickets(
    principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> list[TicketRead]:
    return AgentService(db).list_tickets(principal)
