# JHI-SIG: 69M2705M | Support & AI Agents | John Henry Investments (proprietary)
from datetime import datetime

from pydantic import BaseModel, Field


class AgentInfo(BaseModel):
    key: str
    name: str
    role: str
    persona: str
    expertise: list[str]
    background: str
    avatar: str
    handles: list[str]
    escalates: bool


class AgentRoster(BaseModel):
    count: int
    agents: list[AgentInfo]


class AgentMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    user_email: str | None = None


class AgentReply(BaseModel):
    agent_key: str
    agent_name: str
    agent_role: str
    answer: str
    confidence: float
    category: str | None = None
    escalated: bool = False
    ticket_id: str | None = None
    suggestions: list[str] = Field(default_factory=list)


class TicketRead(BaseModel):
    id: str
    user_email: str | None
    agent: str
    subject: str
    message: str
    category: str | None
    priority: str
    status: str
    assigned_to: str
    created_at: datetime
