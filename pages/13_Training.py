import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import re
import os
import base64
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Training Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# GOOGLE SHEET
# =========================================================

SPREADSHEET_ID = (
    "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
)

TRAINING_SHEET_NAME = "TRAINING"

TRAINING_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet="
    f"{TRAINING_SHEET_NAME}"
)


# =========================================================
# LOAD GOOGLE SHEET
# =========================================================

@st.cache_data(ttl=60)
def get_training_data():

    try:

        data = pd.read_csv(
            TRAINING_CSV_URL
        )

        data.columns = (
            data.columns
            .astype(str)
            .str.replace(
                "\xa0",
                " ",
                regex=False
            )
            .str.replace(
                "\n",
                " ",
                regex=False
            )
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

        return data.replace(
            {
                "nan": "",
                "NaN": "",
                "NAN": ""
            }
        )

    except Exception as exc:

        st.error(
            f"Unable to load Google Sheet "
            f"'{TRAINING_SHEET_NAME}': {exc}"
        )

        return pd.DataFrame()


df = get_training_data()


if df.empty:

    st.error(
        f"No data found in Google Sheet tab "
        f"'{TRAINING_SHEET_NAME}'."
    )

    st.stop()


# =========================================================
# COLUMN NORMALIZATION
# =========================================================

def clean_column_name(value):

    value = str(value)

    value = (
        value
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .lower()
    )

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    return value.strip("_")


column_map = {
    clean_column_name(col): col
    for col in df.columns
}


def find_exact_column(column_name):

    cleaned = clean_column_name(
        column_name
    )

    return column_map.get(
        cleaned
    )


# =========================================================
# ACTUAL TRAINING SHEET COLUMNS
# =========================================================

COL_SL_NO = find_exact_column(
    "Sl No."
)

COL_DEPARTMENT = find_exact_column(
    "Departments"
)

COL_PROCESS = find_exact_column(
    "Process"
)

COL_TOTAL_L08 = find_exact_column(
    "Total Employees (L08 & Above)"
)

COL_TOTAL_BELOW_L08 = find_exact_column(
    "Total Employees (Below L08)"
)

COL_TOTAL_ASSOCIATES = find_exact_column(
    "Total Associates"
)

COL_TOTAL_CONTRACTUAL = find_exact_column(
    "Total Contractual Workers"
)

COL_COMPLETED_L08 = find_exact_column(
    "Completed Training (L08 & Above)"
)

COL_COMPLETED_BELOW_L08 = find_exact_column(
    "Completed Training (Below L08)"
)

COL_COMPLETED_ASSOCIATES = find_exact_column(
    "Completed Training (Associates)"
)

COL_COMPLETED_CONTRACTS = find_exact_column(
    "Completed Training (Contracts)"
)

COL_PCT_L08 = find_exact_column(
    "Completion % (L08 & Above)"
)

COL_PCT_BELOW_L08 = find_exact_column(
    "Completion % (Below L08)"
)

COL_PCT_ASSOCIATES = find_exact_column(
    "Completion % (Associates)"
)

COL_PCT_CONTRACTUAL = find_exact_column(
    "Completion % (Contractual)"
)


# =========================================================
# OPTIONAL MONTH COLUMN
# =========================================================

COL_MONTH = None

for possible_month_column in [
    "Month",
    "Training Month",
    "Date",
    "Training Date"
]:

    found_month_column = find_exact_column(
        possible_month_column
    )

    if found_month_column:

        COL_MONTH = found_month_column

        break


# =========================================================
# REQUIRED COLUMN CHECK
# =========================================================

required_columns = {

    "Sl No.": COL_SL_NO,

    "Departments": COL_DEPARTMENT,

    "Process": COL_PROCESS,

    "Total Employees (L08 & Above)": COL_TOTAL_L08,

    "Total Employees (Below L08)": COL_TOTAL_BELOW_L08,

    "Total Associates": COL_TOTAL_ASSOCIATES,

    "Total Contractual Workers": COL_TOTAL_CONTRACTUAL,

    "Completed Training (L08 & Above)": COL_COMPLETED_L08,

    "Completed Training (Below L08)": COL_COMPLETED_BELOW_L08,

    "Completed Training (Associates)": COL_COMPLETED_ASSOCIATES,

    "Completed Training (Contracts)": COL_COMPLETED_CONTRACTS,

    "Completion % (L08 & Above)": COL_PCT_L08,

    "Completion % (Below L08)": COL_PCT_BELOW_L08,

    "Completion % (Associates)": COL_PCT_ASSOCIATES,

    "Completion % (Contractual)": COL_PCT_CONTRACTUAL

}


missing_columns = [
    name
    for name, actual in required_columns.items()
    if actual is None
]


if missing_columns:

    st.error(
        "The following required columns are missing "
        "from the TRAINING Google Sheet:"
    )

    for column in missing_columns:

        st.write(
            f"- {column}"
        )

    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

work = df.copy()


# =========================================================
# TEXT COLUMNS
# =========================================================

work["_sl_no"] = (
    work[COL_SL_NO]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_department"] = (
    work[COL_DEPARTMENT]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_process"] = (
    work[COL_PROCESS]
    .fillna("")
    .astype(str)
    .str.strip()
)


# =========================================================
# MONTH DATA
# =========================================================

if COL_MONTH:

    work["_date"] = pd.to_datetime(
        work[COL_MONTH],
        errors="coerce",
        dayfirst=True
    )

else:

    work["_date"] = pd.NaT


# =========================================================
# NUMERIC FUNCTION
# =========================================================

def to_numeric(series):

    return pd.to_numeric(

        series
        .astype(str)
        .str.replace(
            ",",
            "",
            regex=False
        )
        .str.replace(
            "%",
            "",
            regex=False
        )
        .str.strip(),

        errors="coerce"

    ).fillna(0)


# =========================================================
# TOTAL EMPLOYEE COLUMNS
# =========================================================

work["_total_l08"] = to_numeric(
    work[COL_TOTAL_L08]
)

work["_total_below_l08"] = to_numeric(
    work[COL_TOTAL_BELOW_L08]
)

work["_total_associates"] = to_numeric(
    work[COL_TOTAL_ASSOCIATES]
)

work["_total_contractual"] = to_numeric(
    work[COL_TOTAL_CONTRACTUAL]
)


# =========================================================
# COMPLETED TRAINING COLUMNS
# =========================================================

work["_completed_l08"] = to_numeric(
    work[COL_COMPLETED_L08]
)

work["_completed_below_l08"] = to_numeric(
    work[COL_COMPLETED_BELOW_L08]
)

work["_completed_associates"] = to_numeric(
    work[COL_COMPLETED_ASSOCIATES]
)

work["_completed_contractual"] = to_numeric(
    work[COL_COMPLETED_CONTRACTS]
)


# =========================================================
# COMPLETION PERCENTAGE COLUMNS
# =========================================================

work["_pct_l08"] = to_numeric(
    work[COL_PCT_L08]
)

work["_pct_below_l08"] = to_numeric(
    work[COL_PCT_BELOW_L08]
)

work["_pct_associates"] = to_numeric(
    work[COL_PCT_ASSOCIATES]
)

work["_pct_contractual"] = to_numeric(
    work[COL_PCT_CONTRACTUAL]
)


# =========================================================
# VISUAL CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   REMOVE DEFAULT STREAMLIT SPACE
   ========================================================= */

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

    overflow-x:hidden !important;

}


