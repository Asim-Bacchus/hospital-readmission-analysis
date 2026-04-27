import pandas as pd
import numpy as np
from scipy import stats
import duckdb

con = duckdb.connect("db/readmissions.duckdb")
with open("sql/02_build_all_conditions_joined.sql") as f:
    con.execute(f.read())

readmissions = con.execute("SELECT * FROM all_readmissions").df()
hcahps = con.execute("SELECT facility_id, nurse_comm_stars FROM hcahps_kpis").df()
hcahps["nurse_comm_stars"] = pd.to_numeric(hcahps["nurse_comm_stars"], errors="coerce")
hcahps = hcahps.dropna(subset=["nurse_comm_stars"])

conditions = {
    "READM-30-HF-HRRP": "Heart Failure",
    "READM-30-COPD-HRRP": "COPD",
    "READM-30-PN-HRRP": "Pneumonia",
    "READM-30-AMI-HRRP": "Heart Attack (AMI)",
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee Replacement",
    "READM-30-CABG-HRRP": "Bypass Surgery (CABG)"
}

results = []
grouped_all = {}

for code, name in conditions.items():
    subset = readmissions[readmissions["condition"] == code].copy()
    merged = subset.merge(hcahps, on="facility_id", how="inner")
    merged = merged.dropna(subset=["nurse_comm_stars", "excess_ratio"])

    n = len(merged)
    r, p = stats.pearsonr(merged["nurse_comm_stars"], merged["excess_ratio"])
    rho, p_spearman = stats.spearmanr(merged["nurse_comm_stars"], merged["excess_ratio"])

    results.append({
        "Condition": name,
        "n": n,
        "Pearson r": round(r, 4),
        "Pearson p": round(p, 4),
        "Spearman rho": round(rho, 4),
        "Spearman p": round(p_spearman, 4)
    })

    grouped = merged.groupby("nurse_comm_stars")["excess_ratio"].agg(["mean", "count"]).reset_index()
    grouped.columns = ["nurse_comm_stars", "avg_ratio", "hospital_count"]
    grouped["condition"] = name
    grouped_all[name] = grouped

    print(f"\n{name} (n={n})")
    print(f"  Pearson r:    {r:.4f}  (p={p:.4f})")
    print(f"  Spearman rho: {rho:.4f}  (p={p_spearman:.4f})")
    print(grouped[["nurse_comm_stars", "avg_ratio", "hospital_count"]].to_string(index=False))

# Save summary table
summary = pd.DataFrame(results)
print("\n\nSUMMARY TABLE:")
print(summary.to_string(index=False))
summary.to_csv("data/processed/all_conditions_summary.csv", index=False)

# Save grouped data
all_grouped = pd.concat(grouped_all.values())
all_grouped.to_csv("data/processed/all_conditions_grouped.csv", index=False)