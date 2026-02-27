import pandas as pd
import os

# ──────────────────────────────────────────────
# PHASE 1: DATA TRUST LAYER
# ──────────────────────────────────────────────

# ── LOAD DATA ──
df = pd.read_csv("data/raw_data.csv", encoding="cp1252")

print("=" * 60)
print("DECISIONFORGE — PHASE 1: DATA TRUST LAYER")
print("=" * 60)

# ──────────────────────────────────────────────
# PART A: UNDERSTAND THE RAW DATA
# ──────────────────────────────────────────────

print("\n[1] DATASET SHAPE")
print(f"    Rows    : {df.shape[0]}")
print(f"    Columns : {df.shape[1]}")

print("\n[2] COLUMN DATA TYPES")
print(df.dtypes)

print("\n[3] NULL VALUES PER COLUMN")
nulls = df.isnull().sum()
print(nulls[nulls >= 0])

print("\n[4] DUPLICATE ROWS")
duplicates = df.duplicated().sum()
print(f"    Duplicate rows found: {duplicates}")

print("\n[5] BASIC STATISTICS (Sales, Profit, Quantity, Discount)")
print(df[["Sales", "Profit", "Quantity", "Discount"]].describe().round(2))

print("\n[6] NEGATIVE SALES CHECK")
neg_sales = df[df["Sales"] < 0]
print(f"    Rows with negative Sales: {len(neg_sales)}")

print("\n[7] DISCOUNT RANGE CHECK (should be 0 to 1)")
bad_discount = df[(df["Discount"] < 0) | (df["Discount"] > 1)]
print(f"    Rows with invalid Discount: {len(bad_discount)}")

# ──────────────────────────────────────────────
# PART B: CLEAN & VALIDATE
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PART B — CLEANING & VALIDATION")
print("=" * 60)

# ── Fix 1: Convert dates to proper datetime format ──
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True, errors="coerce")
print("\n[FIX 1] Dates converted to datetime format ✓")

# ── Fix 2: Remove duplicate rows ──
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"[FIX 2] Duplicates removed: {before - after} rows dropped ✓")

# ── Fix 3: Remove rows where Sales is negative ──
before = len(df)
df = df[df["Sales"] >= 0]
after = len(df)
print(f"[FIX 3] Negative Sales removed: {before - after} rows dropped ✓")

# ── Fix 4: Remove rows where Discount is out of range ──
before = len(df)
df = df[(df["Discount"] >= 0) & (df["Discount"] <= 1)]
after = len(df)
print(f"[FIX 4] Invalid Discounts removed: {before - after} rows dropped ✓")

# ── Fix 5: Handle nulls ──
before = len(df)
df = df.dropna(subset=["Sales", "Profit", "Quantity", "Order Date"])
after = len(df)
print(f"[FIX 5] Rows with critical nulls removed: {before - after} rows dropped ✓")

# ── Fix 6: Strip whitespace from string columns ──
str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
print(f"[FIX 6] Whitespace stripped from all text columns ✓")

# ──────────────────────────────────────────────
# FINAL REPORT
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("FINAL DATA QUALITY REPORT")
print("=" * 60)
print(f"    Clean rows remaining : {len(df)}")
print(f"    Columns              : {df.shape[1]}")
print(f"    Remaining nulls      : {df.isnull().sum().sum()}")
print(f"    Date range           : {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")

# ──────────────────────────────────────────────
# SAVE CLEAN DATA
# ──────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
df.to_csv("data/clean_data.csv", index=False)
print("\n✅ clean_data.csv saved to /data folder")
print("=" * 60)