import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import re
import math

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="Screen 02 - Apex Committee",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONSTANTS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DEPT_DIR = BASE_DIR / "data" / "departments"

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
    "Process Hazard Analysis (PHA)",
    "Operating Procedures",
    "Mechanical Integrity",
    "Training & Competence",
    "Management of Change (MOC)",
    "Pre-Startup Safety Review (PSSR)",
    "Contractor Safety Management",
    "Emergency Planning & Response",
    "Incident Investigation",
    "Compliance & Audit",
    "Employee Participation",
    "Trade Secrets / Critical Info",
    "Management Review",
]

# Exact row/column structure already used by the Individual Department page.
# Excel rows are represented here as zero-based pandas row indexes.
# Row 5 = monthly top section; Row 10 = monthly bottom section.
MONTH_TOP_ROW = 5
MONTH_BOTTOM_ROW = 10

# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #eef5fb;
    }

    .main-header {
        background: linear-gradient(110deg, #062d50, #075f84);
        border: 2px solid #00a8df;
        border-radius: 14px;
        padding: 14px 18px 12px 18px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 18px rgba(0,45,80,.25);
        margin-bottom: 10px;
    }

    .main-title {
        font-size: 18px;
        font-weight: 800;
        letter-spacing: .5px;
    }

    .screen-title {
        font-size: 29px;
        font-weight: 900;
        color: #ffd000;
        margin-top: 3px;
    }

    .main-subtitle {
        font-size: 14px;
        font-weight: 600;
        margin-top: 2px;
    }

    .online {
        display: inline-block;
        background: #063a20;
        color: #54f18a;
        border: 1px solid #24bb61;
        border-radius: 20px;
        padding: 4px 18px;
        margin-top: 7px;
        font-weight: 800;
        font-size: 12px;
    }

    .panel {
        background: white;
        border: 1px solid #7fa7c4;
        border-radius: 10px;
        padding: 8px;
        box-shadow: 0 2px 8px rgba(0,40,80,.12);
    }

    .panel-title {
        text-align: center;
        color: #092d50;
        font-weight: 900;
        font-size: 13px;
        border-bottom: 1px solid #9bb6ca;
        padding: 4px 2px 8px;
        margin-bottom: 7px;
    }

    .section-title {
        color: #07345b;
        font-size: 18px;
        font-weight: 900;
        margin: 9px 0 5px;
        padding: 6px 10px;
        border-left: 5px solid #00a8df;
        background: white;
        border-radius: 5px;
    }

    .data-note {
        background: #eaf6ff;
        border: 1px solid #73b9e5;
        color: #17486c;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0 10px;
        font-weight: 600;
    }

    .pending-note {
        background: #fff8df;
        border: 1px solid #e6c35a;
        color: #705700;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0 10px;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #9db8cc;
        border-radius: 8px;
        padding: 8px 12px;
        box-shadow: 0 2px 6px rgba(0,40,80,.08);
    }

    .real-badge {
        color: #087a2b;
        font-weight: 800;
    }

    .pending-badge {
        color: #a56a00;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================
def clean_number(value):
    """Convert Excel values such as 11, 11.0, 50%, N/A to float/None."""
    if value is None:
        return None

    if isinstance(value, bool):
        return float(value)

    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    upper = text.upper()
    if upper in {"N/A", "NA", "N.A.", "U/P", "UP", "-", "--", "NIL", "NONE"}:
        return None

    # Remove commas and extract first numeric value.
    text = text.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None

    try:
        number = float(match.group())
        if "%" in text:
            return number
        return number
    except Exception:
        return None


def value_at(df, row, col):
    """Safely read a value from the known Excel matrix."""
    try:
        if row >= len(df) or col >= len(df.columns):
            return None
        return clean_number(df.iloc[row, col])
    except Exception:
        return None


def find_file(department):
    """Match dashboard department name to the actual file name."""
    if not DEPT_DIR.exists():
        return None

    files = list(DEPT_DIR.glob("*.xlsx")) + list(DEPT_DIR.glob("*.xls"))

    target = department.lower().strip()

    for f in files:
        stem = f.stem.lower().strip()

        if stem == target:
            return f

    # Current file is named Coke Oven.xlsx while dashboard department is Coke Oven-1.
    if target == "coke oven-1":
        for f in files:
            if f.stem.lower().strip() == "coke oven":
                return f

    return None


def load_excel_data(file_path):
    """Load a department Excel file without assuming column headers."""
    try:
        return pd.read_excel(file_path, header=None)
    except Exception:
        return None


def read_department(department):
    """
    Read actual monthly data from one department Excel.

    Returns a dictionary containing only values supported by the
    current Excel template. No PSM score is invented.
    """
    file_path = find_file(department)

    if file_path is None:
        return {
            "department": department,
            "available": False,
            "file": None,
        }

    df = load_excel_data(file_path)

    if df is None or df.empty:
        return {
            "department": department,
            "available": False,
            "file": file_path.name,
        }

    # Monthly incident / process-safety values.
    l1 = value_at(df, MONTH_TOP_ROW, 1)
    l2 = value_at(df, MONTH_TOP_ROW, 2)
    l3 = value_at(df, MONTH_TOP_ROW, 3)
    l4 = value_at(df, MONTH_TOP_ROW, 4)
    investigation_30 = value_at(df, MONTH_TOP_ROW, 5)
    soc = value_at(df, MONTH_TOP_ROW, 6)
    sol = value_at(df, MONTH_TOP_ROW, 7)
    equipment_failure = value_at(df, MONTH_TOP_ROW, 8)

    # Barrier.
    barrier_total = value_at(df, MONTH_TOP_ROW, 19)
    barrier_assessed = value_at(df, MONTH_TOP_ROW, 20)
    barrier_unacceptable = value_at(df, MONTH_TOP_ROW, 21)

    # Monthly bottom section.
    third_party_close = value_at(df, MONTH_BOTTOM_ROW, 1)
    third_party_delayed = value_at(df, MONTH_BOTTOM_ROW, 2)
    incident_rec_close = value_at(df, MONTH_BOTTOM_ROW, 3)
    incident_rec_delayed = value_at(df, MONTH_BOTTOM_ROW, 4)

    pt_plan = value_at(df, MONTH_BOTTOM_ROW, 6)
    pt_actual = value_at(df, MONTH_BOTTOM_ROW, 7)

    pha_plan = value_at(df, MONTH_BOTTOM_ROW, 8)
    pha_actual = value_at(df, MONTH_BOTTOM_ROW, 9)
    pha_close = value_at(df, MONTH_BOTTOM_ROW, 10)
    pha_delayed = value_at(df, MONTH_BOTTOM_ROW, 11)

    audit_close = value_at(df, MONTH_BOTTOM_ROW, 12)
    audit_delayed = value_at(df, MONTH_BOTTOM_ROW, 13)

    moc_pending = value_at(df, MONTH_BOTTOM_ROW, 14)
    kaizen_moc = value_at(df, MONTH_BOTTOM_ROW, 16)
    emergency_moc = value_at(df, MONTH_BOTTOM_ROW, 18)
    temporary_overdue = value_at(df, MONTH_BOTTOM_ROW, 20)

    interlock_open = value_at(df, MONTH_BOTTOM_ROW, 22)
    normalisation_overdue = value_at(df, MONTH_BOTTOM_ROW, 23)

    incidents = sum(
        x or 0 for x in [l1, l2, l3, l4]
    )

    recommendations_open = sum(
        x or 0
        for x in [
            third_party_delayed,
            incident_rec_delayed,
            pha_delayed,
            audit_delayed,
        ]
    )

    # PSM pillar score is intentionally NOT calculated from these KPIs.
    # It requires actual pillar assessment data.
    return {
        "department": department,
        "available": True,
        "file": file_path.name,

        "l1": l1 or 0,
        "l2": l2 or 0,
        "l3": l3 or 0,
        "l4": l4 or 0,
        "investigation_30": investigation_30 or 0,
        "soc": soc or 0,
        "sol": sol or 0,
        "equipment_failure": equipment_failure or 0,

        "barrier_total": barrier_total or 0,
        "barrier_assessed": barrier_assessed or 0,
        "barrier_unacceptable": barrier_unacceptable or 0,

        "third_party_close": third_party_close or 0,
        "third_party_delayed": third_party_delayed or 0,
        "incident_rec_close": incident_rec_close or 0,
        "incident_rec_delayed": incident_rec_delayed or 0,

        "pt_plan": pt_plan or 0,
        "pt_actual": pt_actual or 0,

        "pha_plan": pha_plan or 0,
        "pha_actual": pha_actual or 0,
        "pha_close": pha_close or 0,
        "pha_delayed": pha_delayed or 0,

        "audit_close": audit_close or 0,
        "audit_delayed": audit_delayed or 0,

        "moc_pending": moc_pending or 0,
        "kaizen_moc": kaizen_moc or 0,
        "emergency_moc": emergency_moc or 0,
        "temporary_overdue": temporary_overdue or 0,

        "interlock_open": interlock_open or 0,
        "normalisation_overdue": normalisation_overdue or 0,

        "incidents": incidents,
        "recommendations_open": recommendations_open,

        "pillar_scores": [None] * 14,
        "overall_score": None,
    }


def load_all_departments():
    return {
        dept: read_department(dept)
        for dept in DEPARTMENTS
    }


def fmt_number(value):
    if value is None:
        return "—"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


# ============================================================
# LOAD REAL DATA
# ============================================================
data = load_all_departments()
available = [d for d in DEPARTMENTS if data[d]["available"]]
pending = [d for d in DEPARTMENTS if not data[d]["available"]]

# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL</div>
        <div class="screen-title">SCREEN 02 : APEX COMMITTEE PERFORMANCE DASHBOARD</div>
        <div class="main-subtitle">Apex Committee Overview of PSM Implementation Across Plant</div>
        <div class="online">PLANT STATUS : ONLINE ●</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CONTROL BAR
# ============================================================
c1, c2, c3 = st.columns([1.2, 1.2, 1.2])

with c1:
    reporting_month = st.selectbox(
        "REPORTING MONTH",
        [
            "January 2026",
            "February 2026",
            "March 2026",
            "April 2026",
            "May 2026",
            "June 2026",
            "July 2026",
            "August 2026",
            "September 2026",
            "October 2026",
            "November 2026",
            "December 2026",
        ],
        index=6,
    )

with c2:
    st.metric("EXCEL DATA AVAILABLE", f"{len(available)} / {len(DEPARTMENTS)}")

with c3:
    st.metric("LAST REFRESH", datetime.now().strftime("%d-%b-%Y %H:%M:%S"))

if available:
    st.markdown(
        f'<div class="data-note">🟢 REAL EXCEL DATA LOADED: '
        f'{", ".join(available)}</div>',
        unsafe_allow_html=True,
    )

if pending:
    st.markdown(
        f'<div class="pending-note">🟡 DATA PENDING: {len(pending)} '
        f'departments have no Excel file yet. Their values are shown as "—".</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# CONSOLIDATED REAL KPIs
# ============================================================
total_incidents = sum(data[d]["incidents"] for d in available)
total_equipment_failures = sum(data[d]["equipment_failure"] for d in available)
total_unacceptable_barriers = sum(data[d]["barrier_unacceptable"] for d in available)
total_interlocks = sum(data[d]["interlock_open"] for d in available)
total_open_recommendations = sum(data[d]["recommendations_open"] for d in available)

# ============================================================
# TOP KPI STRIP
# ============================================================
st.markdown(
    '<div class="section-title">📊 EXECUTIVE DATA SNAPSHOT</div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric("TOTAL DEPARTMENTS", len(DEPARTMENTS))

with k2:
    st.metric("DATA AVAILABLE", f"{len(available)}/{len(DEPARTMENTS)}")

with k3:
    st.metric("PS INCIDENTS (L1-L4)", fmt_number(total_incidents))

with k4:
    st.metric("EQUIPMENT FAILURE", fmt_number(total_equipment_failures))

with k5:
    st.metric("UNACCEPTABLE BARRIERS", fmt_number(total_unacceptable_barriers))

with k6:
    st.metric("INTERLOCK OPEN", fmt_number(total_interlocks))

# ============================================================
# MAIN 3-PANEL AREA
# ============================================================
left, middle, right = st.columns([1.0, 1.45, 1.2])

# ------------------------------------------------------------
# 1. OVERALL PSM IMPLEMENTATION
# ------------------------------------------------------------
with left:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '1. OVERALL PSM IMPLEMENTATION PROGRESS'
        '</div>',
        unsafe_allow_html=True,
    )

    # No fake overall score.
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=0,
            number={
                "suffix": "",
                "font": {"size": 38, "color": "#8b8b8b"},
            },
            title={
                "text": "DATA PENDING",
                "font": {"size": 20, "color": "#8b8b8b"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickvals": [0, 25, 50, 75, 100],
                },
                "bar": {"color": "#9daab5"},
                "steps": [
                    {"range": [0, 70], "color": "#ffd7d7"},
                    {"range": [70, 90], "color": "#fff0b8"},
                    {"range": [90, 100], "color": "#d7f3dc"},
                ],
                "threshold": {
                    "line": {"color": "#333333", "width": 5},
                    "thickness": 0.75,
                    "value": 0,
                },
            },
        )
    )

    gauge.update_layout(
        height=285,
        margin=dict(l=15, r=15, t=25, b=10),
        paper_bgcolor="white",
        font=dict(color="#173b59"),
    )

    st.plotly_chart(
        gauge,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.caption("Overall PSM score will be available when pillar assessment data is provided.")
    st.caption(f"Real department files loaded: {len(available)} / {len(DEPARTMENTS)}")

# ------------------------------------------------------------
# 2. 14 PSM PILLARS
# ------------------------------------------------------------
with middle:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '2. 14 PSM PILLARS PROGRESS'
        '</div>',
        unsafe_allow_html=True,
    )

    pillar_df = pd.DataFrame({
        "PILLAR": range(1, 15),
        "PILLAR NAME": PILLARS,
        "WEIGHTAGE": [
            "7%", "7%", "7%", "10%", "7%", "8%", "6%",
            "6%", "6%", "6%", "6%", "4%", "2%", "4%"
        ],
        "SCORE (%)": ["—"] * 14,
        "STATUS": ["DATA PENDING"] * 14,
    })

    st.dataframe(
        pillar_df,
        use_container_width=True,
        hide_index=True,
        height=440,
        column_config={
            "PILLAR": st.column_config.NumberColumn(width="small"),
            "PILLAR NAME": st.column_config.TextColumn(width="large"),
            "WEIGHTAGE": st.column_config.TextColumn(width="small"),
            "SCORE (%)": st.column_config.TextColumn(width="small"),
            "STATUS": st.column_config.TextColumn(width="medium"),
        },
    )

    st.caption("Pillar scores are not inferred from incident/KPI counts.")

# ------------------------------------------------------------
# 3. DEPARTMENT WISE SCORE / DATA STATUS
# ------------------------------------------------------------
with right:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '3. DEPARTMENT WISE IMPLEMENTATION SCORE'
        '</div>',
        unsafe_allow_html=True,
    )

    rows = []
    for rank, dept in enumerate(DEPARTMENTS, start=1):
        item = data[dept]

        rows.append({
            "RANK": rank,
            "DEPARTMENT": dept,
            "SCORE (%)": "—",
            "DATA STATUS": "DATA AVAILABLE" if item["available"] else "DATA PENDING",
            "FILE": item["file"] or "—",
        })

    dept_df = pd.DataFrame(rows)

    st.dataframe(
        dept_df,
        use_container_width=True,
        hide_index=True,
        height=440,
        column_config={
            "RANK": st.column_config.NumberColumn(width="small"),
            "DEPARTMENT": st.column_config.TextColumn(width="medium"),
            "SCORE (%)": st.column_config.TextColumn(width="small"),
            "DATA STATUS": st.column_config.TextColumn(width="medium"),
            "FILE": st.column_config.TextColumn(width="medium"),
        },
    )

