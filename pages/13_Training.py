import io
import re
import html
import time
from urllib.parse import quote

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Training Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# ============================================================
# STYLE
# ============================================================
st.markdown(
    """
    <style>

    .stApp {
        background:#f3f8fc;
    }

    #MainMenu, footer {
        visibility:hidden;
    }



.block-container {
    padding:0rem 0.35rem 0rem 0.35rem !important;
    margin-top:-35px !important;
    margin-bottom:0px !important;
    max-width:100%;
}

/* REMOVE BOTTOM SPACE */
[data-testid="stAppViewContainer"] {
    padding-bottom:0px !important;
}

[data-testid="stMainBlockContainer"] {
    padding-bottom:0px !important;
    margin-bottom:0px !important;
}

section.main {
    padding-bottom:0px !important;
    margin-bottom:0px !important;
}

   div[data-testid="stMetric"] {
    background:#ffffff;
    border:1px solid #cbddea;
    border-radius:7px;
    padding:6px 6px !important;
    min-height:72px;
    overflow:visible !important;
}

    div[data-testid="stMetricLabel"] {
    font-size:9px !important;
    font-weight:800 !important;
    color:#20384f !important;
    white-space:nowrap !important;
    overflow:visible !important;
    text-overflow:clip !important;
    line-height:1.1 !important;
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] > div,
div[data-testid="stMetricLabel"] p {
    overflow:visible !important;
    text-overflow:clip !important;
    white-space:nowrap !important;
    max-width:none !important;
}

div[data-testid="stMetricLabel"] p {
    margin:0 !important;
    padding:0 !important;
    font-size:8px !important;
    line-height:1.1 !important;
}
    div[data-testid="stMetricValue"] {
        color:#123f77 !important;
        font-size:24px !important;
        font-weight:900 !important;
    }

    .module-card {
        background:#ffffff;
        border:1px solid #d3e0ea;
        border-radius:7px;
        padding:7px;
        margin-bottom:8px;
        box-shadow:0 1px 4px rgba(20,65,95,.06);
    }

    .module-title {
        color:#073f78;
        font-size:12px;
        font-weight:900;
        margin-bottom:6px;
    }

    .section-bar {
        background:#07518b;
        color:#ffffff;
        border-radius:4px;
        padding:6px 8px;
        font-size:10px;
        font-weight:900;
        margin:4px 0 6px 0;
    }

    .live-bar {
        background:#ffffff;
        border:1px solid #cbddea;
        border-radius:4px;
        padding:5px 8px;
        color:#4f6678;
        font-size:10px;
        margin-bottom:6px;
    }

    .footer {
        text-align:center;
        color:#627689;
        background:#edf4f8;
        border-top:1px solid #cbdce7;
        padding:7px;
        font-size:10px;
        font-weight:800;
        margin-top:8px;
    }

    .small-note {
        font-size:9px;
        color:#6c7f8f;
    }

    .stDataFrame {
        border:1px solid #d5e0e8;
    }


/* ========================================================
   REFRESH BUTTON — KEEP BELOW HEADER
   ======================================================== */

div[data-testid="stButton"] {
    margin-top: 1px !important;
    margin-bottom: 1px !important;
}



    /* ========================================================
       MATCH CLICKABLE MODULE HEADINGS WITH NORMAL HEADINGS
       ======================================================== */
    [data-testid="stPageLink"] {
        margin-bottom:0px !important;
    }

    [data-testid="stPageLink"],
    [data-testid="stPageLink"] a,
    [data-testid="stPageLink"] a *,
    [data-testid="stPageLink"] p,
    [data-testid="stPageLink"] span,
    [data-testid="stPageLink"] div {
        color:#073f78 !important;
        font-size:12px !important;
        font-weight:900 !important;
        text-decoration:none !important;
    }

    [data-testid="stPageLink"] a:hover,
    [data-testid="stPageLink"] a:hover * {
        color:#073f78 !important;
        text-decoration:none !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

#=============================================================
#HEADER CODE
#=============================================================
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


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



    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
    padding-top: 0 !important;
    margin-top: -30px !important;
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

now = datetime.now(ZoneInfo("Asia/Kolkata"))

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

                TRAINING 

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
    height=100,
    scrolling=False
)
st.markdown(
    """
    <style>
    /* REMOVE SPACE BELOW HEADER IFRAME */
    div[data-testid="stVerticalBlock"] > div:has(> iframe) {
        margin-bottom: -35px !important;
        padding-bottom: 0px !important;
    }

    /* REMOVE TOP SPACE BEFORE FILTER ROW */
    .top-filter-row {
        margin-top: -20px !important;
        padding-top: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] > div:has(> iframe) {
    margin-bottom: 0px !important;
}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
TRAINING_SHEET_NAME = "TRAINING"

# The TRAINING tab is a wide-format sheet:
# one row = Department + Process/Module,
# with separate Total and Completed Training columns for
# L08 & Above, Below L08, Associates and Contractual Workers.

TRAINING_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet="
    f"{quote(TRAINING_SHEET_NAME)}"
)

# ============================================================
# AUTO REFRESH
# ============================================================
# The page reloads every 30 seconds. The CSV request also receives
# a timestamp so the dashboard does not keep an old Google response.
components.html(
    """ 
    <script> 
        setTimeout(function () { 
            window.parent.location.reload(); 
        }, 30000); 
    </script> 
    """,
    height=0,
)


# ============================================================
# LOAD GOOGLE SHEET - NO STREAMLIT DATA CACHE
# ============================================================
def load_training_data():
    cache_buster = int(time.time())
    url = f"{TRAINING_CSV_URL}&_refresh={cache_buster}"

    response = requests.get(
        url,
        timeout=20,
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0",
        },
    )
    response.raise_for_status()

    data = pd.read_csv(
        io.BytesIO(response.content)
    )

    # Clean column names.
    data.columns = (
        data.columns
        .astype(str)
        .str.replace("\xa0", " ", regex=False)
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

    # Clean text cells.
    for col in data.columns:
        if data[col].dtype == "object":
            data[col] = (
                data[col]
                .astype(str)
                .str.replace("\xa0", " ", regex=False)
                .str.replace("\n", " ", regex=False)
                .str.strip()
            )

    return data.replace(
        {
            "nan": "",
            "NaN": "",
            "NAN": "",
            "None": "",
            "none": "",
        }
    )


try:
    df = load_training_data()
except Exception as exc:
    st.error(
        f"Unable to load Google Sheet tab "
        f"'{TRAINING_SHEET_NAME}': {exc}"
    )
    st.stop()

if df.empty:
    st.error(
        f"No data found in Google Sheet tab "
        f"'{TRAINING_SHEET_NAME}'."
    )
    st.stop()


# ============================================================
# COLUMN NORMALIZATION
# ============================================================
def clean_column_name(value):
    value = (
        str(value)
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .lower()
    )
    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value,
    )
    return value.strip("_")


