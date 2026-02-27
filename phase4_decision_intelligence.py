import pandas as pd
import os

# ──────────────────────────────────────────────
# PHASE 4: DECISION INTELLIGENCE ENGINE
# ──────────────────────────────────────────────

# ── LOAD KPI DATA FROM PHASE 3 ──
df          = pd.read_csv("data/featured_data.csv", parse_dates=["Order Date", "Ship Date"])
kpi_cat     = pd.read_csv("data/kpi_category.csv")
kpi_region  = pd.read_csv("data/kpi_regional.csv")

print("=" * 60)
print("DECISIONFORGE — PHASE 4: DECISION INTELLIGENCE ENGINE")
print("=" * 60)

# ──────────────────────────────────────────────
# HELPER: SCORING FUNCTION
# ──────────────────────────────────────────────

def min_max_score(series, weight):
    """Scale a series to 0–weight range using min-max normalization."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([weight / 2] * len(series), index=series.index)
    return ((series - min_val) / (max_val - min_val) * weight).round(2)

# ──────────────────────────────────────────────
# HELPER: CLASSIFICATION FUNCTION
# ──────────────────────────────────────────────

def classify(score):
    if score >= 70:
        return "🟢 Core"
    elif score >= 45:
        return "🟡 Opportunity"
    elif score >= 20:
        return "🔴 Risk"
    else:
        return "⚪ Low Priority"

# ──────────────────────────────────────────────
# PART A: SUB-CATEGORY DECISION INTELLIGENCE
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PART A — SUB-CATEGORY INTELLIGENCE")
print("=" * 60)

# ── Calculate Year over Year Growth per Sub-Category ──
yearly_subcat = df.groupby(["Sub-Category", "Order Year"])["Sales"].sum().reset_index()
yearly_subcat = yearly_subcat.sort_values(["Sub-Category", "Order Year"])
yearly_subcat["Growth"] = yearly_subcat.groupby("Sub-Category")["Sales"].pct_change()

# Average growth per sub-category
avg_growth = yearly_subcat.groupby("Sub-Category")["Growth"].mean().reset_index()
avg_growth.columns = ["Sub-Category", "Avg_Growth"]

# Merge growth into category KPI
sc = kpi_cat.merge(avg_growth, on="Sub-Category", how="left")
sc["Avg_Growth"] = sc["Avg_Growth"].fillna(0)

# ── Score Each Component ──
sc["Revenue_Score"] = min_max_score(sc["Total_Sales"],     40)
sc["Profit_Score"]  = min_max_score(sc["Avg_Margin_Pct"],  40)
sc["Growth_Score"]  = min_max_score(sc["Avg_Growth"],      20)

# ── Total Score ──
sc["Total_Score"] = (sc["Revenue_Score"] + sc["Profit_Score"] + sc["Growth_Score"]).round(2)

# ── Classify ──
sc["Classification"] = sc["Total_Score"].apply(classify)

# ── Sort by Score ──
sc = sc.sort_values("Total_Score", ascending=False).reset_index(drop=True)

# ── Print Results ──
print(f"\n{'Sub-Category':<20} {'Score':>7} {'Classification':<20} {'Margin%':>9} {'Sales':>12}")
print("-" * 75)
for _, row in sc.iterrows():
    print(f"{row['Sub-Category']:<20} {row['Total_Score']:>7} {row['Classification']:<20} {row['Avg_Margin_Pct']:>8}% ${row['Total_Sales']:>11,.0f}")

# ──────────────────────────────────────────────
# PART B: REGIONAL DECISION INTELLIGENCE
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PART B — REGIONAL INTELLIGENCE")
print("=" * 60)

# ── Calculate Year over Year Growth per Region ──
yearly_region = df.groupby(["Region", "Order Year"])["Sales"].sum().reset_index()
yearly_region = yearly_region.sort_values(["Region", "Order Year"])
yearly_region["Growth"] = yearly_region.groupby("Region")["Sales"].pct_change()

avg_growth_region = yearly_region.groupby("Region")["Growth"].mean().reset_index()
avg_growth_region.columns = ["Region", "Avg_Growth"]

# Merge into regional KPI
rg = kpi_region.merge(avg_growth_region, on="Region", how="left")
rg["Avg_Growth"] = rg["Avg_Growth"].fillna(0)

# ── Score Each Component ──
rg["Revenue_Score"] = min_max_score(rg["Total_Sales"],     40)
rg["Profit_Score"]  = min_max_score(rg["Avg_Margin_Pct"],  40)
rg["Growth_Score"]  = min_max_score(rg["Avg_Growth"],      20)

# ── Total Score ──
rg["Total_Score"] = (rg["Revenue_Score"] + rg["Profit_Score"] + rg["Growth_Score"]).round(2)

# ── Classify ──
rg["Classification"] = rg["Total_Score"].apply(classify)

# ── Sort by Score ──
rg = rg.sort_values("Total_Score", ascending=False).reset_index(drop=True)

# ── Print Results ──
print(f"\n{'Region':<12} {'Score':>7} {'Classification':<20} {'Margin%':>9} {'Sales':>12}")
print("-" * 65)
for _, row in rg.iterrows():
    print(f"{row['Region']:<12} {row['Total_Score']:>7} {row['Classification']:<20} {row['Avg_Margin_Pct']:>8}% ${row['Total_Sales']:>11,.0f}")

# ──────────────────────────────────────────────
# ACTION SUMMARY
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("ACTION SUMMARY")
print("=" * 60)

# Top opportunities
opps = sc[sc["Classification"].isin(["🟢 Core", "🟡 Opportunity"])].head(3)
print("\n🚀 TOP OPPORTUNITIES (Invest / Grow):")
for _, row in opps.iterrows():
    print(f"    → {row['Sub-Category']:<20} | Score: {row['Total_Score']} | {row['Classification']}")

# Top risks
risks = sc[sc["Classification"].isin(["🔴 Risk", "⚪ Low Priority"])].tail(3)
print("\n⚠️  TOP RISKS (Reduce / Fix):")
for _, row in risks.iterrows():
    print(f"    → {row['Sub-Category']:<20} | Score: {row['Total_Score']} | {row['Classification']}")

# Regional flags
risk_regions = rg[rg["Classification"].isin(["🔴 Risk", "⚪ Low Priority"])]
print("\n🌍 REGIONAL FLAGS:")
if len(risk_regions) > 0:
    for _, row in risk_regions.iterrows():
        print(f"    ⚠️  {row['Region']:<12} | Score: {row['Total_Score']} | {row['Classification']}")
else:
    print("    All regions are performing at acceptable levels.")

# ──────────────────────────────────────────────
# SAVE OUTPUTS
# ──────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
sc.to_csv("data/decision_subcategory.csv", index=False)
rg.to_csv("data/decision_region.csv",      index=False)

print("\n✅ Decision Intelligence saved:")
print("    → data/decision_subcategory.csv")
print("    → data/decision_region.csv")
print("=" * 60)