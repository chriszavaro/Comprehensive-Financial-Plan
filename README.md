# Comprehensive Financial Plan

A fictional wealth management case study that connects client discovery, cash flow, retirement income, risk, and estate planning. Two executed Python notebooks contain the calculations and a chart. All amounts are illustrative U.S. dollars as of September 2026.

## Executive recommendation

The Rivera household can provisionally target retirement in 2036, subject to validating Social Security estimates and funding the bridge years. The first retirement withdrawal is **$226,356, or 5.8%** of a **$3.90 million** opening portfolio. The base path ends at Elena's age 95 with **$2.12 million in 2026 purchasing power**. A combined market loss and lower-return path first runs short in **2064**. Retirement timing and spending need annual review.

| Metric | Base: 5% return | 20% loss in 2036 | 4% return | Combined downside |
|---|---:|---:|---:|---:|
| Portfolio at 2036 retirement | $3.90m | $3.90m | $3.59m | $3.59m |
| First-year gross withdrawal | $226k | $226k | $226k | $226k |
| First-year withdrawal rate | 5.8% | 5.8% | 6.3% | 6.3% |
| Age-95 ending portfolio, nominal | $5.70m | $1.73m | $2.09m | $0 |
| First funding shortfall | None through age 95 | None through age 95 | None through age 95 | 2064, age 93 |

These are fixed-assumption paths, **not probabilities of success**. The combined downside applies a 20% loss in 2036 and 4% nominal returns in all other years.

## Fictional client profile

Elena (55) and Marco (53) are married and file jointly. They earn $180,000 and $120,000. Their two adult children are financially independent. They want to retire together when Elena turns 65 in 2036, spend **$145,000 per year in 2026 purchasing power**, and preserve a **$500,000 real legacy** if retirement funding permits. Their risk tolerance is moderate and they are willing to trim discretionary spending after sustained losses.

| Balance sheet item, 2026 | Amount |
|---|---:|
| Tax-deferred retirement accounts | $1,250,000 |
| Roth accounts | $350,000 |
| Taxable investments | $250,000 |
| **Investable retirement portfolio** | **$1,850,000** |
| Emergency cash | $100,000 |
| Home / mortgage | $850,000 / $250,000 |
| **Net worth** | **$2,550,000** |

Annual gross pay is $300,000. The plan assumes $49,000 of combined employer-plan deferrals and $16,000 of other saving, for **$65,000** first-year saving. Current household spending is sketched at $155,000. Using the 2026 joint standard deduction of $32,200, taxable income is $218,800, estimated regular federal ordinary tax is **$37,708**, and the marginal bracket is **24%**. The remaining cash must cover payroll, state, and local taxes and reconcile with pay stubs. The $24,500 individual 401(k) limit and tax inputs come from the [IRS contribution limits](https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions) and [IRS 2026 tax adjustments](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill).

## Retirement cash-flow design

- **Accumulation:** $65,000 first-year saving grows 2% annually until 2036. Base portfolio return is 5% nominal.
- **Spending:** $145,000 in 2026 dollars inflates 2.5% annually. Actual health insurance costs have not been quoted.
- **Social Security:** Illustrative age-67 benefits are $46,000 for Elena and $32,000 for Marco, stated in 2026 dollars. Benefits begin in 2038 and 2040. The [SSA lists full retirement age 67](https://www.ssa.gov/planners/retire/1960.html) for both; actual statements are needed.
- **Withdrawals:** The spending gap after Social Security is divided by 0.82 to add an 18% tax reserve. This is a planning proxy, not an account-level tax calculation.
- **Timing:** Withdrawals occur at the start of each year and returns afterward. Emergency cash and home equity are excluded from the retirement portfolio.

The 5.8% first-year rate exceeds the **3.9% starting reference** in [Morningstar's 2025 retirement-income research](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltb73b87c5d0c70ead/692f43f57737a31596684522/working_file_11.19_FINAL_REVISE.pdf). Its 30-year, 90%-of-funds-remaining result uses different assumptions, so it is a comparison point rather than a pass/fail rule. Social Security later reduces portfolio demand here. Use a 5% current withdrawal rate as an illustrative review trigger: pause discretionary increases and revisit the plan when it is exceeded.

## Holistic advisory actions

1. **Now:** reconcile pay stubs, tax returns, account statements and cost basis, mortgage terms, insurance, and Social Security benefit estimates. Confirm saving and retirement spending.
2. **Before 2036:** earmark liquid assets for the Social Security bridge, set an investment policy and rebalancing rules, and price health coverage through Medicare eligibility. Re-run the model with actual fees, taxes, and holdings.
3. **Each retirement year:** review the funded withdrawal rate, spending, survivor needs, tax brackets, Roth-conversion opportunities, and required minimum distributions. The [IRS RMD guidance](https://www.irs.gov/retirement-plans/retirement-plan-and-ira-required-minimum-distributions-faqs) informs future review; RMDs are not implemented here.
4. **Estate and protection:** reconcile wills or a trust with beneficiaries and property titles; name contingent beneficiaries and successor decision-makers; review durable financial and health-care powers of attorney, advance directives, life and disability coverage, and long-term-care funding. The [CFPB explains durable financial powers of attorney](https://www.consumerfinance.gov/ask-cfpb/what-is-a-power-of-attorney-poa-en-1149/). The [2026 federal estate basic exclusion is $15 million per person](https://www.irs.gov/instructions/i706), above this household's illustrative net worth. State-specific law and document execution need an attorney's review.

## Run the notebooks

Install Python 3.11 or later and the packages in [requirements.txt](requirements.txt). Open Jupyter Lab from the repository root. Run [01_client_profile.ipynb](notebooks/01_client_profile.ipynb), then [02_retirement_and_estate.ipynb](notebooks/02_retirement_and_estate.ipynb). Both notebooks have saved outputs. [financial_plan.py](financial_plan.py) contains the model. Run build_notebooks.py to regenerate blank notebooks, then execute them to refresh outputs.

## Scope and limitations

This is an educational portfolio example, not individualized financial, tax, investment, or legal advice. The model assumes constant returns except for one specified shock. It omits volatility, fees, account-level tax treatment, Social Security taxation, Medicare and health-insurance detail, RMDs, survivor transitions, state estate law, and future tax changes. No Monte Carlo success rate or safe withdrawal rate is claimed. A real plan requires client documents and tax and legal review.
