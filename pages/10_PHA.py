import streamlit as st
import pandas as pd
import requests
import re
from io import StringIO
from difflib import SequenceMatcher
from html import escape
from html.parser import HTMLParser

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PHA Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
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

                PROCESS HAZARD ANALYSIS(PHA)

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
# GOOGLE SHEET
# ============================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
PHA_SHEET = "PHA"
RECOMMENDATION_SHEET = "PHA RECOMENDATION"

# ============================================================
# COLOURS
# ============================================================

BLUE = "#1769AA"
NAVY = "#0B3A70"
RED = "#D71920"
GREEN = "#159447"
YELLOW = "#D9A400"

WHITE = "#FFFFFF"
TEXT = "#17365D"
MUTED = "#667085"
BORDER = "#D5E2F0"
ROW_ALT = "#F7FAFD"
LIGHT_BLUE = "#F5F9FD"

# ============================================================
# PAGE / UI CSS
# ============================================================

st.markdown(
    f""" 
    <style> 

    /* ---------- Remove Streamlit chrome ---------- */ 

    #MainMenu {{ 
        visibility: hidden; 
    }} 

    header {{ 
        visibility: hidden; 
        height: 0 !important; 
    }} 

    [data-testid="stHeader"] {{ 
        display: none; 
    }} 

    [data-testid="stToolbar"] {{ 
        display: none; 
    }} 

    footer {{ 
        visibility: hidden; 
    }} 

    .stApp {{ 
        background: {WHITE}; 
    }} 

    .main {{ 
        background: {WHITE}; 
    }} 

    .block-container {{ 
        max-width: 100% !important; 
        padding-top: 0.8rem !important; 
        padding-bottom: 1.5rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }} 

    /* ---------- General spacing ---------- */ 

    div[data-testid="stVerticalBlock"] > div {{ 
        gap: 0.55rem; 
    }} 

    /* ---------- Department filter ---------- */ 

    .filter-label {{ 
        color: {NAVY}; 
        font-size: 16px; 
        font-weight: 750; 
        margin: 0 0 5px 0; 
    }} 

    div[data-baseweb="select"] > div {{ 
        min-height: 46px; 
        border-radius: 10px !important; 
        border: 1px solid {BORDER} !important; 
        background: #F5F7FA !important; 
        box-shadow: none !important; 
    }} 

    div[data-baseweb="select"] span {{ 
        color: {TEXT} !important; 
        font-weight: 600 !important; 
    }} 

    /* ---------- Section containers ---------- */ 

    div[data-testid="stVerticalBlockBorderWrapper"] {{ 
        border: 1px solid {BORDER} !important; 
        border-radius: 16px !important; 
        background: {WHITE} !important; 
        box-shadow: 0 3px 12px rgba(11, 58, 112, 0.055) !important; 
        padding: 0.8rem 0.75rem 0.85rem 0.75rem !important; 
        box-sizing: border-box !important; 
    }} 

    .section-title {{ 
        color: {NAVY}; 
        font-size: 21px; 
        font-weight: 800; 
        letter-spacing: 0.1px; 
        margin: 0 0 12px 0; 
    }} 

    /* ---------- KPI cards ---------- */ 

    .kpi-card {{ 
        position: relative; 
        width: 100%; 
        height: 118px; 
        min-height: 118px; 
        max-height: 118px; 
        box-sizing: border-box; 
        background: {WHITE}; 
        border: 1px solid {BORDER}; 
        border-radius: 14px; 
        padding: 14px 14px 12px 23px; 
        overflow: hidden; 
        box-shadow: 0 2px 9px rgba(11, 58, 112, 0.055); 
    }} 

    .kpi-card::before {{ 
        content: ""; 
        position: absolute; 
        left: 0; 
        top: 0; 
        bottom: 0; 
        width: 7px; 
        background: var(--accent); 
        border-radius: 14px 0 0 14px; 
    }} 

    .kpi-label {{ 
        color: var(--accent) !important; 
        font-size: 14px; 
        font-weight: 800; 
        line-height: 1.15; 
        margin: 0 0 5px 0; 
    }} 

    .kpi-value {{ 
        color: var(--accent) !important; 
        font-size: 34px; 
        font-weight: 850; 
        line-height: 1; 
        margin: 0 0 6px 0; 
    }} 

    .kpi-context {{ 
        color: var(--accent) !important; 
        font-size: 11.5px; 
        font-weight: 650; 
        line-height: 1.18; 
        margin: 0; 
    }} 

    /* ---------- KPI section bottom breathing room ---------- */ 

    .kpi-section-spacer {{ 
        height: 12px; 
        width: 100%; 
        display: block; 
    }} 

    /* ---------- Equal KPI column/card height ---------- */ 

    div[data-testid="stHorizontalBlock"] {{ 
        align-items: stretch !important; 
    }} 

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{ 
        display: flex !important; 
        align-items: stretch !important; 
    }} 

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div {{ 
        width: 100%; 
    }} 

    /* ---------- Search ---------- */ 

    div[data-testid="stTextInput"] input {{ 
        min-height: 43px; 
        border-radius: 10px !important; 
        border: 1px solid {BORDER} !important; 
        background: {WHITE} !important; 
        color: {TEXT} !important; 
        box-shadow: none !important; 
    }} 

    div[data-testid="stTextInput"] input::placeholder {{ 
        color: #8A94A6 !important; 
        opacity: 1; 
    }} 

    /* ---------- HTML table ---------- */ 

    .table-scroll {{ 
        width: 100%; 
        max-height: 430px; 
        overflow: auto; 
        border: 1px solid {BORDER}; 
        border-radius: 12px; 
        background: {WHITE}; 
    }} 

    .custom-table {{ 
        width: 100%; 
        border-collapse: separate; 
        border-spacing: 0; 
        table-layout: fixed; 
        font-family: "Segoe UI", Arial, sans-serif; 
        color: {TEXT}; 
        font-size: 12px; 
    }} 

    .custom-table th {{ 
        position: sticky; 
        top: 0; 
        z-index: 5; 
        background: {NAVY}; 
        color: {WHITE}; 
        font-weight: 800; 
        font-size: 11.5px; 
        text-align: left; 
        white-space: nowrap; 
        padding: 8px 10px; 
        height: 44px; 
        min-height: 44px; 
        box-sizing: border-box; 
        border-right: 1px solid #FFFFFF; 
        border-bottom: 1px solid #FFFFFF; 
    }} 

    .custom-table thead th:first-child {{ 
        border-top-left-radius: 8px; 
    }} 

    .custom-table thead th:last-child {{ 
        border-top-right-radius: 8px; 
    }} 

    .custom-table td {{ 
        color: {TEXT}; 
        font-weight: 550; 
        font-size: 12px; 
        padding: 9px 12px; 
        border-right: 1px solid {BORDER}; 
        border-bottom: 1px solid {BORDER}; 
        vertical-align: middle; 
        white-space: normal; 
        overflow-wrap: anywhere; 
        word-break: break-word; 
        line-height: 1.35; 
        background: {WHITE}; 
        min-width: 80px; 
    }} 

    .custom-table tbody tr:nth-child(even) td {{ 
        background: {ROW_ALT}; 
    }} 

    .custom-table th:last-child, 
    .custom-table td:last-child {{ 
        border-right: none; 
    }} 

    /* ---------- Unavailable document text ---------- */ 

    .document-none {{ 
        color: #98A2B3 !important; 
        font-size: 10.5px; 
        font-weight: 400; 
        opacity: 0.75; 
        white-space: nowrap; 
    }} 

    /* ---------- Simple status text ---------- */ 

    .status-simple {{ 
        color: {TEXT} !important; 
        font-size: inherit; 
        font-weight: inherit; 
        line-height: inherit; 
        white-space: normal; 
        background: transparent !important; 
        padding: 0; 
        margin: 0; 
    }} 

    /* ---------- Recommendation register column widths ---------- */ 

    /* Keep supporting columns compact and give Recommendation more space. */ 
    #pha-recommendation-table .custom-table th:nth-child(1), 
    #pha-recommendation-table .custom-table td:nth-child(1) {{ 
        width: 65px; 
        min-width: 65px; 
        max-width: 65px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(2), 
    #pha-recommendation-table .custom-table td:nth-child(2) {{ 
        width: 420px; 
        min-width: 420px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(3), 
    #pha-recommendation-table .custom-table td:nth-child(3) {{ 
        width: 105px; 
        min-width: 105px; 
        max-width: 105px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(4), 
    #pha-recommendation-table .custom-table td:nth-child(4) {{ 
        width: 115px; 
        min-width: 115px; 
        max-width: 115px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(5), 
    #pha-recommendation-table .custom-table td:nth-child(5) {{ 
        width: 80px; 
        min-width: 80px; 
        max-width: 80px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(6), 
    #pha-recommendation-table .custom-table td:nth-child(6) {{ 
        width: 95px; 
        min-width: 95px; 
        max-width: 95px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(7), 
    #pha-recommendation-table .custom-table td:nth-child(7) {{ 
        width: 95px; 
        min-width: 95px; 
        max-width: 95px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(8), 
    #pha-recommendation-table .custom-table td:nth-child(8) {{ 
        width: 75px; 
        min-width: 75px; 
        max-width: 75px; 
    }} 

    #pha-recommendation-table .custom-table th:nth-child(9), 
    #pha-recommendation-table .custom-table td:nth-child(9) {{ 
        width: 120px; 
        min-width: 120px; 
        max-width: 120px; 
    }} 

    /* ---------- Scrollbar ---------- */ 

    .table-scroll::-webkit-scrollbar {{ 
        width: 9px; 
        height: 9px; 
    }} 

    .table-scroll::-webkit-scrollbar-track {{ 
        background: #F1F4F8; 
        border-radius: 8px; 
    }} 

    .table-scroll::-webkit-scrollbar-thumb {{ 
        background: #B7C7D9; 
        border-radius: 8px; 
    }} 

    .table-scroll::-webkit-scrollbar-thumb:hover {{ 
        background: #8FA7C0; 
    }} 

    /* ---------- Footer ---------- */ 

    .footer {{ 
        text-align: center; 
        color: #98A2B3; 
        font-size: 11px; 
        padding-top: 12px; 
    }} 

    </style> 
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(sheet_name):
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={sheet_name}"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")
        df.columns = [str(c).strip() for c in df.columns]

        return df

    except Exception as exc:
        st.error(
            f"Unable to load '{sheet_name}'. "
            f"Please check Google Sheet sharing/access. Details: {exc}"
        )
        st.stop()

    # ============================================================


# HELPERS
# ============================================================

def _normalize_column_name(value):
    """
    Normalize column names so small differences such as:
    - spaces
    - underscores
    - hyphens
    - brackets
    - slash spacing
    - punctuation
    do not prevent matching.
    """
    text = str(value).strip().lower()

    # Common wording variations
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = text.replace("\\", " ")
    text = text.replace("_", " ")
    text = text.replace("-", " ")

    # Remove brackets and punctuation
    text = re.sub(r"[\(\)\[\]\{\}:;,.]", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def find_column(df, names):
    """
    Find a column using:
    1. Exact normalized match
    2. Strong substring match
    3. Token overlap
    4. Sequence similarity

    This is deliberately tolerant because Google Sheet headers may
    contain slightly different wording than the expected names.
    """

    columns = list(df.columns)

    if not columns:
        return None

    normalized_columns = {
        col: _normalize_column_name(col)
        for col in columns
    }

    normalized_targets = [
        _normalize_column_name(name)
        for name in names
    ]

    # --------------------------------------------------------
    # 1. Exact normalized match
    # --------------------------------------------------------
    for target in normalized_targets:
        for col, normalized_col in normalized_columns.items():
            if normalized_col == target:
                return col

                # --------------------------------------------------------
    # 2. Strong substring match
    # --------------------------------------------------------
    for target in normalized_targets:
        if len(target) < 5:
            continue

        for col, normalized_col in normalized_columns.items():
            if target in normalized_col or normalized_col in target:
                return col

                # --------------------------------------------------------
    # 3. Token overlap
    # --------------------------------------------------------
    best_col = None
    best_score = 0.0

    for target in normalized_targets:
        target_tokens = set(target.split())

        if not target_tokens:
            continue

        for col, normalized_col in normalized_columns.items():
            col_tokens = set(normalized_col.split())

            if not col_tokens:
                continue

            intersection = len(target_tokens & col_tokens)
            union = len(target_tokens | col_tokens)

            jaccard = intersection / union if union else 0

            # Give additional importance to the important words
            # appearing in the same column.
            containment = (
                intersection / len(target_tokens)
                if target_tokens else 0
            )

            score = (jaccard * 0.45) + (containment * 0.55)

            if score > best_score:
                best_score = score
                best_col = col

                # --------------------------------------------------------
    # 4. Sequence similarity
    # --------------------------------------------------------
    sequence_col = None
    sequence_score = 0.0

    for target in normalized_targets:
        for col, normalized_col in normalized_columns.items():
            score = SequenceMatcher(
                None,
                target,
                normalized_col
            ).ratio()

            if score > sequence_score:
                sequence_score = score
                sequence_col = col

                # Prefer token match if reasonably strong; otherwise use
    # sequence similarity when it is clearly a close match.
    if best_score >= 0.58:
        return best_col

    if sequence_score >= 0.62:
        return sequence_col

    return None


def get_department_column(df):
    return find_column(
        df,
        ["Department", "Dept", "Department Name", "Dept Name"]
    )


def get_status_column(df):
    return find_column(
        df,
        ["Status", "PHA Status", "Recommendation Status"]
    )


def get_status_series(df):
    col = get_status_column(df)

    if col is None:
        return pd.Series("", index=df.index, dtype="object")

    return (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def render_kpi(label, value, context, accent):
    st.markdown(
        f""" 
        <div class="kpi-card" style="--accent:{accent};"> 
            <div class="kpi-label">{escape(str(label))}</div> 
            <div class="kpi-value">{escape(str(value))}</div> 
            <div class="kpi-context">{escape(str(context))}</div> 
        </div> 
        """,
        unsafe_allow_html=True
    )


def status_text_class(value):
    """Return the normal table-text class for every status."""
    return "status-simple"


class GoogleSheetLinkParser(HTMLParser):
    """Extract hyperlink targets from Google Sheets HTML output."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = None
        self.current_cell = None
        self.current_href = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "tr":
            self.current_row = []

        elif tag in ("td", "th") and self.current_row is not None:
            self.current_cell = {"text": [], "href": None}
            self.current_href = None
            self.current_text = []

        elif tag == "a" and self.current_cell is not None:
            self.current_href = attrs.get("href")

        elif tag == "br" and self.current_cell is not None:
            self.current_text.append(" ")

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.current_cell is not None:
            text = " ".join("".join(self.current_text).split())
            self.current_cell["text"] = text
            self.current_cell["href"] = self.current_href

            if self.current_row is not None:
                self.current_row.append(self.current_cell)

            self.current_cell = None
            self.current_href = None
            self.current_text = []

        elif tag == "tr" and self.current_row is not None:
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = None


@st.cache_data(ttl=300, show_spinner=False)
def load_document_links(sheet_name):
    """Read hyperlink targets from a Google Sheet tab."""
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:html&sheet={sheet_name}"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        parser = GoogleSheetLinkParser()
        parser.feed(response.text)

        if not parser.rows:
            return []

        headers = [
            cell["text"].strip()
            for cell in parser.rows[0]
        ]

        header_df = pd.DataFrame(columns=headers)

        document_col = find_column(
            header_df,
            ["Upload Document", "Document", "PHA Document"]
        )

        if document_col is None:
            return []

        document_index = headers.index(document_col)
        links = []

        for row in parser.rows[1:]:
            if document_index < len(row):
                links.append(row[document_index].get("href"))
            else:
                links.append(None)

        return links

    except Exception:
        return []


def extract_url(value):
    """Extract a direct URL or HYPERLINK URL from a cell value."""
    text = safe_text(value)

    if not text:
        return None

    direct = re.search(r"https?://[^\s\"<>]+", text)
    if direct:
        return direct.group(0).rstrip(".,;)")

    hyperlink = re.search(
        r'HYPERLINK\s*\(\s*"([^"]+)"',
        text,
        flags=re.IGNORECASE
    )
    if hyperlink:
        return hyperlink.group(1)

    return None


def render_html_table(
        df,
        table_id,
        document_links=None,
        document_column="Document"
):
    """
    Responsive HTML table with:
    - internal vertical scrolling
    - internal horizontal scrolling
    - sticky header
    - wrapped text
    - dark navy header with white bold text
    - optional View button for document links
    """

    if df.empty:
        st.markdown(
            """ 
            <div style=" 
                padding: 25px; 
                text-align: center; 
                color: #667085; 
                border: 1px solid #D5E2F0; 
                border-radius: 12px; 
                background: #FFFFFF; 
                font-size: 13px; 
            "> 
                No records found. 
            </div> 
            """,
            unsafe_allow_html=True
        )
        return

    headers = "".join(
        f"<th>{escape(str(col))}</th>"
        for col in df.columns
    )

    rows = []

    for row_position, (_, row) in enumerate(df.iterrows()):
        cells = []

        for col in df.columns:

            # ------------------------------------------------
            # Special Document column
            # ------------------------------------------------
            if str(col).strip().lower() == document_column.lower():

                link = None

                if document_links is not None:
                    if row_position < len(document_links):
                        link = document_links[row_position]

                        # Fallback: if the displayed cell itself contains
                # a URL / HYPERLINK formula.
                if not link:
                    link = extract_url(row[col])

                if link:
                    cell_html = (
                        f'<a class="document-view-btn" '
                        f'href="{escape(link, quote=True)}" '
                        f'target="_blank" rel="noopener noreferrer">'
                        f'View</a>'
                    )
                else:
                    cell_html = (
                        '<span class="document-none">Report unavailable</span>'
                    )

                cells.append(f"<td>{cell_html}</td>")
                continue

            value = safe_text(row[col])
            css_class = ""

            normalized_col = _normalize_column_name(col)

            if normalized_col in {
                "status",
                "pha status",
                "recommendation status",
                "status ongoing completed",
                "progress status"
            }:
                # Render status as a fixed-size rounded badge with
                # white text. All status badges use identical
                # dimensions.
                text_class = status_text_class(value)

                if value:
                    cell_html = (
                        f'<span class="{text_class}">'
                        f'{escape(value)}'
                        f'</span>'
                    )
                else:
                    cell_html = ""

                cells.append(
                    f'<td>{cell_html}</td>'
                )
            else:
                cells.append(
                    f'<td>{escape(value)}</td>'
                )

        rows.append(
            "<tr>" + "".join(cells) + "</tr>"
        )

    html = f""" 
    <div class="table-scroll" id="{escape(table_id)}"> 
        <table class="custom-table"> 
            <thead> 
                <tr>{headers}</tr> 
            </thead> 
            <tbody> 
                {''.join(rows)} 
            </tbody> 
        </table> 
    </div> 
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def filter_dataframe(df, search_text):
    if not search_text:
        return df

    search_text = search_text.strip()

    if not search_text:
        return df

    mask = df.astype(str).apply(
        lambda col: col.str.contains(
            search_text,
            case=False,
            na=False,
            regex=False
        )
    ).any(axis=1)

    return df[mask]


# ============================================================
# LOAD ONLY PHA + PHA RECOMENDATION
# ============================================================

pha_df = load_google_sheet(PHA_SHEET)
rec_df = load_google_sheet(RECOMMENDATION_SHEET)

# ============================================================
# DEPARTMENT FILTER
# ============================================================

pha_dept_col = get_department_column(pha_df)
rec_dept_col = get_department_column(rec_df)

all_departments = []

if pha_dept_col:
    all_departments.extend(
        pha_df[pha_dept_col]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

if rec_dept_col:
    all_departments.extend(
        rec_df[rec_dept_col]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

departments = sorted(
    {
        d for d in all_departments
        if d and d.lower() != "nan"
    }
)

# ============================================================
# DEPARTMENT FILTER - NO EXTRA BOX AROUND IT
# ============================================================

filter_col, _ = st.columns([1.15, 4.85])

with filter_col:
    st.markdown(
        '<div class="filter-label">Department</div>',
        unsafe_allow_html=True
    )

    selected_department = st.selectbox(
        "Department",
        ["All Departments"] + departments,
        label_visibility="collapsed"
    )

# ============================================================
# APPLY FILTER
# ============================================================

filtered_pha = pha_df.copy()
filtered_rec = rec_df.copy()

if selected_department != "All Departments":

    if pha_dept_col:
        filtered_pha = filtered_pha[
            filtered_pha[pha_dept_col]
            .astype(str)
            .str.strip()
            == selected_department
            ]

    if rec_dept_col:
        filtered_rec = filtered_rec[
            filtered_rec[rec_dept_col]
            .astype(str)
            .str.strip()
            == selected_department
            ]

    # ============================================================
# PHA KPI CALCULATIONS
# ============================================================

pha_status = get_status_series(filtered_pha)

total_pha = len(filtered_pha)

completed_pha = int(
    pha_status.str.contains(
        "completed|complete|closed",
        regex=True,
        na=False
    ).sum()
)

ongoing_pha = int(
    pha_status.str.contains(
        "ongoing|open|progress|pending",
        regex=True,
        na=False
    ).sum()
)

# Make sure KPI totals remain consistent.
if completed_pha + ongoing_pha < total_pha:
    ongoing_pha += total_pha - completed_pha - ongoing_pha

# ============================================================
# RECOMMENDATION KPI CALCULATIONS
# ============================================================

total_rec = len(filtered_rec)

# ------------------------------------------------------------
# APPROVED / REJECTED
# ------------------------------------------------------------
# These two KPIs MUST use the dedicated column:
# Recommendation (Approved/Rejected)
# ------------------------------------------------------------

approval_col = find_column(
    filtered_rec,
    [
        "Recommendation (Approved/Rejected)",
        "Recommendation (Approved / Rejected)",
        "Recommendation Approved/Rejected",
        "Recommendation Approval Rejection",
        "Recommendation Approved Rejected",
        "Recommendation Status Approved Rejected",
        "Approval Rejection",
        "Approved Rejected",
        "Approval Status"
    ]
)

approved_rec = 0
rejected_rec = 0

if approval_col:
    approval_values = (
        filtered_rec[approval_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    approved_rec = int(
        approval_values.str.fullmatch(
            r"approved|approve",
            case=False,
            na=False
        ).sum()
    )

    rejected_rec = int(
        approval_values.str.fullmatch(
            r"rejected|reject",
            case=False,
            na=False
        ).sum()
    )
else:
    st.warning(
        'The column "Recommendation (Approved/Rejected)" '
        'was not found in the PHA RECOMENDATION sheet.'
    )

# ------------------------------------------------------------
# COMPLETED / PENDING / OVERDUE
# ------------------------------------------------------------
# These three KPIs MUST use the dedicated column:
# Overdue/Pending/Completed.
# Rejected recommendations are excluded from all three.
# ------------------------------------------------------------

progress_col = find_column(
    filtered_rec,
    [
        "Overdue/Pending/Completed",
        "Overdue / Pending / Completed",
        "Overdue Pending Completed"
    ]
)

completed_rec = 0
pending_rec = 0
overdue_rec = 0

if progress_col:
    progress_values = (
        filtered_rec[progress_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # REJECTED recommendations are NOT part of the completion
    # workflow. Therefore they must not be counted as:
    # Completed, Pending, or Overdue.
    #
    # Example:
    # Total = 18
    # Rejected = 2
    # The remaining 16 recommendations are considered for
    # Completed / Pending / Overdue KPIs.
    # --------------------------------------------------------

    if approval_col:
        # Use the same dedicated Approved/Rejected column.
        approval_for_progress = (
            filtered_rec[approval_col]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        valid_progress_mask = ~approval_for_progress.str.fullmatch(
            r"rejected|reject",
            case=False,
            na=False
        )

    else:
        # If the approval column cannot be identified, do not
        # silently exclude records based on another unrelated
        # column.
        valid_progress_mask = pd.Series(
            True,
            index=filtered_rec.index
        )

    completed_rec = int(
        (
                progress_values.str.fullmatch(
                    r"completed|complete",
                    case=False,
                    na=False
                )
                & valid_progress_mask
        ).sum()
    )

    pending_rec = int(
        (
                progress_values.str.fullmatch(
                    r"pending",
                    case=False,
                    na=False
                )
                & valid_progress_mask
        ).sum()
    )

    overdue_rec = int(
        (
                progress_values.str.fullmatch(
                    r"overdue",
                    case=False,
                    na=False
                )
                & valid_progress_mask
        ).sum()
    )

else:
    st.warning(
        'The column "Overdue/Pending/Completed" '
        'was not found in the PHA RECOMENDATION sheet.'
    )

# ============================================================
# TOP AREA: ALL KPI CARDS FIRST
# ============================================================

# -------------------- PHA KPI SECTION -------------------------

with st.container(border=True):
    st.markdown(
        '<div class="section-title">PHA OVERVIEW</div>',
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3, gap="medium")

    with p1:
        render_kpi(
            "TOTAL PHA",
            total_pha,
            "Total PHA assessments",
            BLUE
        )

    with p2:
        render_kpi(
            "COMPLETED",
            completed_pha,
            "PHA assessments completed",
            GREEN
        )

    with p3:
        render_kpi(
            "ONGOING",
            ongoing_pha,
            "PHA assessments in progress",
            YELLOW
        )

        # Extra breathing room keeps the KPI cards completely inside
    # the rounded section border.
    st.markdown(
        '<div class="kpi-section-spacer"></div>',
        unsafe_allow_html=True
    )

# ---------------- Recommendation KPI section -----------------

with st.container(border=True):
    st.markdown(
        '<div class="section-title">PHA RECOMMENDATION OVERVIEW</div>',
        unsafe_allow_html=True
    )

    r1, r2, r3, r4, r5, r6 = st.columns(
        6,
        gap="small"
    )

    with r1:
        render_kpi(
            "TOTAL",
            total_rec,
            "Total recommendations",
            BLUE
        )

    with r2:
        render_kpi(
            "APPROVED",
            approved_rec,
            "Recommendations approved",
            GREEN
        )

    with r3:
        render_kpi(
            "REJECTED",
            rejected_rec,
            "Recommendations rejected",
            RED
        )

    with r4:
        render_kpi(
            "OVERDUE",
            overdue_rec,
            "Past target date",
            RED
        )

    with r5:
        render_kpi(
            "COMPLETED",
            completed_rec,
            "Recommendations completed",
            GREEN
        )

    with r6:
        render_kpi(
            "PENDING",
            pending_rec,
            "Awaiting completion",
            YELLOW
        )

        # Extra breathing room keeps all six KPI cards completely
    # inside the rounded section border.
    st.markdown(
        '<div class="kpi-section-spacer"></div>',
        unsafe_allow_html=True
    )

# ============================================================
# BELOW KPI CARDS: REGISTERS
# ============================================================

# ============================================================
# PHA DETAILS REGISTER
# ============================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-title">PHA DETAILS</div>',
        unsafe_allow_html=True
    )

    search_pha = st.text_input(
        "Search PHA",
        placeholder="Search PHA No, Name of PHA, Department, Product...",
        label_visibility="collapsed",
        key="pha_search"
    )

    display_pha = filter_dataframe(
        filtered_pha.copy(),
        search_pha
    )

    # Preferred order. Any additional source columns are
    # retained after these.
    # Exact display order requested:
    # S. No. -> PHA No. -> Department -> PHA Name ->
    # Status -> Document
    sr_col = find_column(
        display_pha,
        ["S. No.", "Sr No", "Sr. No", "Serial No", "S No"]
    )

    pha_no_col = find_column(
        display_pha,
        ["PHA No", "PHA Number", "PHA No."]
    )

    department_col = get_department_column(display_pha)

    pha_name_col = find_column(
        display_pha,
        ["PHA Name", "Name of PHA", "PHA"]
    )

    pha_status_col = find_column(
        display_pha,
        [
            "Status (Ongoing/Completed)",
            "Status",
            "PHA Status"
        ]
    )

    upload_doc_col = find_column(
        display_pha,
        [
            "Upload Document",
            "Document",
            "PHA Document"
        ]
    )

    pha_column_map = [
        (sr_col, "S. No."),
        (pha_no_col, "PHA No."),
        (department_col, "Department"),
        (pha_name_col, "PHA Name"),
        (pha_status_col, "Status"),
        (upload_doc_col, "Document")
    ]

    pha_display = pd.DataFrame(index=display_pha.index)

    for source_col, display_name in pha_column_map:
        if source_col is not None:
            pha_display[display_name] = display_pha[source_col]
        else:
            pha_display[display_name] = ""

            # Keep the original filtered row index so the recovered
    # Google Sheet document links stay aligned with each record.
    pha_link_map = load_document_links(PHA_SHEET)

    pha_links = []
    for original_index in pha_display.index:
        try:
            link_position = int(original_index)
            if 0 <= link_position < len(pha_link_map):
                pha_links.append(pha_link_map[link_position])
            else:
                pha_links.append(None)
        except Exception:
            pha_links.append(None)

    render_html_table(
        pha_display,
        "pha-details-table",
        document_links=pha_links,
        document_column="Document"
    )

# ============================================================
# PHA RECOMMENDATION REGISTER
# ============================================================

with st.container(border=True):
    st.markdown(
        '<div class="section-title">PHA RECOMMENDATION</div>',
        unsafe_allow_html=True
    )

    search_rec = st.text_input(
        "Search Recommendation",
        placeholder="Search recommendation, PHA No, Department...",
        label_visibility="collapsed",
        key="recommendation_search"
    )

    display_rec = filter_dataframe(
        filtered_rec.copy(),
        search_rec
    )


    # Target Date and Completion Date are intentionally NOT displayed.
    # Build the recommendation register in the exact requested order:
    # S. No. | Recommendation | Department | PHA No. | Date |
    # Approval | Progress | Status | Remarks

    def pick_rec_column(candidates):
        return find_column(display_rec, candidates)


    rec_sr = pick_rec_column(
        ["Sr No", "S. No.", "Sr. No", "Serial No", "S No"]
    )
    rec_recommendation = pick_rec_column(
        ["Recommendation", "Recommendation Details", "Recommendation Description"]
    )
    rec_department = get_department_column(display_rec)
    rec_pha_no = pick_rec_column(
        ["PHA No", "PHA Number", "PHA No."]
    )
    rec_date = pick_rec_column(
        ["Recommendation Date", "Date", "Recommendation Dt"]
    )
    rec_approval = pick_rec_column(
        [
            "Recommendation (Approved/Rejected)",
            "Recommendation (Approved / Rejected)",
            "Recommendation Approved/Rejected",
            "Recommendation Approval Rejection",
            "Recommendation Approved Rejected",
            "Approval Rejection",
            "Approved Rejected"
        ]
    )
    rec_progress = pick_rec_column(
        [
            "Overdue/Pending/Completed",
            "Overdue Pending Completed",
            "Progress Status"
        ]
    )
    rec_status = pick_rec_column(
        [
            "Status (Open/Close)",
            "Status (Open / Close)",
            "Open/Close Status",
            "Status"
        ]
    )
    rec_remarks = pick_rec_column(
        ["Remarks", "Remark", "Comments", "Comment"]
    )

    requested_rec_columns = [
        (rec_sr, "S. No."),
        (rec_recommendation, "Recommendation"),
        (rec_department, "Department"),
        (rec_pha_no, "PHA No."),
        (rec_date, "Date"),
        (rec_approval, "Approval"),
        (rec_progress, "Progress"),
        (rec_status, "Status"),
        (rec_remarks, "Remarks"),
    ]

    recommendation_display = pd.DataFrame(
        index=display_rec.index
    )

    for source_col, display_name in requested_rec_columns:
        if source_col is not None:
            recommendation_display[display_name] = display_rec[source_col]
        else:
            recommendation_display[display_name] = ""

    render_html_table(
        recommendation_display,
        "pha-recommendation-table"
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">PHA Management Dashboard</div>',
    unsafe_allow_html=True
)

