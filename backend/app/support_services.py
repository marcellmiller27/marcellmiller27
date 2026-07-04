"""AI-agent customer service for basic FAQs.

A dependency-free retrieval assistant: it matches a free-text question against a
curated knowledge base using keyword/term overlap scoring, returns the best answer
with a confidence, suggests follow-ups, and escalates to a human when unsure.

The matcher is intentionally deterministic (no external LLM) so it is fast, free,
private, and testable. A hosted LLM could later be slotted in behind the same
``SupportService.ask`` contract for free-form phrasing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.support_models import AskResponse, FaqItem, FaqListResponse

SUPPORT_EMAIL = "support@johnhenryinvestments.example"
CONFIDENCE_FLOOR = 0.18

_STOPWORDS = {
    "the", "a", "an", "is", "are", "do", "does", "did", "i", "my", "how", "what",
    "where", "when", "why", "to", "of", "and", "or", "you", "your", "can", "could",
    "with", "for", "in", "on", "it", "this", "that", "me", "we", "they", "there",
    "be", "have", "has", "will", "would", "should", "if", "about", "please", "am",
}


@dataclass(frozen=True)
class _Faq:
    id: str
    category: str
    question: str
    answer: str
    keywords: tuple[str, ...] = field(default_factory=tuple)


KNOWLEDGE_BASE: list[_Faq] = [
    _Faq(
        "what-is", "Getting started",
        "What is John Henry Investments?",
        "John Henry Investments is a subscription investment-intelligence platform. "
        "It unifies opportunity discovery, a cross-asset Opportunity Score, AI due "
        "diligence, a macro dashboard, and portfolio tracking for individual "
        "investors, business buyers, advisors, and family offices.",
        ("what", "platform", "about", "product", "company", "overview"),
    ),
    _Faq(
        "who-for", "Getting started",
        "Who is the platform for?",
        "Both B2C and B2B users: retail and accredited investors, business "
        "acquisition entrepreneurs, advisors, CPAs, attorneys, bankers, investment "
        "firms, and family offices.",
        ("who", "audience", "retail", "advisor", "family", "office", "b2b", "b2c"),
    ),
    _Faq(
        "pricing", "Billing",
        "How much does it cost?",
        "There are three plans: Consumer ($50/month), Professional ($299/month), and "
        "Enterprise / Family Office ($1,500+/month). See the Pricing page for what "
        "each tier includes.",
        ("price", "pricing", "cost", "plan", "plans", "subscription", "fee", "month", "tier"),
    ),
    _Faq(
        "cancel", "Billing",
        "How do I cancel or change my subscription?",
        "Open Account, then manage your subscription to upgrade, downgrade, or cancel. "
        "Billing is handled through our Stripe-based billing foundation.",
        ("cancel", "change", "upgrade", "downgrade", "refund", "billing", "subscription"),
    ),
    _Faq(
        "signin", "Account & security",
        "How do I sign in?",
        "You can sign in on the web or the mobile app using your email and password. "
        "Accounts with two-step verification will also be asked for a 6-digit code, "
        "and you can enable biometric (Face ID / fingerprint) sign-in on the mobile app.",
        ("sign", "signin", "login", "log", "access", "password", "authenticate"),
    ),
    _Faq(
        "2fa", "Account & security",
        "How do I enable two-factor authentication?",
        "On the mobile app, go to Security & sign-in options and tap Enable "
        "two-factor. You'll get an authenticator secret to add to an app like Google "
        "Authenticator; after that, sign-in asks for a 6-digit code.",
        ("two", "factor", "2fa", "mfa", "authenticator", "otp", "code", "two-step", "verification"),
    ),
    _Faq(
        "biometric", "Account & security",
        "How does biometric sign-in work?",
        "On the mobile app you can register this device's Face ID or fingerprint under "
        "Security & sign-in options. Your biometric never leaves your device; the "
        "platform only stores a device credential reference.",
        ("biometric", "face", "fingerprint", "faceid", "touch", "device", "unlock"),
    ),
    _Faq(
        "reset-password", "Account & security",
        "How do I reset my password?",
        "Use the password reset option on the login screen. For now, if you are "
        f"locked out, contact {SUPPORT_EMAIL} and the team will help you recover access.",
        ("reset", "forgot", "password", "recover", "locked", "change"),
    ),
    _Faq(
        "crypto-keys", "Security & data",
        "Do you store my crypto wallet private keys?",
        "No. The platform is strictly non-custodial: it never stores private keys or "
        "seed phrases and cannot move your funds. Submitting a private key or seed "
        "phrase is rejected for your safety.",
        ("crypto", "wallet", "private", "key", "keys", "seed", "phrase", "custody", "custodial"),
    ),
    _Faq(
        "data-safe", "Security & data",
        "Is my data secure?",
        "Passwords are salted and hashed, sessions use signed expiring tokens, and "
        "sensitive actions are recorded in audit logs. The platform is non-custodial "
        "and never holds fund-moving credentials.",
        ("secure", "security", "safe", "data", "privacy", "protect", "encryption", "hash"),
    ),
    _Faq(
        "market-data", "Market data",
        "Where does the market data come from and is it real-time?",
        "Live quotes come from CoinGecko (crypto), Yahoo Finance (equities, indices, "
        "commodities, treasury yields, FX, bond proxies), and the US BLS (inflation). "
        "The dashboard auto-refreshes, so prices update in near real-time.",
        ("market", "data", "real", "realtime", "live", "price", "quote", "source", "feed", "update"),
    ),
    _Faq(
        "asset-classes", "Market data",
        "Which asset classes are covered?",
        "Crypto, equities and indices, commodities, the treasury yield curve, FX, "
        "fixed-income (bond ETF proxies), real estate (REIT proxy), and inflation. "
        "Private/illiquid classes are tracked via public proxies and models.",
        ("asset", "classes", "coverage", "stocks", "bonds", "fx", "forex", "commodities", "covered"),
    ),
    _Faq(
        "opportunity-score", "Product",
        "What is the John Henry Opportunity Score?",
        "It is a 0-100 score that ranks opportunities across asset classes using "
        "factors like valuation, growth, risk, liquidity, and institutional activity, "
        "giving a consistent way to compare very different investments.",
        ("opportunity", "score", "scoring", "rating", "rank", "0-100"),
    ),
    _Faq(
        "mobile-app", "Product",
        "Is there a mobile app?",
        "Yes. The mobile companion app gives dual (web + mobile) access to the same "
        "account, with password, two-factor, and biometric sign-in.",
        ("mobile", "app", "ios", "android", "phone", "download"),
    ),
    _Faq(
        "advice", "Legal",
        "Is this financial advice?",
        "No. John Henry Investments provides research and decision-support tools for "
        "informational purposes only. It is not investment, legal, or tax advice; "
        "consult a licensed professional before making decisions.",
        ("advice", "financial", "legal", "tax", "fiduciary", "recommendation", "disclaimer"),
    ),
    _Faq(
        "contact", "Support",
        "How do I contact a human?",
        f"Email our team at {SUPPORT_EMAIL} and we'll get back to you. Enterprise "
        "customers also get a dedicated contact.",
        ("contact", "human", "support", "help", "agent", "email", "talk", "representative"),
    ),
]


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in _STOPWORDS and len(t) > 1]


class SupportService:
    def faqs(self, category: str | None = None) -> FaqListResponse:
        items = [
            FaqItem(id=f.id, category=f.category, question=f.question, answer=f.answer)
            for f in KNOWLEDGE_BASE
            if category is None or f.category.lower() == category.lower()
        ]
        categories = sorted({f.category for f in KNOWLEDGE_BASE})
        return FaqListResponse(count=len(items), categories=categories, items=items)

    def ask(self, question: str) -> AskResponse:
        query = _tokenize(question)
        if not query:
            return self._fallback(question)

        scored = sorted(
            ((self._score(faq, query), faq) for faq in KNOWLEDGE_BASE),
            key=lambda pair: pair[0],
            reverse=True,
        )
        best_score, best = scored[0]
        confidence = round(min(best_score / (2 * len(query)), 1.0), 2)

        if best_score <= 0 or confidence < CONFIDENCE_FLOOR:
            return self._fallback(question, near=[faq for _s, faq in scored[:3]])

        suggestions = [faq.question for _s, faq in scored[1:4] if _s > 0]
        return AskResponse(
            answer=best.answer,
            matched_question=best.question,
            category=best.category,
            confidence=confidence,
            escalate=False,
            suggestions=suggestions,
        )

    def _score(self, faq: _Faq, query: list[str]) -> int:
        keywords = set(faq.keywords)
        text_tokens = set(_tokenize(faq.question + " " + faq.answer))
        score = 0
        for token in query:
            singular = token[:-1] if token.endswith("s") and len(token) > 3 else token
            if token in keywords or singular in keywords:
                score += 2
            elif token in text_tokens or singular in text_tokens:
                score += 1
        return score

    def _fallback(self, question: str, near: list[_Faq] | None = None) -> AskResponse:
        suggestions = [f.question for f in (near or KNOWLEDGE_BASE[:3])]
        return AskResponse(
            answer=(
                "I'm not fully sure I understood that. You can rephrase, pick one of "
                f"the suggested questions, or reach a human at {SUPPORT_EMAIL}."
            ),
            matched_question=None,
            category=None,
            confidence=0.0,
            escalate=True,
            suggestions=suggestions,
        )
