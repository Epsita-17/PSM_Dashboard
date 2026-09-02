import math
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# SCREEN 05 - PSM SUB COMMITTEE CHAIRMAN
# REAL DATA ONLY
# ============================================================

st.set_page_config(
    page_title="Screen 05 - PSM Sub Committee Chairman",
    page_icon="🛡️",
    layout="wide",
)

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "departments"

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


# ------------------------------------------------------------
# PAGE STYLE
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #edf4f9;
    }

    .block-container {
        max-width: 100%;
        padding: 0.35rem 0.45rem 0.8rem 0.45rem;
    }

    .dept-label {
        color: #0b3d63;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 0.7px;
        margin: 0 0 2px 2px;
    }

    .header-control {
        background: #ffffff;
        border: 1px solid #b8ccda;
        border-radius: 8px;
        padding: 4px 6px 2px 6px;
        margin-bottom: 5px;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #b8ccda;
        border-radius: 8px;
        padding: 6px;
    }

    .screen-header {
        width: 100%;
        box-sizing: border-box;
        background: linear-gradient(105deg, #031a30, #075d83);
        border: 2px solid #00a7df;
        border-radius: 11px;
        padding: 11px 18px 12px 18px;
        color: white;
        text-align: center;
        margin: 0 0 9px 0;
    }

    .screen-main {
        font-size: 17px;
        font-weight: 900;
        letter-spacing: 0.6px;
    }

    .screen-title {
        color: #ffd21f;
        font-size: 26px;
        font-weight: 900;
        line-height: 1.05;
        margin-top: 3px;
    }

    .screen-sub {
        font-size: 13px;
        font-weight: 700;
        margin-top: 3px;
    }

    .online {
        display: inline-block;
        margin-top: 7px;
        padding: 3px 14px;
        border: 1px solid #25bd61;
        background: #063c20;
        color: #5af28b;
        border-radius: 15px;
        font-size: 10px;
        font-weight: 900;
    }

    .data-ok {
        background: #e6f8ed;
        border: 1px solid #68c58a;
        color: #087333;
        border-radius: 7px;
        padding: 7px 10px;
        font-size: 11px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .data-pending {
        background: #fff6dc;
        border: 1px solid #e1be52;
        color: #765700;
        border-radius: 7px;
        padding: 7px 10px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .section-title {
        background: linear-gradient(90deg, #06466c, #087e9b);
        color: white;
        border-radius: 6px;
        padding: 6px 8px;
        text-align: center;
        font-size: 11px;
        font-weight: 900;
        margin-bottom: 5px;
    }

    .small-note {
        color: #687b89;
        font-size: 9px;
        text-align: center;
        line-height: 1.35;
    }

    .big-pending {
        color: #64727e;
        font-size: 24px;
        font-weight: 900;
        text-align: center;
        padding: 8px 0;
    }

    .focus-row {
        border-bottom: 1px solid #e0e8ed;
        padding: 6px 2px;
        font-size: 10px;
    }

    .assistant {
        background: #f4f9fd;
        border: 1px solid #b9d0df;
        border-radius: 8px;
        padding: 9px;
        font-size: 10px;
        line-height: 1.5;
    }

    .recommend {
        background: #edf9f0;
        border: 1px solid #9ed3ad;
        color: #166534;
        border-radius: 7px;
        padding: 8px;
        margin-top: 7px;
        text-align: center;
        font-size: 10px;
        font-weight: 900;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def number(value):
    """Return a numeric value or None. Never invent a value."""
    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    text = str(value).strip().replace(",", "")
    if text == "":
        return None

    if text.upper() in {
        "NA",
        "N/A",
        "NIL",
        "NONE",
        "-",
        "--",
        "DATA PENDING",
    }:
        return None

    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def display_number(value):
    if value is None:
        return "DATA PENDING"

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.1f}"


def percent(actual, planned):
    if actual is None or planned in (None, 0):
        return None
    return max(0.0, min(100.0, actual / planned * 100.0))


def cell(df, row, col):
    try:
        if row >= len(df.index) or col >= len(df.columns):
            return None
        return number(df.iloc[row, col])
    except Exception:
        return None


def first_existing_file(department):
    if not DATA_DIR.exists():
        return None

    files = list(DATA_DIR.glob("*.xlsx")) + list(DATA_DIR.glob("*.xls"))

    exact = department.lower().strip()

    for file in files:
        if file.stem.lower().strip() == exact:
            return file

    # Your existing file is "Coke Oven.xlsx" but the dashboard
    # displays the department as "Coke Oven-1".
    if department == "Coke Oven-1":
        for file in files:
            if file.stem.lower().strip() == "coke oven":
                return file

    return None


@st.cache_data(show_spinner=False)
def load_department(department):
    file_path = first_existing_file(department)

    if file_path is None:
        return {
            "available": False,
            "file": None,
        }

    try:
        try:
            df = pd.read_excel(
                file_path,
                sheet_name="PSM Dashboard",
                header=None,
            )
        except Exception:
            df = pd.read_excel(
                file_path,
                sheet_name=0,
                header=None,
            )
    except Exception:
        return {
            "available": False,
            "file": file_path.name,
        }

    # Excel template positions:
    # Row 5  -> For the Month
    # Row 6  -> Year till date
    # Row 10 -> For the Month
    # Row 11 -> Year till date
    #
    # pandas is zero-based, therefore the rows are 5, 6, 10, 11.
    month_top = 5
    ytd_top = 6
    month_bottom = 10
    ytd_bottom = 11

    data = {
        "available": True,
        "file": file_path.name,

        # Process Safety Incidents
        "l1": cell(df, month_top, 1),
        "l2": cell(df, month_top, 2),
        "l3": cell(df, month_top, 3),
        "l4": cell(df, month_top, 4),

        # PSM critical equipment
        "equipment_failure": cell(df, month_top, 8),

        # Barrier health
        "barrier_total": cell(df, month_top, 19),
        "barrier_assessed": cell(df, month_top, 20),
        "barrier_unacceptable": cell(df, month_top, 21),

        # Interlock / normalisation
        "interlock_open": cell(df, month_bottom, 22),
        "normalisation_overdue": cell(df, month_bottom, 23),

        # Third-party recommendation
        "third_party_close": cell(df, month_bottom, 1),
        "third_party_delay": cell(df, month_bottom, 2),

        # Process safety incident recommendation
        "incident_rec_close": cell(df, month_bottom, 3),
        "incident_rec_delay": cell(df, month_bottom, 4),

        # RCFA
        "rcfa_overdue": cell(df, month_bottom, 5),

        # PT
        "pt_plan": cell(df, month_bottom, 6),
        "pt_actual": cell(df, month_bottom, 7),

        # PHA
        "pha_plan": cell(df, month_bottom, 8),
        "pha_actual": cell(df, month_bottom, 9),
        "pha_close": cell(df, month_bottom, 10),
        "pha_delay": cell(df, month_bottom, 11),

        # Audit
        "audit_close": cell(df, month_bottom, 12),
        "audit_delay": cell(df, month_bottom, 13),

        # MOC
        "moc_pending": cell(df, month_bottom, 14),
        "moc_kaizen": cell(df, month_bottom, 16),
        "moc_emergency_temp": cell(df, month_bottom, 18),
        "moc_temp_overdue": cell(df, month_bottom, 20),
    }

    data["incident_total"] = sum(
        value or 0
        for value in [
            data["l1"],
            data["l2"],
            data["l3"],
            data["l4"],
        ]
    )

    data["pt_completion"] = percent(
        data["pt_actual"],
        data["pt_plan"],
    )

    data["pha_completion"] = percent(
        data["pha_actual"],
        data["pha_plan"],
    )

    data["barrier_assessment"] = percent(
        data["barrier_assessed"],
        data["barrier_total"],
    )

    data["open_actions"] = sum(
        value or 0
        for value in [
            data["third_party_delay"],
            data["incident_rec_delay"],
            data["rcfa_overdue"],
            data["pha_delay"],
            data["audit_delay"],
            data["moc_pending"],
            data["interlock_open"],
            data["normalisation_overdue"],
        ]
    )

    return data


# ------------------------------------------------------------
# LOAD ALL REAL DEPARTMENT FILES
# ------------------------------------------------------------
all_data = {
    department: load_department(department)
    for department in DEPARTMENTS
}

available_departments = [
    department
    for department in DEPARTMENTS
    if all_data[department]["available"]
]

pending_departments = [
    department
    for department in DEPARTMENTS
    if not all_data[department]["available"]
]

if available_departments:
    default_department = available_departments[0]
else:
    default_department = DEPARTMENTS[0]

# The department selector is deliberately placed inside the header area
# so it does not appear as an isolated control above the dashboard.
selected_department = default_department
d = all_data[selected_department]
now = datetime.now()

# ------------------------------------------------------------
# HEADER — SAME STYLE AS SCREEN 03
# ------------------------------------------------------------
st.markdown(
    """
    <div class="screen-header">
        <div class="screen-main">
            PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        </div>
        <div class="screen-title">
            SCREEN 05 : PSM SUB COMMITTEE CHAIRMAN DASHBOARD
        </div>
        <div class="screen-sub">
            Sub Committee Performance | Implementation Oversight | Escalation Management
        </div>
        <div class="online">
            🟢 PLANT STATUS : ONLINE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# DEPARTMENT FILTER — BELOW HEADER, NOT ABOVE IT
# ------------------------------------------------------------
filter_col, date_col, time_col = st.columns([2.2, 1.2, 1.2], gap="small")

with filter_col:
    selected_department = st.selectbox(
        "Select Department",
        available_departments if available_departments else DEPARTMENTS,
        index=0,
        key="screen05_department",
    )

d = all_data[selected_department]

with date_col:
    st.markdown(
        f"<div class=\"header-control\"><div style=\"font-size:8px;font-weight:900;color:#42627a;\">DATE</div>"
        f"<div style=\"font-size:18px;font-weight:800;color:#183b5b;\">{now.strftime('%d-%b-%Y')}</div></div>",
        unsafe_allow_html=True,
    )

with time_col:
    st.markdown(
        f"<div class=\"header-control\"><div style=\"font-size:8px;font-weight:900;color:#42627a;\">TIME</div>"
        f"<div style=\"font-size:18px;font-weight:800;color:#183b5b;\">{now.strftime('%I:%M:%S %p')}</div></div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# REAL DATA STATUS
# ------------------------------------------------------------
if d["available"]:
    st.markdown(
        f"""
        <div class="data-ok">
            🟢 REAL EXCEL DATA LOADED |
            Selected: {selected_department} |
            Rows/columns read from: {d["file"]} |
            Real Excel files: {len(available_departments)}/{len(DEPARTMENTS)}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.error(
        f"No Excel file was found for {selected_department} "
        "inside data/departments."
    )

if pending_departments:
    st.markdown(
        f"""
        <div class="data-pending">
            🟡 DATA PENDING |
            {len(pending_departments)} department(s) do not have an Excel file.
            No unsupported KPI is being fabricated.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# ROW 1
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns([1.15, 1.45, 1.0, 1.35])

with c1:
    st.markdown(
        '<div class="section-title">1. SUB COMMITTEE OVERALL PERFORMANCE</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge",
            value=0,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#b7c1c9"},
                "steps": [
                    {"range": [0, 70], "color": "#ffd9d9"},
                    {"range": [70, 90], "color": "#fff0bd"},
                    {"range": [90, 100], "color": "#d8f2dc"},
                ],
            },
        )
    )

    fig.update_layout(
        height=190,
        margin=dict(l=8, r=8, t=8, b=0),
        paper_bgcolor="white",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown(
        """
        <div class="big-pending">DATA PENDING</div>
        <div class="small-note">
            A validated PSM pillar score is not contained in the
            selected department Excel file.
        </div>
        <div class="small-note">
            TARGET : ≥ 90%
        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:
    st.markdown(
        '<div class="section-title">2. IMPLEMENTATION PROGRESS — REAL EXCEL DATA</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.metric("PT PLAN", display_number(d["pt_plan"]))

    with b:
        st.metric("PT ACTUAL", display_number(d["pt_actual"]))

    with c:
        pt_text = (
            f'{d["pt_completion"]:.1f}%'
            if d["pt_completion"] is not None
            else "DATA PENDING"
        )
        st.metric("PT COMPLETION", pt_text)

    if d["pt_completion"] is not None:
        st.progress(d["pt_completion"] / 100)

    a, b, c = st.columns(3)

    with a:
        st.metric("PHA PLAN", display_number(d["pha_plan"]))

    with b:
        st.metric("PHA ACTUAL", display_number(d["pha_actual"]))

    with c:
        pha_text = (
            f'{d["pha_completion"]:.1f}%'
            if d["pha_completion"] is not None
            else "DATA PENDING"
        )
        st.metric("PHA COMPLETION", pha_text)

    if d["pha_completion"] is not None:
        st.progress(d["pha_completion"] / 100)

    st.markdown(
        '<div class="small-note">Only Excel plan/actual values are used for these percentages.</div>',
        unsafe_allow_html=True,
    )


with c3:
    st.markdown(
        '<div class="section-title">3. KEY ACTIONS STATUS</div>',
        unsafe_allow_html=True,
    )

    st.metric("OPEN / DELAYED ACTIONS", display_number(d["open_actions"]))
    st.metric("MOC PENDING", display_number(d["moc_pending"]))
    st.metric("PHA DELAYED", display_number(d["pha_delay"]))
    st.metric("AUDIT DELAYED", display_number(d["audit_delay"]))


with c4:
    st.markdown(
        '<div class="section-title">4. OVERDUE / OPEN ACTIONS</div>',
        unsafe_allow_html=True,
    )

    action_rows = [
        ("Third Party Recommendation", d["third_party_delay"]),
        ("Incident Recommendation", d["incident_rec_delay"]),
        ("RCFA", d["rcfa_overdue"]),
        ("PHA", d["pha_delay"]),
        ("Audit", d["audit_delay"]),
        ("MOC", d["moc_pending"]),
        ("Interlock", d["interlock_open"]),
        ("Normalisation", d["normalisation_overdue"]),
    ]

    action_rows = [
        row for row in action_rows
        if row[1] is not None and row[1] > 0
    ]

    action_rows.sort(
        key=lambda row: row[1],
        reverse=True,
    )

    if action_rows:
        action_df = pd.DataFrame(
            [
                {
                    "SR": index + 1,
                    "ACTION / KPI": row[0],
                    "COUNT": int(row[1]),
                }
                for index, row in enumerate(action_rows)
            ]
        )

        st.dataframe(
            action_df,
            use_container_width=True,
            hide_index=True,
            height=220,
        )
    else:
        st.info("No non-zero overdue/open action count is available.")

    st.markdown(
        '<div class="small-note">Owner, due date and ageing are not available in the current Excel template.</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# ROW 2
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="section-title">5. COMPLIANCE STATUS</div>',
        unsafe_allow_html=True,
    )

    compliance_df = pd.DataFrame(
        [
            [
                "PT Completion",
                (
                    f'{d["pt_completion"]:.1f}%'
                    if d["pt_completion"] is not None
                    else "DATA PENDING"
                ),
            ],
            [
                "PHA Completion",
                (
                    f'{d["pha_completion"]:.1f}%'
                    if d["pha_completion"] is not None
                    else "DATA PENDING"
                ),
            ],
            ["Audit Close", display_number(d["audit_close"])],
            ["Audit Delayed", display_number(d["audit_delay"])],
            [
                "Barrier Assessment",
                (
                    f'{d["barrier_assessment"]:.1f}%'
                    if d["barrier_assessment"] is not None
                    else "DATA PENDING"
                ),
            ],
        ],
        columns=["COMPLIANCE ITEM", "VALUE"],
    )

    st.dataframe(
        compliance_df,
        use_container_width=True,
        hide_index=True,
        height=210,
    )


with c2:
    st.markdown(
        '<div class="section-title">6. MOC SUMMARY</div>',
        unsafe_allow_html=True,
    )

    labels = [
        "MOC Pending",
        "Kaizen MOC",
        "Emergency/Temporary MOC",
        "Temporary MOC Overdue",
    ]

    values = [
        d["moc_pending"] or 0,
        d["moc_kaizen"] or 0,
        d["moc_emergency_temp"] or 0,
        d["moc_temp_overdue"] or 0,
    ]

    if sum(values) > 0:
        fig = go.Figure(
            go.Pie(
                labels=labels,
                values=values,
                hole=0.60,
                textinfo="percent",
            )
        )

        fig.update_layout(
            height=210,
            margin=dict(l=0, r=0, t=5, b=0),
            paper_bgcolor="white",
            legend=dict(font=dict(size=8)),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.markdown(
            '<div class="big-pending">DATA PENDING</div>',
            unsafe_allow_html=True,
        )


with c3:
    st.markdown(
        '<div class="section-title">7. INSPECTION & TESTING STATUS</div>',
        unsafe_allow_html=True,
    )

    a, b = st.columns(2)

    with a:
        st.metric("PT PLANNED", display_number(d["pt_plan"]))
        st.metric("PT COMPLETED", display_number(d["pt_actual"]))

    with b:
        st.metric("PHA PLANNED", display_number(d["pha_plan"]))
        st.metric("PHA COMPLETED", display_number(d["pha_actual"]))

    st.markdown(
        f"""
        <div class="small-note">
            PT completion:
            {f'{d["pt_completion"]:.1f}%' if d["pt_completion"] is not None else "DATA PENDING"}
            <br>
            PHA completion:
            {f'{d["pha_completion"]:.1f}%' if d["pha_completion"] is not None else "DATA PENDING"}
        </div>
        """,
        unsafe_allow_html=True,
    )


with c4:
    st.markdown(
        '<div class="section-title">8. TRAINING & COMPETENCY STATUS</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="big-pending">DATA PENDING</div>
        <div class="small-note">
            Training and competency columns are not present in the
            current department Excel template.
            PT/PHA values are NOT reused as training data.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# ROW 3
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="section-title">9. INCIDENTS & NEAR MISSES</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.metric("L1-L4 INCIDENTS", display_number(d["incident_total"]))

    with b:
        st.metric(
            "EQUIPMENT FAILURE",
            display_number(d["equipment_failure"]),
        )

    with c:
        st.metric(
            "UNACCEPTABLE BARRIERS",
            display_number(d["barrier_unacceptable"]),
        )

    fig = go.Figure(
        go.Bar(
            x=["Level 1", "Level 2", "Level 3", "Level 4"],
            y=[
                d["l1"] or 0,
                d["l2"] or 0,
                d["l3"] or 0,
                d["l4"] or 0,
            ],
        )
    )

    fig.update_layout(
        height=145,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


with c2:
    st.markdown(
        '<div class="section-title">10. DOCUMENTS & RECORDS STATUS</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="big-pending">DATA PENDING</div>
        <div class="small-note">
            Document and records register is not present in the
            selected department Excel file.
        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:
    st.markdown(
        '<div class="section-title">11. COMMUNICATION & MEETINGS</div>',
        unsafe_allow_html=True,
    )

    meeting_df = pd.DataFrame(
        [
            ["Meetings Conducted", "DATA PENDING"],
            ["Attendance", "DATA PENDING"],
            ["MOM Closed", "DATA PENDING"],
            ["Open MOMs", "DATA PENDING"],
            ["Communication Issued", "DATA PENDING"],
        ],
        columns=["KPI", "VALUE"],
    )

    st.dataframe(
        meeting_df,
        use_container_width=True,
        hide_index=True,
        height=210,
    )


with c4:
    st.markdown(
        '<div class="section-title">12. MY FOCUS AREAS</div>',
        unsafe_allow_html=True,
    )

    focus_items = [
        ("MOC Pending", d["moc_pending"]),
        ("PHA Delayed", d["pha_delay"]),
        ("Audit Delayed", d["audit_delay"]),
        ("Interlock Open", d["interlock_open"]),
        ("Normalisation Overdue", d["normalisation_overdue"]),
        ("Unacceptable Barriers", d["barrier_unacceptable"]),
    ]

    for label, value in focus_items:
        if value is None:
            status = "DATA PENDING"
        elif value > 0:
            status = f"ATTENTION • {display_number(value)}"
        else:
            status = "ON TRACK • 0"

        st.markdown(
            f"""
            <div class="focus-row">
                <b>• {label}</b><br>
                <span style="color:#63798a">{status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# ROW 4
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="section-title">13. AI CHAIRMAN ASSISTANT</div>',
        unsafe_allow_html=True,
    )

    insights = []

    for label, key in [
        ("MOC pending", "moc_pending"),
        ("PHA delayed", "pha_delay"),
        ("Audit delayed", "audit_delay"),
        ("Interlock open", "interlock_open"),
        ("Normalisation overdue", "normalisation_overdue"),
        ("Unacceptable barriers", "barrier_unacceptable"),
    ]:
        value = d[key]

        if value is not None and value > 0:
            insights.append(
                f"{label}: {display_number(value)}"
            )

    if not insights:
        insights.append(
            "No non-zero action count is available in the selected Excel file."
        )

    st.markdown(
        '<div class="assistant">'
        + "<br>".join(f"• {item}" for item in insights[:6])
        + "</div>"
        '<div class="recommend">'
        "Prioritize all non-zero delayed/open KPIs during management review."
        "</div>",
        unsafe_allow_html=True,
    )


with c2:
    st.markdown(
        '<div class="section-title">14. SELECTED DEPARTMENT SNAPSHOT</div>',
        unsafe_allow_html=True,
    )

    st.metric("DEPARTMENT", selected_department)
    st.metric("INCIDENTS L1-L4", display_number(d["incident_total"]))
    st.metric(
        "EQUIPMENT FAILURE",
        display_number(d["equipment_failure"]),
    )
    st.metric("OPEN ACTIONS", display_number(d["open_actions"]))


with c3:
    st.markdown(
        '<div class="section-title">15. ACTION DELAY DISTRIBUTION</div>',
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        go.Bar(
            x=[
                "Third Party",
                "Incident",
                "RCFA",
                "PHA",
                "Audit",
                "MOC",
            ],
            y=[
                d["third_party_delay"] or 0,
                d["incident_rec_delay"] or 0,
                d["rcfa_overdue"] or 0,
                d["pha_delay"] or 0,
                d["audit_delay"] or 0,
                d["moc_pending"] or 0,
            ],
        )
    )

    fig.update_layout(
        height=210,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


with c4:
    st.markdown(
        '<div class="section-title">16. DATA SOURCE STATUS</div>',
        unsafe_allow_html=True,
    )

    st.metric(
        "EXCEL FILES LOADED",
        f"{len(available_departments)}/{len(DEPARTMENTS)}",
    )

    st.metric(
        "PENDING DEPARTMENTS",
        len(pending_departments),
    )

    st.markdown(
        f"""
        <div class="small-note">
            Selected Excel file:<br>
            <b>{d.get("file") or "Not available"}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# REAL DATA TABLE
# ------------------------------------------------------------
st.markdown(
    '<div class="section-title">REAL DATA — LOADED DEPARTMENT SUMMARY</div>',
    unsafe_allow_html=True,
)

summary_rows = []

for department in available_departments:
    item = all_data[department]

    summary_rows.append(
        {
            "Department": department,
            "Excel File": item["file"],
            "L1": display_number(item["l1"]),
            "L2": display_number(item["l2"]),
            "L3": display_number(item["l3"]),
            "L4": display_number(item["l4"]),
            "Equipment Failure": display_number(
                item["equipment_failure"]
            ),
            "Unacceptable Barrier": display_number(
                item["barrier_unacceptable"]
            ),
            "MOC Pending": display_number(
                item["moc_pending"]
            ),
            "PHA Delayed": display_number(
                item["pha_delay"]
            ),
            "Audit Delayed": display_number(
                item["audit_delay"]
            ),
            "Interlock Open": display_number(
                item["interlock_open"]
            ),
            "Open Actions": display_number(
                item["open_actions"]
            ),
        }
    )

if summary_rows:
    st.dataframe(
        pd.DataFrame(summary_rows),
        use_container_width=True,
        hide_index=True,
        height=250,
    )
else:
    st.warning(
        "No department Excel files were found in data/departments."
    )


st.caption(
    "SCREEN 05 • PSM SUB COMMITTEE CHAIRMAN • "
    "REAL EXCEL DATA ONLY • UNSUPPORTED VALUES ARE NOT FABRICATED"
)