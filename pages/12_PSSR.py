import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import html
import re
from io import StringIO
from html.parser import HTMLParser
from urllib.parse import quote, urljoin

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PSSR Dashboard",
    page_icon="📋",
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

                PRE START-UP SAFETY REVIEW(PSSR)

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

SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
SHEET_NAME = "PSSR"

SHEET_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}"
)

# HTML export is used to recover the actual hyperlink behind
# the filename displayed in the "Attach PSSR Softcopy" column.
SHEET_HTML_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    f"/gviz/tq?tqx=out:html&sheet={quote(SHEET_NAME)}"
)

# Google Apps Script endpoint that returns the real hyperlink URL from
# the Attach PSSR Softcopy cells. Fill this after deploying the Apps Script
# shown below. Leave blank to use the existing HTML/CSV fallbacks.
LINKS_API_URL = ""

# ============================================================
# CSS
# ============================================================

st.markdown(""" 
<style> 

html, body, [class*="css"] { 
    font-family: "Segoe UI", Arial, sans-serif; 
} 

.stApp { 
    background: #FFFFFF; 
} 

header[data-testid="stHeader"], 
[data-testid="stDecoration"] { 
    display: none !important; 
} 

#MainMenu, 
footer { 
    visibility: hidden; 
} 

.main .block-container { 
    padding-top: 0px !important; 
    padding-bottom: 8px !important; 
    padding-left: 14px !important; 
    padding-right: 14px !important; 
    max-width: 1700px !important; 
} 

.stAppViewContainer { 
    padding-top: 0px !important; 
} 

/* ================= FILTER ================= */ 

.filter-label { 
    color: #174A86; 
    font-size: 14px; 
    font-weight: 750; 
    text-transform: uppercase; 
    letter-spacing: .3px; 
    margin-bottom: -2px !important; 
    line-height: 1.1; 
} 

div[data-baseweb="select"] { 
    margin-top: -3px !important; 
} 

div[data-baseweb="select"] > div { 
    background-color: #F7F9FC !important; 
    border: 1px solid #D6E0EA !important; 
    border-radius: 10px !important; 
    min-height: 42px !important; 
    box-shadow: none !important; 
} 

div[data-baseweb="select"] span { 
    color: #354052 !important; 
    font-size: 15px !important; 
} 

/* ================= KPI ================= */ 

.kpi-card { 
    position: relative; 
    width: 100%; 
    height: 105px; 
    box-sizing: border-box; 

    background: #FFFFFF; 

    border: 1px solid #D5DFEA; 
    border-radius: 12px; 

    padding: 11px 18px 8px 28px; 

    text-align: left; 
    overflow: hidden; 

    box-shadow: 0 2px 7px rgba(23,74,134,.035); 
} 

/* Strong left accent */ 

.kpi-card::before { 
    content: ""; 
    position: absolute; 
    left: 0; 
    top: 0; 
    width: 8px; 
    height: 100%; 
} 

.kpi-total::before { 
    background: #19579A; 
} 

.kpi-completed::before { 
    background: #159447; 
} 

.kpi-pending::before { 
    background: #E4B400; 
} 

.kpi-overdue::before { 
    background: #E31E2F; 
} 

.kpi-compliance::before { 
    background: #7047A8; 
} 

/* KPI title */ 

.kpi-title { 
    font-size: 15px; 
    font-weight: 700; 
    text-transform: uppercase; 
    letter-spacing: .1px; 
    line-height: 1.15; 
    margin-bottom: 6px; 
    white-space: nowrap; 
} 

/* KPI value */ 

.kpi-number { 
    font-size: 34px; 
    font-weight: 800; 
    line-height: 1; 
    margin: 0; 
} 

/* KPI subtitle */ 

.kpi-subtitle { 
    font-size: 12px; 
    font-weight: 500; 
    margin-top: 6px; 
    line-height: 1.2; 
    white-space: nowrap; 
} 

/* Text colour = accent */ 

.total-text { 
    color: #19579A; 
} 

.completed-text { 
    color: #159447; 
} 

.pending-text { 
    color: #D3A500; 
} 

.overdue-text { 
    color: #E31E2F; 
} 

.compliance-text { 
    color: #7047A8; 
} 

/* ================= SECTION ================= */ 

.section-title { 
    color: #174A86; 
    font-size: 17px; 
    font-weight: 750; 
    text-transform: uppercase; 
    letter-spacing: .2px; 
    margin-bottom: 0px; 
    padding: 0 2px; 
} 

/* ================= TABLE ================= */ 

.table-container { 
    width: 100%; 
    margin-top: 8px; 
} 

.table-scroll { 
    width: 100%; 
    max-height: 330px; 
    overflow-y: auto; 
    overflow-x: hidden; 
    border-radius: 0 0 10px 10px; 
    scrollbar-width: thin; 
    scrollbar-color: #AEBBC9 #F1F4F7; 
} 

.table-scroll::-webkit-scrollbar { 
    width: 8px; 
} 

.table-scroll::-webkit-scrollbar-track { 
    background: #F1F4F7; 
    border-radius: 8px; 
} 

.table-scroll::-webkit-scrollbar-thumb { 
    background: #AEBBC9; 
    border-radius: 8px; 
} 

.pssr-table { 
    width: 100%; 
    border-collapse: separate; 
    border-spacing: 0; 
    table-layout: fixed; 
    background: #FFFFFF; 
} 

.pssr-table th { 
    position: sticky; 
    top: 0; 
    z-index: 5; 

    background: #193F6B; 
    color: #FFFFFF; 

    padding: 10px 12px; 
    height: 42px; 
    box-sizing: border-box; 

    font-size: 14px; 
    font-weight: 700; 
    text-align: left; 
    vertical-align: middle; 

    border-right: 1px solid rgba(255,255,255,.28); 
    border-bottom: 1px solid #193F6B; 
} 

.pssr-table th:first-child { 
    border-top-left-radius: 3px; 
} 

.pssr-table th:last-child { 
    border-top-right-radius: 3px; 
    border-right: none; 
} 

.pssr-table td { 
    padding: 9px 12px; 

    font-size: 13px; 
    line-height: 1.3; 
    color: #30465E; 

    border-bottom: 1px solid #DFE6EE; 
    border-right: 1px solid #E3E8EE; 

    vertical-align: middle; 
    word-wrap: break-word; 
    overflow-wrap: anywhere; 

    background: #FFFFFF; 
} 

.pssr-table tbody tr:nth-child(even) td { 
    background: #F4F7FA; 
} 

.pssr-table tbody tr:hover td { 
    background: #EDF4FB; 
} 

.pssr-table td:last-child { 
    border-right: none; 
} 

.pssr-table tbody tr:last-child td { 
    border-bottom: none; 
} 

.col-pssr { 
    width: 23%; 
} 

.col-description { 
    width: 28%; 
} 

.col-department { 
    width: 19%; 
} 

.col-status { 
    width: 15%; 
} 

.col-report { 
    width: 15%; 
} 

/* ================= STATUS BADGES ================= */ 

.status-badge { 
    display: inline-block; 

    min-width: 88px; 

    padding: 6px 12px; 

    border-radius: 5px; 

    text-align: center; 

    font-size: 12px; 
    font-weight: 750; 
    line-height: 1.1; 

    box-sizing: border-box; 
} 

.status-completed { 
    background: #159447; 
    color: #FFFFFF !important; 
} 

.status-pending { 
    background: #E4B400; 
    color: #FFFFFF !important; 
} 

.status-overdue { 
    background: #E31E2F; 
    color: #FFFFFF !important; 
} 

/* ================= VIEW REPORT BUTTON ================= */ 

.report-button { 
    display: inline-block; 

    min-width: 70px; 

    padding: 7px 16px; 

    background: #095BBB; 
    color: #FFFFFF !important; 

    border-radius: 8px; 

    font-size: 13px; 
    font-weight: 700; 

    text-align: center; 
    text-decoration: none !important; 

    transition: background .15s ease; 
} 

.report-button:hover { 
    background: #174A86; 
    color: #FFFFFF !important; 
    text-decoration: none !important; 
} 

.no-report { 
    color: #8C99A8; 
    font-size: 13px; 
} 

.empty-state { 
    padding: 35px 20px; 
    text-align: center; 
    color: #8995A5; 
    font-size: 14px; 
} 

.dashboard-footer { 
    text-align: right; 
    color: #A0A9B5; 
    font-size: 10px; 
    padding-top: 4px; 
} 

</style> 
""", unsafe_allow_html=True)


