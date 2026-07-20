"""JHI pricing & margin model — the "mirror NASDAQ mechanism" schema.

Denominates JHI billing in the SAME unit NASDAQ licenses in (the external end
user / paid seat), so cost and revenue move in lockstep. Prints per-unit
economics and scale scenarios (near-term / mid / full-scale) with the NASDAQ
overage handled the way NASDAQ handles it: flat to the cap, higher rate above.

Run:  python3 scripts/pricing_margin_model.py
Numbers are estimates for internal planning — not a forecast. Overage rate is a
placeholder pending the signed NASDAQ Service Description.
"""

from __future__ import annotations

# --- Cost inputs (per external end user / seat, monthly) --------------------
NASDAQ_FLAT_ANNUAL = 18_000.0       # SF1 + NDL platform, up to the cap
NASDAQ_CAP_USERS = 1_000
NASDAQ_OVERAGE_PER_USER_MO = 3.00   # placeholder (2x the at-cap rate); confirm Monday
CLOUD_PER_USER_MO = 1.50            # AWS/GCP audit estimate (cached research SaaS)
PAYMENT_PCT = 0.03                  # card/processing on revenue
FIXED_OPEX_MO = 2_000.0             # lean misc fixed (tooling/base infra); founder $1/yr

NASDAQ_AT_CAP_PER_USER_MO = NASDAQ_FLAT_ANNUAL / 12 / NASDAQ_CAP_USERS  # ~$1.50


# --- Tiers (the mirrored schema) --------------------------------------------
# Consumer / Professional = single seat. Enterprise = base seats + per-add'l
# seat (our mirror of NASDAQ's "up to N, overage above").
TIERS = {
    "Consumer": {"price": 110.0, "seats_included": 1, "extra_seat": 0.0},  # $110 list; $1,188/yr prepaid ($99/mo effective, 10% off)
    "Professional": {"price": 299.0, "seats_included": 1, "extra_seat": 0.0},
    "Enterprise": {"price": 1500.0, "seats_included": 5, "extra_seat": 99.0},
}


def nasdaq_cost_mo(total_users: int) -> float:
    base = NASDAQ_FLAT_ANNUAL / 12
    if total_users <= NASDAQ_CAP_USERS:
        return base
    return base + (total_users - NASDAQ_CAP_USERS) * NASDAQ_OVERAGE_PER_USER_MO


def unit_margin(price_per_seat: float, nasdaq_per_user_mo: float) -> tuple[float, float]:
    """Gross margin $ and % for one incremental seat at a given seat price."""
    cost = nasdaq_per_user_mo + CLOUD_PER_USER_MO + price_per_seat * PAYMENT_PCT
    gm = price_per_seat - cost
    return gm, (gm / price_per_seat * 100 if price_per_seat else 0.0)


def scenario(name: str, accounts: dict[str, int], ent_avg_seats: float) -> None:
    users = accounts["Consumer"] + accounts["Professional"] + int(
        round(accounts["Enterprise"] * ent_avg_seats)
    )
    ent_extra = max(0.0, ent_avg_seats - TIERS["Enterprise"]["seats_included"])
    rev_mo = (
        accounts["Consumer"] * TIERS["Consumer"]["price"]
        + accounts["Professional"] * TIERS["Professional"]["price"]
        + accounts["Enterprise"]
        * (TIERS["Enterprise"]["price"] + ent_extra * TIERS["Enterprise"]["extra_seat"])
    )
    data_mo = nasdaq_cost_mo(users)
    cloud_mo = users * CLOUD_PER_USER_MO
    pay_mo = rev_mo * PAYMENT_PCT
    gross_mo = rev_mo - data_mo - cloud_mo - pay_mo
    ebitda_mo = gross_mo - FIXED_OPEX_MO
    print(f"\n=== {name} ===")
    print(f"  Accounts: Consumer {accounts['Consumer']:,} · "
          f"Professional {accounts['Professional']:,} · "
          f"Enterprise {accounts['Enterprise']:,} (avg {ent_avg_seats} seats)")
    print(f"  Total end users (NASDAQ-counted): {users:,}"
          + ("  [OVER CAP — overage applies]" if users > NASDAQ_CAP_USERS else "  [within cap]"))
    print(f"  Revenue:        ${rev_mo:,.0f}/mo   (${rev_mo*12:,.0f}/yr)")
    print(f"  NASDAQ data:    ${data_mo:,.0f}/mo")
    print(f"  Cloud:          ${cloud_mo:,.0f}/mo")
    print(f"  Processing:     ${pay_mo:,.0f}/mo")
    print(f"  Gross profit:   ${gross_mo:,.0f}/mo   ({gross_mo/rev_mo*100:.1f}% gross margin)")
    print(f"  EBITDA:         ${ebitda_mo:,.0f}/mo   ({ebitda_mo/rev_mo*100:.1f}% EBITDA margin)")


def main() -> None:
    print("JHI PRICING & MARGIN MODEL — 'mirror NASDAQ mechanism' (per external end user)")
    print("=" * 78)
    print(f"NASDAQ cost/user at cap: ${NASDAQ_AT_CAP_PER_USER_MO:.2f}/mo "
          f"(${NASDAQ_FLAT_ANNUAL:,.0f}/yr ÷ {NASDAQ_CAP_USERS:,})")
    print(f"Cloud/user: ${CLOUD_PER_USER_MO:.2f}/mo · Processing: {PAYMENT_PCT*100:.0f}% · "
          f"Overage>cap: ${NASDAQ_OVERAGE_PER_USER_MO:.2f}/user/mo (placeholder)")

    print("\n--- Per-seat unit economics (gross margin per incremental seat) ---")
    print(f"{'Unit':<26}{'Seat price':>12}{'Cost/seat':>12}{'GM $':>10}{'GM %':>8}")
    rows = [
        ("Consumer seat", TIERS["Consumer"]["price"]),
        ("Professional seat", TIERS["Professional"]["price"]),
        ("Enterprise (per-seat*)", TIERS["Enterprise"]["price"] / TIERS["Enterprise"]["seats_included"]),
        ("Enterprise add'l seat", TIERS["Enterprise"]["extra_seat"]),
    ]
    for label, price in rows:
        gm, gmp = unit_margin(price, NASDAQ_AT_CAP_PER_USER_MO)
        cost = price - gm
        print(f"{label:<26}{price:>11.2f}{cost:>12.2f}{gm:>10.2f}{gmp:>7.1f}%")
    print("  *Enterprise base $1,500 / 5 included seats = $300/seat-equiv.")

    print("\n--- Overage stress: Consumer-seat margin as the per-user data cost rises ---")
    for rate in (NASDAQ_AT_CAP_PER_USER_MO, 3.0, 6.0, 10.0, 15.0):
        gm, gmp = unit_margin(TIERS["Consumer"]["price"], rate)
        print(f"  NASDAQ ${rate:>5.2f}/user/mo -> Consumer GM ${gm:5.2f} ({gmp:.1f}%)")

    # Illustrative scale scenarios (mix is illustrative; margins are robust to mix)
    scenario("Near-term (~1,200 users)",
             {"Consumer": 800, "Professional": 330, "Enterprise": 10}, ent_avg_seats=7)
    scenario("Mid (~5,000 users)",
             {"Consumer": 3500, "Professional": 1200, "Enterprise": 40}, ent_avg_seats=8)
    scenario("Full-scale target (~55,500 users)",
             {"Consumer": 50000, "Professional": 5000, "Enterprise": 500}, ent_avg_seats=9)


if __name__ == "__main__":
    main()
