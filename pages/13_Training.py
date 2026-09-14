import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import re
import os
import base64
from pathlib import Path
from datetime import datetime
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

/* =========================================================
   MONTH & DEPARTMENT - WHITE SHINY 3D FILTER BOX
   ========================================================= */

[data-testid="stSelectbox"] {
    margin-bottom:8px !important;
    padding:0 !important;
}

/* Main outer box */
[data-testid="stSelectbox"] > div > div {
    min-height:44px !important;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 35%,
            #f8fbfd 65%,
            #eaf3f8 100%
        ) !important;

    border:1px solid #c7d8e2 !important;
    border-radius:12px !important;

    box-shadow:
        0 8px 18px rgba(55,90,110,0.16),
        0 3px 6px rgba(55,90,110,0.10),
        inset 0 2px 0 rgba(255,255,255,0.98),
        inset 0 -5px 10px rgba(180,205,218,0.16) !important;

    transition:all 0.2s ease-in-out !important;
}

/* Select area */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    min-height:44px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #fbfdfe 45%,
            #eef6fa 100%
        ) !important;

    border:0 !important;
    border-radius:11px !important;
}

/* Text */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    font-family:Arial,sans-serif !important;
    font-size:13px !important;
    font-weight:800 !important;
    color:#193d77 !important;
}

/* Input text */
[data-testid="stSelectbox"] input {
    font-size:13px !important;
    font-weight:800 !important;
    color:#193d77 !important;
}

/* Dropdown arrow */
[data-testid="stSelectbox"] svg {
    color:#193d77 !important;
}

/* Hover - raised 3D effect */
[data-testid="stSelectbox"] > div > div:hover {
    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 45%,
            #eef7fb 100%
        ) !important;

    border-color:#a9c4d4 !important;

    box-shadow:
        0 11px 24px rgba(55,90,110,0.20),
        0 4px 8px rgba(55,90,110,0.12),
        inset 0 2px 0 #ffffff,
        inset 0 -6px 12px rgba(175,202,215,0.18) !important;

    transform:translateY(-1px) !important;
}

/* Focus */
[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
    border:1px solid #9dbdce !important;

    box-shadow:
        0 8px 18px rgba(55,90,110,0.16),
        inset 0 2px 0 #ffffff,
        inset 0 -5px 10px rgba(175,202,215,0.15) !important;
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

    display:none !important;

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

    font-size:39px;

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
            #ffffff 0%,
            #eef7fb 100%
        );

    border-bottom:1px solid #dce7ec;

}


/* =========================================================
   TABLE
   ========================================================= */

.training-table {

    width:100%;

    border-collapse:collapse;

    border:1px solid #cbdde6;

    font-family:Arial,sans-serif;

    font-size:10px;

}


.training-table th {

    background:#193d77;

    color:#ffffff;

    font-weight:900;

    padding:7px 8px;

    border:1px solid #9fb8c8;

    text-align:center;

}


.training-table th:first-child {

    text-align:left;

}


