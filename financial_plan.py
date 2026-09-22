"""Transparent annual cash-flow engine for a fictional wealth-management case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Assumptions:
    start_year: int = 2026
    age_a: int = 55
    age_b: int = 53
    retirement_age_a: int = 65
    claim_age_a: int = 67
    claim_age_b: int = 67
    end_age_a: int = 95
    portfolio: float = 1_850_000
    annual_savings: float = 65_000
    savings_growth: float = 0.02
    retirement_spending_today: float = 145_000
    ss_a_today: float = 46_000
    ss_b_today: float = 32_000
    inflation: float = 0.025
    nominal_return: float = 0.05
    withdrawal_tax_reserve: float = 0.18


def federal_tax_mfj_2026(gross_income: float, pretax_deferrals: float = 0) -> float:
    """Illustrative regular federal ordinary income tax only; no credits/AMT/NIIT."""
    taxable = max(0, gross_income - pretax_deferrals - 32_200)
    brackets = [(24_800, .10), (100_800, .12), (211_400, .22),
                (403_550, .24), (512_450, .32), (768_700, .35),
                (float('inf'), .37)]
    tax, floor = 0.0, 0.0
    for ceiling, rate in brackets:
        slice_income = max(0, min(taxable, ceiling) - floor)
        tax += slice_income * rate
        floor = ceiling
        if taxable <= ceiling:
            break
    return tax


def project(a: Assumptions = Assumptions(), shock_year=None, shock_return=None):
    """List of annual rows. Withdrawals occur at start of year; return follows."""
    rows = []
    balance = a.portfolio
    retirement_year = a.start_year + a.retirement_age_a - a.age_a
    for year in range(a.start_year, a.start_year + a.end_age_a - a.age_a + 1):
        elapsed = year - a.start_year
        age_a, age_b = a.age_a + elapsed, a.age_b + elapsed
        retired = year >= retirement_year
        opening = balance
        spending = a.retirement_spending_today * (1 + a.inflation) ** elapsed if retired else 0.0
        ss_a = a.ss_a_today * (1 + a.inflation) ** elapsed if age_a >= a.claim_age_a else 0.0
        ss_b = a.ss_b_today * (1 + a.inflation) ** elapsed if age_b >= a.claim_age_b else 0.0
        social_security = (ss_a + ss_b) if retired else 0.0
        gap = max(0.0, spending - social_security)
        withdrawal = gap / (1 - a.withdrawal_tax_reserve) if retired else 0.0
        contribution = a.annual_savings * (1 + a.savings_growth) ** elapsed if not retired else 0.0
        rate = shock_return if year == shock_year else a.nominal_return
        funded_withdrawal = min(opening, withdrawal)
        balance = max(0.0, opening - funded_withdrawal) * (1 + rate) + contribution
        shortfall = withdrawal - funded_withdrawal
        rows.append(dict(year=year, age_a=age_a, age_b=age_b, retired=retired,
                         opening=opening, spending=spending, social_security=social_security,
                         portfolio_withdrawal=withdrawal, withdrawal_rate=(withdrawal / opening if opening else 0),
                         contribution=contribution, return_rate=rate, ending=balance,
                         shortfall=shortfall))
    return rows


def summary(rows):
    retirement = next(r for r in rows if r['retired'])
    depleted = next((r['year'] for r in rows if r['shortfall'] > 0), None)
    return dict(retirement_year=retirement['year'], retirement_portfolio=retirement['opening'],
                first_year_withdrawal=retirement['portfolio_withdrawal'],
                first_year_rate=retirement['withdrawal_rate'],
                age_95_portfolio=rows[-1]['ending'], first_shortfall_year=depleted)