[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {

    width:100% !important;

    max-width:none !important;

    margin:0 !important;

    padding:0 8px !important;

}


[data-testid="stAppViewContainer"] > .main > div {

    padding:0 !important;

}


/* =========================================================
   FILTER
   ========================================================= */

.filter-title {

    color:#193d77;

    font-family:Arial,sans-serif;

    font-size:12px;

    font-weight:900;

    margin-bottom:4px;

    letter-spacing:.3px;

}


[data-testid="stSelectbox"] {

    margin-bottom:5px !important;

}


[data-testid="stSelectbox"] > div > div {

    min-height:36px !important;

}


[data-testid="stSelectbox"] div[data-baseweb="select"] {

    min-height:36px !important;

}


[data-testid="stSelectbox"] input {

    font-size:13px !important;

}


[data-testid="stSelectbox"] span {

    font-size:13px !important;

}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi-card {

    min-height:118px;

    padding:14px 10px;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 24%,
            #fffefe 48%,
            #f9fcfd 70%,
            #edf6fa 100%
        );

    border:1px solid #cbdde6;

    border-radius:13px;

    overflow:hidden;

    box-shadow:
        0 10px 23px
        rgba(55,90,110,.13),

        0 4px 8px
        rgba(55,90,110,.08),

        inset 0 2px 0 #ffffff,

        inset 0 -7px 13px
        rgba(175,202,215,.15);

}


.kpi-label {

    color:#193d77;

    font-family:Arial,sans-serif;

    font-size:11px;

    font-weight:950;

    line-height:1.15;

    text-align:center;

}


.kpi-value {

    font-family:Arial,sans-serif;

    font-size:33px;

    font-weight:950;

    line-height:1;

    text-align:center;

}


.kpi-value.blue {

    color:#174b87;

}


.kpi-value.red {

    color:#e1262d;

}


.kpi-sub {

    margin-top:7px;

    color:#587084;

    font-family:Arial,sans-serif;

    font-size:10px;

    font-weight:700;

    text-align:center;

}


/* =========================================================
   DONUT
   ========================================================= */

.donut-card {

    min-height:118px;

    padding:8px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #edf6fa
        );

    border:1px solid #cbdde6;

    border-radius:13px;

    box-shadow:
        0 10px 23px
        rgba(55,90,110,.13),

        inset 0 2px 0 #ffffff;

}


.donut-title {

    color:#193d77;

    font-family:Arial,sans-serif;

    font-size:10px;

    font-weight:950;

    text-align:center;

}


.donut-wrap {

    position:relative;

    width:70px;

    height:70px;

    margin:3px auto;

}


.donut-svg {

    width:70px;

    height:70px;

    transform:rotate(-90deg);

}


.donut-bg {

    fill:none;

    stroke:#dce9ef;

    stroke-width:10;

}


.donut-progress {

    fill:none;

    stroke:#2b66a8;

    stroke-width:10;

    stroke-linecap:round;

}


.donut-text {

    position:absolute;

    top:50%;

    left:50%;

    transform:translate(-50%,-50%);

    color:#193d77;

    font-size:13px;

    font-weight:950;

}


.donut-bottom {

    color:#587084;

    font-size:9px;

    font-weight:800;

    text-align:center;

}


/* =========================================================
   PANELS
   ========================================================= */

.panel,
.chart-panel {

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 24%,
            #fffefe 48%,
            #f9fcfd 70%,
            #edf6fa 100%
        );

    border:1px solid #cbdde6;

    border-radius:13px;

    overflow:hidden;

    box-shadow:
        0 10px 23px
        rgba(55,90,110,.13),

        0 4px 8px
        rgba(55,90,110,.08),

        inset 0 2px 0 #ffffff,

        inset 0 -7px 13px
        rgba(175,202,215,.15);

}


.panel-title,
.chart-panel-title {

    min-height:32px;

    display:flex;

    align-items:center;

    padding:0 12px;

    color:#193d77;

    font-size:12px;

    font-weight:950;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f7fbfc
        );

    border-bottom:1px solid #dce7ec;

}


/* =========================================================
   TABLE
   ========================================================= */

.training-table {

    width:100%;

    border-collapse:collapse;

    font-family:Arial,sans-serif;

    font-size:10px;

}


.training-table th {

    background:#193d77;

    color:#ffffff;

    font-weight:900;

    padding:7px 8px;

    text-align:center;

}


.training-table th:first-child {

    text-align:left;

}


.training-table td {

    padding:6px 8px;

    text-align:center;

    border-bottom:1px solid #e5ebef;

    color:#111111;

    font-weight:700;

    background:#ffffff;

}


.training-table td:first-child {

    text-align:left;

    font-weight:800;

}


.training-table tr:nth-child(even) td {

    background:#fbfdfe;

}


.training-table tr:nth-child(odd) td {

    background:#ffffff;

}


.training-table td.overall {

    font-weight:950;

    color:#193d77;

}


