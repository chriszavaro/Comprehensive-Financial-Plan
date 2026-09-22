"""Render reproducible, README-sized charts from the client scenario model."""

from dataclasses import replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from financial_plan import Assumptions, project

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
BASE = Assumptions()
NAVY = "#16324f"
TEAL = "#087e83"
ORANGE = "#c45d31"
PURPLE = "#7053a2"
GRAY = "#606c77"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#c6d0d8",
    "savefig.facecolor": "white",
})


def dollars_millions(value, _):
    return f"${value:.1f}m"


def setup(title, subtitle, y_label):
    fig, ax = plt.subplots(figsize=(9.4, 5.3))
    fig.subplots_adjust(left=.11, right=.97, top=.80, bottom=.27)
    ax.set_title(title, loc="left", color=NAVY, pad=24)
    ax.text(0, 1.025, subtitle, transform=ax.transAxes, color=GRAY, fontsize=9)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    ax.grid(axis="y", color="#dde4e9", linewidth=.8)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax


def legend_below(fig, ax):
    """Keep every key outside the plotting area."""
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(.5, .02),
               ncol=2, frameon=False, fontsize=9, columnspacing=2)


def real_portfolio(rows):
    return [r["ending"] / r["price_index"] / 1_000_000 for r in rows]


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)


def portfolio_chart(title, subtitle, cases, filename, markers=None):
    fig, ax = setup(title, subtitle, "Portfolio value (2026 dollars)")
    colors = [NAVY, TEAL, ORANGE, PURPLE]
    for (label, rows), color in zip(cases.items(), colors):
        retired = [r for r in rows if r["retired"]]
        ax.plot([r["year"] for r in retired], real_portfolio(retired),
                label=label, color=color, linewidth=2.7)
    ax.axhline(.5, linestyle=":", color=GRAY, linewidth=1.2,
               label="$500k real legacy goal")
    if markers:
        for start, end, label in markers:
            if end is None:
                ax.axvline(start, color=GRAY, linestyle="--", linewidth=1)
            else:
                ax.axvspan(start, end, color="#e7eef0", alpha=.8)
    ax.yaxis.set_major_formatter(FuncFormatter(dollars_millions))
    legend_below(fig, ax)
    save(fig, filename)


portfolio_chart(
    "What changes if retirement moves to 2038?",
    "Same spending and claiming assumptions; two additional working years.",
    {"Retire in 2036": project(BASE),
     "Retire in 2038": project(replace(BASE, retirement_age_a=67))},
    "retirement_timing.png",
)

portfolio_chart(
    "What if spending adjusts after a downturn?",
    "Both paths experience the same 20% portfolio loss in 2036.",
    {"Maintain planned spending": project(BASE, 2036, -.20),
     "Cut discretionary spending in 2037–2039": project(
         replace(BASE, discretionary_cut_today=25_000,
                 cut_start_year=2037, cut_end_year=2039), 2036, -.20)},
    "flexible_spending.png",
    markers=[(2037, 2039, "Spending cut")],
)

fig, ax = setup(
    "What changes when Elena delays Social Security?",
    "Marco claims at 67 in both paths; amounts shown in 2026 purchasing power.",
    "Annual household Social Security (2026 dollars)",
)
for label, rows, color in [
    ("Elena claims at 67", project(BASE), NAVY),
    ("Elena claims at 70", project(replace(BASE, claim_age_a=70)), TEAL),
]:
    years = [r["year"] for r in rows if 2036 <= r["year"] <= 2046]
    benefit = [r["social_security"] / r["price_index"] / 1000
               for r in rows if 2036 <= r["year"] <= 2046]
    ax.step(years, benefit, where="post", label=label, color=color, linewidth=2.7)
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}k"))
legend_below(fig, ax)
save(fig, "social_security_claiming.png")

care_survivor = replace(BASE, care_start_year=2048, care_years=3,
                        care_cost_today=90_000, survivor_year=2051)
portfolio_chart(
    "What if care is needed before a survivor transition?",
    "Care costs in 2048–2050; Marco becomes the surviving spouse in 2051.",
    {"Baseline": project(BASE), "Care, then survivor": project(care_survivor)},
    "care_and_survivor.png",
    markers=[(2048, 2050, "Care costs"), (2051, None, "Survivor")],
)
print("Rendered", ", ".join(p.name for p in sorted(OUT.glob("*.png"))))
