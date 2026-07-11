"""Five-agent AI customer-service team with routing and founder escalation.

Each agent owns a domain. An incoming message is classified (reusing the support
knowledge-base matcher) and routed to the right agent. Platform issues — and anything
the team can't confidently answer — get an **initial response** and are **escalated to
the founder** as a support ticket for further action.

Deterministic (no external LLM): fast, free, private, testable. The same contract can
later be backed by a hosted LLM per agent.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents_models import AgentInfo, AgentReply, AgentRoster, TicketRead
from app.db_models import SupportTicketDB
from app.foundation_models import Principal
from app.support_services import SupportService


@dataclass(frozen=True)
class AgentSpec:
    key: str
    name: str
    role: str
    persona: str
    expertise: tuple[str, ...]
    background: str
    avatar: str
    handles: tuple[str, ...]
    escalates: bool


AGENTS: list[AgentSpec] = [
    AgentSpec(
        "onboarding", "Ava Bennett", "Onboarding Concierge",
        "Warm, guides newly onboarded users to first value.",
        ("User onboarding", "Account setup", "Product walkthroughs", "Activation"),
        "Ava is JHI's onboarding concierge, trained on the platform's onboarding "
        "playbooks and product documentation. She gets every new member from sign-up "
        "to their first insight — accounts, navigation, and first actions.",
        "/team/ava.png", ("Getting started",), False,
    ),
    AgentSpec(
        "billing", "Max Carter", "Subscriptions & Billing Specialist",
        "Clear and helpful on plans, pricing, and account/subscription options.",
        ("Subscription plans", "Pricing & upgrades", "Billing & invoices", "Stripe"),
        "Max handles every subscription and billing question — Consumer, Professional, "
        "and Enterprise plans, upgrades/downgrades, and the Stripe-based billing "
        "foundation. Trained on JHI's plan catalog and billing policies.",
        "/team/max.png", ("Billing",), False,
    ),
    AgentSpec(
        "security", "Sage Okafor", "Account & Security Agent",
        "Careful and reassuring on login, 2FA, biometric, and data protection.",
        ("Authentication", "Two-factor & biometric", "Data protection", "Privacy"),
        "Sage is the account & security specialist, trained on JHI's security model: "
        "password, two-factor, and biometric sign-in, plus how member data is "
        "protected. Calm and precise on anything access- or privacy-related.",
        "/team/sage.png", ("Account & security", "Security & data"), False,
    ),
    AgentSpec(
        "product", "Quinn Alvarez", "Product & Markets Guide",
        "Knowledgeable on features, market data, and the Opportunity Score (no advice).",
        ("Opportunity Score", "Live market data", "Platform modules", "How-to"),
        "Quinn explains how the platform works — the John Henry Opportunity Score, "
        "live multi-asset market data, and the modules — in plain language. Provides "
        "education and product guidance, never personalized financial advice.",
        "/team/quinn.png", ("Product", "Market data", "Legal"), False,
    ),
    AgentSpec(
        "technical", "Tess Nakamura", "Technical Support & Triage",
        "Calm first responder for platform issues; escalates to the founder for action.",
        ("Incident triage", "Troubleshooting", "Bug intake", "Founder escalation"),
        "Tess is the first responder for platform issues. She acknowledges, triages "
        "severity, gives an initial response, and forwards anything needing action to "
        "the founder as a tracked ticket — so nothing falls through the cracks.",
        "/team/tess.png", ("Support",), True,
    ),
]
_AGENT_BY_KEY = {a.key: a for a in AGENTS}

_CATEGORY_TO_AGENT = {
    "Getting started": "onboarding",
    "Billing": "billing",
    "Account & security": "security",
    "Security & data": "security",
    "Product": "product",
    "Market data": "product",
    "Legal": "product",
    "Support": "technical",
}

_ISSUE_KEYWORDS = (
    "broken", "bug", "error", "crash", "not working", "doesn't work", "dont work",
    "can't", "cannot", "won't", "wont", "failed", "failing", "issue", "problem",
    "glitch", "stuck", "frozen", "down", "503", "500", "complaint", "refund me",
    "charged twice", "double charged", "locked out",
)
FOUNDER = "founder"


class AgentService:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.support = SupportService()

    def roster(self) -> AgentRoster:
        return AgentRoster(
            count=len(AGENTS),
            agents=[
                AgentInfo(
                    key=a.key, name=a.name, role=a.role, persona=a.persona,
                    expertise=list(a.expertise), background=a.background, avatar=a.avatar,
                    handles=list(a.handles), escalates=a.escalates,
                )
                for a in AGENTS
            ],
        )

    def handle(self, message: str, user_email: str | None = None) -> AgentReply:
        ask = self.support.ask(message)
        is_issue = self._looks_like_issue(message)

        if is_issue or ask.escalate:
            agent = _AGENT_BY_KEY["technical"]
            escalate = True
        else:
            agent = _AGENT_BY_KEY.get(_CATEGORY_TO_AGENT.get(ask.category or "", ""), None)
            agent = agent or _AGENT_BY_KEY["product"]
            escalate = False

        if escalate:
            lead_in = (
                "Thanks for flagging this — I've logged it and forwarded it to our "
                "founder for further action. "
            )
            answer = lead_in + (ask.answer if not is_issue else
                                "In the meantime, here's what I can confirm: your data is "
                                "safe and no action is lost. We'll follow up by email.")
            ticket_id = self._open_ticket(agent.name, message, ask.category, user_email, is_issue)
        else:
            answer = ask.answer
            ticket_id = None

        return AgentReply(
            agent_key=agent.key,
            agent_name=agent.name,
            agent_role=agent.role,
            answer=answer,
            confidence=ask.confidence,
            category=ask.category,
            escalated=escalate,
            ticket_id=ticket_id,
            suggestions=ask.suggestions,
        )

    def list_tickets(self, _principal: Principal) -> list[TicketRead]:
        assert self.db is not None
        tickets = self.db.scalars(
            select(SupportTicketDB).order_by(SupportTicketDB.created_at.desc())
        ).all()
        return [
            TicketRead(
                id=t.id, user_email=t.user_email, agent=t.agent, subject=t.subject,
                message=t.message, category=t.category, priority=t.priority,
                status=t.status, assigned_to=t.assigned_to, created_at=t.created_at,
            )
            for t in tickets
        ]

    # -- internals -------------------------------------------------------- #
    @staticmethod
    def _looks_like_issue(message: str) -> bool:
        text = message.lower()
        return any(kw in text for kw in _ISSUE_KEYWORDS)

    def _open_ticket(
        self,
        agent_name: str,
        message: str,
        category: str | None,
        user_email: str | None,
        is_issue: bool,
    ) -> str | None:
        if self.db is None:
            return None
        ticket = SupportTicketDB(
            user_email=user_email,
            agent=agent_name,
            subject=(message.strip()[:80] or "Support request"),
            message=message.strip()[:1000],
            category=category,
            priority="high" if is_issue else "normal",
            status="open",
            assigned_to=FOUNDER,
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket.id