/* =========================================================
   FOOTER
   ========================================================= */

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


/* =========================================================
   PLOTLY
   ========================================================= */

[data-testid="stPlotlyChart"] {

    margin-top:-5px !important;

    margin-bottom:-10px !important;

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# PREMIUM 3D INDUSTRIAL HEADER — REFERENCE MATCH
# =========================================================

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "jsw_jfe_logo.jpg"
)

if not os.path.exists(LOGO_PATH):
    st.error(f"Logo file not found: {LOGO_PATH}")
    st.stop()

with open(LOGO_PATH, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode("utf-8")


header_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    background: #ffffff;
}


/* =====================================================
   MAIN OUTER HEADER
   — FULL CORNER CURVE LIKE REFERENCE
   ===================================================== */

.header {
    position: relative;

    width: calc(100% - 8px);
    height: 150px;

    /* Move the complete header slightly downward */
    margin: 8px 4px 0;

    overflow: hidden;

    background:
        radial-gradient(
            ellipse at center,
            #0a3552 0%,
            #062239 35%,
            #031421 67%,
            #010910 100%
        );

    border: 1px solid #51c7f5;

    border-radius: 20px;

    box-shadow:
        0 0 0 2px rgba(4,34,52,.92),
        0 4px 14px rgba(0,0,0,.40),
        inset 0 1px 0 rgba(255,255,255,.12),
        inset 0 -1px 0 rgba(48,194,241,.75);
}


/* =====================================================
   SECONDARY INNER CURVED FRAME
   ===================================================== */

.header-frame {
    position: absolute;

    inset: 5px;

    z-index: 40;

    border: 1px solid rgba(69,190,237,.48);

    border-radius: 15px;

    pointer-events: none;

    box-shadow:
        inset 0 0 18px rgba(0,151,220,.13);
}


/* =====================================================
   TOP REFLECTIVE GLOW
   ===================================================== */

.header-glow {
    position: absolute;

    z-index: 6;

    left: 17%;
    right: 17%;
    top: 2px;

    height: 28px;

    background:
        radial-gradient(
            ellipse,
            rgba(170,235,255,.20) 0%,
            rgba(65,194,242,.10) 35%,
            transparent 72%
        );

    filter: blur(3px);

    pointer-events: none;
}


/* =====================================================
   TECHNICAL GRID
   ===================================================== */

.header::before {
    content: "";

    position: absolute;

    inset: 0;

    background:
        linear-gradient(
            rgba(38,184,242,.045) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(38,184,242,.045) 1px,
            transparent 1px
        );

    background-size: 28px 28px;

    opacity: .9;
}


/* =====================================================
   INDUSTRIAL BACKGROUND
   ===================================================== */

.industrial {
    position: absolute;

    left: 0;
    right: 0;
    bottom: 0;

    width: 100%;
    height: 145px;

    z-index: 2;

    opacity: .55;
}

.industrial .steel {
    fill: #12364e;
    stroke: #2999c4;
    stroke-width: 1.1;
}

.industrial .highlight {
    fill: none;
    stroke: #39c5f5;
    stroke-width: 1;
    opacity: .58;
}

.industrial .warm {
    fill: #f2ad23;
    opacity: .78;
}

.industrial .glass {
    fill: #0a5e92;
    stroke: #53d4ff;
    stroke-width: .7;
    opacity: .45;
}

.tech {
    fill: none;
    stroke: #2ca6d8;
    stroke-width: .8;
    opacity: .18;
}


/* =====================================================
   LOGO PANEL
   — WIDE RECTANGULAR, NOT SQUARE
   ===================================================== */

.logo-panel {
    position: absolute;

    z-index: 30;

    left: 2.6%;
    top: 50%;

    transform: translateY(-50%);

    width: 17.0%;
    max-width: 325px;
    min-width: 235px;

    height: 108px;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 6px 10px;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f9fbfd 42%,
            #e4edf3 100%
        );

    border: 1px solid #a5bccb;

    border-radius: 14px;

    box-shadow:
        0 7px 15px rgba(0,0,0,.40),
        0 0 0 2px rgba(20,63,86,.82),
        inset 0 2px 0 rgba(255,255,255,.98),
        inset 0 -4px 7px rgba(75,105,124,.14);
}

.logo-panel::before {
    content: "";

    position: absolute;

    inset: -4px;

    border-radius: 17px;

    border: 1px solid rgba(84,202,247,.68);

    pointer-events: none;
}

.logo-panel::after {
    content: "";

    position: absolute;

    left: 12%;
    right: 12%;
    top: -3px;

    height: 3px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8fe6ff,
            transparent
        );

    box-shadow:
        0 0 8px rgba(72,204,250,.82);
}

.header-logo {
    display: block;

    width: 100%;
    height: 100%;

    object-fit: contain;
    object-position: center;

    border-radius: 6px;
}


/* =====================================================
   CENTRAL TITLE FRAME
   — LARGE 3D BEVELED PANEL
   ===================================================== */

.title-frame {
    position: absolute;

    z-index: 22;

    left: 50%;
    top: 50%;

    /* Exact horizontal + vertical centering */
    transform: translate(-50%, -50%);

    width: 53%;
    max-width: 995px;
    min-width: 600px;

    height: 112px;

    padding: 3px;

    background:
        linear-gradient(
            135deg,
            #f0fbff 0%,
            #7d9cac 8%,
            #dcecf4 16%,
            #254c63 29%,
            #092337 48%,
            #597f91 70%,
            #eaf8ff 86%,
            #617e8d 100%
        );

    border-radius: 17px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.58),
        0 0 22px rgba(0,160,245,.34);
}


/* INNER TITLE SURFACE */

.title-inner {
    position: relative;

    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: column;

    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            ellipse at 50% 25%,
            #174c6c 0%,
            #0b304b 38%,
            #041b2c 100%
        );

    border: 1px solid #67d4ff;

    border-radius: 13px;

    overflow: hidden;

    box-shadow:
        inset 0 3px 0 rgba(255,255,255,.22),
        inset 0 -10px 18px rgba(0,0,0,.30),
        0 0 15px rgba(28,183,242,.25);
}


