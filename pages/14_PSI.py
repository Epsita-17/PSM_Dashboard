import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Process Safety Incident Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GOOGLE SHEET
# =========================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

# CHANGED: PSSR -> PSI
PSI_SHEET_NAME = "PSI"

PSI_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={PSI_SHEET_NAME}"
)


@st.cache_data(ttl=60)
def get_psi_data():
    try:

        data = pd.read_csv(PSI_CSV_URL)

        data.columns = (
            data.columns
            .astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.strip()
        )

        for col in data.columns:

            if data[col].dtype == "object":
                data[col] = (
                    data[col]
                    .astype(str)
                    .str.replace(
                        "\xa0",
                        " ",
                        regex=False
                    )
                    .str.strip()
                )

        return data.replace({
            "nan": "",
            "NaN": "",
            "NAN": ""
        })

    except Exception as exc:

        st.error(
            f"Unable to load Google Sheet "
            f"'{PSI_SHEET_NAME}': {exc}"
        )

        return pd.DataFrame()


df = get_psi_data()

if df.empty:
    st.error(
        f"No data found in Google Sheet "
        f"tab '{PSI_SHEET_NAME}'."
    )

    st.stop()

# =========================================================
# COLUMN MAPPING - PSI SHEET
# =========================================================
COL = {

    "sr_no": "Sr No",
    "department": "Department",
    "section": "Section",
    "description": "Incident Description",
    "incident_date": "Incident Date",
    "classification": "Incident Classification",
    "level": "Incident Level"

}

missing = [

    key

    for key, column in COL.items()

    if column not in df.columns

]

