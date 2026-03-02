# ⚡ DecisionForge
> Converts raw sales data into trusted insights, scored decisions, and ranked action plans.

---

## 🚀 Pipeline

| Phase | File | What It Does |
|-------|------|--------------|
| 1 | `phase1_data_trust.py` | Validate and clean raw data |
| 2 | `phase2_feature_engineering.py` | Create business signals from raw columns |
| 3 | `phase3_kpi_engine.py` | Summarize 9,994 rows into performance tables |
| 4 | `phase4_decision_intelligence.py` | Score and classify every product and region (0–100) |
| 5 | `phase5_optimization_engine.py` | Rank priorities with recommended actions |
| 6 | `phase6_dashboard.py` | Build interactive HTML executive dashboard |

---

## 📊 Dataset
Superstore Sales — 9,994 orders, 21 columns, Jan 2011 – Dec 2014

---

## 🔍 Key Findings

| Metric | Value |
|--------|-------|
| Business Health Score | 44.13 / 100 🔴 At Risk |
| Total Sales | $2,297,201 |
| Total Profit | $286,397 |
| Avg Profit Margin | 12.03% |
| Loss-making orders | 1,936 out of 9,994 |
| Revenue lost to discounts | $566,734 |
| Worst region | Central — -10.41% margin on $501K sales |
| Best region | West — 21.95% margin |

---

## 🧠 Decision Results

| Entity | Score | Classification | Action |
|--------|-------|----------------|--------|
| West | 100.0 | 🟢 Core | ✅ Maintain |
| East | 83.31 | 🟢 Core | ✅ Maintain |
| Phones | 61.84 | 🟡 Opportunity | 🚀 Invest |
| Copiers | 60.14 | 🟡 Opportunity | 🚀 Invest |
| South | 33.08 | 🔴 Risk | 📉 Reduce Focus |
| Binders | 27.08 | 🔴 Risk | 🔧 Restructure |
| Bookcases | 21.21 | 🔴 Risk | 🔧 Restructure |
| Central | 20.15 | 🔴 Risk | 🔧 Restructure |
| Appliances | 20.29 | 🔴 Risk | 🔧 Restructure |

---

## 🛠️ Tech Stack
Python · pandas · Plotly · HTML/CSS/JS · Git

---

## ▶️ How To Run
```bash
pip install pandas plotly openpyxl

python phase1_data_trust.py
python phase2_feature_engineering.py
python phase3_kpi_engine.py
python phase4_decision_intelligence.py
python phase5_optimization_engine.py
python phase6_dashboard.py
```
Then open `output/decisionforge_dashboard.html` in any browser.

---

## 📁 Structure
```
DecisionForge/
├── data/               ← all csv inputs and outputs
├── output/             ← final dashboard html
├── phase1_data_trust.py
├── phase2_feature_engineering.py
├── phase3_kpi_engine.py
├── phase4_decision_intelligence.py
├── phase5_optimization_engine.py
├── phase6_dashboard.py
└── README.md
```
