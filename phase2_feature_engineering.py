import pandas as pd
import os

# ──────────────────────────────────────────────
# PHASE 2: FEATURE ENGINEERING
# ──────────────────────────────────────────────

# ── LOAD CLEAN DATA FROM PHASE 1 ──
df = pd.read_csv("data/clean_data.csv", parse_dates=["Order Date", "Ship Date"])

print("=" * 60)
print("DECISIONFORGE — PHASE 2: FEATURE ENGINEERING")
print("=" * 60)
print(f"\nLoaded clean data: {df.shape[0]} rows, {df.shape[1]} columns")

# ──────────────────────────────────────────────
# GROUP 1: TIME FEATURES
# ──────────────────────────────────────────────

df["Order Year"]    = df["Order Date"].dt.year
df["Order Month"]   = df["Order Date"].dt.month
df["Order Quarter"] = df["Order Date"].dt.quarter

print("\n[GROUP 1] Time Features created ✓")
print(f"    Years in data    : {sorted(df['Order Year'].unique())}")
print(f"    Quarters in data : {sorted(df['Order Quarter'].unique())}")

# ──────────────────────────────────────────────
# GROUP 2: PROFITABILITY FEATURES
# ──────────────────────────────────────────────

df["Profit Margin %"] = ((df["Profit"] / df["Sales"]) * 100).round(2)
df["Is Profitable"]   = df["Profit"].apply(lambda x: "Yes" if x > 0 else "No")

print("\n[GROUP 2] Profitability Features created ✓")
print(f"    Avg Profit Margin : {df['Profit Margin %'].mean().round(2)}%")
print(f"    Profitable orders : {df[df['Is Profitable'] == 'Yes'].shape[0]}")
print(f"    Loss orders       : {df[df['Is Profitable'] == 'No'].shape[0]}")

# ──────────────────────────────────────────────
# GROUP 3: DISCOUNT IMPACT FEATURES
# ──────────────────────────────────────────────
df["Revenue Without Discount"] = (df["Sales"] / (1 - df["Discount"])).round(2)
df["Revenue Without Discount"] = df["Revenue Without Discount"].replace(
    [float("inf"), float("-inf")], float("nan")
)
df["Revenue Without Discount"] = df["Revenue Without Discount"].fillna(df["Sales"])
df["Discount Given ($)"] = (df["Revenue Without Discount"] - df["Sales"]).round(2)

print("\n[GROUP 3] Discount Impact Features created ✓")
print(f"    Total discount given : ${df['Discount Given ($)'].sum():,.2f}")
print(f"    Revenue lost to disc : ${df['Discount Given ($)'].sum():,.2f}")

# ──────────────────────────────────────────────
# GROUP 4: ORDER SIZE FEATURES
# ──────────────────────────────────────────────

df["Revenue Per Unit"] = (df["Sales"] / df["Quantity"]).round(2)

print("\n[GROUP 4] Order Size Features created ✓")
print(f"    Avg Revenue Per Unit : ${df['Revenue Per Unit'].mean().round(2)}")
print(f"    Max Revenue Per Unit : ${df['Revenue Per Unit'].max().round(2)}")

# ──────────────────────────────────────────────
# GROUP 5: CONTRIBUTION FEATURES
# ──────────────────────────────────────────────

total_sales = df["Sales"].sum()

# Region contribution
region_sales = df.groupby("Region")["Sales"].sum()
df["Region Sales Contribution %"] = df["Region"].map(
    lambda r: round((region_sales[r] / total_sales) * 100, 2)
)

# Category contribution
category_sales = df.groupby("Category")["Sales"].sum()
df["Category Sales Contribution %"] = df["Category"].map(
    lambda c: round((category_sales[c] / total_sales) * 100, 2)
)

print("\n[GROUP 5] Contribution Features created ✓")
print("\n    Region Sales Contribution:")
for region, pct in (region_sales / total_sales * 100).round(2).items():
    print(f"        {region:<10} : {pct}%")

print("\n    Category Sales Contribution:")
for cat, pct in (category_sales / total_sales * 100).round(2).items():
    print(f"        {cat:<20} : {pct}%")

# ──────────────────────────────────────────────
# FINAL SUMMARY
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("FEATURE ENGINEERING SUMMARY")
print("=" * 60)
print(f"    Original columns : 21")
print(f"    New columns added: {df.shape[1] - 21}")
print(f"    Total columns now: {df.shape[1]}")
print(f"    Total rows       : {df.shape[0]}")

# ──────────────────────────────────────────────
# SAVE FEATURED DATA
# ──────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
df.to_csv("data/featured_data.csv", index=False)
print("\n✅ featured_data.csv saved to /data folder")
print("=" * 60)