# JHI-SIG: 69M2705M | Growth / Leads | John Henry Investments (proprietary)
from datetime import datetime

from pydantic import BaseModel, Field


class LeadCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    full_name: str | None = Field(default=None, max_length=255)
    interest: str | None = Field(default=None, max_length=80)
    source: str = Field(default="waitlist", max_length=80)


class LeadRead(BaseModel):
    id: str
    email: str
    full_name: str | None
    interest: str | None
    source: str
    created_at: datetime


class LeadCaptureResponse(BaseModel):
    status: str  # "captured" | "already_on_list"
    message: str
    total: int


class LeadCount(BaseModel):
    count: int
