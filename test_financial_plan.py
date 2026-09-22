"""Checks for material arithmetic, cash-flow decisions, and life-event behavior."""

import unittest
from dataclasses import replace

from financial_plan import Assumptions, federal_tax_mfj_2026, project, summary


class FinancialPlanTests(unittest.TestCase):
    def test_2026_joint_tax_layers(self):
        self.assertAlmostEqual(federal_tax_mfj_2026(300_000, 49_000), 37_708)
        self.assertEqual(federal_tax_mfj_2026(20_000), 0)

    def test_retirement_bridge(self):
        base = project()
        bridge = next(row for row in base if row["year"] == 2036)
        self.assertEqual(bridge["social_security"], 0)
        self.assertAlmostEqual(bridge["portfolio_withdrawal"], bridge["spending"] / .82)
        self.assertLess(next(row for row in base if row["year"] == 2040)["portfolio_withdrawal"],
                        bridge["portfolio_withdrawal"])

    def test_later_retirement_adds_savings_and_reduces_initial_rate(self):
        base = summary(project())
        later = summary(project(replace(Assumptions(), retirement_age_a=67)))
        self.assertEqual(later["retirement_year"], 2038)
        self.assertGreater(later["retirement_portfolio"], base["retirement_portfolio"])
        self.assertLess(later["first_year_rate"], base["first_year_rate"])

    def test_flexible_spending_preserves_floor_and_improves_legacy(self):
        shock = summary(project(shock_year=2036, shock_return=-.20))
        flex_a = replace(Assumptions(), discretionary_cut_today=25_000,
                         cut_start_year=2037, cut_end_year=2039)
        flex_rows = project(flex_a, shock_year=2036, shock_return=-.20)
        self.assertAlmostEqual(summary(flex_rows)["total_spending_cuts_real"], 75_000)
        self.assertAlmostEqual(next(r for r in flex_rows if r["year"] == 2037)["spending"] /
                               next(r for r in flex_rows if r["year"] == 2037)["price_index"], 120_000)
        self.assertGreater(summary(flex_rows)["age_95_portfolio_real"], shock["age_95_portfolio_real"])

    def test_claiming_delay_and_survivor_income(self):
        a = replace(Assumptions(), claim_age_a=70, survivor_year=2051)
        rows = project(a)
        self.assertEqual(next(r for r in rows if r["year"] == 2038)["social_security"], 0)
        row = next(r for r in rows if r["year"] == 2051)
        self.assertTrue(row["survivor"])
        self.assertAlmostEqual(row["social_security"] / row["price_index"], 46_000 * 1.24)

    def test_care_cost_and_shortfall(self):
        a = replace(Assumptions(), care_start_year=2048, care_years=3, care_cost_today=90_000)
        self.assertAlmostEqual(summary(project(a))["total_care_cost_real"], 270_000)
        downside = summary(project(replace(Assumptions(), nominal_return=.04), 2036, -.20))
        self.assertEqual(downside["first_shortfall_year"], 2064)

    def test_invalid_spending_cut(self):
        with self.assertRaises(ValueError):
            project(replace(Assumptions(), discretionary_cut_today=30_000))


if __name__ == "__main__":
    unittest.main()
