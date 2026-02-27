import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ──────────────────────────────────────────────
# PHASE 6: INTERACTIVE HTML DASHBOARD
# ──────────────────────────────────────────────

# ── LOAD ALL DATA ──
kpi_yearly   = pd.read_csv("data/kpi_yearly.csv")
kpi_regional = pd.read_csv("data/kpi_regional.csv")
kpi_category = pd.read_csv("data/kpi_category.csv")
dec_sub      = pd.read_csv("data/decision_subcategory.csv")
dec_reg      = pd.read_csv("data/decision_region.csv")
opt_sub      = pd.read_csv("data/optimization_subcategory.csv")
opt_reg      = pd.read_csv("data/optimization_region.csv")

# ── HEALTH SCORE ──
all_scores   = list(dec_sub["Total_Score"]) + list(dec_reg["Total_Score"])
health_score = round(sum(all_scores) / len(all_scores), 2)
health_color = "#e74c3c" if health_score < 45 else "#f39c12" if health_score < 70 else "#27ae60"

# ── CLASSIFICATION COLORS ──
color_map = {
    "🟢 Core"         : "#27ae60",
    "🟡 Opportunity"  : "#f39c12",
    "🔴 Risk"         : "#e74c3c",
    "⚪ Low Priority" : "#95a5a6"
}

def get_color(classification):
    return color_map.get(classification, "#95a5a6")

# ──────────────────────────────────────────────
# BUILD HTML
# ──────────────────────────────────────────────

html_parts = []

