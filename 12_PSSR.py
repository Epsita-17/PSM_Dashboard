import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
# =========================================================
# OPTIONAL AUTO REFRESH
# =========================================================
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="PSSR Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(
        interval=60 * 1000,
        key="pssr_auto_refresh"
    )


# =========================================================
# GOOGLE SHEET SETTINGS
# =========================================================
SPREADSHEET_ID = (
    "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
)

PSSR_SHEET_NAME = "PSSR"

PSSR_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv"
    f"&sheet={PSSR_SHEET_NAME}"
)


# =========================================================
# LOAD GOOGLE SHEET DATA
# =========================================================
@st.cache_data(ttl=30)
def get_pssr_data():

    try:

        data = pd.read_csv(PSSR_CSV_URL)

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
            f"Unable to load PSSR Google Sheet: {exc}"
        )

        return pd.DataFrame()


df = get_pssr_data()


if df.empty:

    st.error(
        "No data found in the PSSR Google Sheet."
    )

    st.stop()


# =========================================================
# EXACT PSSR HEADER DETAILS
# =========================================================
REQUIRED_HEADERS = [
    "Sr No",
    "PSSR No.",
    "Department",
    "Section",
    "PSSR Description",
    "Due Date",
    "PSSR Completion Date",
    "Overdue/Pending/Completed",
    "Remarks"
]


def normalize_header(value):

    return (
        str(value)
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .lower()
    )


header_lookup = {
    normalize_header(col): col
    for col in df.columns
}


def find_header(header):

    key = normalize_header(header)

    if key in header_lookup:
        return header_lookup[key]

    return None


COL_SR = find_header("Sr No")
COL_PSSR_NO = find_header("PSSR No.")
COL_DEPARTMENT = find_header("Department")
COL_SECTION = find_header("Section")
COL_DESCRIPTION = find_header("PSSR Description")
COL_DUE_DATE = find_header("Due Date")
COL_COMPLETION_DATE = find_header(
    "PSSR Completion Date"
)
COL_STATUS = find_header(
    "Overdue/Pending/Completed"
)
COL_REMARKS = find_header("Remarks")


missing_columns = []

for name, column in [
    ("Sr No", COL_SR),
    ("PSSR No.", COL_PSSR_NO),
    ("Department", COL_DEPARTMENT),
    ("Section", COL_SECTION),
    ("PSSR Description", COL_DESCRIPTION),
    ("Due Date", COL_DUE_DATE),
    ("PSSR Completion Date", COL_COMPLETION_DATE),
    ("Overdue/Pending/Completed", COL_STATUS),
    ("Remarks", COL_REMARKS)
]:

    if column is None:
        missing_columns.append(name)


if missing_columns:

    st.error(
        "The following PSSR headers are missing:"
    )

    st.write(missing_columns)

    st.write(
        "Headers found in Google Sheet:"
    )

    st.write(df.columns.tolist())

    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================
work = df.copy()


work["_department"] = (
    work[COL_DEPARTMENT]
    .fillna("")
    .astype(str)
    .str.strip()
)


work["_section"] = (
    work[COL_SECTION]
    .fillna("")
    .astype(str)
    .str.strip()
)


work["_description"] = (
    work[COL_DESCRIPTION]
    .fillna("")
    .astype(str)
    .str.strip()
)


work["_pssr_no"] = (
    work[COL_PSSR_NO]
    .fillna("")
    .astype(str)
    .str.strip()
)


work["_remarks"] = (
    work[COL_REMARKS]
    .fillna("")
    .astype(str)
    .str.strip()
)


work["_status_raw"] = (
    work[COL_STATUS]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)


work["_due_date"] = pd.to_datetime(
    work[COL_DUE_DATE],
    errors="coerce",
    dayfirst=True
)


work["_completion_date"] = pd.to_datetime(
    work[COL_COMPLETION_DATE],
    errors="coerce",
    dayfirst=True
)


# =========================================================
# STATUS NORMALIZATION
# =========================================================
def normalize_status(row):

    status = str(
        row["_status_raw"]
    ).strip().lower()

    if "overdue" in status:
        return "Overdue"

    if "pending" in status:
        return "Pending"

    if "completed" in status:
        return "Completed"

    if "complete" in status:
        return "Completed"

    # If status is blank, use completion date
    if pd.notna(row["_completion_date"]):
        return "Completed"

    # Otherwise determine overdue from Due Date
    if pd.notna(row["_due_date"]):

        today = pd.Timestamp.today().normalize()

        if row["_due_date"] < today:
            return "Overdue"

    return "Pending"