.training-table td {

    padding:6px 8px;

    text-align:center;

    border:1px solid #cbdde6;

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


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PSM Digital Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# REMOVE STREAMLIT TOP SPACE
# ============================================================

st.markdown(
    """
    <style>

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }

    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    iframe {
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
    }

    /* Control the Streamlit element that contains the header iframe */
    div[data-testid="stElementContainer"]:has(iframe) {
        margin-top: -25px !important;
        margin-bottom: -8px !important;
        padding: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

#=============================================================
#HEADER CODE
#=============================================================
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PSM Digital Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# REMOVE STREAMLIT TOP SPACE
# ============================================================

st.markdown(
    """
    <style>

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
    padding-top: 0 !important;
    margin-top: -15px !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    iframe {
        display: block !important;
        margin-top: -20px !important;
        padding-top: 0 !important;
        border: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# IMAGE TO BASE64
# ============================================================

def image_to_base64(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        return ""

    try:

        with open(file_path, "rb") as file:

            return base64.b64encode(
                file.read()
            ).decode("utf-8")

    except Exception:

        return ""


# ============================================================
# COMPANY LOGO
# ============================================================

logo_path = BASE_DIR / "jsw_jfe_logo.jpg"

logo_base64 = image_to_base64(logo_path)


# ============================================================
# FILE CHECK
# ============================================================

if not logo_base64:

    st.error(
        "jsw_jfe_logo.jpg not found. "
        "Keep jsw_jfe_logo.jpg in the same folder as this Python file."
    )


# ============================================================
# DATE AND TIME
# ============================================================

now = datetime.now()

current_date = now.strftime(
    "%d %b %Y"
).upper()

current_time = now.strftime(
    "%I:%M %p"
)


# ============================================================
# HEADER HTML
# ============================================================

header_html = """

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>


/* ============================================================
   MAIN HEADER
   ============================================================ */

.psm-header {

    position: relative;

    width: 100%;

    height: 90px;

    overflow: hidden;

    background:
        linear-gradient(
            90deg,
            #031d34 0%,
            #052b49 42%,
            #07385c 74%,
            #052b49 100%
        );

    border-radius: 7px;

    box-shadow:
        0 3px 9px
        rgba(0,0,0,0.18);

}


/* ============================================================
   LEFT LOGO AREA
   ============================================================ */

.psm-left {

    position: absolute;

    left: 0;

    top: 0;

    width: 100%;

    height: 95px;

    display: flex;

    align-items: center;

    padding-left: 4px;

    box-sizing: border-box;

    z-index: 20;

    pointer-events: none;

}


/* ============================================================
   LOGO PANEL
   ONLY VERTICAL POSITION CHANGED
   ============================================================ */

.logo-panel {

    width: 195px;

    height: 68px;

    background: #ffffff;

    border-radius: 5px;

    padding: 10px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    box-sizing: border-box;

    box-shadow:
        0 3px 9px
        rgba(0,0,0,0.20);

    position: relative;

    top: -5px;

    left: 5px;

}


/* ============================================================
   COMPANY LOGO
   ============================================================ */

.company-logo {

    width: 100%;

    height: 100%;

    object-fit: contain;

    object-position: center;

    display: block;

}


/* ============================================================
   LEFT VERTICAL DIVIDER
   ============================================================ */

.vertical-line {

    width: 2px;

    height: 83px;

    background:
        rgba(255,255,255,0.65);

    margin-left: 18px;

    margin-right: 20px;

    flex-shrink: 0;

}


/* ============================================================
   CENTER TITLE AREA
   ============================================================ */

.title-area {

    position: absolute;

    left: 50%;

    top: 0;

    height: 95px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    min-width: max-content;

    box-sizing: border-box;

    transform: translateX(-50%);

}


/* ============================================================
   MAIN TITLE
   ============================================================ */

.main-title {

    color: #ffffff;

    font-family:
        "Arial Narrow",
        "Roboto Condensed",
        Arial,
        sans-serif;

    font-size: 27px;

    font-weight: 900;

    line-height: 1;

    letter-spacing: 0.3px;

    white-space: nowrap;

    margin: 0;

    padding: 0;

}


/* ============================================================
   ORANGE TITLE PART
   ============================================================ */

.main-title-orange {

    color: #f28c00;

}


/* ============================================================
   SUBTITLE
   ============================================================ */

.subtitle {

    color: #ffffff;

    font-family:
        Arial,
        sans-serif;

    font-size: 12px;

    font-weight: 400;

    letter-spacing: 3.6px;

    margin-top: 8px;

    line-height: 1;

    white-space: nowrap;

}


/* ============================================================
   SUB-SUBTITLE / TAGLINE
   ============================================================ */

.tagline {

    color:
        rgba(255,255,255,0.82);

    font-family:
        Arial,
        sans-serif;

    font-size: 7px;

    font-weight: 500;

    letter-spacing: 2.2px;

    margin-top: 6px;

    line-height: 1;

    white-space: nowrap;

}


/* ============================================================
   RIGHT DATE / TIME AREA
   ============================================================ */

.psm-right {

    position: absolute;

    right: 16px;

    top: 0;

    width: 15%;

    height: 95px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: flex-end;

    text-align: right;

    color: #ffffff;

    z-index: 30;

    padding-left: 18px;

    box-sizing: border-box;

}


/* ============================================================
   RIGHT VERTICAL DIVIDER
   ============================================================ */

.psm-right::before {

    content: "";

    position: absolute;

    left: 0;

    top: 6px;

    width: 2px;

    height: 83px;

    background:
        rgba(255,255,255,0.65);

}


/* ============================================================
   DATE
   ============================================================ */

.date {

    color:
        rgba(255,255,255,0.95);

    font-family:
        Arial,
        sans-serif;

    font-size: 11px;

    font-weight: 400;

    letter-spacing: 0.7px;

    line-height: 1;

    margin: 0;

    padding: 0;

}


/* ============================================================
   TIME
   ============================================================ */

.time {

    color: #ffffff;

    font-family:
        "Arial Narrow",
        "Roboto Condensed",
        Arial,
        sans-serif;

    font-size: 22px;

    font-weight: 800;

    margin-top: 4px;

    line-height: 1;

    padding: 0;

}


/* ============================================================
   RIGHT HORIZONTAL LINE
   ============================================================ */

.right-line {

    width: 80px;

    height: 2px;

    background:
        rgba(255,255,255,0.75);

    margin-top: 7px;

    flex-shrink: 0;

}


/* ============================================================
   ORANGE BOTTOM BAR
   ============================================================ */

.orange-bar {

    position: absolute;

    left: 0;

    bottom: 0;

    width: 100%;

    height: 9px;

    background: #f28c00;

    z-index: 50;

}


</style>

</head>


<body>


<!-- ============================================================
     MAIN HEADER
     ============================================================ -->

<div class="psm-header">


    <!-- ========================================================
         LEFT LOGO AREA
         ======================================================== -->

    <div class="psm-left">


        <!-- ====================================================
             LOGO
             ==================================================== -->

        <div class="logo-panel">

            <img
                class="company-logo"
                src="data:image/jpeg;base64,LOGO_IMAGE_BASE64"
                alt="JSW JFE Steel Limited"
            >

        </div>


        <!-- ====================================================
             LEFT VERTICAL LINE
             ==================================================== -->

        <div class="vertical-line"></div>


        <!-- ====================================================
             CENTER TITLE GROUP
             ==================================================== -->

        <div class="title-area">


            <!-- MAIN TITLE -->

            <div class="main-title">

                TRAINING & COMPETENCY

                <span class="main-title-orange"></span>

            </div>


            <!-- SUBTITLE -->

            <div class="subtitle">

                PSM DIGITAL DASHBOARD

            </div>


            <!-- SUB-SUBTITLE -->

            <div class="tagline">

                PEOPLE
                &nbsp; | &nbsp;
                PROCESS
                &nbsp; | &nbsp;
                RISK
                &nbsp; | &nbsp;
                COMPLIANCE

            </div>


        </div>


    </div>


    <!-- ========================================================
         RIGHT DATE / TIME
         ======================================================== -->

    <div class="psm-right">


        <div class="date">

            CURRENT_DATE_VALUE

        </div>


        <div class="time">

            CURRENT_TIME_VALUE

        </div>


        <div class="right-line"></div>


    </div>


    <!-- ========================================================
         ORANGE BOTTOM BAR
         ======================================================== -->

    <div class="orange-bar"></div>


</div>


</body>

</html>

"""


# ============================================================
# INSERT LOGO
# ============================================================

header_html = header_html.replace(
    "LOGO_IMAGE_BASE64",
    logo_base64
)


# ============================================================
# INSERT DATE
# ============================================================

header_html = header_html.replace(
    "CURRENT_DATE_VALUE",
    current_date
)


# ============================================================
# INSERT TIME
# ============================================================

header_html = header_html.replace(
    "CURRENT_TIME_VALUE",
    current_time
)


# ============================================================
# DISPLAY HEADER
# ============================================================

components.html(
    header_html,
    height=114,
    scrolling=False
)

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] > div:has(> iframe) {
        margin-bottom: -65px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
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

                {completed_l08:,.0f}

            </div>

            <div class="kpi-sub">

                Actual trained employees

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

                {completed_below_l08:,.0f}

            </div>

            <div class="kpi-sub">

                Actual trained employees

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

                {completed_employees:,.0f}

            </div>

            <div class="kpi-sub">

                Actual trained employees

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

                    color=[
                        "#1677C8",
                        "#28B889",
                        "#F7931E",
                        "#E84A4A",
                        "#6D4CCB",
                        "#D14BB3",
                        "#22A6BE",
                        "#F2B400",
                        "#6E7FD1"
                    ][:len(process_data)],

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

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(238,247,251,0.72)",

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

            gridcolor="#b9d8e8",

            gridwidth=1,

            griddash="dot",

            zeroline=False,

            showline=True,

            linecolor="#9dbdce",

            linewidth=1

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

                    color=[
                        "#0B3D91" if str(dept).strip().lower() == "tube mill"
                        else [
                            "#1677C8",
                            "#28B889",
                            "#F7931E",
                            "#E84A4A",
                            "#6D4CCB",
                            "#D14BB3",
                            "#22A6BE",
                            "#F2B400",
                            "#1677C8",
                            "#28B889",
                            "#F7931E",
                            "#6D4CCB",
                            "#8A63D2"
                        ][i % 13]
                        for i, dept in enumerate(department_data.index)
                    ],

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

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(238,247,251,0.72)",

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

            gridcolor="#b9d8e8",

            gridwidth=1,

            griddash="dot",

            zeroline=False,

            showline=True,

            linecolor="#9dbdce",

            linewidth=1

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