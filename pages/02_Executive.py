import io
import re
import base64
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
from zoneinfo import ZoneInfo

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
    page_title="PSM Dashboard - All Departments",
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
        background:#eef5fa;
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
    background:linear-gradient(180deg,#ffffff 0%,#f9fcff 100%);
    border:1px solid #c9ddea;
    border-radius:10px;
    padding:10px 10px !important;
    min-height:82px;
    overflow:visible !important;
    box-shadow:0 2px 8px rgba(28,73,105,.06);
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
        color:#124a82 !important;
        font-size:28px !important;
        font-weight:950 !important;
        line-height:1.05 !important;
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
        background:#07558f;
        color:#ffffff;
        border-radius:7px;
        padding:9px 11px;
        font-size:10px;
        font-weight:950;
        margin:5px 0 7px 0;
        letter-spacing:.15px;
        box-shadow:0 1px 4px rgba(7,81,139,.12);
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
    width: calc(100% + 20px);
    margin-left: -10px;
    margin-right: -10px;
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

                EXECUTIVE 

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
# MOVE DEPARTMENT SECTION UP
# ============================================================

st.markdown("""
<style>

/* Move ONLY the department selector upward.
   Do NOT move or resize the header. */
div[data-testid="stSelectbox"] {
    margin-top: -55px !important;
}

/* Keep department label close to selector */
div[data-testid="stSelectbox"] label {
    margin-top: 0px !important;
    padding-top: 0px !important;
}

/* Remove extra spacing inside selector */
div[data-testid="stSelectbox"] > div {
    margin-top: 0px !important;
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

    # ALL DEPARTMENTS = no filtering
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
# COMMON DEPARTMENT SELECTOR

# ============================================================
# EXECUTIVE DASHBOARD — MANAGEMENT VIEW
# ============================================================

st.markdown("""
<style>
/* ---------- EXECUTIVE THEME ---------- */
.exec-strip{
    display:flex; justify-content:space-between; align-items:center;
    padding:8px 14px; margin:0 0 8px 0;
    background:linear-gradient(90deg,#06233d,#0a4d7c);
    border-radius:8px; color:#fff;
    box-shadow:0 3px 10px rgba(0,45,80,.12);
}
.exec-strip .title{font-size:15px;font-weight:900;letter-spacing:.4px}
.exec-strip .sub{font-size:9px;opacity:.82;margin-top:2px}
.exec-strip .badge{
    background:#f28c00;color:#fff;padding:5px 10px;border-radius:20px;
    font-size:9px;font-weight:900;letter-spacing:.5px;
}
.exec-kpi{
    width:100% !important;
    height:138px !important;
    min-height:100px !important;
    max-height:100px !important;
    box-sizing:border-box !important;
    background:#fff;border:1px solid #d6e3ed;border-radius:10px;
    padding:12px 12px 10px 12px;
    box-shadow:0 3px 12px rgba(15,60,90,.07);
    position:relative; overflow:hidden;
    display:flex; flex-direction:column; justify-content:flex-start;
}
.exec-kpi:before{
    content:""; position:absolute; left:0; top:0; bottom:0; width:4px;
    background:#0b5b8e;
}
.exec-kpi.orange:before{background:#f28c00}
.exec-kpi.red:before{background:#d71920}
.exec-kpi.green:before{background:#2e9d50}
.exec-kpi .label{font-size:9px;font-weight:900;color:#607588;letter-spacing:.5px}
.exec-kpi .value{font-size:27px;font-weight:950;color:#123f77;line-height:1.05;margin-top:6px}
.exec-kpi .hint{font-size:8px;color:#8797a5;margin-top:5px}
.exec-panel-title{
    display:flex;align-items:center;justify-content:space-between;
    color:#0b4a82;font-size:12px;font-weight:950;
    background:#f7fbfe;
    border:1px solid #d6e3ed;
    border-radius:8px;
    padding:8px 10px;
    margin:0 0 8px 0;
    box-sizing:border-box;
    width:100%;
    letter-spacing:.15px;
}
.exec-panel-title:before{
    content:"";
    width:10px;height:10px;border-radius:50%;
    background:linear-gradient(135deg,#ef5360,#b91f3b);
    margin-right:7px;
    flex:0 0 10px;
    box-shadow:0 1px 3px rgba(185,31,59,.22);
}
.exec-panel-title > div{flex:1}
.exec-panel-title span{font-size:8px;color:#7c8f9f;font-weight:800}
.exec-health{
    padding:8px 10px;border-radius:8px;background:#f5f9fc;
    border:1px solid #dce7ef;margin-bottom:6px;
}
.exec-health .name{font-size:9px;font-weight:900;color:#173f70}
.exec-health .pct{font-size:11px;font-weight:950;color:#173f70}
.exec-bar{height:8px;background:#e5edf3;border-radius:8px;overflow:hidden;margin-top:5px}
.exec-bar > div{height:100%;border-radius:8px}
.exec-note{
    font-size:8px;color:#728494;margin-top:3px;
}
div[data-testid="stVerticalBlockBorderWrapper"]{
    background:linear-gradient(180deg,#f8fcff 0%,#f3f9fd 100%) !important;
    border:1px solid #cbddea !important;
    border-radius:12px !important;
    box-shadow:0 2px 10px rgba(25,70,100,.05) !important;
    padding:10px 10px 8px 10px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div{
    padding:0 !important;
}

/* ---------- STRICT 50:50 EXECUTIVE GRID ---------- */
/* Every two-panel row uses exactly equal column widths and equal outer margins. */
div[data-testid="stHorizontalBlock"]{
    width:100% !important;
    display:flex !important;
    align-items:stretch !important;
    gap:10px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]{
    flex:1 1 0 !important;
    width:0 !important;
    max-width:none !important;
    min-width:0 !important;
    display:flex !important;
    align-items:stretch !important;
}

/* ---------- EQUAL KPI CARD DIMENSIONS ---------- */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.exec-kpi){
    flex:1 1 0 !important;
    width:0 !important;
    min-width:0 !important;
    max-width:none !important;
}
div[data-testid="stHorizontalBlock"]:has(.exec-kpi){
    align-items:stretch !important;
    gap:10px !important;
}
div[data-testid="stHorizontalBlock"]:has(.exec-kpi) > div[data-testid="column"] > div{
    width:100% !important;
    height:138px !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div{
    width:100% !important;
    min-width:0 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] div[data-testid="stVerticalBlockBorderWrapper"]{
    width:100% !important;
    height:100% !important;
    min-height:0 !important;
    box-sizing:border-box !important;
}

/* Header stays inside its own 50:50 panel with equal left/right inset. */
.exec-panel-title{
    box-sizing:border-box !important;
    width:100% !important;
    margin-left:0 !important;
    margin-right:0 !important;
}

/* Do not let Plotly/dataframe elements create horizontal overflow. */
div[data-testid="stHorizontalBlock"] .stPlotlyChart,
div[data-testid="stHorizontalBlock"] [data-testid="stDataFrame"]{
    width:100% !important;
    max-width:100% !important;
}


/* Keep the management-attention chart compact so the panel height is driven by content. */
.exec-management-chart .stPlotlyChart{
    margin-bottom:0 !important;
}

div[data-testid="stSelectbox"] label{
    font-size:9px !important;font-weight:900 !important;color:#173f70 !important;
}
div[data-testid="stSelectbox"] > div > div{
    min-height:32px !important;border-radius:7px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# EXECUTIVE DEPARTMENT LIST
# ============================================================
ALL_DEPARTMENTS = [
    "All Departments",
    "Blast Furnace",
    "Coke Oven",
    "CRM",
    "WRM",
    "CPP",
    "Central Utility",
    "DRI",
    "LCP",
    "Pellet and Beneficiation",
    "Sinter",
    "SMS-1",
    "SMS-2",
    "Tube Mill",
    "CSP",
]

# ---------- DATA FILTER ----------
selected_department = st.selectbox(
    "VIEW DEPARTMENT",
    ALL_DEPARTMENTS,
    index=0,
    key="executive_department_selector",
)

# Keep the executive page independent from the detailed page's filtered objects.
exec_data = {}
for name, df in loaded.items():
    if name in {"PSM CE ", "Barrier Audit", "Failure Data", "Audit Compliance"}:
        exec_data[name] = df.copy() if df is not None else pd.DataFrame()
    else:
        exec_data[name] = filter_selected_department(df, selected_department)

def exec_df(name):
    df = exec_data.get(name)
    return clean_dataframe(df) if df is not None else pd.DataFrame()

def exec_num(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False),
        errors="coerce"
    ).fillna(0)

def module_summary(df, status_names=None):
    x = status_counts(df, status_names)
    total = x["total"]
    done = x["completed"] + x["closed"]
    open_count = x["open"] + x["ongoing"] + x["pending"]
    overdue = x["overdue"]
    pct = (done / total * 100) if total else 0
    return total, done, open_count, overdue, pct

def kpi_card(label, value, hint="", tone="blue"):
    st.markdown(
        f"""<div class="exec-kpi {tone}">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="hint">{hint}</div>
        </div>""",
        unsafe_allow_html=True,
    )

def panel_title(title, subtitle=""):
    st.markdown(
        f"""<div class="exec-panel-title">
            <div>{title}</div><span>{subtitle}</span>
        </div>""",
        unsafe_allow_html=True,
    )

def pct_color(p):
    """Completion percentage colour scale for the Executive dashboard."""
    try:
        p = float(p)
    except Exception:
        p = 0.0

    if p >= 90:
        return "#16a34a"      # Green      90-100%
    elif p >= 70:
        return "#65a30d"      # Lime Green 70-89%
    elif p >= 50:
        return "#f59e0b"      # Amber      50-69%
    elif p >= 25:
        return "#f97316"      # Orange     25-49%
    else:
        return "#dc2626"      # Red        0-24%


def attention_color(value):
    """Management attention colour scale based on number of items."""
    try:
        value = float(value)
    except Exception:
        value = 0.0

    if value >= 50:
        return "#dc2626"      # Critical: 50+
    elif value >= 20:
        return "#f97316"      # High: 20-49
    elif value >= 5:
        return "#facc15"      # Medium: 5-19
    elif value >= 1:
        return "#16a34a"      # Low: 1-4
    else:
        return "#9ca3af"      # None: 0

# ---------- EXECUTIVE KPI CALCULATIONS ----------
pt_df = exec_df("PT")
pha_df = exec_df("PHA")
rec_df = exec_df("PHA Recommendation")
moc_df = exec_df("MOC")
pssr_df = exec_df("PSSR")
training_df = exec_df("Training")
soc_df = exec_df("SOC-SOL")
incident_df = exec_df("PS Incident")
interlock_df = exec_df("Interlock ")
psmce_df = exec_df("PSM CE ")
barrier_df = exec_df("Barrier Audit")
failure_df = exec_df("Failure Data")
audit_df = exec_df("Audit Compliance")

# Action-based modules
action_modules = [
    (pt_df, None), (pha_df, None), (rec_df, [
        "Status (Open/Close)", "Status Open Close", "Open/Close Status",
        "Recommendation Status", "Status"
    ]), (moc_df, None), (pssr_df, [
        "Overdue/Pending/Completed", "Overdue / Pending / Completed",
        "Overdue Pending Completed", "Status", "Current Status"
    ])
]
total_actions = done_actions = open_actions = overdue_actions = 0
for df, candidates in action_modules:
    a,b,c,d,_ = module_summary(df, candidates)
    total_actions += a
    done_actions += b
    open_actions += c
    overdue_actions += d

# Incident KPIs
incident_dept_col = incident_df.columns[1] if len(incident_df.columns) >= 2 else find_col(
    incident_df, ["Department", "Dept"]
)
total_incidents = 0
if incident_dept_col and not incident_df.empty:
    vals = incident_df[incident_dept_col].fillna("").astype(str).str.strip()
    total_incidents = int(vals.replace(["", "-", "nan", "None"], pd.NA).notna().sum())

# Interlock pending
int_status_col = find_col(interlock_df, [
    "Present Status / Action Required", "Present Status",
    "Status / Action Required", "Status"
])
pending_interlocks = 0
if int_status_col and not interlock_df.empty:
    s = interlock_df[int_status_col].fillna("").astype(str).str.lower()
    pending_interlocks = int(
        s.str.contains(r"due\s*for\s*normalization|normalization\s*pending", regex=True, na=False).sum()
    )

# Barrier health
barrier_assessed_col = find_col(barrier_df, [
    "Barrier Health (C4/C5) (Number) Assessed", "Assessed"
])
barrier_unacceptable_col = find_col(barrier_df, [
    "Barrier Health (C4/C5) (Number) Unacceptable",
    "Unacceptable Barrier", "Unacceptable"
])
barrier_assessed = int(exec_num(barrier_df[barrier_assessed_col]).sum()) if barrier_assessed_col and not barrier_df.empty else 0
barr_unacceptable = int(exec_num(barrier_df[barrier_unacceptable_col]).sum()) if barrier_unacceptable_col and not barrier_df.empty else 0

# Audit
audit_date_col = find_col(audit_df, ["Audit Date", "Last Audit Date", "Date"])
audit_done = 0
audit_pending = 0
if audit_date_col and not audit_df.empty:
    audit_dates = pd.to_datetime(audit_df[audit_date_col], errors="coerce")
    audit_done = int(audit_dates.notna().sum())
    audit_pending = int(audit_dates.isna().sum())
elif not audit_df.empty:
    audit_pending = len(audit_df)

# Training completion
training_completion = 0.0
tr_process_col = find_col(training_df, ["Process"])
tr_total_cols = [
    find_col(training_df, ["Total Employees (L08 & Above)"]),
    find_col(training_df, ["Total Employees (Below L08)"]),

]
tr_done_cols = [
    find_col(training_df, ["Completed Training (L08 & Above)"]),
    find_col(training_df, ["Completed Training (Below L08)"]),

]
if not training_df.empty and all(tr_total_cols) and all(tr_done_cols):
    total_people = sum(exec_num(training_df[c]).sum() for c in tr_total_cols)
    done_people = sum(exec_num(training_df[c]).sum() for c in tr_done_cols)
    training_completion = (done_people / total_people * 100) if total_people else 0

# PSM CE completion
psmce_dept_col = find_col(psmce_df, ["Department", "Dept"])
mech_gen = find_col(psmce_df, [
    "Compliance of PSM CE MO – Mechanical – Generated",
    "Compliance of PSM CE MO - Mechanical - Generated",
    "PSM CE MO Mechanical Generated"
])
mech_comp = find_col(psmce_df, [
    "Compliance of PSM CE MO – Mechanical – Completed",
    "Compliance of PSM CE MO - Mechanical - Completed",
    "PSM CE MO Mechanical Completed"
])
ei_gen = find_col(psmce_df, [
    "Compliance of PSM CE MO – E&I – Generated",
    "Compliance of PSM CE MO - E&I - Generated",
    "PSM CE MO E&I Generated"
])
ei_comp = find_col(psmce_df, [
    "Compliance of PSM CE MO – E&I – Completed",
    "Compliance of PSM CE MO - E&I - Completed",
    "PSM CE MO E&I Completed"
])
psmce_gen = (int(exec_num(psmce_df[mech_gen]).sum()) if mech_gen else 0) + (int(exec_num(psmce_df[ei_gen]).sum()) if ei_gen else 0)
psmce_done = (int(exec_num(psmce_df[mech_comp]).sum()) if mech_comp else 0) + (int(exec_num(psmce_df[ei_comp]).sum()) if ei_comp else 0)
psmce_completion = (psmce_done / psmce_gen * 100) if psmce_gen else 0

# Overall action closure — deliberately based only on action-oriented modules in this source.
overall_closure = (done_actions / total_actions * 100) if total_actions else 0

# ---------- KPI ROW ----------
k1,k2,k3,k4,k5,k6,k7,k8 = st.columns(8, gap="small")
with k1: kpi_card("ACTION REGISTER", f"{total_actions:,}", "PT + PHA + PHA Rec. + MOC + PSSR")
with k2: kpi_card("CLOSED / COMPLETE", f"{done_actions:,}", f"{overall_closure:.0f}% closure", "green")
with k3: kpi_card("OPEN / ONGOING", f"{open_actions:,}", "Requires management follow-up", "orange")
with k4: kpi_card("OVERDUE", f"{overdue_actions:,}", "Priority attention", "red")
with k5: kpi_card("PROCESS INCIDENTS", f"{total_incidents:,}", "Recorded process-safety incidents", "red")
with k6: kpi_card("INTERLOCK PENDING", f"{pending_interlocks:,}", "Normalization pending", "orange")
with k7: kpi_card("BARR. UNACCEPT", f"{barr_unacceptable:,}", f"{barrier_assessed:,} assessed", "red")
with k8: kpi_card("AUDIT PENDING", f"{audit_pending:,}", f"{audit_done:,} completed", "orange")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ---------- ROW: PERFORMANCE + MANAGEMENT ATTENTION ----------
left, right = st.columns([1, 1], gap="small")

with left:
    with st.container(border=True):
        panel_title("PSM MODULE PERFORMANCE", "completion / closure view")
        module_rows = [
            ("Process Technology", pt_df, None),
            ("Process Hazard Analysis", pha_df, None),
            ("PHA Recommendation", rec_df, [
                "Status (Open/Close)", "Status Open Close", "Open/Close Status",
                "Recommendation Status", "Status"
            ]),
            ("Management of Change", moc_df, None),
            ("PSSR", pssr_df, [
                "Overdue/Pending/Completed", "Overdue / Pending / Completed",
                "Overdue Pending Completed", "Status", "Current Status"
            ]),
            ("Training", None, None),
            ("PSM CE", None, None),
            ("Audit / Compliance", None, None),
        ]

        perf = []
        for name, df, cand in module_rows:
            if name == "Training":
                p = training_completion
                total = None
            elif name == "PSM CE":
                p = psmce_completion
                total = psmce_gen
            elif name == "Audit / Compliance":
                total = audit_done + audit_pending
                p = (audit_done / total * 100) if total else 0
            else:
                total, done, _, _, p = module_summary(df, cand)
            perf.append((name, p, total))

        for name, p, total in perf:
            c = pct_color(p)
            total_text = f"{total:,} records" if total is not None else ""
            st.markdown(
                f"""<div class="exec-health">
                    <div style="display:flex;justify-content:space-between;">
                        <div class="name">{name}</div>
                        <div class="pct" style="color:{c};">{p:.0f}%</div>
                    </div>
                    <div class="exec-bar"><div style="width:{min(100,max(0,p)):.1f}%;background:{c};"></div></div>
                    <div class="exec-note">{total_text}</div>
                </div>""",
                unsafe_allow_html=True,
            )

with right:
    with st.container(border=True, height=605):
        panel_title("MANAGEMENT ATTENTION", "items needing action")

        attention = pd.DataFrame({
            "Area": [
                "Overdue actions",
                "Open / ongoing actions",
                "Process safety incidents",
                "Interlock normalization",
                "Unacceptable barriers",
                "Pending audits",
            ],
            "Count": [
                overdue_actions,
                open_actions,
                total_incidents,
                pending_interlocks,
                barr_unacceptable,
                audit_pending,
            ],
        }).sort_values("Count", ascending=True)

        fig = go.Figure(go.Bar(
            x=attention["Count"],
            y=attention["Area"],
            orientation="h",
            text=attention["Count"],
            textposition="outside",
            marker=dict(color=[attention_color(v) for v in attention["Count"]]),
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        ))
        fig.update_layout(
            height=400,
            margin=dict(l=8,r=45,t=8,b=18),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=9,color="#173f70"),
            xaxis=dict(showgrid=True,gridcolor="#e5edf4",rangemode="tozero"),
            yaxis=dict(showgrid=False),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown(
            '<div class="exec-note">Higher bars indicate greater management attention; values are calculated from the live source registers.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:5px;
                        font-size:8px;font-weight:800;color:#627689;">
                <span><b style="color:#dc2626;">●</b> Critical (≥50)</span>
                <span><b style="color:#f97316;">●</b> High (20–49)</span>
                <span><b style="color:#facc15;">●</b> Medium (5–19)</span>
                <span><b style="color:#16a34a;">●</b> Low (1–4)</span>
                <span><b style="color:#9ca3af;">●</b> None (0)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- ROW: DEPARTMENT RISK / PERFORMANCE ----------
c1, c2 = st.columns([1, 1], gap="small")

with c1:
    with st.container(border=True, height=340):
        panel_title("DEPARTMENT-WISE SAFETY SIGNAL", "incident + interlock + barrier")

        dept_names = [d for d in ALL_DEPARTMENTS if d != "All Departments"]
        dept_rows = []
        for dept in dept_names:
            inc = len(filter_selected_department(loaded.get("PS Incident"), dept))
            inte = len(filter_selected_department(loaded.get("Interlock "), dept))
            # Barrier source may have its own department column.
            barr = filter_selected_department(loaded.get("Barrier Audit"), dept)
            bu = 0
            if not barr.empty and barrier_unacceptable_col:
                bu = int(exec_num(barr[barrier_unacceptable_col]).sum())
            dept_rows.append([dept, inc, inte, bu, inc + inte + bu])

        dept_df = pd.DataFrame(dept_rows, columns=["Department","Incidents","Interlocks","Unacceptable Barriers","Attention"])
        dept_df = dept_df.sort_values(["Attention","Department"], ascending=[False,True]).head(12)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Incidents", x=dept_df["Department"], y=dept_df["Incidents"]))
        fig.add_trace(go.Bar(name="Interlocks", x=dept_df["Department"], y=dept_df["Interlocks"]))
        fig.add_trace(go.Bar(name="Unacceptable Barriers", x=dept_df["Department"], y=dept_df["Unacceptable Barriers"]))
        fig.update_layout(
            barmode="stack", height=250,
            margin=dict(l=35,r=15,t=10,b=90),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=8,color="#173f70"),
            legend=dict(orientation="h",y=1.08,x=0,font=dict(size=8)),
            xaxis=dict(tickangle=-45,showgrid=False),
            yaxis=dict(rangemode="tozero",showgrid=True,gridcolor="#e5edf4"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

with c2:
    with st.container(border=True):
        panel_title("EXECUTIVE HEALTH GAUGES", "key compliance indicators")

        gauges = [
            ("Action Closure", overall_closure),
            ("Training Completion", training_completion),
            ("PSM CE Completion", psmce_completion),
        ]
        for name, val in gauges:
            c = pct_color(val)
            fig = go.Figure(go.Pie(
                values=[min(100,max(0,val)), max(0,100-min(100,max(0,val)))],
                labels=["Complete","Remaining"],
                hole=.72,
                textinfo="none",
                marker=dict(colors=[c,"#e9eff4"]),
                sort=False,
            ))
            fig.update_layout(
                height=78, margin=dict(l=0,r=0,t=0,b=0),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                annotations=[dict(text=f"<b>{val:.0f}%</b>",x=.5,y=.5,
                                   showarrow=False,font=dict(size=18,color="#173f70"))],
            )
            gc1,gc2 = st.columns([.55,1.45], gap="small")
            with gc1:
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False},
                    key=f"executive_health_gauge_{name}"
                )
            with gc2:
                st.markdown(
                    f"""<div style="padding-top:12px">
                        <div style="font-size:10px;font-weight:900;color:#173f70">{name}</div>
                        <div style="font-size:8px;color:#7b8d9b;margin-top:4px">
                        {"Target / healthy level: 90%+" if name != "Action Closure" else "Based on action-oriented modules in the source data"}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

# ---------- ROW: TREND + CRITICAL REGISTERS ----------
t1, t2 = st.columns([1, 1], gap="small")

with t1:
    with st.container(border=True, height=375):
        panel_title("SOC / SOL DEVIATION TREND", "month-wise")

        if not soc_df.empty:
            month_col = find_col(soc_df, ["Month"])
            soc_col = find_col(soc_df, ["SOC Deviation","SOC Deviation Nos.","SOC Deviation No.","SOC"])
            sol_col = find_col(soc_df, ["SOL Deviation","SOL Deviation Nos.","SOL Deviation No.","SOL"])
            if month_col and soc_col and sol_col:
                temp = pd.DataFrame({
                    "Month": soc_df[month_col].astype(str).str.strip(),
                    "SOC": exec_num(soc_df[soc_col]),
                    "SOL": exec_num(soc_df[sol_col]),
                })
                temp = temp.groupby("Month", as_index=False)[["SOC","SOL"]].sum()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=temp["Month"],y=temp["SOC"],mode="lines+markers+text",
                                         text=[str(int(v)) if v else "" for v in temp["SOC"]],
                                         textposition="top center",name="SOC Deviation",line=dict(width=3)))
                fig.add_trace(go.Scatter(x=temp["Month"],y=temp["SOL"],mode="lines+markers+text",
                                         text=[str(int(v)) if v else "" for v in temp["SOL"]],
                                         textposition="top center",name="SOL Deviation",line=dict(width=3)))
                fig.update_layout(
                    height=250, margin=dict(l=40,r=20,t=10,b=50),
                    plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=8,color="#173f70"),
                    xaxis=dict(showgrid=False,tickangle=-35),
                    yaxis=dict(rangemode="tozero",showgrid=True,gridcolor="#e5edf4"),
                    legend=dict(orientation="h",y=1.08,x=0,font=dict(size=8)),
                    hovermode="x unified",
                )
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            else:
                st.info("SOC / SOL columns not available.")
        else:
            st.info("No SOC / SOL data available.")

with t2:
    with st.container(border=True):
        panel_title("CRITICAL OPEN REGISTERS", "top priorities")

        critical_rows = []
        if not pssr_df.empty:
            x = status_counts(pssr_df, [
                "Overdue/Pending/Completed","Overdue / Pending / Completed",
                "Overdue Pending Completed","Status","Current Status"
            ])
            critical_rows.append(("PSSR overdue", x["overdue"]))
            critical_rows.append(("PSSR pending", x["pending"]))
        if not rec_df.empty:
            x = status_counts(rec_df, [
                "Status (Open/Close)","Status Open Close","Open/Close Status",
                "Recommendation Status","Status"
            ])
            critical_rows.append(("PHA recommendations open", x["open"]))
        if not moc_df.empty:
            x = status_counts(moc_df)
            critical_rows.append(("MOC open", x["open"]))
        critical_rows.extend([
            ("Interlock normalization pending", pending_interlocks),
            ("Unacceptable barriers", barr_unacceptable),
            ("Audit pending", audit_pending),
        ])

        critical_df = pd.DataFrame(critical_rows, columns=["Register","Open"]).sort_values("Open",ascending=False)
        critical_df = critical_df[critical_df["Open"] > 0].head(8)

        if critical_df.empty:
            st.success("No critical open register items detected.")
        else:
            st.dataframe(
                critical_df,
                use_container_width=True,
                hide_index=True,
                height=300,
                column_config={
                    "Register": st.column_config.TextColumn("Register"),
                    "Open": st.column_config.NumberColumn("Open",format="%d"),
                }
            )

# ============================================================
# TWO-COLUMN EXECUTIVE VIEW
# ============================================================

left_section, right_section = st.columns(
    [1, 1],
    gap="small"
)

with left_section:

    # ============================================================
    # PSM LEADING vs LAGGING INDICATORS MATRIX
    # ============================================================
    # This section is self-contained. It uses the existing executive
    # data/filter logic above and does not replace any existing dashboard section.
    # ============================================================

    st.markdown("""
    <style>
    .psm-matrix-wrap{
        background:#ffffff;
        border:1px solid #cbdce8;
        border-radius:10px;
        padding:10px 10px 8px 10px;
        margin:8px 0 4px 0;
        box-shadow:0 2px 8px rgba(15,60,90,.06);
    }
    .psm-matrix-head{
        display:flex;
        align-items:center;
        justify-content:space-between;
        background:linear-gradient(90deg,#073f78,#0b6096);
        color:#ffffff;
        border-radius:7px;
        padding:9px 12px;
        margin-bottom:8px;
        font-size:12px;
        font-weight:950;
        letter-spacing:.2px;
    }
    .psm-matrix-sub{
        color:#5f7385;
        font-size:9px;
        margin:3px 2px 8px 2px;
    }
    .psm-matrix-link{
        display:inline-block;
        background:#073f78;
        color:#ffffff !important;
        padding:6px 10px;
        border-radius:5px;
        text-decoration:none !important;
        font-size:9px;
        font-weight:900;
    }
    .psm-matrix-table{
        width:100%;
        border-collapse:collapse;
        table-layout:fixed;
        font-size:9px;
        color:#173f70;
    }
    .psm-matrix-table th{
        background:#dcecf3;
        color:#173f70;
        font-weight:950;
        text-align:left;
        padding:7px 6px;
        border:1px solid #b7c8d3;
    }
    .psm-matrix-table td{
        background:#ffffff;
        padding:6px;
        border:1px solid #d3dee6;
        vertical-align:middle;
    }
    .psm-matrix-table th:nth-child(1),
    .psm-matrix-table td:nth-child(1){width:5%;text-align:center;}
    .psm-matrix-table th:nth-child(2),
    .psm-matrix-table td:nth-child(2){width:34%;}
    .psm-matrix-table th:nth-child(3),
    .psm-matrix-table td:nth-child(3){width:12%;}
    .psm-matrix-table th:nth-child(4),
    .psm-matrix-table td:nth-child(4){width:13%;}
    .psm-matrix-table th:nth-child(5),
    .psm-matrix-table td:nth-child(5){width:16%;}
    .psm-matrix-table th:nth-child(6),
    .psm-matrix-table td:nth-child(6){width:20%;}
    .matrix-ok{color:#159447;font-weight:900;}
    .matrix-watch{color:#e5a400;font-weight:900;}
    .matrix-critical{color:#d71920;font-weight:900;}
    .matrix-na{color:#8a99a8;font-weight:800;}
    .matrix-note{
        font-size:8px;
        color:#738595;
        margin-top:6px;
    }
    </style>
    """, unsafe_allow_html=True)


    def _matrix_status_pct(df, status_names=None):
        """Closure percentage from the existing status logic."""
        if df is None or df.empty:
            return None
        total, done, _, _, pct = module_summary(df, status_names)
        return pct if total else None


    def _matrix_status_count(df, candidates):
        """Count rows matching active/open/pending wording in a status field."""
        if df is None or df.empty:
            return None
        status_col = find_col(df, candidates)
        if not status_col:
            return None
        s = df[status_col].fillna("").astype(str).str.strip().str.lower()
        valid = s.replace({"nan": "", "none": "", "-": ""})
        valid = valid[valid != ""]
        if valid.empty:
            return 0
        return int(
            valid.str.contains(
                r"active|bypass|due\s*for\s*normalization|normalization\s*pending|pending|open",
                regex=True,
                na=False,
            ).sum()
        )


    def _matrix_yes_count(df, candidates):
        """Count affirmative records from a source column."""
        if df is None or df.empty:
            return None
        col = find_col(df, candidates)
        if not col:
            return None

        s = df[col].fillna("").astype(str).str.strip().str.lower()
        return int(
            s.str.fullmatch(
                r"yes|y|true|1|active|occurred|applicable|non[- ]?compliant",
                case=False,
                na=False,
            ).sum()
        )


    def _matrix_zero_or_pct(actual, target_type="zero"):
        """Return status for zero-target count KPIs or percentage KPIs."""
        if actual is None:
            return "N/A", "matrix-na"
        if target_type == "zero":
            return ("ON TRACK", "matrix-ok") if float(actual) == 0 else ("CRITICAL", "matrix-critical")
        if float(actual) >= 95:
            return "ON TRACK", "matrix-ok"
        if float(actual) >= 80:
            return "WATCH", "matrix-watch"
        return "CRITICAL", "matrix-critical"


    # Use the same selected-department filter for every matrix source.
    # This avoids showing fixed All-Department values when the executive filter changes.
    matrix_pt = filter_selected_department(pt, selected_department)
    matrix_pha = filter_selected_department(pha, selected_department)
    matrix_rec = filter_selected_department(rec, selected_department)
    matrix_moc = filter_selected_department(moc, selected_department)
    matrix_pssr = filter_selected_department(pssr, selected_department)
    matrix_training = filter_selected_department(training, selected_department)
    matrix_incident = filter_selected_department(incident, selected_department)
    matrix_interlock = filter_selected_department(interlock, selected_department)
    matrix_barrier = filter_selected_department(loaded.get("Barrier Audit"), selected_department)
    matrix_failure = filter_selected_department(failure_data, selected_department)
    matrix_audit = filter_selected_department(audit, selected_department)


    # ---- 1. PHA recommendation closure ----
    pha_rec_actual = _matrix_status_pct(
        matrix_rec,
        [
            "Status (Open/Close)",
            "Status Open Close",
            "Open/Close Status",
            "Recommendation Status",
            "Status",
        ],
    )

    # ---- 2. MOC closure compliance ----
    moc_actual = _matrix_status_pct(
        matrix_moc,
        [
            "Status (Open/Close)",
            "Status (Open / Close)",
            "Status",
            "Current Status",
            "MOC Status",
        ],
    )

    # ---- 3. Interlock bypass active count ----
    interlock_active = _matrix_status_count(
        matrix_interlock,
        [
            "Present Status / Action Required",
            "Present Status",
            "Status / Action Required",
            "Status",
        ],
    )

    # ---- 4. Alarm bypass active count ----
    # The current executive source does not load the Alarm tab, so do not
    # substitute Interlock data. Show N/A unless an Alarm field exists.
    alarm_active = None

    # ---- 5. Bow-Tie barrier verification ----
    barrier_assessed_col_m = find_col(
        matrix_barrier,
        ["Barrier Health (C4/C5) (Number) Assessed", "Assessed"]
    )
    barrier_unacceptable_col_m = find_col(
        matrix_barrier,
        [
            "Barrier Health (C4/C5) (Number) Unacceptable",
            "Unacceptable Barrier",
            "Unacceptable",
        ]
    )
    if barrier_assessed_col_m and barrier_unacceptable_col_m and not matrix_barrier.empty:
        assessed_m = float(exec_num(matrix_barrier[barrier_assessed_col_m]).sum())
        unacceptable_m = float(exec_num(matrix_barrier[barrier_unacceptable_col_m]).sum())
        barrier_actual = ((assessed_m - unacceptable_m) / assessed_m * 100) if assessed_m else None
    else:
        barrier_actual = None

    # ---- 6. PSM training completion ----
    training_actual = None
    if not matrix_training.empty:
        tr_total_cols_m = [
            find_col(matrix_training, ["Total Employees (L08 & Above)"]),
            find_col(matrix_training, ["Total Employees (Below L08)"]),

        ]
        tr_done_cols_m = [
            find_col(matrix_training, ["Completed Training (L08 & Above)"]),
            find_col(matrix_training, ["Completed Training (Below L08)"]),

        ]
        if all(tr_total_cols_m) and all(tr_done_cols_m):
            total_people_m = sum(float(exec_num(matrix_training[c]).sum()) for c in tr_total_cols_m)
            done_people_m = sum(float(exec_num(matrix_training[c]).sum()) for c in tr_done_cols_m)
            training_actual = (done_people_m / total_people_m * 100) if total_people_m else None

    # ---- 7. PSM audit observation closure ----
    audit_actual = None
    if not matrix_audit.empty:
        audit_status_col_m = find_col(
            matrix_audit,
            [
                "Status",
                "Observation Status",
                "Action Status",
                "Closure Status",
                "Compliance Status",
            ],
        )
        if audit_status_col_m:
            audit_actual = _matrix_status_pct(
                matrix_audit,
                ["Status", "Observation Status", "Action Status", "Closure Status", "Compliance Status"],
            )
        else:
            # Fall back to the same audit-date logic already used above.
            audit_date_col_m = find_col(matrix_audit, ["Audit Date", "Last Audit Date", "Date"])
            if audit_date_col_m:
                dates_m = pd.to_datetime(matrix_audit[audit_date_col_m], errors="coerce")
                audit_actual = (dates_m.notna().sum() / len(matrix_audit) * 100) if len(matrix_audit) else None

    # ---- 8. Process Safety Incidents ----
    incident_actual = len(matrix_incident) if matrix_incident is not None and not matrix_incident.empty else 0

    # ---- 9. Major equipment failure events ----
    failure_actual = len(matrix_failure) if matrix_failure is not None and not matrix_failure.empty else 0

    # ---- 10–14: derive only where the incident source has an explicit field ----
    def _incident_event_count(df, candidates):
        if df is None or df.empty:
            return None
        col = find_col(df, candidates)
        if not col:
            return None

        s = df[col].fillna("").astype(str).str.strip().str.lower()

        # Numeric event-count fields
        numeric = pd.to_numeric(s.str.replace(",", "", regex=False), errors="coerce")
        if numeric.notna().any():
            return int(numeric.fillna(0).sum())

        return int(
            s.str.fullmatch(
                r"yes|y|true|1|occurred|applicable",
                case=False,
                na=False,
            ).sum()
        )


    loss_containment_actual = _incident_event_count(
        matrix_incident,
        [
            "Loss of Containment",
            "Loss of containment event",
            "LOC",
            "Containment Loss",
        ],
    )

    fire_explosion_actual = _incident_event_count(
        matrix_incident,
        [
            "Fire / Explosion",
            "Fire/Explosion",
            "Fire Explosion",
            "Fire",
            "Explosion",
        ],
    )

    environmental_actual = _incident_event_count(
        matrix_incident,
        [
            "Environmental Release",
            "Environmental release event",
            "Environment Release",
            "Release to Environment",
        ],
    )

    repeat_incident_actual = _incident_event_count(
        matrix_incident,
        [
            "Repeat Incident",
            "Repeat Incidents",
            "Repeat",
        ],
    )

    production_loss_actual = _incident_event_count(
        matrix_incident,
        [
            "Production Loss due to PSM Incident",
            "Production Loss",
            "Production Loss (MT)",
            "Production Loss Due to Incident",
        ],
    )


    matrix_rows = [
        (
            1,
            "PHA recommendation closure",
            ">95%",
            pha_rec_actual,
            "pct",
            "Monthly",
        ),
        (
            2,
            "MOC closure compliance",
            "100%",
            moc_actual,
            "pct",
            "Monthly",
        ),
        (
            3,
            "Interlock bypass active count",
            "0",
            interlock_active,
            "zero",
            "Weekly",
        ),
        (
            4,
            "Alarm bypass active count",
            "0",
            alarm_active,
            "zero",
            "Weekly",
        ),
        (
            5,
            "Bow-Tie barrier verification",
            "100%",
            barrier_actual,
            "pct",
            "Monthly",
        ),
        (
            6,
            "PSM training completion (On Roll employee L08 and above)",
            ">95%",
            training_actual,
            "pct",
            "Monthly",
        ),
        (
            7,
            "PSM audit observation closure",
            ">95%",
            audit_actual,
            "pct",
            "Monthly",
        ),
        (
            8,
            "Process Safety Incidents",
            "0",
            incident_actual,
            "zero",
            "Monthly",
        ),
        (
            9,
            "Major equipment failure events",
            "0",
            failure_actual,
            "zero",
            "Monthly",
        ),
        (
            10,
            "Loss of containment events",
            "0",
            loss_containment_actual,
            "zero",
            "Monthly",
        ),
        (
            11,
            "Fire / explosion events",
            "0",
            fire_explosion_actual,
            "zero",
            "Monthly",
        ),
        (
            12,
            "Environmental release events",
            "0",
            environmental_actual,
            "zero",
            "Monthly",
        ),
        (
            13,
            "Repeat incidents",
            "0",
            repeat_incident_actual,
            "zero",
            "Monthly",
        ),
        (
            14,
            "Production loss due to PSM incident",
            "0",
            production_loss_actual,
            "zero",
            "Monthly",
        ),
    ]


    def _matrix_display(actual, kind):
        if actual is None:
            return "N/A", "N/A", "matrix-na"

        if kind == "pct":
            status, cls = _matrix_zero_or_pct(actual, "pct")
            return f"{actual:.1f}%", status, cls

        status, cls = _matrix_zero_or_pct(actual, "zero")
        if isinstance(actual, float) and actual.is_integer():
            actual = int(actual)
        return f"{actual:,}", status, cls


    matrix_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    html, body { margin:0; padding:0; background:transparent; font-family:Arial, Helvetica, sans-serif; }
    .psm-matrix-wrap{background:#ffffff;border:1px solid #cbdce8;border-radius:10px;padding:10px 10px 8px 10px;margin:0;box-shadow:0 2px 8px rgba(15,60,90,.06);box-sizing:border-box;}
    .psm-matrix-head{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#073f78,#0b6096);color:#ffffff;border-radius:7px;padding:9px 12px;margin-bottom:8px;font-size:12px;font-weight:950;letter-spacing:.2px;}
    .psm-matrix-sub{color:#5f7385;font-size:9px;margin:3px 2px 8px 2px;}
    .psm-matrix-table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:9px;color:#173f70;}
    .psm-matrix-table th{background:#dcecf3;color:#173f70;font-weight:950;text-align:left;padding:7px 6px;border:1px solid #b7c8d3;}
    .psm-matrix-table td{background:#ffffff;padding:6px;border:1px solid #d3dee6;vertical-align:middle;}
    .psm-matrix-table th:nth-child(1),.psm-matrix-table td:nth-child(1){width:5%;text-align:center;}
    .psm-matrix-table th:nth-child(2),.psm-matrix-table td:nth-child(2){width:34%;}
    .psm-matrix-table th:nth-child(3),.psm-matrix-table td:nth-child(3){width:12%;}
    .psm-matrix-table th:nth-child(4),.psm-matrix-table td:nth-child(4){width:13%;}
    .psm-matrix-table th:nth-child(5),.psm-matrix-table td:nth-child(5){width:16%;}
    .psm-matrix-table th:nth-child(6),.psm-matrix-table td:nth-child(6){width:20%;}
    .matrix-ok{color:#159447;font-weight:900;}
    .matrix-watch{color:#e5a400;font-weight:900;}
    .matrix-critical{color:#d71920;font-weight:900;}
    .matrix-na{color:#8a99a8;font-weight:800;}
    .matrix-note{font-size:8px;color:#738595;margin-top:6px;}
    </style>
    </head>
    <body>
    <div class="psm-matrix-wrap">
        <div class="psm-matrix-head">
            <span>PSM LEADING vs LAGGING INDICATORS MATRIX</span>
           
        </div>
        <table class="psm-matrix-table">
            <thead>
                <tr>
                    <th>SL NO</th>
                    <th>KPI</th>
                    <th>TARGET</th>
                    <th>ACTUAL</th>
                    <th>STATUS</th>
                    <th>REVIEW FREQUENCY</th>
                </tr>
            </thead>
            <tbody>
    """

    for sno, kpi, target, actual, kind, frequency in matrix_rows:
        actual_text, status_text, status_cls = _matrix_display(actual, kind)
        matrix_html += f"""
                <tr>
                    <td>{sno}</td>
                    <td>{kpi}</td>
                    <td>{target}</td>
                    <td class="{status_cls}"><b>{actual_text}</b></td>
                    <td class="{status_cls}">{status_text}</td>
                    <td>{frequency}</td>
                </tr>
    """

    matrix_html += """
            </tbody>
        </table>
        <div class="matrix-note">
            Actual values follow the Executive Department filter. N/A is shown where the current source
            does not contain a direct field for that KPI; no value is assumed or hard-coded.
        </div>
    </div>
    </body>
    </html>
    """

    matrix_html = matrix_html.replace("__DEPARTMENT__", str(selected_department))

    # Render the matrix as a real HTML document so table tags are not shown as text.
    components.html(
        matrix_html,
        height=500,
        scrolling=False
    )



# ============================================================
# DEPARTMENT-WISE KPI & DATA PERFORMANCE RANKING
# ============================================================
# Ranking is based directly on the 14 KPIs in the approved matrix.
# The matrix provides targets, but does not provide KPI weights.
# Therefore available KPIs are equally weighted.
# Missing source data is N/A and is NOT treated as 100%.
# ============================================================

st.markdown("""
<style>
.psm-rank-wrap{background:#fff;border:1px solid #cbdce8;border-radius:10px;padding:10px;margin:8px 0 10px;box-shadow:0 2px 8px rgba(15,60,90,.06);}
.psm-rank-head{background:linear-gradient(90deg,#073f78,#0b6096);color:#fff;border-radius:7px;padding:10px 12px;font-size:12px;font-weight:950;}
.psm-rank-note{color:#667b8d;font-size:9px;margin:7px 2px;line-height:1.45;}
.psm-rank-table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:10px;color:#173f70;}
.psm-rank-table th{background:#073f78;color:#fff;font-weight:950;padding:8px 6px;border:1px solid #073f78;}
.psm-rank-table td{padding:8px 6px;border:1px solid #d3dee6;background:#fff;text-align:center;}
.psm-rank-table td.dept{text-align:left;font-weight:800;}
.rank-good{color:#159447;font-weight:900}.rank-watch{color:#e5a400;font-weight:900}.rank-critical{color:#d71920;font-weight:900}.rank-na{color:#8a99a8;font-weight:800;}
</style>
""", unsafe_allow_html=True)

# Matrix targets exactly as shown in the supplied matrix.
MATRIX_KPIS = [
    ("PHA recommendation closure", 95.0, "pct"),
    ("MOC closure compliance", 100.0, "pct"),
    ("Interlock bypass active count", 0.0, "zero"),
    ("Alarm bypass active count", 0.0, "zero"),
    ("Bow-Tie barrier verification", 100.0, "pct"),
    ("PSM training completion", 95.0, "pct"),
    ("PSM audit observation closure", 95.0, "pct"),
    ("Process Safety Incidents", 0.0, "zero"),
    ("Major equipment failure events", 0.0, "zero"),
    ("Loss of containment events", 0.0, "zero"),
    ("Fire / explosion events", 0.0, "zero"),
    ("Environmental release events", 0.0, "zero"),
    ("Repeat incidents", 0.0, "zero"),
    ("Production loss due to PSM incident", 0.0, "zero"),
]

def _dept_df(df, dept):
    if df is None:
        return pd.DataFrame()
    return filter_selected_department(df, dept)

def _pct_status(df, candidates):
    if df is None or df.empty:
        return None
    return _matrix_status_pct(df, candidates)

def _active_interlocks(df):
    if df is None or df.empty:
        return None
    col = find_col(df, [
        "Present Status / Action Required", "Present Status",
        "Status / Action Required", "Status"
    ])
    if not col:
        return None
    s = df[col].fillna("").astype(str).str.lower()
    return float(s.str.contains(
        r"active|normalization\s*pending|due\s*for\s*normalization",
        regex=True, na=False
    ).sum())

def _training_actual(df):
    if df is None or df.empty:
        return None

    total_cols = [
        find_col(df, ["Total Employees (L08 & Above)"]),
        find_col(df, ["Total Employees (Below L08)"]),
        find_col(df, ["Total Associates"]),
        find_col(df, ["Total Contractual Workers"]),
    ]
    done_cols = [
        find_col(df, ["Completed Training (L08 & Above)"]),
        find_col(df, ["Completed Training (Below L08)"]),
        find_col(df, ["Completed Training (Associates)"]),
        find_col(df, ["Completed Training (Contracts)"]),
    ]

    if all(total_cols) and all(done_cols):
        total = sum(float(exec_num(df[c]).sum()) for c in total_cols)
        done = sum(float(exec_num(df[c]).sum()) for c in done_cols)
        return done / total * 100 if total else None

    return _pct_status(df, [
        "Status", "Current Status", "Training Status", "Completion Status"
    ])

def _barrier_actual(df):
    if df is None or df.empty:
        return None
    a = find_col(df, ["Barrier Health (C4/C5) (Number) Assessed", "Assessed"])
    u = find_col(df, [
        "Barrier Health (C4/C5) (Number) Unacceptable",
        "Unacceptable Barrier", "Unacceptable"
    ])
    if not a or not u:
        return None
    assessed = float(exec_num(df[a]).sum())
    unacceptable = float(exec_num(df[u]).sum())
    return (assessed - unacceptable) / assessed * 100 if assessed else None

def _event_field_count(df, candidates):
    # None = source/field unavailable; 0 = field exists and confirms zero events.
    if df is None or df.empty:
        return None
    col = find_col(df, candidates)
    if not col:
        return None

    s = df[col].fillna("").astype(str).str.strip()
    numeric = pd.to_numeric(s.str.replace(",", "", regex=False), errors="coerce")
    if numeric.notna().any():
        return float(numeric.fillna(0).sum())

    return float(s.str.lower().isin([
        "yes", "y", "true", "1", "occurred", "applicable"
    ]).sum())

def _matrix_actuals(dept):
    rec_d = _dept_df(rec, dept)
    moc_d = _dept_df(moc, dept)
    interlock_d = _dept_df(interlock, dept)
    training_d = _dept_df(training, dept)
    barrier_d = _dept_df(loaded.get("Barrier Audit"), dept)
    audit_d = _dept_df(audit, dept)
    incident_d = _dept_df(incident, dept)
    failure_d = _dept_df(failure_data, dept)

    # 1 PHA recommendation closure
    v1 = _pct_status(rec_d, [
        "Status (Open/Close)", "Status Open Close", "Open/Close Status",
        "Recommendation Status", "Status"
    ])

    # 2 MOC closure compliance
    v2 = _pct_status(moc_d, [
        "Status (Open/Close)", "Status (Open / Close)", "Status",
        "Current Status", "MOC Status"
    ])

    # 3 Interlock bypass active count
    v3 = _active_interlocks(interlock_d)

    # 4 Alarm bypass active count: no dedicated source field currently loaded
    v4 = None

    # 5 Bow-Tie barrier verification
    v5 = _barrier_actual(barrier_d)

    # 6 PSM training completion
    v6 = _training_actual(training_d)

    # 7 PSM audit observation closure
    v7 = _pct_status(audit_d, [
        "Status", "Observation Status", "Action Status",
        "Closure Status", "Compliance Status"
    ])

    # 8 Process Safety Incidents
    v8 = float(len(incident_d)) if not incident_d.empty else None

    # 9 Major equipment failure events
    v9 = float(len(failure_d)) if not failure_d.empty else None

    # 10-14 use the PS Incident source only if the exact field exists
    v10 = _event_field_count(incident_d, [
        "Loss of Containment", "Loss of containment event", "LOC"
    ])
    v11 = _event_field_count(incident_d, [
        "Fire / Explosion", "Fire/Explosion", "Fire Explosion", "Fire", "Explosion"
    ])
    v12 = _event_field_count(incident_d, [
        "Environmental Release", "Environmental release event",
        "Environment Release"
    ])
    v13 = _event_field_count(incident_d, [
        "Repeat Incident", "Repeat Incidents", "Repeat"
    ])
    v14 = _event_field_count(incident_d, [
        "Production Loss due to PSM Incident",
        "Production Loss", "Production Loss (MT)"
    ])

    return [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14]

def _score(actual, target, kind):
    if actual is None:
        return None
    if kind == "zero":
        return 100.0 if float(actual) == 0 else 0.0
    return max(0.0, min(100.0, float(actual) / target * 100.0))

ranking_departments = (
    ALL_DEPARTMENTS[1:] if selected_department == "All Departments"
    else [selected_department]
)

ranking_rows = []
for dept in ranking_departments:
    actuals = _matrix_actuals(dept)
    scores = [
        _score(actual, target, kind)
        for actual, (_, target, kind) in zip(actuals, MATRIX_KPIS)
    ]
    usable = [s for s in scores if s is not None]
    overall = sum(usable) / len(usable) if usable else None

    ranking_rows.append({
        "Department": dept,
        "Score": overall,
        "KPI Count": len(usable),
    })

ranking_df = pd.DataFrame(ranking_rows)
if not ranking_df.empty:
    ranking_df = ranking_df.sort_values(
        ["Score", "KPI Count"],
        ascending=[False, False],
        na_position="last"
    ).reset_index(drop=True)
    ranking_df["Rank"] = range(1, len(ranking_df) + 1)

with right_section:

    if ranking_df.empty:
        rank_table_html = """<div style="padding:20px;text-align:center;color:#738595;font-size:10px;">No department data available for ranking.</div>"""
    else:
        rank_table_html = """
        <table class="psm-rank-table">
          <thead><tr>
            <th style="width:7%">RANK</th>
            <th style="width:33%;text-align:left">DEPARTMENT</th>
            <th style="width:20%">PSM SCORE</th>
            <th style="width:15%">KPIs USED</th>
            <th style="width:25%">STATUS</th>
          </tr></thead><tbody>
        """

        for _, r in ranking_df.iterrows():
            score = r["Score"]
            if score is None or pd.isna(score):
                score_text, status, cls = "N/A", "NO DATA", "rank-na"
            else:
                score_text = f"{score:.1f}%"
                if score >= 80:
                    status, cls = "ON TRACK", "rank-good"
                elif score >= 60:
                    status, cls = "WATCH", "rank-watch"
                else:
                    status, cls = "CRITICAL", "rank-critical"

            rank_table_html += f"""
            <tr>
              <td><b>{int(r["Rank"])}</b></td>
              <td class="dept">{r["Department"]}</td>
              <td class="{cls}">{score_text}</td>
              <td>{int(r["KPI Count"])} / 14</td>
              <td class="{cls}">{status}</td>
            </tr>
            """

        rank_table_html += "</tbody></table>"

    ranking_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    html, body {{ margin:0; padding:0; background:transparent; font-family:Arial, Helvetica, sans-serif; }}
    .psm-rank-wrap{{
        width:100%;
        height:500px;
        box-sizing:border-box;
        background:#ffffff;
        border:1px solid #cbdce8;
        border-radius:10px;
        padding:10px 10px 8px 10px;
        margin:16px 0 0 0;
        box-shadow:0 2px 8px rgba(15,60,90,.06);
        overflow:hidden;
    }}
    .psm-rank-scroll{{
        height:430px;
        overflow-y:auto;
        overflow-x:hidden;
        box-sizing:border-box;
        padding-right:2px;
    }}
    .psm-rank-scroll::-webkit-scrollbar{{
        width:7px;
    }}
    .psm-rank-scroll::-webkit-scrollbar-track{{
        background:#eef4f8;
        border-radius:6px;
    }}
    .psm-rank-scroll::-webkit-scrollbar-thumb{{
        background:#8fa8bb;
        border-radius:6px;
    }}
    .psm-rank-head{{
        display:flex;
        align-items:center;
        justify-content:space-between;
        box-sizing:border-box;
        width:100%;
        height:30px;
        min-height:30px;
        max-height:30px;
        background:linear-gradient(90deg,#073f78,#0b6096);
        color:#ffffff;
        border-radius:7px;
        padding:9px 12px;
        margin:0 0 8px 0;
        font-size:12px;
        font-weight:950;
        letter-spacing:.2px;
    }}
    .psm-rank-note{{
        color:#5f7385;
        font-size:8px;
        margin:3px 2px 6px 2px;
        line-height:1.25;
    }}
    .psm-rank-table{{width:100%;border-collapse:collapse;table-layout:fixed;font-size:9px;color:#173f70;}}
    .psm-rank-table th{{background:#073f78;color:#ffffff;font-weight:950;padding:6px 5px;border:1px solid #073f78;height:24px;}}
    .psm-rank-table td{{padding:5px 5px;border:1px solid #d3dee6;background:#ffffff;text-align:center;height:22px;}}
    .psm-rank-table td.dept{{text-align:left;font-weight:800;}}
    .rank-good{{color:#159447;font-weight:900;}}
    .rank-watch{{color:#e5a400;font-weight:900;}}
    .rank-critical{{color:#d71920;font-weight:900;}}
    .rank-na{{color:#8a99a8;font-weight:800;}}
    </style>
    </head>
    <body>
      <div class="psm-rank-wrap">
        <div class="psm-rank-head">DEPARTMENT-WISE KPI &amp; DATA PERFORMANCE RANKING</div>
        <div class="psm-rank-scroll">
          {rank_table_html}
        </div>
      </div>
    </body>
    </html>
    """

    components.html(
        ranking_html,
        height=500,
        scrolling=False
    )

# ============================================================
# PSM MODULE NAVIGATION
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PSM NAVIGATION HEADER
   ========================================================= */

.psm-nav-title {
    width: 100%;
    box-sizing: border-box;

    background: linear-gradient(
        90deg,
        #073f78 0%,
        #07518b 55%,
        #0b6096 100%
    );

    color: #ffffff;

    border-radius: 9px;

    padding: 10px 16px;

    margin: 6px 0 9px 0;

    min-height: 46px;

    font-size: 12px;
    font-weight: 900;

    letter-spacing: 0.5px;

    box-shadow:
        0 3px 9px rgba(15, 60, 95, 0.16);

    line-height: 26px;
}


/* Instruction text */

.psm-nav-title .nav-instruction {
    float: right;

    color: rgba(255, 255, 255, 0.82);

    font-size: 8px;

    font-weight: 700;

    letter-spacing: 0.3px;

    line-height: 26px;
}

/* =========================================================
   PAGE LINK CARD
   ========================================================= */

/* Outer Streamlit page-link block */
div[data-testid="stPageLink"] {
    margin: 0 !important;
    padding: 0 !important;
}


/* Actual clickable card */
div[data-testid="stPageLink"] a {
    position: relative !important;

    display: flex !important;

    align-items: center !important;

    justify-content: flex-start !important;

    width: 100% !important;

    min-height: 58px !important;

    box-sizing: border-box !important;

    padding: 9px 10px 9px 13px !important;

    background: #ffffff !important;

    border: 1px solid #d5e2ec !important;

    border-radius: 9px !important;

    color: #073f78 !important;

    text-decoration: none !important;

    box-shadow:
        0 2px 7px rgba(20, 65, 95, 0.08) !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease,
        background 0.18s ease !important;

    overflow: hidden !important;
}


/* =========================================================
   BLUE ACCENT STRIPE
   ========================================================= */

div[data-testid="stPageLink"] a::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background: #1261a0;

    border-radius: 9px 0 0 9px;
}


/* =========================================================
   HOVER EFFECT
   ========================================================= */

div[data-testid="stPageLink"] a:hover {

    transform: translateY(-3px) !important;

    background: #f8fbfe !important;

    border-color: #8eb6d2 !important;

    box-shadow:
        0 7px 15px rgba(18, 63, 100, 0.15) !important;
}


/* =========================================================
   PAGE LINK TEXT
   ========================================================= */

div[data-testid="stPageLink"] a p {

    margin: 0 !important;

    padding: 0 !important;

    color: #173f70 !important;

    font-size: 9px !important;

    font-weight: 900 !important;

    letter-spacing: 0.1px !important;

    white-space: nowrap !important;
}


/* =========================================================
   ICON
   ========================================================= */

div[data-testid="stPageLink"] a svg {

    width: 18px !important;

    height: 18px !important;

    margin-right: 6px !important;

    flex-shrink: 0 !important;
}


/* =========================================================
   REMOVE STREAMLIT EXCESS SPACING
   ========================================================= */

div[data-testid="stPageLink"] + div {
    margin-top: 0 !important;
}


/* =========================================================
   COLUMN SPACING
   ========================================================= */

div[data-testid="column"] {
    padding-left: 3px !important;
    padding-right: 3px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION HEADER
# ============================================================

st.markdown(
    """
    <div class="psm-nav-title">
        🔴 &nbsp; PSM MODULE NAVIGATION
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span class="nav-instruction">
            CLICK A MODULE FOR DETAILED VIEW
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>

/* ============================================================
   MODULE NAVIGATION — ZERO GAP
   ============================================================ */

/* Remove gap between all 8 columns */
[data-testid="stHorizontalBlock"] {
    gap: 0px !important;
    column-gap: 0px !important;
}

/* Remove column padding */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    padding-left: 0px !important;
    padding-right: 0px !important;
    margin-left: 0px !important;
    margin-right: 0px !important;
}

/* Same fixed size for every button */
[data-testid="stPageLink"] {
    width: 150px !important;
    min-width: 150px !important;
    max-width: 150px !important;

    height: 56px !important;
    min-height: 56px !important;
    max-height: 56px !important;

    margin: 0px !important;
    padding: 0px !important;

    box-sizing: border-box !important;
}

/* Link fills the card */
[data-testid="stPageLink"] a {
    width: 150px !important;
    height: 56px !important;

    margin: 0px !important;
    padding: 0px 8px !important;

    box-sizing: border-box !important;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# MODULE NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4, nav5, nav6, nav7, nav8 = st.columns(
    8,
    gap="small"
)


with nav1:
    st.page_link(
        "pages/09_PT.py",
        label="PT",
        icon="📋"
    )


with nav2:
    st.page_link(
        "pages/10_PHA.py",
        label="PHA",
        icon="⚠️"
    )


with nav3:
    st.page_link(
        "pages/11_MOC.py",
        label="MOC",
        icon="🔄"
    )


with nav4:
    st.page_link(
        "pages/12_PSSR.py",
        label="PSSR",
        icon="🚀"
    )


with nav5:
    st.page_link(
        "pages/13_Training.py",
        label="TRAINING",
        icon="🎓"
    )


with nav6:
    st.page_link(
        "pages/14_PSI.py",
        label="PS INCIDENT",
        icon="🚨"
    )


with nav7:
    st.page_link(
        "pages/19_ALARM_&_INTERLOCK_MANAGEMENT.py",
        label="INTERLOCK",
        icon="⚙️"
    )


with nav8:
    st.page_link(
        "pages/20_PSM CE & BARRIER HEALTH.py",
        label="PSM CE / BARRIER",
        icon="🛡️"
    )
# ---------- FOOTER ----------
st.markdown(
    f"""<div class="footer">
        PSM EXECUTIVE CONTROL CENTER &nbsp;|&nbsp;
        View: <b>{selected_department}</b> &nbsp;|&nbsp;
        Live source: Google Sheet &nbsp;|&nbsp;
        Last refresh: {datetime.now().strftime("%d-%b-%Y %H:%M:%S")}
    </div>""",
    unsafe_allow_html=True,
)
