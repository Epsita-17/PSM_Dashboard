import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import re
import math

# ============================================================
# SCREEN 03 - PSM STEERING COMMITTEE DASHBOARD
# DATA SOURCE:
#     data/departments/*.xlsx
#
# This page uses REAL values available in the current
# department Excel template. It does NOT invent unsupported
# PSM scores, decisions, budgets or trends.
# ============================================================

st.set_page_config(
    page_title="Screen 03 - Steering Committee",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PATHS / MASTER LIST
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

# Existing Individual Department Excel structure:
# monthly top section = pandas row 5
# monthly bottom section = pandas row 10
TOP_ROW = 5
BOTTOM_ROW = 10


# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #eaf2f8;
    }

    .main-header {
        background: linear-gradient(105deg, #041d36, #075b82);
        border: 2px solid #00a9e8;
        border-radius: 12px;
        color: white;
        padding: 8px 14px 10px;
        text-align: center;
        margin-bottom: 8px;
        box-shadow: 0 4px 14px rgba(0,35,65,.22);
    }

    .main-title {
        font-size: 17px;
        font-weight: 800;
        letter-spacing: .4px;
    }

    .screen-title {
        color: #ffd000;
        font-size: 27px;
        font-weight: 900;
        line-height: 1.05;
        margin: 2px 0;
    }

    .sub-title {
        font-size: 13px;
        font-weight: 700;
    }

    .online {
        display: inline-block;
        margin-top: 5px;
        padding: 3px 15px;
        border: 1px solid #27bb62;
        background: #073b22;
        color: #54ef88;
        border-radius: 15px;
        font-weight: 800;
        font-size: 11px;
    }

    .panel {
        background: white;
        border: 1px solid #7fa6c2;
        border-radius: 9px;
        padding: 7px;
        box-shadow: 0 2px 7px rgba(0,40,80,.12);
        height: 100%;
    }

    .panel-title {
        color: #0a3154;
        font-weight: 900;
        font-size: 12px;
        text-align: center;
        border-bottom: 1px solid #9cb5c8;
        padding: 3px 2px 7px;
        margin-bottom: 5px;
    }

    .section-title {
        background: white;
        color: #07345b;
        border-left: 5px solid #00a9e8;
        border-radius: 5px;
        padding: 6px 10px;
        margin: 8px 0 5px;
        font-size: 16px;
        font-weight: 900;
    }

    .real {
        background: #e6f7ed;
        color: #096c2d;
        border: 1px solid #79c998;
        padding: 6px 10px;
        border-radius: 6px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .pending {
        background: #fff7df;
        color: #735900;
        border: 1px solid #e3c15a;
        padding: 6px 10px;
        border-radius: 6px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #9db9ce;
        border-radius: 7px;
        padding: 6px 10px;
    }

    .small-note {
        color: #536d82;
        font-size: 11px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA HELPERS
# ============================================================
def number(value):
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

    if text.upper() in {
        "N/A", "NA", "N.A.", "U/P", "UP", "-", "--",
        "NIL", "NONE", "NOT APPLICABLE"
    }:
        return None

    text = text.replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?", text)

    if not m:
        return None

    try:
        return float(m.group())
    except Exception:
        return None


def value_at(df, row, col):
    try:
        if row >= len(df) or col >= len(df.columns):
            return None
        return number(df.iloc[row, col])
    except Exception:
        return None


def find_excel(department):
    if not DEPT_DIR.exists():
        return None

    files = list(DEPT_DIR.glob("*.xlsx")) + list(DEPT_DIR.glob("*.xls"))

    target = department.lower().strip()

    for f in files:
        if f.stem.lower().strip() == target:
            return f

    # Existing project file: Coke Oven.xlsx
    if target == "coke oven-1":
        for f in files:
            if f.stem.lower().strip() == "coke oven":
                return f

    return None


@st.cache_data(show_spinner=False)
def read_excel(path_string):
    try:
        return pd.read_excel(path_string, header=None)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_department(department):
    path = find_excel(department)

    if path is None:
        return {
            "available": False,
            "department": department,
            "file": None,
        }

    df = read_excel(str(path))

    if df is None or df.empty:
        return {
            "available": False,
            "department": department,
            "file": path.name,
        }

    # --------------------------------------------------------
    # REAL VALUES FROM EXISTING DEPARTMENT TEMPLATE
    # --------------------------------------------------------

    # Incident / process safety section
    l1 = value_at(df, TOP_ROW, 1)
    l2 = value_at(df, TOP_ROW, 2)
    l3 = value_at(df, TOP_ROW, 3)
    l4 = value_at(df, TOP_ROW, 4)

    investigation_30 = value_at(df, TOP_ROW, 5)
    soc = value_at(df, TOP_ROW, 6)
    sol = value_at(df, TOP_ROW, 7)

    equipment_failure = value_at(df, TOP_ROW, 8)

    # Barrier section
    barrier_total = value_at(df, TOP_ROW, 19)
    barrier_assessed = value_at(df, TOP_ROW, 20)
    barrier_unacceptable = value_at(df, TOP_ROW, 21)

    # Recommendation section
    third_party_close = value_at(df, BOTTOM_ROW, 1)
    third_party_delayed = value_at(df, BOTTOM_ROW, 2)

    incident_rec_close = value_at(df, BOTTOM_ROW, 3)
    incident_rec_delayed = value_at(df, BOTTOM_ROW, 4)

    # Training
    pt_plan = value_at(df, BOTTOM_ROW, 6)
    pt_actual = value_at(df, BOTTOM_ROW, 7)

    # PHA
    pha_plan = value_at(df, BOTTOM_ROW, 8)
    pha_actual = value_at(df, BOTTOM_ROW, 9)
    pha_close = value_at(df, BOTTOM_ROW, 10)
    pha_delayed = value_at(df, BOTTOM_ROW, 11)

    # Audit
    audit_close = value_at(df, BOTTOM_ROW, 12)
    audit_delayed = value_at(df, BOTTOM_ROW, 13)

    # MOC
    moc_pending = value_at(df, BOTTOM_ROW, 14)
    kaizen_moc = value_at(df, BOTTOM_ROW, 16)
    emergency_moc = value_at(df, BOTTOM_ROW, 18)
    temporary_overdue = value_at(df, BOTTOM_ROW, 20)

    # Interlock
    interlock_open = value_at(df, BOTTOM_ROW, 22)
    normalisation_overdue = value_at(df, BOTTOM_ROW, 23)

    incident_total = sum(x or 0 for x in [l1, l2, l3, l4])

    open_actions = sum(
        x or 0 for x in [
            third_party_delayed,
            incident_rec_delayed,
            pha_delayed,
            audit_delayed,
        ]
    )

    # A training completion percentage can be calculated only
    # when the Excel contains plan and actual values.
    pt_pct = None
    if pt_plan not in (None, 0) and pt_actual is not None:
        pt_pct = min(100.0, (pt_actual / pt_plan) * 100.0)

    pha_pct = None
    if pha_plan not in (None, 0) and pha_actual is not None:
        pha_pct = min(100.0, (pha_actual / pha_plan) * 100.0)

    # PSM overall/pillar score is deliberately not calculated
    # from unrelated KPI counts.
    return {
        "available": True,
        "department": department,
        "file": path.name,

        "l1": l1 or 0,
        "l2": l2 or 0,
        "l3": l3 or 0,
        "l4": l4 or 0,
        "incident_total": incident_total,

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
        "pt_pct": pt_pct,

        "pha_plan": pha_plan or 0,
        "pha_actual": pha_actual or 0,
        "pha_close": pha_close or 0,
        "pha_delayed": pha_delayed or 0,
        "pha_pct": pha_pct,

        "audit_close": audit_close or 0,
        "audit_delayed": audit_delayed or 0,

        "moc_pending": moc_pending or 0,
        "kaizen_moc": kaizen_moc or 0,
        "emergency_moc": emergency_moc or 0,
        "temporary_overdue": temporary_overdue or 0,

        "interlock_open": interlock_open or 0,
        "normalisation_overdue": normalisation_overdue or 0,

        "open_actions": open_actions,
    }


def fmt(v):
    if v is None:
        return "—"
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.1f}"


# ============================================================
# LOAD ALL REAL DATA
# ============================================================
DATA = {d: load_department(d) for d in DEPARTMENTS}

available = [d for d in DEPARTMENTS if DATA[d]["available"]]
pending = [d for d in DEPARTMENTS if not DATA[d]["available"]]

# Aggregates from real files only.
total_incidents = sum(DATA[d]["incident_total"] for d in available)
total_equipment_failure = sum(DATA[d]["equipment_failure"] for d in available)
total_barrier_bad = sum(DATA[d]["barrier_unacceptable"] for d in available)
total_open_actions = sum(DATA[d]["open_actions"] for d in available)
total_moc_pending = sum(DATA[d]["moc_pending"] for d in available)
total_interlock_open = sum(DATA[d]["interlock_open"] for d in available)
total_audit_delayed = sum(DATA[d]["audit_delayed"] for d in available)
total_pha_delayed = sum(DATA[d]["pha_delayed"] for d in available)

total_pt_plan = sum(DATA[d]["pt_plan"] for d in available)
total_pt_actual = sum(DATA[d]["pt_actual"] for d in available)

total_pha_plan = sum(DATA[d]["pha_plan"] for d in available)
total_pha_actual = sum(DATA[d]["pha_actual"] for d in available)

overall_pt_pct = (
    (total_pt_actual / total_pt_plan) * 100
    if total_pt_plan else None
)

overall_pha_pct = (
    (total_pha_actual / total_pha_plan) * 100
    if total_pha_plan else None
)


# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">
            PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        </div>
        <div class="screen-title">
            SCREEN 03 : PSM STEERING COMMITTEE DASHBOARD
        </div>
        <div class="sub-title">
            Steering Committee Overview | Review | Decision Support
        </div>
        <div class="online">
            PLANT STATUS : ONLINE ●
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOP STATUS
# ============================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("DATE", datetime.now().strftime("%d-%b-%Y"))

with c2:
    st.metric("TIME", datetime.now().strftime("%I:%M:%S %p"))

with c3:
    st.metric("LAST DATA REFRESH", datetime.now().strftime("%I:%M:%S %p"))

with c4:
    st.metric("REAL EXCEL DATA", f"{len(available)}/{len(DEPARTMENTS)}")


st.markdown(
    f'<div class="real">🟢 REAL DATA SOURCE: '
    f'{len(available)} department Excel file(s) loaded.</div>',
    unsafe_allow_html=True,
)

if pending:
    st.markdown(
        f'<div class="pending">🟡 DATA PENDING: '
        f'{len(pending)} department(s) do not have an Excel file yet. '
        f'No value is fabricated for those departments.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# ROW 1
# ============================================================
r1a, r1b, r1c, r1d, r1e = st.columns(
    [1.0, 1.35, 1.0, 1.0, 1.0]
)

# ------------------------------------------------------------
# 1. IMPLEMENTATION SCORE
# ------------------------------------------------------------
with r1a:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '1. PSM IMPLEMENTATION SCORE'
        '</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=0,
            number={
                "suffix": "",
                "font": {"size": 36, "color": "#7d8a94"},
            },
            title={
                "text": "DATA PENDING",
                "font": {"size": 16, "color": "#7d8a94"},
            },
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#8d9aa5"},
                "steps": [
                    {"range": [0, 70], "color": "#ffd8d8"},
                    {"range": [70, 90], "color": "#fff0bd"},
                    {"range": [90, 100], "color": "#d9f2dc"},
                ],
            },
        )
    )

    fig.update_layout(
        height=245,
        margin=dict(l=10, r=10, t=25, b=5),
        paper_bgcolor="white",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.caption(
        "Overall implementation score requires actual 14-pillar "
        "assessment data."
    )

# ------------------------------------------------------------
# 2. PILLAR PERFORMANCE
# ------------------------------------------------------------
with r1b:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '2. PILLAR PERFORMANCE — AVAILABLE REAL DATA'
        '</div>',
        unsafe_allow_html=True,
    )

    pillar_rows = []

    # Only metrics actually available from the Excel template.
    pillar_rows.append({
        "PILLAR": "Training & Competency",
        "ACTUAL": fmt(overall_pt_pct) + ("%" if overall_pt_pct is not None else ""),
        "SOURCE": "PT plan / actual",
    })

    pillar_rows.append({
        "PILLAR": "Process Hazard Analysis (PHA)",
        "ACTUAL": fmt(overall_pha_pct) + ("%" if overall_pha_pct is not None else ""),
        "SOURCE": "PHA plan / actual",
    })

    pillar_rows.append({
        "PILLAR": "Management of Change (MOC)",
        "ACTUAL": fmt(total_moc_pending),
        "SOURCE": "MOC pending count",
    })

    pillar_rows.append({
        "PILLAR": "Incident Investigation",
        "ACTUAL": fmt(total_incidents),
        "SOURCE": "L1 + L2 + L3 + L4",
    })

    pillar_rows.append({
        "PILLAR": "Compliance & Audit",
        "ACTUAL": fmt(total_audit_delayed),
        "SOURCE": "Audit delayed count",
    })

    pillar_rows.append({
        "PILLAR": "Mechanical Integrity",
        "ACTUAL": fmt(total_equipment_failure),
        "SOURCE": "Equipment failure count",
    })

    st.dataframe(
        pd.DataFrame(pillar_rows),
        use_container_width=True,
        hide_index=True,
        height=270,
    )

    st.caption(
        "The Excel template does not contain a complete 14-pillar score "
        "history, so unsupported scores are not generated."
    )