work["_status"] = work.apply(
    normalize_status,
    axis=1
)


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>

/* ======================================================
   PAGE
   ====================================================== */

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
[data-testid="stAppViewContainer"] {
    margin:0 !important;
    padding:0 !important;
}

[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    width:100% !important;
    max-width:none !important;
    margin:0 !important;
    padding:0 8px !important;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #f8fbfd 0%,
            #f4f9fc 55%,
            #edf5f9 100%
        ) !important;
}

[data-testid="stVerticalBlock"] {
    gap:0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap:7px !important;
}


/* ======================================================
   FILTERS
   ====================================================== */

.filter-title {
    color:#193d77;
    font-size:10px;
    font-weight:900;
    margin:0 0 2px 3px;
}

div[data-baseweb="select"] > div {
    height:30px !important;
    min-height:30px !important;
    border-radius:6px !important;
    background:#ffffff !important;
    border:1px solid #d2dce3 !important;
}

div[data-baseweb="select"] * {
    color:#26384a !important;
    font-size:10px !important;
}

div[data-baseweb="select"] svg {
    fill:#193d77 !important;
}


/* ======================================================
   KPI CARDS
   ====================================================== */

.kpi-card {
    height:118px;
    position:relative;
    overflow:hidden;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 30%,
            #fcfdfe 60%,
            #f3f8fa 100%
        );

    border:1px solid #dfe7eb;
    border-radius:9px;

    box-shadow:
        0 8px 20px rgba(55,90,110,.09),
        0 2px 5px rgba(55,90,110,.06),
        inset 0 1px 0 #ffffff;
}

.kpi-label {
    color:#193d77;
    font-size:11px;
    font-weight:950;
    text-align:center;
    padding-top:12px;
}

.kpi-value {
    color:#164b91;
    font-size:39px;
    line-height:1;
    font-weight:950;
    text-align:center;
    margin-top:9px;
}

.kpi-value.red {
    color:#d9272e;
}

.kpi-sub {
    color:#536779;
    font-size:10px;
    font-weight:700;
    text-align:center;
    margin-top:7px;
}


/* ======================================================
   COMPLIANCE
   ====================================================== */

.compliance-card {
    height:118px;
    position:relative;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f3f8fa
        );

    border:1px solid #dfe7eb;
    border-radius:9px;

    box-shadow:
        0 8px 20px rgba(55,90,110,.09),
        inset 0 1px 0 #ffffff;
}

.compliance-title {
    position:absolute;
    top:10px;
    left:0;
    right:0;
    text-align:center;

    font-size:11px;
    color:#193d77;
    font-weight:950;
}

.donut-wrap {
    width:80px;
    height:80px;
    position:relative;
    margin-top:8px;
}

.donut-svg {
    width:80px;
    height:80px;
    transform:rotate(-90deg);
}

.donut-bg {
    fill:none;
    stroke:#dfe5ea;
    stroke-width:10;
}

.donut-progress {
    fill:none;
    stroke:#164b91;
    stroke-width:10;
}

.donut-text {
    position:absolute;
    top:27px;
    left:0;
    right:0;

    text-align:center;

    font-size:22px;
    font-weight:950;
    color:#172b43;
}

.compliance-sub {
    position:absolute;
    bottom:7px;
    left:0;
    right:0;

    text-align:center;

    font-size:9px;
    color:#52677b;
}


/* ======================================================
   CHART PANELS
   ====================================================== */

.chart-panel {
    background:#ffffff;

    border:1px solid #dfe7eb;
    border-radius:9px;

    overflow:hidden;

    box-shadow:
        0 7px 18px rgba(55,90,110,.08),
        0 2px 5px rgba(55,90,110,.05);
}

.chart-title {
    height:35px;

    display:flex;
    align-items:center;

    padding:0 15px;

    color:#193d77;

    font-size:11px;
    font-weight:950;

    background:#ffffff;

    border-bottom:1px solid #edf1f4;
}

.chart-content {
    padding:2px 5px 5px;
    background:#ffffff;
}


/* ======================================================
   REGISTER
   ====================================================== */