/* TOP BLUE REFLECTION */

.title-inner::before {
    content: "";

    position: absolute;

    z-index: 1;

    left: 12%;
    right: 12%;
    top: 5px;

    height: 4px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(192,242,255,.95),
            rgba(73,202,248,1),
            rgba(192,242,255,.95),
            transparent
        );

    box-shadow:
        0 0 10px rgba(72,210,255,.90);
}


/* CENTRAL HIGHLIGHT */

.title-inner::after {
    content: "";

    position: absolute;

    z-index: 1;

    left: 38%;
    right: 38%;
    top: 0;

    height: 8px;

    background:
        radial-gradient(
            ellipse,
            rgba(128,228,255,.9),
            transparent 70%
        );

    filter: blur(2px);
}


/* =====================================================
   3D TITLE TEXT
   ===================================================== */

.title-text {
    position: relative;

    z-index: 5;

    display: flex;
    flex-direction: row;

    align-items: center;
    justify-content: center;
    gap: 12px;

    width: 100%;
    height: 100%;

    line-height: .88;
    white-space: nowrap;
    text-align: center;

    font-weight: 950;
    letter-spacing: 1px;
}


/* PROCESS */

.title-process {
    font-size: clamp(25px, 2.55vw, 43px);

    color: #ffffff;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #ffffff 40%,
            #f2fbff 65%,
            #d4f1ff 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* TECHNOLOGY */

.title-technology {
    margin-top: 4px;

    font-size: clamp(27px, 2.85vw, 48px);

    color: #35c6ff;

    color: #ffffff;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #ffffff 40%,
            #f2fbff 65%,
            #d4f1ff 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* PT GOLD */

.title-pt {
    color: #ffc31b;

    background:
        linear-gradient(
            180deg,
            #fff39a 0%,
            #ffc51c 38%,
            #f09b00 70%,
            #c66b00 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* =====================================================
   TITLE BOTTOM ACCENT
   ===================================================== */

.title-line {
    position: absolute;

    z-index: 6;

    left: 21%;
    right: 21%;
    bottom: 9px;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #22baf3 18%,
            #d3f7ff 50%,
            #22baf3 82%,
            transparent
        );

    box-shadow:
        0 0 8px rgba(44,195,250,.85);
}


/* =====================================================
   TITLE SIDE WINGS
   ===================================================== */

.title-wing {
    position: absolute;

    z-index: 19;

    top: 50%;

    width: 43px;
    height: 44px;

    transform: translateY(-50%);

    background:
        linear-gradient(
            135deg,
            #1a4862,
            #061d30
        );

    border-top: 1px solid #65d5ff;
    border-bottom: 1px solid #176b91;

    box-shadow:
        0 5px 10px rgba(0,0,0,.44);
}

.title-wing.left {
    left: 23.0%;

    clip-path:
        polygon(
            25% 0,
            100% 0,
            100% 100%,
            25% 100%,
            0 50%
        );
}

.title-wing.right {
    right: 23.0%;

    clip-path:
        polygon(
            0 0,
            75% 0,
            100% 50%,
            75% 100%,
            0 100%
        );
}


/* =====================================================
   TAGLINE
   ===================================================== */

.tagline {
    position: absolute;

    z-index: 27;

    left: 50%;
    bottom: 6px;

    transform: translateX(-50%);

    color: #a9ddec;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 2px;

    white-space: nowrap;
}


/* =====================================================
   RIGHT DATE/TIME PANEL
   — SAME WIDE RECTANGULAR PROPORTION AS LOGO
   ===================================================== */

.status-panel {
    position: absolute;

    z-index: 30;

    right: 2.6%;
    top: 50%;

    transform: translateY(-50%);

    width: 17.0%;
    max-width: 325px;
    min-width: 235px;

    height: 108px;

    padding: 8px 13px;

    background:
        linear-gradient(
            145deg,
            #123c55 0%,
            #08263b 45%,
            #031522 100%
        );

    border: 1px solid #55c7ee;

    border-radius: 14px;

    box-shadow:
        0 7px 15px rgba(0,0,0,.48),
        0 0 0 2px rgba(12,50,70,.92),
        inset 0 2px 0 rgba(255,255,255,.13),
        inset 0 -6px 12px rgba(0,0,0,.30);
}

.status-panel::before {
    content: "";

    position: absolute;

    inset: -4px;

    border-radius: 17px;

    border: 1px solid rgba(83,202,246,.62);

    pointer-events: none;
}

.status-panel::after {
    content: "";

    position: absolute;

    left: 12%;
    right: 12%;
    top: -3px;

    height: 3px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8fe8ff,
            transparent
        );

    box-shadow:
        0 0 8px rgba(71,204,250,.82);
}


/* ONLINE */

.status-top {
    height: 20px;

    display: flex;

    align-items: center;
    justify-content: center;

    gap: 8px;

    color: #a9ddec;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 1.2px;
}

.status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #2de57f;

    box-shadow:
        0 0 8px rgba(45,229,127,.95);
}


/* DIVIDER */

.status-divider {
    height: 1px;

    margin: 3px 8px 4px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #3cc2ed,
            transparent
        );
}


/* DATE/TIME ROW */

.status-row {
    height: 29px;

    display: flex;

    align-items: center;
    justify-content: flex-start;

    gap: 9px;

    padding-left: 16px;

    color: #ffffff;

    font-size: 15px;

    font-weight: 900;

    letter-spacing: .45px;

    font-variant-numeric: tabular-nums;
}

.status-row.time {
    color: #c4f2ff;
}

#current-date,
#current-time {
    text-align: left;
    font-variant-numeric: tabular-nums;
}

.status-icon {
    width: 18px;

    color: #20c3f7;

    font-size: 15px;

    text-align: center;
}

.status-label {
    width: 39px;

    color: #b9dfed;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: .25px;

    text-align: left;
}


/* =====================================================
   BOTTOM METALLIC RAIL
   ===================================================== */

.bottom-rail {
    position: absolute;

    z-index: 35;

    left: 0;
    right: 0;
    bottom: 0;

    height: 7px;

    background:
        linear-gradient(
            90deg,
            #063d64 0%,
            #1399d0 20%,
            #91e8ff 50%,
            #1399d0 80%,
            #063d64 100%
        );

    box-shadow:
        0 0 9px rgba(35,194,249,.90);
}