# ============================================================
# RECOVER GOOGLE SHEET HYPERLINKS
# ============================================================

class SheetLinkParser(HTMLParser):
    """Collect visible text and href values from <a> tags."""

    def __init__(self):
        super().__init__()
        self.links = {}
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            attrs_dict = dict(attrs)
            self._href = attrs_dict.get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href:
            text = " ".join("".join(self._text).split()).strip()
            if text:
                self.links[text] = self._href
            self._href = None
            self._text = []


def normalize_link_text(value):
    return " ".join(str(value).strip().lower().split())


@st.cache_data(ttl=60, show_spinner=False)
def load_report_links():
    """
    Recover the real Google Drive/Docs URL behind filenames in the
    ``Attach PSSR Softcopy`` column.  Google Sheets CSV export often
    returns only the visible filename, so this function checks the
    rendered HTML first and then the public sheet page as a fallback.
    """
    links = {}

    def add_link(text, url):
        if not text or not url:
            return
        text = normalize_link_text(text)
        url = html.unescape(str(url)).strip()
        url = url.replace('\\/', '/')
        url = url.replace('\\u003d', '=').replace('\\u0026', '&')
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = urljoin(SHEET_HTML_URL, url)
        if url.startswith(('http://', 'https://')):
            links[text] = url

            # 0) Preferred method: Google Apps Script reads the actual RichText

    # hyperlink attached to column I. This works for links created with
    # Ctrl+K / Insert link as well as HYPERLINK() formulas.
    if LINKS_API_URL.strip():
        try:
            api_response = requests.get(
                LINKS_API_URL.strip(),
                timeout=20
            )
            api_response.raise_for_status()
            payload = api_response.json()
            rows = payload.get("links", []) if isinstance(payload, dict) else payload
            if isinstance(rows, list):
                for item in rows:
                    if not isinstance(item, dict):
                        continue
                    add_link(item.get("text", ""), item.get("url", ""))
        except Exception:
            pass

            # 1) Google Visualization HTML export.
    try:
        response = requests.get(SHEET_HTML_URL, timeout=20)
        response.raise_for_status()

        parser = SheetLinkParser()
        parser.feed(response.text)

        for text, url in parser.links.items():
            add_link(text, url)

            # Some rich-text links are not emitted as <a> tags.  Look for a
        # URL close to each filename from the CSV export in the returned HTML.
        raw = html.unescape(response.text)
        url_pattern = re.compile(r'https?://[^\s"<>\']+')
        for filename in load_sheet_data()[REPORT_COL].dropna().astype(str):
            filename = filename.strip()
            if not filename or filename.lower() == 'nan':
                continue
            if normalize_link_text(filename) in links:
                continue
            pos = raw.lower().find(filename.lower())
            if pos >= 0:
                nearby = raw[max(0, pos - 2500):pos + 2500]
                matches = url_pattern.findall(nearby)
                for candidate in matches:
                    if ('drive.google.com' in candidate or
                            'docs.google.com' in candidate or
                            'googleusercontent.com' in candidate):
                        add_link(filename, candidate)
                        break

    except Exception:
        pass

        # 2) Public Google Sheet page fallback.  This catches links that are
    # stored as rich-text links rather than HYPERLINK() formulas.
    try:
        edit_url = (
            f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
        )
        response = requests.get(edit_url, timeout=20)
        response.raise_for_status()
        raw = html.unescape(response.text)
        raw = raw.replace('\\u003d', '=').replace('\\u0026', '&')
        raw = raw.replace('\\/', '/')

        # Use filenames from the CSV as anchors and search around each one.
        for value in load_sheet_data()[REPORT_COL].dropna().astype(str):
            filename = value.strip()
            if not filename or filename.lower() == 'nan':
                continue
            key = normalize_link_text(filename)
            if key in links:
                continue

            pos = raw.lower().find(filename.lower())
            if pos < 0:
                continue

            nearby = raw[max(0, pos - 5000):pos + 5000]
            matches = re.findall(r'https?://[^\s"<>\']+', nearby)
            for candidate in matches:
                candidate = candidate.rstrip('\\),;')
                if ('drive.google.com' in candidate or
                        'docs.google.com' in candidate or
                        'googleusercontent.com' in candidate):
                    add_link(filename, candidate)
                    break

    except Exception:
        pass

    return links


