import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# PSM EXECUTIVE DASHBOARD
# Separate page from "02_All_Departments.py"
# Uses available department Excel data only.
# Missing department data remains Pending.
# ============================================================

st.set_page_config(
    page_title="PSM | Executive Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPT_DIR = os.path.join(BASE_DIR, "data", "departments")

# ------------------------------------------------------------
# ALL 15 DEPARTMENTS
# ------------------------------------------------------------
DEPARTMENTS = [
    "Blast Furnace",
    "Coke Oven-1",
    "Coke Oven-2",
    "CRM",
    "WRM",
    "CPP",
    "CU",
    "DRI",
    "LCP",
    "Pellet and Beneficiation",
    "Sinter",
    "SMS-1",
    "SMS-2",
    "Tube Mill",
    "CSP",
]

PILLARS = [
    "Process Safety Information",
    "Process Hazard Analysis",
    "Operating Procedures",
    "Mechanical Integrity",
    "Training",
    "Management of Change",
    "Pre-Startup Safety Review",
    "Contractor Safety",
    "Emergency Planning",
    "Incident Investigation",
    "Compliance Audits",
    "Employee Participation",
    "Trade Secrets",
    "Management Review",
]

# Same mapping used by the current department workbook structure.
MONTH_COLUMNS = {
    "level1": 1,
    "level2": 2,
    "level3": 3,
    "level4": 4,
    "investigation_30": 5,
    "soc": 6,
    "sol": 7,
    "equipment_failure": 8,
    "mechanical_generated": 9,
    "mechanical_completed": 10,
    "iem_generated": 11,
    "iem_completed": 12,
    "z01_open": 13,
    "z01_closed": 14,
    "iem_open": 15,
    "iem_closed": 16,
    "barrier_plan": 17,
    "barrier_actual": 18,
    "barrier_total": 19,
    "barrier_assessed": 20,
    "barrier_unacceptable": 21,
    "tabletop_planned": 22,
    "tabletop_actual": 23,
}

LOWER_COLUMNS = {
    "third_party_close": 1,
    "third_party_delayed": 2,
    "incident_rec_close": 3,
    "incident_rec_delayed": 4,
    "pha_plan": 8,
    "pha_actual": 9,
    "pha_close": 10,
    "pha_delayed": 11,
    "audit_close": 12,
    "audit_delayed": 13,
    "moc_pending": 14,
    "kaizen_moc": 16,
    "emergency_moc": 18,
    "temporary_overdue": 20,
    "interlock_open": 22,
    "normalisation_overdue": 23,
}

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown(
    """
<style>
.stApp {
    background: #edf4f9;
}
.block-container {
    max-width: 1900px;
    padding: 0.25rem 0.45rem 1rem 0.45rem;
}
header {visibility:hidden;}
footer {visibility:hidden;}

.exec-header {
    background: linear-gradient(105deg,#031f3c,#073b63 52%,#087aa0);
    border: 2px solid #08aee5;
    border-radius: 12px;
    padding: 8px 18px 7px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,40,70,.24);
}
.exec-small {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}
.exec-title {
    font-size: 25px;
    font-weight: 950;
    line-height: 29px;
}
.exec-screen {
    font-size: 18px;
    font-weight: 900;
    margin-top: 1px;
}
.exec-sub {
    font-size: 10px;
    margin-top: 2px;
}
.plant-online {
    display:inline-block;
    margin-top:4px;
    padding:3px 13px;
    border-radius:16px;
    background:#087d38;
    border:1px solid #52f28a;
    font-size:9px;
    font-weight:900;
}

.section {
    color:#092f50;
    font-size:15px;
    font-weight:950;
    border-bottom:2px solid #b9d2e3;
    border-left:6px solid #08a8dc;
    padding:4px 8px;
    margin:7px 0 5px;
}

.kpi {
    background:white;
    border:1px solid #c9d9e5;
    border-radius:9px;
    padding:7px 5px;
    text-align:center;
    box-shadow:0 2px 7px rgba(20,50,75,.10);
    min-height:82px;
}
.kpi-icon {font-size:18px;}
.kpi-title {
    font-size:9px;
    font-weight:850;
    color:#173d5c;
    line-height:11px;
}
.kpi-value {
    font-size:24px;
    line-height:26px;
    font-weight:950;
    margin-top:2px;
}
.kpi-sub {
    font-size:7px;
    color:#718292;
}

.blue {color:#126fc0;}
.green {color:#218b37;}
.orange {color:#df8c00;}
.red {color:#d71820;}
.purple {color:#6542a8;}
.gray {color:#738391;}

.panel {
    background:white;
    border:1px solid #cbdbe7;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(20,50,75,.08);
    padding:7px;
}

.pillar {
    background:white;
    border:1px solid #bfd2e1;
    border-radius:8px;
    padding:6px 3px;
    text-align:center;
    min-height:76px;
    box-shadow:0 2px 5px rgba(20,50,75,.07);
}
.pillar-no {
    font-size:9px;
    color:#52718b;
    font-weight:900;
}
.pillar-name {
    font-size:8px;
    color:#163c5b;
    font-weight:850;
    line-height:10px;
}
.pillar-score {
    font-size:19px;
    font-weight:950;
    margin-top:3px;
}
.pillar-green {color:#1b8a35;}
.pillar-amber {color:#e39700;}
.pillar-red {color:#d71920;}
.pillar-pending {color:#7b8995;}

.info {
    background:#e4f0fb;
    border:1px solid #c7dced;
    border-radius:7px;
    padding:6px 9px;
    color:#315773;
    font-size:9px;
    margin:4px 0;
}

.legend {
    display:flex;
    justify-content:center;
    gap:20px;
    font-size:9px;
    color:#50687a;
    padding:3px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def num(v):
    try:
        if pd.isna(v):
            return 0.0
        return float(str(v).replace(",", "").strip())
    except Exception:
        return 0.0


def fmt(v):
    x = num(v)
    return str(int(x)) if x.is_integer() else f"{x:.1f}"


def norm(s):
    return (
        str(s).lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("&", "and")
        .replace(".", "")
    )


def read_cell(df, row, col):
    try:
        return df.iloc[row, col]
    except Exception:
        return 0


def locate_file(dept):
    if not os.path.isdir(DEPT_DIR):
        return None

    files = [
        f for f in os.listdir(DEPT_DIR)
        if f.lower().endswith((".xlsx", ".xls"))
    ]

    target = norm(dept)

    for f in files:
        if norm(os.path.splitext(f)[0]) == target:
            return os.path.join(DEPT_DIR, f)

    return None


@st.cache_data(show_spinner=False)
def load_file(path):
    try:
        return pd.read_excel(path, header=None)
    except Exception:
        return None


def load_department(dept):
    path = locate_file(dept)

    if path is None:
        return {
            "department": dept,
            "loaded": False,
            "source": None,
        }

    df = load_file(path)

    if df is None:
        return {
            "department": dept,
            "loaded": False,
            "source": os.path.basename(path),
        }

    d = {
        "department": dept,
        "loaded": True,
        "source": os.path.basename(path),
    }

    for key, col in MONTH_COLUMNS.items():
        d[key] = num(read_cell(df, 5, col))

    for key, col in LOWER_COLUMNS.items():
        d[key] = num(read_cell(df, 10, col))

    d["incidents"] = (
        d["level1"] +
        d["level2"] +
        d["level3"] +
        d["level4"]
    )

    d["recommendations"] = (
        d["third_party_delayed"] +
        d["incident_rec_delayed"] +
        d["pha_delayed"] +
        d["audit_delayed"]
    )

    if d["barrier_assessed"] > 0:
        d["barrier_health"] = (
            (d["barrier_assessed"] - d["barrier_unacceptable"])
            / d["barrier_assessed"]
        ) * 100
    else:
        d["barrier_health"] = None

    return d


def kpi(icon, title, value, color="blue", sub=""):
    return f"""
    <div class="kpi">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value {color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


# ------------------------------------------------------------
# LOAD ALL DEPARTMENTS
# ------------------------------------------------------------
records = [load_department(d) for d in DEPARTMENTS]
loaded = [r for r in records if r["loaded"]]

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown(
    """
<div class="exec-header">
    <div class="exec-small">PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL</div>
    <div class="exec-title">SCREEN 01 : ENTERPRISE EXECUTIVE OVERVIEW</div>
    <div class="exec-sub">Enterprise PSM Health at a Glance</div>
    <div class="plant-online">● PLANT STATUS : ONLINE</div>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# TOP CONTROLS
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns([1.15, 1.15, 1.0, 1.0])

with c1:
    month = st.selectbox(
        "DATE / REPORTING MONTH",
        ["July 2026", "June 2026", "May 2026", "April 2026"],
        index=0,
    )

with c2:
    view = st.radio(
        "VIEW",
        ["For the Month", "Year Till Date"],
        horizontal=True,
    )

with c3:
    st.metric("DATA REFRESH", "Current")

with c4:
    st.metric("DEPARTMENTS", f"{len(loaded)}/15")

# ------------------------------------------------------------
# CALCULATE ENTERPRISE TOTALS
# ------------------------------------------------------------
def total(key):
    return sum(num(r.get(key, 0)) for r in loaded)


incidents = total("incidents")
equipment = total("equipment_failure")
barrier_bad = total("barrier_unacceptable")
interlock = total("interlock_open")
moc_pending = total("moc_pending")
recommendations = total("recommendations")
audit_delayed = total("audit_delayed")
pha_delayed = total("pha_delayed")

assessed = total("barrier_assessed")
barrier_health = (
    ((assessed - barrier_bad) / assessed) * 100
    if assessed > 0 else None
)

# ------------------------------------------------------------
# ENTERPRISE HEALTH / PILLARS
# Current department Excel does not contain 14-pillar score cells.
# Therefore these are displayed as Pending rather than fabricated.
# ------------------------------------------------------------
st.markdown('<div class="section">1. ENTERPRISE PSM HEALTH SCORE</div>', unsafe_allow_html=True)

health_col, pillar_col, risk_col = st.columns([1.0, 1.65, 1.0])

with health_col:
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=0,
            number={"suffix": "%", "font": {"size": 38, "color": "#758391"}},
            title={"text": "PSM HEALTH<br><span style='font-size:11px'>DATA PENDING</span>"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#b7c4ce"},
                "steps": [
                    {"range": [0, 70], "color": "#f3dddd"},
                    {"range": [70, 90], "color": "#f7edcf"},
                    {"range": [90, 100], "color": "#dff0df"},
                ],
            },
        )
    )
    gauge.update_layout(
        height=270,
        margin=dict(l=20, r=20, t=45, b=10),
    )
    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div class="info"><b>Target:</b> 95% &nbsp; | &nbsp; '
        'Enterprise health score will be calculated when the 14-pillar score source is connected.</div>',
        unsafe_allow_html=True,
    )

with pillar_col:
    st.markdown('<div class="section">2. 14 PSM PILLARS STATUS</div>', unsafe_allow_html=True)

    rows = []
    for start in range(0, 14, 5):
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            p = start + idx
            if p >= 14:
                continue
            with col:
                st.markdown(
                    f"""
                    <div class="pillar">
                        <div class="pillar-no">{p+1}</div>
                        <div class="pillar-name">{PILLARS[p]}</div>
                        <div class="pillar-score pillar-pending">—</div>
                        <div class="kpi-sub">DATA PENDING</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        '<div class="legend">'
        '<span>🟢 ≥90% Excellent</span>'
        '<span>🟠 70–89% Needs Attention</span>'
        '<span>🔴 &lt;70% Poor</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with risk_col:
    st.markdown('<div class="section">3. ENTERPRISE RISK STATUS</div>', unsafe_allow_html=True)

    risk_fig = go.Figure(
        go.Pie(
            labels=["Risk Register"],
            values=[1],
            hole=.63,
            textinfo="none",
            marker=dict(colors=["#d8e0e6"]),
        )
    )
    risk_fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        annotations=[
            dict(
                text="DATA<br>PENDING",
                x=.5, y=.5,
                font=dict(size=16, color="#71818d"),
                showarrow=False,
            )
        ],
    )
    st.plotly_chart(risk_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div class="info">Enterprise risk counts require the PSM risk register. '
        'No risk values are copied from department incident data.</div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# EXECUTIVE KPI STRIP
# ------------------------------------------------------------
st.markdown('<div class="section">4. EXECUTIVE STATUS AT A GLANCE</div>', unsafe_allow_html=True)

cols = st.columns(6)

items = [
    ("🏭", "DEPARTMENTS", "15", "blue", "Configured"),
    ("📂", "DATA AVAILABLE", f"{len(loaded)}/15",
     "green" if len(loaded) == 15 else "orange", "Excel sources"),
    ("⚠️", "PS INCIDENTS", fmt(incidents),
     "red" if incidents > 0 else "green", "Available data"),
    ("⚙️", "EQUIPMENT FAILURE", fmt(equipment),
     "red" if equipment > 0 else "green", "Available data"),
    ("🧱", "UNACCEPTABLE BARRIERS", fmt(barrier_bad),
     "red" if barrier_bad > 0 else "green", "Available data"),
    ("🔐", "INTERLOCK OPEN", fmt(interlock),
     "orange" if interlock > 0 else "green", "Available data"),
]

for col, item in zip(cols, items):
    with col:
        st.markdown(kpi(*item), unsafe_allow_html=True)

# ------------------------------------------------------------
# DEPARTMENT PERFORMANCE
# ------------------------------------------------------------
st.markdown('<div class="section">5. DEPARTMENT PERFORMANCE</div>', unsafe_allow_html=True)

df = pd.DataFrame([
    {
        "Department": r["department"],
        "Status": "Available" if r["loaded"] else "Pending",
        "Incidents": r.get("incidents", 0) if r["loaded"] else None,
        "MOC Pending": r.get("moc_pending", 0) if r["loaded"] else None,
        "Recommendations": r.get("recommendations", 0) if r["loaded"] else None,
        "Barrier Health %": r.get("barrier_health") if r["loaded"] else None,
    }
    for r in records
])

chart_df = df[df["Status"] == "Available"].copy()

if not chart_df.empty:
    fig = px.bar(
        chart_df,
        x="Department",
        y="Incidents",
        title="PROCESS SAFETY INCIDENTS BY DEPARTMENT",
        text_auto=True,
    )
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=70),
        xaxis_tickangle=-45,
        font=dict(size=9),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
else:
    st.info("No department Excel data available.")

# ------------------------------------------------------------
# LOWER DASHBOARD BLOCKS
# ------------------------------------------------------------
a, b, c, d = st.columns(4)

with a:
    st.markdown('<div class="section">6. INCIDENT STATUS</div>', unsafe_allow_html=True)
    for icon, name, key, color in [
        ("🔴", "Tier-1 / Level-1", "level1", "red"),
        ("🟠", "Tier-2 / Level-2", "level2", "orange"),
        ("🟡", "Tier-3 / Level-3", "level3", "orange"),
        ("🟢", "Level-4", "level4", "green"),
    ]:
        st.markdown(
            kpi(icon, name, fmt(total(key)), color),
            unsafe_allow_html=True,
        )

with b:
    st.markdown('<div class="section">7. MOC STATUS</div>', unsafe_allow_html=True)
    for icon, name, key, color in [
        ("🔵", "Open / Pending", "moc_pending", "blue"),
        ("🟣", "Kaizen MOC", "kaizen_moc", "purple"),
        ("🟠", "Emergency MOC", "emergency_moc", "orange"),
        ("🔴", "Temporary Overdue", "temporary_overdue", "red"),
    ]:
        st.markdown(
            kpi(icon, name, fmt(total(key)), color),
            unsafe_allow_html=True,
        )

with c:
    st.markdown('<div class="section">8. PSSR / TRAINING</div>', unsafe_allow_html=True)
    st.markdown(kpi("📋", "PSSR", "—", "gray", "Source not connected"), unsafe_allow_html=True)
    st.markdown(kpi("🎓", "TRAINING", "—", "gray", "Source not connected"), unsafe_allow_html=True)
    st.markdown(kpi("👷", "CONTRACTOR", "—", "gray", "Source not connected"), unsafe_allow_html=True)

with d:
    st.markdown('<div class="section">9. AUDIT / RECOMMENDATIONS</div>', unsafe_allow_html=True)
    st.markdown(kpi("📌", "OPEN RECOMMENDATIONS", fmt(recommendations),
                    "red" if recommendations else "green"), unsafe_allow_html=True)
    st.markdown(kpi("🧾", "AUDIT DELAYED", fmt(audit_delayed),
                    "red" if audit_delayed else "green"), unsafe_allow_html=True)
    st.markdown(kpi("📋", "PHA DELAYED", fmt(pha_delayed),
                    "orange" if pha_delayed else "green"), unsafe_allow_html=True)

# ------------------------------------------------------------
# BARRIER / MOC / INCIDENT GRAPH
# ------------------------------------------------------------
st.markdown('<div class="section">10. ENTERPRISE PSM PERFORMANCE GRAPHICS</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    if not chart_df.empty:
        plot = chart_df[
            ["Department", "MOC Pending", "Recommendations"]
        ].melt(
            id_vars="Department",
            var_name="Metric",
            value_name="Value",
        )

        fig = px.bar(
            plot,
            x="Department",
            y="Value",
            color="Metric",
            barmode="group",
            title="MOC & RECOMMENDATIONS BY DEPARTMENT",
        )
        fig.update_layout(
            height=310,
            margin=dict(l=10, r=10, t=45, b=70),
            xaxis_tickangle=-45,
            font=dict(size=9),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with g2:
    if barrier_health is not None:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=barrier_health,
                number={"suffix": "%"},
                title={"text": "ENTERPRISE SAFETY BARRIER HEALTH"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#198b37"},
                    "steps": [
                        {"range": [0, 70], "color": "#f4dada"},
                        {"range": [70, 90], "color": "#f8edc9"},
                        {"range": [90, 100], "color": "#dff1df"},
                    ],
                },
            )
        )
        fig.update_layout(
            height=310,
            margin=dict(l=20, r=20, t=45, b=10),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown(
            '<div class="panel" style="height:310px;text-align:center;padding-top:120px;">'
            '<b style="color:#6e7f8d;">SAFETY BARRIER HEALTH<br><br>'
            'DATA PENDING</b></div>',
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------
# ENTERPRISE RANKING
# ------------------------------------------------------------
st.markdown('<div class="section">11. DEPARTMENT DATA STATUS</div>', unsafe_allow_html=True)

status_df = pd.DataFrame({
    "Rank": range(1, 16),
    "Department": DEPARTMENTS,
    "Data Status": [
        "AVAILABLE" if r["loaded"] else "DATA PENDING"
        for r in records
    ],
    "Source": [
        r["source"] if r["loaded"] else "Excel not available"
        for r in records
    ],
})

st.dataframe(
    status_df,
    use_container_width=True,
    hide_index=True,
)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
pending_count = 15 - len(loaded)

st.markdown(
    f"""
    <div class="info" style="text-align:center;margin-top:8px;">
        <b>PSM EXECUTIVE DASHBOARD</b> &nbsp;|&nbsp;
        Reporting: {month} &nbsp;|&nbsp; {view} &nbsp;|&nbsp;
        {len(loaded)} department Excel source(s) connected &nbsp;|&nbsp;
        {pending_count} department(s) pending data.
        <br>
        No missing department values are substituted with another department's data.
    </div>
    """,
    unsafe_allow_html=True,
)