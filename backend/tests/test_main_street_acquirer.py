# JHI-SIG: 69M2705M | The Main Street Acquirer — engines + edition + cadence tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Network-free tests for the Main Street Acquirer build:

  • SBA Lending Intelligence engine (sample load, derivation, resilient fetch fallback)
  • Recession-resilience + boomer-succession industry model (scoring, rotation)
  • The "main-street-acquirer" newsletter edition (sections, fact-lock, governance)
  • Distribution cadence (metadata, scheduled-generation hook)
  • Free-subscriber capture (double opt-in stub) + SES cadence broadcast (dry-run)

Everything runs offline: the SBA engine ships a sample dataset and the edition/broadcast
paths accept injected quotes so no market feed is polled.
"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app import industry_resilience as ir
from app import newsletter_subscriptions as subs
from app import sba_intelligence as sba
from app.email_service import broadcast_by_cadence
from app.main import app
from app.market_models import Quote
from app.newsletter_content import (
    CADENCES,
    EDITION_CADENCE,
    EDITION_SLUGS,
    build_edition,
    cadence_for,
    editions_for_cadence,
    generate_scheduled_editions,
)

client = TestClient(app)


def _q(symbol: str, name: str, price: float, unit: str = "%", asset_class: str = "macro") -> Quote:
    return Quote(symbol=symbol, name=name, asset_class=asset_class, price=price, unit=unit, source="fred")


def _macro_quotes() -> list[Quote]:
    return [
        _q("INFLATION", "US CPI", 3.10),
        _q("FED_FUNDS", "Fed Funds", 4.50),
        _q("UST10Y", "10-Year Treasury", 4.20),
        _q("UNEMPLOYMENT", "Unemployment", 4.10),
        _q("GDP", "GDP", 28000.0, "USD bn"),
        _q("SPX", "S&P 500", 5600.0, "index", "equity"),
        _q("GOLD", "Gold", 2400.0, "USD/oz", "commodity"),
        _q("BTC", "Bitcoin", 65000.0, "USD", "crypto"),
    ]


_NOW = datetime(2026, 8, 10, tzinfo=timezone.utc)


# ── SBA Lending Intelligence engine ──────────────────────────────────────────
def test_sba_sample_loads_and_summarizes() -> None:
    sba.reset_cache()
    loans, mode = sba.load_loans()
    assert mode in ("sample", "cache")  # offline → sample (no live URL configured)
    assert len(loans) >= 20
    intel = sba.summarize(loans, "sample")
    assert intel.loan_count == len(loans)
    assert intel.total_gross_approval > 0
    assert intel.fiscal_years == sorted(intel.fiscal_years)
    # Derived aggregates present.
    assert intel.by_industry and intel.by_industry[0].loan_count >= 1
    assert intel.active_lenders and intel.active_lenders[0].loan_count >= 1
    assert intel.yearly_trends and all(t.loan_count > 0 for t in intel.yearly_trends)
    # Change-of-ownership share is a valid percentage.
    for row in intel.by_industry:
        assert 0.0 <= row.change_of_ownership_pct <= 100.0
        assert row.median_gross_approval > 0


def test_sba_industry_snapshot_aggregates_by_naics_prefix() -> None:
    intel = sba.intelligence(top_n=20)
    snap = sba.industry_snapshot(intel, ["2382"])  # the building-trades cluster
    assert snap is not None
    assert snap.loan_count >= 1
    assert snap.total_gross_approval > 0
    assert sba.industry_snapshot(intel, ["999999"]) is None  # no match → None


def test_sba_fetch_is_resilient_and_parses_live_shape(monkeypatch) -> None:
    # Point at a "live" URL and monkeypatch the fetcher — stays fully network-free.
    csv_text = (
        "Program,BorrState,NaicsCode,NaicsDescription,ApprovalFiscalYear,GrossApproval,"
        "SBAGuaranteedApproval,TermInMonths,BankName,JobsSupported,BusinessType\n"
        "7a,TX,238220,HVAC,2024,800000,600000,120,Test Bank,10,Change of Ownership\n"
        "7a,TX,238220,HVAC,2024,,,120,Test Bank,10,Existing\n"  # skipped: no gross approval
    )
    monkeypatch.setattr(sba, "SBA_7A_DATASET_URL", "https://example.test/sba.csv")
    monkeypatch.setattr(sba, "fetch_sba_dataset", lambda url: csv_text)
    # Avoid writing/reading the on-disk cache in the test.
    monkeypatch.setattr(sba, "_read_disk_cache", lambda: None)
    monkeypatch.setattr(sba, "_write_disk_cache", lambda loans: None)
    loans, mode = sba.load_loans(refresh=True)
    assert mode == "live"
    assert len(loans) == 1  # the malformed row is dropped
    assert loans[0].is_change_of_ownership is True