# ============================================================
# LOAD DATA - TTL 60 SECONDS
# ============================================================

@st.cache_data(ttl=60, show_spinner=False)
def load_sheet_data():
    try:
        response = requests.get(
            SHEET_CSV_URL,
            timeout=20
        )
        response.raise_for_status()

        data = pd.read_csv(
            StringIO(response.text)
        )

        data.columns = [
            str(c).strip()
            for c in data.columns
        ]

        return data.dropna(how="all")

    except Exception as error:
        st.error(
            f"Unable to load Google Sheet data: {error}"
        )
        return pd.DataFrame()


df = load_sheet_data()
report_links = load_report_links()

if df.empty:
    st.html(""" 
        <div class="empty-state"> 
            No PSSR data available from the Google Sheet. 
        </div> 
    """)
    st.stop()

# ============================================================
# COLUMN DEFINITIONS
# ============================================================

PSSR_COL = "PSSR No."
DEPARTMENT_COL = "Department"
DESCRIPTION_COL = "PSSR Description"
DUE_DATE_COL = "Due Date"
STATUS_COL = "Overdue/Pending/Completed"
REPORT_COL = "Attach PSSR Softcopy"

required_columns = [
    PSSR_COL,
    DEPARTMENT_COL,
    DESCRIPTION_COL,
    DUE_DATE_COL,
    STATUS_COL,
    REPORT_COL
]