.register-panel {
    background:#ffffff;

    border:1px solid #dfe7eb;
    border-radius:9px;

    overflow:hidden;

    box-shadow:
        0 7px 18px rgba(55,90,110,.08),
        0 2px 5px rgba(55,90,110,.05);
}

.register-title {
    height:31px;

    display:flex;
    align-items:center;

    padding:0 14px;

    color:#193d77;

    font-size:11px;
    font-weight:950;

    background:#ffffff;

    border-bottom:1px solid #e5ebef;
}

.pssr-table {
    width:100%;
    border-collapse:collapse;
    table-layout:fixed;

    font-family:Arial,sans-serif;
    font-size:10px;
}

.pssr-table th {
    background:#164b91;
    color:#ffffff;

    font-weight:900;

    padding:8px 5px;

    text-align:center;

    border-right:
        1px solid rgba(255,255,255,.35);

    white-space:nowrap;
}

.pssr-table td {
    height:36px;

    padding:5px 7px;

    text-align:center;

    border-bottom:1px solid #e5ebef;
    border-right:1px solid #e8edf0;

    color:#26384a;

    background:#ffffff;

    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
}

.pssr-table tr:nth-child(even) td {
    background:#fbfdfe;
}

.pssr-table td.left {
    text-align:left;
}

.status-badge {
    display:inline-flex;

    align-items:center;
    justify-content:center;

    min-width:68px;

    padding:4px 8px;

    border-radius:4px;

    font-size:9px;
    font-weight:900;
}

.status-completed {
    background:#e6f5ec;
    color:#27834c;
}

.status-pending {
    background:#fff5dc;
    color:#bd7910;
}

.status-overdue {
    background:#fde4e4;
    color:#d9272e;
}

.icon-btn {
    display:inline-flex;

    align-items:center;
    justify-content:center;

    width:25px;
    height:25px;

    border:1px solid #cbd9e2;
    border-radius:5px;

    background:#ffffff;
    color:#164b91;

    font-size:13px;
    text-decoration:none;
}

.remark-icon {
    font-size:16px;
    color:#164b91;
}

.register-footer {
    height:35px;

    display:flex;
    align-items:center;
    justify-content:space-between;

    padding:0 14px;

    color:#586b7b;
    font-size:9px;

    background:#ffffff;
}

.pagination {
    display:flex;
    align-items:center;
    gap:5px;
}

.page-btn {
    min-width:27px;
    height:25px;

    display:flex;
    align-items:center;
    justify-content:center;

    border:1px solid #d5dfe5;
    border-radius:5px;

    background:#ffffff;
    color:#26384a;

    font-size:10px;
}

.page-current {
    background:#164b91;
    border-color:#164b91;
    color:#ffffff;
    font-weight:900;
}


/* ======================================================
   FOOTER
   ====================================================== */

.footer {
    height:20px;

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

    font-size:9px;
    font-weight:800;

    border-top:1px solid #d7e3ea;
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

    width:560px;
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

        <!-- LEFT TOWER -->

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


        <!-- LEFT PIPE -->

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


        <!-- LEFT PIPING -->

        <g class="light">

            <path d="M55 113 H245 V85 H320"/>

            <path d="M120 125 H260 V105 H355"/>

            <path d="M180 96 H285 V65 H340"/>

            <path d="M215 130 V70 H280"/>

        </g>


        <!-- LEFT VESSEL -->

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


        <!-- RIGHT TOWER -->

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


        <!-- RIGHT PIPE -->

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


        <!-- RIGHT PIPING -->

        <g class="light">

            <path d="M1620 112 H1425 V85 H1350"/>

            <path d="M1575 125 H1410 V104 H1330"/>

            <path d="M1500 95 H1390 V65 H1335"/>

            <path d="M1465 130 V70 H1390"/>

        </g>


        <!-- RIGHT VESSEL -->

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


        <!-- FLOOR PIPING -->

        <g class="light">

            <path d="M0 137 H1672"/>

            <path d="M0 126 H420 V116 H650"/>

            <path d="M1672 126 H1250 V116 H1020"/>

        </g>


        <!-- HEXAGONS -->

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
            PILLAR: PSSR
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
# MONTH + DEPARTMENT FILTER
# =========================================================
filter_month, filter_department = st.columns(
    [1, 1],
    gap="small"
)


with filter_month:

    st.markdown(
        "<div class='filter-title'>MONTH</div>",
        unsafe_allow_html=True
    )

    valid_dates = (
        work["_due_date"]
        .dropna()
    )

    if not valid_dates.empty:

        month_values = (
            valid_dates
            .dt.to_period("M")
            .drop_duplicates()
            .sort_values(
                ascending=False
            )
        )

        month_labels = [
            period.strftime("%B %Y")
            for period in month_values
        ]

    else:

        month_labels = []


    month_options = [
        "All Months"
    ] + month_labels


    selected_month = st.selectbox(
        "Month",
        month_options,
        index=0,
        label_visibility="collapsed",
        key="pssr_month"
    )


with filter_department:

    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )


    departments = sorted(
        [
            str(x).strip()
            for x in
            work["_department"].unique()
            if str(x).strip()
        ],
        key=lambda x: x.lower()
    )


    department_options = [
        "All Departments"
    ] + departments


    selected_department = st.selectbox(
        "Department",
        department_options,
        index=0,
        label_visibility="collapsed",
        key="pssr_department"
    )