.bottom-rail::before,
.bottom-rail::after {
    content: "";

    position: absolute;

    top: 1px;

    width: 82px;
    height: 5px;

    background:
        repeating-linear-gradient(
            135deg,
            transparent 0 8px,
            rgba(255,255,255,.80) 8px 11px,
            transparent 11px 18px
        );
}

.bottom-rail::before {
    left: 18%;
}

.bottom-rail::after {
    right: 18%;
}


/* =====================================================
   RESPONSIVE
   ===================================================== */

@media (max-width: 1200px) {

    .logo-panel,
    .status-panel {
        width: 18%;
        min-width: 205px;
        height: 94px;
    }

    .title-frame {
        width: 49%;
        min-width: 500px;
        height: 100px;
    }

    .title-wing {
        display: none;
    }

    .tagline {
        font-size: 7px;
    }
}

@media (max-width: 900px) {

    .header {
        height: 125px;
        border-radius: 16px;
    }

    .industrial {
        height: 120px;
    }

    .logo-panel {
        left: 1.5%;
        width: 19%;
        min-width: 150px;
        height: 78px;
        border-radius: 11px;
    }

    .title-frame {
        width: 47%;
        min-width: 280px;
        height: 84px;
        border-radius: 12px;
    }

    .title-inner {
        border-radius: 9px;
    }

    .title-process {
        font-size: 21px;
    }

    .title-technology {
        font-size: 23px;
    }

    .status-panel {
        right: 1.5%;
        width: 19%;
        min-width: 150px;
        height: 78px;
        border-radius: 11px;
        padding: 5px 7px;
    }

    .status-row {
        font-size: 10px;
        height: 22px;
    }

    .status-top {
        font-size: 6px;
        height: 15px;
    }

    .tagline {
        display: none;
    }
}

</style>
</head>

<body>

<div class="header">

    <!-- INNER CURVED FRAME -->
    <div class="header-frame"></div>

    <!-- TOP GLOSS -->
    <div class="header-glow"></div>


    <!-- INDUSTRIAL BACKGROUND -->

    <svg
        class="industrial"
        viewBox="0 0 1672 145"
        preserveAspectRatio="none"
        aria-hidden="true">

        <!-- LEFT PLANT -->

        <g>

            <rect class="steel"
                  x="48" y="58"
                  width="22" height="82"
                  rx="3"/>

            <rect class="steel"
                  x="82" y="40"
                  width="34" height="100"
                  rx="5"/>

            <rect class="steel"
                  x="88" y="23"
                  width="22" height="19"/>

            <rect class="steel"
                  x="93" y="10"
                  width="12" height="15"/>

            <circle class="warm"
                    cx="99" cy="58" r="3"/>

            <circle class="warm"
                    cx="99" cy="81" r="3"/>

            <circle class="warm"
                    cx="99" cy="104" r="3"/>

            <path class="highlight"
                  d="
                    M99 10 V140
                    M84 62 H114
                    M84 86 H114
                    M84 110 H114
                  "/>

            <rect class="steel"
                  x="137" y="72"
                  width="52" height="68"
                  rx="25"/>

            <path class="highlight"
                  d="
                    M137 91 H189
                    M137 114 H189
                  "/>

            <circle class="glass"
                    cx="163" cy="102" r="5"/>

        </g>


        <!-- LEFT PIPING -->

        <g class="highlight">

            <path d="
                M0 121
                H310
                V92
                H395
            "/>

            <path d="
                M35 132
                H270
                V108
                H420
            "/>

            <path d="
                M170 77
                H285
                V52
                H380
            "/>

            <path d="
                M247 140
                V70
                H335
            "/>

        </g>


        <!-- RIGHT PLANT -->

        <g>

            <rect class="steel"
                  x="1430" y="57"
                  width="22" height="83"
                  rx="3"/>

            <rect class="steel"
                  x="1470" y="40"
                  width="34" height="100"
                  rx="5"/>

            <rect class="steel"
                  x="1476" y="23"
                  width="22" height="19"/>

            <rect class="steel"
                  x="1481" y="10"
                  width="12" height="15"/>

            <circle class="warm"
                    cx="1487" cy="58" r="3"/>

            <circle class="warm"
                    cx="1487" cy="81" r="3"/>

            <circle class="warm"
                    cx="1487" cy="104" r="3"/>

            <path class="highlight"
                  d="
                    M1487 10 V140
                    M1472 62 H1502
                    M1472 86 H1502
                    M1472 110 H1502
                  "/>

            <rect class="steel"
                  x="1533" y="72"
                  width="52" height="68"
                  rx="25"/>

            <path class="highlight"
                  d="
                    M1533 91 H1585
                    M1533 114 H1585
                  "/>

            <circle class="glass"
                    cx="1559" cy="102" r="5"/>

        </g>


        <!-- RIGHT PIPING -->

        <g class="highlight">

            <path d="
                M1672 121
                H1362
                V92
                H1277
            "/>

            <path d="
                M1637 132
                H1402
                V108
                H1252
            "/>

            <path d="
                M1502 77
                H1387
                V52
                H1292
            "/>

            <path d="
                M1425 140
                V70
                H1337
            "/>

        </g>


        <!-- TECHNICAL HEXAGONS -->

        <g class="tech">

            <path d="
                M270 25
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M309 58
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M1366 25
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M1405 58
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

        </g>

    </svg>


    <!-- LOGO -->

    <div class="logo-panel">

        <img
            class="header-logo"
            src="data:image/jpeg;base64,LOGO_BASE64"
            alt="JSW JFE Steel Limited"
        >

    </div>


    <!-- TITLE SIDE WINGS -->

    <div class="title-wing left"></div>
    <div class="title-wing right"></div>


    <!-- CENTRAL 3D TITLE -->

    <div class="title-frame">

        <div class="title-inner">

            <div class="title-text">

                <div class="title-process">
                    PROCESS
                </div>

                <div class="title-technology">
                     TRAINING
                    <span class="title-pt">(TRAINING)</span>
                </div>

            </div>

            <div class="title-line"></div>

        </div>

    </div>


    <!-- TAGLINE -->

    <div class="tagline">
        PROCESS SAFETY MANAGEMENT • DIGITAL OPERATIONS
    </div>


    <!-- RIGHT DATE / TIME PANEL -->

    <div class="status-panel">

        <div class="status-top">

            <span class="status-dot"></span>

            <span>SYSTEM ONLINE</span>

        </div>

        <div class="status-divider"></div>

        <div class="status-row">

            <span class="status-icon">▣</span>

            <span class="status-label">Date:</span>

            <span id="current-date">
                03.09.2026
            </span>

        </div>

        <div class="status-row time">

            <span class="status-icon">◷</span>

            <span class="status-label">Time:</span>

            <span id="current-time">
                00.00.00
            </span>

        </div>

    </div>


    <!-- BOTTOM RAIL -->

    <div class="bottom-rail"></div>