missing_columns = [
    c for c in required_columns
    if c not in df.columns
]

if missing_columns:
    st.error(
        "Required columns are missing from the PSSR sheet."
    )
    st.write("Missing columns:", missing_columns)
    st.write("Available columns:", list(df.columns))
    st.stop()

# ============================================================
# CLEAN DATA
# ============================================================

for col in [
    PSSR_COL,
    DEPARTMENT_COL,
    DESCRIPTION_COL,
    STATUS_COL,
    REPORT_COL
]:
    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# FINANCIAL YEAR FROM DUE DATE
# April 2026 - March 2027 = FY 2026-27
# ============================================================

def calculate_financial_year(value):
    if value is None:
        return ""

    value = str(value).strip()

    if not value or value.lower() == "nan":
        return ""

    try:
        date_value = pd.to_datetime(
            value,
            dayfirst=True,
            errors="coerce"
        )

        if pd.isna(date_value):
            return ""

        start_year = (
            date_value.year
            if date_value.month >= 4
            else date_value.year - 1
        )

        return (
            f"{start_year}-"
            f"{str(start_year + 1)[-2:]}"
        )

    except Exception:
        return ""


df["Financial Year"] = (
    df[DUE_DATE_COL]
    .apply(calculate_financial_year)
)

financial_years = sorted(
    [
        y for y in df["Financial Year"].unique()
        if str(y).strip()
    ],
    reverse=True
)

departments = sorted(
    [
        d for d in df[DEPARTMENT_COL].unique()
        if str(d).strip()
    ]
)

# ============================================================
# FILTERS
# ============================================================

with st.container(border=True):
    filter_col1, filter_col2 = st.columns(
        2,
        gap="medium"
    )

    with filter_col1:
        st.html(""" 
            <div class="filter-label"> 
                Financial Year 
            </div> 
        """)

        selected_fy = st.selectbox(
            "Financial Year",
            ["All Financial Years"] + financial_years,
            label_visibility="collapsed"
        )

    with filter_col2:
        st.html(""" 
            <div class="filter-label"> 
                Department 
            </div> 
        """)

        selected_department = st.selectbox(
            "Department",
            ["All Departments"] + departments,
            label_visibility="collapsed"
        )

    # ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_fy != "All Financial Years":
    filtered_df = filtered_df[
        filtered_df["Financial Year"] == selected_fy
        ]

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df[DEPARTMENT_COL] == selected_department
        ]

# ============================================================
# STATUS COUNTS
# STATUS COMES ONLY FROM COLUMN H
# ============================================================

status_series = (
    filtered_df[STATUS_COL]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

completed_count = int(
    status_series.eq("completed").sum()
)

pending_count = int(
    status_series.eq("pending").sum()
)

overdue_count = int(
    status_series.eq("overdue").sum()
)

total_count = int(
    len(filtered_df)
)

compliance = (
    completed_count / total_count * 100
    if total_count > 0
    else 0
)

# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(
    5,
    gap="small"
)

with kpi1:
    st.html(f""" 
        <div class="kpi-card kpi-total"> 
            <div class="kpi-title total-text"> 
                Total PSSR 
            </div> 
            <div class="kpi-number total-text"> 
                {total_count} 
            </div> 
            <div class="kpi-subtitle total-text"> 
                Total assessments planned 
            </div> 
        </div> 
    """)

with kpi2:
    st.html(f""" 
        <div class="kpi-card kpi-completed"> 
            <div class="kpi-title completed-text"> 
                Completed PSSR 
            </div> 
            <div class="kpi-number completed-text"> 
                {completed_count} 
            </div> 
            <div class="kpi-subtitle completed-text"> 
                Assessments completed 
            </div> 
        </div> 
    """)

