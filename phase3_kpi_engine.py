import pandas as pd
import os

# ──────────────────────────────────────────────
# PHASE 3: KPI ENGINE
# ──────────────────────────────────────────────

# ── LOAD FEATURED DATA FROM PHASE 2 ──
df = pd.read_csv("data/featured_data.csv", parse_dates=["Order Date", "Ship Date"])

print("=" * 60)
print("DECISIONFORGE — PHASE 3: KPI ENGINE")
print("=" * 60)
print(f"\nLoaded featured data: {df.shape[0]} rows, {df.shape[1]} columns")

# ──────────────────────────────────────────────
# KPI TABLE 1: YEARLY PERFORMANCE
# ──────────────────────────────────────────────

yearly = df.groupby("Order Year").agg(
    Total_Sales    = ("Sales",           "sum"),
    Total_Profit   = ("Profit",          "sum"),
    Total_Orders   = ("Order ID",        "count"),
    Avg_Margin_Pct = ("Profit Margin %", "mean")
).round(2).reset_index()

# Year over Year Sales Growth %
yearly["YoY_Growth_%"] = yearly["Total_Sales"].pct_change().mul(100).round(2)

print("\n" + "=" * 60)
print("KPI TABLE 1 — YEARLY PERFORMANCE")
print("=" * 60)
print(yearly.to_string(index=False))

# ──────────────────────────────────────────────
# KPI TABLE 2: REGIONAL PERFORMANCE
# ──────────────────────────────────────────────

regional = df.groupby("Region").agg(
    Total_Sales      = ("Sales",           "sum"),
    Total_Profit     = ("Profit",          "sum"),
    Total_Orders     = ("Order ID",        "count"),
    Avg_Margin_Pct   = ("Profit Margin %", "mean"),
    Sales_Contrib_Pct= ("Region Sales Contribution %", "first")
).round(2).reset_index()

regional = regional.sort_values("Total_Sales", ascending=False)

print("\n" + "=" * 60)
print("KPI TABLE 2 — REGIONAL PERFORMANCE")
print("=" * 60)
print(regional.to_string(index=False))

# ──────────────────────────────────────────────
# KPI TABLE 3: CATEGORY & SUB-CATEGORY PERFORMANCE
# ──────────────────────────────────────────────

category = df.groupby(["Category", "Sub-Category"]).agg(
    Total_Sales      = ("Sales",            "sum"),
    Total_Profit     = ("Profit",           "sum"),
    Total_Orders     = ("Order ID",         "count"),
    Avg_Margin_Pct   = ("Profit Margin %",  "mean"),
    Avg_Discount     = ("Discount",         "mean"),
    Loss_Orders      = ("Is Profitable",    lambda x: (x == "No").sum())
).round(2).reset_index()

category = category.sort_values("Total_Sales", ascending=False)

print("\n" + "=" * 60)
print("KPI TABLE 3 — CATEGORY & SUB-CATEGORY PERFORMANCE")
print("=" * 60)
print(category.to_string(index=False))

# ──────────────────────────────────────────────
# KPI TABLE 4: CUSTOMER SEGMENT PERFORMANCE
# ──────────────────────────────────────────────

segment = df.groupby("Segment").agg(
    Total_Sales     = ("Sales",   "sum"),
    Total_Profit    = ("Profit",  "sum"),
    Total_Orders    = ("Order ID","count"),
    Avg_Order_Value = ("Sales",   "mean"),
    Avg_Margin_Pct  = ("Profit Margin %", "mean")
).round(2).reset_index()

segment = segment.sort_values("Total_Sales", ascending=False)

print("\n" + "=" * 60)
print("KPI TABLE 4 — CUSTOMER SEGMENT PERFORMANCE")
print("=" * 60)
print(segment.to_string(index=False))

# ──────────────────────────────────────────────
# BUSINESS HIGHLIGHTS — QUICK WINS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("BUSINESS HIGHLIGHTS")
print("=" * 60)

best_year    = yearly.loc[yearly["Total_Sales"].idxmax(), "Order Year"]
worst_region = regional.loc[regional["Total_Profit"].idxmin(), "Region"]
best_region  = regional.loc[regional["Total_Profit"].idxmax(), "Region"]
worst_subcat = category.loc[category["Total_Profit"].idxmin(), "Sub-Category"]
best_subcat  = category.loc[category["Total_Profit"].idxmax(), "Sub-Category"]
best_segment = segment.loc[segment["Total_Profit"].idxmax(), "Segment"]

print(f"    Best Year         : {best_year}")
print(f"    Best Region       : {best_region}")
print(f"    Worst Region      : {worst_region} ⚠️")
print(f"    Best Sub-Category : {best_subcat}")
print(f"    Worst Sub-Category: {worst_subcat} ⚠️")
print(f"    Best Segment      : {best_segment}")

# ──────────────────────────────────────────────
# SAVE ALL KPI TABLES
# ──────────────────────────────────────────────

os.makedirs("data", exist_ok=True)

yearly.to_csv("data/kpi_yearly.csv",     index=False)
regional.to_csv("data/kpi_regional.csv", index=False)
category.to_csv("data/kpi_category.csv", index=False)
segment.to_csv("data/kpi_segment.csv",   index=False)

print("\n✅ KPI tables saved:")
print("    → data/kpi_yearly.csv")
print("    → data/kpi_regional.csv")
print("    → data/kpi_category.csv")
print("    → data/kpi_segment.csv")
print("=" * 60)