column_map = {
    clean_column_name(col): col
    for col in df.columns
}


def find_column(names):
    # Exact matches first.
    for name in names:
        key = clean_column_name(name)
        if key in column_map:
            return column_map[key]

            # Conservative partial matches second.
    for key, original in column_map.items():
        for name in names:
            search_key = clean_column_name(name)
            if search_key and (
                    search_key in key
                    or key in search_key
            ):
                return original

    return None


# ============================================================
# DETECT GOOGLE SHEET COLUMNS
# ============================================================
COL_MODULE = find_column(
    [
        "Module",
        "Pillar",
        "Training Module",
        "Training Pillar",
        "Topic",
        "Process",
    ]
)

COL_DEPARTMENT = find_column(
    [
        "Department",
        "Departments",
        "Dept",
    ]
)

COL_BAND = find_column(
    [
        "Band",
        "Employee Band",
        "Employee Category / Band",
        "Grade Band",
        "Manpower Category",
        "Band / Category",
        "Employee Category",
    ]
)

COL_LEVEL = find_column(
    [
        "Level",
        "L08",
        "L08 Level",
        "Employee Level",
        "Grade",
        "Employee Grade",
    ]
)

COL_PERSON_TYPE = find_column(
    [
        "Person Type",
        "Employee Type",
        "Worker Type",
        "Associate / Contractual",
        "Associate Type",
        "Employment Type",
        "Worker Category",
        "Employee Category",
    ]
)

COL_TOTAL = find_column(
    [
        "Total",
        "Total Employees",
        "Total Workers",
        "Total Headcount",
        "Total Associates",
        "Target",
        "No. of Employees",
        "Employee Count",
        "Headcount",
    ]
)

COL_TRAINED = find_column(
    [
        "Trained",
        "Training Completed",
        "Completed",
        "No. Trained",
        "Number Trained",
        "Trained Employees",
        "No of Trained",
    ]
)

COL_COMPLETION = find_column(
    [
        "Completion %",
        "Completion Percentage",
        "Completion",
        "Training Completion %",
        "%",
    ]
)

# ============================================================
# BAND-SPECIFIC COLUMNS IN THE TRAINING SHEET
# ============================================================
# The TRAINING tab is a wide-format sheet. Each row contains
# separate employee totals and completed-training values for:
#   1. L08 & Above
#   2. Below L08
#   3. Associates
#   4. Contractual / Off-roll
#
# IMPORTANT:
# Do NOT use the generic "Total Employees" column here.
# The generic partial-match logic previously picked the
# "Total Employees (L08 & Above)" column and therefore
# treated 1,127 as the entire employee population.
#
# The actual sheet totals visible in the supplied data are:
#   L08 & Above       = 1,127
#   Below L08         = 1,212
#   Associates        = 1,504
#   Contractual       = 4,019
#   All bands total   = 7,862
#
# These dedicated columns are now the source of truth.

COL_TOTAL_L08_ABOVE = find_column(
    [
        "Total Employees (L08 & Above)",
        "Total Employee (L08 & Above)",
        "Total Employees L08 & Above",
        "L08 & Above Total Employees",
    ]
)

COL_TOTAL_L08_BELOW = find_column(
    [
        "Total Employees (Below L08)",
        "Total Employees (L08 below)",
        "Total Employees Below L08",
        "Below L08 Total Employees",
    ]
)

COL_TOTAL_ASSOCIATES = find_column(
    [
        "Total Associates",
        "Total Associate Employees",
        "Associates Total",
    ]
)

COL_TOTAL_OFFROLL = find_column(
    [
        "Total Contractual Worker",
        "Total Contractual Workers",
        "Total Contractual Worker(s)",
        "Total Contracts",
        "Total Contract",
        "Total Off-roll Employees",
        "Total Off Roll Employees",
        "Contractual Worker Total",
    ]
)

COL_TRAINED_L08_ABOVE = find_column(
    [
        "Completed Training (L08 & Above)",
        "Completed Training L08 & Above",
        "Completed Training (L08 Above)",
        "L08 & Above Completed Training",
    ]
)

COL_TRAINED_L08_BELOW = find_column(
    [
        "Completed Training (Below L08)",
        "Completed Training (L08 below)",
        "Completed Training Below L08",
        "Below L08 Completed Training",
    ]
)

COL_TRAINED_ASSOCIATES = find_column(
    [
        "Completed Training (Associates)",
        "Completed Training Associates",
        "Associates Completed Training",
    ]
)

COL_TRAINED_OFFROLL = find_column(
    [
        # The TRAINING sheet uses "Contracts" for the Off-roll/
        # Contractual completed-training column.
        "Completed Training (Contracts)",
        "Completed Training Contracts",
        "Completed Training (Contract)",
        "Completed Training (Contractual Worker)",
        "Completed Training (Contractual Workers)",
        "Completed Training (Off-roll Employees)",
        "Completed Training (Off Roll Employees)",
        "Contractual Worker Completed Training",
    ]
)

WIDE_BAND_COLUMNS = {
    "L08 & Above": {
        "total": COL_TOTAL_L08_ABOVE,
        "trained": COL_TRAINED_L08_ABOVE,
    },
    "L08 below": {
        "total": COL_TOTAL_L08_BELOW,
        "trained": COL_TRAINED_L08_BELOW,
    },
    "Associates": {
        "total": COL_TOTAL_ASSOCIATES,
        "trained": COL_TRAINED_ASSOCIATES,
    },
    "Off-roll Employees": {
        "total": COL_TOTAL_OFFROLL,
        "trained": COL_TRAINED_OFFROLL,
    },
}

WIDE_BAND_DATA_AVAILABLE = any(
    item["total"] is not None
    for item in WIDE_BAND_COLUMNS.values()
)

# ============================================================
# DATA PREPARATION
# ============================================================
work = df.copy()


def text_series(column, default=""):
    if column is None:
        return pd.Series(
            default,
            index=work.index,
            dtype="object",
        )

    return (
        work[column]
        .fillna("")
        .astype(str)
        .str.replace("\xa0", " ", regex=False)
        .str.strip()
    )