# ── HEAD & STYLE ──
html_parts.append(f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DecisionForge Dashboard</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #ffffff; }}

  .header {{
    background: linear-gradient(135deg, #1a1f2e, #2d3561);
    padding: 30px 40px;
    border-bottom: 2px solid #3d4574;
  }}
  .header h1 {{ font-size: 28px; letter-spacing: 2px; color: #7c83fd; }}
  .header p  {{ color: #8892b0; margin-top: 5px; font-size: 14px; }}

  .nav {{
    background: #1a1f2e;
    padding: 0 40px;
    display: flex;
    gap: 5px;
    border-bottom: 1px solid #2d3561;
  }}
  .nav a {{
    color: #8892b0;
    text-decoration: none;
    padding: 14px 20px;
    font-size: 14px;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
  }}
  .nav a:hover, .nav a.active {{
    color: #7c83fd;
    border-bottom-color: #7c83fd;
  }}

  .page {{ display: none; padding: 30px 40px; }}
  .page.active {{ display: block; }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 30px;
  }}
  .kpi-card {{
    background: #1a1f2e;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
  }}
  .kpi-card .value {{ font-size: 28px; font-weight: bold; margin-bottom: 5px; }}
  .kpi-card .label {{ font-size: 12px; color: #8892b0; text-transform: uppercase; letter-spacing: 1px; }}

  .chart-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
  }}
  .chart-box {{
    background: #1a1f2e;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 20px;
  }}
  .chart-box.full {{ grid-column: 1 / -1; }}
  .chart-box h3 {{ font-size: 14px; color: #8892b0; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}

  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #2d3561; color: #8892b0; padding: 10px 12px; text-align: left; font-weight: 600; letter-spacing: 1px; font-size: 11px; text-transform: uppercase; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #1e2433; }}
  tr:hover td {{ background: #1e2433; }}

  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
  }}
  .badge-core    {{ background: #1a3a2a; color: #27ae60; }}
  .badge-opp     {{ background: #3a2e1a; color: #f39c12; }}
  .badge-risk    {{ background: #3a1a1a; color: #e74c3c; }}
  .badge-low     {{ background: #2a2a2a; color: #95a5a6; }}

  .action-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
  }}
  .action-card {{
    background: #1a1f2e;
    border: 1px solid #2d3561;
    border-radius: 10px;
    padding: 20px;
  }}
  .action-card h3 {{ font-size: 13px; color: #8892b0; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
  .action-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e2433;
    font-size: 13px;
  }}
  .action-item:last-child {{ border-bottom: none; }}

  .health-big {{
    text-align: center;
    padding: 20px;
    font-size: 52px;
    font-weight: bold;
    color: {health_color};
  }}
  .health-label {{
    text-align: center;
    color: #8892b0;
    font-size: 13px;
    margin-top: -10px;
    margin-bottom: 10px;
  }}
</style>
</head>
<body>
""")

# ── HEADER ──
html_parts.append("""
<div class="header">
  <h1>⚡ DECISIONFORGE</h1>
  <p>Business Intelligence & Decision Engine — Executive Dashboard</p>
</div>
""")

# ── NAV ──
html_parts.append("""
<div class="nav">
  <a href="#" class="active" onclick="showPage('p1', this)">📊 Business Health</a>
  <a href="#" onclick="showPage('p2', this)">🧠 Decision Intelligence</a>
  <a href="#" onclick="showPage('p3', this)">🚀 Action Plan</a>
</div>
""")

# ──────────────────────────────────────────────
# PAGE 1: BUSINESS HEALTH
# ──────────────────────────────────────────────

total_sales   = kpi_yearly["Total_Sales"].sum()
total_profit  = kpi_yearly["Total_Profit"].sum()
total_orders  = kpi_yearly["Total_Orders"].sum()
avg_margin    = round(kpi_yearly["Avg_Margin_Pct"].mean(), 2)

html_parts.append(f"""
<div id="p1" class="page active">

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="value" style="color:{health_color}">{health_score}</div>
      <div class="label">Health Score / 100</div>
    </div>
    <div class="kpi-card">
      <div class="value" style="color:#7c83fd">${total_sales:,.0f}</div>
      <div class="label">Total Sales</div>
    </div>
    <div class="kpi-card">
      <div class="value" style="color:#27ae60">${total_profit:,.0f}</div>
      <div class="label">Total Profit</div>
    </div>
    <div class="kpi-card">
      <div class="value" style="color:#f39c12">{total_orders:,}</div>
      <div class="label">Total Orders</div>
    </div>
  </div>

  <div class="chart-grid">
""")

# Sales Trend Chart
fig_sales = go.Figure()
fig_sales.add_trace(go.Scatter(
    x=kpi_yearly["Order Year"],
    y=kpi_yearly["Total_Sales"],
    mode="lines+markers+text",
    text=[f"${v:,.0f}" for v in kpi_yearly["Total_Sales"]],
    textposition="top center",
    line=dict(color="#7c83fd", width=3),
    marker=dict(size=8),
    fill="tozeroy",
    fillcolor="rgba(124,131,253,0.1)"
))
fig_sales.update_layout(
    title="Sales Trend by Year",
    paper_bgcolor="#1a1f2e", plot_bgcolor="#1a1f2e",
    font=dict(color="#8892b0"),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300,
    xaxis=dict(gridcolor="#2d3561"),
    yaxis=dict(gridcolor="#2d3561")
)

# Profit Trend Chart
fig_profit = go.Figure()
fig_profit.add_trace(go.Bar(
    x=kpi_yearly["Order Year"],
    y=kpi_yearly["Total_Profit"],
    text=[f"${v:,.0f}" for v in kpi_yearly["Total_Profit"]],
    textposition="outside",
    marker_color=["#e74c3c" if v < 0 else "#27ae60" for v in kpi_yearly["Total_Profit"]]
))
fig_profit.update_layout(
    title="Profit by Year",
    paper_bgcolor="#1a1f2e", plot_bgcolor="#1a1f2e",
    font=dict(color="#8892b0"),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300,
    xaxis=dict(gridcolor="#2d3561"),
    yaxis=dict(gridcolor="#2d3561")
)

# Regional Donut
fig_donut = go.Figure(go.Pie(
    labels=kpi_regional["Region"],
    values=kpi_regional["Total_Sales"],
    hole=0.6,
    marker=dict(colors=["#7c83fd", "#27ae60", "#f39c12", "#e74c3c"])
))
fig_donut.update_layout(
    title="Sales by Region",
    paper_bgcolor="#1a1f2e",
    font=dict(color="#8892b0"),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300
)

# YoY Growth Chart
fig_growth = go.Figure()
fig_growth.add_trace(go.Bar(
    x=kpi_yearly["Order Year"],
    y=kpi_yearly["YoY_Growth_%"].fillna(0),
    text=[f"{v:.1f}%" for v in kpi_yearly["YoY_Growth_%"].fillna(0)],
    textposition="outside",
    marker_color=["#95a5a6" if v <= 0 else "#27ae60" for v in kpi_yearly["YoY_Growth_%"].fillna(0)]
))
fig_growth.update_layout(
    title="Year over Year Growth %",
    paper_bgcolor="#1a1f2e", plot_bgcolor="#1a1f2e",
    font=dict(color="#8892b0"),
    margin=dict(l=20, r=20, t=40, b=20),
    height=300,
    xaxis=dict(gridcolor="#2d3561"),
    yaxis=dict(gridcolor="#2d3561")
)

html_parts.append(f"""
    <div class="chart-box">{fig_sales.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div class="chart-box">{fig_profit.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div class="chart-box">{fig_donut.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div class="chart-box">{fig_growth.to_html(full_html=False, include_plotlyjs=False)}</div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# PAGE 2: DECISION INTELLIGENCE
# ──────────────────────────────────────────────

def badge(classification):
    if "Core"     in classification: return f'<span class="badge badge-core">Core</span>'
    if "Opport"   in classification: return f'<span class="badge badge-opp">Opportunity</span>'
    if "Risk"     in classification: return f'<span class="badge badge-risk">Risk</span>'
    return f'<span class="badge badge-low">Low Priority</span>'

# Sub-category table rows
sc_rows = ""
for _, row in dec_sub.sort_values("Total_Score", ascending=False).iterrows():
    bar_width = int(row["Total_Score"])
    bar_color = get_color(row["Classification"])
    sc_rows += f"""
    <tr>
      <td>{row['Sub-Category']}</td>
      <td>
        <div style="background:#2d3561;border-radius:4px;height:8px;width:100%">
          <div style="background:{bar_color};width:{bar_width}%;height:8px;border-radius:4px"></div>
        </div>
        <small style="color:#8892b0">{row['Total_Score']}</small>
      </td>
      <td>{badge(row['Classification'])}</td>
      <td style="color:{'#e74c3c' if row['Avg_Margin_Pct'] < 0 else '#27ae60'}">{row['Avg_Margin_Pct']}%</td>
      <td style="color:#7c83fd">${row['Total_Sales']:,.0f}</td>
      <td style="color:#8892b0">{int(row['Loss_Orders'])}</td>
    </tr>"""

# Region table rows
rg_rows = ""
for _, row in dec_reg.sort_values("Total_Score", ascending=False).iterrows():
    bar_width = int(row["Total_Score"])
    bar_color = get_color(row["Classification"])
    rg_rows += f"""
    <tr>
      <td>{row['Region']}</td>
      <td>
        <div style="background:#2d3561;border-radius:4px;height:8px;width:100%">
          <div style="background:{bar_color};width:{bar_width}%;height:8px;border-radius:4px"></div>
        </div>
        <small style="color:#8892b0">{row['Total_Score']}</small>
      </td>
      <td>{badge(row['Classification'])}</td>
      <td style="color:{'#e74c3c' if row['Avg_Margin_Pct'] < 0 else '#27ae60'}">{row['Avg_Margin_Pct']}%</td>
      <td style="color:#7c83fd">${row['Total_Sales']:,.0f}</td>
    </tr>"""

html_parts.append(f"""
<div id="p2" class="page">
  <div class="chart-box full" style="margin-bottom:20px">
    <h3>Sub-Category Intelligence</h3>
    <table>
      <tr>
        <th>Sub-Category</th>
        <th>Score</th>
        <th>Classification</th>
        <th>Margin %</th>
        <th>Total Sales</th>
        <th>Loss Orders</th>
      </tr>
      {sc_rows}
    </table>
  </div>

  <div class="chart-box full">
    <h3>Regional Intelligence</h3>
    <table>
      <tr>
        <th>Region</th>
        <th>Score</th>
        <th>Classification</th>
        <th>Margin %</th>
        <th>Total Sales</th>
      </tr>
      {rg_rows}
    </table>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# PAGE 3: ACTION PLAN
# ──────────────────────────────────────────────

action_colors = {
    "🔧 Restructure" : "#e74c3c",
    "📉 Reduce Focus": "#f39c12",
    "🚀 Invest"      : "#27ae60",
    "👁️  Monitor"    : "#3498db",
    "✅ Maintain"    : "#7c83fd",
    "⏸️  Deprioritize": "#95a5a6"
}

# Sub-category action rows
opt_rows = ""
for _, row in opt_sub.iterrows():
    action = row["Recommended_Action"]
    color  = action_colors.get(action, "#8892b0")
    opt_rows += f"""
    <tr>
      <td style="color:#8892b0;font-weight:bold">{int(row['Rank'])}</td>
      <td>{row['Sub-Category']}</td>
      <td><span style="color:{color};font-weight:600">{action}</span></td>
      <td style="color:#7c83fd">{row['Priority_Score']}</td>
      <td style="color:#8892b0">{row['Total_Score']}</td>
      <td style="color:{'#e74c3c' if row['Avg_Margin_Pct'] < 0 else '#27ae60'}">{row['Avg_Margin_Pct']}%</td>
    </tr>"""

# Region action rows
reg_opt_rows = ""
for _, row in opt_reg.iterrows():
    action = row["Recommended_Action"]
    color  = action_colors.get(action, "#8892b0")
    reg_opt_rows += f"""
    <tr>
      <td style="color:#8892b0;font-weight:bold">{int(row['Rank'])}</td>
      <td>{row['Region']}</td>
      <td><span style="color:{color};font-weight:600">{action}</span></td>
      <td style="color:#7c83fd">{row['Priority_Score']}</td>
      <td style="color:#8892b0">{row['Total_Score']}</td>
      <td style="color:{'#e74c3c' if row['Avg_Margin_Pct'] < 0 else '#27ae60'}">{row['Avg_Margin_Pct']}%</td>
    </tr>"""

html_parts.append(f"""
<div id="p3" class="page">

  <div class="health-big">{health_score}</div>
  <div class="health-label">OVERALL BUSINESS HEALTH SCORE — 
    {"🔴 AT RISK" if health_score < 45 else "🟡 MODERATE" if health_score < 70 else "🟢 HEALTHY"}
  </div>

  <div class="chart-box full" style="margin-bottom:20px;margin-top:20px">
    <h3>Product Action Plan — Ranked by Priority</h3>
    <table>
      <tr>
        <th>Rank</th>
        <th>Sub-Category</th>
        <th>Action</th>
        <th>Priority Score</th>
        <th>Decision Score</th>
        <th>Margin %</th>
      </tr>
      {opt_rows}
    </table>
  </div>

  <div class="chart-box full">
    <h3>Regional Action Plan — Ranked by Priority</h3>
    <table>
      <tr>
        <th>Rank</th>
        <th>Region</th>
        <th>Action</th>
        <th>Priority Score</th>
        <th>Decision Score</th>
        <th>Margin %</th>
      </tr>
      {reg_opt_rows}
    </table>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# JAVASCRIPT + CLOSE HTML
# ──────────────────────────────────────────────

html_parts.append("""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
function showPage(pageId, clickedLink) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
  document.getElementById(pageId).classList.add('active');
  clickedLink.classList.add('active');
}
</script>
</body>
</html>
""")

# ──────────────────────────────────────────────
# SAVE DASHBOARD
# ──────────────────────────────────────────────

os.makedirs("output", exist_ok=True)
dashboard_path = "output/decisionforge_dashboard.html"

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print("=" * 60)
print("DECISIONFORGE — PHASE 6: DASHBOARD COMPLETE")
print("=" * 60)
print(f"\n✅ Dashboard saved to: {dashboard_path}")
print("\n👉 Open this file in your browser:")
print(f"   {os.path.abspath(dashboard_path)}")
print("=" * 60)