# ------------------------------------------------------------
# 3. STEERING DECISIONS
# ------------------------------------------------------------
with r1c:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '3. STEERING COMMITTEE DECISIONS (YTD)'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("DECISIONS TAKEN", "—")
    st.metric("DECISIONS CLOSED", "—")
    st.metric("PENDING DECISIONS", "—")
    st.metric("OVERDUE DECISIONS", "—")

    st.caption("Decision-register Excel data not yet connected.")

# ------------------------------------------------------------
# 4. CRITICAL FOCUS AREAS
# ------------------------------------------------------------
with r1d:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '4. CRITICAL FOCUS AREAS'
        '</div>',
        unsafe_allow_html=True,
    )

    focus = [
        ("Management of Change", total_moc_pending),
        ("Mechanical Integrity", total_equipment_failure),
        ("Training & Competency", None),
        ("Incident Investigation", total_incidents),
        ("Audit Closure", total_audit_delayed),
        ("PHA", total_pha_delayed),
        ("Interlock", total_interlock_open),
    ]

    focus_df = pd.DataFrame(
        [
            {
                "FOCUS AREA": name,
                "REAL VALUE": fmt(value),
                "STATUS": (
                    "DATA PENDING"
                    if value is None
                    else ("ATTENTION" if value > 0 else "ON TRACK")
                ),
            }
            for name, value in focus
        ]
    )

    st.dataframe(
        focus_df,
        use_container_width=True,
        hide_index=True,
        height=270,
    )

