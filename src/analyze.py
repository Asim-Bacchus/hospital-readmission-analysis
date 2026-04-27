import pandas as pd
import numpy as np
from scipy import stats
import duckdb

# Run SQL pipeline first
con = duckdb.connect("db/readmissions.duckdb")
with open("sql/01_build_hf_joined.sql") as f:
    con.execute(f.read())

# Load joined data
df = pd.read_csv("data/processed/hf_nurse_comm_joined.csv")
df = df.dropna(subset=["nurse_comm_stars", "hf_excess_ratio"])
df["nurse_comm_stars"] = pd.to_numeric(df["nurse_comm_stars"], errors="coerce")
df = df.dropna()

print(f"Sample size: {len(df)} hospitals")
print(f"Nurse stars range: {df['nurse_comm_stars'].min()} - {df['nurse_comm_stars'].max()}")
print(f"HF ratio range: {df['hf_excess_ratio'].min():.4f} - {df['hf_excess_ratio'].max():.4f}")

# Pearson correlation
r, p = stats.pearsonr(df["nurse_comm_stars"], df["hf_excess_ratio"])
print(f"\nCorrelation (r): {r:.4f}")
print(f"P-value: {p:.4f}")

rho, p_spearman = stats.spearmanr(df["nurse_comm_stars"], df["hf_excess_ratio"])
print(f"Spearman rho: {rho:.4f}")
print(f"Spearman p-value: {p_spearman:.4f}")
# Grouped means by nurse star rating
grouped = df.groupby("nurse_comm_stars")["hf_excess_ratio"].agg(["mean", "count"]).reset_index()
grouped.columns = ["nurse_comm_stars", "avg_hf_ratio", "hospital_count"]
print("\nGrouped means:")
print(grouped.to_string(index=False))

# Save grouped summary
grouped.to_csv("data/processed/hf_grouped_summary.csv", index=False)