with kpi3:
    st.html(f""" 
        <div class="kpi-card kpi-pending"> 
            <div class="kpi-title pending-text"> 
                Pending PSSR 
            </div> 
            <div class="kpi-number pending-text"> 
                {pending_count} 
            </div> 
            <div class="kpi-subtitle pending-text"> 
                Awaiting completion 
            </div> 
        </div> 
    """)

with kpi4:
    st.html(f""" 
        <div class="kpi-card kpi-overdue"> 
            <div class="kpi-title overdue-text"> 
                Overdue PSSR 
            </div> 
            <div class="kpi-number overdue-text"> 
                {overdue_count} 
            </div> 
            <div class="kpi-subtitle overdue-text"> 
                Past due date 
            </div> 
        </div> 
    """)

with kpi5:
    st.html(f""" 
        <div class="kpi-card kpi-compliance"> 
            <div class="kpi-title compliance-text"> 
                PSSR Compliance 
            </div> 
            <div class="kpi-number compliance-text"> 
                {compliance:.1f}% 
            </div> 
            <div class="kpi-subtitle compliance-text"> 
                Completed / Total 
            </div> 
        </div> 
    """)

# ============================================================
# DEPARTMENT DATA
# ============================================================

department_data = (
    filtered_df
    .groupby(DEPARTMENT_COL)
    .size()
    .reset_index(name="PSSR Count")
    .sort_values(
        "PSSR Count",
        ascending=False
    )
)

# ============================================================
# CHARTS
# ============================================================

chart_left, chart_right = st.columns(
    [1.05, 1],
    gap="small"
)

# ============================================================
# DEPARTMENT CHART
# ============================================================

