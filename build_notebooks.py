"""Regenerate the two portfolio notebooks with the standard-library JSON writer."""

import json
import hashlib
from pathlib import Path


def md(source):
    return {"cell_type": "markdown", "id": hashlib.sha1(source.encode()).hexdigest()[:8], "metadata": {}, "source": source.splitlines(True)}


def code(source):
    return {"cell_type": "code", "id": hashlib.sha1(source.encode()).hexdigest()[:8], "execution_count": None, "metadata": {},
            "outputs": [], "source": source.splitlines(True)}


def save(name, cells):
    Path("notebooks").mkdir(exist_ok=True)
    payload = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
              "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    Path("notebooks", name).write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")


save("01_client_profile.ipynb", [
    md("""# 01 | Client discovery and planning baseline

**Rivera household — fictional case, September 2026.** Both spouses are assumed to be U.S. residents filing jointly. All dollar figures are illustrative, not client records. The goal is to show how an adviser frames tradeoffs and identifies missing data before a recommendation."""),
    md("""## Discovery snapshot

| Topic | Working assumption |
|---|---|
| Elena / Marco | Ages 55 / 53; both employed; retirement target when Elena turns 65 (2036) |
| Income | $180,000 / $120,000 gross salary; $300,000 combined |
| Family | Two financially independent adult children; support for aging parent is a possible future expense |
| Goals | Retire together in 2036; spend $145,000 a year in 2026 purchasing power; leave at least $500,000 real to heirs if feasible |
| Risk | Moderate; willing to reduce discretionary spending after sustained losses, but wants a cash buffer |
| Social Security | Illustrative age-67 benefits of $46,000 / $32,000 annually in 2026 dollars; verify with SSA statements |
| Residence | New York assumed for context; state and local tax are outside the numerical model |

**Key missing documents:** pay stubs and tax returns, account statements and cost basis, Social Security estimates, insurance policies, pension details, mortgages, beneficiary forms, wills, and health coverage options."""),
    code("""import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()))
import pandas as pd
from financial_plan import Assumptions, federal_tax_mfj_2026

a = Assumptions()
assets = {'Tax-deferred retirement': 1_250_000, 'Roth accounts': 350_000,
          'Taxable investments': 250_000, 'Emergency cash': 100_000,
          'Home': 850_000}
liabilities = {'Mortgage': 250_000}
balance_sheet = pd.DataFrame({'Assets': pd.Series(assets), 'Liabilities': pd.Series(liabilities)}).fillna(0)
display(balance_sheet.style.format('${:,.0f}'))
print(f'Investable portfolio: ${a.portfolio:,.0f}')
print(f'Net worth including home and cash: ${sum(assets.values())-sum(liabilities.values()):,.0f}')"""),
    md("""## Current cash flow and tax context

The couple contributes $49,000 to employer plans in 2026 ($24,500 each), then saves another $16,000 across taxable and other accounts. The simplified federal calculation uses the 2026 joint standard deduction and ordinary brackets. It excludes payroll, New York, investment, credit, and other tax provisions; the unallocated cash is **not** a claimed surplus."""),
    code("""gross = 300_000
deferrals = 49_000
spending = 155_000
other_savings = 16_000
federal = federal_tax_mfj_2026(gross, deferrals)
cash_flow = pd.Series({'Gross pay': gross, 'Employer-plan deferrals': -deferrals,
                       'Illustrative federal income tax': -federal,
                       'Current spending': -spending, 'Other saving': -other_savings,
                       'Remainder for payroll/state/local taxes and reconciliation': -(gross-deferrals-federal-spending-other_savings)})
display(cash_flow.to_frame('2026 amount').style.format('${:,.0f}'))
print(f'Federal ordinary tax estimate: ${federal:,.0f}; taxable income: ${gross-deferrals-32_200:,.0f}; marginal bracket: 24%')"""),
    md("""## Planning interpretation

The $65,000 annual savings assumption fits the balance sheet and cash-flow sketch, but must be reconciled with actual payroll and state taxes. The portfolio excludes $100,000 emergency cash and home equity because neither is assumed to fund regular retirement spending. Treat the estate goal as a secondary objective until healthcare, longevity, and survivor needs have been stress tested.

**Sources:** [IRS tax brackets and deduction](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill), [IRS 401(k) limit](https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions), [SSA full retirement age](https://www.ssa.gov/planners/retire/1960.html).""")
])

