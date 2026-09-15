import io
import re
import base64
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime

import pandas as pd
import requests
from openpyxl import load_workbook
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM Sub Committee Chairman Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# GOOGLE SHEET
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

# IMPORTANT:
# These are the GIDs used for the All Departments dashboard.
# PT and the other modules are NOT read by row count from the
# whole workbook. Each module is loaded from its own tab/GID.
SHEETS = {
    "PT": "1997330551",
    "PHA": "1151637695",
    "PHA Recommendation": "1114420199",
    "MOC": "1493447251",
    "PSSR": "1914804736",
    "PS Incident": "354502422",  # corrected: Incident
    "Training": "1071736559",  # corrected: Training
    "SOC-SOL": "510439154",
    "Interlock ": 1552637895,
    "PSM CE ": 1552637895,
    "Failure Data": 1071263265,
    "Barrier Audit": "1741048982",
    "Audit Compliance": "1790395364",
}

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

    /* ============================================================
       AUDIT REGISTER - COMPACT LOOK
       ============================================================ */
    .audit-register-wrap {
        width:100%;
        max-height:180px;
        overflow-y:auto;
        overflow-x:hidden;
        border:1px solid #d5e0e8;
        border-radius:4px;
        background:#ffffff;
    }

    .audit-register-table {
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        font-size:10px;
        color:#173f70;
    }

    .audit-register-table th {
        position:sticky;
        top:0;
        z-index:2;
        background:#f3f7fa;
        color:#627689;
        font-weight:800;
        text-align:left;
        padding:7px 8px;
        border-bottom:1px solid #d5e0e8;
    }

    .audit-register-table td {
        padding:7px 8px;
        border-bottom:1px solid #e1e8ee;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
    }

    .audit-register-table th:nth-child(1), .audit-register-table td:nth-child(1) { width:8%; }
    .audit-register-table th:nth-child(2), .audit-register-table td:nth-child(2) { width:24%; }
    .audit-register-table th:nth-child(3), .audit-register-table td:nth-child(3) { width:18%; }
    .audit-register-table th:nth-child(4), .audit-register-table td:nth-child(4) { width:17%; }
    .audit-register-table th:nth-child(5), .audit-register-table td:nth-child(5) { width:33%; }

    .audit-register-table a {
        color:#0067c5 !important;
        font-weight:700;
        text-decoration:none;
    }

    .audit-register-table a:hover {
        text-decoration:underline;
    }


    /* ========================================================
       REDUCE SPACE BETWEEN HEADER AND REFRESH BUTTON
       ======================================================== */

    div[data-testid="stButton"] {
        margin-top:-35px !important;
        margin-bottom:0px !important;
    }


/* ============================================================
   MATCH CLICKABLE MODULE HEADINGS WITH NORMAL MODULE HEADING
   ============================================================ */
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

    padding: 4px; 

    display: flex; 

    align-items: center; 

    justify-content: center; 

    flex-shrink: 0; 

    box-sizing: border-box; 

    box-shadow: 
        0 3px 9px 
        rgba(0,0,0,0.20); 

    position: relative; 

    top: -6px; 

    left: 6px; 

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

    height: 4px; 

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

                PSM SUB COMMITTEE CHAIRMAN 

                <span class="main-title-orange"></span> 

            </div> 


            <!-- SUBTITLE --> 

            <div class="subtitle"> 

                PSM SUB COMMITTEE | EXECUTIVE COMMAND CENTER 

            </div> 


            <!-- SUB-SUBTITLE --> 

            <div class="tagline"> 

                GOVERNANCE 
                &nbsp; | &nbsp; 
                RISK 
                &nbsp; | &nbsp; 
                COMPLIANCE 
                &nbsp; | &nbsp; 
                ASSURANCE 

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
    "<div style='height:12px;'></div>",
    unsafe_allow_html=True
)
# ============================================================
# DEPARTMENT STATUS - NO GAP BELOW HEADER
# ============================================================

st.markdown("""
<style>

/* Move complete Department Status section upward */
div[data-testid="stSelectbox"] {
    margin-top: -58px !important;
    margin-bottom: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}

/* Department Status label */
div[data-testid="stSelectbox"] label {
    margin-top: 0px !important;
    margin-bottom: 4px !important;
    padding: 0px !important;

    color: #587086 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.2 !important;
}

/* Selectbox container */
div[data-testid="stSelectbox"] > div {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

/* Dropdown */
div[data-baseweb="select"] {
    margin-top: 0px !important;
}

/* Dropdown box */
div[data-baseweb="select"] > div {
    height: 58px !important;
    min-height: 58px !important;

    background: #ffffff !important;
    border: 1px solid #d2dfe8 !important;
    border-radius: 12px !important;

    box-shadow: 0 4px 14px rgba(15,55,85,0.08) !important;
}

/* Dropdown text */
div[data-baseweb="select"] span {
    font-size: 16px !important;
    color: #394957 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    width: 20px !important;
    height: 20px !important;
}

/* Remove Streamlit bottom spacing */
div[data-testid="stSelectbox"] {
    margin-bottom: -5px !important;
}

</style>
""", unsafe_allow_html=True)

# HELPERS
# ============================================================
def norm(value):
    """Normalize text for safe column/department matching."""
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def find_col(df, candidates):
    """Find a column using exact normalized match, then partial match."""
    if df is None or df.empty:
        return None

    normalized = {norm(c): c for c in df.columns}

    for candidate in candidates:
        key = norm(candidate)
        if key in normalized:
            return normalized[key]

    for column in df.columns:
        ckey = norm(column)
        for candidate in candidates:
            nkey = norm(candidate)
            if nkey in ckey or ckey in nkey:
                return column

    return None