def numeric_series(column):
    if column is None:
        return pd.Series(
            0.0,
            index=work.index,
            dtype=float,
        )

    cleaned = (
        work[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(
        cleaned,
        errors="coerce",
    ).fillna(0.0)


work["_module"] = text_series(
    COL_MODULE,
    "Other",
)

work["_department"] = text_series(
    COL_DEPARTMENT,
    "Others",
)

work["_band_source"] = text_series(
    COL_BAND,
)

work["_level"] = text_series(
    COL_LEVEL,
)

work["_person_type"] = text_series(
    COL_PERSON_TYPE,
)

work["_total"] = numeric_series(
    COL_TOTAL,
)

work["_trained"] = numeric_series(
    COL_TRAINED,
)

work["_completion_raw"] = numeric_series(
    COL_COMPLETION,
)

# Numeric band-specific totals/completions.
for _band_name, _band_cols in WIDE_BAND_COLUMNS.items():
    _suffix = {
        "L08 & Above": "l08_above",
        "L08 below": "l08_below",
        "Associates": "associates",
        "Off-roll Employees": "offroll",
    }[_band_name]

    work[f"_total_{_suffix}"] = numeric_series(
        _band_cols["total"]
    )

    work[f"_trained_{_suffix}"] = numeric_series(
        _band_cols["trained"]
    )

# ============================================================
# NORMALIZE COMPLETION %
# ============================================================
if COL_COMPLETION:
    max_completion = (
        float(work["_completion_raw"].max())
        if not work.empty
        else 0
    )

    # Supports both 0.85 and 85 formats.
    if 0 < max_completion <= 1.5:
        work["_completion"] = (
                work["_completion_raw"] * 100
        )
    else:
        work["_completion"] = (
            work["_completion_raw"]
        )
else:
    work["_completion"] = 0.0

work["_completion"] = (
    work["_completion"]
    .clip(0, 100)
)

# If the sheet does not contain a completion column,
# calculate it from Trained / Total.
if COL_COMPLETION is None:
    valid_total = work["_total"] > 0

    work.loc[
        valid_total,
        "_completion",
    ] = (
            work.loc[
                valid_total,
                "_trained",
            ]
            /
            work.loc[
                valid_total,
                "_total",
            ]
            * 100
    )

# ============================================================
# BAND DEFINITIONS
# ============================================================
BAND_ORDER = [
    "L08 & Above",
    "L08 below",
    "Associates",
    "Off-roll Employees",
]


def normalize_band(value):
    text = str(value).strip().lower()

    if text in {
        "",
        "nan",
        "none",
        "null",
        "-",
    }:
        return ""

    text = re.sub(
        r"[‐‑‒–—−]",
        "-",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    # Off-roll / contractual must be checked first.
    if re.search(
            r"off\s*[- ]?roll"
            r"|contract(?:ual|or)?"
            r"|third\s*party"
            r"|contract\s*labou?r",
            text,
    ):
        return "Off-roll Employees"

        # Associates next.
    if re.search(
            r"\bassociate(?:s)?\b",
            text,
    ):
        return "Associates"

        # Explicit L08 above / below.
    if re.search(
            r"\bl\s*0?8\s*(?:and|&)?\s*above\b",
            text,
    ):
        return "L08 & Above"

    if re.search(
            r"\bl\s*0?8\s*(?:and|&)?\s*below\b",
            text,
    ):
        return "L08 below"

        # L08+ / L8+ / >=8.
    if re.search(
            r"l\s*0?8\s*\+"
            r"|l\s*0?8\s*(?:or|and)\s*above"
            r"|>=\s*8"
            r"|8\s*\+"
            r"|above\s*8",
            text,
    ):
        return "L08 & Above"

        # Below L08 / L01-L07.
    if re.search(
            r"below\s*8"
            r"|<\s*8"
            r"|l\s*0?[1-7]\b",
            text,
    ):
        return "L08 below"

        # L08, L09, L10, etc.
    level_match = re.search(
        r"\bl\s*0?(\d+)\b",
        text,
    )

    if level_match:
        level = int(
            level_match.group(1)
        )

        return (
            "L08 & Above"
            if level >= 8
            else "L08 below"
        )

        # Pure numeric level.
    if re.fullmatch(
            r"\d+(?:\.0+)?",
            text,
    ):
        return (
            "L08 & Above"
            if float(text) >= 8
            else "L08 below"
        )

    return ""


def resolve_band(row):
    """
    Band priority:
    1. Off-roll / contractual
    2. Associates
    3. Explicit Band column
    4. Level column
    5. Person Type
    """

    person = str(
        row["_person_type"]
    )

    band_source = str(
        row["_band_source"]
    )

    level = str(
        row["_level"]
    )

    special_text = (
        f"{person} | {band_source}"
    ).lower()

    if re.search(
            r"off\s*[- ]?roll"
            r"|contract(?:ual|or)?"
            r"|third\s*party"
            r"|contract\s*labou?r",
            special_text,
    ):
        return "Off-roll Employees"

    if re.search(
            r"\bassociate(?:s)?\b",
            special_text,
    ):
        return "Associates"

    explicit_band = normalize_band(
        band_source
    )

    if explicit_band:
        return explicit_band

    level_band = normalize_band(
        level
    )

    if level_band:
        return level_band

    person_band = normalize_band(
        person
    )

    if person_band:
        return person_band

    return ""


work["_band"] = work.apply(
    resolve_band,
    axis=1,
)

# ============================================================
# FIXED MODULE ORDER
# ============================================================
PREFERRED_MODULE_ORDER = [
    "PSM GA",
    "PT",
    "PHA",
    "MOC",
    "OP",
    "BOWTIE",
    "PSSR",
    "LOPA",
    "MIQA",
]

# Display-only KPI card titles. Internal module names remain unchanged.
MODULE_TITLES = {
    "PSM GA": "PSM General Awareness (PSM GA)",
    "PT": "Process Technology (PT)",
    "PHA": "Process Hazard Analysis (PHA)",
    "MOC": "Management of Change (MOC)",
    "OP": "Operating Procedure (OP)",
    "BOWTIE": "Bow-Tie",
    "PSSR": "Pre-Start Up Safety Review (PSSR)",
    "LOPA": "Layer of Protection Analysis (LOPA)",
    "MIQA": "Mechanical Integrity & Quality Assurance (MIQA)",
}


def order_modules(values):
    values = [
        str(x).strip()
        for x in values
        if str(x).strip()
    ]

    lookup = {
        value.lower(): value
        for value in values
    }

    result = []

    for preferred in PREFERRED_MODULE_ORDER:
        if preferred.lower() in lookup:
            result.append(
                lookup[
                    preferred.lower()
                ]
            )

    remaining = [
        value
        for value in values
        if value.lower()
           not in {
               item.lower()
               for item in result
           }
    ]

    result.extend(
        sorted(
            remaining,
            key=str.lower,
        )
    )

    return result


module_names = order_modules(
    work["_module"].unique().tolist()
)

# ============================================================
# COMPLETE VISUAL THEME
# ============================================================
st.markdown(
    """ 
    <style> 
    @import url( 
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap' 
    ); 

    * { 
        box-sizing: border-box; 
    } 

    html, 
    body, 
    .stApp, 
    [class*="css"] { 
        font-family: 
            "Inter", 
            Arial, 
            sans-serif !important; 
    } 

    /* Hide Streamlit chrome. */ 
    #MainMenu, 
    header, 
    footer, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"] { 
        display: none !important; 
    } 

    /* Clean white dashboard background. */ 
    .stApp, 
    [data-testid="stAppViewContainer"] > .main { 
        background: #f7f9fc !important; 
        color: #172554 !important; 
    } 

    /* Remove unnecessary top padding. */ 
    [data-testid="stMainBlockContainer"], 
    [data-testid="stAppViewBlockContainer"], 
    .block-container { 
        width: 100% !important; 
        max-width: 100% !important; 
        margin: 0 !important; 
        padding: 
            0 10px 18px 10px !important; 
    } 

    [data-testid="stVerticalBlock"] { 
        gap: 0 !important; 
    } 

    [data-testid="stHorizontalBlock"] { 
        gap: 14px !important; 
        align-items: center !important; 
    } 

    /* ======================================================== 
       FILTERS 
       ======================================================== */ 
    .filter-caption { 
        display: block !important; 
        width: 100% !important; 

        margin: 0 0 6px 0 !important; 
        padding: 0 !important; 

        color: #12357d !important; 

        font-family: "Inter", Arial, sans-serif !important; 
        font-size: 11px !important; 
        font-weight: 700 !important; 
        line-height: 16px !important; 

        text-align: left !important; 
        white-space: nowrap !important; 
    } 

    .filter-control 
    div[data-baseweb="select"] > div { 
        min-height: 36px !important; 
        height: 36px !important; 
        border-radius: 8px !important; 
        background: #eef1f5 !important; 
        border: 1px solid #d9e0e8 !important; 
        box-shadow: none !important; 
    } 

    .filter-control 
    div[data-baseweb="select"] * { 
        font-family: 
            "Inter", 
            Arial, 
            sans-serif !important; 
        color: #374151 !important; 
        font-size: 11px !important; 
    } 

    .filter-control 
    div[data-baseweb="select"] svg { 
        fill: #374151 !important; 
    } 

    /* ======================================================== 
       MODULE STATUS TITLE 
       ======================================================== */ 
    .status-title { 
        display: flex; 
        align-items: center; 

        position: relative; 

        width: 100%; 
        min-height: 38px; 

        margin: 0 0 10px 0; 
        padding: 0 0 7px 0; 

        color: #12357d; 

        font-size: 25px; 
        font-weight: 800; 
        line-height: 1.2; 

        letter-spacing: -.55px; 

        overflow: visible; 
    } 

    .status-title-accent { 
        position: static; 

        display: inline-block; 

        width: 35px; 
        min-width: 35px; 
        height: 4px; 

        margin: 0 10px 0 2px; 

        border-radius: 4px; 

        background: #1268e8; 
    } 

    /* ======================================================== 
       MODULE-WISE TRAINING STATUS 
       One real HTML grid is used for all 9 cards. 
       This avoids Streamlit column-height/Markdown overlap. 
       ======================================================== */ 
    .kpi-section { 
        width: 100%; 
        box-sizing: border-box; 

        margin: 0 0 14px 0; 
        padding: 12px 12px 14px 12px; 

        background: #ffffff; 
        border: 1px solid #e3e8ef; 
        border-radius: 12px; 

        box-shadow: 
            0 2px 8px rgba(31, 52, 76, .035); 
    } 

    .kpi-section-title { 
        display: flex; 
        align-items: center; 

        min-height: 34px; 
        margin: 0 0 10px 0; 
        padding: 0 2px; 

        color: #12357d; 
        font-size: 23px; 
        font-weight: 800; 
        line-height: 1.2; 
        letter-spacing: -.45px; 
    } 

    .kpi-section-title-accent { 
        width: 7px; 
        min-width: 7px; 
        height: 27px; 
        min-height: 27px; 

        margin-right: 11px; 

        border-radius: 5px; 
        background: #1268e8; 
    } 

    .kpi-grid { 
        display: grid; 

        grid-template-columns: 
            repeat(3, minmax(0, 1fr)); 

        column-gap: 14px; 
        row-gap: 14px; 

        width: 100%; 
        box-sizing: border-box; 
    } 

    .module-card { 
        position: relative; 

        width: 100%; 
        height: 106px; 
        min-height: 106px; 
        box-sizing: border-box; 

        overflow: hidden; 

        background: var(--card-bg); 

        border: 1px solid var(--card-border); 
        border-radius: 10px; 

        padding: 9px 14px 7px 32px; 

        box-shadow: 
            0 2px 8px 
            rgba(31, 52, 76, .07); 
    } 

    .module-card::before { 
        content: ""; 

        position: absolute; 

        left: 0; 
        top: 0; 
        bottom: 0; 

        width: 8px; 

        background: var(--accent); 

        border-radius: 10px 0 0 10px; 
    } 

    .module-name { 
        margin: 0 0 5px 0; 

        color: var(--accent); 

        font-size: 16px; 
        font-weight: 800; 
        line-height: 1.15; 

        white-space: nowrap; 
        overflow: hidden; 
        text-overflow: ellipsis; 
    } 

    .band-row { 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 

        min-height: 18px; 
        gap: 10px; 

        color: var(--accent); 

        font-size: 10px; 
        font-weight: 500; 
        line-height: 1.35; 
    } 

    .band-value { 
        min-width: 74px; 

        text-align: right; 

        color: var(--accent); 

        font-size: 10px; 
        font-weight: 800; 

        white-space: nowrap; 
    } 

    /* Keep cards stable at smaller screen widths. */ 
    @media (max-width: 1100px) { 
        .kpi-grid { 
            grid-template-columns: 
                repeat(3, minmax(0, 1fr)); 
            column-gap: 10px; 
            row-gap: 12px; 
        } 

        .module-card { 
            height: 106px; 
            min-height: 106px; 
        } 
    } 

    @media (max-width: 760px) { 
        .kpi-grid { 
            grid-template-columns: 
                repeat(1, minmax(0, 1fr)); 
            row-gap: 12px; 
        } 

        .kpi-section { 
            padding: 10px; 
        } 
    } 

    /* ======================================================== 
       CHART SECTION CARDS 
       ======================================================== */ 



    /* Breathing room from the browser's top edge */ 
    .block-container { 
        padding-top: 22px !important; 
    } 

    /* Keep the dashboard's first filter row cleanly aligned */ 
    .top-filter-row { 
        margin-top: 0 !important; 
        margin-bottom: 5px !important; 
    } 
    /* PERFECTLY ALIGN FILTER LABELS AND DROPDOWNS */
.filter-caption {
    display: flex !important;
    align-items: center !important;
    height: 38px !important;
    margin: 0 !important;
    padding: 0 !important;
}

.filter-control {
    width: 100% !important;
    height: 38px !important;
    margin: 0 !important;
    padding: 0 !important;
}
    /* Top filter controls — identical typography and alignment */ 
    .filter-control, 
    .filter-control * { 
        font-family: "Inter", Arial, sans-serif !important; 
    } 

    .filter-control div[data-baseweb="select"] { 
        width: 100% !important; 
    } 

    .filter-control div[data-baseweb="select"] > div { 
        min-height: 38px !important; 
        height: 38px !important; 

        display: flex !important; 
        align-items: center !important; 

        border-radius: 9px !important; 
    } 

    .filter-control div[data-baseweb="select"] span { 
        font-family: "Inter", Arial, sans-serif !important; 
        font-size: 13px !important; 
        font-weight: 500 !important; 
        line-height: 18px !important; 
    } 

    .filter-control input { 
        font-family: "Inter", Arial, sans-serif !important; 
        font-size: 13px !important; 
        font-weight: 500 !important; 
    } 

    /* Keep all four filter elements on one visual center line */ 
    .top-filter-row [data-testid="stHorizontalBlock"] { 
        align-items: center !important; 
    } 

    .top-filter-row [data-testid="stHorizontalBlock"] > div { 
        align-self: center !important; 
    } 

    .section-heading { 
        display: flex; 
        align-items: center; 

        width: 100%; 
        min-height: 56px; 
        height: 56px; 

        margin-top: 14px; 
        margin-bottom: 0; 
        padding: 8px 16px; 

        background: #ffffff; 

        border: 1px solid #d9e6f1; 
        border-radius: 9px 9px 0 0; 

        color: #12357d; 

        font-size: 18px; 
        font-weight: 800; 
        line-height: 1.35; 

        letter-spacing: -.35px; 

        box-shadow: 
            0 2px 7px 
            rgba(25,55,90,.025); 

        overflow: visible; 
    } 

    .section-heading-accent { 
        width: 7px; 
        min-width: 7px; 
        height: 28px; 
        min-height: 28px; 

        flex: 0 0 auto; 

        margin-right: 12px; 

        border-radius: 5px; 
    } 

    .section-card { 
        width: 100%; 

        margin-top: 14px; 

        overflow: hidden; 

        border: 1px solid #dbe4ed; 
        border-radius: 12px; 

        box-shadow: 
            0 2px 9px 
            rgba(15, 23, 42, .045); 
    } 

    .section-red { 
        background: #fff8f8; 
    } 

    .section-blue { 
        background: #f7fbff; 
    } 

    .section-green { 
        background: #f7fcf9; 
    } 

    .section-title { 
        display: flex; 
        align-items: center; 

        min-height: 50px; 

        padding: 
            8px 18px; 

        color: #12357d; 

        font-size: 19px; 
        font-weight: 800; 
        line-height: 1.2; 

        letter-spacing: -.35px; 
    } 

    .section-accent { 
        width: 7px; 
        height: 25px; 

        flex: 0 0 auto; 

        margin-right: 12px; 

        border-radius: 5px; 

        background: var(--accent); 
    } 

    .plot-shell { 
        margin: 
            0 8px 8px 8px; 

        padding: 
            4px 5px; 

        background: #ffffff; 

        border: 
            1px solid 
            rgba(215, 225, 236, .75); 

        border-radius: 9px; 
    } 

    [data-testid="stPlotlyChart"] { 
        background: #ffffff !important; 
        border-radius: 8px !important; 
        overflow: hidden !important; 
    } 

    .empty-message { 
        margin: 
            0 8px 8px 8px; 

        padding: 24px; 

        background: #ffffff; 

        border-radius: 9px; 

        color: #64748b; 

        text-align: center; 

        font-size: 12px; 
    } 

    .refresh-note { 
        height: 24px; 

        display: flex; 
        align-items: center; 
        justify-content: flex-end; 

        color: #94a3b8; 

        font-size: 8px; 

        padding-right: 4px; 
    } 

    @media (max-width: 900px) { 
        [data-testid="stMainBlockContainer"], 
        [data-testid="stAppViewBlockContainer"], 
        .block-container { 
            padding: 
                0 7px 12px 7px !important; 
        } 

        .module-card { 
            height: 106px; 
            min-height: 106px; 
        } 

        .section-title { 
            font-size: 17px; 
        } 
    } 
    </style> 
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FILTERS
# ============================================================
department_values = sorted(
    [
        value
        for value in
        work["_department"]
        .dropna()
        .unique()
        .tolist()
        if str(value).strip()
    ],
    key=lambda x: str(x).lower(),
)

department_options = [
                         "All Departments"
                     ] + department_values

band_options = [
                   "All Bands"
               ] + BAND_ORDER

# Keep filter state through the 30-second automatic refresh.
query_department = st.query_params.get(
    "department",
    "All Departments",
)

query_band = st.query_params.get(
    "band",
    "All Bands",
)

if query_department not in department_options:
    query_department = "All Departments"

if query_band not in band_options:
    query_band = "All Bands"

filter_department, filter_band = st.columns(
    [1, 1],
    gap="small",
)

with filter_department:
    label_col, control_col = st.columns(
        [0.24, 0.76],
        gap="small",
    )

    with label_col:
        st.markdown(
            '<div class="filter-caption">'
            'Department'
            '</div>',
            unsafe_allow_html=True,
        )

    with control_col:
        st.markdown(
            '<div class="filter-control">',
            unsafe_allow_html=True,
        )

        selected_department = st.selectbox(
            "Department",
            department_options,
            index=department_options.index(
                query_department
            ),
            label_visibility="collapsed",
            key="department_filter",
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

with filter_band:
    label_col, control_col = st.columns(
        [0.24, 0.76],
        gap="small",
    )

    with label_col:
        st.markdown(
            '<div class="filter-caption">'
            'Training Band'
            '</div>',
            unsafe_allow_html=True,
        )

    with control_col:
        st.markdown(
            '<div class="filter-control">',
            unsafe_allow_html=True,
        )

        selected_band = st.selectbox(
            "Band",
            band_options,
            index=band_options.index(
                query_band
            ),
            label_visibility="collapsed",
            key="band_filter",
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

st.query_params["department"] = (
    selected_department
)

st.query_params["band"] = (
    selected_band
)

# ============================================================
# APPLY FILTERS
# ============================================================
filtered_df = work.copy()

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["_department"]
        == selected_department
        ]

# The TRAINING sheet stores all four bands as separate columns,
# not as one Band field per row. Therefore, when the wide-format
# columns are available, the Band filter is applied inside the
# calculation functions instead of deleting rows here.
#
# Only use row-level filtering as a fallback for a different
# long-format data source.
if (
        selected_band != "All Bands"
        and not WIDE_BAND_DATA_AVAILABLE
):
    filtered_df = filtered_df[
        filtered_df["_band"]
        == selected_band
        ]

# ============================================================
# CALCULATION FUNCTIONS
# ============================================================
# WIDE-FORMAT TRAINING CALCULATION
#
# The dashboard must calculate:
#
#   L08 & Above  = 1,127
#   Below L08    = 1,212
#   Associates   = 1,504
#   Off-roll     = 4,019
#   ALL BANDS    = 7,862
#
# for the supplied TRAINING data.
#
# Completion is always:
#       completed training / employee total * 100
#
# The selected Band filter controls which band is used in the
# charts. "All Bands" combines all four populations.
# ============================================================

BAND_SUFFIX = {
    "L08 & Above": "l08_above",
    "L08 below": "l08_below",
    "Associates": "associates",
    "Off-roll Employees": "offroll",
}


def _band_sum(group, band, value_type):
    """Sum one band-specific column for a group."""
    if group.empty:
        return 0.0

    suffix = BAND_SUFFIX.get(band)
    if suffix is None:
        return 0.0

    column = f"_{value_type}_{suffix}"

    if column not in group.columns:
        return 0.0

    return float(
        pd.to_numeric(
            group[column],
            errors="coerce",
        ).fillna(0).sum()
    )


def _selected_bands():
    """Return the band(s) included by the current filter."""
    if selected_band == "All Bands":
        return BAND_ORDER

    return [selected_band]


def total_value(group, band=None):
    if group.empty:
        return 0

        # Explicit band is used by KPI rows.
    if WIDE_BAND_DATA_AVAILABLE:
        bands = (
            [band]
            if band in BAND_ORDER
            else _selected_bands()
        )

        return int(
            round(
                sum(
                    _band_sum(
                        group,
                        item,
                        "total",
                    )
                    for item in bands
                )
            )
        )

        # Fallback for long-format data.
    if COL_TOTAL:
        return int(
            round(
                float(
                    group["_total"].sum()
                )
            )
        )

    return int(len(group))


def trained_value(group, band=None):
    if group.empty:
        return 0

    if WIDE_BAND_DATA_AVAILABLE:
        bands = (
            [band]
            if band in BAND_ORDER
            else _selected_bands()
        )

        return int(
            round(
                sum(
                    _band_sum(
                        group,
                        item,
                        "trained",
                    )
                    for item in bands
                )
            )
        )

        # Fallback for long-format data.
    if COL_TRAINED:
        return int(
            round(
                float(
                    group["_trained"].sum()
                )
            )
        )

    total = total_value(
        group,
        band=band,
    )

    if total <= 0:
        return 0

    return int(
        round(
            total
            * completion_value(
                group,
                band=band,
            )
            / 100
        )
    )


def completion_value(group, band=None):
    if group.empty:
        return 0.0

    if WIDE_BAND_DATA_AVAILABLE:
        total = float(
            total_value(
                group,
                band=band,
            )
        )

        trained = float(
            trained_value(
                group,
                band=band,
            )
        )

        if total <= 0:
            return 0.0

        return (
                trained
                / total
                * 100
        )

        # Fallback for long-format data.
    total = float(
        group["_total"].sum()
    )

    trained = float(
        group["_trained"].sum()
    )

    if (
            COL_TOTAL
            and COL_TRAINED
            and total > 0
    ):
        return float(
            trained
            / total
            * 100
        )

    if COL_COMPLETION:
        return float(
            group["_completion"].mean()
        )

    return 0.0


def status_text(group, band):
    return (
        f"{trained_value(group, band=band):,}"
        f"/"
        f"{total_value(group, band=band):,}"
    )


# ============================================================
# SANITY CHECK FOR THE CURRENT ALL-BANDS DATA
# ============================================================
# This is intentionally not displayed on the dashboard.
# It makes the expected population logic explicit and protects
# against the previous error where only the L08 & Above column
# (1,127) was used as the entire employee population.
if WIDE_BAND_DATA_AVAILABLE:
    _all_band_total = sum(
        total_value(
            filtered_df,
            band=_band,
        )
        for _band in BAND_ORDER
    )

    _expected_total = (
            total_value(
                filtered_df,
                band="L08 & Above",
            )
            + total_value(
        filtered_df,
        band="L08 below",
    )
            + total_value(
        filtered_df,
        band="Associates",
    )
            + total_value(
        filtered_df,
        band="Off-roll Employees",
    )
    )

    # Both expressions must be identical.
    if _all_band_total != _expected_total:
        raise RuntimeError(
            "Training-band population calculation mismatch."
        )

    # ============================================================
# MODULE-WISE TRAINING STATUS
# ============================================================
# All nine KPI cards are rendered inside ONE HTML grid.
# This is important: using separate Streamlit columns for each
# row can cause the browser to calculate inconsistent element
# heights and visually overlap the next row.
# ============================================================

card_accents = [
    "#1976D2",  # PSM GA
    "#E72A3B",  # PT
    "#18A765",  # PHA
    "#7C2CFF",  # MOC
    "#F2A20C",  # OP
    "#18B8C2",  # BOWTIE
    "#ED2D8D",  # PSSR
    "#F15B2A",  # LOPA
    "#6840E8",  # MIQA
]

card_backgrounds = [
    "#EEF6FF",  # PSM GA
    "#FFF0F2",  # PT
    "#EFFAF5",  # PHA
    "#F4EFFF",  # MOC
    "#FFF8E9",  # OP
    "#ECFAFC",  # BOWTIE
    "#FFF0F7",  # PSSR
    "#FFF2EC",  # LOPA
    "#F1EEFF",  # MIQA
]

card_borders = [
    "#CFE2F7",  # PSM GA
    "#F4CDD3",  # PT
    "#CDEDDD",  # PHA
    "#DDD0FA",  # MOC
    "#F1D9A4",  # OP
    "#C7EAF0",  # BOWTIE
    "#F2CADD",  # PSSR
    "#F2D1C3",  # LOPA
    "#D7CEFA",  # MIQA
]

kpi_html = (
    '<div class="kpi-section">'
    '<div class="kpi-section-title">'
    '<span class="kpi-section-title-accent"></span>'
    '<span>Module-wise training status</span>'
    '</div>'
    '<div class="kpi-grid">'
)

for index, module_name in enumerate(module_names):
    group = filtered_df[
        filtered_df["_module"] == module_name
        ]

    accent = card_accents[
        index % len(card_accents)
        ]

    card_bg = card_backgrounds[
        index % len(card_backgrounds)
        ]

    card_border = card_borders[
        index % len(card_borders)
        ]

    # Change only the visible KPI card title; calculations/filtering
    # continue to use the original Google Sheet module name.
    display_module = MODULE_TITLES.get(
        str(module_name).strip(),
        str(module_name),
    )
    safe_module = html.escape(
        display_module
    )

    status = {}

    for band in BAND_ORDER:
        # When a specific band is selected, preserve the existing
        # visual behavior: show that band's value and keep the
        # other rows at 0/0. With "All Bands", show all four.
        if (
                selected_band != "All Bands"
                and band != selected_band
        ):
            status[band] = "0/0"
        else:
            status[band] = status_text(
                group,
                band,
            )

    kpi_html += (
        '<div class="module-card" '
        f'style="--accent:{accent};'
        f'--card-bg:{card_bg};'
        f'--card-border:{card_border};">'
        f'<div class="module-name">{safe_module}</div>'

        '<div class="band-row">'
        '<span>L08 &amp; above</span>'
        f'<span class="band-value">'
        f'{status["L08 & Above"]}'
        '</span>'
        '</div>'

        '<div class="band-row">'
        '<span>L08 below</span>'
        f'<span class="band-value">'
        f'{status["L08 below"]}'
        '</span>'
        '</div>'

        '<div class="band-row">'
        '<span>Associates</span>'
        f'<span class="band-value">'
        f'{status["Associates"]}'
        '</span>'
        '</div>'

        '<div class="band-row">'
        '<span>Off Roll</span>'
        f'<span class="band-value">'
        f'{status["Off-roll Employees"]}'
        '</span>'
        '</div>'

        '</div>'
    )

kpi_html += (
    '</div>'
    '</div>'
)

st.markdown(
    kpi_html,
    unsafe_allow_html=True,
)

# ============================================================
# MODULE CHART DATA
# ============================================================
module_rows = []

for module_name in module_names:
    group = filtered_df[
        filtered_df["_module"]
        == module_name
        ]

    module_rows.append(
        {
            "module": module_name,
            "total": total_value(group),
            "trained": trained_value(group),
            "percentage": completion_value(group),
        }
    )

module_data = pd.DataFrame(
    module_rows
)

# ============================================================
# CHART 1:
# MODULE-WISE TRAINING COMPLIANCE
# ============================================================
st.markdown(
    '<div class="section-heading">'
    '<span class="section-heading-accent" style="background:#E72A3B;"></span>'
    '<span>Module-wise Training Compliance</span>'
    '</div>',
    unsafe_allow_html=True,
)

if not module_data.empty:

    fig_module = go.Figure()

    fig_module.add_trace(
        go.Bar(
            x=module_data["module"],
            y=module_data["total"],
            name="Total Employees",
            marker_color="#5AAAF0",
            marker_line_color="#4B9FE8",
            marker_line_width=0.5,
            text=[
                f"{value:,.0f}"
                for value in
                module_data["total"]
            ],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Total Employees: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig_module.add_trace(
        go.Bar(
            x=module_data["module"],
            y=module_data["trained"],
            name="Trained Employees",
            marker_color="#EF2733",
            marker_line_color="#D91F2A",
            marker_line_width=0.5,
            text=[
                f"{value:,.0f}"
                for value in
                module_data["trained"]
            ],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Trained Employees: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig_module.add_trace(
        go.Scatter(
            x=module_data["module"],
            y=module_data["percentage"],
            name="Compliance %",
            mode="lines+markers+text",
            yaxis="y2",
            line=dict(
                color="#1260C9",
                width=2.2,
            ),
            marker=dict(
                color="#1260C9",
                size=8,
                line=dict(
                    color="#FFFFFF",
                    width=1.5,
                ),
            ),
            text=[
                f"{value:.1f}%"
                for value in
                module_data["percentage"]
            ],
            textposition="top center",
            textfont=dict(
                size=10,
                color="#1249A3",
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Compliance: %{y:.1f}%"
                "<extra></extra>"
            ),
        )
    )

    employee_max = max(
        float(
            module_data[
                ["total", "trained"]
            ].max().max()
        ),
        100,
    )

    chart_y_max = (
            employee_max * 1.18
    )

    fig_module.update_layout(
        height=280,
        barmode="group",
        bargap=0.25,
        bargroupgap=0.07,
        margin=dict(
            l=55,
            r=60,
            t=45,
            b=50,
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#12357D",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,.95)",
            bordercolor="#EDF1F5",
            borderwidth=1,
            font=dict(size=9),
        ),
        yaxis=dict(
            title="No. of Employees",
            range=[
                0,
                chart_y_max,
            ],
            title_font=dict(
                size=10,
                color="#12357D",
            ),
            tickfont=dict(
                size=9,
                color="#12357D",
            ),
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="#B9CCE0",
        ),
        yaxis2=dict(
            title="Compliance %",
            overlaying="y",
            side="right",
            range=[0, 100],
            dtick=20,
            title_font=dict(
                size=10,
                color="#12357D",
            ),
            tickfont=dict(
                size=9,
                color="#12357D",
            ),
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor="#B9CCE0",
        ),
        xaxis=dict(
            tickfont=dict(
                size=9,
                color="#12357D",
            ),
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
    )

    st.plotly_chart(
        fig_module,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )

else:
    st.markdown(
        '<div class="empty-message">'
        'No module data is available.'
        '</div>',
        unsafe_allow_html=True,
    )
# ============================================================
# CHART 2:
# TRAINING COMPLETION BY DEPARTMENT
# ============================================================
department_rows = []

for department, group in (
        filtered_df
                .groupby(
            "_department",
            dropna=False,
        )
):
    department_rows.append(
        {
            "department": department,
            "percentage": completion_value(
                group
            ),
        }
    )

department_data = pd.DataFrame(
    department_rows
)

if not department_data.empty:
    department_data = (
        department_data
        .sort_values(
            "percentage",
            ascending=True,
        )
    )

# Prepare heatmap data before rendering the side-by-side chart columns.
# This block was accidentally omitted in the previous side-by-side version.
heat_rows = []

for (
        module_name,
        department_name,
), group in (
        filtered_df
                .groupby(
            [
                "_module",
                "_department",
            ],
            dropna=False,
        )
):
    heat_rows.append(
        {
            "module": module_name,
            "department": department_name,
            "percentage": completion_value(
                group
            ),
        }
    )

heat_data = pd.DataFrame(
    heat_rows
)

# ============================================================
# CHARTS 2 & 3 — SIDE BY SIDE
# LEFT: DEPARTMENT COMPLETION BAR CHART
# RIGHT: MODULE/DEPARTMENT HEATMAP
# ============================================================

chart_left, chart_right = st.columns(
    [1, 1],
    gap="medium",
)

with chart_left:
    st.markdown(
        '<div class="section-heading">'
        '<span class="section-heading-accent" style="background:#1677E8;"></span>'
        '<span>Training Completion by Department (Overall %)</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not department_data.empty:

        fig_department = go.Figure(
            go.Bar(
                x=department_data["percentage"],
                y=department_data["department"],
                orientation="h",
                marker=dict(
                    color=[
                        '#4C9FE8', '#E95D6A', '#43B883',
                        '#8B5CF6', '#F2A93B', '#22B8CF',
                        '#E6499A', '#F27645', '#6366D9',
                        '#36A269', '#D977B5', '#E0A12C',
                        '#4B83C4', '#7A63B8', '#4FAF9B',
                    ][:len(department_data)],
                    line=dict(
                        color="#FFFFFF",
                        width=0.5,
                    ),
                ),
                text=[
                    f"{value:.1f}%"
                    for value in department_data["percentage"]
                ],
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Overall Completion: %{x:.1f}%"
                    "<extra></extra>"
                ),
            )
        )

        fig_department.update_layout(
            height=540,

            margin=dict(
                l=120,
                r=45,
                t=18,
                b=45,
            ),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                family="Inter, Arial, sans-serif",
                color="#12357D",
            ),
            xaxis=dict(
                range=[0, 105],
                dtick=20,
                title="Overall Completion %",
                title_font=dict(
                    size=10,
                    color="#12357D",
                ),
                tickfont=dict(
                    size=9,
                    color="#12357D",
                ),
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor="#B9CCE0",
            ),
            yaxis=dict(
                tickfont=dict(
                    size=9,
                    color="#12357D",
                ),
                showgrid=False,
                showline=False,
                zeroline=False,
            ),
            showlegend=False,
            bargap=0.25,
        )

        st.plotly_chart(
            fig_department,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

    else:
        st.markdown(
            '<div class="empty-message">'
            'No department data is available.'
            '</div>',
            unsafe_allow_html=True,
        )

with chart_right:
    st.markdown(
        '<div class="section-heading">'
        '<span class="section-heading-accent" style="background:#16A765;"></span>'
        '<span>Module-wise Training Completion by Department (%)</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not heat_data.empty:

        heat_table = heat_data.pivot(
            index="module",
            columns="department",
            values="percentage",
        ).fillna(0)

        # Fixed module order.
        heat_modules = [
            module
            for module in module_names
            if module in heat_table.index
        ]

        heat_table = heat_table.reindex(
            heat_modules
        )

        # Department order: highest average compliance first.
        ordered_departments = (
            heat_table
            .mean(axis=0)
            .sort_values(
                ascending=False
            )
            .index
            .tolist()
        )

        heat_table = heat_table[
            ordered_departments
        ]

        fig_heatmap = go.Figure(
            go.Heatmap(
                z=heat_table.values,
                x=heat_table.columns.tolist(),
                y=heat_table.index.tolist(),
                zmin=0,
                zmax=100,

                colorscale=[
                    [0.00, "#EF233C"],
                    [0.25, "#F46B2D"],
                    [0.50, "#F5D313"],
                    [0.75, "#8FD13F"],
                    [1.00, "#10A85A"],
                ],

                text=[
                    [
                        f"{value:.1f}%"
                        for value in row
                    ]
                    for row in heat_table.values
                ],

                texttemplate="%{text}",

                textfont=dict(
                    size=8,
                    color="#172033",
                ),

                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Department: %{x}<br>"
                    "Completion: %{z:.1f}%"
                    "<extra></extra>"
                ),

                colorbar=dict(
                    title="%",
                    thickness=12,
                    len=0.86,
                    tickvals=[
                        0,
                        25,
                        50,
                        75,
                        100,
                    ],
                    ticktext=[
                        "0",
                        "25",
                        "50",
                        "75",
                        "100",
                    ],
                    tickfont=dict(
                        size=8,
                        color="#12357D",
                    ),
                    title_font=dict(
                        size=9,
                        color="#12357D",
                    ),
                ),

                xgap=1.5,
                ygap=1.5,
            )
        )

        fig_heatmap.update_layout(
            height=540,

            margin=dict(
                l=75,
                r=45,
                t=8,
                b=105,
            ),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(
                family="Inter, Arial, sans-serif",
                color="#12357D",
            ),
            xaxis=dict(
                tickfont=dict(
                    size=8,
                    color="#12357D",
                ),
                tickangle=-40,
                showgrid=False,
                showline=False,
                zeroline=False,
            ),
            yaxis=dict(
                tickfont=dict(
                    size=8,
                    color="#12357D",
                ),
                showgrid=False,
                showline=False,
                zeroline=False,
                autorange="reversed",
            ),
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

    else:
        st.markdown(
            '<div class="empty-message">'
            'No module/department data is available.'
            '</div>',
            unsafe_allow_html=True,
        )