# ------------------------------------------------------------
# 5. RISK PROFILE
# ------------------------------------------------------------
with r1e:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '5. RISK PROFILE SUMMARY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("TOTAL RISK", "—")
    st.metric("CRITICAL", "—")
    st.metric("HIGH", "—")
    st.metric("MEDIUM", "—")
    st.metric("LOW", "—")

    st.caption("Risk-register data is not part of the current department Excel.")


# ============================================================
# ROW 2
# ============================================================
st.markdown(
    '<div class="section-title">6–9. COMMITTEE PERFORMANCE & REVIEW</div>',
    unsafe_allow_html=True,
)

r2a, r2b, r2c, r2d = st.columns([1.05, 1.55, 1.25, 1.0])

# ------------------------------------------------------------
# 6. DEPARTMENT STATUS
# ------------------------------------------------------------
with r2a:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '6. DEPARTMENT IMPLEMENTATION STATUS'
        '</div>',
        unsafe_allow_html=True,
    )

    rows = []

    for rank, dept in enumerate(available, start=1):
        x = DATA[dept]

        # This is NOT a PSM score.
        # It is a real-data activity indicator only.
        issue_count = (
            x["incident_total"]
            + x["moc_pending"]
            + x["interlock_open"]
            + x["audit_delayed"]
            + x["pha_delayed"]
            + x["barrier_unacceptable"]
        )

        status = "Attention" if issue_count > 0 else "On Track"

        rows.append({
            "RANK": rank,
            "DEPARTMENT": dept,
            "ISSUES": int(issue_count),
            "STATUS": status,
        })

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
            height=310,
        )
    else:
        st.info("No Excel files available.")

