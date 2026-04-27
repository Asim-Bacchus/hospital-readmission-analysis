import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load grouped summary
grouped = pd.read_csv("data/processed/hf_grouped_summary.csv")

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#FAFAF8")
ax.set_facecolor("#FAFAF8")

colors = ["#A83C2A", "#C17A3A", "#D4A03A", "#6B9E8F", "#4A7C6F"]
bars = ax.bar(grouped["nurse_comm_stars"], grouped["avg_hf_ratio"],
              color=colors, width=0.6, zorder=3)

# Value labels and sample sizes
for bar, val, n in zip(bars, grouped["avg_hf_ratio"], grouped["hospital_count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0008,
            f"{val:.3f}", ha="center", va="bottom", fontsize=12,
            fontweight="bold", fontfamily="serif", color="#1a1a1a")
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.003,
            f"n={n}", ha="center", va="top", fontsize=9,
            fontfamily="serif", color="#ffffff")

# Benchmark line
ax.axhline(1.0, color="#555", linestyle="--", linewidth=1.2, zorder=2)
ax.text(5.42, 1.0005, "Expected = 1.00", va="bottom", ha="right",
        fontsize=9, color="#555", fontfamily="serif", fontstyle="italic")

ax.set_ylim(0.96, 1.05)
ax.set_xlabel("Nurse Communication Star Rating", fontsize=12, fontfamily="serif", labelpad=10)
ax.set_ylabel("Avg Excess Readmission Ratio (HF)", fontsize=12, fontfamily="serif", labelpad=10)
ax.set_title("Heart Failure Readmissions\nby Nurse Communication Rating",
             fontsize=15, fontweight="bold", fontfamily="serif", pad=16)

fig.text(0.5, 0.93, "CMS Data · 2,520 U.S. Hospitals · 2021–2024 Readmission Window",
         ha="center", fontsize=9, color="#888", fontfamily="serif")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#ddd")
ax.spines["bottom"].set_color("#ddd")
ax.tick_params(colors="#555", labelsize=11)
ax.yaxis.grid(True, color="#e8e8e8", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("dashboard/figures/01_hf_nurse_comm.png", dpi=180,
            bbox_inches="tight", facecolor="#FAFAF8")
print("Figure saved.")

import pandas as pd
import matplotlib.pyplot as plt

# Load summary data
summary = pd.read_csv("data/processed/all_conditions_summary.csv")
summary = summary.sort_values("Pearson r")

fig, ax = plt.subplots(figsize=(11, 6.5))
fig.patch.set_facecolor("#FAFAF8")
ax.set_facecolor("#FAFAF8")

colors = ["#4A7C6F", "#4A7C6F", "#6B9E8F", "#6B9E8F", "#C17A3A", "#C17A3A"]
bars = ax.barh(summary["Condition"], summary["Pearson r"], color=colors, height=0.55, zorder=3)

for bar, val in zip(bars, summary["Pearson r"]):
    ax.text(val - 0.002, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}", ha="right", va="center", fontsize=11,
            fontweight="bold", fontfamily="serif", color="#d0d0d0")

ax.axvline(0, color="#888", linewidth=1.0, zorder=2)

ax.set_xlabel("Correlation with Nurse Communication Rating (r)",
              fontsize=11, fontfamily="serif", labelpad=10)
ax.set_title("Nurse Communication vs Readmission Ratio\nAcross All Six CMS Conditions",
             fontsize=15, fontweight="bold", fontfamily="serif", pad=16)

fig.text(0.5, 0.93,
         "Better nurse communication aligned with lower readmissions across all six conditions",
         ha="center", fontsize=11.5, color="#333", fontfamily="serif", fontstyle="italic")

fig.text(0.5, 0.01,
         "Pearson correlations shown · All p < 0.05 · Source: CMS Hospital Data",
         ha="center", fontsize=8.5, color="#999", fontfamily="serif")

ax.set_xlim(-0.23, 0.02)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#ddd")
ax.spines["bottom"].set_color("#ddd")
ax.tick_params(colors="#555", labelsize=11)
ax.xaxis.grid(True, color="#e8e8e8", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout(rect=[0, 0.04, 1, 0.92])
plt.savefig("dashboard/figures/02_correlation_by_condition.png", dpi=180,
            bbox_inches="tight", facecolor="#FAFAF8")
print("Figure saved.")