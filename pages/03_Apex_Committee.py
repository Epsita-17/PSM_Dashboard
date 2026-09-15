
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

                APEX COMMITTEE

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
    "<div style='height:12px;'></div>",
    unsafe_allow_html=True
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

selected_department = st.selectbox(
    "Department Status",
    ALL_DEPARTMENTS,
    index=0,
    key="global_department_selector",
)
# ============================================================
# APPLY GLOBAL DEPARTMENT FILTER
# ============================================================

pt = filter_selected_department(
    pt,
    selected_department
)

pha = filter_selected_department(
    pha,
    selected_department
)

rec = filter_selected_department(
    rec,
    selected_department
)

moc = filter_selected_department(
    moc,
    selected_department
)

pssr = filter_selected_department(
    pssr,
    selected_department
)

training = filter_selected_department(
    training,
    selected_department
)

soc = filter_selected_department(
    soc,
    selected_department
)

incident = filter_selected_department(
    incident,
    selected_department
)

interlock = filter_selected_department(
    interlock,
    selected_department
)

# Apply the same department selector to PSM CE so that KPI values
# and department-wise progress show the selected department only.
psm_ce = filter_selected_department(
    psm_ce,
    selected_department
)

# IMPORTANT: APEX KPIs must also follow the global department selector.
# Previously Barrier Audit and Audit Compliance were left unfiltered,
# which made their values appear fixed when the department was changed.
barrier_audit = filter_selected_department(
    loaded.get("Barrier Audit"),
    selected_department
)

audit = filter_selected_department(
    audit,
    selected_department
)

# ============================================================
# LIVE DATA BAR
# ============================================================
module_count = sum(
    1 for df in loaded.values()
    if df is not None and not df.empty
)