# =========================================================
# APPLY FILTER
# =========================================================
filtered_df = work.copy()


if selected_department != "All Departments":

    filtered_df = filtered_df[
        filtered_df["_department"]
        == selected_department
    ]


if selected_month != "All Months":

    month_period = pd.Period(
        pd.to_datetime(
            selected_month,
            format="%B %Y"
        ),
        freq="M"
    )

    filtered_df = filtered_df[
        filtered_df["_due_date"]
        .dt
        .to_period("M")
        == month_period
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================
total_pssr = len(filtered_df)

completed = int(
    (
        filtered_df["_status"]
        == "Completed"
    ).sum()
)

pending = int(
    (
        filtered_df["_status"]
        == "Pending"
    ).sum()
)

overdue = int(
    (
        filtered_df["_status"]
        == "Overdue"
    ).sum()
)

compliance = (
    completed / total_pssr * 100
    if total_pssr > 0
    else 0
)


# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5 = st.columns(
    [1.05, 1.05, 1.05, 1.05, .95],
    gap="small"
)


# ---------------------------------------------------------
# TOTAL PSSR
# ---------------------------------------------------------
with k1:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TOTAL PSSR
            </div>

            <div class="kpi-value">
                {total_pssr}
            </div>

            <div class="kpi-sub">
                100% of total
            </div>

        </div>
        """
    )


# ---------------------------------------------------------
# COMPLETED
# ---------------------------------------------------------
with k2:

    completed_pct = (
        completed / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                COMPLETED PSSR
            </div>

            <div class="kpi-value">
                {completed}
            </div>

            <div class="kpi-sub">
                {completed_pct:.1f}% completed
            </div>

        </div>
        """
    )


# ---------------------------------------------------------
# PENDING
# ---------------------------------------------------------
with k3:

    pending_pct = (
        pending / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                PENDING PSSR
            </div>

            <div class="kpi-value red">
                {pending}
            </div>

            <div class="kpi-sub">
                {pending_pct:.1f}% of total
            </div>

        </div>
        """
    )


# ---------------------------------------------------------
# OVERDUE
# ---------------------------------------------------------
with k4:

    overdue_pct = (
        overdue / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                OVERDUE PSSR
            </div>

            <div class="kpi-value red">
                {overdue}
            </div>

            <div class="kpi-sub">
                {overdue_pct:.1f}% of total
            </div>

        </div>
        """
    )


# ---------------------------------------------------------
# COMPLIANCE
# ---------------------------------------------------------
with k5:

    radius = 40

    circumference = (
        2 * 3.14159265359 * radius
    )

    progress = (
        circumference
        * min(
            max(compliance, 0),
            100
        )
        / 100
    )

    st.html(
        f"""
        <div class="compliance-card">

            <div class="compliance-title">
                PSSR COMPLIANCE
            </div>

            <div class="donut-wrap">

                <svg
                    class="donut-svg"
                    viewBox="0 0 100 100"
                >

                    <circle
                        class="donut-bg"
                        cx="50"
                        cy="50"
                        r="{radius}"
                    />

                    <circle
                        class="donut-progress"
                        cx="50"
                        cy="50"
                        r="{radius}"
                        stroke-dasharray="
                            {progress:.2f}
                            {circumference:.2f}
                        "
                    />

                </svg>

                <div class="donut-text">
                    {compliance:.1f}%
                </div>

            </div>

            <div class="compliance-sub">
                Compliance Percentage
            </div>

        </div>
        """
    )