# ------------------------------------------------------------
# 7. TOP OVERDUE ACTIONS
# ------------------------------------------------------------
with r2b:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '7. TOP OVERDUE ACTIONS — ALL COMMITTEES'
        '</div>',
        unsafe_allow_html=True,
    )

    overdue_rows = []

    for dept in available:
        x = DATA[dept]

        items = [
            ("PHA delayed", x["pha_delayed"], "PHA"),
            ("Audit delayed", x["audit_delayed"], "AUDIT"),
            ("Third-party delayed", x["third_party_delayed"], "RECOMMENDATION"),
            ("Incident recommendation delayed", x["incident_rec_delayed"], "INCIDENT"),
            ("MOC pending", x["moc_pending"], "MOC"),
            ("Interlock open", x["interlock_open"], "INTERLOCK"),
            ("Normalization overdue", x["normalisation_overdue"], "INTERLOCK"),
        ]

        for description, value, pillar in items:
            if value and value > 0:
                overdue_rows.append({
                    "DEPARTMENT": dept,
                    "ACTION": description,
                    "PILLAR": pillar,
                    "COUNT": int(value),
                })

    overdue_rows = sorted(
        overdue_rows,
        key=lambda x: x["COUNT"],
        reverse=True,
    )[:10]

    if overdue_rows:
        st.dataframe(
            pd.DataFrame(overdue_rows),
            use_container_width=True,
            hide_index=True,
            height=310,
        )
    else:
        st.info("No overdue/open action count found in available Excel data.")

