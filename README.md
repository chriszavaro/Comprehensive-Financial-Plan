# Comprehensive Financial Plan

A fictional, client-facing wealth management case study built with three executed Python notebooks. It moves from discovery to baseline cash flows, then tests decisions a household can make. All dollars are illustrative as of September 2026.

## Executive recommendation

Elena and Marco can provisionally target retirement in 2036, but the first modeled portfolio withdrawal is **5.8%** because both Social Security benefits begin later. Working through 2038 reduces that opening rate to **3.6%** and raises the modeled 2066 portfolio from **$2.12 million to $3.13 million in 2026 purchasing power**. That extra security requires two more working years. The choice should be made only after confirming their budget, benefit statements, health coverage, and willingness to adjust discretionary spending.

| Client decision | Compared paths | Key modeled result |
|---|---|---|
| **When to retire?** | 2036 versus 2038 | First withdrawal rate 5.8% versus 3.6%; 2066 real portfolio $2.12m versus $3.13m |
| **How to respond to a downturn?** | Keep $145k real spending versus cut to a $120k essential floor for 2037–2039 after the same 2036 loss | Three $25k real cuts preserve about $189k more real portfolio value by 2066 ($831k versus $643k) |
| **When should Elena claim Social Security?** | Claim at 67 versus 70; Marco claims at 67 in both | Elena's assumed 2026-dollar benefit rises from $46k to $57,040; 2066 real portfolio $2.12m versus $2.29m |
| **Can the survivor absorb care costs?** | Base versus $90k real annual care costs in 2048–2050 and Elena's death in 2051 | Care-then-survivor path ends 2066 at about $1.67m real; Marco is age 93 |

The 2036 downturn in the spending comparison is an assumed **20% investment return loss for that one year in both paths**. It isolates the spending choice rather than presenting a market-return assumption as a recommendation. All paths are deterministic illustrations, **not probabilities of success**.

## Fictional client profile

Elena (55) and Marco (53) are married, file jointly, and earn $180,000 and $120,000. Their two adult children are financially independent. They would like to retire together when Elena turns 65 in 2036, spend **$145,000 annually in 2026 purchasing power**, preserve a **$120,000 essential-spending floor**, and leave at least **$500,000 real** to heirs if feasible. Their risk tolerance is moderate.

| Balance sheet item, 2026 | Amount |
|---|---:|
| Tax-deferred retirement accounts | $1,250,000 |
| Roth accounts | $350,000 |
| Taxable investments | $250,000 |
| **Investable retirement portfolio** | **$1,850,000** |
| Emergency cash | $100,000 |
| Home / mortgage | $850,000 / $250,000 |
| **Net worth** | **$2,550,000** |

The plan assumes $49,000 of combined 2026 employer-plan deferrals and $16,000 of other saving, or **$65,000** first-year saving. Current spending is sketched at $155,000. With the $32,200 joint standard deduction, modeled taxable income is $218,800, estimated regular federal ordinary tax is **$37,708**, and the marginal bracket is **24%**. Payroll, state, and local taxes still require reconciliation with real pay stubs. Sources: [IRS 2026 contribution limits](https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions) and [IRS 2026 tax adjustments](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill).

## Model and scenario assumptions

- Saving starts at $65,000 and grows 2% each year until retirement. The base portfolio return is a constant 5% nominal annually. Inflation is 2.5%.
- Planned retirement spending starts at $145,000 in 2026 dollars. Social Security benefits start at illustrative age-67 amounts of $46,000 for Elena and $32,000 for Marco. Actual SSA statements are required.
- Gross portfolio withdrawals equal the spending gap after Social Security divided by 0.82. The 18% tax reserve is a planning proxy, not a federal or state tax projection. Withdrawals occur at the beginning of each year.
- Delaying Elena's claim from 67 to 70 adds 8% of the age-67 benefit for each year, reaching 124% at 70, consistent with the [SSA delayed-credit schedule](https://www.ssa.gov/benefits/retirement/planner/delayret.html). The model compares annual ages rather than exact claiming months.
- The flexible-spending path cuts $25,000 in 2026 dollars in 2037, 2038, and 2039, then restores planned spending. The separate $100,000 emergency cash and home are excluded from portfolio withdrawals.
- The care/survivor case adds $90,000 real care expense for three years. In 2051, Marco's assumed single-person spending becomes $110,000 real and household Social Security becomes the higher modeled benefit rather than the sum. This is a simplified survivor proxy. [SSA explains survivor claiming options](https://www.ssa.gov/benefits/retirement/planner/claiming.html).

The [Morningstar 2025 retirement-income study](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/The_State_of_Retirement_Income_2025.pdf) provides context for flexible withdrawals and a 3.9% starting reference under its own assumptions. That reference is not a pass/fail test for this household.

## Advisory action plan

1. **Validate discovery:** obtain pay stubs, tax returns, account statements and cost basis, debt terms, benefit estimates, insurance, wills, trust documents, and beneficiary forms. Confirm essential and discretionary expenses.
2. **Choose retirement timing:** discuss the value of two additional working years against health, family, and lifestyle priorities. Price coverage before Medicare eligibility and re-run the plan with actual fees, taxes, and account allocations.
3. **Set a spending policy:** identify the specific $25,000 of discretionary expenses that could be paused after a severe decline. Agree on the start, review, and restoration rules with the clients.
4. **Coordinate claiming and survivor needs:** compare actual SSA estimates at 67 and 70, single-survivor cash flow, life insurance, and long-term-care funding choices. Review beneficiary designations and property titles with an estate attorney.
5. **Review taxes and estate documents:** assess withdrawal order, Roth conversions, eventual [required minimum distributions](https://www.irs.gov/retirement-plans/retirement-plan-and-ira-required-minimum-distributions-faqs), durable powers of attorney, and advance directives. The [2026 federal estate basic exclusion is $15 million per person](https://www.irs.gov/instructions/i706), above this fictional current net worth, but state-specific law and document execution still matter.

## Reproduce

Install Python 3.11 or later and the packages in [requirements.txt](requirements.txt). Open Jupyter Lab from the repository root and run these notebooks in order:

1. [01_client_profile.ipynb](notebooks/01_client_profile.ipynb) — discovery, balance sheet, current tax and cash-flow context.
2. [02_retirement_and_estate.ipynb](notebooks/02_retirement_and_estate.ipynb) — baseline retirement paycheck and estate checklist.
3. [03_client_decisions.ipynb](notebooks/03_client_decisions.ipynb) — four decision comparisons, charts, and adviser follow-up.

The notebooks include saved outputs. [financial_plan.py](financial_plan.py) contains the model and [test_financial_plan.py](test_financial_plan.py) checks its material mechanics. Run build_notebooks.py to regenerate blank notebooks, then execute them to refresh outputs.

## Limits

This is an educational portfolio example, not individualized financial, investment, tax, or legal advice. Constant annual returns, one specified loss, fixed inflation, and a fixed tax reserve cannot capture market volatility, investment fees, account-level taxes, Social Security taxation, Medicare premiums, exact benefit rules, RMDs, state estate law, or changes in legislation. Care costs and survivor spending are hypothetical. No Monte Carlo success rate, safe withdrawal rate, or guaranteed inheritance is claimed.
