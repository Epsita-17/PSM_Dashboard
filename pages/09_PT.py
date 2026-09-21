import streamlit as st
import pandas as pd
import requests
from io import StringIO
import html
import re
from pathlib import Path
from datetime import datetime
import streamlit.components.v1 as components
import base64
from zoneinfo import ZoneInfo
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PSM Digital Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HIDE STREAMLIT DEFAULT UI
# =========================================================

st.markdown("""
<style>

/* Hide Streamlit default menu */
#MainMenu {
    visibility: hidden !important;
    display: none !important;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden !important;
    display: none !important;
}

/* SHOW Streamlit default header */
header {
    visibility: visible !important;
    display: block !important;
}

/* SHOW Streamlit toolbar */
[data-testid="stToolbar"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
}

/* SHOW Deploy button */
[data-testid="stAppDeployButton"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
}

/* Hide Streamlit decoration */
[data-testid="stDecoration"] {
    visibility: hidden !important;
    display: none !important;
}

/* Hide status widget */
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


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
# GOOGLE SHEET
# ============================================================

GOOGLE_SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
SHEET_NAME = "PT"

GOOGLE_SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{GOOGLE_SHEET_ID}/gviz/tq?"
    f"tqx=out:csv&sheet={SHEET_NAME}"
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
        margin-bottom: -70px !important;
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
    width: calc(100% + 10px);
    margin-left: -5px;
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

    top: 6px;

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

                PROCESS TECHNOLOGY (PT)

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

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   PAGE
   ============================================================ */

.stApp {
    background: #ffffff !important;
}

.main .block-container {
    max-width: 100% !important;
    padding: 0 28px 20px 28px !important;
}

footer {
    visibility: hidden !important;
}

* {
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
}

/* ============================================================
   DEPARTMENT FILTER
   SMALL + LEFT ALIGNED
   ============================================================ */

.department-area {
    width: 18%;
    margin-bottom: 18px;
}

.department-area div[data-baseweb="select"] > div {
    min-height: 40px !important;
    height: 40px !important;
    background: #f6f8fb !important;
    border: 1px solid #cbd8e6 !important;
    border-radius: 5px !important;
    box-shadow: none !important;
}

.department-area div[data-baseweb="select"] span {
    color: #173f70 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ============================================================
   SECTION CONTAINERS
   PROCESS TECHNOLOGY + KPI CARDS
   PT REGISTER + SEARCH + TABLE

   These are Streamlit native bordered containers. Keeping the
   border on the actual Streamlit container makes the border
   wrap all widgets/elements inside it correctly.
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #cbd9e7 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(18, 63, 115, 0.04) !important;
    margin-bottom: 18px !important;
    padding: 0 !important;
    overflow: visible !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: 8px !important;
    padding: 20px !important;
    overflow: visible !important;
}

/* Bottom space is created by a real child inside the Streamlit
   bordered container. This reliably makes the outer border extend
   below the KPI cards. */
.kpi-section-spacer {
    height: 32px !important;
    width: 100%;
    display: block;
}

/* Do not use artificial min-height here; Streamlit sizes the border
   from its actual children, including the spacer above. */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.kpi-card) > div {
    padding-bottom: 0 !important;
}

/* ============================================================
   PROCESS TECHNOLOGY TITLE
   NO SEPARATE BORDER
   ============================================================ */

.section-title {
    color: #17477d;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 0.2px;
    margin: 0 0 18px 0;
    padding: 0;
}

/* ============================================================
   KPI CARDS
   NO BORDER / NO SEPARATE CONTAINER
   ONLY LEFT ACCENT
   ============================================================ */

.kpi-card {
    position: relative;
    min-height: 128px;
    height: 128px;
    background: #ffffff;
    border: 1px solid #d3deea !important;
    border-radius: 6px !important;
    padding: 13px 12px 10px 18px;
    box-sizing: border-box;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(18, 63, 115, 0.045) !important;
}

.kpi-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    background: var(--accent);
}

.kpi-label {
    color: var(--accent);
    font-size: 14px;
    line-height: 1.25;
    font-weight: 800;
    letter-spacing: 0.2px;
    margin-bottom: 8px;
}

.kpi-value {
    color: var(--accent);
    font-size: 40px;
    line-height: 1;
    font-weight: 800;
    margin-bottom: 8px;
}

.kpi-subtitle {
    color: var(--accent);
    font-size: 11px;
    line-height: 1.2;
    font-weight: 600;
    opacity: 0.82;
}

/* ============================================================
   PT REGISTER
   TITLE + SEARCH + TABLE ARE INSIDE ONE BORDERED CONTAINER
   ============================================================ */

.register-title {
    color: #17477d;
    font-size: 18px;
    font-weight: 750;
    letter-spacing: 0.2px;
    margin: 0 0 13px 0;
}

/* ============================================================
   SEARCH
   ============================================================ */

div[data-testid="stTextInput"] {
    margin-bottom: 9px !important;
}

div[data-testid="stTextInput"] input {
    min-height: 40px !important;
    background: #ffffff !important;
    border: 1px solid #cbd8e6 !important;
    border-radius: 5px !important;
    color: #173f70 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #1c6fba !important;
    box-shadow: 0 0 0 1px #1c6fba !important;
}

/* ============================================================
   TABLE SCROLL
   APPROX. 10 RECORDS AT A TIME
   ============================================================ */

.table-scroll {
    height: 552px;
    overflow-y: auto;
    overflow-x: auto;
    border: 1px solid #ccd8e5;
    border-radius: 5px;
    background: #ffffff;
}

.table-scroll::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

.table-scroll::-webkit-scrollbar-track {
    background: #f1f5f9;
}

.table-scroll::-webkit-scrollbar-thumb {
    background: #aebfd0;
    border-radius: 4px;
}

/* ============================================================
   TABLE
   ============================================================ */

.pt-table {
    width: 100%;
    min-width: 900px;
    border-collapse: separate;
    border-spacing: 0;
    table-layout: fixed;
    background: #ffffff;
}

.pt-table th {
    position: sticky;
    top: 0;
    z-index: 5;
    background: #17477d;
    color: #ffffff;
    font-size: 12px;
    font-weight: 750;
    padding: 12px 10px;
    text-align: left;
    border-right: 1px solid rgba(255,255,255,0.25);
    border-bottom: 1px solid #17477d;
    white-space: nowrap;
}

.pt-table td {
    color: #173f70;
    font-size: 12px;
    font-weight: 600;
    padding: 11px 10px;
    border-right: 1px solid #d9e2ec;
    border-bottom: 1px solid #d9e2ec;
    vertical-align: middle;
    word-wrap: break-word;
    background: #ffffff;
}

.pt-table tbody tr:nth-child(even) td {
    background: #f8fbfe;
}

.pt-table tbody tr:hover td {
    background: #eef5fb;
}

/* ============================================================
   TABLE WIDTHS
   ============================================================ */

.sr-col {
    width: 6%;
    text-align: center !important;
}

.pt-col {
    width: 19%;
}

.dept-col {
    width: 14%;
}

.name-col {
    width: 28%;
}

.status-col {
    width: 15%;
    text-align: center !important;
}

.document-col {
    width: 18%;
    text-align: center !important;
}

/* ============================================================
   STATUS
   ============================================================ */

.status-badge {
    display: inline-block;
    min-width: 82px;
    padding: 4px 9px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 800;
    text-align: center;
    letter-spacing: 0.2px;
    border: 1px solid transparent;
}

.status-completed {
    color: #13834a;
    background: #eef9f2;
    border-color: #8ed0aa;
}

.status-pending {
    color: #9a6500;
    background: #fff9e8;
    border-color: #e3bc55;
}

.status-ongoing {
    color: #b77a00;
    background: #fff9e8;
    border-color: #e3bc55;
}

.status-approved {
    color: #1768a9;
    background: #edf5fc;
    border-color: #9bc2e2;
}

.status-default {
    color: #5d6874;
    background: #f3f5f7;
    border-color: #cbd3db;
}

/* ============================================================
   DOCUMENT LINK
   ============================================================ */

.document-link {
    color: #155b9e !important;
    text-decoration: none !important;
    font-weight: 700;
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
}

.document-link:hover {
    color: #c7353d !important;
    text-decoration: underline !important;
}

/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-state {
    padding: 28px 18px;
    text-align: center;
    color: #718096;
    font-size: 13px;
    border: 1px dashed #cbd7e4;
    border-radius: 5px;
    background: #fafcff;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .main .block-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .department-area {
        width: 100%;
    }

    .kpi-card {
        height: 118px;
    }

    .kpi-value {
        font-size: 34px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=10)
def load_data():

    try:
        response = requests.get(
            GOOGLE_SHEET_URL,
            timeout=20
        )

        response.raise_for_status()

        df = pd.read_csv(
            StringIO(response.text)
        )

        if df.empty:
            return pd.DataFrame(), None

        df = df.dropna(
            axis=1,
            how="all"
        )

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = (
                    df[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        return df, None

    except Exception as e:
        return pd.DataFrame(), str(e)


# ============================================================
# HELPERS
# ============================================================

def normalize_column_name(name):
    return re.sub(
        r"[^a-z0-9]",
        "",
        str(name).lower()
    )


def find_column(df, possible_names):

    normalized_columns = {
        normalize_column_name(col): col
        for col in df.columns
    }

    for name in possible_names:

        key = normalize_column_name(name)

        if key in normalized_columns:
            return normalized_columns[key]

    for name in possible_names:

        key = normalize_column_name(name)

        for normalized, original in normalized_columns.items():

            if (
                key in normalized
                or normalized in key
            ):
                return original

    return None


def clean_value(value):

    if pd.isna(value):
        return ""

    value = str(value).strip()

    if value.lower() in ["nan", "none"]:
        return ""

    return value


def get_status_class(status):

    status = clean_value(status).upper()

    if "COMPLETED" in status:
        return "status-completed"

    if "PENDING" in status:
        return "status-pending"

    if "ONGOING" in status:
        return "status-ongoing"

    if "APPROVED" in status:
        return "status-approved"

    return "status-default"


def percentage(value, total):

    if total == 0:
        return 0

    return round(
        (value / total) * 100
    )


# ============================================================
# GET DATA
# ============================================================

df, error = load_data()

if error:

    st.markdown(
        f"""
<div class="empty-state">
<b>Unable to load the PT worksheet.</b>
<br><br>
Please ensure the Google Sheet is accessible and the worksheet is named <b>PT</b>.
<br><br>
{html.escape(error)}
</div>
""",
        unsafe_allow_html=True
    )

    st.stop()


if df.empty:

    st.markdown(
        """
<div class="empty-state">
No data was found in the PT worksheet.
</div>
""",
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# FIND COLUMNS
# ============================================================

pt_no_col = find_column(
    df,
    [
        "PT No.",
        "PT No",
        "PT Number",
        "PT Number.",
        "Permit No",
        "Permit Number"
    ]
)

department_col = find_column(
    df,
    [
        "Department",
        "Dept",
        "Department Name"
    ]
)

name_col = find_column(
    df,
    [
        "Name of PT",
        "PT Name",
        "Name",
        "Process Technology",
        "Description"
    ]
)

status_col = find_column(
    df,
    [
        "Status",
        "PT Status",
        "Current Status"
    ]
)

approved_col = find_column(
    df,
    [
        "Approved (Yes/No)",
        "Approved(Yes/No)",
        "Approved",
        "Approval",
        "Approved Yes No",
        "Approved (Yes / No)",
        "Approval Status"
    ]
)

# IMPORTANT: The dashboard's "View Document" column must use the
# URL stored in "Attach PT Softcopy Link". Do not use a column
# named "View Document" because that may contain only a date/display value.
document_col = find_column(
    df,
    [
        "Attach PT Softcopy Link",
        "Attach PT Softcopy Links",
        "PT Softcopy Link",
        "PT Softcopy Links",
        "Attach PT Soft Copy Link",
        "Attach PT Soft Copy Links",
        "Softcopy Link",
        "Soft Copy Link",
        "Document Link",
        "Document URL",
        "File Link",
        "Link",
        "URL"
    ]
)

# Fallbacks
if pt_no_col is None:
    pt_no_col = df.columns[0]

if department_col is None and len(df.columns) > 1:
    department_col = df.columns[1]

if name_col is None and len(df.columns) > 2:
    name_col = df.columns[2]

if status_col is None and len(df.columns) > 3:
    status_col = df.columns[3]

# Do NOT fall back to a generic "View Document" / date column.
# The document button is intentionally tied to the softcopy URL column.


# ============================================================
# DEPARTMENT FILTER
# SMALL + LEFT SIDE
# ============================================================

st.markdown(
    '<div class="department-area">',
    unsafe_allow_html=True
)

if department_col:

    departments = (
        df[department_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    departments = sorted(
        [
            d for d in departments.unique()
            if d
        ]
    )

    department_options = [
        "All Departments"
    ] + departments

    selected_department = st.selectbox(
        "Department",
        department_options,
        label_visibility="collapsed"
    )

else:
    selected_department = "All Departments"

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# APPLY DEPARTMENT FILTER
# ============================================================

filtered_df = df.copy()

if (
    selected_department != "All Departments"
    and department_col
):

    filtered_df = filtered_df[
        filtered_df[department_col]
        .astype(str)
        .str.strip()
        == selected_department
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_pt = len(filtered_df)

approved = 0
pending = 0
completed = 0
ongoing = 0


# ------------------------------------------------------------
# APPROVED / PENDING FOR APPROVAL
# ------------------------------------------------------------

if approved_col:

    approval_series = (
        filtered_df[approved_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    approved = approval_series.isin(
        [
            "YES",
            "Y",
            "APPROVED",
            "TRUE",
            "1"
        ]
    ).sum()

    pending = approval_series.isin(
        [
            "NO",
            "N",
            "PENDING",
            "FALSE",
            "0"
        ]
    ).sum()

else:

    if status_col:

        status_series = (
            filtered_df[status_col]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

        approved = status_series.str.contains(
            "APPROVED",
            na=False
        ).sum()

        pending = status_series.str.contains(
            "PENDING",
            na=False
        ).sum()


# ------------------------------------------------------------
# COMPLETED / ONGOING
# ------------------------------------------------------------

if status_col:

    status_series = (
        filtered_df[status_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    completed = status_series.str.contains(
        "COMPLETED",
        na=False
    ).sum()

    ongoing = status_series.str.contains(
        "ONGOING",
        na=False
    ).sum()


approved_pct = percentage(
    approved,
    total_pt
)

pending_pct = percentage(
    pending,
    total_pt
)

completed_pct = percentage(
    completed,
    total_pt
)

ongoing_pct = percentage(
    ongoing,
    total_pt
)


# ============================================================
# SECTION 1
# ONE SINGLE BORDER:
# PROCESS TECHNOLOGY DOCUMENTATION + ALL KPI CARDS
# ============================================================
with st.container(border=True):

    st.markdown(
        '<div class="section-title">PROCESS TECHNOLOGY DOCUMENTATION</div>',
        unsafe_allow_html=True
    )
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(
        5,
        gap="small"
    )


    with kpi1:

        st.markdown(
            f"""
    <div class="kpi-card" style="--accent:#145a96;">
    <div class="kpi-label">TOTAL</div>
    <div class="kpi-value">{total_pt}</div>
    <div class="kpi-subtitle">100% of PT records</div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with kpi2:

        st.markdown(
            f"""
    <div class="kpi-card" style="--accent:#176fc1;">
    <div class="kpi-label">APPROVED</div>
    <div class="kpi-value">{approved}</div>
    <div class="kpi-subtitle">{approved_pct}% of total PT</div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with kpi3:

        st.markdown(
            f"""
    <div class="kpi-card" style="--accent:#c58a00;">
    <div class="kpi-label">PENDING FOR APPROVAL</div>
    <div class="kpi-value">{pending}</div>
    <div class="kpi-subtitle">{pending_pct}% of total PT</div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with kpi4:

        st.markdown(
            f"""
    <div class="kpi-card" style="--accent:#14854a;">
    <div class="kpi-label">COMPLETED</div>
    <div class="kpi-value">{completed}</div>
    <div class="kpi-subtitle">{completed_pct}% of total PT</div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with kpi5:

        st.markdown(
            f"""
    <div class="kpi-card" style="--accent:#c7353d;">
    <div class="kpi-label">ONGOING</div>
    <div class="kpi-value">{ongoing}</div>
    <div class="kpi-subtitle">{ongoing_pct}% of total PT</div>
    </div>
    """,
            unsafe_allow_html=True
        )

    # Real vertical spacer INSIDE the bordered section.
    # This creates a visible gap between the KPI cards and the bottom border.
    st.markdown(
        '<div class="kpi-section-spacer"></div>',
        unsafe_allow_html=True
    )

# ============================================================
# SECTION 2
# ONE SINGLE BORDER:
# PT REGISTER + SEARCH + TABLE
# ============================================================
with st.container(border=True):

    st.markdown(
        '<div class="register-title">PT REGISTER</div>',
        unsafe_allow_html=True
    )
    # ============================================================
    # SEARCH
    # ============================================================

    search_text = st.text_input(
        "Search",
        placeholder="Search PT No., Name of PT, Department...",
        label_visibility="collapsed"
    )


    # ============================================================
    # SEARCH FILTER
    # ============================================================

    display_df = filtered_df.copy()

    if search_text.strip():

        search_value = search_text.strip().lower()

        search_mask = pd.Series(
            False,
            index=display_df.index
        )

        for column in display_df.columns:

            try:

                search_mask = (
                    search_mask
                    |
                    display_df[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        search_value,
                        na=False,
                        regex=False
                    )
                )

            except Exception:
                pass

        display_df = display_df[
            search_mask
        ]


    # ============================================================
    # TABLE
    # ============================================================

    if display_df.empty:

        st.markdown(
            """
    <div class="empty-state">
    No PT records match the selected search.
    </div>
    """,
            unsafe_allow_html=True
        )

    else:

        table_html = """
    <div class="table-scroll">

    <table class="pt-table">

    <thead>
    <tr>
    <th class="sr-col">Sr No.</th>
    <th class="pt-col">PT No.</th>
    <th class="dept-col">Department</th>
    <th class="name-col">Name of PT</th>
    <th class="status-col">Status</th>
    <th class="document-col">View Document</th>
    </tr>
    </thead>

    <tbody>
    """

        # --------------------------------------------------------
        # ROWS
        # --------------------------------------------------------

        for index, (_, row) in enumerate(
            display_df.iterrows(),
            start=1
        ):

            pt_number = (
                clean_value(row[pt_no_col])
                if pt_no_col in row
                else ""
            )

            department = (
                clean_value(row[department_col])
                if department_col in row
                else ""
            )

            pt_name = (
                clean_value(row[name_col])
                if name_col in row
                else ""
            )

            status = (
                clean_value(row[status_col])
                if status_col in row
                else ""
            )

            pt_number_safe = html.escape(
                pt_number
            )

            department_safe = html.escape(
                department
            )

            pt_name_safe = html.escape(
                pt_name
            )

            status_safe = html.escape(
                status
            )


            # ----------------------------------------------------
            # STATUS BADGE
            # ----------------------------------------------------

            badge_class = get_status_class(
                status
            )

            if status:

                status_html = (
                    f'<span class="status-badge '
                    f'{badge_class}">'
                    f'{status_safe.upper()}'
                    f'</span>'
                )

            else:

                status_html = "—"


            # ----------------------------------------------------
            # DOCUMENT
            # ----------------------------------------------------

            document_html = "—"

            if (
                document_col
                and document_col in row
            ):

                document_value = clean_value(
                    row[document_col]
                )

                if document_value:

                    # Accept normal web links as well as Google Drive/Docs
                    # links stored in the "Attach PT Softcopy Link" column.
                    if re.match(r"^https?://", document_value, re.IGNORECASE):

                        document_url = html.escape(
                            document_value,
                            quote=True
                        )

                        document_html = (
                            f'<a class="document-link" '
                            f'href="{document_url}" '
                            f'target="_blank">'
                            f'View Document'
                            f'</a>'
                        )

                    else:

                        document_html = html.escape(
                            document_value
                        )


            table_html += f"""
    <tr>
    <td class="sr-col">{index}</td>
    <td>{pt_number_safe}</td>
    <td>{department_safe}</td>
    <td>{pt_name_safe}</td>
    <td class="status-col">{status_html}</td>
    <td class="document-col">{document_html}</td>
    </tr>
    """


        table_html += """
    </tbody>
    </table>

    </div>
    """

        st.markdown(
            table_html,
            unsafe_allow_html=True
        )