if missing:
    st.error(
        "Required PSI columns are missing: "
        + ", ".join(
            COL[key]
            for key in missing
        )
    )

    st.write(
        "Columns found in the PSI sheet:"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()

# =========================================================
# DATA PREPARATION
# =========================================================
work = df.copy()

# CHANGED: Incident Date is now the dashboard date
work["_due_date"] = pd.to_datetime(
    work[COL["incident_date"]],
    errors="coerce",
    dayfirst=True
)

work["_completion_date"] = pd.NaT

work["_department"] = (
    work[COL["department"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_section"] = (
    work[COL["section"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_description"] = (
    work[COL["description"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =========================================================
# PSI CLASSIFICATION
# =========================================================
work["_classification_raw"] = (
    work[COL["classification"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =========================================================
# PSI LEVEL
# =========================================================
work["_level_raw"] = (
    work[COL["level"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# ---------------------------------------------------------
# Kept for compatibility with the existing KPI section.
# PSI sheet has no separate status column.
# ---------------------------------------------------------
work["_status_raw"] = ""


def normalize_psi_status(value):
    value = str(value).strip().lower()

    if "completed" in value:
        return "Completed"

    if "overdue" in value:
        return "Overdue"

    if "pending" in value:
        return "Pending"

    return "Pending"


work["_status_display"] = (
    work["_status_raw"]
    .apply(normalize_psi_status)
)

# CHANGED: trend uses Incident Date
work["_trend_date"] = work["_due_date"]

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(
    """
<style>

#MainMenu,
header,
footer,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display:none !important;
}


html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {

    margin:0 !important;
    padding:0 !important;
    overflow:hidden !important;
}


[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {

    width:100% !important;
    max-width:none !important;
    margin:0 !important;
    padding:0 3px !important;
}


[data-testid="stAppViewContainer"] > .main > div {
    padding:0 !important;
}


.stApp {

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f7fbfe 48%,
            #eef5f9 100%
        ) !important;

    color:#17324d !important;
}


[data-testid="stVerticalBlock"] {
    gap:0 !important;
}


[data-testid="stHorizontalBlock"] {
    gap:5px !important;
}


/* =========================================================
   FILTERS
   ========================================================= */

.filter-title {

    color:#173b5c;

    font-size:12px;

    font-weight:900;

    letter-spacing:.4px;

    margin:0 0 0 3px;
}


div[data-baseweb="select"] > div {

    height:30px !important;

    min-height:30px !important;

    border-radius:7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f4f8fb
        ) !important;

    border:1px solid #b8d5e8 !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 2px 6px rgba(22,72,110,.08) !important;
}


div[data-baseweb="select"] * {

    color:#23445f !important;

    font-size:11px !important;
}


div[data-baseweb="select"] svg {
    fill:#176da0 !important;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi-card {

    position:relative;

    height:108px;

    overflow:hidden;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f8fbfd 58%,
            #edf5f9 100%
        );

    border:1px solid #c5dce9;

    border-top:4px solid #159ee4;

    border-radius:10px;

    padding:14px 16px;

    box-shadow:
        0 4px 12px rgba(28,78,110,.12),
        0 1px 2px rgba(28,78,110,.08),
        inset 0 1px 0 rgba(255,255,255,.95);
}


.kpi-card.completed {
    border-top-color:#18a957;
}


.kpi-card.pending,
.kpi-card.compliance {
    border-top-color:#d9272e;
}


.kpi-icon {

    position:absolute;

    left:17px;

    top:18px;

    width:54px;

    height:54px;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

    color:#123f7a;

    background:#ffffff;

    border:3px solid #123f7a;

    font-size:29px;

    font-weight:900;
}


.kpi-card.completed .kpi-icon {

    color:#149c53;

    border-color:#149c53;
}


.kpi-card.pending .kpi-icon,
.kpi-card.compliance .kpi-icon {

    color:#d9272e;

    border-color:#d9272e;
}


.kpi-content {
    margin-left:70px;
}


.kpi-label {

    color:#087bc1;

    font-size:11px;

    font-weight:950;

    letter-spacing:.45px;

    line-height:1.1;

    margin-top:1px;
}


.kpi-card.completed .kpi-label {
    color:#11984e;
}


.kpi-card.pending .kpi-label,
.kpi-card.compliance .kpi-label {
    color:#c9232b;
}


.kpi-value {

    font-size:37px;

    line-height:1;

    font-weight:950;

    margin-top:8px;

    color:#173b5a;
}


.kpi-value.green {
    color:#149c53;
}


.kpi-value.red {
    color:#d9272e;
}


.kpi-value.blue {
    color:#164b91;
}


.kpi-description {

    color:#5c7181;

    font-size:12px;

    margin-top:7px;

    line-height:1.1;
}


/* =========================================================
   PANELS
   ========================================================= */

.panel {

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f6fafc
        );

    border:1px solid #c5dce9;

    border-radius:9px;

    box-shadow:
        0 4px 12px rgba(28,78,110,.10);

    overflow:hidden;
}


.panel-title {

    height:25px;

    display:flex;

    align-items:center;

    padding:0 13px;

    color:#163b5b;

    font-size:11px;

    font-weight:950;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #eef6fa
        );

    border-bottom:2px solid #158fd0;
}


.chart-box {

    margin:6px 7px 7px 7px;

    padding:2px 5px 0 5px;

    background:#ffffff;

    border:1px solid #e2eaf0;

    border-radius:7px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 1px 3px rgba(28,78,110,.06);

    overflow:hidden;
}


/* =========================================================
   LEVEL CARDS
   ========================================================= */

.level-card {

    height:100px;

    border:1px solid #c5dce9;

    border-radius:9px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f7fafc
        );

    box-shadow:
        0 3px 9px rgba(28,78,110,.08);

    text-align:center;

    padding-top:12px;
}


.level-title {

    font-size:12px;

    font-weight:950;

    letter-spacing:.4px;
}


.level-value {

    font-size:30px;

    line-height:1;

    font-weight:950;

    margin-top:7px;
}


.level-pct {

    color:#263c52;

    font-size:14px;

    margin-top:7px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    height:18px;

    display:flex;

    align-items:center;

    justify-content:center;

    color:#587084;

    background:
        linear-gradient(
            180deg,
            #f8fbfd,
            #eaf2f6
        );

    font-size:11px;

    font-weight:800;

    border-top:1px solid #c8dce8;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
header_html = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing:border-box;
}


html,
body {

    margin:0;

    padding:0;

    width:100%;

    height:100%;

    overflow:hidden;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


body {
    background:#f4f9fc;
}


.header {

    position:relative;

    width:100%;

    height:72px;

    overflow:hidden;

    display:flex;

    align-items:center;

    justify-content:center;

    background:

        radial-gradient(
            ellipse at center,
            rgba(55,160,218,.24) 0%,
            rgba(223,242,252,.82) 45%,
            rgba(244,250,253,.98) 100%
        ),

        linear-gradient(
            180deg,
            #edf8fd 0%,
            #dceff8 100%
        );

    border-top:2px solid #0b91d1;

    border-bottom:3px solid #1487c2;

    box-shadow:
        0 4px 12px rgba(21,92,130,.18);
}


.header::before {

    content:"";

    position:absolute;

    inset:0;

    background-image:

        radial-gradient(
            circle,
            rgba(0,122,190,.17) 1.2px,
            transparent 1.5px
        );

    background-size:15px 15px;

    opacity:.65;
}


.header::after {

    content:"";

    position:absolute;

    inset:0;

    background:

        linear-gradient(
            135deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        ),

        linear-gradient(
            315deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        );
}


.industrial {

    position:absolute;

    left:0;

    right:0;

    bottom:0;

    width:100%;

    height:72px;

    opacity:.38;

    z-index:1;
}


.industrial .steel {

    fill:#a8c9da;

    stroke:#5791af;

    stroke-width:1.5;
}


.industrial .light {

    fill:none;

    stroke:#2e8bb9;

    stroke-width:1.2;

    opacity:.70;
}


.industrial .window {

    fill:#2787b5;

    opacity:.65;
}


.hex {

    fill:none;

    stroke:#278abd;

    stroke-width:1;

    opacity:.28;
}


.content {

    position:relative;

    z-index:8;

    width:100%;

    height:100%;

    display:flex;

    align-items:center;

    justify-content:center;
}


.pillar {

    position:relative;

    width:840px;

    height:48px;

    display:flex;

    align-items:center;

    justify-content:center;

    background:

        linear-gradient(
            180deg,
            #197fbd 0%,
            #07538d 48%,
            #032f5b 100%
        );

    border:1px solid #0877ba;

    border-radius:14px;

    color:#ffd21a;

    font-size:32px;

    font-weight:950;

    letter-spacing:1px;

    white-space:nowrap;

    box-shadow:

        0 7px 16px rgba(11,83,130,.30),

        inset 0 1px 0 rgba(255,255,255,.32),

        inset 0 -5px 12px rgba(0,35,75,.18);
}


.pillar::before,
.pillar::after {

    position:absolute;

    top:50%;

    transform:translateY(-50%);

    color:#51c5ff;

    font-size:20px;

    font-weight:950;

    letter-spacing:-5px;
}


.pillar::before {

    content:"◀◀";

    left:17px;
}


.pillar::after {

    content:"▶▶";

    right:17px;
}


.top-line {

    position:absolute;

    top:0;

    left:24%;

    width:52%;

    height:3px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00a9ff 18%,
            #ffffff 50%,
            #00a9ff 82%,
            transparent
        );
}


.scan {

    position:absolute;

    z-index:12;

    bottom:0;

    left:-16%;

    width:16%;

    height:4px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00b5ff,
            #ffffff,
            #00b5ff,
            transparent
        );

    animation:
        scanline 3s linear infinite;
}


@keyframes scanline {

    0% {
        left:-16%;
    }

    100% {
        left:100%;
    }
}


.corner-light {

    position:absolute;

    z-index:10;

    width:110px;

    height:3px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00baff,
            transparent
        );
}


.corner-left {

    left:7%;

    top:7px;
}


.corner-right {

    right:7%;

    top:7px;
}

</style>

</head>


<body>

<div class="header">

    <div class="top-line"></div>

    <div class="corner-light corner-left"></div>

    <div class="corner-light corner-right"></div>


    <svg
        class="industrial"
        viewBox="0 0 1672 145"
        preserveAspectRatio="none"
        aria-hidden="true"
    >

        <g>

            <rect
                class="steel"
                x="85"
                y="24"
                width="34"
                height="116"
                rx="4"
            />

            <rect
                class="steel"
                x="91"
                y="9"
                width="22"
                height="18"
            />

            <rect
                class="steel"
                x="96"
                y="0"
                width="12"
                height="12"
            />

            <path
                class="light"
                d="
                    M102 0 L102 140
                    M87 55 L117 55
                    M87 78 L117 78
                    M87 103 L117 103
                "
            />

            <circle
                class="window"
                cx="102"
                cy="43"
                r="3"
            />

            <circle
                class="window"
                cx="102"
                cy="67"
                r="3"
            />

            <circle
                class="window"
                cx="102"
                cy="91"
                r="3"
            />

        </g>


        <g>

            <rect
                class="steel"
                x="150"
                y="52"
                width="17"
                height="88"
            />

            <rect
                class="steel"
                x="146"
                y="48"
                width="25"
                height="8"
            />

            <path
                class="light"
                d="M158 52 L158 140"
            />

        </g>


        <g class="light">

            <path d="M55 113 H245 V85 H320"/>

            <path d="M120 125 H260 V105 H355"/>

            <path d="M180 96 H285 V65 H340"/>

            <path d="M215 130 V70 H280"/>

        </g>


        <g>

            <rect
                class="steel"
                x="260"
                y="64"
                width="58"
                height="76"
                rx="26"
            />

            <path
                class="light"
                d="M260 82 H318 M260 107 H318"
            />

            <circle
                class="window"
                cx="289"
                cy="95"
                r="4"
            />

        </g>


        <g>

            <rect
                class="steel"
                x="1512"
                y="25"
                width="36"
                height="115"
                rx="4"
            />

            <rect
                class="steel"
                x="1518"
                y="9"
                width="24"
                height="18"
            />

            <rect
                class="steel"
                x="1523"
                y="0"
                width="14"
                height="12"
            />

            <path
                class="light"
                d="
                    M1530 0 L1530 140
                    M1514 54 L1546 54
                    M1514 79 L1546 79
                    M1514 103 L1546 103
                "
            />

            <circle
                class="window"
                cx="1530"
                cy="42"
                r="3"
            />

            <circle
                class="window"
                cx="1530"
                cy="66"
                r="3"
            />

            <circle
                class="window"
                cx="1530"
                cy="90"
                r="3"
            />

        </g>


        <g>

            <rect
                class="steel"
                x="1450"
                y="54"
                width="18"
                height="86"
            />

            <rect
                class="steel"
                x="1446"
                y="49"
                width="26"
                height="8"
            />

            <path
                class="light"
                d="M1459 54 L1459 140"
            />

        </g>


        <g class="light">

            <path d="M1620 112 H1425 V85 H1350"/>

            <path d="M1575 125 H1410 V104 H1330"/>

            <path d="M1500 95 H1390 V65 H1335"/>

            <path d="M1465 130 V70 H1390"/>

        </g>


        <g>

            <rect
                class="steel"
                x="1350"
                y="64"
                width="58"
                height="76"
                rx="26"
            />

            <path
                class="light"
                d="M1350 82 H1408 M1350 107 H1408"
            />

            <circle
                class="window"
                cx="1379"
                cy="95"
                r="4"
            />

        </g>


        <g class="light">

            <path d="M0 137 H1672"/>

            <path d="M0 126 H420 V116 H650"/>

            <path d="M1672 126 H1250 V116 H1020"/>

        </g>


        <g class="hex">

            <path
                d="
                    M250 25
                    l18 -11
                    l18 11
                    v22
                    l-18 11
                    l-18-11
                    z
                "
            />

            <path
                d="
                    M282 54
                    l18 -11
                    l18 11
                    v22
                    l-18 11
                    l-18-11
                    z
                "
            />

            <path
                d="
                    M1335 25
                    l18 -11
                    l18 11
                    v22
                    l-18 11
                    l-18-11
                    z
                "
            />

            <path
                d="
                    M1370 54
                    l18 -11
                    l18 11
                    v22
                    l-18 11
                    l-18-11
                    z
                "
            />

        </g>

    </svg>


    <div class="content">

        <div class="pillar">
            PILLAR: PROCESS SAFETY INCIDENT
        </div>

    </div>


    <div class="scan"></div>

</div>

</body>

</html>
"""

components.html(
    header_html,
    height=78,
    scrolling=False
)

# =========================================================
# FILTERS
# =========================================================
filter_month, filter_department = st.columns(
    [1.0, 1.0],
    gap="small"
)

with filter_month:
    st.markdown(
        "<div class='filter-title'>MONTH</div>",
        unsafe_allow_html=True
    )

    valid_dates = (
        work["_trend_date"]
        .dropna()
    )

    month_values = (

        valid_dates
        .dt
        .to_period("M")
        .drop_duplicates()
        .sort_values(
            ascending=False
        )

        if not valid_dates.empty

        else pd.Series(
            [],
            dtype="period[M]"
        )

    )

    month_labels = [

        p.strftime("%B %Y")

        for p in month_values

    ]

    month_options = [
                        "All Months"
                    ] + month_labels

    selected_month = st.selectbox(

        "Month",

        month_options,

        index=0,

        label_visibility="collapsed",

        key="psi_month"

    )

with filter_department:
    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )

    department_options = [

                             "All Departments"

                         ] + sorted(

        [

            x

            for x in
            work["_department"]
            .unique()
            .tolist()

            if x and
               x.lower() != "nan"

        ],

        key=lambda x: x.lower()

    )

    selected_department = st.selectbox(

        "Department",

        department_options,

        index=0,

        label_visibility="collapsed",

        key="psi_department"

    )

# =========================================================
# APPLY FILTERS
# =========================================================
filtered_df = work.copy()

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["_department"]
        == selected_department
        ]

if selected_month != "All Months":
    selected_period = pd.Period(

        pd.to_datetime(
            selected_month,
            format="%B %Y"
        ),

        freq="M"

    )

    filtered_df = filtered_df[

        filtered_df["_trend_date"]
        .dt
        .to_period("M")
        == selected_period

        ]

trend_df = work.copy()

if selected_department != "All Departments":
    trend_df = trend_df[
        trend_df["_department"]
        == selected_department
        ]

# =========================================================
# KPI CALCULATIONS
# =========================================================
total_pssr = len(filtered_df)

completed = int(

    (
            filtered_df["_status_display"]
            == "Completed"
    ).sum()

)

pending = int(

    (
            filtered_df["_status_display"]
            == "Pending"
    ).sum()

)

overdue = int(

    (
            filtered_df["_status_display"]
            == "Overdue"
    ).sum()

)

pending_overdue = pending + overdue

compliance = (

    completed
    / total_pssr
    * 100

    if total_pssr

    else 0

)

# =========================================================
# ROW 1 KPI CARDS
# =========================================================
k1, k2, k3, k4, k5 = st.columns(
    [1, 1, 1, 1, 1],
    gap="small"
)

with k1:
    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                ▣
            </div>

            <div class="kpi-content">

                <div class="kpi-label">
                    TOTAL INCIDENTS
                </div>

                <div class="kpi-value blue">
                    {total_pssr}
                </div>

                <div class="kpi-description">
                    100% of total
                </div>

            </div>

        </div>
        """

    )

with k2:
    completed_pct = (

        completed
        / total_pssr
        * 100

        if total_pssr

        else 0

    )

    st.html(

        f"""
        <div class="kpi-card completed">

            <div class="kpi-icon">
                ✓
            </div>

            <div class="kpi-content">

                <div class="kpi-label">
                    INVESTIGATION COMPLETED
                </div>

                <div class="kpi-value green">
                    {completed}
                </div>

                <div class="kpi-description">
                    {completed_pct:.1f}% completed
                </div>

            </div>

        </div>
        """

    )

with k3:
    pending_pct = (

        pending_overdue
        / total_pssr
        * 100

        if total_pssr

        else 0

    )

    st.html(

        f"""
        <div class="kpi-card pending">

            <div class="kpi-icon">
                ◷
            </div>

            <div class="kpi-content">

                <div class="kpi-label">
                    INVESTIGATION PENDING
                </div>

                <div class="kpi-value red">
                    {pending_overdue}
                </div>

                <div class="kpi-description">
                    {pending_pct:.1f}% of total
                </div>

            </div>

        </div>
        """

    )

with k4:
    st.html(

        f"""
        <div class="kpi-card compliance">

            <div class="kpi-icon">
                ◔
            </div>

            <div class="kpi-content">

                <div class="kpi-label">
                    COMPLIANCE
                </div>

                <div class="kpi-value red">
                    {compliance:.1f}%
                </div>

                <div class="kpi-description">
                    Completed %
                </div>

            </div>

        </div>
        """

    )

with k5:
    status_total = (
        total_pssr
        if total_pssr
        else 1
    )

    completed_pct_status = (

            completed
            / status_total
            * 100

    )

    st.html(

        f"""
        <div
            class="kpi-card compliance"
            style="height:108px;"
        >

            <div
                class="kpi-content"
                style="margin-left:0;"
            >

                <div class="kpi-label">
                    INVESTIGATION STATUS
                </div>

                <div
                    style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                        margin-top:7px;
                    "
                >

                    <div
                        style="
                            width:54px;
                            height:54px;
                            border-radius:50%;

                            background:
                            conic-gradient(
                                #149c53
                                0 {completed_pct_status}%,

                                #d9272e
                                {completed_pct_status}% 100%
                            );

                            position:relative;

                            flex:0 0 54px;
                        "
                    >

                        <div
                            style="
                                position:absolute;

                                left:8px;
                                top:8px;

                                width:38px;
                                height:38px;

                                border-radius:50%;

                                background:#ffffff;

                                display:flex;

                                align-items:center;

                                justify-content:center;

                                color:#17324d;

                                font-size:13px;

                                font-weight:950;
                            "
                        >
                            {total_pssr}
                        </div>

                    </div>


                    <div
                        style="
                            font-size:10px;

                            line-height:1.55;

                            color:#263f53;

                            font-weight:800;
                        "
                    >

                        <span style="color:#149c53;">
                            ● Completed {completed}
                        </span>

                        <br>

                        <span style="color:#d9272e;">
                            ● Pending/Overdue {pending_overdue}
                        </span>

                    </div>

                </div>

            </div>

        </div>
        """

    )

# =========================================================
# MAIN CHART ROW
# =========================================================
c1, c2, c3 = st.columns(
    [1.05, 1.05, .72],
    gap="small"
)

# =========================================================
# INCIDENTS BY DEPARTMENTS
# =========================================================
with c1:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENTS BY DEPARTMENTS
            </div>

            <div class="chart-box">
        """

    )

    dept = (

        filtered_df["_department"]

        .replace(
            "",
            "Not Specified"
        )

        .value_counts()

        .sort_values(
            ascending=False
        )

    )

    fig_dept = go.Figure()

    fig_dept.add_trace(

        go.Bar(

            x=dept.index.tolist(),

            y=dept.values.tolist(),

            text=dept.values.tolist(),

            textposition="outside",

            marker=dict(

                color="#123f7a",

                line=dict(

                    color="#0a2d5a",

                    width=1

                )

            ),

            hovertemplate=(

                "%{x}<br>"
                "Incidents: %{y}"
                "<extra></extra>"

            )

        )

    )

    fig_dept.update_layout(

        height=185,

        margin=dict(

            l=40,

            r=10,

            t=10,

            b=42

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        yaxis=dict(

            title="No. of Incidents",

            dtick=1,

            gridcolor="#e4edf3",

            zeroline=False,

            tickfont=dict(
                size=9
            ),

            title_font=dict(
                size=10
            )

        ),

        xaxis=dict(

            title="Department",

            tickfont=dict(
                size=9
            ),

            title_font=dict(
                size=10
            ),

            showgrid=False

        )

    )

    st.plotly_chart(

        fig_dept,

        use_container_width=True,

        config={
            "displayModeBar": False
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# INCIDENTS MONTH-WISE TREND
# =========================================================
with c2:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENTS MONTH-WISE TREND
            </div>

            <div class="chart-box">
        """

    )

    trend_source = (

        trend_df

        .dropna(
            subset=["_trend_date"]
        )

        .copy()

    )

    if not trend_source.empty:

        trend_source["_month"] = (

            trend_source["_trend_date"]

            .dt
            .to_period("M")

        )

        trend = (

            trend_source

            .groupby("_month")

            .size()

            .sort_index()

        )

        trend_labels = [

            p.strftime("%b %y")

            for p in trend.index

        ]

        trend_values = (
            trend.values.tolist()
        )


    else:

        trend_labels = []

        trend_values = []

    fig_trend = go.Figure()

    fig_trend.add_trace(

        go.Scatter(

            x=trend_labels,

            y=trend_values,

            mode="lines+markers+text",

            text=trend_values,

            textposition="top center",

            line=dict(

                color="#123f7a",

                width=2

            ),

            marker=dict(

                size=7,

                color="#123f7a",

                line=dict(

                    color="#ffffff",

                    width=1.5

                )

            ),

            hovertemplate=(

                "%{x}<br>"
                "Incidents: %{y}"
                "<extra></extra>"

            )

        )

    )

    fig_trend.update_layout(

        height=185,

        margin=dict(

            l=35,

            r=10,

            t=10,

            b=35

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        yaxis=dict(

            title="No. of Incidents",

            dtick=1,

            gridcolor="#e4edf3",

            zeroline=False,

            tickfont=dict(
                size=9
            ),

            title_font=dict(
                size=10
            )

        ),

        xaxis=dict(

            tickfont=dict(
                size=9
            ),

            showgrid=False

        )

    )

    st.plotly_chart(

        fig_trend,

        use_container_width=True,

        config={
            "displayModeBar": False
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# INCIDENT CLASSIFICATION
# =========================================================
with c3:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENT CLASSIFICATION
            </div>

            <div class="chart-box">
        """

    )

    classification_labels = [

        "Near-Miss",

        "Process Safety Incident",

        "Serious Process Safety Incident"

    ]

    classification_values = [

        14,
        7,
        3

    ]

    labels_plot = (
        classification_labels[::-1]
    )

    values_plot = (
        classification_values[::-1]
    )

    fig_incident_classification = go.Figure()

    # =====================================================
    # BAR GRAPH
    # THIS IS KEPT UNCHANGED
    # =====================================================
    fig_incident_classification.add_trace(

        go.Bar(

            x=values_plot,

            y=labels_plot,

            orientation="h",

            text=values_plot,

            textposition="outside",

            cliponaxis=False,

            marker=dict(

                color="#123f7a",

                line=dict(

                    color="#0a2d5a",

                    width=1

                )

            ),

            hovertemplate=(

                "%{y}<br>"
                "No. of Incidents: %{x}"
                "<extra></extra>"

            )

        )

    )

    classification_annotations = [

        dict(

            x=-1.30,

            y=2,

            xref="paper",

            yref="y",

            text="Near-Miss",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        ),

        dict(

            x=-1.30,

            y=1,

            xref="paper",

            yref="y",

            text="Process Safety Incident",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        ),

        dict(

            x=-1.30,

            y=0,

            xref="paper",

            yref="y",

            text="Serious Process Safety Incident",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        )

    ]

    fig_incident_classification.update_layout(

        height=185,

        margin=dict(

            l=180,

            r=25,

            t=8,

            b=42

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial, sans-serif",

            size=10,

            color="#213c55"

        ),

        xaxis=dict(

            title="No. of Incidents",

            range=[0, 16],

            tickmode="array",

            tickvals=[

                0,
                5,
                10,
                15

            ],

            ticktext=[

                "0",
                "5",
                "10",
                "15"

            ],

            gridcolor="#e4edf3",

            gridwidth=1,

            zeroline=False,

            showline=False,

            tickfont=dict(

                size=9,

                color="#536a7b"

            ),

            title_font=dict(

                size=10,

                color="#17324d"

            )

        ),

        yaxis=dict(

            showticklabels=False,

            showgrid=False,

            zeroline=False,

            showline=False,

            range=[-0.5, 2.5]

        ),

        annotations=classification_annotations,

        showlegend=False,

        bargap=.48

    )

    st.plotly_chart(

        fig_incident_classification,

        use_container_width=True,

        config={

            "displayModeBar": False,

            "responsive": True

        }

    )

    st.html(

        """
            </div>
        </div>
        """

    )

# =========================================================
# THIRD ROW
# =========================================================
r3_left, r3_right = st.columns(

    [1.05, 2.00],

    gap="small"

)

# =========================================================
# INCIDENT LEVEL DISTRIBUTION
# =========================================================
with r3_left:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENT LEVEL DISTRIBUTION
            </div>

            <div class="chart-box">
        """

    )

    level_labels = [

        "Level 1",
        "Level 2",
        "Level 3",
        "Level 4"

    ]

    level_values = [

        6,
        8,
        5,
        5

    ]

    level_total = sum(
        level_values
    )

    fig_level = go.Figure(

        data=[

            go.Pie(

                labels=level_labels,

                values=level_values,

                hole=.58,

                sort=False,

                direction="clockwise",

                textinfo="none",

                domain=dict(

                    x=[
                        0.00,
                        0.58
                    ],

                    y=[
                        0.02,
                        0.98
                    ]

                ),

                marker=dict(

                    colors=[

                        "#18a957",
                        "#2455a4",
                        "#f4bd27",
                        "#d9272e"

                    ],

                    line=dict(

                        color="#ffffff",

                        width=2

                    )

                ),

                hovertemplate=(

                    "%{label}: %{value}"

                    "<extra></extra>"

                )

            )

        ]

    )

    fig_level.update_layout(

        height=150,

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        showlegend=True,

        legend=dict(

            orientation="v",

            x=0.62,

            y=0.50,

            xanchor="left",

            yanchor="middle",

            font=dict(

                family="Arial, sans-serif",

                size=10,

                color="#31485d"

            ),

            bgcolor="rgba(255,255,255,0)",

            traceorder="normal",

            itemsizing="constant"

        ),

        annotations=[

            dict(

                text=(

                    f"<b>{level_total}</b>"

                    "<br>"

                    "<span "
                    "style='font-size:9px'>"
                    "TOTAL"
                    "</span>"

                ),

                x=0.25,

                y=0.50,

                xref="paper",

                yref="paper",

                showarrow=False,

                align="center",

                font=dict(

                    family="Arial, sans-serif",

                    size=15,

                    color="#243c54"

                )

            )

        ]

    )

    st.plotly_chart(

        fig_level,

        use_container_width=True,

        config={

            "displayModeBar": False,

            "responsive": True

        }

    )

    st.html(

        """
            </div>
        </div>
        """

    )

# =========================================================
# LEVEL SUMMARY CARDS
# =========================================================
with r3_right:
    level_columns = st.columns(

        4,

        gap="small"

    )

    level_card_data = [

        (
            "LEVEL 1",
            6,
            25.0,
            "#15984d"
        ),

        (
            "LEVEL 2",
            8,
            33.3,
            "#2455a4"
        ),

        (
            "LEVEL 3",
            5,
            20.8,
            "#d99c00"
        ),

        (
            "LEVEL 4",
            5,
            20.8,
            "#d9272e"
        )

    ]

    for i, (

            title,
            value,
            percentage,
            text_color

    ) in enumerate(
        level_card_data
    ):
        with level_columns[i]:
            st.html(

                f"""
                <div
                    class="level-card"
                    style="
                        margin-top:6px;
                    "
                >

                    <div
                        class="level-title"
                        style="
                            color:{text_color};
                        "
                    >
                        {title}
                    </div>


                    <div
                        class="level-value"
                        style="
                            color:{text_color};
                        "
                    >
                        {value}
                    </div>


                    <div
                        class="level-pct"
                    >
                        {percentage:.1f}%
                    </div>

                </div>
                """

            )

# =========================================================
# FOOTER
# =========================================================
st.html(

    """
    <div class="footer">

        🛡 &nbsp;

        © 2026 Process Safety Management Dashboard

        &nbsp; | &nbsp;

        Pillar: PROCESS SAFETY INCIDENT

    </div>
    """

)

# =========================================================
# PSI GOOGLE SHEET DATA - SHOW BELOW DASHBOARD
# =========================================================

st.markdown(
    """
    <div style="
        margin-top:15px;
        margin-bottom:0;
        padding:9px 12px;
        background:linear-gradient(
            180deg,
            #ffffff,
            #eef6fa
        );
        border:1px solid #c5dce9;
        border-bottom:2px solid #158fd0;
        border-radius:8px 8px 0 0;
        color:#173b5b;
        font-size:12px;
        font-weight:950;
        letter-spacing:.3px;
    ">
        PSI DATA - GOOGLE SHEET
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# PSI SHEET DATA
# ---------------------------------------------------------

try:

    st.dataframe(
        df,
        use_container_width=True,
        height=500,
        hide_index=True
    )

except Exception as exc:

    st.error(
        f"Unable to display PSI Google Sheet data: {exc}"
    )