st.markdown(
    f"""
    <div class="live-bar">
        <b>LIVE DATA: Google Sheet → All Departments</b>
        &nbsp; | &nbsp;
        Refresh: 5 minutes
        &nbsp; | &nbsp;
        Modules with data: <b>{module_count}</b>
        &nbsp; | &nbsp;
        Last load: <b>{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# APEX COMMITTEE DASHBOARD
# ============================================================

st.markdown("""
<style>
.apex-hero{background:linear-gradient(135deg,#061a2d 0%,#073f78 55%,#0b6fa4 100%);border-radius:12px;padding:18px 22px;margin:4px 0 10px;box-shadow:0 5px 18px rgba(5,35,60,.20)}
.apex-title{color:#fff;font-size:28px;font-weight:900;letter-spacing:1px;line-height:1.05}
.apex-sub{color:#c7e4f5;font-size:10px;font-weight:800;letter-spacing:2.5px;margin-top:6px}
.apex-live{color:#9de7bb;font-size:9px;font-weight:800;margin-top:9px}
.apex-section{background:linear-gradient(90deg,#073f78,#0b6096);color:#fff;border-radius:7px;padding:7px 11px;font-size:10px;font-weight:900;letter-spacing:.7px;margin:9px 0 6px}
.apex-kpi{background:#fff;border:1px solid #d5e2ec;border-radius:9px;padding:10px 10px 9px;min-height:86px;box-shadow:0 2px 9px rgba(17,57,84,.08)}
.apex-kpi-label{color:#64788b;font-size:8px;font-weight:900;line-height:1.15;min-height:20px}
.apex-kpi-value{color:#073f78;font-size:25px;font-weight:900;margin-top:3px;line-height:1.1}
.apex-kpi-note{color:#8293a2;font-size:7px;margin-top:3px;line-height:1.15}
.apex-panel{background:#fff;border:1px solid #d5e2ec;border-radius:9px;padding:10px;box-shadow:0 2px 9px rgba(17,57,84,.07);height:100%}
.apex-panel-title{color:#073f78;font-size:10px;font-weight:900;letter-spacing:.4px;margin-bottom:4px}
.apex-att{border-radius:6px;padding:7px 9px;margin:5px 0;border-left:4px solid #d71920;background:#fff1f1}
.apex-att.warn{border-left-color:#e5a400;background:#fff8e5}
.apex-att.good{border-left-color:#279650;background:#eef9f1}
.apex-att-label{color:#627689;font-size:8px;font-weight:900}
.apex-att-value{color:#173f70;font-size:17px;font-weight:900;margin-top:2px}
.apex-footer{background:#061f35;color:#c7dce9;border-radius:7px;padding:8px;text-align:center;font-size:8px;font-weight:800;letter-spacing:.6px;margin-top:10px}
</style>
""", unsafe_allow_html=True)


# ============================================================
# RAW DATA FOR EXECUTIVE COMPARISON
# Keep the existing selected-department data untouched above;
# use loaded/raw sheets for the department ranking below.
# ============================================================
raw_pt = loaded.get("PT")
raw_pha = loaded.get("PHA")
raw_pssr = loaded.get("PSSR")
raw_moc = loaded.get("MOC")
raw_incident = loaded.get("PS Incident")
raw_interlock = loaded.get("Interlock ")
raw_barrier = loaded.get("Barrier Audit")
raw_audit = loaded.get("Audit Compliance")

# ------------------------------------------------------------
# STATUS HELPERS
# ------------------------------------------------------------
def safe_status(df, candidates=None):
    return status_counts(df, candidates)

# ============================================================
# CURRENT FILTER KPI CALCULATIONS
# ============================================================
pha_s = safe_status(pha)
pt_s = safe_status(pt)

pssr_s = safe_status(
    pssr,
    [
        "Overdue/Pending/Completed",
        "Overdue / Pending / Completed",
        "Status",
        "Current Status",
    ],
)

moc_s = safe_status(
    moc,
    [
        "Status (Open/Close)",
        "Status",
        "Current Status",
        "MOC Status",
    ],
)

# ------------------------------------------------------------
# INCIDENT
# ------------------------------------------------------------
incident_total = 0
incident_completed = 0
incident_pending = 0

if incident is not None and not incident.empty:
    incident_total = len(incident)
    inv_col = find_col(
        incident,
        ["Investigation status", "Investigation Status", "Investigation", "Status"],
    )
    if inv_col:
        inv = incident[inv_col].fillna("").astype(str).str.strip().str.lower()
        incident_completed = int(inv.isin(["completed", "complete", "closed", "done"]).sum())
        incident_pending = int(inv.isin(["pending", "ongoing", "open", "in progress", "in-progress"]).sum())

# ------------------------------------------------------------
# INTERLOCK
# ------------------------------------------------------------
interlock_pending = 0
if interlock is not None and not interlock.empty:
    il_status_col = find_col(
        interlock,
        ["Present Status / Action Required", "Present Status", "Status / Action Required", "Status"],
    )
    if il_status_col:
        il_status = interlock[il_status_col].fillna("").astype(str).str.lower()
        interlock_pending = int(il_status.str.contains(r"due\s*for\s*normalization|normalization\s*pending", regex=True, na=False).sum())

# ------------------------------------------------------------
# BARRIER
# ------------------------------------------------------------
barrier_assessed = 0
barrier_unacceptable = 0
barrier_df = clean_dataframe(barrier_audit)
if not barrier_df.empty:
    b_assessed = find_col(barrier_df, ["Barrier Health (C4/C5) (Number) Assessed", "Assessed"])
    b_unacceptable = find_col(barrier_df, ["Barrier Health (C4/C5) (Number) Unacceptable", "Unacceptable Barrier", "Unacceptable"])
    if b_assessed:
        barrier_assessed = int(pd.to_numeric(barrier_df[b_assessed], errors="coerce").fillna(0).sum())
    if b_unacceptable:
        barrier_unacceptable = int(pd.to_numeric(barrier_df[b_unacceptable], errors="coerce").fillna(0).sum())

# ------------------------------------------------------------
# AUDIT
# ------------------------------------------------------------
audit_done = 0
audit_pending = 0
if audit is not None and not audit.empty:
    audit_date_col = find_col(audit, ["Audit Date", "Last Audit Date", "Date"])
    if audit_date_col:
        ad = pd.to_datetime(audit[audit_date_col], errors="coerce")
        audit_done = int(ad.notna().sum())
        audit_pending = int(ad.isna().sum())
    else:
        audit_pending = len(audit)

# ============================================================
# OVERALL PSM HEALTH
# ============================================================
score_parts = []
if pha_s["total"] > 0:
    score_parts.append(pha_s["completed"] / pha_s["total"] * 100)
if pt_s["total"] > 0:
    score_parts.append(pt_s["completed"] / pt_s["total"] * 100)
if pssr_s["total"] > 0:
    score_parts.append(pssr_s["completed"] / pssr_s["total"] * 100)
if moc_s["total"] > 0:
    score_parts.append(moc_s["closed"] / moc_s["total"] * 100)
if incident_total > 0:
    score_parts.append(incident_completed / incident_total * 100)
if barrier_assessed > 0:
    score_parts.append(max(0, (barrier_assessed - barrier_unacceptable) / barrier_assessed * 100))

overall_score = sum(score_parts) / len(score_parts) if score_parts else 0
overall_score = max(0, min(100, overall_score))

# ============================================================
# EXECUTIVE SCORECARD
# ============================================================
st.markdown('<div class="apex-section">EXECUTIVE SAFETY SCORECARD</div>', unsafe_allow_html=True)

kpis = [
    ("OVERALL PSM HEALTH", f"{overall_score:.1f}%", "Integrated management health"),
    ("PSSR OVERDUE", f"{pssr_s['overdue']:,}", "Immediate attention"),
    ("OPEN MOC", f"{moc_s['open']:,}", "Changes requiring closure"),
    ("PS INCIDENTS", f"{incident_total:,}", "Recorded process incidents"),
    ("INVESTIGATION PENDING", f"{incident_pending:,}", "Incident closure"),
    ("INTERLOCK PENDING", f"{interlock_pending:,}", "Normalization required"),
    ("UNACCEPTABLE BARRIERS", f"{barrier_unacceptable:,}", "Critical barrier health"),
    ("AUDIT PENDING", f"{audit_pending:,}", "Audit coverage gap"),
]

cols = st.columns(8, gap="small")
for col, (label, value, note) in zip(cols, kpis):
    with col:
        st.markdown(
            f'<div class="apex-kpi"><div class="apex-kpi-label">{label}</div><div class="apex-kpi-value">{value}</div><div class="apex-kpi-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

# ============================================================
# EXECUTIVE MANAGEMENT VIEW
# ============================================================
st.markdown('<div class="apex-section">APEX MANAGEMENT VIEW</div>', unsafe_allow_html=True)

left, center, right = st.columns([1.0, 1.45, 1.0], gap="small")

# ------------------------------------------------------------
# HEALTH GAUGE
# ------------------------------------------------------------
with left:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">OVERALL PSM HEALTH</div>', unsafe_allow_html=True)
    gauge_color = "#159447" if overall_score >= 80 else "#e5a400" if overall_score >= 60 else "#d71920"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_score,
        number={"suffix": "%", "font": {"size": 30, "color": gauge_color}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 8}},
            "bar": {"color": gauge_color, "thickness": 0.25},
            "steps": [
                {"range": [0, 60], "color": "#fdeaea"},
                {"range": [60, 80], "color": "#fff4d6"},
                {"range": [80, 100], "color": "#eaf7ef"},
            ],
            "threshold": {"line": {"color": "#173f70", "width": 3}, "thickness": 0.8, "value": 90},
        },
    ))
    fig_gauge.update_layout(height=215, margin=dict(l=12, r=12, t=8, b=0), paper_bgcolor="white")
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False}, key="apex_health_gauge")
    state = "HEALTHY" if overall_score >= 80 else "WATCH" if overall_score >= 60 else "CRITICAL"
    st.markdown(f'<div style="text-align:center;font-size:10px;font-weight:900;color:{gauge_color};">● {state}</div></div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# MODULE PERFORMANCE
# ------------------------------------------------------------
with center:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">CORE PSM MODULE PERFORMANCE</div>', unsafe_allow_html=True)
    module_names = ["PT / PROCESS TECHNOLOGY", "PHA", "PSSR", "MOC", "INCIDENT INVESTIGATION", "BARRIER HEALTH"]
    module_scores = [
        pt_s["completed"] / pt_s["total"] * 100 if pt_s["total"] else 0,
        pha_s["completed"] / pha_s["total"] * 100 if pha_s["total"] else 0,
        pssr_s["completed"] / pssr_s["total"] * 100 if pssr_s["total"] else 0,
        moc_s["closed"] / moc_s["total"] * 100 if moc_s["total"] else 0,
        incident_completed / incident_total * 100 if incident_total else 0,
        (barrier_assessed - barrier_unacceptable) / barrier_assessed * 100 if barrier_assessed else 0,
    ]
    fig_mod = go.Figure(go.Bar(
        x=module_scores,
        y=module_names,
        orientation="h",
        text=[
            (
                f"{x:.0f}%"
                if total > 0
                else "N/A"
            )
            for x, total in [
                (module_scores[0], pt_s["total"]),
                (module_scores[1], pha_s["total"]),
                (module_scores[2], pssr_s["total"]),
                (module_scores[3], moc_s["total"]),
                (module_scores[4], incident_total),
                (module_scores[5], barrier_assessed),
            ]
        ],
        textposition="outside",
        marker=dict(color=["#159447" if x >= 80 else "#e5a400" if x >= 60 else "#d71920" for x in module_scores]),
    ))
    fig_mod.update_layout(
        height=270,
        margin=dict(l=5, r=42, t=4, b=4),
        xaxis=dict(range=[0, 110], ticksuffix="%", showgrid=True, gridcolor="#e4ebf1"),
        yaxis=dict(autorange="reversed", tickfont=dict(size=8)),
        paper_bgcolor="white", plot_bgcolor="white", showlegend=False,
    )
    st.plotly_chart(fig_mod, use_container_width=True, config={"displayModeBar": False}, key="apex_module_scores")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# MANAGEMENT ATTENTION
# ------------------------------------------------------------
with right:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">MANAGEMENT ATTENTION</div>', unsafe_allow_html=True)
    attention = [
        ("PSSR OVERDUE", pssr_s["overdue"], "critical"),
        ("OPEN MOC", moc_s["open"], "warn"),
        ("INTERLOCK PENDING", interlock_pending, "critical"),
        ("UNACCEPTABLE BARRIER", barrier_unacceptable, "critical"),
        ("AUDIT PENDING", audit_pending, "warn"),
    ]
    for label, value, cls in attention:
        st.markdown(f'<div class="apex-att {cls if cls != "critical" else ""}"><div class="apex-att-label">{label}</div><div class="apex-att-value">{value:,}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# DEPARTMENT-WISE EXECUTIVE RANKING
# ============================================================
st.markdown('<div class="apex-section">DEPARTMENT-WISE PSM PERFORMANCE</div>', unsafe_allow_html=True)

raw_sets = [raw_pt, raw_pha, raw_pssr, raw_moc, raw_incident]
department_scores = []

# Department ranking:
# - All Departments -> show every department
# - Individual department -> show only the selected department
ranking_departments = (
    ALL_DEPARTMENTS[1:]
    if selected_department == "All Departments"
    else [selected_department]
)

for department in ranking_departments:
    scores = []
    for dataset in raw_sets:
        if dataset is None or dataset.empty:
            continue
        ddf = filter_selected_department(dataset, department)
        if ddf.empty:
            continue
        if dataset is raw_incident:
            inv_col = find_col(ddf, ["Investigation status", "Investigation Status", "Investigation", "Status"])
            if inv_col:
                total = len(ddf)
                inv = ddf[inv_col].fillna("").astype(str).str.strip().str.lower()
                done = int(inv.isin(["completed", "complete", "closed", "done"]).sum())
                scores.append(done / total * 100 if total else 100)
        else:
            ss = safe_status(ddf)
            if ss["total"]:
                if dataset is raw_moc:
                    scores.append(ss["closed"] / ss["total"] * 100)
                else:
                    scores.append(ss["completed"] / ss["total"] * 100)
    if scores:
        department_scores.append({"Department": department, "PSM Score": sum(scores) / len(scores)})

department_df = pd.DataFrame(department_scores)

if not department_df.empty:
    department_df = department_df.sort_values("PSM Score", ascending=False).reset_index(drop=True)
    rank_cols = st.columns([0.9, 2.4, 1.2, 1.2], gap="small")
    for c, h in zip(rank_cols, ["RANK", "DEPARTMENT", "PSM SCORE", "STATUS"]):
        c.markdown(f'<div style="background:#073f78;color:#fff;padding:7px 8px;font-size:10px;font-weight:900;">{h}</div>', unsafe_allow_html=True)
    for idx, row in department_df.iterrows():
        score = float(row["PSM Score"])
        cls = "#159447" if score >= 80 else "#e5a400" if score >= 60 else "#d71920"
        status = "HEALTHY" if score >= 80 else "WATCH" if score >= 60 else "CRITICAL"
        vals = [str(idx + 1), str(row["Department"]), f"{score:.1f}%", status]
        row_cols = st.columns([0.9, 2.4, 1.2, 1.2], gap="small")
        for j, (c, val) in enumerate(zip(row_cols, vals)):
            extra = f"color:{cls};font-weight:900;" if j >= 2 else "color:#173f70;"
            c.markdown(f'<div style="background:#fff;border-bottom:1px solid #e2e9ef;padding:8px 8px;font-size:12px;{extra}">{val}</div>', unsafe_allow_html=True)
else:
    st.info("Department-wise performance data is not available.")

# ============================================================
# CRITICAL MODULE SNAPSHOT
# ============================================================
st.markdown('<div class="apex-section">CRITICAL MODULE SNAPSHOT</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="small")

with c1:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">PSSR GOVERNANCE</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3, gap="small")
    a.metric("TOTAL", pssr_s["total"])
    b.metric("COMPLETED", pssr_s["completed"])
    c.metric("OVERDUE", pssr_s["overdue"])
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">MANAGEMENT OF CHANGE</div>', unsafe_allow_html=True)
    a, b = st.columns(2, gap="small")
    a.metric("OPEN", moc_s["open"])
    b.metric("CLOSED", moc_s["closed"])
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="apex-panel"><div class="apex-panel-title">PROCESS SAFETY INCIDENT</div>', unsafe_allow_html=True)
    a, b = st.columns(2, gap="small")
    a.metric("TOTAL", incident_total)
    b.metric("PENDING", incident_pending)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# APEX DECISION BOARD
# ============================================================
st.markdown('<div class="apex-section">APEX COMMITTEE DECISION BOARD</div>', unsafe_allow_html=True)
d1, d2, d3, d4 = st.columns(4, gap="small")

cards = [
    (d1, "🔴", "IMMEDIATE ACTION", pssr_s["overdue"] + interlock_pending + barrier_unacceptable, "Critical safety exposure"),
    (d2, "🟠", "MANAGEMENT FOLLOW-UP", moc_s["open"] + audit_pending, "Governance actions"),
    (d3, "⚠️", "INVESTIGATION", incident_pending, "Incident closure"),
    (d4, "🟢", "PSM HEALTH", f"{overall_score:.1f}%", "Current integrated score"),
]

for container, icon, title, value, note in cards:
    with container:
        st.markdown(f'<div class="apex-kpi" style="text-align:center;min-height:96px;"><div style="font-size:20px;">{icon}</div><div class="apex-kpi-label">{title}</div><div class="apex-kpi-value">{value}</div><div class="apex-kpi-note">{note}</div></div>', unsafe_allow_html=True)

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
# ============================================================
# FOOTER
# ============================================================
st.markdown('''
<div class="apex-footer">
APEX COMMITTEE • PROCESS SAFETY MANAGEMENT • EXECUTIVE GOVERNANCE VIEW • LIVE DATA FROM GOOGLE SHEETS
</div>
''', unsafe_allow_html=True)


