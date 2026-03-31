"""
Kenya Mental Health M&E Dataset Generator
==========================================
Simulates DHIS2-style monthly reporting data for 47 Kenyan counties.
Run this script to regenerate kenya_health_m_e_dataset.csv
"""

import pandas as pd
import numpy as np
import random

# ── Reproducibility ──────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Kenya Counties ────────────────────────────────────────────────────────────
COUNTIES = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
    "Meru", "Nyeri", "Kakamega", "Machakos", "Kitui",
    "Garissa", "Wajir", "Mandera", "Turkana", "Marsabit",
    "Isiolo", "Samburu", "Trans Nzoia", "Uasin Gishu", "Elgeyo Marakwet",
    "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok",
    "Kajiado", "Kericho", "Bomet", "Kakamega", "Vihiga",
    "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay",
    "Migori", "Kisii", "Nyamira", "Nairobi", "Kiambu",
    "Murang'a", "Kirinyaga", "Nyeri", "Nyandarua", "Meru",
    "Tharaka Nithi", "Embu"
]
# Deduplicate while preserving order
seen = set()
COUNTIES_UNIQUE = []
for c in COUNTIES:
    if c not in seen:
        seen.add(c)
        COUNTIES_UNIQUE.append(c)

# ── Facility Types per County ─────────────────────────────────────────────────
FACILITY_TEMPLATES = [
    "{county} County Referral Hospital",
    "{county} Sub-County Hospital",
    "{county} Health Centre A",
    "{county} Health Centre B",
    "{county} Community Dispensary",
]

# ── Reporting Period: Jan 2022 – Dec 2023 ─────────────────────────────────────
reporting_months = pd.date_range(start="2022-01-01", end="2023-12-01", freq="MS")

# ── Prevalence & Burden Lookup (county-level fixed characteristics) ────────────
county_base = {}
for county in COUNTIES_UNIQUE:
    county_base[county] = {
        "prevalence": round(np.random.uniform(0.08, 0.22), 4),   # 8–22%
        "burden_daly": round(np.random.uniform(1200, 4500), 1),  # DALYs per 100k
        "capacity_factor": round(np.random.uniform(0.4, 0.95), 2),
    }

# ── Build Dataset ─────────────────────────────────────────────────────────────
rows = []

for county in COUNTIES_UNIQUE:
    base = county_base[county]
    facilities = [t.format(county=county) for t in FACILITY_TEMPLATES]

    for facility in facilities:
        facility_factor = np.random.uniform(0.5, 1.2)  # facility-level variation

        for month in reporting_months:
            # Seasonal adjustment (higher burden in Jan, Jul)
            seasonal = 1.0 + 0.1 * np.sin(2 * np.pi * month.month / 12)

            screened = int(
                np.random.poisson(
                    lam=120 * base["capacity_factor"] * facility_factor * seasonal
                )
            )
            screened = max(screened, 5)  # floor

            # Treatment gap varies by county capacity
            gap_rate = round(np.random.uniform(0.25, 0.70), 4)
            treated = int(screened * (1 - gap_rate) * np.random.uniform(0.9, 1.1))
            treated = min(treated, screened)  # can't treat more than screened
            treated = max(treated, 0)

            treatment_gap = round(1 - (treated / screened), 4) if screened > 0 else 1.0

            rows.append({
                "county": county,
                "facility_name": facility,
                "reporting_month": month.strftime("%Y-%m-%d"),
                "mental_health_prevalence": base["prevalence"],
                "mental_health_burden_daly": base["burden_daly"],
                "patients_screened": screened,
                "patients_treated": treated,
                "treatment_gap": treatment_gap,
                "reporting_year": month.year,
                "reporting_quarter": f"Q{month.quarter}",
            })

df = pd.DataFrame(rows)

# ── Derived KPIs ──────────────────────────────────────────────────────────────
df["treatment_rate"] = (df["patients_treated"] / df["patients_screened"]).round(4)
df["unmet_need"] = df["patients_screened"] - df["patients_treated"]

# ── Export ────────────────────────────────────────────────────────────────────
output_path = "kenya_health_m_e_dataset.csv"
df.to_csv(output_path, index=False)

print(f"✅ Dataset generated: {output_path}")
print(f"   Rows    : {len(df):,}")
print(f"   Counties: {df['county'].nunique()}")
print(f"   Facilities: {df['facility_name'].nunique()}")
print(f"   Months  : {df['reporting_month'].nunique()}")
print(f"\nColumn summary:")
print(df.dtypes)
print(f"\nSample rows:")
print(df.head(3).to_string())