# ------------------------------------------------------------
# 8. COMMITTEE MEETING SUMMARY
# ------------------------------------------------------------
with r2c:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '8. COMMITTEE MEETING SUMMARY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("MEETINGS HELD", "—")
    st.metric("ATTENDANCE", "—")
    st.metric("AGENDA ITEMS", "—")
    st.metric("DECISIONS", "—")
    st.metric("ACTION ITEMS", fmt(total_open_actions))
    st.metric("CLOSED ACTIONS", "—")

    st.caption("Meeting register is not in current department Excel.")

# ------------------------------------------------------------
# 9. PSM AUDIT OVERVIEW
# ------------------------------------------------------------
with r2d:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '9. PSM AUDIT OVERVIEW'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("AUDIT DELAYED", fmt(total_audit_delayed))
    st.metric("PHA DELAYED", fmt(total_pha_delayed))
    st.metric("AUDIT CLOSED", fmt(
        sum(DATA[d]["audit_close"] for d in available)
    ))
    st.metric("PHA CLOSED", fmt(
        sum(DATA[d]["pha_close"] for d in available)
    ))

    st.caption("Internal/Cross-functional/Third-party split needs audit data.")


# ============================================================
# ROW 3
# ============================================================
st.markdown(
    '<div class="section-title">10–15. LEADING / LAGGING INDICATORS</div>',
    unsafe_allow_html=True,
)

r3a, r3b, r3c, r3d, r3e, r3f = st.columns(
    [1.0, 1.0, 1.15, 1.15, 1.0, 1.25]
)

# ------------------------------------------------------------
# 10 TRAINING
# ------------------------------------------------------------
with r3a:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '10. TRAINING & COMPETENCY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric(
        "PT COMPLETION",
        fmt(overall_pt_pct) + ("%" if overall_pt_pct is not None else "")
    )
    st.metric("PT ACTUAL", fmt(total_pt_actual))
    st.metric("PT PLAN", fmt(total_pt_plan))

    if overall_pt_pct is not None:
        st.progress(min(1.0, overall_pt_pct / 100))

# ------------------------------------------------------------
# 11 INCIDENT
# ------------------------------------------------------------
with r3b:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '11. INCIDENT SUMMARY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("TIER-1", fmt(sum(DATA[d]["l1"] for d in available)))
    st.metric("TIER-2", fmt(sum(DATA[d]["l2"] for d in available)))
    st.metric("TIER-3", fmt(sum(DATA[d]["l3"] for d in available)))
    st.metric("TIER-4", fmt(sum(DATA[d]["l4"] for d in available)))
    st.metric("TOTAL L1-L4", fmt(total_incidents))