# =========================================================
# CHART ROW
# =========================================================
chart_left, chart_right = st.columns(
    [1.03, .97],
    gap="small"
)


# =========================================================
# DEPARTMENT-WISE PSSR
# =========================================================
with chart_left:

    st.html(
        """
        <div class="chart-panel">

            <div class="chart-title">
                NO. OF PSSR PERFORMED BY DEPARTMENT
            </div>

            <div class="chart-content">
        """
    )


    department_counts = (
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


    fig_department = go.Figure()


    fig_department.add_trace(
        go.Bar(

            x=department_counts.index.tolist(),

            y=department_counts.values.tolist(),

            text=department_counts.values.tolist(),

            textposition="outside",

            cliponaxis=False,

            marker=dict(

                color="#164b91",

                line=dict(
                    color="#0a2d5a",
                    width=1
                )

            ),

            hovertemplate=(
                "%{x}<br>"
                "No. of PSSR: %{y}"
                "<extra></extra>"
            )
        )
    )


    max_value = (
        int(department_counts.max())
        if not department_counts.empty
        else 1
    )


    fig_department.update_layout(

        height=190,

        margin=dict(
            l=45,
            r=18,
            t=15,
            b=43
        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            color="#111111"
        ),

        yaxis=dict(

            title="No. of PSSR",

            range=[
                0,
                max(
                    max_value + 3,
                    5
                )
            ],

            dtick=5
                if max_value >= 10
                else 1,

            gridcolor="#dce7ed",

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

            showgrid=False,

            title_font=dict(
                size=10
            )

        ),

        showlegend=False,

        bargap=.32

    )


    st.plotly_chart(

        fig_department,

        use_container_width=True,

        config={
            "displayModeBar":False,
            "responsive":True
        }

    )


    st.html(
        "</div></div>"
    )


# =========================================================
# STATUS SUMMARY
# =========================================================
with chart_right:

    st.html(
        """
        <div class="chart-panel">

            <div class="chart-title">
                PSSR STATUS SUMMARY
            </div>

            <div class="chart-content">
        """
    )


    status_labels = [
        "Completed",
        "Pending",
        "Overdue"
    ]


    status_values = [
        completed,
        pending,
        overdue
    ]


    fig_status = go.Figure()


    fig_status.add_trace(

        go.Pie(

            labels=status_labels,

            values=status_values,

            hole=.55,

            sort=False,

            direction="clockwise",

            textinfo="none",

            marker=dict(

                colors=[
                    "#164b91",
                    "#e51f28",
                    "#f36d72"
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

    )


    fig_status.update_layout(

        height=190,

        margin=dict(
            l=5,
            r=5,
            t=0,
            b=0
        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        showlegend=True,

        legend=dict(

            orientation="v",

            x=.68,

            y=.50,

            xanchor="left",

            yanchor="middle",

            font=dict(
                family="Arial",
                size=10,
                color="#26384a"
            ),

            bgcolor="rgba(255,255,255,0)",

            itemsizing="constant"

        ),

        annotations=[

            dict(

                text=(
                    f"<b>{total_pssr}</b>"
                    "<br>"
                    "<span "
                    "style='font-size:10px'>"
                    "TOTAL"
                    "</span>"
                ),

                x=.50,

                y=.50,

                xref="paper",

                yref="paper",

                showarrow=False,

                align="center",

                font=dict(

                    family="Arial",

                    size=24,

                    color="#172b43"

                )

            )

        ]

    )


    st.plotly_chart(

        fig_status,

        use_container_width=True,

        config={
            "displayModeBar":False,
            "responsive":True
        }

    )


    st.html(
        "</div></div>"
    )


# =========================================================
# PSSR REGISTER
# =========================================================
st.html(
    """
    <div class="register-panel">

        <div class="register-title">
            PSSR REGISTER
        </div>
    """
)


# =========================================================
# PAGINATION
# =========================================================
PAGE_SIZE = 5


if "pssr_page" not in st.session_state:
    st.session_state.pssr_page = 1


total_pages = max(
    1,
    (
        len(filtered_df)
        + PAGE_SIZE
        - 1
    )
    // PAGE_SIZE
)


if st.session_state.pssr_page > total_pages:

    st.session_state.pssr_page = total_pages


page = st.session_state.pssr_page


start_idx = (
    page - 1
) * PAGE_SIZE


end_idx = (
    start_idx
    + PAGE_SIZE
)


page_df = filtered_df.iloc[
    start_idx:end_idx
].copy()


# =========================================================
# TABLE
# =========================================================
html = """

<div style="
    padding:0 6px;
">

<table class="pssr-table">

<colgroup>

    <col style="width:19%;">

    <col style="width:19%;">

    <col style="width:14%;">

    <col style="width:10%;">

    <col style="width:10%;">

    <col style="width:10%;">

    <col style="width:18%;">

</colgroup>

<thead>

<tr>

    <th>PSSR No.</th>

    <th>PSSR Description</th>

    <th>Department</th>

    <th>Status</th>

    <th>Upload Report</th>

    <th>View Report</th>

    <th>Remark</th>

</tr>

</thead>

<tbody>
"""


def escape_html(value):

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


for _, row in page_df.iterrows():

    status = row["_status"]


    if status == "Completed":

        status_class = (
            "status-completed"
        )

    elif status == "Overdue":

        status_class = (
            "status-overdue"
        )

    else:

        status_class = (
            "status-pending"
        )


    pssr_no = escape_html(
        row["_pssr_no"]
    )

    description = escape_html(
        row["_description"]
    )

    department = escape_html(
        row["_department"]
    )

    remarks = escape_html(
        row["_remarks"]
    )


    html += f"""

<tr>

    <td
        class="left"
        title="{pssr_no}"
    >
        {pssr_no}
    </td>


    <td
        title="{description}"
    >
        {description}
    </td>


    <td>
        {department}
    </td>


    <td>

        <span
            class="
                status-badge
                {status_class}
            "
        >
            {status.upper()}
        </span>

    </td>


    <td>

        <span
            class="icon-btn"
            title="Upload Report"
        >
            ⇧
        </span>

    </td>


    <td>

        <span
            class="icon-btn"
            title="View Report"
        >
            ◉
        </span>

    </td>


    <td>

        <span
            class="remark-icon"
            title="{remarks}"
        >
            ▱
        </span>

    </td>

</tr>

"""


if page_df.empty:

    html += """

<tr>

<td
    colspan="7"
    style="
        height:120px;
        text-align:center;
        color:#71808d;
    "
>
    No PSSR records found
    for the selected filters.
</td>

</tr>

"""


html += """

</tbody>

</table>

</div>

"""


st.html(html)


# =========================================================
# REGISTER FOOTER
# =========================================================
shown_from = (
    start_idx + 1
    if len(filtered_df) > 0
    else 0
)


shown_to = min(
    end_idx,
    len(filtered_df)
)


st.html(
    f"""
    <div class="register-footer">

        <div>

            Showing
            {shown_from}
            to
            {shown_to}
            of
            {len(filtered_df)}
            entries

        </div>


        <div class="pagination">

            <span class="page-btn">
                «
            </span>

            <span class="page-btn">
                ‹
            </span>

            <span class="page-btn page-current">
                {page}
            </span>

            <span class="page-btn">
                {min(
                    page + 1,
                    total_pages
                )}
            </span>

            <span class="page-btn">
                …
            </span>

            <span class="page-btn">
                {total_pages}
            </span>

            <span class="page-btn">
                ›
            </span>

            <span class="page-btn">
                »
            </span>

        </div>

    </div>
    """
)


# =========================================================
# REAL PAGINATION BUTTONS
# =========================================================
if total_pages > 1:

    p1, p2, p3 = st.columns(
        [1, 1, 1]
    )


    with p1:

        if page > 1:

            if st.button(
                "← Previous",
                key="pssr_previous"
            ):

                st.session_state.pssr_page -= 1

                st.rerun()


    with p3:

        if page < total_pages:

            if st.button(
                "Next →",
                key="pssr_next"
            ):

                st.session_state.pssr_page += 1

                st.rerun()


st.html(
    "</div>"
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

        Pillar: PSSR

    </div>
    """
)


# =========================================================
# AUTO REFRESH MESSAGE
# =========================================================
if not AUTO_REFRESH_AVAILABLE:

    st.caption(
        "Automatic refresh is disabled. "
        "Install streamlit-autorefresh with: "
        "pip install streamlit-autorefresh"
    )

