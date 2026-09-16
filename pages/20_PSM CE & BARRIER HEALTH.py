import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import re
from urllib.parse import quote
import plotly.graph_objects as go

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PSM CE & Barriers Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
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

                PSM SC & BARRIER HEALTH

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
# AUTO REFRESH
# ============================================================

if st_autorefresh is not None:
    st_autorefresh(
        interval=30_000,
        limit=None,
        key="psm_dashboard_refresh"
    )


# ============================================================
# GOOGLE SHEET
# ============================================================

SHEET_ID = (
    "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
)

SHEET_NAMES = [
    "PSM CE",
    "Barrier Audit",
    "Failure Data"
]


# ============================================================
# FILTER OPTIONS
# ============================================================

FY_OPTIONS = [
    "FY 2026-27",
    "FY 2025-26"
]

MONTHS = [
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar"
]

MONTH_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

FULL_MONTH_MAP = {
    "january": "Jan",
    "february": "Feb",
    "march": "Mar",
    "april": "Apr",
    "may": "May",
    "june": "Jun",
    "july": "Jul",
    "august": "Aug",
    "september": "Sep",
    "october": "Oct",
    "november": "Nov",
    "december": "Dec"
}


# ============================================================
# REQUIRED COLUMNS
# ============================================================

PSM_FAILED_COLUMN = (
    "No. of PSM CE failed (Breakdown)"
)

Z10_FAILED_COLUMN = (
    "No. of Equipment declared failed after testing "
    "(Z10 Notification)"
)

MECH_GENERATED_COLUMN = (
    "Compliance of PSM CE MO – Mechanical – Generated"
)

MECH_COMPLETED_COLUMN = (
    "Compliance of PSM CE MO – Mechanical – Completed"
)

EI_GENERATED_COLUMN = (
    "Compliance of PSM CE MO – E&I – Generated"
)

EI_COMPLETED_COLUMN = (
    "Compliance of PSM CE MO – E&I – Completed"
)

BARRIER_PLAN_COLUMN = (
    "Barrier Audit Conducted (Plan)"
)

BARRIER_ACTUAL_COLUMN = (
    "Barrier Audit Conducted (Actual)"
)

BARRIER_ASSESSED_COLUMN = (
    "Barrier Health (C4/C5) (Number) Assessed"
)

