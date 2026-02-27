import pandas as pd
import os

# ──────────────────────────────────────────────
# PHASE 5: OPTIMIZATION ENGINE
# ──────────────────────────────────────────────

# ── LOAD DECISION INTELLIGENCE FROM PHASE 4 ──
sc = pd.read_csv("data/decision_subcategory.csv")
rg = pd.read_csv("data/decision_region.csv")

print("=" * 60)
print("DECISIONFORGE — PHASE 5: OPTIMIZATION ENGINE")
print("=" * 60)

# ──────────────────────────────────────────────
# HELPER: URGENCY SCORE
# ──────────────────────────────────────────────

def calculate_urgency(row):
    """
    Urgency bonus added on top of decision score.
    Higher urgency = needs attention faster.
    """
    urgency = 0

    # Losing money right now → highest urgency
    if row["Avg_Margin_Pct"] < 0:
        urgency += 30

    # High revenue but classified as Risk → dangerous
    if row["Classification"] in ["🔴 Risk", "⚪ Low Priority"]:
        if row["Total_Sales"] > 100000:
            urgency += 20
        else:
            urgency += 10

    # Opportunity but not yet Core → moderate urgency
    if row["Classification"] == "🟡 Opportunity":
        urgency += 5

    return urgency

# ──────────────────────────────────────────────
# HELPER: ACTION RECOMMENDATION
# ──────────────────────────────────────────────

def recommend_action(row):
    classification = row["Classification"]
    margin         = row["Avg_Margin_Pct"]
    growth         = row.get("Avg_Growth", 0)

    if classification == "🟢 Core":
        return "✅ Maintain"

    elif classification == "🟡 Opportunity":
        if growth > 0.1:
            return "🚀 Invest"
        else:
            return "👁️  Monitor"

    elif classification == "🔴 Risk":
        if margin < 0:
            return "🔧 Restructure"
        else:
            return "📉 Reduce Focus"

    else:  # Low Priority
        return "⏸️  Deprioritize"

# ──────────────────────────────────────────────
# PART A: OPTIMIZE SUB-CATEGORIES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PART A — SUB-CATEGORY OPTIMIZATION PLAN")
print("=" * 60)

# ── Calculate Urgency ──
sc["Urgency_Score"] = sc.apply(calculate_urgency, axis=1)

# ── Priority Score = Decision Score inverted for risks + Urgency ──
# Lower decision score + higher urgency = act first
sc["Priority_Score"] = (100 - sc["Total_Score"] + sc["Urgency_Score"]).round(2)

# ── Recommend Action ──
sc["Recommended_Action"] = sc.apply(recommend_action, axis=1)

# ── Rank by Priority ──
sc = sc.sort_values("Priority_Score", ascending=False).reset_index(drop=True)
sc.index += 1
sc.index.name = "Rank"

# ── Print Results ──
print(f"\n{'Rank':<6} {'Sub-Category':<20} {'Action':<20} {'Priority':>9} {'Score':>7} {'Margin%':>9}")
print("-" * 78)
for rank, row in sc.iterrows():
    print(
        f"{rank:<6} "
        f"{row['Sub-Category']:<20} "
        f"{row['Recommended_Action']:<20} "
        f"{row['Priority_Score']:>9} "
        f"{row['Total_Score']:>7} "
        f"{row['Avg_Margin_Pct']:>8}%"
    )

# ──────────────────────────────────────────────
# PART B: OPTIMIZE REGIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("PART B — REGIONAL OPTIMIZATION PLAN")
print("=" * 60)

# ── Calculate Urgency ──
rg["Urgency_Score"] = rg.apply(calculate_urgency, axis=1)

# ── Priority Score ──
rg["Priority_Score"] = (100 - rg["Total_Score"] + rg["Urgency_Score"]).round(2)

# ── Recommend Action ──
rg["Recommended_Action"] = rg.apply(recommend_action, axis=1)

# ── Rank by Priority ──
rg = rg.sort_values("Priority_Score", ascending=False).reset_index(drop=True)
rg.index += 1
rg.index.name = "Rank"

# ── Print Results ──
print(f"\n{'Rank':<6} {'Region':<12} {'Action':<20} {'Priority':>9} {'Score':>7} {'Margin%':>9}")
print("-" * 65)
for rank, row in rg.iterrows():
    print(
        f"{rank:<6} "
        f"{row['Region']:<12} "
        f"{row['Recommended_Action']:<20} "
        f"{row['Priority_Score']:>9} "
        f"{row['Total_Score']:>7} "
        f"{row['Avg_Margin_Pct']:>8}%"
    )

# ──────────────────────────────────────────────
# FINAL EXECUTIVE SUMMARY
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("FINAL EXECUTIVE SUMMARY — TOP ACTIONS RIGHT NOW")
print("=" * 60)

# Top 3 sub-category actions
print("\n📋 TOP 3 PRODUCT ACTIONS:")
for rank, row in sc.head(3).iterrows():
    print(f"    {rank}. {row['Sub-Category']:<20} → {row['Recommended_Action']}")
    if row["Avg_Margin_Pct"] < 0:
        print(f"       ⚠️  Losing {abs(row['Avg_Margin_Pct'])}% on every sale. Fix pricing or cut discounts.")
    elif row["Recommended_Action"] == "🚀 Invest":
        print(f"       💡 Growing fast with {row['Avg_Margin_Pct']}% margin. Push volume here.")
    else:
        print(f"       📌 Score: {row['Total_Score']} | Margin: {row['Avg_Margin_Pct']}%")

# Top regional actions
print("\n🌍 TOP REGIONAL ACTIONS:")
for rank, row in rg.head(2).iterrows():
    print(f"    {rank}. {row['Region']:<12} → {row['Recommended_Action']}")
    if row["Avg_Margin_Pct"] < 0:
        print(f"       ⚠️  Negative margin region. Every sale is costing the business money.")
    else:
        print(f"       📌 Score: {row['Total_Score']} | Margin: {row['Avg_Margin_Pct']}%")

# Overall business health
all_scores  = list(sc["Total_Score"]) + list(rg["Total_Score"])
health      = round(sum(all_scores) / len(all_scores), 2)

print(f"\n📊 OVERALL BUSINESS HEALTH SCORE: {health} / 100")
if health >= 70:
    print("    Status: 🟢 Healthy")
elif health >= 45:
    print("    Status: 🟡 Moderate — attention needed in key areas")
else:
    print("    Status: 🔴 At Risk — immediate action required")

# ──────────────────────────────────────────────
# SAVE OUTPUTS
# ──────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
sc.reset_index().to_csv("data/optimization_subcategory.csv", index=False)
rg.reset_index().to_csv("data/optimization_region.csv",      index=False)

print("\n✅ Optimization plans saved:")
print("    → data/optimization_subcategory.csv")
print("    → data/optimization_region.csv")
print("=" * 60)