def test_sba_fetch_failure_falls_back_to_sample(monkeypatch) -> None:
    def _boom(url):
        raise sba.ProviderError("network down")

    monkeypatch.setattr(sba, "SBA_7A_DATASET_URL", "https://example.test/sba.csv")
    monkeypatch.setattr(sba, "fetch_sba_dataset", _boom)
    monkeypatch.setattr(sba, "_read_disk_cache", lambda: None)
    loans, mode = sba.load_loans(refresh=True)
    assert mode == "sample" and len(loans) >= 20  # always deliver


# ── Industry resilience / succession model ───────────────────────────────────
def test_resilience_scores_are_weighted_composites() -> None:
    hvac = ir.get("hvac")
    assert hvac is not None
    r = hvac.resilience_inputs
    expected = round(
        100 * (0.45 * r.essential_service + 0.35 * r.demand_stability + 0.20 * r.recurring_contract), 1
    )
    assert hvac.recession_resilience == expected
    assert 0 <= hvac.recession_resilience <= 100
    assert 0 <= hvac.succession_opportunity <= 100
    # Discretionary trades score materially lower on resilience than essential ones.
    assert ir.get("restaurant").recession_resilience < hvac.recession_resilience


def test_industry_ranking_and_spotlight_rotation() -> None:
    ranked = ir.rank_by("combined_score")
    assert ranked == sorted(ranked, key=lambda p: p.combined_score, reverse=True)
    # Deterministic: same instant → same spotlight; different weeks rotate.
    a = ir.spotlight_for(_NOW)
    b = ir.spotlight_for(_NOW)
    assert a.key == b.key
    weeks = {ir.spotlight_for(datetime(2026, m, 1, tzinfo=timezone.utc)).key for m in range(1, 13)}
    assert len(weeks) >= 2  # the spotlight actually rotates across the year


# ── The Main Street Acquirer edition ─────────────────────────────────────────
def test_edition_registered_and_full_has_all_sections() -> None:
    assert "main-street-acquirer" in EDITION_SLUGS
    ed = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    assert ed.title == "The Main Street Acquirer"
    assert ed.cadence == cadence_for("main-street-acquirer")
    headings = " || ".join(g.heading for g in ed.groups)
    assert "SBA Lending Intelligence" in headings
    assert "Recession-Resilient Industry Spotlight" in headings
    assert "Acquisition Playbook" in headings
    assert "Deal Teardown" in headings
    assert "Financing Corner" in headings
    assert "Metric of the Issue" in headings
    # Executive thesis is acquirer-framed and fact-locked (references the debt/real-rate read).
    assert "DSCR" in ed.intro or "debt-service" in ed.intro.lower()


def test_edition_teaser_is_gated_and_thinner() -> None:
    full = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    teaser = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=False)
    assert teaser.teaser is True and full.teaser is False
    assert len(full.groups) > len(teaser.groups)
    assert teaser.charts == []  # teaser stays lightweight


def test_edition_carries_derived_charts_when_full() -> None:
    ed = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    charts = [c for g in ed.groups for c in g.charts]
    assert charts, "expected group-level charts in the full edition"
    for c in charts:
        assert c.image.startswith("data:image/png;base64,")
        assert c.caption and c.source


def test_edition_is_deterministic() -> None:
    a = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    b = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    assert [g.heading for g in a.groups] == [g.heading for g in b.groups]
    a_charts = [c.image for g in a.groups for c in g.charts]
    b_charts = [c.image for g in b.groups for c in g.charts]
    assert a_charts == b_charts


def test_edition_methodology_has_attribution_and_governance() -> None:
    ed = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    method = ed.methodology
    assert "U.S. Small Business Administration" in method
    assert "Bureau of Labor Statistics" in method
    assert "derived metrics only" in method
    # Governance: no raw borrower-level rows leak into any surfaced text.
    blob = " ".join(
        [ed.intro]
        + [g.blurb for g in ed.groups]
        + [it.body for g in ed.groups for it in g.items]
        + [it.source or "" for g in ed.groups for it in g.items]
    )
    assert "Sample Borrower" not in blob  # sample borrower names never surface