BARRIER_UNACCEPTABLE_COLUMN = (
    "Barrier Health (C4/C5) (Number) Unacceptable"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================================================
       GLOBAL / PAGE
       ========================================================= */
    .stApp {
        background: #fcfdff !important;
    }

    .main .block-container {
        max-width: 1700px;
        padding-top: 0.25rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
    }

    header[data-testid="stHeader"],
    footer,
    #MainMenu {
        display: none !important;
    }

    /* Deliberately add breathing room between dashboard elements. */
    div[data-testid="stVerticalBlock"] {
        gap: 0.65rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.65rem !important;
    }

    div[data-testid="stElementContainer"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    /* =========================================================
       FILTERS
       ========================================================= */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {
        color: #234a82 !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 40px !important;
        height: 40px !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        border: 1px solid #d2deea !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] span {
        color: #3f4854 !important;
        font-size: 13px !important;
    }

    /* =========================================================
       MAIN SECTION BORDERS
       ========================================================= */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #d4dee8 !important;
        border-radius: 11px !important;
        background: rgba(255,255,255,0.72) !important;
        box-shadow: none !important;
        padding: 10px !important;
    }

    /* Main dashboard sections — same outer height so both
       sections end at exactly the same level. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-marker) {
        height: 1015px !important;
        min-height: 1015px !important;
        max-height: 1015px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        padding-bottom: 12px !important;
    }


    /* Right section: exactly the same outer height as PSM CE. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-marker-right) {
        height: 1015px !important;
        min-height: 1015px !important;
        max-height: 1015px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }

    .section-marker {
        display: none !important;
    }

    /* Prevent Plotly/Streamlit internals from creating an outer
       horizontal scrollbar on the main section. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-marker)
        > div {
        max-width: 100% !important;
        box-sizing: border-box !important;
        min-height: 0 !important;
    }

    /* Both main dashboard sections must end at exactly the same
       vertical level. The fixed height applies only to the outer
       section border; table-scroll remains independently scrollable. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-marker) {
        height: 1015px !important;
        min-height: 1015px !important;
        max-height: 1015px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        padding-bottom: 12px !important;
    }

    /* Only the tables may scroll internally. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-marker)
        .table-scroll {
        overflow-y: auto !important;
    }

    /* =========================================================
       SECTION HEADERS
       ========================================================= */
    .dashboard-section-blue,
    .dashboard-section-red {
        height: 52px;
        display: flex;
        align-items: center;
        padding: 0 16px;
        border-radius: 7px;
        box-sizing: border-box;
        font-size: 27px;
        font-weight: 750;
        letter-spacing: -0.2px;
    }

    .dashboard-section-blue {
        background: #eaf4ff;
        border: 1px solid #c9def3;
        color: #194686;
    }

    .dashboard-section-red {
        background: #fff1f3;
        border: 1px solid #efcdd1;
        color: #df2434;
    }

    /* =========================================================
       KPI CARDS
       ========================================================= */
    .dashboard-kpi {
        position: relative;
        height: 132px;
        box-sizing: border-box;
        background: #ffffff;
        border: 1px solid #d4e0ea;
        border-radius: 8px;
        text-align: center;
        padding: 11px 8px;
        overflow: hidden;
    }

    .dashboard-kpi::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        border-radius: 8px 0 0 8px;
        background: #2d7fca;
    }

    .dashboard-kpi.accent-red::before {
        background: #ed2639;
    }

    .dashboard-kpi.accent-orange::before {
        background: #e39a25;
    }

    .dashboard-kpi.accent-teal::before {
        background: #169b91;
    }

    .dashboard-kpi.accent-blue::before {
        background: #2d7fca;
    }

    /* KPI title uses exactly the same colour as its accent. */
    .dashboard-kpi.accent-red .dashboard-kpi-title {
        color: #ed2639;
    }

    .dashboard-kpi.accent-orange .dashboard-kpi-title {
        color: #e39a25;
    }

    .dashboard-kpi.accent-teal .dashboard-kpi-title {
        color: #169b91;
    }

    .dashboard-kpi.accent-blue .dashboard-kpi-title {
        color: #2d7fca;
    }

    .dashboard-kpi-title {
        font-size: 14px;
        line-height: 1.15;
        font-weight: 700;
        min-height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .dashboard-kpi-red,
    .dashboard-kpi-orange,
    .dashboard-kpi-teal,
    .dashboard-kpi-blue {
        font-size: 44px;
        line-height: 1;
        font-weight: 750;
        margin-top: 12px;
    }

    .dashboard-kpi-red {
        color: #ed2639;
    }

    .dashboard-kpi-orange {
        color: #e39a25;
    }

    .dashboard-kpi-teal {
        color: #169b91;
    }

    .dashboard-kpi-blue {
        color: #2d7fca;
    }

    /* =========================================================
       COMPLIANCE CARD
       ========================================================= */
    .dashboard-compliance {
        height: 132px;
        background: #ffffff;
        border: 1px solid #d4e0ea;
        border-radius: 8px;
        overflow: hidden;
        box-sizing: border-box;
    }

    .compliance-header {
        height: 31px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #eaf4ff;
        border-bottom: 1px solid #d4e2ef;
        color: #194686;
        font-size: 14px;
        font-weight: 700;
    }

    .compliance-body {
        height: 100px;
        display: flex;
    }

    .compliance-half {
        width: 50%;
        text-align: center;
        padding-top: 5px;
        box-sizing: border-box;
    }

    .compliance-half-right {
        border-left: 1px solid #d5e0ea;
    }

    .compliance-name {
        color: #194686;
        font-size: 13px;
        font-weight: 700;
    }

    .compliance-percent-blue,
    .compliance-percent-red {
        font-size: 25px;
        font-weight: 750;
        line-height: 1.05;
    }

    .compliance-percent-blue {
        color: #194b91;
    }

    .compliance-percent-red {
        color: #ed2639;
    }

    .progress-bg {
        height: 10px;
        margin: 5px 14px 5px 14px;
        background: #dce7f1;
        border-radius: 5px;
        overflow: hidden;
    }

    .progress-blue {
        height: 100%;
        background: #2d7fca;
    }

    .progress-red {
        height: 100%;
        background: #ed2639;
    }

    .compliance-count {
        color: #526982;
        font-size: 10px;
    }

    /* =========================================================
       CHART CARDS
       ========================================================= */
    .stPlotlyChart {
        margin: 0 !important;
        position: relative !important;
        top: -12px !important;
    }

    /* Every chart receives its own subtle card border. */
    div[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.section-marker)) {
        background: #ffffff !important;
        border-color: #d5e0e9 !important;
        border-radius: 10px !important;
        padding: 9px 8px 5px 8px !important;
    }

    /* =========================================================
       TABLE CARDS + INTERNAL SCROLL
       ========================================================= */
    .table-wrapper {
        border: 1px solid #d4e0ea;
        border-radius: 9px;
        overflow: hidden;
        background: #ffffff;
    }

    .table-title-blue,
    .table-title-red {
        font-size: 15px;
        font-weight: 700;
        padding: 8px 11px;
        border-bottom: 1px solid #d9e3ec;
    }

    .table-title-blue {
        background: #eaf4ff;
        color: #194686;
    }

    .table-title-red {
        background: #fff1f3;
        color: #df2434;
    }

    .data-table th,
    .data-table th *,
    .barrier-data-table th,
    .barrier-data-table th * {
        font-weight: 700 !important;
    }

    .table-scroll {
        max-height: 250px;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        scrollbar-color: #b8c8d7 transparent;
    }

    .data-table,
    .barrier-data-table {
        width: 100%;
        border-collapse: collapse;
        color: #234a82;
        font-size: 12px;
    }

    .data-table th,
    .barrier-data-table th {
        position: sticky;
        top: 0;
        z-index: 2;
        padding: 7px 5px;
        text-align: center;
        font-weight: 700;
    }

    .data-table th {
        background: #eaf4ff;
        color: #194686 !important;
        border: 1px solid #c9def3;
    }

    .barrier-data-table th {
        background: #fff1f3;
        color: #df2434 !important;
        border: 1px solid #efcdd1;
    }

    .data-table td,
    .barrier-data-table td {
        border: 1px solid #dce5ec;
        padding: 7px 8px;
        background: #ffffff;
        vertical-align: middle;
    }

    .data-table td:first-child,
    .barrier-data-table td:first-child {
        text-align: center;
    }

    .empty-message {
        padding: 18px;
        text-align: center;
        color: #6c7d90;
        background: #ffffff;
        min-height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    /* Explicit visual spacing helpers. */
    .dashboard-gap {
        height: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# COLUMN NORMALIZATION
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    text = str(value)

    text = (
        text
        .replace("\ufeff", "")
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("–", "-")
        .replace("—", "-")
        .replace("-", "-")
        .replace("&", "and")
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip().lower()


def compact_text(value):

    return re.sub(
        r"[^a-z0-9]",
        "",
        normalize_text(value)
    )


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(
    df,
    requested,
    required=True
):

    requested_normalized = normalize_text(
        requested
    )

    requested_compact = compact_text(
        requested
    )

    # Exact normalized
    for column in df.columns:

        if normalize_text(column) == requested_normalized:
            return column

    # Exact compact
    for column in df.columns:

        if compact_text(column) == requested_compact:
            return column

    # Partial
    for column in df.columns:

        current = normalize_text(
            column
        )

        if (
            requested_normalized in current
            or current in requested_normalized
        ):
            return column

    if required:

        raise ValueError(
            f"Column not found: {requested}\n\n"
            f"Available columns:\n"
            + "\n".join(
                [str(x) for x in df.columns]
            )
        )

    return None


# ============================================================
# GOOGLE SHEET LOADER
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def load_sheet(
    sheet_name
):

    encoded_sheet = quote(
        sheet_name
    )

    url = (
        "https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={encoded_sheet}"
    )

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    df = pd.read_csv(
        io.BytesIO(
            response.content
        ),
        dtype=object
    )

    df.columns = [
        str(column)
        .replace("\ufeff", "")
        .strip()
        for column in df.columns
    ]

    # Remove fully blank rows
    df = df.dropna(
        how="all"
    ).reset_index(
        drop=True
    )

    # Replace NaN with empty string
    df = df.fillna("")

    return df


# ============================================================
# NUMERIC CONVERSION
# ============================================================

def to_number(
    value
):

    if pd.isna(value):
        return 0.0

    text = str(value).strip()

    if text == "":
        return 0.0

    # Remove commas
    text = text.replace(
        ",",
        ""
    )

    # Remove percentage sign
    text = text.replace(
        "%",
        ""
    )

    # Handle brackets
    if (
        text.startswith("(")
        and text.endswith(")")
    ):
        text = "-" + text[1:-1]

    number = pd.to_numeric(
        text,
        errors="coerce"
    )

    if pd.isna(number):
        return 0.0

    return float(number)


def numeric_sum(
    df,
    column
):

    if (
        df is None
        or df.empty
        or column is None
    ):
        return 0.0

    return df[column].apply(
        to_number
    ).sum()


# ============================================================
# FINANCIAL YEAR NORMALIZATION
# ============================================================

def normalize_fy(
    value
):

    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text:
        return None

    # Already correct
    match = re.search(
        r"(20\d{2})\s*[-/]\s*(\d{2}|20\d{2})",
        text
    )

    if not match:
        return None

    start_year = int(
        match.group(1)
    )

    end_value = match.group(2)

    if len(end_value) == 2:

        end_year = (
            (start_year // 100) * 100
            + int(end_value)
        )

    else:

        end_year = int(
            end_value
        )

    return (
        f"FY {start_year}-"
        f"{str(end_year)[-2:]}"
    )


# ============================================================
# DATE PARSING
# ============================================================

def parse_date(
    value
):

    if pd.isna(value):
        return pd.NaT

    if isinstance(
        value,
        pd.Timestamp
    ):
        return value

    text = str(value).strip()

    if not text:
        return pd.NaT

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%b-%y",
        "%B-%y",
        "%b-%Y",
        "%B-%Y",
        "%m/%Y",
        "%m-%Y",
        "%Y-%m"
    ]

    for fmt in formats:

        try:

            return pd.to_datetime(
                text,
                format=fmt
            )

        except Exception:
            pass

    return pd.to_datetime(
        text,
        errors="coerce",
        dayfirst=True
    )


# ============================================================
# MONTH NORMALIZATION
# ============================================================

def normalize_month(
    value
):

    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text:
        return None

    lower = text.lower()

    # Full month
    if lower in FULL_MONTH_MAP:
        return FULL_MONTH_MAP[lower]

    # Extract first 3 letters
    first = lower[:3]

    for month in MONTHS:

        if month.lower() == first:
            return month

    # Try date
    parsed = parse_date(
        text
    )

    if not pd.isna(parsed):

        return parsed.strftime(
            "%b"
        )

    return None


# ============================================================
# FIND FY / MONTH / DATE COLUMNS
# ============================================================

def get_fy_column(
    df
):

    candidates = [
        "Financial Year",
        "Financial FY",
        "FY",
        "FY Year",
        "Financial Yr"
    ]

    for candidate in candidates:

        column = find_column(
            df,
            candidate,
            required=False
        )

        if column:
            return column

    return None


def get_month_column(
    df
):

    candidates = [
        "Month",
        "Month Name",
        "Month-Year",
        "Month Year",
        "Financial Month"
    ]

    for candidate in candidates:

        column = find_column(
            df,
            candidate,
            required=False
        )

        if column:
            return column

    return None


def get_date_column(
    df
):

    candidates = [
        "Date",
        "Request Date",
        "Failure Date",
        "Date of Failure",
        "Breakdown Date",
        "Date of Breakdown",
        "Audit Date",
        "Barrier Audit Date"
    ]

    for candidate in candidates:

        column = find_column(
            df,
            candidate,
            required=False
        )

        if column:
            return column

    return None


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(
    df
):

    df = df.copy()

    fy_column = get_fy_column(
        df
    )

    month_column = get_month_column(
        df
    )

    date_column = get_date_column(
        df
    )

    # --------------------------------------------------------
    # EXPLICIT FY
    # --------------------------------------------------------

    if fy_column:

        df["_FY"] = df[
            fy_column
        ].apply(
            normalize_fy
        )

    else:

        df["_FY"] = None

    # --------------------------------------------------------
    # MONTH
    # --------------------------------------------------------

    if month_column:

        df["_Month"] = df[
            month_column
        ].apply(
            normalize_month
        )

    else:

        df["_Month"] = None

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if date_column:

        df["_Date"] = df[
            date_column
        ].apply(
            parse_date
        )

    else:

        df["_Date"] = pd.NaT

    # If Month itself contains a date,
    # use it for _Date where possible.
    if month_column:

        month_dates = df[
            month_column
        ].apply(
            parse_date
        )

        df["_Date"] = (
            df["_Date"]
            .fillna(month_dates)
        )

    # --------------------------------------------------------
    # DERIVE FY ONLY WHEN EXPLICIT FY DOES NOT EXIST
    # --------------------------------------------------------

    missing_fy = df[
        "_FY"
    ].isna()

    if missing_fy.any():

        derived_fy = (
            df.loc[
                missing_fy,
                "_Date"
            ]
            .apply(
                lambda x:
                (
                    None
                    if pd.isna(x)
                    else
                    (
                        f"FY {x.year}-"
                        f"{str(x.year + 1)[-2:]}"
                        if x.month >= 4
                        else
                        f"FY {x.year - 1}-"
                        f"{str(x.year)[-2:]}"
                    )
                )
            )
        )

        df.loc[
            missing_fy,
            "_FY"
        ] = derived_fy

    # --------------------------------------------------------
    # DERIVE MONTH FROM DATE IF NECESSARY
    # --------------------------------------------------------

    missing_month = df[
        "_Month"
    ].isna()

    if missing_month.any():

        df.loc[
            missing_month,
            "_Month"
        ] = df.loc[
            missing_month,
            "_Date"
        ].apply(
            lambda x:
            None
            if pd.isna(x)
            else x.strftime("%b")
        )

    return df


# ============================================================
# FILTER DATA
# ============================================================

def apply_filters(
    df,
    fy,
    month,
    department
):

    result = df.copy()

    # --------------------------------------------------------
    # FINANCIAL YEAR
    # --------------------------------------------------------

    if fy != "All":

        result = result[
            result["_FY"]
            .astype(str)
            .str.strip()
            == fy
        ]

    # --------------------------------------------------------
    # MONTH
    # --------------------------------------------------------

    if month != "All Months":

        month_short = normalize_month(
            month
        )

        result = result[
            result["_Month"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(month_short).lower()
        ]

    # --------------------------------------------------------
    # DEPARTMENT
    # --------------------------------------------------------

    department_column = find_column(
        result,
        "Department",
        required=False
    )

    if (
        department_column
        and department != "All Departments"
    ):

        result = result[
            result[
                department_column
            ]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            department
            .strip()
            .lower()
        ]

    return result


# ============================================================
# DEPARTMENTS
# ============================================================

def get_departments(
    dataframes
):

    values = set()

    for df in dataframes:

        department_column = find_column(
            df,
            "Department",
            required=False
        )

        if department_column:

            for value in df[
                department_column
            ]:

                text = str(
                    value
                ).strip()

                if text:
                    values.add(
                        text
                    )

    return [
        "All Departments"
    ] + sorted(
        values,
        key=lambda x: x.lower()
    )


# ============================================================
# MONTH OPTIONS
# ============================================================

def get_month_options(
    dataframes,
    selected_fy
):

    found = []

    for df in dataframes:

        temp = df[
            df["_FY"]
            .astype(str)
            .str.strip()
            == selected_fy
        ]

        for month in temp[
            "_Month"
        ].dropna():

            month = str(
                month
            ).strip()

            if month in MONTHS:
                found.append(
                    month
                )

    unique = []

    for month in MONTHS:

        if month in found:
            unique.append(
                month
            )

    # If data doesn't contain an FY column,
    # still show all possible months.
    if not unique:
        unique = MONTHS.copy()

    # Display month-year according to selected FY
    start_year = int(
        selected_fy.split()[1].split("-")[0]
    )

    options = [
        "All Months"
    ]

    for month in unique:

        month_number = MONTH_NUMBER[
            month
        ]

        year = (
            start_year
            if month_number >= 4
            else start_year + 1
        )

        options.append(
            f"{month}-{str(year)[-2:]}"
        )

    return options


# ============================================================
# FY MONTH TIMELINE
# ============================================================

def fy_timeline(
    fy
):

    start_year = int(
        fy.split()[1].split("-")[0]
    )

    timeline = []

    for month_number in range(
        4,
        13
    ):

        dt = pd.Timestamp(
            year=start_year,
            month=month_number,
            day=1
        )

        timeline.append(
            {
                "month": dt.strftime(
                    "%b"
                ),
                "date": dt,
                "label": dt.strftime(
                    "%b-%y"
                )
            }
        )

    for month_number in range(
        1,
        4
    ):

        dt = pd.Timestamp(
            year=start_year + 1,
            month=month_number,
            day=1
        )

        timeline.append(
            {
                "month": dt.strftime(
                    "%b"
                ),
                "date": dt,
                "label": dt.strftime(
                    "%b-%y"
                )
            }
        )

    return timeline


# ============================================================
# TREND DATA
# ============================================================

def make_trend(
    df,
    generated_column,
    completed_column,
    fy
):

    timeline = fy_timeline(
        fy
    )

    rows = []

    for item in timeline:

        month = item["month"]

        month_df = df[
            df["_Month"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            month.lower()
        ]

        generated = numeric_sum(
            month_df,
            generated_column
        )

        completed = numeric_sum(
            month_df,
            completed_column
        )

        rows.append(
            {
                "Date": item["date"],
                "Label": item["label"],
                "Generated": generated,
                "Completed": completed
            }
        )

    return pd.DataFrame(
        rows
    )


def make_single_trend(
    df,
    value_column,
    fy
):

    timeline = fy_timeline(
        fy
    )

    rows = []

    for item in timeline:

        month = item["month"]

        month_df = df[
            df["_Month"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            month.lower()
        ]

        value = numeric_sum(
            month_df,
            value_column
        )

        rows.append(
            {
                "Date": item["date"],
                "Label": item["label"],
                "Value": value
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# LINE CHART
# ============================================================

def line_chart(
    data,
    title
):

    maximum = max(
        data["Generated"].max(),
        data["Completed"].max(),
        1
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Generated"],
            mode="lines+markers",
            name="Generated",
            line=dict(
                color="#2584dc",
                width=2
            ),
            marker=dict(
                color="#2584dc",
                size=6
            ),
            hovertemplate=(
                "<b>%{x|%b-%y}</b><br>"
                "Generated: %{y}<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Completed"],
            mode="lines+markers",
            name="Completed",
            line=dict(
                color="#ef2639",
                width=2
            ),
            marker=dict(
                color="#ef2639",
                size=6
            ),
            hovertemplate=(
                "<b>%{x|%b-%y}</b><br>"
                "Completed: %{y}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        height=190,
        margin=dict(
            l=34,
            r=8,
            t=52,
            b=62
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        title=dict(
            text=title,
            x=0.01,
            y=0.88,
            yanchor="top",
            font=dict(
                size=12,
                color="#123d87",
                family="Arial"
            )
        ),
        xaxis=dict(
            type="date",
            tickmode="array",
            tickvals=data["Date"],
            ticktext=data["Label"],
            tickangle=-45,
            automargin=True,
            showgrid=False,
            tickfont=dict(
                size=9,
                color="#123d87"
            )
        ),
        yaxis=dict(
            range=[
                0,
                maximum * 1.20
            ],
            showgrid=True,
            gridcolor="#dce7f3",
            zeroline=False,
            tickfont=dict(
                size=9,
                color="#123d87"
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.79,
            xanchor="right",
            x=1.0,
            font=dict(
                size=9,
                color="#123d87"
            ),
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0
        )
    )

    return fig


# ============================================================
# BAR CHART
# ============================================================

def breakdown_chart(
    data
):

    maximum = max(
        data["Value"].max(),
        1
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["Value"],
            marker_color="#2584dc",
            text=[
                f"{int(x)}"
                if float(x).is_integer()
                else f"{x:g}"
                for x in data["Value"]
            ],
            textposition="outside",
            textfont=dict(
                size=12,
                color="#123d87"
            ),
            hovertemplate=(
                "<b>%{x|%b-%y}</b><br>"
                "Breakdown: %{y}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        height=190,
        margin=dict(
            l=34,
            r=8,
            t=50,
            b=58
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        title=dict(
            text="PSM CE Breakdown",
            x=0.01,
            y=0.88,
            yanchor="top",
            font=dict(
                size=13,
                color="#123d87"
            )
        ),
        xaxis=dict(
            type="date",
            tickmode="array",
            tickvals=data["Date"],
            ticktext=data["Label"],
            tickangle=-45,
            automargin=True,
            tickfont=dict(
                size=9,
                color="#123d87"
            ),
            showgrid=False
        ),
        yaxis=dict(
            range=[
                0,
                maximum * 1.30
            ],
            showgrid=True,
            gridcolor="#dce7f3",
            zeroline=False,
            tickfont=dict(
                size=11,
                color="#123d87"
            )
        ),
        showlegend=False
    )

    return fig


# ============================================================
# BARRIER AUDIT CHART
# ============================================================

def barrier_chart(
    df,
    plan_column,
    actual_column,
    fy
):

    plan = make_single_trend(
        df,
        plan_column,
        fy
    )

    actual = make_single_trend(
        df,
        actual_column,
        fy
    )

    maximum = max(
        plan["Value"].max(),
        actual["Value"].max(),
        1
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plan["Date"],
            y=plan["Value"],
            name="Planned",
            marker_color="#2584dc",
            hovertemplate=(
                "<b>%{x|%b-%y}</b><br>"
                "Planned: %{y}<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Bar(
            x=actual["Date"],
            y=actual["Value"],
            name="Conducted",
            marker_color="#ef2639",
            hovertemplate=(
                "<b>%{x|%b-%y}</b><br>"
                "Conducted: %{y}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        barmode="group",
        height=205,
        margin=dict(
            l=34,
            r=8,
            t=50,
            b=62
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        title=dict(
            text=(
                "Barrier Audit – Planned vs. "
                "Conducted"
            ),
            x=0.01,
            y=0.88,
            yanchor="top",
            font=dict(
                size=13,
                color="#123d87"
            )
        ),
        xaxis=dict(
            type="date",
            tickmode="array",
            tickvals=plan["Date"],
            ticktext=plan["Label"],
            tickangle=-45,
            automargin=True,
            tickfont=dict(
                size=9,
                color="#123d87"
            ),
            showgrid=False
        ),
        yaxis=dict(
            range=[
                0,
                maximum * 1.25
            ],
            showgrid=True,
            gridcolor="#dce7f3",
            zeroline=False,
            tickfont=dict(
                size=11,
                color="#123d87"
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.79,
            xanchor="right",
            x=1.0,
            font=dict(
                size=9,
                color="#123d87"
            ),
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0
        )
    )

    return fig


# ============================================================
# COMPLIANCE
# ============================================================

def compliance_percentage(
    generated,
    completed
):

    if generated <= 0:
        return 0

    return (
        completed
        / generated
        * 100
    )


# ============================================================
# PSM FAILURE TABLE
# ============================================================

def build_psm_failure_html(
    df
):

    category_column = find_column(
        df,
        "PSM CE/Barrier",
        required=False
    )

    if category_column:

        data = df[
            df[
                category_column
            ]
            .astype(str)
            .str.strip()
            .str.lower()
            == "psm ce"
        ].copy()

    else:

        # Compatibility with older sheet headings
        category_column = find_column(
            df,
            "Failure Category",
            required=False
        )

        if category_column:

            data = df[
                df[
                    category_column
                ]
                .astype(str)
                .str.strip()
                .str.lower()
                == "psm ce"
            ].copy()

        else:

            data = df.copy()

    department_column = find_column(
        data,
        "Department",
        required=False
    )

    name_column = find_column(
        data,
        "PSM CE Name",
        required=False
    )

    if name_column is None:

        for candidate in [
            "Equipment Name",
            "Equipment",
            "PSM CE"
        ]:

            name_column = find_column(
                data,
                candidate,
                required=False
            )

            if name_column:
                break

    reason_column = find_column(
        data,
        "Reason of Failure",
        required=False
    )

    if reason_column is None:

        reason_column = find_column(
            data,
            "Remarks",
            required=False
        )

    if reason_column is None:

        reason_column = find_column(
            data,
            "Remarks/Reason of Failure",
            required=False
        )

    if data.empty:

        return (
            '<div class="empty-message">'
            'No PSM CE failure records available.'
            '</div>'
        )

    rows = ""

    for index, (_, row) in enumerate(
        data.iterrows(),
        start=1
    ):

        department = (
            str(
                row[
                    department_column
                ]
            )
            if department_column
            else ""
        )

        name = (
            str(
                row[
                    name_column
                ]
            )
            if name_column
            else ""
        )

        reason = (
            str(
                row[
                    reason_column
                ]
            )
            if reason_column
            else ""
        )

        rows += (
            "<tr>"
            f"<td>{index}</td>"
            f"<td>{department}</td>"
            f"<td>{name}</td>"
            f"<td>{reason}</td>"
            "</tr>"
        )

    return (
        '<table class="data-table">'
        '<thead>'
        '<tr>'
        '<th>Sl. No.</th>'
        '<th>Department</th>'
        '<th>PSM CE Name</th>'
        '<th>Reason of Failure</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
        f'{rows}'
        '</tbody>'
        '</table>'
    )


# ============================================================
# BARRIER FAILURE TABLE
# ============================================================

def build_barrier_failure_html(
    df
):

    category_column = find_column(
        df,
        "PSM CE/Barrier",
        required=False
    )

    if category_column:

        data = df[
            df[
                category_column
            ]
            .astype(str)
            .str.strip()
            .str.lower()
            == "barrier"
        ].copy()

    else:

        category_column = find_column(
            df,
            "Failure Category",
            required=False
        )

        if category_column:

            data = df[
                df[
                    category_column
                ]
                .astype(str)
                .str.strip()
                .str.lower()
                == "barrier"
            ].copy()

        else:

            data = df.copy()

    department_column = find_column(
        data,
        "Department",
        required=False
    )

    barrier_column = find_column(
        data,
        "Barrier Name",
        required=False
    )

    if barrier_column is None:

        for candidate in [
            "Barrier",
            "Barrier Description",
            "Barrier Name"
        ]:

            barrier_column = find_column(
                data,
                candidate,
                required=False
            )

            if barrier_column:
                break

    reason_column = find_column(
        data,
        "Reason of Failure",
        required=False
    )

    if reason_column is None:

        reason_column = find_column(
            data,
            "Remarks",
            required=False
        )

    if reason_column is None:

        reason_column = find_column(
            data,
            "Remarks/Reason of Failure",
            required=False
        )

    if data.empty:

        return (
            '<div class="empty-message">'
            'No unacceptable barrier records available.'
            '</div>'
        )

    rows = ""

    for index, (_, row) in enumerate(
        data.iterrows(),
        start=1
    ):

        department = (
            str(
                row[
                    department_column
                ]
            )
            if department_column
            else ""
        )

        barrier = (
            str(
                row[
                    barrier_column
                ]
            )
            if barrier_column
            else ""
        )

        reason = (
            str(
                row[
                    reason_column
                ]
            )
            if reason_column
            else ""
        )

        rows += (
            "<tr>"
            f"<td>{index}</td>"
            f"<td>{department}</td>"
            f"<td>{barrier}</td>"
            f"<td>{reason}</td>"
            "</tr>"
        )

    return (
        '<table class="barrier-data-table">'
        '<thead>'
        '<tr>'
        '<th>Sl. No.</th>'
        '<th>Department</th>'
        '<th>Barrier Name</th>'
        '<th>Reason of Failure</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
        f'{rows}'
        '</tbody>'
        '</table>'
    )


# ============================================================
# HTML COMPONENT HELPERS
# IMPORTANT:
# Use st.html() instead of st.markdown() for custom HTML.
# This completely prevents HTML source from appearing.
# ============================================================

def render_html(
    html
):
    st.html(html)


# ============================================================
# LOAD DATA
# ============================================================

try:

    psm_df = prepare_data(
        load_sheet(
            "PSM CE"
        )
    )

    barrier_df = prepare_data(
        load_sheet(
            "Barrier Audit"
        )
    )

    failure_df = prepare_data(
        load_sheet(
            "Failure Data"
        )
    )

except Exception as error:

    st.error(
        "Unable to read the Google Sheet."
    )

    st.exception(
        error
    )

    st.stop()


# ============================================================
# FIND REQUIRED METRIC COLUMNS
# ============================================================

try:

    psm_failed_column = find_column(
        psm_df,
        PSM_FAILED_COLUMN
    )

    z10_failed_column = find_column(
        psm_df,
        Z10_FAILED_COLUMN
    )

    mech_generated_column = find_column(
        psm_df,
        MECH_GENERATED_COLUMN
    )

    mech_completed_column = find_column(
        psm_df,
        MECH_COMPLETED_COLUMN
    )

    ei_generated_column = find_column(
        psm_df,
        EI_GENERATED_COLUMN
    )

    ei_completed_column = find_column(
        psm_df,
        EI_COMPLETED_COLUMN
    )

    barrier_plan_column = find_column(
        barrier_df,
        BARRIER_PLAN_COLUMN
    )

    barrier_actual_column = find_column(
        barrier_df,
        BARRIER_ACTUAL_COLUMN
    )

    barrier_assessed_column = find_column(
        barrier_df,
        BARRIER_ASSESSED_COLUMN
    )

    barrier_unacceptable_column = find_column(
        barrier_df,
        BARRIER_UNACCEPTABLE_COLUMN
    )

except Exception as error:

    st.error(
        "A required column is missing from the Google Sheet."
    )

    st.exception(
        error
    )

    st.stop()


# ============================================================
# FILTER OPTIONS
# ============================================================

departments = get_departments(
    [
        psm_df,
        barrier_df,
        failure_df
    ]
)


# ============================================================
# FILTER AREA
# ============================================================

filter1, filter2, filter3 = st.columns(
    [1, 1, 1],
    gap="large"
)

with filter1:

    selected_fy = st.selectbox(
        "Financial Year",
        FY_OPTIONS,
        index=0
    )

with filter2:

    month_options = get_month_options(
        [
            psm_df,
            barrier_df,
            failure_df
        ],
        selected_fy
    )

    selected_month = st.selectbox(
        "Month",
        month_options,
        index=0
    )

with filter3:

    selected_department = st.selectbox(
        "Department",
        departments,
        index=0
    )


# ============================================================
# APPLY FILTERS
# ============================================================

psm_filtered = apply_filters(
    psm_df,
    selected_fy,
    selected_month,
    selected_department
)

barrier_filtered = apply_filters(
    barrier_df,
    selected_fy,
    selected_month,
    selected_department
)

failure_filtered = apply_filters(
    failure_df,
    selected_fy,
    selected_month,
    selected_department
)


# ============================================================
# KPI VALUES
# ============================================================

psm_failed = numeric_sum(
    psm_filtered,
    psm_failed_column
)

z10_failed = numeric_sum(
    psm_filtered,
    z10_failed_column
)

mechanical_generated = numeric_sum(
    psm_filtered,
    mech_generated_column
)

mechanical_completed = numeric_sum(
    psm_filtered,
    mech_completed_column
)

ei_generated = numeric_sum(
    psm_filtered,
    ei_generated_column
)

ei_completed = numeric_sum(
    psm_filtered,
    ei_completed_column
)

mechanical_compliance = compliance_percentage(
    mechanical_generated,
    mechanical_completed
)

ei_compliance = compliance_percentage(
    ei_generated,
    ei_completed
)

barriers_assessed = numeric_sum(
    barrier_filtered,
    barrier_assessed_column
)

unacceptable_barriers = numeric_sum(
    barrier_filtered,
    barrier_unacceptable_column
)


# ============================================================
# MAIN TWO-COLUMN LAYOUT
# ============================================================

left, right = st.columns(
    [2.05, 1.08],
    gap="small"
)


# ============================================================
# LEFT — PSM CE SECTION
# ============================================================

with left:

    # Same-height main section border. The marker is used only by CSS.
    with st.container(border=True):
        st.markdown('<span class="section-marker"></span>', unsafe_allow_html=True)

        render_html(
            '<div class="dashboard-section-blue">'
            'PSM CRITICAL EQUIPMENT'
            '</div>'
        )

        # --------------------------------------------------------
        # KPI ROW
        # --------------------------------------------------------

        kpi1, kpi2, compliance = st.columns(
            [0.82, 0.82, 2.12],
            gap="small"
        )

        with kpi1:
            render_html(
                '<div class="dashboard-kpi accent-red">'
                '<div class="dashboard-kpi-title">'
                'PSM CE Failure'
                '</div>'
                f'<div class="dashboard-kpi-red">{psm_failed:g}</div>'
                '</div>'
            )

        with kpi2:
            render_html(
                '<div class="dashboard-kpi accent-orange">'
                '<div class="dashboard-kpi-title">'
                'Declared Failed<br>(After Testing)'
                '</div>'
                f'<div class="dashboard-kpi-orange">{z10_failed:g}</div>'
                '</div>'
            )

        with compliance:
            mechanical_width = max(0, min(mechanical_compliance, 100))
            ei_width = max(0, min(ei_compliance, 100))

            render_html(
                '<div class="dashboard-compliance">'
                '<div class="compliance-header">'
                'Compliance of PSM CE Notification'
                '</div>'
                '<div class="compliance-body">'
                '<div class="compliance-half">'
                '<div class="compliance-name">Mechanical</div>'
                f'<div class="compliance-percent-blue">{mechanical_compliance:.0f}%</div>'
                '<div class="progress-bg">'
                f'<div class="progress-blue" style="width:{mechanical_width:.1f}%"></div>'
                '</div>'
                f'<div class="compliance-count">{mechanical_completed:g} Completed / {mechanical_generated:g} Generated</div>'
                '</div>'
                '<div class="compliance-half compliance-half-right">'
                '<div class="compliance-name">E&amp;I</div>'
                f'<div class="compliance-percent-red">{ei_compliance:.0f}%</div>'
                '<div class="progress-bg">'
                f'<div class="progress-red" style="width:{ei_width:.1f}%"></div>'
                '</div>'
                f'<div class="compliance-count">{ei_completed:g} Completed / {ei_generated:g} Generated</div>'
                '</div>'
                '</div>'
                '</div>'
            )

        st.markdown('<div class="dashboard-gap"></div>', unsafe_allow_html=True)

        # --------------------------------------------------------
        # MECHANICAL / E&I TRENDS — INDIVIDUAL CHART BORDERS
        # --------------------------------------------------------

        chart1, chart2 = st.columns(
            [1, 1],
            gap="small"
        )

        mechanical_data = make_trend(
            psm_filtered,
            mech_generated_column,
            mech_completed_column,
            selected_fy
        )

        ei_data = make_trend(
            psm_filtered,
            ei_generated_column,
            ei_completed_column,
            selected_fy
        )

        with chart1:
            with st.container(border=True):
                st.plotly_chart(
                    line_chart(
                        mechanical_data,
                        "PSM CE Notification Compliance - Mechanical"
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        with chart2:
            with st.container(border=True):
                st.plotly_chart(
                    line_chart(
                        ei_data,
                        "PSM CE Notification Compliance"
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        st.markdown('<div class="dashboard-gap"></div>', unsafe_allow_html=True)

        # --------------------------------------------------------
        # BREAKDOWN — INDIVIDUAL CHART BORDER
        # --------------------------------------------------------

        breakdown_data = make_single_trend(
            psm_filtered,
            psm_failed_column,
            selected_fy
        )

        with st.container(border=True):
            st.plotly_chart(
                breakdown_chart(breakdown_data),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # --------------------------------------------------------
        # PSM FAILURE DETAILS — INTERNAL SCROLL
        # --------------------------------------------------------

        psm_table = build_psm_failure_html(failure_filtered)

        render_html(
            '<div class="table-wrapper">'
            '<div class="table-title-blue">PSM CE failure details</div>'
            '<div class="table-scroll">'
            f'{psm_table}'
            '</div>'
            '</div>'
        )


# ============================================================
# RIGHT — BARRIERS SECTION
# ============================================================

with right:

    # Same-height main section border as PSM CE.
    with st.container(border=True):
        st.markdown('<span class="section-marker section-marker-right"></span>', unsafe_allow_html=True)

        render_html(
            '<div class="dashboard-section-red">'
            'BARRIER HEALTH (C4/C5)'
            '</div>'
        )

        # --------------------------------------------------------
        # BARRIER KPI ROW
        # --------------------------------------------------------

        barrier1, barrier2 = st.columns(
            [1, 1],
            gap="small"
        )

        with barrier1:
            render_html(
                '<div class="dashboard-kpi accent-teal">'
                '<div class="dashboard-kpi-title">Assessed</div>'
                f'<div class="dashboard-kpi-teal">{barriers_assessed:g}</div>'
                '</div>'
            )

        with barrier2:
            render_html(
                '<div class="dashboard-kpi accent-red">'
                '<div class="dashboard-kpi-title">Unacceptable</div>'
                f'<div class="dashboard-kpi-red">{unacceptable_barriers:g}</div>'
                '</div>'
            )

        st.markdown('<div class="dashboard-gap"></div>', unsafe_allow_html=True)

        # --------------------------------------------------------
        # BARRIER AUDIT — INDIVIDUAL CHART BORDER
        # --------------------------------------------------------

        with st.container(border=True):
            st.plotly_chart(
                barrier_chart(
                    barrier_filtered,
                    barrier_plan_column,
                    barrier_actual_column,
                    selected_fy
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.markdown('<div class="dashboard-gap"></div>', unsafe_allow_html=True)

        # --------------------------------------------------------
        # BARRIER FAILURE DETAILS — INTERNAL SCROLL
        # --------------------------------------------------------

        barrier_table = build_barrier_failure_html(failure_filtered)

        render_html(
            '<div class="table-wrapper">'
            '<div class="table-title-red">Unacceptable Barriers details</div>'
            '<div class="table-scroll">'
            f'{barrier_table}'
            '</div>'
            '</div>'
        )