with chart_left:
    with st.container(border=True):

        st.html(""" 
            <div class="section-title"> 
                No. of PSSR Performed by Department 
            </div> 
        """)

        if not department_data.empty:

            fig_department = go.Figure()

            fig_department.add_trace(
                go.Bar(
                    x=department_data[DEPARTMENT_COL],
                    y=department_data["PSSR Count"],
                    text=department_data["PSSR Count"],
                    textposition="outside",
                    marker=dict(
                        color="#19579A"
                    ),
                    hovertemplate=
                    "<b>%{x}</b><br>"
                    "PSSR: %{y}"
                    "<extra></extra>"
                )
            )

            fig_department.update_layout(
                height=245,
                margin=dict(
                    l=12,
                    r=12,
                    t=10,
                    b=32
                ),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                showlegend=False,
                font=dict(
                    family="Segoe UI",
                    color="#65758B"
                ),
                xaxis=dict(
                    title=None,
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(size=11)
                ),
                yaxis=dict(
                    title=None,
                    showgrid=True,
                    gridcolor="#E3EAF2",
                    zeroline=False,
                    dtick=1,
                    tickfont=dict(size=10)
                )
            )

            st.plotly_chart(
                fig_department,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        else:
            st.html(""" 
                <div class="empty-state"> 
                    No department data available. 
                </div> 
            """)

        # ============================================================
# STATUS DONUT
# ============================================================

with chart_right:
    with st.container(border=True):
        st.html(""" 
            <div class="section-title"> 
                PSSR Status Summary 
            </div> 
        """)

        # Include the live count in each legend item.
        status_labels = [
            f"Completed  {completed_count}",
            f"Pending  {pending_count}",
            f"Overdue  {overdue_count}"
        ]

        status_values = [
            completed_count,
            pending_count,
            overdue_count
        ]

        fig_status = go.Figure()

        fig_status.add_trace(
            go.Pie(
                labels=status_labels,
                values=status_values,
                hole=0.68,
                sort=False,

                # Numeric data labels are displayed outside
                # their respective donut sectors.
                textinfo="value",
                textposition="outside",
                texttemplate="%{value}",
                outsidetextfont=dict(
                    size=12,
                    color="#30465E"
                ),

                automargin=True,

                marker=dict(
                    colors=[
                        "#19579A",
                        "#E4B400",
                        "#E31E2F"
                    ],
                    line=dict(
                        color="#FFFFFF",
                        width=2
                    )
                ),

                hovertemplate=
                "<b>%{label}</b><br>"
                "PSSR: %{value}"
                "<extra></extra>"
            )
        )

        fig_status.update_layout(
            height=245,

            margin=dict(
                l=10,
                r=10,
                t=2,
                b=38
            ),

            paper_bgcolor="#FFFFFF",

            font=dict(
                family="Segoe UI",
                color="#30465E"
            ),

            # Keep legend at bottom centre and include counts.
            legend=dict(
                orientation="h",
                x=0.50,
                y=-0.02,
                xanchor="center",
                yanchor="top",
                font=dict(size=11),
                traceorder="normal"
            ),

            annotations=[
                dict(
                    text=f"<b>{total_count}</b>",
                    x=0.50,
                    y=0.55,
                    showarrow=False,
                    font=dict(
                        size=34,
                        color="#17324D"
                    )
                ),
                dict(
                    text="TOTAL",
                    x=0.50,
                    y=0.40,
                    showarrow=False,
                    font=dict(
                        size=12,
                        color="#65758B"
                    )
                )
            ]
        )

        # Add counts to legend labels using Plotly's trace text.
        fig_status.update_traces(
            name="",
            legendgrouptitle_text=None
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # PSSR DETAILS
# ============================================================

with st.container(border=True):
    st.html(""" 
        <div class="section-title"> 
            PSSR Details 
        </div> 
    """)

    if filtered_df.empty:

        st.html(""" 
            <div class="empty-state"> 
                No PSSR records found for the selected filters. 
            </div> 
        """)

    else:

        table_html = """ 
        <div class="table-container"> 
        <div class="table-scroll"> 

        <table class="pssr-table"> 

        <thead> 
            <tr> 
                <th class="col-pssr">PSSR No.</th> 
                <th class="col-description">Description</th> 
                <th class="col-department">Department</th> 
                <th class="col-status">Status</th> 
                <th class="col-report">View Report</th> 
            </tr> 
        </thead> 

        <tbody> 
        """

        for _, row in filtered_df.iterrows():

            pssr_number = html.escape(
                str(row[PSSR_COL])
            )

            description = html.escape(
                str(row[DESCRIPTION_COL])
            )

            department = html.escape(
                str(row[DEPARTMENT_COL])
            )

            status = str(
                row[STATUS_COL]
            ).strip()

            status_lower = status.lower()

            # ------------------------------------------------
            # STATUS BADGE
            # ------------------------------------------------

            if status_lower == "completed":

                status_class = "status-completed"

            elif status_lower == "pending":

                status_class = "status-pending"

            elif status_lower == "overdue":

                status_class = "status-overdue"

            else:

                status_class = ""

            status_display = html.escape(
                status.upper()
            )

            if status_class:

                status_html = (
                    f'<span class="status-badge '
                    f'{status_class}">'
                    f'{status_display}'
                    f'</span>'
                )

            else:

                status_html = (
                    f'<span>'
                    f'{status_display}'
                    f'</span>'
                )

                # ------------------------------------------------
            # REPORT URL
            # ------------------------------------------------

            report_value = str(
                row[REPORT_COL]
            ).strip()

            report_url = ""

            # Case 1: CSV contains the actual URL.
            if (
                    report_value.startswith("https://")
                    or report_value.startswith("http://")
            ):
                report_url = report_value

                # Case 2: CSV contains a HYPERLINK formula.
            if not report_url:
                formula_match = re.search(
                    r'HYPERLINK\s*\(\s*"([^"]+)"',
                    report_value,
                    flags=re.IGNORECASE
                )

                if formula_match:
                    report_url = formula_match.group(1)

                    # Case 3: CSV contains only the filename/display text.
            if not report_url and report_value:
                report_url = report_links.get(
                    normalize_link_text(report_value),
                    ""
                )

                # ------------------------------------------------
            # VIEW BUTTON
            # ------------------------------------------------

            if report_url:

                report_html = (
                    f'<a class="report-button" '
                    f'href="{html.escape(report_url)}" '
                    f'target="_blank" '
                    f'rel="noopener noreferrer">'
                    f'View'
                    f'</a>'
                )

            else:

                report_html = (
                    '<span class="no-report">—</span>'
                )

            table_html += f""" 
            <tr> 

                <td> 
                    <b>{pssr_number}</b> 
                </td> 

                <td> 
                    {description} 
                </td> 

                <td> 
                    {department} 
                </td> 

                <td> 
                    {status_html} 
                </td> 

                <td> 
                    {report_html} 
                </td> 

            </tr> 
            """

        table_html += """ 
        </tbody> 

        </table> 

        </div> 
        </div> 
        """

        st.html(table_html)

    # FOOTER
# ============================================================

st.html(""" 
    <div class="dashboard-footer"> 
        PSSR Management Dashboard 
    </div> 
""")