def test_edition_deal_teardown_is_derived_from_engine() -> None:
    ed = build_edition("main-street-acquirer", _macro_quotes(), _NOW, full=True)
    teardown = next(g for g in ed.groups if g.heading == "Deal Teardown")
    labels = {it.label for it in teardown.items}
    assert "Deal X-Ray score" in labels
    assert "Valuation lens" in labels
    financing = next(g for g in ed.groups if g.heading.startswith("Financing Corner"))
    # The SBA 7(a) structure is surfaced with a derived DSCR read.
    assert any("DSCR" in it.value for it in financing.items)


# ── Distribution cadence ─────────────────────────────────────────────────────
def test_cadence_metadata_and_membership() -> None:
    assert set(EDITION_CADENCE["main-street-acquirer"]) == {"weekly-pulse", "monthly-deep-dive"}
    assert "main-street-acquirer" in editions_for_cadence("weekly-pulse")
    assert "main-street-acquirer" in editions_for_cadence("monthly-deep-dive")
    for c in CADENCES:
        for slug in editions_for_cadence(c):
            assert slug in EDITION_SLUGS


def test_scheduled_generation_hook_builds_cadence_batch() -> None:
    editions = generate_scheduled_editions("weekly-pulse", now=_NOW, quotes=_macro_quotes())
    slugs = {e.slug for e in editions}
    assert slugs == set(editions_for_cadence("weekly-pulse"))
    assert all(e.teaser is False for e in editions)  # full editions for the send


# ── Free-subscriber capture (double opt-in stub) ─────────────────────────────
def test_double_opt_in_flow() -> None:
    subs.reset()
    r = subs.subscribe("acquirer@example.com", "weekly-pulse")
    assert r["status"] == "pending" and r["confirm_token"]
    # Not a recipient until confirmed.
    assert subs.confirmed_recipients("weekly-pulse") == []
    c = subs.confirm(r["confirm_token"])
    assert c["status"] == "confirmed"
    assert subs.confirmed_recipients("weekly-pulse") == ["acquirer@example.com"]
    # A used/invalid token is rejected.
    assert subs.confirm(r["confirm_token"])["status"] == "invalid"
    # Unsubscribe removes them from the broadcast target.
    subs.unsubscribe("acquirer@example.com")
    assert subs.confirmed_recipients("weekly-pulse") == []


def test_subscribe_rejects_bad_email() -> None:
    subs.reset()
    assert subs.subscribe("not-an-email")["status"] == "invalid"


# ── SES cadence broadcast (dry-run, network-free) ────────────────────────────
def test_broadcast_by_cadence_is_dry_run_by_default(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_EMAIL_SEND", raising=False)
    monkeypatch.delenv("SES_SENDER", raising=False)
    subs.reset()
    token = subs.subscribe("reader@example.com", "monthly-deep-dive")["confirm_token"]
    subs.confirm(token)
    res = broadcast_by_cadence("monthly-deep-dive", now=_NOW, quotes=_macro_quotes())
    assert res["cadence"] == "monthly-deep-dive"
    assert set(res["editions"]) == set(editions_for_cadence("monthly-deep-dive"))
    assert res["recipient_count"] == 1
    assert res["live"] is False
    assert res["results"] and all(r["status"] == "dry_run" for r in res["results"])


# ── Router endpoints (subscribe/confirm/cadences) ────────────────────────────
def test_subscribe_confirm_endpoints() -> None:
    subs.reset()
    r = client.post("/api/v1/newsletters/subscribe", json={"email": "web@example.com", "cadence": "weekly-pulse"})
    assert r.status_code == 200
    token = r.json()["confirm_token"]
    c = client.get("/api/v1/newsletters/subscribe/confirm", params={"token": token})
    assert c.status_code == 200 and c.json()["status"] == "confirmed"
    assert client.get("/api/v1/newsletters/subscribe/confirm", params={"token": "bogus"}).status_code == 404


def test_broadcast_endpoint_requires_staff() -> None:
    r = client.post("/api/v1/newsletters/broadcast", json={"cadence": "weekly-pulse"})
    assert r.status_code in (401, 403)


def test_cadences_endpoint_lists_editions() -> None:
    body = client.get("/api/v1/newsletters/cadences").json()
    cadences = {c["cadence"]: c["editions"] for c in body["cadences"]}
    assert "main-street-acquirer" in cadences["weekly-pulse"]
    assert "main-street-acquirer" in cadences["monthly-deep-dive"]