</div>


<script>

function updateDateTime() {

    const now = new Date();


    /* =================================================
       DATE — DD.MM.YYYY
       ================================================= */

    const dateParts = new Intl.DateTimeFormat(
        "en-GB",
        {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            timeZone: "Asia/Kolkata"
        }
    ).formatToParts(now);

    let day = "";
    let month = "";
    let year = "";

    dateParts.forEach(function(part) {

        if (part.type === "day") {
            day = part.value;
        }

        if (part.type === "month") {
            month = part.value;
        }

        if (part.type === "year") {
            year = part.value;
        }

    });

    document.getElementById("current-date").textContent =
        day + "." + month + "." + year;


    /* =================================================
       TIME — HH.MM.SS AM/PM
       ================================================= */

    const timeParts = new Intl.DateTimeFormat(
        "en-GB",
        {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,
            timeZone: "Asia/Kolkata"
        }
    ).formatToParts(now);

    let hour = "";
    let minute = "";
    let second = "";
    let dayPeriod = "";

    timeParts.forEach(function(part) {

        if (part.type === "hour") {
            hour = part.value;
        }

        if (part.type === "minute") {
            minute = part.value;
        }

        if (part.type === "second") {
            second = part.value;
        }

        if (part.type === "dayPeriod") {
            dayPeriod = part.value.toUpperCase();
        }

    });

    document.getElementById("current-time").textContent =
        hour + "." + minute + "." + second + " " + dayPeriod;
}


updateDateTime();

setInterval(
    updateDateTime,
    1000
);

</script>

</body>
</html>
"""

header_html = header_html.replace(
    "LOGO_BASE64",
    logo_base64
)

components.html(
    header_html,
    height=160,
    scrolling=False
)

# =========================================================
# FILTERS
# =========================================================

filter_month, filter_department = st.columns(
    [1, 1],
    gap="small"
)


# =========================================================
# MONTH FILTER
# =========================================================

with filter_month:

    st.markdown(
        "<div class='filter-title'>MONTH</div>",
        unsafe_allow_html=True
    )


    if COL_MONTH:

        valid_dates = (
            work["_date"]
            .dropna()
        )


        if not valid_dates.empty:

            month_periods = (
                valid_dates
                .dt
                .to_period("M")
                .drop_duplicates()
                .sort_values(
                    ascending=False
                )
            )


            month_labels = [

                period.strftime(
                    "%B %Y"
                )

                for period
                in month_periods

            ]

        else:

            month_labels = []

    else:

        month_labels = []


    month_options = [
        "All Months"
    ] + month_labels


    selected_month = st.selectbox(

        "Month",

        month_options,

        index=0,

        key="month_selector",

        label_visibility="collapsed"

    )


# =========================================================
# DEPARTMENT FILTER
# =========================================================

with filter_department:

    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )


    department_values = sorted(

        [

            value

            for value
            in work["_department"]
            .unique()
            .tolist()

            if str(value).strip()

        ],

        key=lambda x:
        str(x).lower()

    )


    department_options = [
        "All Departments"
    ] + department_values


    selected_department = st.selectbox(

        "Department",

        department_options,

        index=0,

        key="department_selector",

        label_visibility="collapsed"

    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = work.copy()


# =========================================================
# DEPARTMENT FILTER
# =========================================================

if (
    selected_department
    !=
    "All Departments"
):

    filtered_df = filtered_df[
        filtered_df["_department"]
        ==
        selected_department
    ]


# =========================================================
# MONTH FILTER
# =========================================================

if (
    selected_month
    !=
    "All Months"
    and
    COL_MONTH
):

    selected_period = pd.Period(

        pd.to_datetime(
            selected_month,
            format="%B %Y"
        ),

        freq="M"

    )


    filtered_df = filtered_df[

        filtered_df["_date"]
        .dt
        .to_period("M")
        ==
        selected_period

    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_l08 = (
    filtered_df["_total_l08"].sum()
)

total_below_l08 = (
    filtered_df["_total_below_l08"].sum()
)

total_associates = (
    filtered_df["_total_associates"].sum()
)

total_contractual = (
    filtered_df["_total_contractual"].sum()
)


completed_l08 = (
    filtered_df["_completed_l08"].sum()
)

completed_below_l08 = (
    filtered_df["_completed_below_l08"].sum()
)

completed_associates = (
    filtered_df["_completed_associates"].sum()
)

completed_contractual = (
    filtered_df["_completed_contractual"].sum()
)


# =========================================================
# OVERALL EMPLOYEE COMPLETION
# =========================================================

total_employees = (

    total_l08
    +
    total_below_l08

)


completed_employees = (

    completed_l08
    +
    completed_below_l08

)


if total_employees > 0:

    overall_pct = (

        completed_employees
        /
        total_employees
        *
        100

    )

else:

    overall_pct = 0


# =========================================================
# ASSOCIATES COMPLETION
# =========================================================

if total_associates > 0:

    associate_pct = (

        completed_associates
        /
        total_associates
        *
        100

    )

else:

    associate_pct = 0


# =========================================================
# CONTRACTUAL COMPLETION
# =========================================================

if total_contractual > 0:

    contractual_pct = (

        completed_contractual
        /
        total_contractual
        *
        100

    )

else:

    contractual_pct = 0


# =========================================================
# L08 COMPLETION
# =========================================================

if total_l08 > 0:

    l08_pct = (

        completed_l08
        /
        total_l08
        *
        100

    )

else:

    l08_pct = 0


# =========================================================
# BELOW L08 COMPLETION
# =========================================================

if total_below_l08 > 0:

    below_l08_pct = (

        completed_below_l08
        /
        total_below_l08
        *
        100

    )

else:

    below_l08_pct = 0


# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4, k5, k6 = st.columns(

    [1.05, 1, 1.05, 1, 1, 1],

    gap="small"

)


# =========================================================
# KPI 1
# =========================================================

with k1:

    radius = 42

    circumference = (
        2
        *
        3.14159
        *
        radius
    )

    dash = (

        circumference
        *
        min(
            max(
                overall_pct,
                0
            ),
            100
        )
        /
        100

    )


    st.html(

        f"""
        <div class="donut-card">

            <div class="donut-title">
                OVERALL TRAINING COMPLETION
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
                            {dash:.1f}
                            {circumference:.1f}
                        "
                    />

                </svg>

                <div class="donut-text">

                    {overall_pct:.1f}%

                </div>

            </div>

            <div class="donut-bottom">

                Overall % Trained

            </div>

        </div>
        """

    )


# =========================================================
# KPI 2
# =========================================================

with k2:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:18px;"
            >

                {total_associates:,.0f}

            </div>

            <div class="kpi-sub">

                Trained:
                {completed_associates:,.0f}

                ({associate_pct:.1f}%)

            </div>

        </div>
        """

    )