def clean_dataframe(df):
    if df is None or df.empty:
        return pd.DataFrame()

    out = df.copy()
    out.columns = [
        str(c).strip().replace("\n", " ").replace("\r", " ")
        for c in out.columns
    ]

    out = out.dropna(how="all").copy()

    for c in out.columns:
        if out[c].dtype == "object":
            out[c] = out[c].astype(str).str.strip()

    return out


# ============================================================
# GLOBAL DEPARTMENT FILTER
# ============================================================

def filter_selected_department(df, selected_department):
    df = clean_dataframe(df)

    if df.empty:
        return df

    # PSM SUB COMMITTEE CHAIRMAN = no filtering
    if selected_department == "All Departments":
        return df.copy()

    department_col = find_col(
        df,
        [
            "Department",
            "Departments",
            "Dept",
            "Department Name",
            "Department_Name",
            "Dept Name",
            "Dept_Name",
        ],
    )

    # If department column does not exist,
    # return empty for an individual department.
    if department_col is None:
        return pd.DataFrame(columns=df.columns)

    department_values = (
        df[department_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Normalize both sides
    selected_norm = norm(selected_department)

    data_norm = department_values.map(norm)

    # Normal exact match
    mask = data_norm == selected_norm

    # Additional handling for common department names
    if selected_norm == "blastfurnace":
        mask = department_values.str.contains(
            r"blast\s*[-_/ ]*\s*furnace",
            case=False,
            regex=True,
            na=False,
        )

    elif selected_norm == "cokeoven":
        mask = department_values.str.contains(
            r"coke\s*[-_/ ]*oven",
            case=False,
            regex=True,
            na=False,
        )


    elif selected_norm == "sms1":
        mask = department_values.str.contains(
            r"sms\s*[-_/ ]*1",
            case=False,
            regex=True,
            na=False,
        )

    elif selected_norm == "sms2":
        mask = department_values.str.contains(
            r"sms\s*[-_/ ]*2",
            case=False,
            regex=True,
            na=False,
        )

    elif selected_norm == "centralutility":
        mask = department_values.str.contains(
            r"central\s*[-_/ ]*utility",
            case=False,
            regex=True,
            na=False,
        )

    elif selected_norm == "tubeMill".lower():
        mask = department_values.str.contains(
            r"tube\s*[-_/ ]*mill",
            case=False,
            regex=True,
            na=False,
        )

    elif selected_norm == "pelletbeneficiation":
        mask = department_values.str.contains(
            r"pellet.*beneficiation|beneficiation.*pellet",
            case=False,
            regex=True,
            na=False,
        )

    return df.loc[mask].copy()


def load_csv_from_url(url):
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    # Google export is normally UTF-8 CSV.
    # Use StringIO so pandas gets a text stream.
    return pd.read_csv(io.StringIO(response.content.decode("utf-8-sig")))


@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(gid):
    """
    Load ONE exact Google Sheet tab by GID.

    This avoids the previous problem where the code used sheet
    names and could end up reading the wrong tab.
    """
    if not gid:
        return pd.DataFrame()

    export_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=csv&gid={gid}"
    )

    try:
        df = load_csv_from_url(export_url)
        return clean_dataframe(df)
    except Exception:
        # Fallback to Google visualization endpoint.
        gviz_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{SPREADSHEET_ID}/gviz/tq?"
            f"tqx=out:csv&gid={gid}"
        )

        try:
            df = load_csv_from_url(gviz_url)
            return clean_dataframe(df)
        except Exception:
            return pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def load_interlock_sheet():
    """
    Find and load the real Interlock tab from the Google workbook.

    The Interlock tab is identified by its actual register headers rather
    than a hard-coded GID. This prevents the dashboard from accidentally
    reading another tab when the GID is incorrect.
    """
    xlsx_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=xlsx"
    )

    try:
        response = requests.get(
            xlsx_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        workbook = load_workbook(
            filename=io.BytesIO(response.content),
            data_only=True,
            read_only=True,
        )

        required_headers = {
            "sno",
            "department",
            "interlockdescription",
            "datebypassed",
            "presentstatusactionrequired",
        }

        for worksheet in workbook.worksheets:
            rows = worksheet.iter_rows(values_only=True)

            # Look through the first 10 rows for the register header.
            header_found = None
            buffered = []
            for row_number, row in enumerate(rows):
                buffered.append(row)
                if row_number >= 9:
                    break

                normalized_headers = {
                    re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())
                    for value in row
                    if value is not None
                }

                if required_headers.issubset(normalized_headers):
                    header_found = row_number
                    break

            if header_found is None:
                continue

            all_rows = list(buffered)
            all_rows.extend(list(rows))

            headers = list(all_rows[header_found])
            data_rows = all_rows[header_found + 1:]

            # Remove completely blank columns from the header.
            valid_columns = [
                i for i, value in enumerate(headers)
                if value is not None and str(value).strip() != ""
            ]

            if not valid_columns:
                continue

            clean_headers = [str(headers[i]).strip() for i in valid_columns]
            records = []

            for row in data_rows:
                values = [
                    row[i] if i < len(row) else None
                    for i in valid_columns
                ]
                if any(
                    value is not None and str(value).strip() != ""
                    for value in values
                ):
                    records.append(values)

            return clean_dataframe(
                pd.DataFrame(records, columns=clean_headers)
            )

    except Exception:
        return pd.DataFrame()

    return pd.DataFrame()


