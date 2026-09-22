"""Regenerate the three portfolio notebooks with the standard-library JSON writer."""

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
    md("""# 02 | Baseline retirement cash flow and estate review

This notebook establishes a common baseline for the decisions in Notebook 03. Elena and Marco retire in 2036, claim their illustrative benefits at age 67, and hold planned spending at $145,000 in 2026 dollars. Annual returns are fixed at 5% nominal and inflation at 2.5%. The model is deterministic, not a probability-of-success forecast. Withdrawals precede investment returns. The 18% reserve on portfolio withdrawals is a tax planning proxy, not an account-level tax calculation."""),
    code("""import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()))
import pandas as pd
import matplotlib.pyplot as plt
from financial_plan import Assumptions, project, summary

a = Assumptions()
base = pd.DataFrame(project(a))
report = summary(base.to_dict('records'))
display(pd.Series(report, name='Baseline result').to_frame())
print(f"2066 portfolio: ${report['age_95_portfolio_real']:,.0f} in 2026 purchasing power")"""),
    md("""## Where the retirement paycheck comes from

The first two retirement years precede both Social Security benefits. Elena begins her modeled benefit in 2038 and Marco in 2040. The annual withdrawal is the spending gap divided by 0.82 to allow an illustrative 18% tax reserve. The portfolio never uses the separate $100,000 emergency cash or home equity."""),
    code("""display(base.loc[base.year.between(2035, 2042),
                 ['year','age_a','age_b','opening','spending','social_security','portfolio_withdrawal','withdrawal_rate','ending']]
        .style.format({'opening':'${:,.0f}','spending':'${:,.0f}',
                       'social_security':'${:,.0f}','portfolio_withdrawal':'${:,.0f}',
                       'withdrawal_rate':'{:.1%}','ending':'${:,.0f}'}))
ret = base[base.retired]
fig, ax = plt.subplots(figsize=(9, 5))
for column, label in [('spending','Household spending'), ('social_security','Social Security'),
                      ('portfolio_withdrawal','Gross portfolio withdrawal')]:
    ax.plot(ret.year, ret[column] / ret.price_index / 1000, label=label)
ax.set(xlabel='Year', ylabel='Annual amount ($ thousands, 2026 dollars)',
       title='Baseline retirement cash flows')
ax.legend(); ax.grid(alpha=.2); plt.show()"""),
    md("""## Advisory interpretation

The initial 5.8% withdrawal rate warrants review because it occurs before Social Security income begins. The [Morningstar 2025 retirement-income study](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/The_State_of_Retirement_Income_2025.pdf) reports a 3.9% starting reference under its own 30-year assumptions. It is not a pass/fail test for this household. Notebook 03 compares actions the couple could take.

## Estate and implementation checklist

1. Reconcile wills or a trust with account beneficiaries, contingent beneficiaries, and property titles.
2. Review durable financial and health-care powers of attorney and advance directives with qualified counsel. [CFPB guidance](https://www.consumerfinance.gov/ask-cfpb/what-is-a-power-of-attorney-poa-en-1149/).
3. Price survivor, life, disability, and long-term-care protection; test a single-survivor budget in Notebook 03.
4. Review Roth conversions, withdrawal order, and RMD timing with a tax professional. [IRS RMD guidance](https://www.irs.gov/retirement-plans/retirement-plan-and-ira-required-minimum-distributions-faqs).
5. The [2026 federal estate basic exclusion is $15 million per person](https://www.irs.gov/instructions/i706), above the fictional current net worth. State-specific law and document execution still matter.

The baseline omits fees, return volatility, account-level taxes, Medicare premiums, and changes in law.""")
])