# ============================================================
# REAL DATA GRAPHICS
# ============================================================
st.markdown(
    '<div class="section-title">📈 REAL DEPARTMENT DATA ANALYSIS</div>',
    unsafe_allow_html=True,
)

g1, g2, g3 = st.columns(3)

# ------------------------------------------------------------
# Incident chart
# ------------------------------------------------------------
with g1:
    incident_rows = []
    for dept in available:
        incident_rows.append({
            "Department": dept,
            "L1": data[dept]["l1"],
            "L2": data[dept]["l2"],
            "L3": data[dept]["l3"],
            "L4": data[dept]["l4"],
        })

    if incident_rows:
        inc_df = pd.DataFrame(incident_rows)

        fig = go.Figure()
        for level in ["L1", "L2", "L3", "L4"]:
            fig.add_trace(
                go.Bar(
                    x=inc_df["Department"],
                    y=inc_df[level],
                    name=level,
                )
            )

        fig.update_layout(
            title="PROCESS SAFETY INCIDENTS",
            barmode="stack",
            height=330,
            margin=dict(l=10, r=10, t=45, b=80),
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(orientation="h"),
            xaxis=dict(tickangle=-35),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.info("No department Excel data available.")

# ------------------------------------------------------------
# Recommendations chart
# ------------------------------------------------------------
with g2:
    if available:
        rec_df = pd.DataFrame([
            {
                "Department": d,
                "Open Recommendations": data[d]["recommendations_open"],
            }
            for d in available
        ])

        fig = go.Figure(
            go.Bar(
                x=rec_df["Department"],
                y=rec_df["Open Recommendations"],
                text=rec_df["Open Recommendations"],
                textposition="outside",
            )
        )

        fig.update_layout(
            title="OPEN RECOMMENDATIONS",
            height=330,
            margin=dict(l=10, r=10, t=45, b=80),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(tickangle=-35),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.info("No department Excel data available.")

# ------------------------------------------------------------
# Interlock chart
# ------------------------------------------------------------
with g3:
    if available:
        interlock_df = pd.DataFrame([
            {
                "Department": d,
                "Interlock Open": data[d]["interlock_open"],
                "Normalization Overdue": data[d]["normalisation_overdue"],
            }
            for d in available
        ])

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=interlock_df["Department"],
                y=interlock_df["Interlock Open"],
                name="Interlock Open",
            )
        )
        fig.add_trace(
            go.Bar(
                x=interlock_df["Department"],
                y=interlock_df["Normalization Overdue"],
                name="Normalization Overdue",
            )
        )

        fig.update_layout(
            title="INTERLOCK / NORMALISATION STATUS",
            barmode="group",
            height=330,
            margin=dict(l=10, r=10, t=45, b=80),
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict(orientation="h"),
            xaxis=dict(tickangle=-35),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.info("No department Excel data available.")

# ============================================================
# ACTION TRACKER
# ============================================================
st.markdown(
    '<div class="section-title">4. APEX COMMITTEE ACTION / RECOMMENDATION TRACKER</div>',
    unsafe_allow_html=True,
)

a1, a2, a3, a4 = st.columns(4)

with a1:
    st.metric("OPEN RECOMMENDATIONS", fmt_number(total_open_recommendations))

with a2:
    st.metric(
        "THIRD PARTY DELAYED",
        fmt_number(sum(data[d]["third_party_delayed"] for d in available)),
    )

with a3:
    st.metric(
        "PHA DELAYED",
        fmt_number(sum(data[d]["pha_delayed"] for d in available)),
    )

with a4:
    st.metric(
        "AUDIT DELAYED",
        fmt_number(sum(data[d]["audit_delayed"] for d in available)),
    )

# ============================================================
# REAL DATA DETAIL TABLE
# ============================================================
st.markdown(
    '<div class="section-title">5. DEPARTMENT KPI DETAIL — REAL EXCEL DATA</div>',
    unsafe_allow_html=True,
)

detail_rows = []

for dept in available:
    x = data[dept]

    detail_rows.append({
        "Department": dept,
        "Incidents L1-L4": fmt_number(x["incidents"]),
        "Equipment Failure": fmt_number(x["equipment_failure"]),
        "Barrier Unacceptable": fmt_number(x["barrier_unacceptable"]),
        "Open Recommendations": fmt_number(x["recommendations_open"]),
        "MOC Pending": fmt_number(x["moc_pending"]),
        "Interlock Open": fmt_number(x["interlock_open"]),
        "Normalization Overdue": fmt_number(x["normalisation_overdue"]),
        "PT Actual": fmt_number(x["pt_actual"]),
        "PT Planned": fmt_number(x["pt_plan"]),
        "PHA Actual": fmt_number(x["pha_actual"]),
        "PHA Planned": fmt_number(x["pha_plan"]),
    })

if detail_rows:
    detail_df = pd.DataFrame(detail_rows)

    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
        height=250,
    )
else:
    st.info("No actual department Excel data is currently available.")

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div style="
        text-align:center;
        color:#52718a;
        padding:12px;
        font-size:12px;
        font-weight:600;
    ">
        PSM Dashboard • Screen 02 • Apex Committee Performance
        • Real Excel data where available
    </div>
    """,
    unsafe_allow_html=True,
)