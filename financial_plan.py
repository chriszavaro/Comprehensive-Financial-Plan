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
    essential_spending_today: float = 120_000
    survivor_spending_today: float = 110_000
    ss_a_today: float = 46_000
    ss_b_today: float = 32_000
    inflation: float = 0.025
    nominal_return: float = 0.05
    withdrawal_tax_reserve: float = 0.18
    discretionary_cut_today: float = 0.0
    cut_start_year: int | None = None
    cut_end_year: int | None = None
    survivor_year: int | None = None
    care_start_year: int | None = None
    care_years: int = 0
    care_cost_today: float = 0.0


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


def _validate(a: Assumptions, shock_year, shock_return) -> None:
    if not 67 <= a.claim_age_a <= 70 or not 67 <= a.claim_age_b <= 70:
        raise ValueError("This case supports Social Security claiming ages 67 through 70")
    if not 0 <= a.discretionary_cut_today <= a.retirement_spending_today - a.essential_spending_today:
        raise ValueError("Spending cut must preserve the essential-spending floor")
    if a.care_cost_today < 0 or a.care_years < 0:
        raise ValueError("Care cost and duration cannot be negative")
    if shock_year is not None and shock_return is None:
        raise ValueError("A shock year requires a return")
    if a.cut_start_year is not None and a.cut_end_year is None:
        raise ValueError("A spending cut requires an end year")


def project(a: Assumptions = Assumptions(), shock_year=None, shock_return=None):
    """Annual rows. Withdrawals occur at start of year; return follows.

    Benefits and spending use annual, inflation-indexed proxies. A survivor
    receives the higher modeled benefit, not both. This is not a tax engine.
    """
    _validate(a, shock_year, shock_return)
    rows = []
    balance = a.portfolio
    retirement_year = a.start_year + a.retirement_age_a - a.age_a
    for year in range(a.start_year, a.start_year + a.end_age_a - a.age_a + 1):
        elapsed = year - a.start_year
        age_a, age_b = a.age_a + elapsed, a.age_b + elapsed
        retired = year >= retirement_year
        opening = balance
        price_index = (1 + a.inflation) ** elapsed
        survivor = a.survivor_year is not None and year >= a.survivor_year
        scheduled_cut = (a.cut_start_year is not None and a.cut_end_year is not None
                         and a.cut_start_year <= year <= a.cut_end_year and not survivor)
        spending_cut = a.discretionary_cut_today * price_index if retired and scheduled_cut else 0.0
        care_cost = (a.care_cost_today * price_index if retired and a.care_start_year is not None
                     and a.care_start_year <= year < a.care_start_year + a.care_years else 0.0)
        household_spending_today = a.survivor_spending_today if survivor else a.retirement_spending_today
        spending = household_spending_today * price_index - spending_cut + care_cost if retired else 0.0

        # Illustrative FRA=67 benefit; 8% delayed credit for each year to age 70.
        ss_a = (a.ss_a_today * (1 + .08 * (a.claim_age_a - 67)) * price_index
                if age_a >= a.claim_age_a else 0.0)
        ss_b = (a.ss_b_today * (1 + .08 * (a.claim_age_b - 67)) * price_index
                if age_b >= a.claim_age_b else 0.0)
        social_security = (max(ss_a, ss_b) if survivor else ss_a + ss_b) if retired else 0.0

        gap = max(0.0, spending - social_security)
        withdrawal = gap / (1 - a.withdrawal_tax_reserve) if retired else 0.0
        contribution = a.annual_savings * (1 + a.savings_growth) ** elapsed if not retired else 0.0
        rate = shock_return if year == shock_year else a.nominal_return
        funded_withdrawal = min(opening, withdrawal)
        balance = max(0.0, opening - funded_withdrawal) * (1 + rate) + contribution
        shortfall = withdrawal - funded_withdrawal
        rows.append(dict(year=year, age_a=age_a, age_b=age_b, retired=retired,
                         opening=opening, spending=spending, spending_cut=spending_cut,
                         care_cost=care_cost, survivor=survivor, price_index=price_index,
                         social_security=social_security, portfolio_withdrawal=withdrawal,
                         withdrawal_rate=(withdrawal / opening if opening else 0),
                         contribution=contribution, return_rate=rate, ending=balance,
                         shortfall=shortfall,
                         net_spending_shortfall=shortfall * (1 - a.withdrawal_tax_reserve)))
    return rows


def summary(rows):
    retirement = next(r for r in rows if r["retired"])
    depleted = next((r["year"] for r in rows if r["shortfall"] > 0), None)
    retired_rows = [r for r in rows if r["retired"]]
    return dict(retirement_year=retirement["year"],
                retirement_portfolio=retirement["opening"],
                first_year_withdrawal=retirement["portfolio_withdrawal"],
                first_year_rate=retirement["withdrawal_rate"],
                age_95_portfolio=rows[-1]["ending"],
                age_95_portfolio_real=rows[-1]["ending"] / rows[-1]["price_index"],
                lowest_retirement_balance_real=min(r["ending"] / r["price_index"] for r in retired_rows),
                total_spending_cuts_real=sum(r["spending_cut"] / r["price_index"] for r in retired_rows),
                total_care_cost_real=sum(r["care_cost"] / r["price_index"] for r in retired_rows),
                first_shortfall_year=depleted)