# ------------------------------------------------------------
# 12 MOC
# ------------------------------------------------------------
with r3c:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '12. MOC SUMMARY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("MOC PENDING", fmt(total_moc_pending))
    st.metric(
        "KAIZEN MOC",
        fmt(sum(DATA[d]["kaizen_moc"] for d in available)),
    )
    st.metric(
        "EMERGENCY MOC",
        fmt(sum(DATA[d]["emergency_moc"] for d in available)),
    )
    st.metric(
        "TEMP. OVERDUE",
        fmt(sum(DATA[d]["temporary_overdue"] for d in available)),
    )

# ------------------------------------------------------------
# 13 PSSR / PHA
# ------------------------------------------------------------
with r3d:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '13. PSSR / PHA SUMMARY'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("PHA PLAN", fmt(total_pha_plan))
    st.metric("PHA ACTUAL", fmt(total_pha_actual))
    st.metric("PHA CLOSED", fmt(
        sum(DATA[d]["pha_close"] for d in available)
    ))
    st.metric("PHA DELAYED", fmt(total_pha_delayed))

    if overall_pha_pct is not None:
        st.progress(min(1.0, overall_pha_pct / 100))

# ------------------------------------------------------------
# 14 BUDGET
# ------------------------------------------------------------
with r3e:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '14. BUDGET UTILIZATION'
        '</div>',
        unsafe_allow_html=True,
    )

    st.metric("BUDGET", "—")
    st.metric("SPENT", "—")
    st.metric("BALANCE", "—")
    st.caption("Budget data source not connected.")

# ------------------------------------------------------------
# 15 AI INSIGHTS
# ------------------------------------------------------------
with r3f:
    st.markdown(
        '<div class="panel"><div class="panel-title">'
        '15. DATA-DRIVEN STEERING INSIGHTS'
        '</div>',
        unsafe_allow_html=True,
    )

    if available:
        insights = []

        if total_moc_pending > 0:
            insights.append(
                f"MOC pending count across loaded departments is {int(total_moc_pending)}."
            )

        if total_interlock_open > 0:
            insights.append(
                f"{int(total_interlock_open)} interlock-open item(s) require review."
            )

        if total_barrier_bad > 0:
            insights.append(
                f"{int(total_barrier_bad)} unacceptable barrier item(s) are recorded."
            )

        if total_pha_delayed > 0:
            insights.append(
                f"{int(total_pha_delayed)} PHA item(s) are delayed."
            )

        if total_audit_delayed > 0:
            insights.append(
                f"{int(total_audit_delayed)} audit item(s) are delayed."
            )

        if total_incidents > 0:
            insights.append(
                f"{int(total_incidents)} Level 1-4 process-safety incident(s) are recorded."
            )

        if not insights:
            insights.append(
                "No open issue count was found in the currently loaded Excel data."
            )

        for item in insights[:6]:
            st.markdown(f"• {item}")

    else:
        st.info("Load department Excel files to generate insights.")

    st.caption(
        "These are rule-based insights from real Excel values, "
        "not fabricated AI predictions."
    )


# ============================================================
# DEPARTMENT DATA TABLE
# ============================================================
st.markdown(
    '<div class="section-title">📋 REAL DATA — ALL LOADED DEPARTMENTS</div>',
    unsafe_allow_html=True,
)

rows = []

for dept in available:
    x = DATA[dept]

    rows.append({
        "Department": dept,
        "File": x["file"],
        "L1": fmt(x["l1"]),
        "L2": fmt(x["l2"]),
        "L3": fmt(x["l3"]),
        "L4": fmt(x["l4"]),
        "Equipment Failure": fmt(x["equipment_failure"]),
        "Barrier Unacceptable": fmt(x["barrier_unacceptable"]),
        "MOC Pending": fmt(x["moc_pending"]),
        "PHA Delayed": fmt(x["pha_delayed"]),
        "Audit Delayed": fmt(x["audit_delayed"]),
        "Interlock Open": fmt(x["interlock_open"]),
        "Open Actions": fmt(x["open_actions"]),
    })

if rows:
    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
        height=260,
    )
else:
    st.warning(
        "No department Excel files found in data/departments."
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div style="
        text-align:center;
        color:#55738b;
        padding:10px;
        font-size:11px;
        font-weight:700;">
        SCREEN 03 • PSM STEERING COMMITTEE •
        REAL DEPARTMENT EXCEL DATA
    </div>
    """,
    unsafe_allow_html=True,
)