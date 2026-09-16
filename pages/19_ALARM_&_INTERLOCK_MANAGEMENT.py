import io
from datetime import date
from html import escape
from urllib.parse import quote

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Alarm & Interlock management",
    page_icon="📊",
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
    margin-top:-65px !important;
    margin-bottom:-10px !important;
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
        margin-bottom:6px !important;
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
    padding-top: 5px !important;
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

    font-size: 23px;

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

            ALARM & INTERLOCK MANAGEMENT 

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

# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================

GOOGLE_SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SOC_SHEET = "SOC-SOL Deviation"
INTERLOCK_SHEET = "Interlock"
ALARM_SHEET = "Alarm"

REFRESH_SECONDS = 30


# ============================================================
# FINANCIAL YEAR
# APRIL -> MARCH
# ============================================================

FY_MONTHS = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
]


# ============================================================
# AUTO REFRESH
# ============================================================

st_autorefresh(
    interval=REFRESH_SECONDS * 1000,
    key="alarm_interlock_refresh",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       PAGE
       -------------------------------------------------------- */

    .stApp,
    .main {
        background-color: #f4f8fc;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.85rem;
        padding-bottom: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }


    /* --------------------------------------------------------
       COLUMNS
       -------------------------------------------------------- */

    div[data-testid="stHorizontalBlock"] {
        gap: 0.35rem !important;
        align-items: stretch !important;
    }

    div[data-testid="column"] {
        padding-left: 0.04rem;
        padding-right: 0.04rem;
        align-self: stretch;
    }


    /* --------------------------------------------------------
       SECTION PANELS
       -------------------------------------------------------- */

    .st-key-soc-panel,
    .st-key-interlock-panel,
    .st-key-alarm-panel {
        height: 900px !important;
        min-height: 900px !important;
        max-height: 900px !important;
        box-sizing: border-box;
        border-radius: 10px;
        padding: 7px 7px 2px 7px;
        margin-top: 2px;
        margin-bottom: 0;
        overflow: hidden !important;
        align-self: stretch !important;
        flex: 0 0 900px !important;
    }

    .st-key-soc-panel {
        background-color: #f2f8ff;
        border: 1px solid #d5e7f7;
    }

    .st-key-interlock-panel {
        background-color: #f5f9ff;
        border: 1px solid #d7e7f4;
    }

    .st-key-alarm-panel {
        background-color: #f7f8ff;
        border: 1px solid #d9e0f3;
    }

    .st-key-soc-panel .dashboard-section,
    .st-key-interlock-panel .dashboard-section,
    .st-key-alarm-panel .dashboard-section {
        margin-top: 0;
    }


    /* --------------------------------------------------------
       FILTERS
       -------------------------------------------------------- */

    div[data-testid="stSelectbox"] {
        margin-bottom: 0.25rem;
    }

    div[data-testid="stSelectbox"] label {
        color: #0645a5 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #c8d8e8 !important;
        border-radius: 6px !important;
        min-height: 39px !important;
    }


    /* --------------------------------------------------------
       MAIN SECTION HEADER
       -------------------------------------------------------- */

    .section-header {
        background:
            linear-gradient(
                96deg,
                #0848a5 0%,
                #0848a5 90%,
                #f51d3b 90%,
                #f51d3b 100%
            );

        color: #ffffff;

        border-radius: 6px;

        padding: 7px 12px;

        margin-top: 2px;
        margin-bottom: 15px;

        min-height: 42px;

        display: flex;
        align-items: center;

        font-size: 17px;
        font-weight: 750;
        line-height: 1.2;
    }


    /* --------------------------------------------------------
       SUB TITLE
       -------------------------------------------------------- */

    .sub-title {
        color: #0645a5;

        font-size: 14px;
        font-weight: 750;

        line-height: 1.2;

        margin-top: 12px;
        margin-bottom: 10px;

        padding: 0;
    }


    /* --------------------------------------------------------
       METRIC BOX
       -------------------------------------------------------- */

    [data-testid="stMetric"] {
        background-color: #eaf5ff;

        border: 1px solid #d2e5f6;

        border-radius: 8px;

        padding: 7px 10px;

        min-height: 75px;

        margin-bottom: 6px;
    }

    [data-testid="stMetricLabel"] {
        color: #0645a5 !important;

        font-size: 11px !important;

        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #0645a5 !important;

        font-size: 24px !important;

        font-weight: 750 !important;
    }


    /* --------------------------------------------------------
       PLOTLY
       -------------------------------------------------------- */

    div[data-testid="stPlotlyChart"] {
        background-color: #ffffff;

        border: 1px solid #d6e5f3;

        border-radius: 7px;

        margin-top: 5px !important;
        margin-bottom: 8px !important;

        padding: 0 !important;

        max-width: 100% !important;
    }

    /* --------------------------------------------------------
       LINE CHARTS ONLY - NO INTERNAL SCROLLBARS
       Pie/donut charts are intentionally NOT affected.
       -------------------------------------------------------- */

    .st-key-soc-line-chart div[data-testid="stPlotlyChart"],
    .st-key-soc-line-chart div[data-testid="stPlotlyChart"] > div,
    .st-key-soc-line-chart div[data-testid="stPlotlyChart"] iframe,
    .st-key-soc-line-chart div[data-testid="stPlotlyChart"] .js-plotly-plot,
    .st-key-soc-line-chart div[data-testid="stPlotlyChart"] .plot-container,
    .st-key-soc-line-chart div[data-testid="stPlotlyChart"] .svg-container,

    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"],
    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"] > div,
    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"] iframe,
    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"] .js-plotly-plot,
    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"] .plot-container,
    .st-key-alarm-line-chart div[data-testid="stPlotlyChart"] .svg-container {
        overflow: hidden !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        max-width: 100% !important;
    }


    /* --------------------------------------------------------
       CUSTOM TABLE
       -------------------------------------------------------- */

    .table-scroll {
        width: 100%;

        overflow-x: auto;
        overflow-y: auto;

        background: #ffffff;

        border: 1px solid #d2e3f2;

        border-radius: 8px;

        margin-top: 2px;
        margin-bottom: 5px;
    }

    .dashboard-table {
        width: 100%;

        border-collapse: collapse;

        table-layout: auto;

        font-family: Arial, sans-serif;

        font-size: 11.5px;

        color: #17324d;
    }

    .dashboard-table th {
        background: #dceefb;

        color: #0645a5;

        font-weight: 700;

        text-align: left !important;

        padding: 5px 8px;

        border-right: 1px solid #c9dbe9;
        border-bottom: 1px solid #c9dbe9;

        white-space: nowrap;

        position: sticky;
        top: 0;

        z-index: 2;
    }

    .dashboard-table td {
        text-align: left !important;

        padding: 4px 8px;

        border-right: 1px solid #e0e7ee;
        border-bottom: 1px solid #e0e7ee;

        white-space: nowrap;
    }

    .dashboard-table th:last-child,
    .dashboard-table td:last-child {
        border-right: none;
    }

    .dashboard-table tbody tr:hover td {
        background-color: #f7fbff;
    }


    /* --------------------------------------------------------
       INFO
       -------------------------------------------------------- */

    div[data-testid="stAlert"] {
        margin-top: 3px;
        margin-bottom: 5px;
        border-radius: 7px;
    }


    /* --------------------------------------------------------
       FOOTER
       -------------------------------------------------------- */

    .footer-text {
        text-align: center;

        color: #8190a0;

        font-size: 10px;

        margin-top: 2px;
    }


    /* --------------------------------------------------------
       GENERAL SPACING
       -------------------------------------------------------- */

    div[data-testid="stVerticalBlock"] {
        gap: 0.60rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_columns(df):
    result = df.copy()

    result.columns = [
        " ".join(
            str(column)
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("\xa0", " ")
            .strip()
            .split()
        )
        for column in result.columns
    ]

    return (
        result
        .dropna(how="all")
        .reset_index(drop=True)
    )


def to_number(series):
    return pd.to_numeric(
        series.astype(str)
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False),
        errors="coerce",
    ).fillna(0)


def parse_date(value):

    if pd.isna(value):
        return pd.NaT

    text = str(value).strip()

    if text == "":
        return pd.NaT

    # Excel serial date
    try:
        serial = float(text)

        if 20000 <= serial <= 60000:
            return (
                pd.Timestamp("1899-12-30")
                + pd.to_timedelta(
                    serial,
                    unit="D",
                )
            )
    except (TypeError, ValueError):
        pass

    formats = [
        "%d-%b-%y",
        "%d-%b-%Y",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%d-%m-%Y",
        "%d-%m-%y",
        "%Y-%m-%d",
        "%b-%y",
        "%b-%Y",
        "%B-%y",
        "%B-%Y",
        "%b %y",
        "%B %y",
        "%b %Y",
        "%B %Y",
    ]

    for fmt in formats:

        result = pd.to_datetime(
            text,
            format=fmt,
            errors="coerce",
        )

        if not pd.isna(result):
            return result

    return pd.to_datetime(
        text,
        errors="coerce",
        dayfirst=True,
    )


def get_fy(dt):

    if pd.isna(dt):
        return None

    start_year = (
        dt.year
        if dt.month >= 4
        else dt.year - 1
    )

    return (
        f"{start_year}-"
        f"{str(start_year + 1)[-2:]}"
    )


def get_month(dt):

    if pd.isna(dt):
        return None

    return dt.strftime("%B")


def current_fy():

    today = date.today()

    start_year = (
        today.year
        if today.month >= 4
        else today.year - 1
    )

    return (
        f"{start_year}-"
        f"{str(start_year + 1)[-2:]}"
    )


def load_sheet(sheet_name):

    url = (
        "https://docs.google.com/spreadsheets/d/"
        + GOOGLE_SHEET_ID
        + "/gviz/tq?"
        + "tqx=out:csv&sheet="
        + quote(sheet_name)
    )

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    if not response.text.strip():
        raise ValueError(
            f"Google Sheet tab '{sheet_name}' is empty."
        )

    return clean_columns(
        pd.read_csv(
            io.StringIO(
                response.text
            )
        )
    )


def check_columns(
    dataframe,
    required,
    sheet_name,
):

    missing = [
        column
        for column in required
        if column not in dataframe.columns
    ]

    if missing:

        st.error(
            f"Missing columns in '{sheet_name}'."
        )

        st.write(
            "Missing columns:",
            missing,
        )

        st.write(
            "Columns actually found:",
            list(dataframe.columns),
        )

        st.stop()


def apply_filters(
    dataframe,
    selected_year,
    selected_month,
    selected_department,
):

    result = dataframe[
        dataframe["Financial Year"]
        == selected_year
    ].copy()

    if selected_month != "All":

        result = result[
            result["Month Name"]
            == selected_month
        ]

    if selected_department != "All":

        result = result[
            result["Department"]
            == selected_department
        ]

    return result


def render_table(
    dataframe,
    height=300,
    min_width=600,
):

    if dataframe.empty:

        st.info(
            "No data available."
        )

        return

    header = "".join(
        f"<th>{escape(str(column))}</th>"
        for column in dataframe.columns
    )

    rows = []

    for _, row in dataframe.iterrows():

        cells = []

        for value in row:

            if pd.isna(value):
                text = ""
            else:
                text = str(value)

            cells.append(
                f"<td>{escape(text)}</td>"
            )

        rows.append(
            "<tr>"
            + "".join(cells)
            + "</tr>"
        )

    html = (
        f'<div class="table-scroll" '
        f'style="height:{height}px;">'
        f'<table class="dashboard-table" '
        f'style="min-width:{min_width}px;">'
        f'<thead><tr>{header}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        f'</table></div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def common_plot_layout(
    height,
    left=50,
    right=10,
    top=12,
    bottom=45,
):

    return dict(
        height=height,
        margin=dict(
            l=left,
            r=right,
            t=top,
            b=bottom,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )


# ============================================================
# LOAD SHEETS
# ============================================================

try:

    soc_df = load_sheet(
        SOC_SHEET
    )

    interlock_df = load_sheet(
        INTERLOCK_SHEET
    )

    alarm_df = load_sheet(
        ALARM_SHEET
    )

except Exception as error:

    st.error(
        "Unable to load the Google Sheet."
    )

    st.code(
        str(error)
    )

    st.warning(
        "Set the Google Sheet to "
        "Anyone with the link → Viewer."
    )

    st.stop()


# ============================================================
# SOC PREPARATION
# ============================================================

check_columns(
    soc_df,
    [
        "Month",
        "Department",
        "SOC Deviation",
        "SOL Deviation",
        "Remarks",
    ],
    SOC_SHEET,
)


soc_df["Department"] = (
    soc_df["Department"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

soc_df["Month Date"] = (
    soc_df["Month"]
    .apply(parse_date)
)

soc_df["Financial Year"] = (
    soc_df["Month Date"]
    .apply(get_fy)
)

soc_df["Month Name"] = (
    soc_df["Month Date"]
    .apply(get_month)
)

soc_df["SOC Deviation"] = (
    to_number(
        soc_df["SOC Deviation"]
    )
)

soc_df["SOL Deviation"] = (
    to_number(
        soc_df["SOL Deviation"]
    )
)

soc_df["Remarks"] = (
    soc_df["Remarks"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# INTERLOCK PREPARATION
# ============================================================

check_columns(
    interlock_df,
    [
        "Department",
        "Interlock Description",
        "Date Bypassed",
    ],
    INTERLOCK_SHEET,
)


interlock_df["Department"] = (
    interlock_df["Department"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

interlock_df["Bypassed Date"] = (
    interlock_df["Date Bypassed"]
    .apply(parse_date)
)

interlock_df["Financial Year"] = (
    interlock_df["Bypassed Date"]
    .apply(get_fy)
)

interlock_df["Month Name"] = (
    interlock_df["Bypassed Date"]
    .apply(get_month)
)

interlock_df["Days Open"] = (
    pd.Timestamp(date.today())
    - interlock_df["Bypassed Date"]
).dt.days

interlock_df["Days Open"] = (
    interlock_df["Days Open"]
    .fillna(0)
    .clip(lower=0)
    .astype(int)
)


# ============================================================
# ALARM PREPARATION
# ============================================================

check_columns(
    alarm_df,
    [
        "Month",
        "Department",
        "Process Alarms",
        "System Alarms",
        "No. of Class 1 Alarms",
        "No. of Class 2 Alarms",
        "No. of Class 3 Alarms",
        "No. of Class 4 Alarms",
    ],
    ALARM_SHEET,
)


alarm_df["Department"] = (
    alarm_df["Department"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

alarm_df["Month Date"] = (
    alarm_df["Month"]
    .apply(parse_date)
)

alarm_df["Financial Year"] = (
    alarm_df["Month Date"]
    .apply(get_fy)
)

alarm_df["Month Name"] = (
    alarm_df["Month Date"]
    .apply(get_month)
)


ALARM_COLUMNS = [
    "Process Alarms",
    "System Alarms",
    "No. of Class 1 Alarms",
    "No. of Class 2 Alarms",
    "No. of Class 3 Alarms",
    "No. of Class 4 Alarms",
]


for column in ALARM_COLUMNS:

    alarm_df[column] = (
        to_number(
            alarm_df[column]
        )
    )


# ============================================================
# FILTER OPTIONS
# ============================================================

CURRENT_FY = current_fy()

def fy_start_year(fy_value):
    try:
        return int(str(fy_value).split("-")[0])
    except (ValueError, IndexError):
        return date.today().year


def fy_month_labels(fy_value):
    start_year = fy_start_year(fy_value)
    labels = []

    for index, month in enumerate(FY_MONTHS):
        year = start_year if index <= 8 else start_year + 1
        labels.append(f"{month[:3]}-{str(year)[-2:]}")

    return labels


all_years = set()

for dataframe in [
    soc_df,
    interlock_df,
    alarm_df,
]:

    all_years.update(
        dataframe["Financial Year"]
        .dropna()
        .astype(str)
        .tolist()
    )


def year_key(value):

    try:
        return int(
            str(value).split("-")[0]
        )
    except (ValueError, IndexError):
        return 0


all_years = sorted(
    all_years,
    key=year_key,
    reverse=True,
)


if CURRENT_FY not in all_years:

    all_years.insert(
        0,
        CURRENT_FY,
    )


all_departments = set()

for dataframe in [
    soc_df,
    interlock_df,
    alarm_df,
]:

    all_departments.update(
        dataframe["Department"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


all_departments = sorted(
    department
    for department in all_departments
    if department
    and department.lower() != "nan"
)


# ============================================================
# FILTERS
# ============================================================

year_col, month_col, dept_col = (
    st.columns(
        3,
        gap="small",
    )
)


with year_col:

    selected_year = st.selectbox(
        "Year",
        all_years,
        index=all_years.index(
            CURRENT_FY
        ),
    )


with month_col:

    month_display_options = ["All"] + fy_month_labels(selected_year)

    selected_month_display = st.selectbox(
        "Month",
        month_display_options,
        index=0,
    )

    if selected_month_display == "All":
        selected_month = "All"
    else:
        selected_month = FY_MONTHS[
            month_display_options.index(selected_month_display) - 1
        ]


with dept_col:

    selected_department = st.selectbox(
        "Department",
        ["All"] + all_departments,
        index=0,
    )


# ============================================================
# FILTERED DATA
# ============================================================

soc = apply_filters(
    soc_df,
    selected_year,
    selected_month,
    selected_department,
)

interlock = apply_filters(
    interlock_df,
    selected_year,
    selected_month,
    selected_department,
)

alarm = apply_filters(
    alarm_df,
    selected_year,
    selected_month,
    selected_department,
)


MONTH_DISPLAY = {
    month: label
    for month, label in zip(
        FY_MONTHS,
        fy_month_labels(selected_year),
    )
}


# ============================================================
# THREE COLUMNS
# ============================================================

left, middle, right = st.columns(
    3,
    gap="small",
)


# ============================================================
# LEFT: SOC SOL
# ============================================================

with left:
    with st.container(key="soc-panel"):

        st.markdown(
            '<div class="section-header">'
            'SOC & SOL Deviation'
            '</div>',
            unsafe_allow_html=True,
        )


        soc_total = int(
            soc["SOC Deviation"].sum()
        )

        sol_total = int(
            soc["SOL Deviation"].sum()
        )


        k1, k2 = st.columns(2)

        with k1:

            st.metric(
                "SOC Deviation",
                f"{soc_total:,}",
            )

        with k2:

            st.metric(
                "SOL Deviation",
                f"{sol_total:,}",
            )


        st.markdown(
            '<div class="sub-title">'
            'Monthwise SOC &amp; SOL Deviation'
            '</div>',
            unsafe_allow_html=True,
        )


        # --------------------------------------------------------
        # SUM EVERY DEPARTMENT FOR EACH MONTH
        # --------------------------------------------------------

        soc_monthly = (
            soc
            .groupby(
                "Month Name",
                as_index=False,
            )
            .agg(
                {
                    "SOC Deviation": "sum",
                    "SOL Deviation": "sum",
                }
            )
            .rename(
                columns={
                    "Month Name": "Month"
                }
            )
        )


        # --------------------------------------------------------
        # ALWAYS PREPARE APRIL -> MARCH
        # Missing / upcoming months = 0
        # --------------------------------------------------------

        soc_monthly = (
            pd.DataFrame(
                {
                    "Month": FY_MONTHS
                }
            )
            .merge(
                soc_monthly,
                on="Month",
                how="left",
            )
        )


        soc_monthly[
            "SOC Deviation"
        ] = (
            soc_monthly[
                "SOC Deviation"
            ]
            .fillna(0)
        )


        soc_monthly[
            "SOL Deviation"
        ] = (
            soc_monthly[
                "SOL Deviation"
            ]
            .fillna(0)
        )


        soc_chart = soc_monthly.copy()


        if selected_month != "All":

            soc_chart = soc_chart[
                soc_chart["Month"]
                == selected_month
            ]


        maximum = max(
            float(
                soc_chart[
                    "SOC Deviation"
                ].max()
            ),
            float(
                soc_chart[
                    "SOL Deviation"
                ].max()
            ),
            0.0,
        )


        soc_ymax = (
            1
            if maximum == 0
            else maximum * 1.15
        )


        fig_soc = go.Figure()


        soc_x_labels = (
            soc_chart["Month"]
            .map(MONTH_DISPLAY)
            .tolist()
        )


        fig_soc.add_trace(
            go.Scatter(
                x=soc_x_labels,
                y=soc_chart[
                    "SOC Deviation"
                ],
                mode="lines+markers",
                name="SOC Deviation",
                line=dict(width=3),
                marker=dict(size=6),
            )
        )


        fig_soc.add_trace(
            go.Scatter(
                x=soc_x_labels,
                y=soc_chart[
                    "SOL Deviation"
                ],
                mode="lines+markers",
                name="SOL Deviation",
                line=dict(width=3),
                marker=dict(size=6),
            )
        )


        layout = common_plot_layout(
            height=300,
            left=48,
            right=8,
            top=38,
            bottom=58,
        )

        layout.update(
            xaxis=dict(
                title="",
                type="category",
                categoryorder="array",
                categoryarray=fy_month_labels(selected_year),
                tickmode="array",
                tickvals=fy_month_labels(selected_year),
                ticktext=fy_month_labels(selected_year),
                tickangle=-45,
                automargin=True,
            ),
            yaxis=dict(
                range=[
                    0,
                    soc_ymax,
                ],
                rangemode="tozero",
            ),
            legend=dict(
                orientation="h",
                y=1.08,
                x=0.5,
                xanchor="center",
                font=dict(size=11),
            ),
            hovermode="x unified",
        )


        fig_soc.update_layout(**layout)


        with st.container(key="soc-line-chart"):
            st.plotly_chart(
                fig_soc,
                use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": False,
            },
        )


        # --------------------------------------------------------
        # TABLE
        # IMPORTANT:
        # ALL 12 MONTHS ARE PREPARED.
        # UPCOMING MONTHS SHOW 0.
        # --------------------------------------------------------

        st.markdown(
            '<div class="sub-title">'
            'Months with Deviation'
            '</div>',
            unsafe_allow_html=True,
        )


        soc_table_data = (
            soc
            .groupby(
                "Month Name",
                as_index=False,
            )
            .agg(
                {
                    "SOC Deviation": "sum",
                    "SOL Deviation": "sum",
                }
            )
            .rename(
                columns={
                    "Month Name": "Month"
                }
            )
        )


        soc_remarks = (
            soc
            .groupby(
                "Month Name"
            )["Remarks"]
            .apply(
                lambda values:
                ", ".join(
                    sorted(
                        {
                            str(value).strip()
                            for value in values
                            if str(value).strip()
                            and str(value).strip().lower()
                            not in {
                                "",
                                "nan",
                                "none",
                                "-"
                            }
                        }
                    )
                )
            )
            .reset_index()
            .rename(
                columns={
                    "Month Name": "Month"
                }
            )
        )


        soc_table_data = soc_table_data.merge(
            soc_remarks,
            on="Month",
            how="left",
        )


        # --------------------------------------------------------
        # FORCE ALL MONTHS INTO TABLE
        # --------------------------------------------------------

        soc_table = (
            pd.DataFrame(
                {
                    "Month": FY_MONTHS
                }
            )
            .merge(
                soc_table_data,
                on="Month",
                how="left",
            )
        )


        soc_table[
            "SOC Deviation"
        ] = (
            soc_table[
                "SOC Deviation"
            ]
            .fillna(0)
            .astype(int)
        )


        soc_table[
            "SOL Deviation"
        ] = (
            soc_table[
                "SOL Deviation"
            ]
            .fillna(0)
            .astype(int)
        )


        soc_table["Remarks"] = (
            soc_table["Remarks"]
            .fillna("-")
            .replace("", "-")
        )


        if selected_month != "All":

            soc_table = soc_table[
                soc_table["Month"]
                == selected_month
            ]


        soc_table = soc_table[
            [
                "Month",
                "SOC Deviation",
                "SOL Deviation",
                "Remarks",
            ]
        ]


        soc_table["Month"] = soc_table["Month"].map(MONTH_DISPLAY)

        render_table(
            soc_table,
            height=364,
            min_width=570,
        )


# ============================================================
# MIDDLE: INTERLOCK
# ============================================================

with middle:
    with st.container(key="interlock-panel"):

        st.markdown(
            '<div class="section-header">'
            'Interlock Bypass'
            '</div>',
            unsafe_allow_html=True,
        )


        pending_count = len(
            interlock
        )


        st.metric(
            "Normalization Pending",
            f"{pending_count:,}",
        )


        st.markdown(
            '<div class="sub-title">'
            'Pending for Normalization by Department'
            '</div>',
            unsafe_allow_html=True,
        )


        if interlock.empty:

            st.info(
                "No interlock is pending for normalization."
            )

        else:

            department_counts = (
                interlock
                .groupby(
                    "Department",
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size":
                        "Pending"
                    }
                )
            )


            fig_interlock = go.Figure(
                data=[
                    go.Pie(
                        labels=department_counts[
                            "Department"
                        ],
                        values=department_counts[
                            "Pending"
                        ],
                        hole=0.56,

                        # NUMBER ONLY
                        textinfo="value",

                        textposition="inside",

                        domain=dict(
                            x=[
                                0.00,
                                0.58
                            ],
                            y=[
                                0.00,
                                1.00
                            ]
                        ),

                        insidetextorientation="horizontal",
                    )
                ]
            )


            fig_interlock.update_layout(
                height=270,

                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0,
                ),

                paper_bgcolor="white",

                legend=dict(
                    orientation="v",

                    x=0.62,
                    y=0.5,

                    xanchor="left",
                    yanchor="middle",

                    font=dict(
                        size=9
                    )
                ),

                annotations=[
                    dict(
                        text=(
                            f"<b>{pending_count}</b>"
                            "<br>Pending"
                        ),
                        x=0.29,
                        y=0.50,
                        xref="paper",
                        yref="paper",
                        xanchor="center",
                        yanchor="middle",
                        showarrow=False,
                        font=dict(
                            size=16
                        )
                    )
                ],
            )


            st.plotly_chart(
                fig_interlock,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )


        st.markdown(
            '<div class="sub-title">'
            'List of Interlock Bypass - Normalization Pending'
            '</div>',
            unsafe_allow_html=True,
        )


        if interlock.empty:

            st.info(
                "No interlock is pending for normalization."
            )

        else:

            interlock_table = (
                interlock[
                    [
                        "Department",
                        "Interlock Description",
                        "Bypassed Date",
                        "Days Open",
                    ]
                ]
                .copy()
            )


            interlock_table = (
                interlock_table
                .rename(
                    columns={
                        "Bypassed Date":
                        "Date Bypassed"
                    }
                )
            )


            interlock_table[
                "Date Bypassed"
            ] = (
                interlock_table[
                    "Date Bypassed"
                ]
                .dt.strftime(
                    "%d-%b-%y"
                )
            )


            interlock_table = (
                interlock_table
                .sort_values(
                    "Days Open",
                    ascending=False,
                )
            )


            render_table(
                interlock_table,
                height=394,
                min_width=620,
            )


# ============================================================
# RIGHT: ALARM
# ============================================================

with right:
    with st.container(key="alarm-panel"):

        st.markdown(
            '<div class="section-header">'
            'Alarm Management'
            '</div>',
            unsafe_allow_html=True,
        )


        process_total = int(
            alarm[
                "Process Alarms"
            ].sum()
        )


        system_total = int(
            alarm[
                "System Alarms"
            ].sum()
        )


        c1, c2 = st.columns(2)


        with c1:

            st.metric(
                "Process Alarms",
                f"{process_total:,}",
            )


        with c2:

            st.metric(
                "System Alarms",
                f"{system_total:,}",
            )


        class1 = int(
            alarm[
                "No. of Class 1 Alarms"
            ].sum()
        )


        class2 = int(
            alarm[
                "No. of Class 2 Alarms"
            ].sum()
        )


        class3 = int(
            alarm[
                "No. of Class 3 Alarms"
            ].sum()
        )


        class4 = int(
            alarm[
                "No. of Class 4 Alarms"
            ].sum()
        )


        # ========================================================
        # CLASS 1-4 - SINGLE ROW
        # ========================================================

        class1_col, class2_col, class3_col, class4_col = (
            st.columns(
                4,
                gap="small",
            )
        )


        with class1_col:

            st.metric(
                "Class 1",
                f"{class1:,}",
            )


        with class2_col:

            st.metric(
                "Class 2",
                f"{class2:,}",
            )


        with class3_col:

            st.metric(
                "Class 3",
                f"{class3:,}",
            )


        with class4_col:

            st.metric(
                "Class 4",
                f"{class4:,}",
            )


        st.markdown(
            '<div class="sub-title">'
            'Alarm Distribution by Class'
            '</div>',
            unsafe_allow_html=True,
        )


        class_values = [
            class1,
            class2,
            class3,
            class4,
        ]


        total_alarms = sum(
            class_values
        )


        if total_alarms == 0:

            st.info(
                "No alarm class data available."
            )

        else:

            # ----------------------------------------------------
            # DONUT:
            # ACTUAL NUMBERS, NOT PERCENTAGES
            # ----------------------------------------------------

            fig_alarm_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Class 1",
                            "Class 2",
                            "Class 3",
                            "Class 4",
                        ],
                        values=class_values,

                        hole=0.57,

                        textinfo="value",

                        textposition="inside",

                        domain=dict(
                            x=[
                                0.02,
                                0.98
                            ]
                        ),

                        insidetextorientation="horizontal",
                    )
                ]
            )


            fig_alarm_donut.update_layout(
                height=245,

                margin=dict(
                    l=5,
                    r=5,
                    t=0,
                    b=28,
                ),

                paper_bgcolor="white",

                legend=dict(
                    orientation="h",
                    y=-0.02,
                    x=0.5,
                    xanchor="center",
                    font=dict(
                        size=10
                    ),
                ),

                annotations=[
                    dict(
                        text=(
                            f"<b>"
                            f"{total_alarms:,}"
                            f"</b><br>Total"
                        ),
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(
                            size=15
                        ),
                    )
                ],
            )


            st.plotly_chart(
                fig_alarm_donut,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )


        # --------------------------------------------------------
        # ALARM TREND
        # --------------------------------------------------------

        st.markdown(
            '<div class="sub-title">'
            'Monthwise Alarm Distribution'
            '</div>',
            unsafe_allow_html=True,
        )


        alarm_monthly = (
            alarm
            .groupby(
                "Month Name",
                as_index=False,
            )
            .agg(
                {
                    "No. of Class 1 Alarms":
                        "sum",

                    "No. of Class 2 Alarms":
                        "sum",

                    "No. of Class 3 Alarms":
                        "sum",

                    "No. of Class 4 Alarms":
                        "sum",
                }
            )
            .rename(
                columns={
                    "Month Name":
                    "Month"
                }
            )
        )


        # --------------------------------------------------------
        # FORCE ALL 12 MONTHS
        # --------------------------------------------------------

        alarm_monthly = (
            pd.DataFrame(
                {
                    "Month": FY_MONTHS
                }
            )
            .merge(
                alarm_monthly,
                on="Month",
                how="left",
            )
        )


        for column in [
            "No. of Class 1 Alarms",
            "No. of Class 2 Alarms",
            "No. of Class 3 Alarms",
            "No. of Class 4 Alarms",
        ]:

            alarm_monthly[column] = (
                alarm_monthly[column]
                .fillna(0)
            )


        if selected_month != "All":

            alarm_chart = alarm_monthly[
                alarm_monthly["Month"]
                == selected_month
            ].copy()

        else:

            alarm_chart = (
                alarm_monthly.copy()
            )


        max_alarm = max(
            float(
                alarm_chart[
                    "No. of Class 1 Alarms"
                ].max()
            ),
            float(
                alarm_chart[
                    "No. of Class 2 Alarms"
                ].max()
            ),
            float(
                alarm_chart[
                    "No. of Class 3 Alarms"
                ].max()
            ),
            float(
                alarm_chart[
                    "No. of Class 4 Alarms"
                ].max()
            ),
            0.0,
        )


        alarm_ymax = (
            1
            if max_alarm == 0
            else max_alarm * 1.15
        )


        fig_alarm_trend = go.Figure()


        for column, label in [
            (
                "No. of Class 1 Alarms",
                "Class 1",
            ),
            (
                "No. of Class 2 Alarms",
                "Class 2",
            ),
            (
                "No. of Class 3 Alarms",
                "Class 3",
            ),
            (
                "No. of Class 4 Alarms",
                "Class 4",
            ),
        ]:

            fig_alarm_trend.add_trace(
                go.Scatter(
                    x=alarm_chart["Month"].map(MONTH_DISPLAY),
                    y=alarm_chart[column],
                    mode="lines+markers",
                    name=label,
                    line=dict(
                        width=3
                    ),
                    marker=dict(
                        size=5
                    ),
                )
            )


        layout = common_plot_layout(
            height=300,
            left=50,
            right=8,
            top=38,
            bottom=62,
        )


        layout.update(
            xaxis=dict(
                title="",
                type="category",
                categoryorder="array",
                categoryarray=fy_month_labels(selected_year),
                tickmode="array",
                tickvals=fy_month_labels(selected_year),
                ticktext=fy_month_labels(selected_year),
                tickangle=-45,
                automargin=True,
            ),

            yaxis=dict(
                               # ALWAYS START AT ZERO
                range=[
                    0,
                    alarm_ymax
                ],

                rangemode="tozero",
            ),

            legend=dict(
                orientation="h",
                y=1.08,
                x=0.5,
                xanchor="center",
                font=dict(
                    size=10
                ),
            ),

            hovermode="x unified",
        )


        fig_alarm_trend.update_layout(
            **layout
        )


        with st.container(key="alarm-line-chart"):
            st.plotly_chart(
                fig_alarm_trend,
                use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": False,
            },
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer-text">
        Financial Year: {escape(str(selected_year))}
        &nbsp; | &nbsp;
        Month: {escape(str(selected_month_display))}
        &nbsp; | &nbsp;
        Department: {escape(str(selected_department))}
        &nbsp; | &nbsp;
        Auto refresh: {REFRESH_SECONDS}s
    </div>
    """,
    unsafe_allow_html=True,
)