# =========================================================
# KPI 3
# =========================================================

with k3:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL CONTRACTUAL
                WORKERS TRAINED

            </div>

            <div
                class="kpi-value red"
                style="margin-top:18px;"
            >

                {total_contractual:,.0f}

            </div>

            <div class="kpi-sub">

                Trained:
                {completed_contractual:,.0f}

                ({contractual_pct:.1f}%)

            </div>

        </div>
        """

    )


# =========================================================
# KPI 4
# =========================================================

with k4:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

                <br>

                (L08 & ABOVE)

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:15px;"
            >

                {l08_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# KPI 5
# =========================================================

with k5:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

                <br>

                (BELOW L08)

            </div>

            <div
                class="kpi-value red"
                style="margin-top:15px;"
            >

                {below_l08_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# KPI 6
# =========================================================

with k6:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                OVERALL TRAINING

                <br>

                COMPLETION

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:15px;"
            >

                {overall_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# PROCESS DATA
# =========================================================

process_data = (

    filtered_df

    .groupby(
        "_process",
        sort=False
    )

    .agg(

        total_l08=(
            "_total_l08",
            "sum"
        ),

        total_below_l08=(
            "_total_below_l08",
            "sum"
        ),

        completed_l08=(
            "_completed_l08",
            "sum"
        ),

        completed_below_l08=(
            "_completed_below_l08",
            "sum"
        )

    )

)


if not process_data.empty:

    process_data["total"] = (

        process_data["total_l08"]
        +
        process_data["total_below_l08"]

    )


    process_data["completed"] = (

        process_data["completed_l08"]
        +
        process_data["completed_below_l08"]

    )


    process_data["percentage"] = (

        process_data.apply(

            lambda row:

                (
                    row["completed"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else 0,

            axis=1

        )

    )


    process_data = (

        process_data

        .sort_values(
            "percentage",
            ascending=False
        )

    )


# =========================================================
# DEPARTMENT DATA
# =========================================================

department_data = (

    filtered_df

    .groupby(
        "_department",
        sort=False
    )

    .agg(

        total_l08=(
            "_total_l08",
            "sum"
        ),

        total_below_l08=(
            "_total_below_l08",
            "sum"
        ),

        completed_l08=(
            "_completed_l08",
            "sum"
        ),

        completed_below_l08=(
            "_completed_below_l08",
            "sum"
        )

    )

)


if not department_data.empty:

    department_data["total"] = (

        department_data["total_l08"]
        +
        department_data["total_below_l08"]

    )


    department_data["completed"] = (

        department_data["completed_l08"]
        +
        department_data["completed_below_l08"]

    )


    department_data["percentage"] = (

        department_data.apply(

            lambda row:

                (
                    row["completed"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else 0,

            axis=1

        )

    )


    department_data = (

        department_data

        .sort_values(
            "percentage",
            ascending=True
        )

    )


# =========================================================
# CHART ROW
# =========================================================

chart_left, chart_right = st.columns(

    [1, 1.08],

    gap="small"

)


# =========================================================
# PROCESS CHART
# =========================================================

with chart_left:

    st.html(

        """
        <div class="chart-panel">

            <div class="chart-panel-title">

                TRAINING COMPLETION BY PROCESS
                (PLANT WIDE)

            </div>

            <div>

        """

    )


    fig_process = go.Figure()


    if not process_data.empty:

        fig_process.add_trace(

            go.Bar(

                x=process_data.index.tolist(),

                y=process_data[
                    "percentage"
                ].tolist(),

                text=[

                    f"{value:.1f}%"

                    for value
                    in process_data[
                        "percentage"
                    ]

                ],

                textposition="outside",

                cliponaxis=False,

                marker=dict(

                    color="#2b66a8",

                    line=dict(

                        color="#164f8b",

                        width=1.2

                    )

                ),

                hovertemplate=

                    "%{x}<br>"
                    "Completion: "
                    "%{y:.1f}%"
                    "<extra></extra>"

            )

        )


    fig_process.update_layout(

        height=300,

        margin=dict(

            l=50,

            r=30,

            t=25,

            b=55

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial",

            color="#111111"

        ),

        yaxis=dict(

            range=[
                0,
                100
            ],

            dtick=25,

            title="Completion %",

            title_font=dict(
                size=12
            ),

            tickfont=dict(
                size=10
            ),

            gridcolor="#d2e4ed",

            gridwidth=1,

            zeroline=False,

            showline=False

        ),

        xaxis=dict(

            tickfont=dict(
                size=10
            ),

            showgrid=False,

            showline=False,

            zeroline=False

        ),

        showlegend=False,

        bargap=.30

    )


    st.plotly_chart(

        fig_process,

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
# DEPARTMENT CHART
# =========================================================

with chart_right:

    st.html(

        """
        <div class="chart-panel">

            <div class="chart-panel-title">

                TRAINING COMPLETION BY DEPARTMENT
                (OVERALL %)

            </div>

            <div>

        """

    )


    fig_department = go.Figure()


    if not department_data.empty:

        fig_department.add_trace(

            go.Bar(

                x=department_data[
                    "percentage"
                ].tolist(),

                y=department_data.index.tolist(),

                orientation="h",

                text=[

                    f"{value:.1f}%"

                    for value
                    in department_data[
                        "percentage"
                    ]

                ],

                textposition="outside",

                cliponaxis=False,

                marker=dict(

                    color="#2b66a8",

                    line=dict(

                        color="#164f8b",

                        width=1.2

                    )

                ),

                hovertemplate=

                    "%{y}<br>"
                    "Completion: "
                    "%{x:.1f}%"
                    "<extra></extra>"

            )

        )


    fig_department.update_layout(

        height=300,

        margin=dict(

            l=95,

            r=55,

            t=25,

            b=50

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial",

            color="#111111"

        ),

        xaxis=dict(

            range=[
                0,
                100
            ],

            dtick=20,

            title="Overall Completion %",

            title_font=dict(
                size=12
            ),

            tickfont=dict(
                size=10
            ),

            gridcolor="#d2e4ed",

            gridwidth=1,

            zeroline=False,

            showline=False

        ),

        yaxis=dict(

            tickfont=dict(
                size=10
            ),

            showgrid=False,

            showline=False,

            zeroline=False

        ),

        showlegend=False,

        bargap=.25

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
# PROCESS-WISE TABLE
# =========================================================

st.html(

    """
    <div
        class="panel"
        style="margin-top:6px;"
    >

        <div class="panel-title">

            PROCESS WISE TRAINING COMPLETION
            BY DEPARTMENT (%)

        </div>

        <div style="
            padding:6px;
            overflow-x:auto;
        ">

    """

)


if not filtered_df.empty:

    pivot_source = (

        filtered_df

        .groupby(
            [
                "_process",
                "_department"
            ],

            sort=False

        )

        .agg(

            total_l08=(
                "_total_l08",
                "sum"
            ),

            total_below_l08=(
                "_total_below_l08",
                "sum"
            ),

            completed_l08=(
                "_completed_l08",
                "sum"
            ),

            completed_below_l08=(
                "_completed_below_l08",
                "sum"
            )

        )

    )


    pivot_source["total"] = (

        pivot_source["total_l08"]
        +
        pivot_source["total_below_l08"]

    )


    pivot_source["completed"] = (

        pivot_source["completed_l08"]
        +
        pivot_source["completed_below_l08"]

    )


    pivot_source["percentage"] = (

        pivot_source.apply(

            lambda row:

                (
                    row["completed"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else 0,

            axis=1

        )

    )


    pivot_source = (
        pivot_source
        .reset_index()
    )


    table_data = pivot_source.pivot(

        index="_process",

        columns="_department",

        values="percentage"

    )


    table_data = (
        table_data
        .fillna(0)
    )


    # =====================================================
    # OVERALL PROCESS %
    # =====================================================

    overall_process = (

        filtered_df

        .groupby(
            "_process",
            sort=False
        )

        .agg(

            total_l08=(
                "_total_l08",
                "sum"
            ),

            total_below_l08=(
                "_total_below_l08",
                "sum"
            ),

            completed_l08=(
                "_completed_l08",
                "sum"
            ),

            completed_below_l08=(
                "_completed_below_l08",
                "sum"
            )

        )

    )


    overall_process["total"] = (

        overall_process["total_l08"]
        +
        overall_process["total_below_l08"]

    )


    overall_process["completed"] = (

        overall_process["completed_l08"]
        +
        overall_process["completed_below_l08"]

    )


    overall_process["Overall"] = (

        overall_process.apply(

            lambda row:

                (
                    row["completed"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else 0,

            axis=1

        )

    )


    table_data["Overall"] = (
        overall_process["Overall"]
    )


    # =====================================================
    # DEPARTMENT ORDER
    # =====================================================

    preferred_departments = [

        "Blast Furnace-1",
        "Blast Furnace-2",
        "SMS-1",
        "SMS-2",
        "SMS",
        "PSM GA",
        "Coke Oven",
        "Power Plant",
        "Utilities",
        "Lime Plant",
        "Others"

    ]


    existing_columns = (
        table_data.columns.tolist()
    )


    ordered_departments = [

        value

        for value
        in preferred_departments

        if value
        in existing_columns

    ]


    remaining_departments = [

        value

        for value
        in existing_columns

        if value
        not in ordered_departments

        and value != "Overall"

    ]


    ordered_departments += sorted(

        remaining_departments,

        key=lambda x:
        str(x).lower()

    )


    if "Overall" in table_data.columns:

        ordered_departments.append(
            "Overall"
        )


    table_data = table_data[
        ordered_departments
    ]


    # =====================================================
    # BUILD HTML TABLE
    # =====================================================

    html = """

    <table class="training-table">

        <thead>

            <tr>

                <th>
                    Process
                </th>

    """


    for col in table_data.columns:

        html += f"""

                <th>
                    {col}
                </th>

        """


    html += """

            </tr>

        </thead>

        <tbody>

    """


    for process_name, row in (
        table_data.iterrows()
    ):

        html += f"""

            <tr>

                <td>
                    {process_name}
                </td>

        """


        for col in table_data.columns:

            value = row[col]


            if pd.isna(value):

                value = 0


            extra_class = (

                "overall"

                if col == "Overall"

                else ""

            )


            html += f"""

                <td class="{extra_class}">

                    {value:.1f}%

                </td>

            """


        html += """

            </tr>

        """


    html += """

        </tbody>

    </table>

    """


    st.html(
        html
    )


else:

    st.info(
        "Process-wise training data is not available."
    )


st.html(

    """
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

        📚 &nbsp;

        © 2026 Training Dashboard

        &nbsp; | &nbsp;

        Training

    </div>
    """

)