save("02_retirement_and_estate.ipynb", [
    md("""# 02 | Retirement income, stress test, and estate review

The annual model is deterministic and **does not estimate a probability of success**. It shows whether the stated assumptions support the spending target and how a large loss at retirement changes the path. All spending and Social Security inputs are in 2026 dollars and inflate 2.5% yearly. The portfolio return is a nominal, constant 5% base case; contributions grow 2% until retirement. Portfolio withdrawals occur before each year's return. The 18% withdrawal tax reserve is a planning proxy, not a tax calculation."""),
    code("""import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()))
import pandas as pd
import matplotlib.pyplot as plt
from financial_plan import Assumptions, project, summary

a = Assumptions()
base = pd.DataFrame(project(a))
stress = pd.DataFrame(project(a, shock_year=2036, shock_return=-0.20))
low_return = pd.DataFrame(project(Assumptions(nominal_return=0.04)))
combined = pd.DataFrame(project(Assumptions(nominal_return=0.04), shock_year=2036, shock_return=-0.20))
cases = pd.DataFrame({name: summary(frame.to_dict('records')) for name, frame in
                      [('Base: 5% nominal', base), ('2036 loss: -20%', stress), ('4% nominal', low_return), ('Combined downside', combined)]}).T
display(cases.style.format({'retirement_portfolio':'${:,.0f}', 'first_year_withdrawal':'${:,.0f}',
                            'first_year_rate':'{:.1%}', 'age_95_portfolio':'${:,.0f}'}))"""),
    md("""## Retirement paycheck

The couple retires in 2036. Elena's modeled Social Security begins at age 67 in 2038; Marco's begins at 67 in 2040. The two bridge years have the highest starting withdrawal pressure. The model does not optimize claiming ages or calculate taxation of Social Security, Medicare premiums, ACA coverage, capital gains, RMDs, or individual account withdrawal order."""),
    code("""display(base.loc[base.year.between(2035, 2042),
                 ['year','age_a','age_b','opening','spending','social_security','portfolio_withdrawal','withdrawal_rate','ending']]
        .style.format({'opening':'${:,.0f}','spending':'${:,.0f}',
                       'social_security':'${:,.0f}','portfolio_withdrawal':'${:,.0f}',
                       'withdrawal_rate':'{:.1%}','ending':'${:,.0f}'}))
fig, ax = plt.subplots(figsize=(9, 5))
for label, frame in [('Base',base), ('20% loss at retirement',stress), ('4% return',low_return), ('Combined downside',combined)]:
    ax.plot(frame.age_a, frame.ending / 1e6 / (1+a.inflation)**(frame.year-a.start_year), label=label)
ax.axhline(.5, color='gray', linestyle=':', label='$500k real legacy goal')
ax.set(xlabel='Elena age', ylabel='Year-end portfolio ($ millions, 2026 dollars)', title='Illustrative portfolio paths')
ax.legend(); ax.grid(alpha=.2); plt.show()"""),
    md("""## Withdrawal guardrail and adviser judgment

Compare the first retirement withdrawal with the opening retirement portfolio and the [Morningstar 2025 base-case 3.9% starting rate](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/692f43f57737a31596684522/working_file_11.19_FINAL_REVISE.pdf), which assumes a 30-year horizon and 90% probability of funds remaining under its own capital-market assumptions. This case has a two-year Social Security bridge and a roughly 30-year horizon, so 3.9% is only a reference point. An adviser should review an annual guardrail: if the current withdrawal rate rises above 5%, pause discretionary increases and revisit the plan; below 4%, review whether spending or gifting can rise. These thresholds are illustrative policy choices, not proven safe rates."""),
    code("""retirement = base[base.retired].iloc[0]
print(f'Opening retirement portfolio: ${retirement.opening:,.0f}')
print(f'First-year gross portfolio withdrawal: ${retirement.portfolio_withdrawal:,.0f}')
print(f'First-year withdrawal rate: {retirement.withdrawal_rate:.2%}')
print(f'Base age-95 portfolio in 2026 dollars: ${base.iloc[-1].ending/(1+a.inflation)**(base.iloc[-1].year-a.start_year):,.0f}')
print(f'Loss scenario age-95 portfolio in 2026 dollars: ${stress.iloc[-1].ending/(1+a.inflation)**(stress.iloc[-1].year-a.start_year):,.0f}')"""),
    md("""## Estate, protection, and implementation checklist

1. **Title and beneficiaries:** reconcile the will or revocable trust with retirement-account and life-insurance beneficiary designations. Check contingent beneficiaries and whether assets pass outside probate.
2. **Incapacity:** have a qualified attorney prepare or review durable financial and health-care powers of attorney, advance directives, and any trust documents under the relevant state law. Name successors.
3. **Survivor and insurance risk:** review term-life coverage before retirement, disability coverage while working, long-term-care funding choices, and the cash needs of the surviving spouse. A single-survivor tax and Social Security model remains to be built from real client data.
4. **Estate tax:** the 2026 federal basic exclusion is $15 million per person. The current illustrative net worth is well below that level, so execution, beneficiary coordination, and state-specific law are more immediate than federal estate tax minimization. Future law and appreciation require review.
5. **Tax coordination:** review Roth conversions during lower-income years, investment location, RMD timing, charitable intent, and capital-gain realization with a tax professional. The present notebook does not optimize these decisions.

**Sources:** [IRS estate exclusion](https://www.irs.gov/instructions/i706), [CFPB durable financial power of attorney](https://www.consumerfinance.gov/ask-cfpb/what-is-a-power-of-attorney-poa-en-1149/), [IRS RMD FAQ](https://www.irs.gov/retirement-plans/retirement-plan-and-ira-required-minimum-distributions-faqs).""")
])