save("03_client_decisions.ipynb", [
    md("""# 03 | Client decisions and resilience

Four comparisons turn the financial plan into an advisory conversation: retirement timing, a spending response to a downturn, Social Security claiming, and care plus survivor needs. Every dollar amount in a scenario is an explicit illustration, not a prediction. The comparisons share a 5% nominal annual return and 2.5% inflation unless the same one-year 2036 downturn is imposed on both choices in the spending comparison. No success probability is claimed.

**Read the endpoint correctly:** 2066 is Elena's modeled age 95 and Marco's age 93. In the survivor case Elena dies in 2051, so the 2066 balance belongs to Marco's remaining household, not to Elena."""),
    code("""import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()))
from dataclasses import replace
import pandas as pd
import matplotlib.pyplot as plt
from financial_plan import Assumptions, project, summary

a = Assumptions()
def frame(assumptions=a, shock=False):
    return pd.DataFrame(project(assumptions, shock_year=2036 if shock else None,
                                shock_return=-.20 if shock else None))
def metrics(cases):
    records = {}
    for name, data in cases.items():
        s = summary(data.to_dict('records'))
        records[name] = {'Retire': s['retirement_year'],
                         'First withdrawal rate': s['first_year_rate'],
                         'Lowest real portfolio': s['lowest_retirement_balance_real'],
                         '2066 real portfolio': s['age_95_portfolio_real'],
                         'First shortfall': s['first_shortfall_year'] or 'None',
                         'Real spending cuts': s['total_spending_cuts_real'],
                         'Real care cost': s['total_care_cost_real']}
    return pd.DataFrame.from_dict(records, orient='index')
def show(cases):
    display(metrics(cases).style.format({
        'First withdrawal rate':'{:.1%}',
        'Lowest real portfolio':'${:,.0f}',
        '2066 real portfolio':'${:,.0f}',
        'Real spending cuts':'${:,.0f}',
        'Real care cost':'${:,.0f}'}))
def plot(cases, title):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for name, data in cases.items():
        r = data[data.retired]
        ax.plot(r.year, r.ending / r.price_index / 1e6, label=name)
    ax.axhline(.5, color='gray', linestyle=':', label='$500k real legacy goal')
    ax.set(xlabel='Year', ylabel='Portfolio ($ millions, 2026 dollars)', title=title)
    ax.legend(); ax.grid(alpha=.2); plt.show()
"""),
    md("""## Decision 1 — Retire in 2036 or work until 2038?

Both spouses work and continue modeled saving for two more years in the later-retirement case. The same spending target and claiming ages are used, so the comparison isolates the added contributions and two fewer withdrawal years. It does **not** value the time, health, or satisfaction from retiring earlier."""),
    code("""timing = {'Retire 2036': frame(),
          'Retire 2038': frame(replace(a, retirement_age_a=67))}
show(timing)
plot(timing, 'Retirement timing')
print('Trade-off: two more working years reduce the first-year portfolio withdrawal rate and increase the modeled 2066 balance.')"""),
    md("""## Decision 2 — Hold spending or make a temporary discretionary cut?

Both paths suffer the same illustrative 20% portfolio return in 2036. The flexible path cuts $25,000 a year in 2026 purchasing power during 2037–2039, reducing the $145,000 target to the stated $120,000 essential-spending floor for those years. Spending returns to the original target in 2040. This is a defined client choice, not an automatically optimized withdrawal rule. [Morningstar's retirement-income research](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/The_State_of_Retirement_Income_2025.pdf) discusses flexible spending methods; these exact cut amounts are our case assumptions."""),
    code("""flex_a = replace(a, discretionary_cut_today=25_000, cut_start_year=2037, cut_end_year=2039)
spending_cases = {'Maintain $145k target': frame(shock=True),
                  'Cut to $120k for 3 years': frame(flex_a, shock=True)}
show(spending_cases)
plot(spending_cases, 'Same downturn, different spending decisions')
display(spending_cases['Cut to $120k for 3 years'].loc[
    lambda x: x.year.between(2036, 2040),
    ['year','spending','spending_cut','portfolio_withdrawal','ending']]
    .style.format({'spending':'${:,.0f}','spending_cut':'${:,.0f}',
                   'portfolio_withdrawal':'${:,.0f}','ending':'${:,.0f}'}))"""),
    md("""## Decision 3 — Claim Elena's benefit at 67 or 70?

Marco claims at 67 in both paths. Delaying Elena's modeled $46,000 age-67 benefit to 70 raises it by 24% to $57,040 in 2026 dollars under the [SSA delayed-credit schedule](https://www.ssa.gov/benefits/retirement/planner/delayret.html). The household must fund three more years without Elena's benefit. The second comparison adds the same 2051 survivor transition to both paths. The model uses the higher of the two benefits as a simplified survivor-income proxy; actual survivor rules and benefit statements require an SSA review."""),
    code("""claiming = {'Elena claims 67': frame(),
            'Elena claims 70': frame(replace(a, claim_age_a=70))}
show(claiming)
display(pd.DataFrame({
    name: data.loc[data.year.between(2038, 2043), 'social_security'].to_numpy() /
          data.loc[data.year.between(2038, 2043), 'price_index'].to_numpy()
    for name, data in claiming.items()}, index=range(2038, 2044)).style.format('${:,.0f}'))
survivor_claiming = {'Claim 67, survivor in 2051': frame(replace(a, survivor_year=2051)),
                    'Claim 70, survivor in 2051': frame(replace(a, claim_age_a=70, survivor_year=2051))}
show(survivor_claiming)"""),
    md("""## Decision 4 — Fund care and protect the surviving spouse

Assume an extra $90,000 per year in 2026 purchasing power for care during 2048–2050. Then Elena dies in 2051; Marco's household spending falls from $145,000 to an assumed $110,000 real annually, and Social Security falls from two benefits to a simplified higher-benefit survivor proxy. Separate care-only and survivor-only paths reveal how each assumption changes the result. The 18% portfolio-withdrawal tax reserve remains fixed, so this is **not** a widow tax or long-term-care insurance analysis."""),
    code("""care_a = replace(a, care_start_year=2048, care_years=3, care_cost_today=90_000)
survivor_a = replace(a, survivor_year=2051)
combined_a = replace(care_a, survivor_year=2051)
life_events = {'No life event': frame(), 'Care only': frame(care_a),
               'Survivor only': frame(survivor_a), 'Care then survivor': frame(combined_a)}
show(life_events)
plot(life_events, 'Care expense and survivor cash flow')
display(life_events['Care then survivor'].loc[
    lambda x: x.year.between(2047, 2053),
    ['year','spending','care_cost','social_security','portfolio_withdrawal','ending']]
    .style.format({'spending':'${:,.0f}','care_cost':'${:,.0f}',
                   'social_security':'${:,.0f}','portfolio_withdrawal':'${:,.0f}',
                   'ending':'${:,.0f}'}))"""),
    md("""## Adviser recommendation and follow-up

1. Confirm the household's actual benefit statements, health costs, and essential-versus-discretionary budget. The 2038 retirement option materially reduces initial withdrawal pressure, but its lifestyle cost must be discussed.
2. Write a spending policy before retirement: identify the $25,000 of discretionary expenses that could be paused for three years. Agree on when the cut starts and ends; do not assume clients will accept it without discussion.
3. Compare Social Security claiming with individual life expectancy and survivor needs. Claiming at 70 raises the modeled benefit but requires more early portfolio cash.
4. Obtain long-term-care quotes and legal documents. The care and survivor costs are assumptions, while actual benefits, taxes, insurance, estate documents, and state law must be verified.
5. Recalculate annually. These deterministic paths omit return volatility beyond the stated shock, investment fees, tax-bracket interactions, Medicare premiums, RMDs, and changes in law. The 2066 balance is an illustration, not a guaranteed inheritance.

**Sources:** [SSA delayed credits](https://www.ssa.gov/benefits/retirement/planner/delayret.html), [SSA survivor-benefit overview](https://www.ssa.gov/benefits/retirement/planner/claiming.html), [Morningstar 2025 retirement-income research](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/The_State_of_Retirement_Income_2025.pdf), [IRS beneficiary guidance](https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-beneficiary).""")
])
