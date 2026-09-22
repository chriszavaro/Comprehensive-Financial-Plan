"""Checks for the material arithmetic and scenario behavior in the case study."""

import unittest

from financial_plan import Assumptions, federal_tax_mfj_2026, project, summary


class FinancialPlanTests(unittest.TestCase):
    def test_2026_joint_tax_layers(self):
        self.assertAlmostEqual(federal_tax_mfj_2026(300_000, 49_000), 37_708)
        self.assertEqual(federal_tax_mfj_2026(20_000), 0)

    def test_retirement_bridge_and_scenario(self):
        base = project()
        bridge = next(row for row in base if row['year'] == 2036)
        self.assertEqual(bridge['social_security'], 0)
        self.assertAlmostEqual(bridge['portfolio_withdrawal'], bridge['spending'] / .82)
        self.assertLess(next(row for row in base if row['year'] == 2040)['portfolio_withdrawal'], bridge['portfolio_withdrawal'])
        downside = summary(project(Assumptions(nominal_return=.04), 2036, -.20))
        self.assertEqual(downside['first_shortfall_year'], 2064)


if __name__ == '__main__':
    unittest.main()
