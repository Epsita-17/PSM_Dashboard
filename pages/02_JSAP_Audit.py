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
    width: 100% !important;
    max-width: 1900px !important;
    padding: 0 1.25rem 0.5rem 1.25rem !important;
    margin-top: -8px !important;
    overflow: visible !important;
}


    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    iframe {
    display: block !important;
    margin-top: -10px !important;
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

                JSW SAFETY ASSURANCE PROTOCOL (JSAP) AUDIT

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
    /* Reduce blank space reserved below the header */
    div[data-testid="stVerticalBlock"] > div:has(> iframe) {
        margin-bottom: -30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



import re
import json
from io import StringIO
from html import escape

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="JSAP Audit Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEET_URLS = {
    "JSAP": (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        "/gviz/tq?tqx=out:csv&sheet=JSAP"
    ),
    "JSAP Audit Compliance": (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        "/gviz/tq?tqx=out:csv&sheet=JSAP%20Audit%20Compliance"
    ),
}

BLUE = "#0645C0"
RED = "#FF1717"
GREEN = "#07983A"

PANEL_HEIGHT = 500
REPORT_TABLE_HEIGHT = 390
CHART_HEIGHT = 320
CHART_FRAME_HEIGHT = 345

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700;800&display=swap');

    html, body {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stApp {
        background: #FFFFFF;
        color: #0645C0;
        font-family: Roboto, Arial, sans-serif;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer {
        display: none !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding: 0 12px 16px !important;
        margin-top: 0 !important;
    }

    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        gap: 12px !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(
        .performance-panel-marker
    ),
    [data-testid="stVerticalBlockBorderWrapper"]:has(
        .reports-panel-marker
    ) {
        height: 500px !important;
        min-height: 500px !important;
        max-height: 500px !important;
        box-sizing: border-box !important;
        border: 1px solid #D4D7DC !important;
        border-radius: 11px !important;
        padding: 10px !important;
        background: #FFFFFF !important;
        overflow: hidden !important;
        flex: 0 0 500px !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(
        .performance-panel-marker
    ) > [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"]:has(
        .reports-panel-marker
    ) > [data-testid="stVerticalBlock"] {
        height: 100% !important;
        min-height: 0 !important;
        max-height: 100% !important;
        gap: 0 !important;
        overflow: hidden !important;
    }

    .performance-panel-marker,
    .reports-panel-marker {
        display: none !important;
    }

    .section-title {
        font-size: clamp(21px, 1.8vw, 29px);
        line-height: 1.15;
        font-weight: 800;
        color: #0645C0;
        margin: 0 0 10px 0;
        padding: 0;
    }

    .scale-card {
        height: 52px;
        width: 100%;
        box-sizing: border-box;
        border-radius: 9px;
        text-align: center;
        padding: 4px 2px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        line-height: 1.35;
        font-size: 11px;
    }

    .scale-card strong {
        font-size: 13px;
        font-weight: 800;
    }

    .scale-red {
        background: #FFF0F2;
        color: #F01420;
        border: 1px solid #FFE0E3;
    }

    .scale-orange {
        background: #FFF5EE;
        color: #CB4D00;
        border: 1px solid #FFE8DA;
    }

    .scale-yellow {
        background: #FFF9E8;
        color: #BA6500;
        border: 1px solid #FFEFCB;
    }

    .scale-blue {
        background: #EDF6FF;
        color: #0645C0;
        border: 1px solid #D6EBFF;
    }

    .scale-green {
        background: #ECFBF5;
        color: #007D56;
        border: 1px solid #D1F4E7;
    }

    .report-table-container {
        width: 100%;
        height: 390px;
        max-height: 390px;
        overflow-y: auto;
        overflow-x: auto;
        border: 1px solid #C8E4FF;
        border-radius: 9px;
        box-sizing: border-box;
        background: #FFFFFF;
        scrollbar-color: #8CB5FF #EDF6FF;
    }

    .report-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
        font-size: 12px;
        color: #0645C0;
        text-align: center;
    }

    .report-table th,
    .report-table td {
        padding: 7px 5px;
        height: 37px;
        box-sizing: border-box;
        border-right: 1px solid #D7E9FF;
        border-bottom: 1px solid #D7E9FF;
        vertical-align: middle;
        overflow-wrap: anywhere;
    }

    .report-table th {
        position: sticky;
        top: 0;
        z-index: 5;
        background: #EAF5FF;
        color: #0645C0;
        font-weight: 800;
    }

    .report-table th:last-child,
    .report-table td:last-child {
        border-right: none;
    }

    .report-link {
        display: inline-block;
        padding: 6px 9px;
        min-width: 95px;
        max-width: 100%;
        box-sizing: border-box;
        border-radius: 8px;
        background: #0645C0;
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 11px;
        text-decoration: none !important;
        white-space: nowrap;
    }

    .report-link:hover {
        background: #00358F;
    }

    .report-unavailable {
        color: #8292BD;
        font-size: 11px;
    }

    .observation-heading {
        color: #0645C0;
        font-size: clamp(22px, 2vw, 32px);
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
        padding: 0;
    }

    div[data-testid="stSelectbox"] label {
        display: none !important;
    }

    div[data-testid="stSelectbox"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        min-height: 34px !important;
        height: 34px !important;
        border: 1px solid #8CB5FF !important;
        border-radius: 7px !important;
        background: #FFFFFF !important;
        font-size: 13px !important;
        box-shadow: none !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        min-height: 34px !important;
        height: 34px !important;
        font-size: 13px !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] span {
        font-size: 13px !important;
    }

    .kpi-card {
        height: 94px;
        min-height: 94px;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid;
        border-radius: 9px;
        padding: 5px 3px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        overflow-wrap: anywhere;
    }

    .kpi-label {
        min-height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(9px, 0.82vw, 12px);
        line-height: 1.3;
        font-weight: 800;
    }

    .kpi-value {
        font-size: clamp(24px, 2.3vw, 38px);
        font-weight: 800;
        line-height: 1.1;
        margin: 2px 0;
    }

    .kpi-subtitle {
        font-size: clamp(9px, 0.9vw, 13px);
        line-height: 1.25;
    }

    .kpi-blue {
        background: #EAF5FF;
        border-color: #83D0FF;
        color: #0645C0;
    }

    .kpi-purple {
        background: #F5EDFF;
        border-color: #CFA8FF;
        color: #6500B8;
    }

    .kpi-red {
        background: #FFF0F0;
        border-color: #FF9696;
        color: #F01414;
    }

    .kpi-orange {
        background: #FFF9E8;
        border-color: #FFE09A;
        color: #B96700;
    }

    .kpi-green {
        background: #EAFBF6;
        border-color: #9BE8D1;
        color: #087C5C;
    }

    .obs-table-wrap {
        width: 100%;
        max-height: 390px;
        overflow: auto;
        border: 1px solid #D0E8FF;
        border-radius: 8px;
        box-sizing: border-box;
        scrollbar-color: #8CB5FF #EDF6FF;
    }

    .obs-table {
        width: 100%;
        min-width: 1020px;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
        font-size: 12px;
        color: #0645C0;
    }

    .obs-table th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #EAF5FF;
        padding: 10px 7px;
        border-bottom: 1px solid #C9E3FF;
        border-right: 1px solid #D6E9FF;
        font-weight: 800;
        text-align: center;
        white-space: nowrap;
    }

    .obs-table th.left {
        text-align: left;
    }

    .obs-table td {
        padding: 7px 8px;
        border-bottom: 1px solid #D7E9FF;
        border-right: 1px solid #D7E9FF;
        vertical-align: middle;
        line-height: 1.4;
        background: #FFFFFF;
        overflow-wrap: anywhere;
    }

    .obs-table tbody tr:hover td {
        background: #F4FAFF;
    }

    .obs-table th:last-child,
    .obs-table td:last-child {
        border-right: none;
    }

    .obs-table td.serial,
    .obs-table td.department {
        text-align: center;
    }

    .pillar-badge,
    .severity-badge,
    .status-open,
    .status-closed {
        display: block;
        text-align: center;
        border-radius: 7px;
        padding: 6px 3px;
        font-weight: 700;
        font-size: 11px;
        white-space: nowrap;
    }

    .pillar-psm {
        background: #D9EEFF;
        color: #0645C0;
    }

    .pillar-moc {
        background: #D8F7EA;
        color: #00784B;
    }

    .severity-high {
        background: #FFE4E4;
        color: #E50000;
    }

    .severity-medium {
        background: #FFF3D6;
        color: #B75B00;
    }

    .severity-low {
        background: #E3F8F0;
        color: #007A4C;
    }

    .status-open {
        border: 1px solid #FF3838;
        background: #FFF8F8;
        color: #E50000;
    }

    .status-closed {
        border: 1px solid #13A36B;
        background: #F1FFF8;
        color: #007A4C;
    }

    .small-link {
        display: block;
        background: #0645C0;
        color: #FFFFFF !important;
        text-decoration: none !important;
        text-align: center;
        padding: 7px 3px;
        border-radius: 7px;
        font-size: 11px;
        font-weight: 700;
        white-space: nowrap;
    }

    .small-link:hover {
        background: #00358F;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def norm(value):
    return re.sub(r"[^a-z0-9]", "", str(value).strip().lower())


def find_col(df, aliases):
    if df is None or df.empty:
        return None

    columns = {norm(c): c for c in df.columns}

    for alias in aliases:
        if norm(alias) in columns:
            return columns[norm(alias)]

    for alias in aliases:
        key = norm(alias)
        if len(key) < 4:
            continue

        for normalized, original in columns.items():
            if key in normalized or normalized in key:
                return original

    return None


def txt(value, default=""):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    value = str(value).strip()

    if value.lower() in {"nan", "none", "nat", "null", "-"}:
        return default

    return value


def number(value):
    value = txt(value).replace(",", "").replace("%", "")
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group()) if match else None


def pct(n, total):
    return round(n * 100 / total, 1) if total else 0.0


def url_value(value):
    value = txt(value)

    if not value:
        return ""

    match = re.search(r"https?://[^\s<>\"']+", value)

    if not match:
        return ""

    return match.group(0).rstrip(".,);]")


def pillar_value(value):
    value = txt(value).lower()

    if "moc" in value or "management of change" in value:
        return "MOC"

    return "Process Safety"


def severity_value(value):
    value = txt(value).lower()

    if "critical" in value or "high" in value:
        return "High"

    if "medium" in value or "moderate" in value:
        return "Medium"

    if "low" in value or "minor" in value:
        return "Low"

    return "Medium"


def status_value(value):
    if isinstance(value, bool):
        return "Closed" if value else "Open"

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value):
            return "Open"
        return "Closed" if value == 1 else "Open"

    value = txt(value).strip().lower()

    if value in {
        "true", "yes", "y", "1", "closed",
        "complete", "completed", "complied", "implemented",
    }:
        return "Closed"

    if value in {
        "false", "no", "n", "0", "open",
        "pending", "not closed", "in progress",
        "outstanding", "not completed", "not implemented",
    }:
        return "Open"

    if "not closed" in value or "not completed" in value:
        return "Open"

    if "false" in value:
        return "Open"

    if "true" in value:
        return "Closed"

    if any(term in value for term in ["open", "pending", "in progress"]):
        return "Open"

    if any(term in value for term in ["closed", "completed", "complied"]):
        return "Closed"

    return "Open"


def observation_col(df):
    return find_col(
        df,
        [
            "Observation Description",
            "Audit Observation",
            "Observation",
            "Finding Description",
            "Findings",
            "Finding",
            "Issue Description",
            "Non Compliance",
            "Recommendation",
            "Remarks",
        ],
    )


# =========================================================
# GOOGLE SHEETS
# =========================================================
@st.cache_data(ttl=30, show_spinner=False)
def read_sheet(sheet_name):
    response = requests.get(SHEET_URLS[sheet_name], timeout=30)
    response.raise_for_status()

    if "<html" in response.text.lower():
        raise ValueError(
            f"Cannot read {sheet_name}. Check spreadsheet permissions "
            "and the exact Google Sheets tab name."
        )

    df = pd.read_csv(StringIO(response.text), dtype=object)

    df.columns = [
        str(c).strip().replace("\n", " ")
        for c in df.columns
    ]

    return (
        df.dropna(how="all")
        .dropna(axis=1, how="all")
        .reset_index(drop=True)
    )


@st.cache_data(ttl=30, show_spinner=False)
def load_data():
    return (
        read_sheet("JSAP"),
        read_sheet("JSAP Audit Compliance"),
    )


# =========================================================
# OBSERVATION DATA
# =========================================================
def prepare_observations(jsap, compliance):
    desc_col = observation_col(jsap)
    source = jsap.copy() if desc_col else compliance.copy()

    if not desc_col:
        desc_col = observation_col(source)

    columns = [
        "Observation", "Pillar", "Severity",
        "Department", "Compliance", "Compliance Report",
    ]

    if not desc_col:
        return pd.DataFrame(columns=columns)

    pillar_col = find_col(
        source,
        ["Pillar", "Observation Pillar", "PSM Pillar", "Audit Category"],
    )

    severity_col = find_col(
        source,
        ["Severity", "Risk Level", "Observation Severity", "Priority"],
    )

    department_col = find_col(
        source,
        ["Department", "Department Name", "Unit", "Plant", "Area"],
    )

    status_col = find_col(
        source,
        [
            "Compliance Status", "Closure Status", "Observation Status",
            "Action Status", "Compliance", "Complied", "Is Compliant",
            "Is Closed", "Closed", "Status",
        ],
    )

    report_col = find_col(
        source,
        [
            "Compliance Report", "Compliance Report Link",
            "Compliance Report URL", "Compliance Document Link",
            "Compliance Document URL", "Compliance Evidence Link",
            "Compliance Evidence", "Compliance Proof",
            "Closure Evidence Link", "Closure Report Link",
            "Supporting Document Link", "Evidence Link",
            "Document URL", "Document Link",
        ],
    )

    records = []

    for _, row in source.iterrows():
        description = txt(row.get(desc_col))

        if not description:
            continue

        records.append({
            "Observation": description,
            "Pillar": pillar_value(
                row.get(pillar_col) if pillar_col else "Process Safety"
            ),
            "Severity": severity_value(
                row.get(severity_col) if severity_col else "Medium"
            ),
            "Department": (
                txt(row.get(department_col), "All")
                if department_col else "All"
            ),
            "Compliance": status_value(
                row.get(status_col) if status_col else False
            ),
            "Compliance Report": (
                txt(row.get(report_col)) if report_col else ""
            ),
        })

    return (
        pd.DataFrame(records, columns=columns)
        .drop_duplicates(
            subset=["Observation", "Department", "Pillar"],
            keep="first",
        )
        .reset_index(drop=True)
    )


# =========================================================
# AUDIT REPORTS
# =========================================================
def prepare_reports(jsap, compliance):
    date_aliases = [
        "Audit Date", "Audit Period", "Audit Duration",
        "Audit Date Range", "Date of Audit", "Audit Month",
        "Period", "Date",
    ]

    link_aliases = [
        "Audit Report", "Audit Report Link", "Report Link",
        "Report URL", "Document Link", "Report", "URL", "Link",
    ]

    records = []

    for df in (jsap, compliance):
        date_col = find_col(df, date_aliases)
        link_col = find_col(df, link_aliases)

        if not date_col:
            continue

        for _, row in df.iterrows():
            date = txt(row.get(date_col))
            link = txt(row.get(link_col)) if link_col else ""

            if date:
                records.append({
                    "Audit Date": date,
                    "Audit Report": link,
                })

    if not records:
        return pd.DataFrame(columns=["Audit Date", "Audit Report"])

    result = pd.DataFrame(records).drop_duplicates()

    result["_sort_date"] = pd.to_datetime(
        result["Audit Date"],
        errors="coerce",
        dayfirst=True,
    )

    return (
        result.sort_values(
            "_sort_date",
            ascending=False,
            na_position="last",
        )
        .drop(columns="_sort_date")
        .reset_index(drop=True)
    )


# =========================================================
# SCORE DATA
# =========================================================
def prepare_scores(jsap, compliance):
    date_aliases = [
        "Audit Date", "Audit Period", "Audit Date Range",
        "Audit Month", "Date of Audit", "Period", "Date",
    ]

    score_aliases = {
        "Unit Overall Score": [
            "Unit Overall Score", "Overall Audit Score",
            "Overall Score", "JSAP Overall Score",
            "Audit Score", "Overall Compliance Score",
        ],
        "Unit Process Safety Score": [
            "Unit Process Safety Score", "Process Safety Score",
            "PSM Score", "PSM Audit Score",
        ],
        "Unit MOC Score": [
            "Unit MOC Score", "MOC Score",
            "Management of Change Score", "MOC Audit Score",
        ],
    }

    records = []

    for df in (jsap, compliance):
        date_col = find_col(df, date_aliases)

        score_cols = {
            name: find_col(df, aliases)
            for name, aliases in score_aliases.items()
        }

        if not date_col or not any(score_cols.values()):
            continue

        for _, row in df.iterrows():
            date = txt(row.get(date_col))

            if not date:
                continue

            values = {
                name: number(row.get(col)) if col else None
                for name, col in score_cols.items()
            }

            if any(value is not None for value in values.values()):
                records.append({"Audit Date": date, **values})

    columns = [
        "Audit Date",
        "Unit Overall Score",
        "Unit Process Safety Score",
        "Unit MOC Score",
    ]

    if not records:
        return pd.DataFrame(columns=columns)

    return (
        pd.DataFrame(records, columns=columns)
        .drop_duplicates(subset=["Audit Date"], keep="first")
        .reset_index(drop=True)
    )


# =========================================================
# PERFORMANCE GRAPH WITH VERTICAL HOVER LINE + TOOLTIP
# =========================================================
def render_chart(scores):
    series = [
        ("Unit Overall Score", BLUE),
        ("Unit Process Safety Score", RED),
        ("Unit MOC Score", GREEN),
    ]

    labels = (
        scores["Audit Date"].astype(str).tolist()
        if not scores.empty else []
    )

    chart_width = max(760, len(labels) * 115 + 150)
    fig = go.Figure()

    # Main graph traces
    for name, color in series:
        if scores.empty:
            continue

        values = pd.to_numeric(scores[name], errors="coerce")

        if values.notna().sum() == 0:
            continue

        fig.add_trace(
            go.Scatter(
                x=labels,
                y=values.tolist(),
                name=name,
                mode="lines+markers+text",
                line=dict(color=color, width=2.5),
                marker=dict(
                    color=color,
                    size=7,
                    symbol="circle",
                ),
                text=[
                    f"{v:g}" if pd.notna(v) else ""
                    for v in values
                ],
                textposition="top center",
                textfont=dict(color=color, size=10),
                connectgaps=False,
                cliponaxis=False,
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Horizontal legend
    for name, color in series:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                name=name,
                mode="markers",
                marker=dict(
                    color=color,
                    size=9,
                    symbol="circle",
                    line=dict(width=0),
                ),
                showlegend=True,
                hoverinfo="skip",
            )
        )

    if scores.empty:
        fig.add_annotation(
            text="No audit score data available",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
        )

    fig.update_layout(
        width=chart_width,
        height=CHART_HEIGHT,
        autosize=False,
        margin=dict(l=48, r=15, t=65, b=85),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Roboto, Arial, sans-serif",
            size=11,
            color=BLUE,
        ),
        legend=dict(
            orientation="h",
            x=0,
            y=1.19,
            xanchor="left",
            yanchor="bottom",
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
            font=dict(size=11, color=BLUE),
            itemsizing="constant",
        ),
        xaxis=dict(
            type="category",
            categoryorder="array",
            categoryarray=labels,
            tickmode="array",
            tickvals=labels,
            ticktext=labels,
            tickangle=-35,
            tickfont=dict(size=10, color=BLUE),
            automargin=True,
            showgrid=True,
            gridcolor="#D8EBFF",
            griddash="dash",
            showspikes=False,
            fixedrange=True,
        ),
        yaxis=dict(
            range=[0, 100],
            dtick=20,
            automargin=True,
            showgrid=True,
            gridcolor="#D8EBFF",
            griddash="dash",
            tickfont=dict(size=10, color=BLUE),
            zeroline=False,
            fixedrange=True,
        ),
        showlegend=True,
        hovermode=False,
    )

    # Prepare tooltip data for each date
    chart_data = []

    for _, row in scores.iterrows():
        point = {
            "date": str(row["Audit Date"]),
            "scores": [],
        }

        for name, color in series:
            value = pd.to_numeric(
                pd.Series([row.get(name)]),
                errors="coerce",
            ).iloc[0]

            if pd.notna(value):
                point["scores"].append({
                    "name": name,
                    "value": float(value),
                    "color": color,
                })

        chart_data.append(point)

    safe_data = json.dumps(chart_data).replace("</", "<\\/")

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config={
            "displayModeBar": False,
            "responsive": False,
            "scrollZoom": False,
        },
    )

    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; }}

        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #FFFFFF;
            font-family: Roboto, Arial, sans-serif;
        }}

        .chart-scroll {{
            width: 100%;
            height: {CHART_FRAME_HEIGHT}px;
            overflow-x: auto;
            overflow-y: hidden;
            position: relative;
            background: #FFFFFF;
            scrollbar-color: #8CB5FF #EDF6FF;
        }}

        .chart-inner {{
            width: {chart_width}px;
            height: {CHART_HEIGHT}px;
            position: relative;
        }}

        .chart-inner .plotly-graph-div {{
            width: {chart_width}px !important;
            height: {CHART_HEIGHT}px !important;
        }}

        /* Keep a crosshair cursor instead of a pointing hand */
        #chartInner .js-plotly-plot .cursor-pointer,
        #chartInner .js-plotly-plot .nsewdrag,
        #chartInner .js-plotly-plot .draglayer .drag {{
            cursor: crosshair !important;
        }}

        /* Vertical line that follows the hovered audit date */
        .hover-vline {{
            display: none;
            position: absolute;
            width: 1px;
            border-left: 1px dashed #0645C0;
            opacity: 0.85;
            pointer-events: none;
            z-index: 5000;
        }}

        /* Hide Plotly default tooltip */
        .hoverlayer {{
            visibility: hidden !important;
        }}

        .custom-tooltip {{
            display: none;
            position: absolute;
            z-index: 10000;
            pointer-events: none;
            min-width: 230px;
            padding: 9px 10px;
            background: #FFFFFF;
            border: 1px solid #BBD9FF;
            box-shadow: 0 2px 5px rgba(0, 40, 100, 0.08);
            font-size: 12px;
            line-height: 1.4;
        }}

        .tooltip-date {{
            margin-bottom: 7px;
            color: #0645C0;
            font-size: 12px;
            font-weight: 400;
        }}

        .tooltip-row {{
            display: flex;
            align-items: center;
            gap: 7px;
            margin: 5px 0;
            white-space: nowrap;
        }}

        .tooltip-dot {{
            display: inline-block;
            width: 9px;
            height: 9px;
            min-width: 9px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .tooltip-name {{
            font-weight: 700;
        }}

        .tooltip-value {{
            font-weight: 400;
        }}

        .chart-scroll::-webkit-scrollbar {{
            height: 10px;
        }}

        .chart-scroll::-webkit-scrollbar-track {{
            background: #EDF6FF;
            border-radius: 8px;
        }}

        .chart-scroll::-webkit-scrollbar-thumb {{
            background: #8CB5FF;
            border-radius: 8px;
        }}
      </style>
    </head>

    <body>
      <div class="chart-scroll" id="chartScroll">
        <div class="chart-inner" id="chartInner">
          {plot_html}

          <div class="hover-vline" id="hoverVline"></div>
          <div class="custom-tooltip" id="customTooltip"></div>
        </div>
      </div>

      <script>
        const auditPoints = {safe_data};
        const graph = document.querySelector(
            '#chartInner .plotly-graph-div'
        );
        const tooltip = document.getElementById('customTooltip');
        const hoverVline = document.getElementById('hoverVline');
        const chartScroll = document.getElementById('chartScroll');

        function escapeHTML(value) {{
            return String(value).replace(/[&<>"']/g, function(ch) {{
                return {{
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#39;'
                }}[ch];
            }});
        }}

        function findAuditPoint(label) {{
            return auditPoints.find(
                point => point.date === String(label)
            );
        }}

        function hideHoverElements() {{
            tooltip.style.display = 'none';
            hoverVline.style.display = 'none';
        }}

        /*
         * Draw the vertical line at the selected audit-date position.
         * The line spans the graph plotting area, from top to bottom.
         */
        function showVerticalLine(pointIndex) {{
            if (
                !graph ||
                !graph._fullLayout ||
                !graph._fullLayout.xaxis ||
                pointIndex < 0 ||
                pointIndex >= auditPoints.length
            ) {{
                hoverVline.style.display = 'none';
                return;
            }}

            const layout = graph._fullLayout;
            const xaxis = layout.xaxis;

            const plotLeft = layout.margin.l;
            const plotTop = layout.margin.t;
            const plotHeight = layout.height -
                layout.margin.t - layout.margin.b;

            const pointX = plotLeft + xaxis.d2p(pointIndex);

            hoverVline.style.left = pointX + 'px';
            hoverVline.style.top = plotTop + 'px';
            hoverVline.style.height = plotHeight + 'px';
            hoverVline.style.display = 'block';
        }}

        function showTooltip(point, mouseX, mouseY) {{
            if (!point || !point.scores.length) {{
                tooltip.style.display = 'none';
                return;
            }}

            let html =
                '<div class="tooltip-date">' +
                escapeHTML(point.date) +
                '</div>';

            point.scores.forEach(function(score) {{
                html +=
                    '<div class="tooltip-row">' +
                        '<span class="tooltip-dot" style="background:' +
                            score.color + ';"></span>' +
                        '<span>' +
                            '<span class="tooltip-name" style="color:' +
                                score.color + ';">' +
                                escapeHTML(score.name) +
                            '</span>' +
                            '<span class="tooltip-value" style="color:' +
                                score.color + ';">: ' +
                                Number(score.value).toFixed(1) + '%' +
                            '</span>' +
                        '</span>' +
                    '</div>';
            }});

            tooltip.innerHTML = html;
            tooltip.style.display = 'block';

            const scrollLeft = chartScroll.scrollLeft;
            const visibleRight =
                scrollLeft + chartScroll.clientWidth;

            const tipWidth = tooltip.offsetWidth;
            const tipHeight = tooltip.offsetHeight;

            let left = mouseX + 12;
            let top = mouseY + 12;

            if (left + tipWidth > visibleRight - 5) {{
                left = mouseX - tipWidth - 12;
            }}

            left = Math.max(scrollLeft + 4, left);

            if (top + tipHeight > {CHART_HEIGHT} - 4) {{
                top = mouseY - tipHeight - 12;
            }}

            top = Math.max(4, top);

            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';
        }}

        function pointerCoordinates(event) {{
            const graphRect = graph.getBoundingClientRect();
            const scrollRect = chartScroll.getBoundingClientRect();

            return {{
                x: event.clientX - graphRect.left,
                y: event.clientY - graphRect.top,
                tooltipX: event.clientX - scrollRect.left +
                          chartScroll.scrollLeft,
                tooltipY: event.clientY - scrollRect.top
            }};
        }}

        function getNearestPoint(event) {{
            const layout = graph._fullLayout;

            if (!layout || !layout.xaxis || !layout.yaxis) {{
                return null;
            }}

            const pos = pointerCoordinates(event);
            const xaxis = layout.xaxis;
            const yaxis = layout.yaxis;

            const localX = pos.x - layout.margin.l;
            const localY = pos.y - layout.margin.t;

            if (
                localX < 0 ||
                localX > xaxis._length ||
                localY < 0 ||
                localY > yaxis._length
            ) {{
                return null;
            }}

            let nearest = null;
            let nearestIndex = -1;
            let smallestDistance = Infinity;

            auditPoints.forEach(function(point, index) {{
                const px = xaxis.d2p(index);
                const distance = Math.abs(px - localX);

                if (distance < smallestDistance) {{
                    smallestDistance = distance;
                    nearest = point;
                    nearestIndex = index;
                }}
            }});

            /*
             * Only activate near an audit-date position.
             * This prevents the line appearing randomly between dates.
             */
            if (smallestDistance > 18) {{
                return null;
            }}

            return {{
                point: nearest,
                index: nearestIndex,
                x: pos.tooltipX,
                y: pos.tooltipY
            }};
        }}

        function attachEvents() {{
            if (!graph || !graph.on) return;

            /*
             * Native Plotly hover event.
             * Keep tooltip and vertical line synchronized.
             */
            graph.on('plotly_hover', function(eventData) {{
                if (
                    !eventData ||
                    !eventData.points ||
                    !eventData.points.length
                ) {{
                    return;
                }}

                const hovered = eventData.points.find(
                    p => p.curveNumber < {len(series)}
                );

                if (!hovered) return;

                const point = findAuditPoint(hovered.x);

                if (!point) {{
                    hideHoverElements();
                    return;
                }}

                const index = auditPoints.findIndex(
                    p => p.date === String(hovered.x)
                );

                showVerticalLine(index);

                let x;
                let y;

                if (eventData.event) {{
                    const rect = chartScroll.getBoundingClientRect();

                    x = eventData.event.clientX - rect.left +
                        chartScroll.scrollLeft;

                    y = eventData.event.clientY - rect.top;
                }} else {{
                    const layout = graph._fullLayout;

                    x = layout.margin.l +
                        hovered.xaxis.d2p(hovered.x) +
                        chartScroll.scrollLeft;

                    y = layout.margin.t +
                        hovered.yaxis.d2p(hovered.y);
                }}

                showTooltip(point, x, y);
            }});

            /*
             * Mouse movement fallback for category-axis graphs.
             * This also ensures the vertical line appears when hovering
             * between the markers of the same audit-date column.
             */
            graph.addEventListener('mousemove', function(event) {{
                const nearest = getNearestPoint(event);

                if (!nearest || !nearest.point) {{
                    hideHoverElements();
                    return;
                }}

                showVerticalLine(nearest.index);

                showTooltip(
                    nearest.point,
                    nearest.x,
                    nearest.y
                );
            }});

            graph.addEventListener(
                'mouseleave',
                hideHoverElements
            );

            chartScroll.addEventListener(
                'scroll',
                hideHoverElements
            );
        }}

        if (graph && graph.on) {{
            attachEvents();
        }} else {{
            window.addEventListener('load', attachEvents);
        }}
      </script>
    </body>
    </html>
    """

    components.html(
        html_doc,
        height=CHART_FRAME_HEIGHT + 4,
        scrolling=False,
    )


# =========================================================
# AUDIT REPORT TABLE
# =========================================================
def make_report_table(reports):
    rows = []

    for _, row in reports.iterrows():
        date = escape(txt(row["Audit Date"], "—"))
        link = url_value(row["Audit Report"])

        if link:
            action = (
                f'<a class="report-link" '
                f'href="{escape(link, quote=True)}" '
                'target="_blank" rel="noopener noreferrer">'
                'View Report</a>'
            )
        else:
            action = (
                '<span class="report-unavailable">'
                'No Report Attached</span>'
            )

        rows.append(f"<tr><td>{date}</td><td>{action}</td></tr>")

    if not rows:
        rows.append(
            '<tr><td colspan="2">No audit reports available</td></tr>'
        )

    return f"""
    <div class="report-table-container">
      <table class="report-table">
        <colgroup>
          <col style="width:50%">
          <col style="width:50%">
        </colgroup>
        <thead>
          <tr>
            <th>Audit Date</th>
            <th>Audit Report</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """


def render_report_table(reports):
    table = make_report_table(reports)

    html_doc = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; }}

        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: white;
            font-family: Roboto, Arial, sans-serif;
            overflow: hidden;
        }}

        .report-table-container {{
            width: 100%;
            height: {REPORT_TABLE_HEIGHT}px;
            max-height: {REPORT_TABLE_HEIGHT}px;
            overflow-y: auto;
            overflow-x: auto;
            border: 1px solid #C8E4FF;
            border-radius: 9px;
            scrollbar-color: #8CB5FF #EDF6FF;
        }}

        .report-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            table-layout: fixed;
            font-size: 12px;
            color: #0645C0;
            text-align: center;
        }}

        .report-table th,
        .report-table td {{
            padding: 7px 5px;
            height: 37px;
            border-right: 1px solid #D7E9FF;
            border-bottom: 1px solid #D7E9FF;
            vertical-align: middle;
            overflow-wrap: anywhere;
        }}

        .report-table th {{
            position: sticky;
            top: 0;
            z-index: 5;
            background: #EAF5FF;
            color: #0645C0;
            font-weight: 800;
        }}

        .report-table th:last-child,
        .report-table td:last-child {{
            border-right: none;
        }}

        .report-link {{
            display: inline-block;
            padding: 6px 9px;
            min-width: 95px;
            border-radius: 8px;
            background: #0645C0;
            color: white !important;
            font-weight: 700;
            font-size: 11px;
            text-decoration: none !important;
            white-space: nowrap;
        }}

        .report-unavailable {{
            color: #8292BD;
            font-size: 11px;
        }}
      </style>
    </head>
    <body>{table}</body>
    </html>
    """

    components.html(
        html_doc,
        height=REPORT_TABLE_HEIGHT + 4,
        scrolling=False,
    )


# =========================================================
# KPI CARDS
# =========================================================
def kpi_html(label, value, subtitle, css_class):
    return (
        f'<div class="kpi-card {css_class}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-subtitle">{subtitle}</div>'
        '</div>'
    )


# =========================================================
# OBSERVATION TABLE
# =========================================================
def make_observation_table(data):
    rows = []

    for i, (_, row) in enumerate(data.iterrows(), start=1):
        pillar = pillar_value(row["Pillar"])
        severity = severity_value(row["Severity"])
        status = status_value(row["Compliance"])

        pillar_class = (
            "pillar-moc" if pillar == "MOC" else "pillar-psm"
        )

        severity_class = {
            "High": "severity-high",
            "Medium": "severity-medium",
            "Low": "severity-low",
        }[severity]

        status_class = (
            "status-closed" if status == "Closed" else "status-open"
        )

        link = url_value(row["Compliance Report"])

        if link:
            report = (
                f'<a class="small-link" '
                f'href="{escape(link, quote=True)}" '
                'target="_blank" rel="noopener noreferrer">'
                'View Report</a>'
            )
        else:
            report = (
                '<span class="report-unavailable">'
                'No Report Attached</span>'
            )

        rows.append(
            f'<tr>'
            f'<td class="serial">{i}</td>'
            f'<td>{escape(txt(row["Observation"], "—"))}</td>'
            f'<td><span class="pillar-badge {pillar_class}">'
            f'{pillar}</span></td>'
            f'<td><span class="severity-badge {severity_class}">'
            f'{severity}</span></td>'
            f'<td class="department">'
            f'{escape(txt(row["Department"], "—"))}</td>'
            f'<td><span class="{status_class}">{status}</span></td>'
            f'<td>{report}</td>'
            f'</tr>'
        )

    if not rows:
        rows.append(
            '<tr><td colspan="7" '
            'style="text-align:center;padding:20px">'
            'No observations available for the selected department.'
            '</td></tr>'
        )

    return f"""
    <div class="obs-table-wrap">
      <table class="obs-table">
        <colgroup>
          <col style="width:6.8%">
          <col style="width:40.5%">
          <col style="width:10.6%">
          <col style="width:8.5%">
          <col style="width:10%">
          <col style="width:10%">
          <col style="width:13.6%">
        </colgroup>
        <thead>
          <tr>
            <th>S. No.</th>
            <th class="left">Observation</th>
            <th>Pillar</th>
            <th>Severity</th>
            <th>Department</th>
            <th>Compliance</th>
            <th>Compliance Report</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """


# =========================================================
# LOAD DATA
# =========================================================
try:
    jsap_df, compliance_df = load_data()

    observations = prepare_observations(
        jsap_df,
        compliance_df,
    )

    reports = prepare_reports(
        jsap_df,
        compliance_df,
    )

    scores = prepare_scores(
        jsap_df,
        compliance_df,
    )

except Exception as error:
    st.error(
        "Unable to load Google Sheets. Confirm that the spreadsheet "
        "is accessible and that the tab names are exactly 'JSAP' and "
        "'JSAP Audit Compliance'."
    )
    st.code(str(error))
    st.stop()


# =========================================================
# PERFORMANCE + REPORTS
# =========================================================
left_panel, right_panel = st.columns(
    [1.5, 1],
    gap="small",
)

with left_panel:
    with st.container(height=PANEL_HEIGHT, border=True):
        st.markdown(
            '<div class="performance-panel-marker"></div>'
            '<div class="section-title">'
            'JSAP AUDIT PERFORMANCE'
            '</div>',
            unsafe_allow_html=True,
        )

        scale_items = [
            ("&lt; 40%", "Not Acceptable", "scale-red"),
            ("40 – 59%", "Developing", "scale-orange"),
            ("60 – 79%", "Acceptable", "scale-yellow"),
            ("80 – 89%", "Mature", "scale-blue"),
            ("90 – 99%", "Leading", "scale-green"),
            ("100%", "Best Practice", "scale-green"),
        ]

        scale_cols = st.columns(6, gap="small")

        for col, (score, label, css_class) in zip(
            scale_cols,
            scale_items,
        ):
            with col:
                st.markdown(
                    f'<div class="scale-card {css_class}">'
                    f'<strong>{score}</strong>{label}'
                    '</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            "<div style='height:2px'></div>",
            unsafe_allow_html=True,
        )

        render_chart(scores)


with right_panel:
    with st.container(height=PANEL_HEIGHT, border=True):
        st.markdown(
            '<div class="reports-panel-marker"></div>'
            '<div class="section-title">AUDIT REPORTS</div>',
            unsafe_allow_html=True,
        )

        render_report_table(reports)


# =========================================================
# JSAP AUDIT OBSERVATIONS
# =========================================================
st.markdown(
    "<div style='height:5px'></div>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(
        '<div class="observation-heading">'
        'JSAP AUDIT OBSERVATIONS'
        '</div>',
        unsafe_allow_html=True,
    )

    departments = ["All Departments"]

    if not observations.empty:
        departments += sorted({
            txt(value)
            for value in observations["Department"]
            if txt(value) and txt(value) != "All"
        })

    _, filter_col = st.columns([4.5, 1.15], gap="small")

    with filter_col:
        selected_department = st.selectbox(
            "Department",
            departments,
            index=0,
            label_visibility="collapsed",
            key="department_filter",
        )

    filtered = observations.copy()

    if (
        selected_department != "All Departments"
        and not filtered.empty
    ):
        filtered = filtered[
            filtered["Department"].astype(str).str.strip()
            == selected_department
        ].copy()

    total = len(filtered)

    psm_count = (
        int((filtered["Pillar"] == "Process Safety").sum())
        if total else 0
    )

    moc_count = (
        int((filtered["Pillar"] == "MOC").sum())
        if total else 0
    )

    closed_count = (
        int((filtered["Compliance"] == "Closed").sum())
        if total else 0
    )

    high_count = (
        int((filtered["Severity"] == "High").sum())
        if total else 0
    )

    medium_count = (
        int((filtered["Severity"] == "Medium").sum())
        if total else 0
    )

    low_count = (
        int((filtered["Severity"] == "Low").sum())
        if total else 0
    )

    kpis = [
        (
            "TOTAL OBSERVATIONS",
            str(total),
            "Across all audits",
            "kpi-blue",
        ),
        (
            "PROCESS SAFETY-RELATED<br>OBSERVATIONS",
            str(psm_count),
            "Observation points",
            "kpi-blue",
        ),
        (
            "MOC-RELATED<br>OBSERVATIONS",
            str(moc_count),
            "Observation points",
            "kpi-blue",
        ),
        (
            "COMPLIANCE",
            f"{pct(closed_count, total):.1f}%",
            f"{closed_count} of {total} closed",
            "kpi-purple",
        ),
        (
            "HIGH SEVERITY",
            f"{pct(high_count, total):.1f}%",
            f"{high_count} observations",
            "kpi-red",
        ),
        (
            "MEDIUM SEVERITY",
            f"{pct(medium_count, total):.1f}%",
            f"{medium_count} observations",
            "kpi-orange",
        ),
        (
            "LOW SEVERITY",
            f"{pct(low_count, total):.1f}%",
            f"{low_count} observations",
            "kpi-green",
        ),
    ]

    kpi_cols = st.columns(7, gap="small")

    for col, (label, value, subtitle, css_class) in zip(
        kpi_cols,
        kpis,
    ):
        with col:
            st.markdown(
                kpi_html(label, value, subtitle, css_class),
                unsafe_allow_html=True,
            )

    st.markdown(
        "<div style='height:14px'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        make_observation_table(filtered),
        unsafe_allow_html=True,
    )