class _AuditLinkParser(HTMLParser):
    """Extract cell text and real hyperlinks from Google Sheets GViz HTML."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self._row = None
        self._cell_open = False
        self._cell_href = ""
        self._cell_text = []
        self._in_table = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()

        if tag == "table":
            self._in_table = True
        elif self._in_table and tag == "tr":
            self._row = []
        elif self._in_table and tag in ("td", "th") and self._row is not None:
            self._cell_open = True
            self._cell_href = ""
            self._cell_text = []
        elif self._in_table and tag == "a" and self._cell_open:
            self._cell_href = attrs.get("href", "") or ""

    def handle_data(self, data):
        if self._cell_open:
            self._cell_text.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("td", "th") and self._cell_open:
            self._row.append({
                "text": " ".join(self._cell_text).strip(),
                "href": self._cell_href.strip(),
            })
            self._cell_open = False
            self._cell_href = ""
            self._cell_text = []
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
        elif tag == "table":
            self._in_table = False


def load_audit_with_links(gid):
    """Load Audit tab and recover the live Audit Report hyperlinks.

    The Google Sheet uses rich-text hyperlinks in the Audit Report column.
    We first try XLSX hyperlinks, then GViz HTML, and finally create a
    row-specific Google Sheet link so a report is never incorrectly shown
    as 'Not attached' when the report name exists.
    """
    df = load_google_sheet(gid)
    if df.empty or not gid:
        return df

    df = clean_dataframe(df).copy()
    url_values = [""] * len(df)

    # Identify the actual Audit Report column from the loaded sheet.
    audit_report_col = find_col(
        df,
        ["Audit Report", "Audit Report Link", "Compliance Report", "Report"],
    )

    # ------------------------------------------------------------
    # METHOD 1: XLSX cell hyperlinks
    # ------------------------------------------------------------
    xlsx_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=xlsx&gid={gid}"
    )

    try:
        response = requests.get(
            xlsx_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        workbook = load_workbook(
            filename=io.BytesIO(response.content),
            data_only=False,
            read_only=False,
        )
        ws = workbook.active

        header_row = None
        report_col_num = None

        for row in ws.iter_rows():
            for cell in row:
                value = norm(cell.value)
                if value in {
                    "auditreport",
                    "auditreportlink",
                    "compliancereport",
                    "compliancereportlink",
                    "report",
                }:
                    header_row = cell.row
                    report_col_num = cell.column
                    break
            if report_col_num is not None:
                break

        if report_col_num is not None:
            for row_no in range((header_row or 1) + 1, ws.max_row + 1):
                cell = ws.cell(row=row_no, column=report_col_num)
                url = ""

                if cell.hyperlink:
                    try:
                        url = str(cell.hyperlink.target or "").strip()
                    except Exception:
                        url = ""

                if not url and isinstance(cell.value, str):
                    match = re.search(
                        r'HYPERLINK\s*\(\s*["\'](https?://[^"\']+)["\']',
                        cell.value,
                        flags=re.IGNORECASE,
                    )
                    if match:
                        url = match.group(1).strip()

                idx = row_no - (header_row or 1) - 1
                if 0 <= idx < len(url_values) and url:
                    url_values[idx] = url

        workbook.close()
    except Exception:
        pass

    # ------------------------------------------------------------
    # METHOD 2: GViz HTML - preserves rich-text hyperlinks
    # ------------------------------------------------------------
    try:
        gviz_html_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{SPREADSHEET_ID}/gviz/tq?"
            f"tqx=out:html&gid={gid}"
        )

        gviz_response = requests.get(
            gviz_html_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        gviz_response.raise_for_status()

        parser = _AuditLinkParser()
        parser.feed(gviz_response.text)

        if parser.rows and audit_report_col:
            report_index = list(df.columns).index(audit_report_col)
            source_rows = parser.rows[1:]  # first row is the header

            for i, parsed_row in enumerate(source_rows):
                if i >= len(url_values) or url_values[i]:
                    continue

                if report_index < len(parsed_row):
                    href = parsed_row[report_index].get("href", "").strip()
                    if href:
                        url_values[i] = href
    except Exception:
        pass

    # ------------------------------------------------------------
    # METHOD 3: if the rich-text URL cannot be exposed by Google,
    # link directly to the corresponding Audit Report cell.
    # This keeps the report accessible instead of showing Not attached.
    # ------------------------------------------------------------
    if audit_report_col:
        for i in range(len(df)):
            if url_values[i]:
                continue

            report_name = str(df.iloc[i][audit_report_col]).strip()
            if report_name and report_name.lower() not in {"nan", "none"}:
                sheet_row = i + 2  # header is row 1
                url_values[i] = (
                    f"https://docs.google.com/spreadsheets/d/"
                    f"{SPREADSHEET_ID}/edit?gid={gid}"
                    f"&range=E{sheet_row}"
                )

    df["__COMPLIANCE_REPORT_URL"] = url_values
    return df



@st.cache_data(ttl=300, show_spinner=False)
def load_psm_ce_sheet():
    """
    Find and load the real PSM CE tab from the Google workbook.

    The PSM CE tab is identified from its actual headers so it does not
    depend on a possibly incorrect/hard-coded GID.
    """
    xlsx_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=xlsx"
    )

    try:
        response = requests.get(
            xlsx_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        workbook = load_workbook(
            filename=io.BytesIO(response.content),
            data_only=True,
            read_only=True,
        )

        required_headers = {
            "slno",
            "month",
            "department",
            "noofpsmcefailedbreakdown",
            "complianceofpsmcemo–mechanical–generated",
            "complianceofpsmcemo–mechanical–completed",
            "complianceofpsmcemo–e&i–generated",
            "complianceofpsmcemo–e&i–completed",
        }

        def normalized_header(value):
            text = str(value).strip().lower()
            text = text.replace("–", "-").replace("—", "-")
            text = text.replace("&", "and")
            return re.sub(r"[^a-z0-9]+", "", text)

        for worksheet in workbook.worksheets:
            rows = worksheet.iter_rows(values_only=True)
            buffered = []
            header_found = None

            for row_number, row in enumerate(rows):
                buffered.append(row)
                if row_number >= 9:
                    break

                normalized_headers = {
                    normalized_header(value)
                    for value in row
                    if value is not None
                }

                # Use the distinctive PSM CE headers.  The exact wording
                # can vary slightly in punctuation, so use key fragments.
                has_slno = "slno" in normalized_headers
                has_month = "month" in normalized_headers
                has_department = "department" in normalized_headers
                has_failed = any(
                    "noofpsmcefailedbreakdown" in h
                    for h in normalized_headers
                )
                has_mech_generated = any(
                    "complianceofpsmcemo" in h
                    and "mechanical" in h
                    and "generated" in h
                    for h in normalized_headers
                )
                has_mech_completed = any(
                    "complianceofpsmcemo" in h
                    and "mechanical" in h
                    and "completed" in h
                    for h in normalized_headers
                )
                has_ei_generated = any(
                    "complianceofpsmcemo" in h
                    and ("ei" in h or "eandl" in h or "eandi" in h)
                    and "generated" in h
                    for h in normalized_headers
                )
                has_ei_completed = any(
                    "complianceofpsmcemo" in h
                    and ("ei" in h or "eandl" in h or "eandi" in h)
                    and "completed" in h
                    for h in normalized_headers
                )

                if (
                    has_slno
                    and has_month
                    and has_department
                    and has_failed
                    and has_mech_generated
                    and has_mech_completed
                    and has_ei_generated
                    and has_ei_completed
                ):
                    header_found = row_number
                    break

            if header_found is None:
                continue

            all_rows = list(buffered)
            all_rows.extend(list(rows))

            headers = list(all_rows[header_found])
            valid_columns = [
                i for i, value in enumerate(headers)
                if value is not None and str(value).strip() != ""
            ]

            if not valid_columns:
                continue

            clean_headers = [
                str(headers[i]).strip()
                for i in valid_columns
            ]
            records = []

            for row in all_rows[header_found + 1:]:
                values = [
                    row[i] if i < len(row) else None
                    for i in valid_columns
                ]
                if any(
                    value is not None and str(value).strip() != ""
                    for value in values
                ):
                    records.append(values)

            return clean_dataframe(
                pd.DataFrame(records, columns=clean_headers)
            )

    except Exception:
        return pd.DataFrame()

    return pd.DataFrame()

def load_module(name):
    """Load the complete module data for all departments."""
    return load_google_sheet(SHEETS.get(name))


def status_counts(df, status_candidates=None):
    result = {
        "total": 0,
        "completed": 0,
        "ongoing": 0,
        "pending": 0,
        "overdue": 0,
        "open": 0,
        "closed": 0,
    }

    if df is None or df.empty:
        return result

    result["total"] = len(df)

    if status_candidates is None:
        status_candidates = [
            "Status",
            "Current Status",
            "Action Status",
            "Completion Status",
            "Investigation Status",
            "Recommendation Status",
        ]

    status_col = find_col(df, status_candidates)

    if status_col is None:
        return result

    s = (
        df[status_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    result["completed"] = int(
        s.str.contains(r"\bcompleted?\b|\bcomplete\b", regex=True).sum()
    )

    result["ongoing"] = int(
        s.str.contains(r"ongoing|in progress|in-progress", regex=True).sum()
    )

    result["pending"] = int(
        s.str.contains(r"pending", regex=True).sum()
    )

    result["overdue"] = int(
        s.str.contains(r"overdue", regex=True).sum()
    )

    result["open"] = int(
        s.str.fullmatch(r"open", case=False, na=False).sum()
    )

    result["closed"] = int(
        s.str.fullmatch(r"closed", case=False, na=False).sum()
    )

    return result


def make_register(df, id_names, description_names, status_names):
    if df is None or df.empty:
        return pd.DataFrame()

    id_col = find_col(df, id_names)
    desc_col = find_col(df, description_names)
    status_col = find_col(df, status_names)

    result = pd.DataFrame(index=df.index)

    # -----------------------------
    # ID / NUMBER
    # -----------------------------
    if id_col:
        result["No."] = (
            df[id_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )
    else:
        result["No."] = [
            f"{i + 1:03d}" for i in range(len(df))
        ]

    # -----------------------------
    # DESCRIPTION
    # -----------------------------
    if desc_col:
        result["Description"] = (
            df[desc_col]
            .fillna("-")
            .astype(str)
            .str.strip()
        )
    else:
        result["Description"] = "-"

    # -----------------------------
    # STATUS
    # -----------------------------
    if status_col:
        result["Status"] = (
            df[status_col]
            .fillna("-")
            .astype(str)
            .str.strip()
        )
    else:
        result["Status"] = "-"

    return result.reset_index(drop=True)


# ============================================================
# STATUS COLOUR
# ============================================================

def status_style(value):
    value = str(value).strip().lower()

    if value in ["completed", "complete", "closed"]:
        return "color: #008000; font-weight: 800;"

    elif value in ["ongoing", "in progress", "in-progress", "pending"]:
        return "color: #e67e00; font-weight: 800;"

    elif value in ["overdue", "open"]:
        return "color: #d71920; font-weight: 800;"

    else:
        return "color: #333333;"


# ============================================================
# REGISTER DISPLAY
# ============================================================

def show_register(title, df, id_names, description_names, status_names):
    st.markdown(
        f'<div class="section-bar">{title}</div>',
        unsafe_allow_html=True,
    )

    register_df = make_register(
        df,
        id_names,
        description_names,
        status_names,
    )

    if register_df.empty:

        st.info("No records found.")

    else:

        # Apply colour ONLY to Status column
        styled_df = (
            register_df.style
            .map(
                status_style,
                subset=["Status"]
            )
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            height=260,
        )


def make_moc_register(df):
    """Build the compact MOC register: MOC No., Description, Type, Status, Remarks."""
    if df is None or df.empty:
        return pd.DataFrame()

    moc_no_col = find_col(
        df,
        [
            "MOC No",
            "MOC No.",
            "MOC Number",
            "MOC ID",
            "Request No",
            "Request ID",
            "Sr No",
            "Sr. No",
            "Serial No",
            "ID",
        ],
    )

    desc_col = find_col(
        df,
        [
            "Description of Change",
            "Description of the Change",
            "MOC Description",
            "Change Description",
            "Description",
        ],
    )

    type_col = find_col(
        df,
        [
            "Change Type (Permanent/Temporary/Emergency)",
            "Change Type (Permanent / Temporary / Emergency)",
            "Change Type",
            "MOC Change Type",
            "Type of Change",
            "Type",
        ],
    )

    status_col = find_col(
        df,
        [
            "Status (Open/Close)",
            "Status (Open / Close)",
            "Status",
            "Current Status",
            "MOC Status",
        ],
    )

    remarks_col = find_col(
        df,
        [
            "Remarks",
            "Remark",
            "Comments",
            "Comment",
        ],
    )

    result = pd.DataFrame(index=df.index)

    if moc_no_col:
        result["MOC No."] = (
            df[moc_no_col].fillna("").astype(str).str.strip()
        )
    else:
        result["MOC No."] = [
            f"{i + 1:03d}" for i in range(len(df))
        ]

    result["Description"] = (
        df[desc_col].fillna("-").astype(str).str.strip()
        if desc_col else "-"
    )

    result["Type"] = (
        df[type_col].fillna("-").astype(str).str.strip()
        if type_col else "-"
    )

    result["Status"] = (
        df[status_col].fillna("-").astype(str).str.strip()
        if status_col else "-"
    )

    result["Remarks"] = (
        df[remarks_col].fillna("-").astype(str).str.strip()
        if remarks_col else "-"
    )

    return result.reset_index(drop=True)


def show_moc_register(df):
    st.markdown(
        '<div class="section-bar">MOC REGISTER</div>',
        unsafe_allow_html=True,
    )

    register_df = make_moc_register(df)

    if register_df.empty:
        st.info("No MOC records found.")
        return

    styled_df = (
        register_df.style
        .map(
            status_style,
            subset=["Status"]
        )
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=120,
        column_config={
            "MOC No.": st.column_config.TextColumn("MOC No.", width="small"),
            "Description": st.column_config.TextColumn("Description", width="small"),
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Remarks": st.column_config.TextColumn("Remarks", width="small"),
        },
    )


# ============================================================
# MODULE PAGE LINKS
# ============================================================

MODULE_PAGE_LINKS = {
    "PROCESS TECHNOLOGY (PT)": "pages/09_PT.py",
    "PROCESS HAZARD ANALYSIS (PHA)": "pages/10_PHA.py",
    "PHA RECOMMENDATION": "pages/10_PHA.py",
    "MOC": "pages/11_MOC.py",
    "PRE-STARTUP SAFETY REVIEW (PSSR)": "pages/12_PSSR.py",
    "PROCESS SAFETY INCIDENT": "pages/14_PSI.py",
    "TRAINING": "pages/13_Training.py",
    "INTERLOCK BYPASS": "pages/19_ALARM_&_INTERLOCK_MANAGEMENT.py",
    "PSM CE": "pages/20_PSM CE & BARRIER HEALTH.py",
}


def show_module_title(number, icon, title):
    page = MODULE_PAGE_LINKS.get(title)

    if page:
        st.page_link(
            page,
            label=f"🔴 {number} {icon} {title}",
        )
    else:
        st.markdown(
            f'<div class="module-title">🔴 {number} {icon} {title}</div>',
            unsafe_allow_html=True,
        )


def show_metric_row(items):
    cols = st.columns(len(items), gap="small")
    for c, (label, value) in zip(cols, items):
        with c:
            st.metric(label, value)


def get_date_column(df):
    return find_col(
        df,
        [
            "Date",
            "Audit Date",
            "Last Audit Date",
            "Deviation Date",
            "Record Date",
            "Incident Date",
        ],
    )


# ============================================================
# LOAD DATA
# ============================================================
loaded = {}

for module_name in SHEETS:
    loaded[module_name] = load_module(module_name)

pt = loaded["PT"]
pha = loaded["PHA"]
rec = loaded["PHA Recommendation"]
moc = loaded["MOC"]
pssr = loaded["PSSR"]
training = loaded["Training"]
soc = loaded["SOC-SOL"]
incident = loaded["PS Incident"]
interlock = load_interlock_sheet()
psm_ce = load_psm_ce_sheet()
loaded["PSM CE "] = psm_ce
audit = load_audit_with_links(SHEETS["Audit Compliance"])
failure_data = loaded["Failure Data"]

# ============================================================
# PSM SUB COMMITTEE CHAIRMAN — EXECUTIVE COMMAND CENTER
# Uses ONLY live Google Sheet data loaded above.
# No KPI values are hard-coded; missing source data is shown as —.
# ============================================================

st.markdown("""
<style>
/* PROFESSIONAL EXECUTIVE DASHBOARD BACKGROUND */
.stApp {
    background:
        radial-gradient(circle at 92% 8%, rgba(7,81,139,.055) 0, rgba(7,81,139,0) 28%),
        radial-gradient(circle at 6% 42%, rgba(242,140,0,.035) 0, rgba(242,140,0,0) 24%),
        linear-gradient(180deg, #f7f9fb 0%, #eef3f7 100%) !important;
}
[data-testid="stAppViewContainer"] {
    background:transparent !important;
}
[data-testid="stHeader"] {
    background:transparent !important;
}
.main .block-container {
    background:transparent !important;
}
/* Clean, readable department selector area */
div[data-testid="stSelectbox"] label {
    color:#52687a !important;
    font-weight:800 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background:#ffffff !important;
    border:1px solid #d5e0e8 !important;
    box-shadow:0 3px 12px rgba(22,55,78,.06) !important;
}
.block-container { padding:0.25rem 1rem 1rem 1rem !important; max-width:100% !important; }
.chair-wrap { margin-top:-10px; }
.chair-banner { position:relative; overflow:hidden; border-radius:16px; padding:18px 24px 16px; background:linear-gradient(110deg,#041725,#0a3554 55%,#0b5575); border:1px solid rgba(255,255,255,.16); box-shadow:0 12px 32px rgba(0,0,0,.25); }
.chair-banner:after { content:""; position:absolute; width:360px; height:360px; right:-150px; top:-180px; border-radius:50%; border:55px solid rgba(242,140,0,.12); }
.chair-kicker { color:#f5a623; font-size:11px; font-weight:900; letter-spacing:3px; text-transform:uppercase; }
.chair-title { color:#fff; font-size:30px; line-height:1.05; font-weight:950; margin-top:5px; letter-spacing:.3px; }
.chair-sub { color:#c9dbe8; font-size:12px; margin-top:7px; letter-spacing:1.8px; font-weight:700; }
.live-pill { display:inline-block; margin-top:12px; padding:5px 10px; border-radius:99px; background:rgba(28,188,117,.15); border:1px solid rgba(28,188,117,.45); color:#83efbd; font-size:10px; font-weight:900; letter-spacing:1px; }
.filter-card { background:rgba(255,255,255,.96); border:1px solid #d5e1e9; border-radius:12px; padding:8px 12px 2px; box-shadow:0 5px 18px rgba(17,49,72,.10); margin:10px 0; }
.section-head { display:flex; align-items:center; justify-content:space-between; padding:7px 2px 6px; margin-top:6px; }
.section-head .left { color:#073f78; font-size:14px; font-weight:950; letter-spacing:.6px; }
.section-head .right { color:#708394; font-size:9px; font-weight:800; text-transform:uppercase; letter-spacing:1.2px; }
.kpi { position:relative; height:150px; min-height:150px; max-height:150px; box-sizing:border-box; border-radius:13px; padding:14px 15px; background:#fff; border:1px solid #d7e2e9; box-shadow:0 7px 20px rgba(17,49,72,.10); overflow:hidden; display:flex; flex-direction:column; }
.kpi:before { content:""; position:absolute; left:0; top:0; bottom:0; width:5px; background:#0b5b87; }
.kpi.warn:before { background:#e99a16; } .kpi.danger:before { background:#d42f3d; }
.kpi-label { color:#60788a; font-size:9px; font-weight:900; letter-spacing:1.1px; text-transform:uppercase; line-height:1.45; height:38px; min-height:38px; max-height:38px; overflow:hidden; display:flex; align-items:flex-start; }
.kpi-value { color:#0b3459; font-size:30px; line-height:1.05; font-weight:950; margin-top:4px; height:34px; min-height:34px; }
.kpi-note { color:#8798a5; font-size:9px; line-height:1.55; margin-top:5px; font-weight:700; min-height:28px; overflow:hidden; }
.module-card { background:#fff; border:1px solid #d7e2e9; border-radius:13px; padding:12px 13px; box-shadow:0 7px 20px rgba(17,49,72,.09); min-height:178px; }
.module-top { display:flex; justify-content:space-between; align-items:center; }
.module-name { color:#073f78; font-size:11px; font-weight:950; letter-spacing:.5px; }
.module-number { color:#f28c00; font-size:10px; font-weight:950; }
.module-value { font-size:28px; color:#0b3459; font-weight:950; margin-top:10px; }
.module-meta { font-size:9px; color:#718596; margin-top:2px; font-weight:700; }
.bar-bg { height:7px; border-radius:99px; background:#e8eef2; margin-top:12px; overflow:hidden; }
.bar-fill { height:100%; border-radius:99px; background:linear-gradient(90deg,#0a557d,#18a6a2); }
.alert-box { background:linear-gradient(110deg,#fff,#fff8ed); border:1px solid #f0d6a0; border-left:5px solid #e99a16; border-radius:12px; padding:12px 14px; margin-bottom:8px; }
.alert-title { color:#8b5b08; font-size:11px; font-weight:950; letter-spacing:.7px; }
.alert-value { color:#243c50; font-size:22px; font-weight:950; margin-top:2px; }
.note { color:#718596; font-size:9px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

def _source_status_counts(df):
    out={"total":None,"completed":None,"open":None,"overdue":None}
    if df is None or df.empty: return out
    out["total"]=int(len(df))
    col=find_col(df,["Status","Current Status","Action Status","Completion Status","Investigation Status","Recommendation Status","Overdue/Pending/Completed","Present Status / Action Required"])
    if col is None: return out
    s=df[col].fillna("").astype(str).str.strip().str.lower()
    out["completed"]=int(s.str.contains(r"completed?|closed",regex=True).sum())
    out["open"]=int(s.str.contains(r"open|ongoing|in progress|in-progress|pending|due",regex=True).sum())
    out["overdue"]=int(s.str.contains(r"overdue",regex=True).sum())
    return out

def _fmt(v):
    if v is None: return "—"
    if isinstance(v,float) and v.is_integer(): return f"{int(v):,}"
    return f"{v:,}" if isinstance(v,(int,float)) else str(v)

def _pct(done,total):
    if done is None or total in (None,0): return None
    return max(0,min(100,done/total*100))

def _num_col_sum(df,candidates):
    if df is None or df.empty: return None
    col=find_col(df,candidates)
    if col is None: return None
    v=pd.to_numeric(df[col],errors="coerce").dropna()
    return float(v.sum()) if not v.empty else None

def _dept_col(df):
    return find_col(df,["Department","Departments","Dept","Department Name","Department_Name","Dept Name","Dept_Name"])

def _dept_names():
    names=set()
    for df in loaded.values():
        if df is None or df.empty: continue
        c=_dept_col(df)
        if c:
            names.update(x for x in df[c].dropna().astype(str).str.strip() if x and x.lower() not in {"nan","none","-"})
    return sorted(names,key=str.casefold)

def _filter(df,dept):
    return filter_selected_department(df,dept) if dept!="All Departments" else clean_dataframe(df)

def _status_sum(frames,key):
    found=False; total=0
    for df in frames:
        c=_source_status_counts(df)
        if c[key] is not None: found=True; total+=c[key]
    return total if found else None

# ============================================================
# FIXED DEPARTMENT LIST
# Use exactly the approved department names for this dashboard.
# ============================================================
ALL_DEPARTMENTS = [
    "All Departments",
    "Blast Furnace",
    "Coke Oven",
    "SMS-1",
    "SMS-2",
    "DRI",
    "Central Utility",
    "CRM",
    "WRM",
    "CPP",
    "Sinter",
    "Tube Mill",
    "CSP",
    "Pellet & Beneficiation",
    "LCP",
]

with st.container():
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    selected_department = st.selectbox(
        "Department Status",
        ALL_DEPARTMENTS,
        index=0,
        key="chairman_department_selector",
    )
    st.markdown('</div>', unsafe_allow_html=True)

D={k:_filter(v,selected_department) for k,v in loaded.items()}
D["Interlock "]=_filter(interlock,selected_department)
D["PSM CE "]=_filter(psm_ce,selected_department)
D["Audit Compliance"]=_filter(audit,selected_department)

active_rows=sum(len(v) for v in D.values() if v is not None and not v.empty)
modules_with_data=sum(1 for v in D.values() if v is not None and not v.empty)


st.markdown(f'<div class="section-head"><div class="left">EXECUTIVE SAFETY PULSE</div><div class="right">ACTUAL SOURCE DATA • {selected_department}</div></div>',unsafe_allow_html=True)

core=["PT","PHA","PHA Recommendation","MOC","PSSR","Training","SOC-SOL","PS Incident","Interlock ","PSM CE ","Audit Compliance","Failure Data","Barrier Audit"]
frames=[D[k] for k in core]
total_records=sum(len(x) for x in frames if x is not None and not x.empty)
open_items=_status_sum(frames,"open")
overdue=_status_sum(frames,"overdue")
incidents=len(D["PS Incident"]) if D["PS Incident"] is not None and not D["PS Incident"].empty else None
moc=_source_status_counts(D["MOC"]); pssr=_source_status_counts(D["PSSR"]); inter=_source_status_counts(D["Interlock "])
psmce_failed=_num_col_sum(D["PSM CE "],["No. of PSM CE failed (Breakdown)","No. Of PSM CE Failed (Breakdown)","PSM CE Failed","PSM CE Failed (Breakdown)"])

kpis=[
("PSM SOURCE RECORDS",_fmt(total_records),"Live rows across source modules",""),
("OPEN / ACTIVE",_fmt(open_items),"Open • ongoing • pending • due","warn"),
("OVERDUE",_fmt(overdue),"Actual source status","danger"),
("PROCESS SAFETY INCIDENTS",_fmt(incidents),"Actual incident records","danger" if incidents and incidents>0 else ""),
("MOC OPEN / ACTIVE",_fmt(moc["open"]),"Actual MOC status","warn"),
("PSSR OVERDUE",_fmt(pssr["overdue"]),"Actual PSSR status","danger"),
("INTERLOCK ACTION",_fmt(inter["open"]),"Actual interlock status","warn"),
("PSM CE FAILED",_fmt(psmce_failed),"Actual PSM CE breakdown","danger" if psmce_failed and psmce_failed>0 else ""),]
cols=st.columns(8,gap="small")
for col,(label,val,note,kind) in zip(cols,kpis):
    with col: st.markdown(f'<div class="kpi {kind}"><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section-head"><div class="left">PSM GOVERNANCE MODULE PULSE</div><div class="right">SOURCE-BACKED • NO FIXED KPI VALUES</div></div>',unsafe_allow_html=True)
modules=[("PT","PROCESS TECHNOLOGY"),("PHA","PROCESS HAZARD ANALYSIS"),("PHA Recommendation","PHA RECOMMENDATION"),("MOC","MANAGEMENT OF CHANGE"),("PSSR","PRE-STARTUP SAFETY REVIEW"),("PS Incident","PROCESS SAFETY INCIDENT"),("Training","TRAINING"),("SOC-SOL","SOC / SOL DEVIATION"),("Audit Compliance","AUDIT / COMPLIANCE"),("Interlock ","INTERLOCK BYPASS"),("PSM CE ","PSM CE NOTIFICATION"),("Barrier Audit","BARRIER AUDIT"),("Failure Data","C4/C5 FAILURE DATA")]
for start in range(0,len(modules),4):
    row=st.columns(4,gap="small")
    for col,(key,label) in zip(row,modules[start:start+4]):
        df=D.get(key,pd.DataFrame()); c=_source_status_counts(df); total=c["total"]
        if key=="PS Incident": headline=_fmt(total); note="Actual incident records"; pct=None
        elif key=="PSM CE ": headline=_fmt(psmce_failed); note="Actual PSM CE failed / breakdown"; pct=None
        else:
            headline=_fmt(total); note=f'Completed: {_fmt(c["completed"])} • Open: {_fmt(c["open"])}'; pct=_pct(c["completed"],total)
        bar="" if pct is None else f'<div class="bar-bg"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="module-meta">{pct:.1f}% completed (derived)</div>'
        with col: st.markdown(f'<div class="module-card"><div class="module-top"><div class="module-name">{label}</div><div class="module-number">{key.strip()}</div></div><div class="module-value">{headline}</div><div class="module-meta">{note}</div>{bar}</div>',unsafe_allow_html=True)

st.markdown('<div class="section-head"><div class="left">DEPARTMENT ACTION WATCHLIST</div><div class="right">RANKED USING ACTUAL STATUS FIELDS</div></div>',unsafe_allow_html=True)
rows=[]
for dept in _dept_names():
    tr=co=op=ov=0; has=False
    for df in loaded.values():
        f=_filter(df,dept)
        if f is None or f.empty: continue
        c=_source_status_counts(f); has=True
        tr+=c["total"] or 0; co+=c["completed"] or 0; op+=c["open"] or 0; ov+=c["overdue"] or 0
    if has: rows.append({"Department":dept,"Source Records":tr,"Completed":co,"Open / Active":op,"Overdue":ov})
if selected_department!="All Departments": rows=[r for r in rows if r["Department"]==selected_department]
watch=pd.DataFrame(rows)
if not watch.empty:
    watch=watch.sort_values(["Overdue","Open / Active","Source Records"],ascending=[False,False,False]).reset_index(drop=True)
    st.dataframe(watch,use_container_width=True,hide_index=True,height=min(390,80+len(watch)*35),column_config={"Department":st.column_config.TextColumn("DEPARTMENT"),"Source Records":st.column_config.NumberColumn("SOURCE RECORDS",format="%d"),"Completed":st.column_config.NumberColumn("COMPLETED",format="%d"),"Open / Active":st.column_config.NumberColumn("OPEN / ACTIVE",format="%d"),"Overdue":st.column_config.NumberColumn("OVERDUE",format="%d")})
else: st.info("No department-level status data is available in the Google Sheet for this view.")

st.markdown('<div class="section-head"><div class="left">CHAIRMAN ATTENTION PANEL</div><div class="right">ONLY SOURCE-BACKED EXCEPTIONS</div></div>',unsafe_allow_html=True)
attention=[]
def add_attention(title,value,detail):
    if value is not None and value>0: attention.append((title,value,detail))
add_attention("OVERDUE PSM ITEMS",overdue,"Actual overdue statuses")
add_attention("PSSR OVERDUE",pssr["overdue"],"Actual PSSR status")
add_attention("MOC OPEN / ACTIVE",moc["open"],"Actual MOC status")
add_attention("INTERLOCK ACTIONS",inter["open"],"Actual interlock status / action")
add_attention("PSM CE FAILED",psmce_failed,"Actual PSM CE breakdown field")
add_attention("PROCESS SAFETY INCIDENTS",incidents,"Actual incident records")
if attention:
    ac=st.columns(min(3,len(attention)),gap="small")
    for col,(title,val,detail) in zip(ac,attention):
        with col: st.markdown(f'<div class="alert-box"><div class="alert-title">{title}</div><div class="alert-value">{_fmt(val)}</div><div class="note">{detail}</div></div>',unsafe_allow_html=True)
else: st.success("No source-backed exception count is above zero in the selected view.")

audit_df=D.get("Audit Compliance")
if audit_df is not None and not audit_df.empty:
    score_col=find_col(audit_df,["Audit Score","Score","Audit Compliance Score"])
    if score_col:
        scores=pd.to_numeric(audit_df[score_col],errors="coerce").dropna()
        if not scores.empty:
            st.markdown('<div class="section-head"><div class="left">AUDIT ASSURANCE — SOURCE SCORE</div><div class="right">DIRECT FROM AUDIT COMPLIANCE SHEET</div></div>',unsafe_allow_html=True)
            a1,a2,a3=st.columns(3,gap="small")
            with a1: st.metric("AVERAGE AUDIT SCORE",f"{scores.mean():.1f}")
            with a2: st.metric("HIGHEST AUDIT SCORE",f"{scores.max():.1f}")
            with a3: st.metric("AUDIT RECORDS SCORED",f"{len(scores):,}")

st.markdown(f'<div style="text-align:center;padding:12px;color:#7890a0;font-size:9px;font-weight:800;letter-spacing:1px;">PSM SUB COMMITTEE CHAIRMAN DASHBOARD • GOOGLE SHEET SOURCE • LAST REFRESH {datetime.now().strftime("%d-%b-%Y %H:%M:%S")} • VIEW: {selected_department.upper()}</div>',unsafe_allow_html=True)
