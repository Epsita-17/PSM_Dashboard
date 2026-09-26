import io
import re
import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from html.parser import HTMLParser

from openpyxl import load_workbook

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM Dashboard - LIME PLANT",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GOOGLE SHEET
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

# IMPORTANT:
# These are the GIDs supplied for the LIME PLANT dashboard.
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
    "Interlock ": 1595602222,
    "PSM CE ": 1552637895,
    "Failure Data": 1071263265,
    "Barrier Audit": "1741048982",
    "Audit Compliance": "1790395364",
}

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
    margin-top: -50px !important;
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

                LIME CALCINATION PLANT

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


def filter_LIME_PLANT(df):
    """
    Filter only LIME PLANT records.

    VERY IMPORTANT:
    If a Department column exists, we MUST filter it.
    The old code returned the entire sheet when the Department
    column was not found, which is how a workbook row count such
    as 94 could incorrectly become TOTAL PT = 94.

    If no Department column exists, the sheet is treated as a
    module-specific sheet and its rows are retained.
    """
    df = clean_dataframe(df)

    if df.empty:
        return df

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

    if department_col is None:
        # Some module sheets may be dedicated to one module and
        # have no Department field. Do NOT destroy valid data.
        return df.copy()

    department = (
        df[department_col]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # Matches:
    # LIME PLANT
    # LIME PLANT
    # LIME PLANT
    # LIME PLANT
    # etc.
    mask = department.str.fullmatch(
        r"LIME PLANT",
        case=False,
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
# ============================================================
# AUDIT REPORT HYPERLINK LOADER
# ============================================================

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
    """
    Load Audit Compliance sheet and recover
    the actual Audit Report hyperlinks.
    """

    df = load_google_sheet(gid)

    if df.empty or not gid:
        return df

    df = clean_dataframe(df).copy()

    url_values = [""] * len(df)

    # --------------------------------------------------------
    # FIND AUDIT REPORT COLUMN
    # --------------------------------------------------------

    audit_report_col = find_col(
        df,
        [
            "Audit Report",
            "Audit Report Link",
            "Compliance Report",
            "Report",
        ],
    )

    # --------------------------------------------------------
    # METHOD 1 — XLSX HYPERLINKS
    # --------------------------------------------------------

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

            for row_no in range(
                (header_row or 1) + 1,
                ws.max_row + 1
            ):

                cell = ws.cell(
                    row=row_no,
                    column=report_col_num
                )

                url = ""

                # Normal hyperlink
                if cell.hyperlink:

                    try:
                        url = str(
                            cell.hyperlink.target or ""
                        ).strip()

                    except Exception:
                        url = ""

                # HYPERLINK() formula
                if not url and isinstance(cell.value, str):

                    match = re.search(
                        r'HYPERLINK\s*\(\s*["\']'
                        r'(https?://[^"\']+)["\']',
                        cell.value,
                        flags=re.IGNORECASE,
                    )

                    if match:
                        url = match.group(1).strip()

                idx = (
                    row_no
                    - (header_row or 1)
                    - 1
                )

                if (
                    0 <= idx < len(url_values)
                    and url
                ):
                    url_values[idx] = url

        workbook.close()

    except Exception:
        pass

    # --------------------------------------------------------
    # METHOD 2 — GVIZ HTML
    # --------------------------------------------------------

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

            report_index = list(
                df.columns
            ).index(audit_report_col)

            source_rows = parser.rows[1:]

            for i, parsed_row in enumerate(
                source_rows
            ):

                if i >= len(url_values):
                    continue

                if url_values[i]:
                    continue

                if report_index < len(parsed_row):

                    href = parsed_row[
                        report_index
                    ].get(
                        "href",
                        ""
                    ).strip()

                    if href:
                        url_values[i] = href

    except Exception:
        pass

    # --------------------------------------------------------
    # METHOD 3 — FALLBACK TO GOOGLE SHEET CELL
    # --------------------------------------------------------

    if audit_report_col:

        for i in range(len(df)):

            if url_values[i]:
                continue

            report_name = str(
                df.iloc[i][audit_report_col]
            ).strip()

            if (
                report_name
                and report_name.lower()
                not in {"nan", "none"}
            ):

                sheet_row = i + 2

                url_values[i] = (
                    f"https://docs.google.com/"
                    f"spreadsheets/d/"
                    f"{SPREADSHEET_ID}/edit?"
                    f"gid={gid}"
                    f"&range=E{sheet_row}"
                )

    # --------------------------------------------------------
    # STORE LIVE URL
    # --------------------------------------------------------

    df["__COMPLIANCE_REPORT_URL"] = url_values

    return df

def load_module(name):
    """Load a module and then apply the LIME PLANT filter."""
    raw = load_google_sheet(SHEETS.get(name))
    return filter_LIME_PLANT(raw)


def find_status_col(df, candidates=None):
    """Find the real status column, prioritizing explicit Open/Close fields."""
    if df is None or df.empty:
        return None

    normalized = {norm(c): c for c in df.columns}

    priority = [
        "Status (Open/Close)",
        "Status (Open / Close)",
        "Status",
        "Current Status",
        "Action Status",
        "Completion Status",
        "Investigation Status",
        "Recommendation Status",
    ]

    if candidates:
        priority = list(candidates) + priority

    seen = set()
    for candidate in priority:
        key = norm(candidate)
        if key in seen:
            continue
        seen.add(key)
        if key in normalized:
            return normalized[key]

    for column in df.columns:
        key = norm(column)
        if any(k in key for k in [
            "status",
            "actionstatus",
            "completionstatus",
            "investigationstatus",
            "recommendationstatus",
        ]):
            return column

    return None


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

    status_col = find_status_col(df, status_candidates)

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
    status_col = find_status_col(df, status_names)

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

    return result.reset_index(drop=True).head(5)


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

        st.info("No LIME PLANT records found.")

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
            height=178,
        )


MODULE_PAGE_LINKS = {
    "PROCESS TECHNOLOGY (PT)": "pages/09_PT.py",
    "PROCESS HAZARD ANALYSIS (PHA)": "pages/10_PHA.py",
    "PHA RECOMMENDATION": "pages/10_PHA.py",
    "MOC": "pages/11_MOC.py",
    "PRE-STARTUP SAFETY REVIEW (PSSR)": "pages/12_PSSR.py",
    "PROCESS SAFETY INCIDENT": "pages/14_PSI.py",
    "TRAINING": "pages/13_Training.py",
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
# CUSTOM KPI CARD
# ============================================================

def show_kpi_card(label, value):

    html = f'''<div style="
background:#ffffff;
border:1px solid #cbddea;
border-radius:8px;
padding:10px 8px;
min-height:75px;
text-align:left;
box-sizing:border-box;
margin-bottom:8px;
">
<div style="
color:#285779;
font-size:11px;
font-weight:800;
line-height:1.2;
margin-bottom:8px;
">{label}</div>
<div style="
color:#123f77;
font-size:28px;
font-weight:900;
line-height:1;
">{value}</div>
</div>'''

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

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

interlock = loaded["Interlock "]
psm_ce = loaded["PSM CE "]
audit = load_audit_with_links(SHEETS["Audit Compliance"])
audit = filter_LIME_PLANT(audit)
failure_data = loaded["Failure Data"]


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
        <b>LIVE DATA: Google Sheet → LIME PLANT</b>
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
# ROW 1 — PT / PHA / RECOMMENDATION / MOC
# ============================================================
a, b, c = st.columns(3, gap="small")


with a:

    with st.container(border=True):

        # PT HEADER
        show_module_title(
            1,
            "",
            "PROCESS TECHNOLOGY (PT)"
        )

        # PT KPI
        x = status_counts(pt)

        show_metric_row([
            ("TOTAL PT", x["total"]),
            ("COMPLETED", x["completed"]),
            ("ONGOING", x["ongoing"]),
        ])

        # PT REGISTER
        show_register(
            "PT REGISTER",
            pt,
            [
                "PT No",
                "PT No.",
                "PT ID",
                "ID"
            ],
            [
                "NAME OF PT",
                "Name of PT",
                "PT Name",
                "PT Description",
                "Description",
            ],
            [
                "Status",
                "Current Status"
            ],
        )

# ============================================================
# 2 — PROCESS HAZARD ANALYSIS (PHA)
# ============================================================


with b:

    with st.container(border=True):

        show_module_title(
            2,
            "△",
            "PROCESS HAZARD ANALYSIS (PHA)"
        )

        x = status_counts(pha)

        show_metric_row([
            ("TOTAL PHA", x["total"]),
            ("COMPLETED", x["completed"]),
            ("ONGOING", x["ongoing"]),
        ])

        show_register(
            "PHA REGISTER",
            pha,
            [
                "PHA No",
                "PHA No.",
                "PHA ID",
                "ID"
            ],
            [
                "Name of PHA",
                "PHA Name",
                "PHA Description",
                "Description"
            ],
            [
                "Status",
                "Current Status"
            ],
        )



# ============================================================
# 3 — PHA RECOMMENDATION
# ============================================================

with c:

    with st.container(border=True):

        show_module_title(
            3,
            "♧",
            "PHA RECOMMENDATION"
        )

        x = status_counts(
            rec,
            [
                "Status (Open/Close)",
                "Status (Open / Close)",
                "Status",
                "Action Status",
                "Recommendation Status",
            ],
        )

        show_metric_row([
            (
                "TOTAL RECOMMENDATIONS",
                x["total"]
            ),
            (
                "OPEN",
                x["open"]
            ),
            (
                "CLOSED",
                x["closed"]
            ),
        ])

        show_register(
            "RECOMMENDATION REGISTER",
            rec,
            [
                "PHA No",
                "PHA No.",
                "Recommendation No",
                "Recommendation ID",
                "ID"
            ],
            [
                "Recommendation Description",
                "Recommendation",
                "Description"
            ],
            [
                "Status (Open/Close)",
                "Status (Open / Close)",
                "Status",
                "Action Status",
                "Recommendation Status",
            ],
        )



# ============================================================
# 4 — MANAGEMENT OF CHANGE (MOC)
# LCP — FINAL HORIZONTAL LAYOUT
# ============================================================

with st.container(
        border=True,
        height=460
    ):

        # ----------------------------------------------------
        # MOC TITLE
        # ----------------------------------------------------

        show_module_title(
            "",
            "",
            "MANAGEMENT OF CHANGE(MOC)"
        )

        # ----------------------------------------------------
        # MOC COLUMN MAPPING
        # ----------------------------------------------------

        moc_change_type_col = find_col(
            moc,
            [
                "Change Type (Permanent/Temporary/Emergency)",
                "Change Type",
                "Type",
            ],
        )

        moc_category_col = find_col(
            moc,
            [
                "Category of changes (Technology/Personnel/Facility)",
                "Category of changes",
                "Category",
            ],
        )

        # ====================================================
        # LCP MOC REGISTER
        # ====================================================

        moc_chart = moc.copy()

        moc_department_col = find_col(
            moc,
            [
                "Department", "Departments", "Dept", "Department Name",
            ],
        )

        if moc_department_col:

            moc_chart = moc_chart[
                moc_chart[moc_department_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.upper()
                .str.contains(
                    "LCP",
                    na=False
                )
            ].copy()

        # ====================================================
        # FOUR HORIZONTAL SECTIONS
        #
        # SUMMARY | TYPE CHART | CATEGORY CHART | REGISTER
        # ====================================================

        moc_kpi_col, moc_type_col, moc_category_col_box, moc_register_col = st.columns(
            [0.70, 1.70, 1.70, 2.50],
            gap="small"
        )

        # ========================================================
        # 1 — MOC SUMMARY
        # ========================================================

        with moc_kpi_col:

            with st.container(
                    border=True,
                    height=390
            ):
                st.markdown(
                    """
                    <div style="
                        background:#07558E;
                        color:white;
                        font-size:10px;
                        font-weight:800;
                        padding:10px 5px;
                        border-radius:5px;
                        text-align:center;
                        margin-bottom:10px;
                        white-space:nowrap;
                    ">
                        MOC SUMMARY
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                x = status_counts(moc_chart)

                st.metric(
                    label="TOTAL",
                    value=x["total"]
                )

                st.metric(
                    label="OPEN",
                    value=x["open"]
                )

                st.metric(
                    label="CLOSED",
                    value=x["closed"]
                )

        # ====================================================
        # 2 — TYPE-WISE DISTRIBUTION
        # ====================================================

        with moc_type_col:

            with st.container(
                border=True,
                height=390
            ):

                st.markdown(
                    """
                    <div style="
                        background:#07558E;
                        color:white;
                        font-size:11px;
                        font-weight:800;
                        padding:8px 8px;
                        border-radius:4px;
                        text-align:center;
                        margin-bottom:5px;
                    ">
                        TYPE-WISE DISTRIBUTION
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if (
                    moc_change_type_col
                    and not moc_chart.empty
                ):

                    type_data = (
                        moc_chart[moc_change_type_col]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                    )

                    type_data = type_data[
                        type_data != ""
                    ]

                    type_counts = (
                        type_data.value_counts()
                    )

                    if not type_counts.empty:

                        type_labels = [
                            f"{label} {int(value)} "
                            f"({value / type_counts.sum() * 100:.0f}%)"
                            for label, value
                            in zip(
                                type_counts.index,
                                type_counts.values
                            )
                        ]

                        fig_type = go.Figure(
                            data=[
                                go.Pie(
                                    labels=type_labels,
                                    values=type_counts.values,
                                    hole=0.60,
                                    textinfo="none",
                                    hovertemplate=(
                                        "%{label}"
                                        "<extra></extra>"
                                    ),
                                )
                            ]
                        )

                        # CENTER VALUE
                        fig_type.add_annotation(
                            text=(
                                f"<b>{x['total']}</b>"
                                "<br>"
                                "<span style='font-size:11px'>"
                                "Total MOC"
                                "</span>"
                            ),
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(
                                size=24,
                                color="#173F70"
                            ),
                            align="center",
                        )

                        fig_type.update_layout(
                            height=330,

                            margin=dict(
                                l=5,
                                r=5,
                                t=5,
                                b=45
                            ),

                            showlegend=True,

                            # LEGEND AT BOTTOM
                            legend=dict(
                                orientation="h",
                                x=0.5,
                                y=-0.08,
                                xanchor="center",
                                yanchor="top",
                                font=dict(
                                    size=9
                                ),
                            ),

                            font=dict(
                                size=9
                            ),
                        )

                        st.plotly_chart(
                            fig_type,
                            use_container_width=True,
                            config={
                                "displayModeBar": False
                            },
                            key="coke_oven_type_donut_final",
                        )

                    else:

                        st.info(
                            "No LCP MOC Type data found."
                        )

                else:

                    st.info(
                        "MOC Change Type column not found."
                    )

        # ====================================================
        # 3 — CATEGORY-WISE DISTRIBUTION
        # ====================================================

        with moc_category_col_box:

            with st.container(
                border=True,
                height=390
            ):

                st.markdown(
                    """
                    <div style="
                        background:#07558E;
                        color:white;
                        font-size:11px;
                        font-weight:800;
                        padding:8px 8px;
                        border-radius:4px;
                        text-align:center;
                        margin-bottom:5px;
                    ">
                        CATEGORY-WISE DISTRIBUTION
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if (
                    moc_category_col
                    and not moc_chart.empty
                ):

                    category_data = (
                        moc_chart[moc_category_col]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                    )

                    category_data = category_data[
                        category_data != ""
                    ]

                    category_counts = (
                        category_data.value_counts()
                    )

                    if not category_counts.empty:

                        category_labels = [
                            f"{label} {int(value)} "
                            f"({value / category_counts.sum() * 100:.0f}%)"
                            for label, value
                            in zip(
                                category_counts.index,
                                category_counts.values
                            )
                        ]

                        fig_category = go.Figure(
                            data=[
                                go.Pie(
                                    labels=category_labels,
                                    values=category_counts.values,
                                    hole=0.60,
                                    textinfo="none",
                                    hovertemplate=(
                                        "%{label}"
                                        "<extra></extra>"
                                    ),
                                )
                            ]
                        )

                        # CENTER VALUE
                        fig_category.add_annotation(
                            text=(
                                f"<b>{x['total']}</b>"
                                "<br>"
                                "<span style='font-size:11px'>"
                                "Total MOC"
                                "</span>"
                            ),
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(
                                size=24,
                                color="#173F70"
                            ),
                            align="center",
                        )

                        fig_category.update_layout(
                            height=330,

                            margin=dict(
                                l=5,
                                r=5,
                                t=5,
                                b=45
                            ),

                            showlegend=True,

                            # LEGEND AT BOTTOM
                            legend=dict(
                                orientation="h",
                                x=0.5,
                                y=-0.08,
                                xanchor="center",
                                yanchor="top",
                                font=dict(
                                    size=9
                                ),
                            ),

                            font=dict(
                                size=9
                            ),
                        )

                        st.plotly_chart(
                            fig_category,
                            use_container_width=True,
                            config={
                                "displayModeBar": False
                            },
                            key="coke_oven_moc_category_donut_final",
                        )

                    else:

                        st.info(
                            "No LCP MOC Category data found."
                        )

                else:

                    st.info(
                        "MOC Category column not found."
                    )

        # ====================================================
        # 4 — MOC REGISTER
        # ====================================================

        with moc_register_col:

            with st.container(
                border=True,
                height=390
            ):

                st.markdown(
                    """
                    <div style="
                        background:#07558E;
                        color:white;
                        font-size:11px;
                        font-weight:800;
                        padding:8px 10px;
                        border-radius:4px;
                        text-align:left;
                        margin-bottom:8px;
                    ">
                        MOC REGISTER
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ========================================================
                # LCP MOC REGISTER
                # ========================================================

                register_df = moc_chart.copy()

                if register_df.empty:

                    st.info(
                        "No LCP MOC records found."
                    )

                else:

                    # ----------------------------------------------------
                    # FIND MOC NUMBER COLUMN
                    # ----------------------------------------------------

                    moc_no_col = find_col(
                        register_df,
                        [
                            "MOC No.",
                            "MOC No",
                            "MOC Number",
                            "MOC ID",
                            "ID",
                        ],
                    )

                    # ----------------------------------------------------
                    # FIND DESCRIPTION COLUMN
                    # ----------------------------------------------------

                    moc_desc_col = find_col(
                        register_df,
                        [
                            "Description of Change",
                            "Description",
                            "MOC Description",
                            "Name of MOC",
                            "MOC Name",
                        ],
                    )

                    # ----------------------------------------------------
                    # FIND TYPE COLUMN
                    # ----------------------------------------------------

                    moc_type_col = find_col(
                        register_df,
                        [
                            "Change Type (Permanent/Temporary/Emergency)",
                            "Change Type",
                            "Type",
                        ],
                    )

                    # ----------------------------------------------------
                    # FIND STATUS COLUMN
                    # ----------------------------------------------------

                    moc_status_col = find_col(
                        register_df,
                        [
                            "Status",
                            "Current Status",
                            "MOC Status",
                        ],
                    )

                    # ----------------------------------------------------
                    # FIND REMARKS COLUMN
                    # ----------------------------------------------------

                    moc_remarks_col = find_col(
                        register_df,
                        [
                            "Remarks",
                            "Remark",
                            "Comments",
                        ],
                    )

                    # ----------------------------------------------------
                    # CREATE DISPLAY REGISTER
                    # ----------------------------------------------------

                    display_moc = pd.DataFrame(
                        index=register_df.index
                    )

                    if moc_no_col:

                        display_moc["MOC No."] = (
                            register_df[moc_no_col]
                            .fillna("-")
                            .astype(str)
                            .str.strip()
                        )

                    else:

                        display_moc["MOC No."] = "-"

                    if moc_desc_col:

                        display_moc["Description"] = (
                            register_df[moc_desc_col]
                            .fillna("-")
                            .astype(str)
                            .str.strip()
                        )

                    else:

                        display_moc["Description"] = "-"

                    if moc_type_col:

                        display_moc["Type"] = (
                            register_df[moc_type_col]
                            .fillna("-")
                            .astype(str)
                            .str.strip()
                        )

                    else:

                        display_moc["Type"] = "-"

                    if moc_status_col:

                        display_moc["Status"] = (
                            register_df[moc_status_col]
                            .fillna("-")
                            .astype(str)
                            .str.strip()
                        )

                    else:

                        display_moc["Status"] = "-"

                    if moc_remarks_col:

                        display_moc["Remarks"] = (
                            register_df[moc_remarks_col]
                            .fillna("-")
                            .astype(str)
                            .str.strip()
                        )

                    else:

                        display_moc["Remarks"] = "-"

                    # ----------------------------------------------------
                    # STATUS COLOUR
                    # ----------------------------------------------------

                    styled_df = (
                        display_moc.style
                        .map(
                            status_style,
                            subset=["Status"]
                        )
                    )

                    # ----------------------------------------------------
                    # DISPLAY REGISTER
                    # ----------------------------------------------------

                    st.dataframe(
                        styled_df,
                        use_container_width=True,
                        hide_index=True,
                        height=315,

                        column_config={

                            "MOC No.": st.column_config.TextColumn(
                                "MOC No.",
                                width="medium"
                            ),

                            "Description": st.column_config.TextColumn(
                                "Description",
                                width="large"
                            ),

                            "Type": st.column_config.TextColumn(
                                "Type",
                                width="small"
                            ),

                            "Status": st.column_config.TextColumn(
                                "Status",
                                width="small"
                            ),

                            "Remarks": st.column_config.TextColumn(
                                "Remarks",
                                width="small"
                            ),
                        },
                    )


# ============================================================
# ROW 2 — PSSR / INCIDENT / TRAINING
# ============================================================

a, b, c = st.columns(
    [1.20, 1.40, 1.40],
    gap="small"
)


# ============================================================
# 5 — PSSR
# ============================================================

with a:
    with st.container(border=True):

        show_module_title(
            5,
            "",
            "PRE-STARTUP SAFETY REVIEW (PSSR)"
        )

        # --------------------------------------------------------
        # FIND PSSR STATUS COLUMN
        # --------------------------------------------------------
        pssr_status_col = find_col(
            pssr,
            [
                "Overdue/Pending/Completed",
                "Overdue / Pending / Completed",
                "Overdue Pending Completed",
                "Status",
                "Current Status"
            ]
        )

        # --------------------------------------------------------
        # CALCULATE PSSR STATUS COUNTS
        # --------------------------------------------------------
        if pssr is None or pssr.empty:

            total_pssr = 0
            completed_pssr = 0
            pending_pssr = 0
            overdue_pssr = 0

        else:

            total_pssr = len(pssr)

            if pssr_status_col is not None:

                pssr_status = (
                    pssr[pssr_status_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.casefold()
                )

                completed_pssr = int(
                    pssr_status.str.contains(
                        "completed",
                        na=False
                    ).sum()
                )

                pending_pssr = int(
                    pssr_status.str.contains(
                        "pending",
                        na=False
                    ).sum()
                )

                overdue_pssr = int(
                    pssr_status.str.contains(
                        "overdue",
                        na=False
                    ).sum()
                )

            else:

                completed_pssr = 0
                pending_pssr = 0
                overdue_pssr = 0

        # --------------------------------------------------------
        # KPI CARDS
        # --------------------------------------------------------
        show_metric_row([
            ("TOTAL PSSR", total_pssr),
            ("COMPLETED", completed_pssr),
            ("PENDING", pending_pssr),
            ("OVERDUE", overdue_pssr),
        ])

        # --------------------------------------------------------
        # PSSR REGISTER
        # --------------------------------------------------------
        show_register(
            "PSSR REGISTER",
            pssr,
            [
                "PSSR No.",
                "PSSR No",
                "PSSR ID",
                "ID"
            ],
            [
                "PSSR Description",
                "Description",
                "PSSR Name"
            ],
            [
                "Overdue/Pending/Completed",
                "Overdue / Pending / Completed",
                "Status",
                "Current Status"
            ],
        )
# ============================================================
# 6 — PROCESS SAFETY INCIDENT
# ============================================================

with b:

    with st.container(
        border=True,
        height=365
    ):

        show_module_title(
            6,
            "⚠",
            "PROCESS SAFETY INCIDENT"
        )

        # ----------------------------------------------------
        # COLUMN MAPPING
        # B = Department → Total Incidents
        # F = Incident Classification
        # G = Incident Level
        # J = Investigation Status
        # ----------------------------------------------------

        if len(incident.columns) >= 2:
            department_col = incident.columns[1]
        else:
            department_col = None

        if len(incident.columns) >= 6:
            classification_col = incident.columns[5]
        else:
            classification_col = find_col(
                incident,
                [
                    "Incident Classification",
                    "Incident classification",
                    "Classification",
                ]
            )

        if len(incident.columns) >= 7:
            level_col = incident.columns[6]
        else:
            level_col = find_col(
                incident,
                [
                    "Incident Level",
                    "Incident level",
                    "Level",
                ]
            )

        if len(incident.columns) >= 10:
            investigation_status_col = (
                incident.columns[9]
            )
        else:
            investigation_status_col = find_col(
                incident,
                [
                    "Investigation status",
                    "Investigation Status",
                    "Investigation",
                    "Status",
                ]
            )

        # ----------------------------------------------------
        # TOTAL INCIDENTS — COLUMN B
        # ----------------------------------------------------

        total_incidents = 0

        if (
            department_col
            and not incident.empty
        ):

            department_values = (
                incident[department_col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            total_incidents = (
                department_values
                .replace(
                    [
                        "",
                        "-",
                        "nan",
                        "None"
                    ],
                    pd.NA
                )
                .notna()
                .sum()
            )

        # ----------------------------------------------------
        # INVESTIGATION STATUS — COLUMN J
        # ----------------------------------------------------

        investigation_completed = 0
        investigation_pending = 0

        if (
            investigation_status_col
            and not incident.empty
        ):

            investigation_values = (
                incident[
                    investigation_status_col
                ]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            investigation_completed = (
                investigation_values
                .isin(
                    [
                        "completed",
                        "complete",
                        "closed",
                        "done",
                    ]
                )
                .sum()
            )

            investigation_pending = (
                investigation_values
                .isin(
                    [
                        "pending",
                        "ongoing",
                        "open",
                        "in progress",
                        "in-progress",
                    ]
                )
                .sum()
            )

        # ----------------------------------------------------
        # COMPACT KPI CARDS
        # ----------------------------------------------------

        m1, m2, m3 = st.columns(
            [0.70, 0.70, 0.70],
            gap="small"
        )

        with m1:

            st.metric(
                "TOTAL INCIDENTS",
                int(total_incidents)
            )

        with m2:

            st.metric(
                "INVESTIGATION COMPLETED",
                int(investigation_completed)
            )

        with m3:

            st.metric(
                "INVESTIGATION PENDING",
                int(investigation_pending)
            )

        # ====================================================
        # TWO PSI GRAPHS
        # ====================================================

        p1, p2 = st.columns(
            2,
            gap="small"
        )

        # ====================================================
        # CLASSIFICATION-WISE
        # ====================================================

        with p1:

            st.caption(
                "CLASSIFICATION-WISE DISTRIBUTION"
            )

            if (
                classification_col
                and not incident.empty
            ):

                classification_values = (
                    incident[
                        classification_col
                    ]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                classification_values = (
                    classification_values[
                        ~classification_values.isin(
                            [
                                "",
                                "-",
                                "nan",
                                "none"
                            ]
                        )
                    ]
                )

                # ------------------------------------------------
                # STANDARDIZE CLASSIFICATION
                # Serious must be checked FIRST
                # ------------------------------------------------

                classification_values = (
                    classification_values.map(
                        lambda x:
                        "Serious Process Incident"
                        if (
                            "serious" in x
                            and "process" in x
                            and "incident" in x
                        )
                        else
                        "Process Incident"
                        if (
                            "process" in x
                            and "incident" in x
                        )
                        else
                        "Near Miss"
                        if (
                            "near" in x
                            and "miss" in x
                        )
                        else x.title()
                    )
                )

                classification_counts = (
                    classification_values
                    .value_counts()
                )

                classification_order = [
                    "Near Miss",
                    "Process Incident",
                    "Serious Process Incident",
                ]

                classification_counts = (
                    classification_counts
                    .reindex(
                        classification_order,
                        fill_value=0
                    )
                )

                classification_counts = (
                    classification_counts[
                        classification_counts > 0
                    ]
                )

                if not classification_counts.empty:

                    fig_class = go.Figure()

                    fig_class.add_trace(
                        go.Bar(
                            x=classification_counts.values,
                            y=classification_counts.index,
                            orientation="h",
                            width=0.50,
                            text=classification_counts.values,
                            textposition="outside",

                            marker=dict(
                                color=[
                                    "#0751a5"
                                    if x == "Near Miss"
                                    else "#e31b23"
                                    if x == "Process Incident"
                                    else "#808080"
                                    for x
                                    in classification_counts.index
                                ]
                            ),

                            hovertemplate=(
                                "%{y}: %{x}"
                                "<extra></extra>"
                            ),
                        )
                    )

                    fig_class.update_layout(
                        height=180,
                        margin=dict(
                            l=5,
                            r=25,
                            t=5,
                            b=5
                        ),
                        showlegend=False,
                        font=dict(size=9),

                        xaxis=dict(
                            title=None,
                            dtick=1,
                            showgrid=True,
                            gridcolor="#e1e7ef",
                            zeroline=False,
                        ),

                        yaxis=dict(
                            title=None,
                            autorange="reversed",
                        ),

                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )

                    st.plotly_chart(
                        fig_class,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="psi_classification_chart",
                    )

                else:

                    st.info(
                        "No incident classification data."
                    )

            else:

                st.info(
                    "Incident Classification column not found."
                )

        # ====================================================
        # LEVEL-WISE
        # ====================================================

        with p2:

            st.caption(
                "LEVEL-WISE DISTRIBUTION"
            )

            if (
                level_col
                and not incident.empty
            ):

                level_values = (
                    incident[level_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                level_values = (
                    level_values[
                        ~level_values.isin(
                            [
                                "",
                                "-",
                                "nan",
                                "none"
                            ]
                        )
                    ]
                )

                level_values = (
                    level_values.map(
                        lambda x:
                        "Level 1"
                        if "level 1" in x
                        else
                        "Level 2"
                        if "level 2" in x
                        else
                        "Level 3"
                        if "level 3" in x
                        else
                        "Level 4"
                        if "level 4" in x
                        else x.title()
                    )
                )

                level_counts = (
                    level_values
                    .value_counts()
                )

                level_order = [
                    "Level 1",
                    "Level 2",
                    "Level 3",
                    "Level 4",
                ]

                level_counts = (
                    level_counts
                    .reindex(
                        level_order,
                        fill_value=0
                    )
                )

                level_counts = (
                    level_counts[
                        level_counts > 0
                    ]
                )

                if not level_counts.empty:

                    fig_level = go.Figure()

                    fig_level.add_trace(
                        go.Bar(
                            x=level_counts.values,
                            y=level_counts.index,
                            orientation="h",
                            width=0.50,
                            text=level_counts.values,
                            textposition="outside",

                            marker=dict(
                                color=[
                                    "#0751a5"
                                    if x == "Level 1"
                                    else "#e31b23"
                                    if x == "Level 2"
                                    else "#808080"
                                    if x == "Level 3"
                                    else "#173f70"
                                    for x
                                    in level_counts.index
                                ]
                            ),

                            hovertemplate=(
                                "%{y}: %{x}"
                                "<extra></extra>"
                            ),
                        )
                    )

                    fig_level.update_layout(
                        height=180,
                        margin=dict(
                            l=5,
                            r=25,
                            t=5,
                            b=5
                        ),
                        showlegend=False,
                        font=dict(size=9),

                        xaxis=dict(
                            title=None,
                            dtick=1,
                            showgrid=True,
                            gridcolor="#e1e7ef",
                            zeroline=False,
                        ),

                        yaxis=dict(
                            title=None,
                            autorange="reversed",
                        ),

                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )

                    st.plotly_chart(
                        fig_level,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="psi_level_chart",
                    )

                else:

                    st.info(
                        "No incident level data."
                    )

            else:

                st.info(
                    "Incident Level column not found."
                )


# ============================================================
# 7 — TRAINING
# ============================================================

with c:

    with st.container(
        border=True,
        height=365
    ):

        show_module_title(
            7,
            "♙",
            "TRAINING"
        )


        if (
            training is None
            or training.empty
        ):

            st.info(
                "No LIME PLANT training data found."
            )

        else:

            tr = training.copy()

            # ------------------------------------------------
            # FIND COLUMNS
            # ------------------------------------------------

            process_col = find_col(
                tr,
                ["Process"]
            )

            department_col = find_col(
                tr,
                ["Departments"]
            )

            total_l08_col = find_col(
                tr,
                [
                    "Total Employees (L08 & Above)"
                ]
            )

            total_below_l08_col = find_col(
                tr,
                [
                    "Total Employees (Below L08)"
                ]
            )

            total_associates_col = find_col(
                tr,
                [
                    "Total Associates"
                ]
            )

            total_contractual_col = find_col(
                tr,
                [
                    "Total Contractual Workers"
                ]
            )

            completed_l08_col = find_col(
                tr,
                [
                    "Completed Training (L08 & Above)"
                ]
            )

            completed_below_l08_col = find_col(
                tr,
                [
                    "Completed Training (Below L08)"
                ]
            )

            completed_associates_col = find_col(
                tr,
                [
                    "Completed Training (Associates)"
                ]
            )

            completed_contractual_col = find_col(
                tr,
                [
                    "Completed Training (Contracts)"
                ]
            )

            required_columns = [
                process_col,
                total_l08_col,
                total_below_l08_col,
                total_associates_col,
                total_contractual_col,
                completed_l08_col,
                completed_below_l08_col,
                completed_associates_col,
                completed_contractual_col,
            ]

            if any(
                col is None
                for col in required_columns
            ):

                st.error(
                    "Training Google Sheet column mapping error."
                )

            else:

                def to_number(series):

                    return pd.to_numeric(
                        series
                        .astype(str)
                        .str.replace(
                            ",",
                            "",
                            regex=False
                        )
                        .str.replace(
                            "%",
                            "",
                            regex=False
                        )
                        .str.strip(),
                        errors="coerce"
                    )

                # ------------------------------------------------
                # BUILD HEATMAP DATA
                # ------------------------------------------------

                heatmap_df = pd.DataFrame()

                heatmap_df["Module"] = (
                    tr[process_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                total_l08 = to_number(
                    tr[total_l08_col]
                )

                total_below_l08 = to_number(
                    tr[total_below_l08_col]
                )

                total_associates = to_number(
                    tr[total_associates_col]
                )

                total_contractual = to_number(
                    tr[total_contractual_col]
                )

                completed_l08 = to_number(
                    tr[completed_l08_col]
                )

                completed_below_l08 = to_number(
                    tr[completed_below_l08_col]
                )

                completed_associates = to_number(
                    tr[completed_associates_col]
                )

                completed_contractual = to_number(
                    tr[completed_contractual_col]
                )

                # ------------------------------------------------
                # COMPLETION %
                # Completed / Total × 100
                # ------------------------------------------------

                heatmap_df["L08 & Above"] = (
                    completed_l08
                    .div(
                        total_l08.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Below L08"] = (
                    completed_below_l08
                    .div(
                        total_below_l08.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Associates"] = (
                    completed_associates
                    .div(
                        total_associates.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Contractual"] = (
                    completed_contractual
                    .div(
                        total_contractual.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df = heatmap_df[
                    heatmap_df["Module"]
                    .str.strip() != ""
                ].copy()

                # ------------------------------------------------
                # MODULE ORDER
                # ------------------------------------------------

                module_order = [
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

                heatmap_df["_order"] = (
                    heatmap_df["Module"]
                    .apply(
                        lambda x:
                        module_order.index(x)
                        if x in module_order
                        else 999
                    )
                )

                heatmap_df = (
                    heatmap_df
                    .sort_values(
                        ["_order", "Module"]
                    )
                    .drop(
                        columns="_order"
                    )
                )

                # ------------------------------------------------
                # DISPLAY DATA
                # ------------------------------------------------

                display_df = heatmap_df.copy()

                percentage_columns = [
                    "L08 & Above",
                    "Below L08",
                    "Associates",
                    "Contractual",
                ]

                for column in percentage_columns:

                    display_df[column] = (
                        display_df[column]
                        .apply(
                            lambda x:
                            "—"
                            if pd.isna(x)
                            else f"{x:.2f}%"
                        )
                    )

                # ------------------------------------------------
                # HEATMAP STYLE
                # ------------------------------------------------

                def heatmap_style(column):

                    styles = []

                    for value in column:

                        numeric = pd.to_numeric(
                            str(value)
                            .replace("%", ""),
                            errors="coerce"
                        )

                        if pd.isna(numeric):

                            styles.append(
                                "background-color:#ffffff;"
                                "color:#8a97a5;"
                                "text-align:center;"
                            )

                        else:

                            numeric = max(
                                0,
                                min(
                                    100,
                                    float(numeric)
                                )
                            )

                            if numeric <= 50:

                                ratio = numeric / 50

                                red = 255

                                green = int(
                                    220
                                    + (
                                        25 * ratio
                                    )
                                )

                                blue = int(
                                    220
                                    - (
                                        70 * ratio
                                    )
                                )

                            else:

                                ratio = (
                                    numeric - 50
                                ) / 50

                                red = int(
                                    255
                                    - (
                                        55 * ratio
                                    )
                                )

                                green = 245

                                blue = int(
                                    150
                                    + (
                                        45 * ratio
                                    )
                                )

                            styles.append(
                                f"background-color:"
                                f"rgb({red},{green},{blue});"
                                "color:#173f70;"
                                "font-weight:700;"
                                "text-align:center;"
                            )

                    return styles

                styled_df = (
                    display_df.style
                    .apply(
                        heatmap_style,
                        subset=percentage_columns,
                        axis=0,
                    )
                    .set_properties(
                        subset=["Module"],
                        **{
                            "font-weight": "700",
                            "color": "#173f70",
                            "text-align": "left",
                        }
                    )
                    .set_properties(
                        **{
                            "font-size": "10px",
                            "border": "1px solid #d6e1eb",
                        }
                    )
                    .set_table_styles(
                        [
                            {
                                "selector": "th",
                                "props": [
                                    (
                                        "background-color",
                                        "#073f7c"
                                    ),
                                    (
                                        "color",
                                        "white"
                                    ),
                                    (
                                        "font-weight",
                                        "700"
                                    ),
                                    (
                                        "text-align",
                                        "center"
                                    ),
                                    (
                                        "font-size",
                                        "10px"
                                    ),
                                ],
                            }
                        ]
                    )
                )

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    height=245,
                    key="bf_training_heatmap",
                )


# ============================================================
# ROW 3 — SOC / SOL + AUDIT
# ============================================================

a, b = st.columns(
    [1.35, 1.65],
    gap="small"
)


# ============================================================
# 8 — SOC / SOL DEVIATION
# ============================================================

with a:

    with st.container(border=True):

        show_module_title(
            8,
            "",
            "SOC / SOL DEVIATION"
        )

        if (
            soc is None
            or soc.empty
        ):

            st.info(
                "No SOC / SOL data available."
            )

        else:

            month_col = find_col(
                soc,
                [
                    "Month",
                    "MONTH",
                    "month"
                ]
            )

            department_col = find_col(
                soc,
                [
                    "Department",
                    "DEPARTMENT",
                    "department"
                ]
            )

            soc_col = find_col(
                soc,
                [
                    "SOC Deviation Nos.",
                    "SOC Deviation No.",
                    "SOC Deviation",
                    "SOC"
                ]
            )

            sol_col = find_col(
                soc,
                [
                    "SOL Deviation Nos.",
                    "SOL Deviation No.",
                    "SOL Deviation",
                    "SOL"
                ]
            )

            if month_col is None:

                st.error(
                    "Month column not found in SOC / SOL Google Sheet."
                )

            else:

                df_socsol = soc.copy()

                # ------------------------------------------------
                # MONTH
                # ------------------------------------------------

                df_socsol["_MONTH"] = (
                    df_socsol[month_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                df_socsol = df_socsol[
                    df_socsol["_MONTH"] != ""
                ].copy()

                # ------------------------------------------------
                # LIME PLANT FILTER
                # ------------------------------------------------

                if department_col is not None:
                    df_socsol["_DEPARTMENT"] = (
                        df_socsol[department_col]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                        .str.lower()
                    )

                    df_socsol = df_socsol[
                        df_socsol["_DEPARTMENT"].str.contains(
                            "LIME PLANT",
                            case=False,
                            na=False
                        )
                    ].copy()

                # ------------------------------------------------
                # SOC
                # ------------------------------------------------

                if soc_col is not None:

                    df_socsol["_SOC_VALUE"] = (
                        pd.to_numeric(
                            df_socsol[soc_col],
                            errors="coerce"
                        )
                        .fillna(0)
                    )

                else:

                    df_socsol["_SOC_VALUE"] = 0

                # ------------------------------------------------
                # SOL
                # ------------------------------------------------

                if sol_col is not None:

                    df_socsol["_SOL_VALUE"] = (
                        pd.to_numeric(
                            df_socsol[sol_col],
                            errors="coerce"
                        )
                        .fillna(0)
                    )

                else:

                    df_socsol["_SOL_VALUE"] = 0

                # ------------------------------------------------
                # FY MONTHS
                # ------------------------------------------------

                fy_months = [
                    "Apr-26",
                    "May-26",
                    "Jun-26",
                    "Jul-26",
                    "Aug-26",
                    "Sep-26",
                    "Oct-26",
                    "Nov-26",
                    "Dec-26",
                    "Jan-27",
                    "Feb-27",
                    "Mar-27",
                ]

                # ------------------------------------------------
                # MONTH-WISE SOC
                # ------------------------------------------------

                soc_monthly = (
                    df_socsol
                    .groupby(
                        "_MONTH",
                        as_index=False
                    )["_SOC_VALUE"]
                    .sum()
                )

                # ------------------------------------------------
                # MONTH-WISE SOL
                # ------------------------------------------------

                sol_monthly = (
                    df_socsol
                    .groupby(
                        "_MONTH",
                        as_index=False
                    )["_SOL_VALUE"]
                    .sum()
                )

                # ------------------------------------------------
                # CREATE MONTHLY TABLE
                # ------------------------------------------------

                monthly = pd.DataFrame({
                    "_MONTH": fy_months
                })

                monthly = monthly.merge(
                    soc_monthly,
                    on="_MONTH",
                    how="left"
                )

                monthly = monthly.merge(
                    sol_monthly,
                    on="_MONTH",
                    how="left"
                )

                monthly["_SOC_VALUE"] = (
                    pd.to_numeric(
                        monthly["_SOC_VALUE"],
                        errors="coerce"
                    )
                    .fillna(0)
                )

                monthly["_SOL_VALUE"] = (
                    pd.to_numeric(
                        monthly["_SOL_VALUE"],
                        errors="coerce"
                    )
                    .fillna(0)
                )

                # ------------------------------------------------
                # GRAPH
                # ------------------------------------------------

                fig = go.Figure()

                # SOC
                fig.add_trace(
                    go.Scatter(
                        x=monthly["_MONTH"],
                        y=monthly["_SOC_VALUE"],
                        mode="lines+markers+text",
                        name="SOC Deviation",

                        # Show only non-zero values
                        text=[
                            str(int(v)) if v > 0 else ""
                            for v in monthly["_SOC_VALUE"]
                        ],

                        textposition="top center",
                        textfont=dict(size=11),

                        line=dict(
                            width=3
                        ),

                        marker=dict(
                            size=7
                        ),

                        hovertemplate=(
                            "<b>SOC</b><br>"
                            "Month: %{x}<br>"
                            "Deviation: %{y}"
                            "<extra></extra>"
                        )
                    )
                )

                # SOL
                fig.add_trace(
                    go.Scatter(
                        x=monthly["_MONTH"],
                        y=monthly["_SOL_VALUE"],
                        mode="lines+markers+text",
                        name="SOL Deviation",

                        # Show only non-zero values
                        text=[
                            str(int(v)) if v > 0 else ""
                            for v in monthly["_SOL_VALUE"]
                        ],

                        textposition="top center",
                        textfont=dict(size=11),

                        line=dict(
                            width=3,
                            dash="solid"
                        ),

                        marker=dict(
                            size=7
                        ),

                        hovertemplate=(
                            "<b>SOL</b><br>"
                            "Month: %{x}<br>"
                            "Deviation: %{y}"
                            "<extra></extra>"
                        )
                    )
                )

                fig.update_layout(
                    height=280,

                    margin=dict(
                        l=45,
                        r=20,
                        t=45,
                        b=45
                    ),

                    title=dict(
                        text=(
                            "MONTH-WISE DISTRIBUTION "
                            "OF SOC / SOL DEVIATION"
                        ),
                        x=0.5,
                        xanchor="center",
                        font=dict(
                            size=12,
                            color="#173f73"
                        )
                    ),

                    xaxis=dict(
                        title="Month",
                        categoryorder="array",
                        categoryarray=fy_months,
                        tickangle=-45,
                        showgrid=False
                    ),

                    yaxis=dict(
                        title="No. of Deviations",
                        rangemode="tozero",

                        # Extra space above highest value
                        range=[
                            0,
                            max(
                                monthly["_SOC_VALUE"].max(),
                                monthly["_SOL_VALUE"].max(),
                                1
                            ) + 1
                        ],

                        showgrid=True,
                        dtick=1
                    ),

                    legend=dict(
                        orientation="v",
                        x=0.78,
                        y=1.02,
                        xanchor="left",
                        yanchor="top",
                        font=dict(size=9),
                        bgcolor="rgba(255,255,255,0)"
                    ),

                    plot_bgcolor="white",
                    paper_bgcolor="white",

                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    },
                    key="bf_soc_sol_deviation_chart"
                )

# ============================================================
# 9 — AUDIT / COMPLIANCE
# ============================================================

with b:
    with st.container(
            border=True,
            height=460
    ):

        show_module_title(
            "",
            "",
            "AUDIT / COMPLIANCE"
        )

        # ========================================================
        # AUDIT KPI SUMMARY
        # ========================================================

        # TOTAL NO. OF AUDIT DONE = records with a valid Audit Date
        # PENDING FOR AUDIT = records without a valid Audit Date
        total_audit_done = 0
        pending_audit = 0

        if audit is not None and not audit.empty:
            audit_date_for_kpi = find_col(
                audit,
                [
                    "Audit Date",
                    "Last Audit Date",
                    "Date",
                ],
            )

            if audit_date_for_kpi:
                audit_dates = pd.to_datetime(
                    audit[audit_date_for_kpi],
                    errors="coerce",
                )
                total_audit_done = int(audit_dates.notna().sum())
                pending_audit = int(audit_dates.isna().sum())
            else:
                pending_audit = int(len(audit))

        ak1, ak2 = st.columns(2, gap="xxsmall")

        with ak1:
            show_kpi_card(
                "TOTAL NO. OF AUDIT DONE",
                total_audit_done
            )

        with ak2:
            show_kpi_card(
                "PENDING FOR AUDIT",
                pending_audit
            )

        # ========================================================
        # AUDIT / COMPLIANCE REGISTER
        # ========================================================

        st.markdown(
            '<div class="section-title">AUDIT / COMPLIANCE REGISTER</div>',
            unsafe_allow_html=True,
        )

        if audit is None or audit.empty:
            st.info("No audit records available.")
        else:
            audit_sno_col = find_col(
                audit,
                [
                    "S.No.",
                    "S.No",
                    "Sr No",
                    "Sr. No",
                    "Serial No",
                    "S No",
                ],
            )

            audit_dept_col = find_col(
                audit,
                [
                    "Department",
                    "Dept",
                    "Department Name",
                ],
            )

            audit_date_col = find_col(
                audit,
                [
                    "Audit Date",
                    "Last Audit Date",
                    "Date",
                ],
            )

            audit_score_col = find_col(
                audit,
                [
                    "Audit Score",
                    "Score",
                    "Audit Compliance",
                    "Compliance",
                    "Compliance %",
                    "Percentage",
                ],
            )

            # The live Google Sheet stores the uploaded audit files in the
            # separate "Audit Report" column (column E).
            audit_report_col = find_col(
                audit,
                [
                    "Audit Report",
                    "Audit Report Link",
                    "Report",
                ],
            )

            register_df = pd.DataFrame(index=audit.index)

            if audit_sno_col:
                register_df["S.No."] = audit[audit_sno_col].fillna("").astype(str).str.strip()
            else:
                register_df["S.No."] = range(1, len(audit) + 1)

            if audit_dept_col:
                register_df["Department"] = audit[audit_dept_col].fillna("").astype(str).str.strip()
            else:
                register_df["Department"] = ""

            if audit_date_col:
                register_df["Audit Date"] = audit[audit_date_col].fillna("").astype(str).str.strip()
            else:
                register_df["Audit Date"] = ""

            if audit_score_col:
                register_df["Audit Score"] = audit[audit_score_col].fillna("").astype(str).str.strip()
            else:
                register_df["Audit Score"] = ""

            # IMPORTANT:
            # The sheet screenshot shows the uploaded files under "Audit Report",
            # not under "Compliance Report". Keep the displayed file name from
            # the sheet and use the extracted live URL when one is available.
            if audit_report_col:
                register_df["Audit Report"] = (
                    audit[audit_report_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )
            else:
                register_df["Audit Report"] = ""

            if "__COMPLIANCE_REPORT_URL" in audit.columns:
                register_df["__REPORT_URL"] = (
                    audit["__COMPLIANCE_REPORT_URL"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )
            else:
                register_df["__REPORT_URL"] = ""

            # --------------------------------------------------------
            # AUDIT REPORT BUTTONS / FILE NAMES
            # --------------------------------------------------------
            rows_html = []

            for _, row in register_df.iterrows():
                report_name = str(row.get("Audit Report", "")).strip()
                report_url = str(row.get("__REPORT_URL", "")).strip()

                if report_url.startswith(("http://", "https://")):
                    report_cell = (
                        f'<a href="{report_url}" target="_blank" rel="noopener noreferrer" '
                        'style="display:inline-block;padding:4px 10px;'
                        'background:#07518b;color:#ffffff !important;border-radius:4px;'
                        'text-decoration:none;font-weight:700;font-size:9px;">'
                        'VIEW AUDIT REPORT ↗</a>'
                    )
                elif report_name and report_name.lower() not in {"nan", "none"}:
                    # Rich-text links from Google Sheets can sometimes lose the URL
                    # during export. Still show the actual report name instead of
                    # incorrectly displaying "Not attached".
                    report_cell = (
                        f'<span style="color:#0067c5;font-weight:700;font-size:9px;">'
                        f'{report_name}</span>'
                    )
                else:
                    report_cell = '<span style="color:#9aa7b3;font-size:9px;">Not attached</span>'

                rows_html.append(
                    f"""
                    <tr>
                        <td>{row['S.No.']}</td>
                        <td>{row['Department']}</td>
                        <td>{row['Audit Date']}</td>
                        <td>{row['Audit Score']}</td>
                        <td>{report_cell}</td>
                    </tr>
                    """
                )

            # Use a real HTML component so the live SharePoint/Google-sheet
            # hyperlink remains an actual clickable button.
            audit_table_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                html, body {{
                    margin:0; padding:0; background:transparent;
                    font-family:Arial, Helvetica, sans-serif;
                }}
                .audit-register-wrap {{
                    width:100%; max-height:400px; overflow-y:auto;
                    border:1px solid #d5e0e8; border-radius:4px;
                    background:#ffffff;
                }}
                table {{
                    width:100%; border-collapse:collapse; table-layout:fixed;
                    font-size:9px; color:#173f70;
                }}
                th {{
                    position:sticky; top:0; z-index:2;
                    background:#f3f7fa; color:#627689;
                    font-weight:800; text-align:left;
                    padding:5px 8px; border-bottom:1px solid #d5e0e8;
                    line-height:1.1;
                }}
                td {{
                    padding:5px 8px; border-bottom:1px solid #e1e8ee;
                    line-height:1.1;
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                }}
                th:nth-child(1), td:nth-child(1) {{ width:8%; }}
                th:nth-child(2), td:nth-child(2) {{ width:24%; }}
                th:nth-child(3), td:nth-child(3) {{ width:18%; }}
                th:nth-child(4), td:nth-child(4) {{ width:17%; }}
                th:nth-child(5), td:nth-child(5) {{ width:33%; }}
                .report-btn {{
                    display:inline-block; padding:4px 10px;
                    background:#07518b; color:#ffffff !important;
                    border-radius:4px; text-decoration:none !important;
                    font-weight:700; font-size:9px; cursor:pointer;
                }}
                .report-btn:hover {{ background:#063e70; }}
            </style>
            </head>
            <body>
                <div class="audit-register-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>S.No.</th>
                                <th>Department</th>
                                <th>Audit Date</th>
                                <th>Audit Score</th>
                                <th>Audit Report</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(rows_html)}
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """

            st.components.v1.html(
                audit_table_html,
                height=305,
                scrolling=False,
            )


# ============================================================
# 10 — INTERLOCK BYPASS
# ============================================================

with st.container(
        border=True,
        height=460
    ):

    show_module_title(
        "",
        "",
        "INTERLOCK BYPASS"
    )

    # ------------------------------------------------------------
    # PREPARE LIVE INTERLOCK REGISTER
    # ------------------------------------------------------------

    interlock_data = clean_dataframe(interlock)

    sno_col = find_col(
        interlock_data,
        ["S.No.", "S No", "S.No", "Serial No", "Sr No", "Sr. No."]
    )
    department_col = find_col(
        interlock_data,
        ["Department", "Departments", "Dept", "Department Name"]
    )
    description_col = find_col(
        interlock_data,
        ["Interlock Description", "Interlock Details", "Description"]
    )
    bypassed_date_col = find_col(
        interlock_data,
        ["Date Bypassed", "Bypassed Date", "Date of Bypass"]
    )
    status_col = find_col(
        interlock_data,
        [
            "Present Status / Action Required",
            "Present Status",
            "Status / Action Required",
            "Status",
        ]
    )

    if interlock_data.empty:
        pending_interlock = pd.DataFrame()

    else:
        # Keep only actual register rows using S.No.
        if sno_col:
            sno_numeric = pd.to_numeric(
                interlock_data[sno_col],
                errors="coerce",
            )
            valid_rows = sno_numeric.notna()
            interlock_data = interlock_data.loc[valid_rows].copy()

            # Protect against accidental duplicate rows from the source.
            interlock_data["__sno_numeric"] = sno_numeric.loc[valid_rows]
            interlock_data = (
                interlock_data
                .drop_duplicates(subset=["__sno_numeric"], keep="first")
                .drop(columns=["__sno_numeric"])
            )

        # Only records currently due for normalization are pending.
        if status_col:
            status_values = (
                interlock_data[status_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            pending_mask = status_values.str.contains(
                r"due\s*for\s*normalization|normalization\s*pending",
                case=False,
                regex=True,
                na=False,
            )
            pending_interlock = interlock_data.loc[pending_mask].copy()
        else:
            pending_interlock = interlock_data.copy()

    pending_count = len(pending_interlock)

    # ------------------------------------------------------------
    # KPI
    # ------------------------------------------------------------
    show_kpi_card(
        "NORMALIZATION PENDING",
        f"{pending_count:,}",
    )

    # ------------------------------------------------------------
    # CHART + REGISTER SIDE BY SIDE
    # ------------------------------------------------------------
    chart_col, register_col = st.columns([1.05, 1.95], gap="small")

    with chart_col:
        st.markdown(
            '<div class="section-bar">'
            'Pending for Normalization by Department'
            '</div>',
            unsafe_allow_html=True,
        )

        if pending_interlock.empty:
            st.info("No interlock is pending for normalization.")

        else:
            if department_col:
                department_values = (
                    pending_interlock[department_col]
                    .fillna("Unknown")
                    .astype(str)
                    .str.strip()
                    .replace("", "Unknown")
                )

                department_counts = (
                    pd.DataFrame({"Department": department_values})
                    .groupby("Department", as_index=False)
                    .size()
                    .rename(columns={"size": "Pending"})
                )
            else:
                department_counts = pd.DataFrame(
                    {
                        "Department": ["Unknown"],
                        "Pending": [pending_count],
                    }
                )

            fig_interlock = go.Figure(
                data=[
                    go.Pie(
                        labels=department_counts["Department"],
                        values=department_counts["Pending"],
                        hole=0.56,
                        textinfo="value",
                        textposition="inside",
                        domain=dict(x=[0.00, 0.58], y=[0.00, 1.00]),
                        insidetextorientation="horizontal",
                    )
                ]
            )

            fig_interlock.update_layout(
                height=394,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="white",
                plot_bgcolor="white",
                legend=dict(
                    orientation="v",
                    x=0.62,
                    y=0.5,
                    xanchor="left",
                    yanchor="middle",
                    font=dict(size=9),
                ),
                annotations=[
                    dict(
                        text=f"<b>{pending_count}</b><br>Pending",
                        x=0.29,
                        y=0.50,
                        xref="paper",
                        yref="paper",
                        xanchor="center",
                        yanchor="middle",
                        showarrow=False,
                        font=dict(size=16),
                    )
                ],
            )

            st.plotly_chart(
                fig_interlock,
                use_container_width=True,
                config={"displayModeBar": False},
                key="all_department_interlock_donut",
            )

    with register_col:
        st.markdown(
            '<div class="section-bar">'
            'Interlock Bypass Register - Normalization Pending'
            '</div>',
            unsafe_allow_html=True,
        )

        if pending_interlock.empty:
            st.info("No interlock bypass is pending for normalization.")

        else:
            register_df = pd.DataFrame(index=pending_interlock.index)

            if sno_col:
                register_df["S.No."] = pd.to_numeric(
                    pending_interlock[sno_col],
                    errors="coerce",
                ).astype("Int64")
            else:
                register_df["S.No."] = range(1, len(pending_interlock) + 1)

            if department_col:
                register_df["Department"] = (
                    pending_interlock[department_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )
            else:
                register_df["Department"] = ""

            if description_col:
                register_df["Interlock Description"] = (
                    pending_interlock[description_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )
            else:
                register_df["Interlock Description"] = ""

            if bypassed_date_col:
                raw_dates = pd.to_datetime(
                    pending_interlock[bypassed_date_col],
                    errors="coerce",
                    dayfirst=True,
                )
            else:
                raw_dates = pd.Series(
                    pd.NaT,
                    index=pending_interlock.index,
                )

            today = pd.Timestamp(datetime.now(ZoneInfo("Asia/Kolkata")).date())
            days_open = (today - raw_dates.dt.normalize()).dt.days

            register_df["Date Bypassed"] = (
                raw_dates.dt.strftime("%d-%b-%Y").fillna("-")
            )
            register_df["Days Open"] = days_open.fillna(0).astype(int)

            register_df = register_df.sort_values(
                "Days Open",
                ascending=False,
            )

            st.dataframe(
                register_df,
                use_container_width=True,
                hide_index=True,
                height=394,
                column_config={
                    "S.No.": st.column_config.NumberColumn(
                        "S.No.",
                        format="%d",
                    ),
                    "Department": st.column_config.TextColumn(
                        "Department"
                    ),
                    "Interlock Description": st.column_config.TextColumn(
                        "Interlock Description"
                    ),
                    "Date Bypassed": st.column_config.TextColumn(
                        "Date Bypassed"
                    ),
                    "Days Open": st.column_config.NumberColumn(
                        "Days Open",
                        format="%d",
                    ),
                },
            )

# ============================================================
# 11 — PSM CE
# ============================================================

with st.container(border=True):

    show_module_title(
        "",
        "",
        "PSM CRITICAL EQUIPMENT NOTIFICATION"
    )

    psm_ce_data = clean_dataframe(psm_ce)

    # Actual Google Sheet columns.
    failed_col = find_col(
        psm_ce_data,
        [
            "No. of PSM CE failed (Breakdown)",
            "No. Of PSM CE Failed (Breakdown)",
            "PSM CE Failed",
            "PSM CE Failed (Breakdown)",
        ],
    )
    mech_generated_col = find_col(
        psm_ce_data,
        [
            "Compliance of PSM CE MO – Mechanical – Generated",
            "Compliance of PSM CE MO - Mechanical - Generated",
            "PSM CE MO Mechanical Generated",
        ],
    )
    mech_completed_col = find_col(
        psm_ce_data,
        [
            "Compliance of PSM CE MO – Mechanical – Completed",
            "Compliance of PSM CE MO - Mechanical - Completed",
            "PSM CE MO Mechanical Completed",
        ],
    )
    ei_generated_col = find_col(
        psm_ce_data,
        [
            "Compliance of PSM CE MO – E&I – Generated",
            "Compliance of PSM CE MO - E&I - Generated",
            "PSM CE MO E&I Generated",
        ],
    )
    ei_completed_col = find_col(
        psm_ce_data,
        [
            "Compliance of PSM CE MO – E&I – Completed",
            "Compliance of PSM CE MO - E&I - Completed",
            "PSM CE MO E&I Completed",
        ],
    )

    def numeric_total(df, column):
        if column is None or df.empty:
            return 0
        return int(
            pd.to_numeric(df[column], errors="coerce")
            .fillna(0)
            .sum()
        )

    total_psm_ce_failed = numeric_total(psm_ce_data, failed_col)
    mech_generated = numeric_total(psm_ce_data, mech_generated_col)
    mech_completed = numeric_total(psm_ce_data, mech_completed_col)
    ei_generated = numeric_total(psm_ce_data, ei_generated_col)
    ei_completed = numeric_total(psm_ce_data, ei_completed_col)

    # Short dashboard labels.
    show_metric_row([
        ("TOTAL PSM CE FAILED", total_psm_ce_failed),
        ("MECHANICAL-MAINTENANCE ORDER GENERATED", mech_generated),
        ("MECHANICAL-MAINTENANCE ORDER COMPLETED", mech_completed),
        ("E&I-MAINTENANCE ORDER GENERATED", ei_generated),
        ("E&I-MAINTENANCE ORDER COMPLETED", ei_completed),
    ])

    # --------------------------------------------------------
    # DEPARTMENT-WISE PSM CE COMPLETION PROGRESS
    # --------------------------------------------------------
    dept_col_progress = find_col(psm_ce_data, ["Department", "Dept"])
    if not psm_ce_data.empty and dept_col_progress is not None:
        progress_df = pd.DataFrame({
            "Department": psm_ce_data[dept_col_progress].fillna("").astype(str).str.strip(),
            "M Generated": pd.to_numeric(psm_ce_data[mech_generated_col], errors="coerce").fillna(0) if mech_generated_col else 0,
            "M Completed": pd.to_numeric(psm_ce_data[mech_completed_col], errors="coerce").fillna(0) if mech_completed_col else 0,
            "E&I Generated": pd.to_numeric(psm_ce_data[ei_generated_col], errors="coerce").fillna(0) if ei_generated_col else 0,
            "E&I Completed": pd.to_numeric(psm_ce_data[ei_completed_col], errors="coerce").fillna(0) if ei_completed_col else 0,
        })
        progress_df = (
            progress_df.groupby("Department", as_index=False)[
                ["M Generated", "M Completed", "E&I Generated", "E&I Completed"]
            ].sum()
        )
        progress_df = progress_df[progress_df["Department"].str.strip() != ""]

        if not progress_df.empty:
            st.markdown(
                '<div class="section-bar">PSM CE Completion Progress by Department</div>',
                unsafe_allow_html=True,
            )

            def progress_color(pct):
                # Completion status: red < 50%, amber 50-79%, green >= 80%.
                if pct < 50:
                    return "#e53935"
                if pct < 80:
                    return "#f5a623"
                return "#2e9d50"

            progress_rows = []
            for _, r in progress_df.iterrows():
                m_gen = float(r["M Generated"])
                m_comp = float(r["M Completed"])
                ei_gen = float(r["E&I Generated"])
                ei_comp = float(r["E&I Completed"])

                m_pct = (100.0 if m_gen <= 0 and m_comp > 0 else
                         0.0 if m_gen <= 0 else min(100.0, max(0.0, m_comp / m_gen * 100.0)))
                ei_pct = (100.0 if ei_gen <= 0 and ei_comp > 0 else
                          0.0 if ei_gen <= 0 else min(100.0, max(0.0, ei_comp / ei_gen * 100.0)))

                m_color = progress_color(m_pct)
                ei_color = progress_color(ei_pct)

                progress_rows.append(
                    f'<div style="display:grid;grid-template-columns:180px 1fr 52px 1fr 52px;gap:10px;align-items:center;margin:5px 0;font-family:Arial,sans-serif;font-size:10px;color:#173f70;">'
                    f'<div style="font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{r["Department"]}</div>'
                    f'<div style="height:9px;background:#e8eef3;border-radius:8px;overflow:hidden;"><div style="width:{m_pct:.1f}%;height:100%;background:{m_color};border-radius:8px;"></div></div>'
                    f'<div style="font-weight:700;text-align:right;color:{m_color};">M {m_pct:.0f}%</div>'
                    f'<div style="height:9px;background:#e8eef3;border-radius:8px;overflow:hidden;"><div style="width:{ei_pct:.1f}%;height:100%;background:{ei_color};border-radius:8px;"></div></div>'
                    f'<div style="font-weight:700;text-align:right;color:{ei_color};">E&I {ei_pct:.0f}%</div>'
                    f'</div>'
                )

            progress_html = (
                '<div style="background:#fff;border:1px solid #d5e0e8;border-radius:5px;padding:8px 12px;">'
                '<div style="display:grid;grid-template-columns:180px 1fr 52px 1fr 52px;gap:10px;align-items:center;'
                'font-family:Arial,sans-serif;font-size:9px;font-weight:800;color:#627689;margin-bottom:6px;">'
                '<div>Department</div><div>MECHANICAL MAINTENANCE ORDER</div><div></div><div>E&I MAINTENANCE ORDER</div><div></div>'
                '</div>'
                + ''.join(progress_rows)
                + '</div>'
            )
            st.markdown(progress_html, unsafe_allow_html=True)


# ============================================================
# ROW 5 — BARRIER AUDIT + FAILURE DATA
# ============================================================

barrier_col, failure_col = st.columns(
    [1, 1],
    gap="small"
)

# ============================================================
# ROW 5 — BARRIER AUDIT + FAILURE DATA
# ============================================================

barrier_col, failure_col = st.columns(
    [1, 1],
    gap="small"
)

# ============================================================
# ROW 5 — BARRIER AUDIT + FAILURE DATA
# ============================================================

barrier_col, failure_col = st.columns(
    [1, 1],
    gap="small"
)

# ============================================================
# 12 — BARRIER AUDIT
# ============================================================

with barrier_col:
    with st.container(border=True, height=520):

        show_module_title(
            "",
            "",
            "(C4/C5)BARRIER AUDIT"
        )

        barrier_data = (
            clean_dataframe(loaded.get("Barrier Audit"))
            if loaded.get("Barrier Audit") is not None
            else pd.DataFrame()
        )

        if barrier_data.empty:
            st.info("No Barrier Audit data available.")

        else:
            # ----------------------------------------------------
            # COLUMN DETECTION
            # ----------------------------------------------------
            month_col = find_col(
                barrier_data,
                ["Month"]
            )

            dept_col = find_col(
                barrier_data,
                ["Department", "Dept"]
            )

            plan_col = find_col(
                barrier_data,
                [
                    "Barrier Audit Conducted (Plan)",
                    "Barrier Audit Conducted Plan",
                ],
            )

            actual_col = find_col(
                barrier_data,
                [
                    "Barrier Audit Conducted (Actual)",
                    "Barrier Audit Conducted Actual",
                ],
            )

            assessed_col = find_col(
                barrier_data,
                [
                    "Barrier Health (C4/C5) (Number) Assessed",
                    "Assessed",
                ],
            )

            unacceptable_col = find_col(
                barrier_data,
                [
                    "Barrier Health (C4/C5) (Number) Unacceptable",
                    "Unacceptable Barrier",
                    "Unacceptable",
                ],
            )

            # ----------------------------------------------------
            # APPLY EXISTING GLOBAL DEPARTMENT SELECTION
            # No separate filter is created inside this module.
            # ----------------------------------------------------
            barrier_display = barrier_data.copy()


            # ----------------------------------------------------
            # TOTAL ASSESSED / UNACCEPTABLE
            # ----------------------------------------------------
            total_assessed = (
                int(
                    pd.to_numeric(
                        barrier_display[assessed_col],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                )
                if assessed_col and not barrier_display.empty
                else 0
            )

            total_unacceptable = (
                int(
                    pd.to_numeric(
                        barrier_display[unacceptable_col],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                )
                if unacceptable_col and not barrier_display.empty
                else 0
            )

            # ----------------------------------------------------
            # KPI — BARRIER HEALTH
            # ----------------------------------------------------
            show_metric_row([
                (
                    "BARRIER HEALTH ASSESSED",
                    total_assessed
                ),
                (
                    "BARRIER HEALTH UNACCEPTABLE",
                    total_unacceptable
                ),
            ])

            # ====================================================
            # GRAPH — BARRIER AUDIT CONDUCTED
            # MONTH-WISE PLAN VS ACTUAL
            # ====================================================
            if month_col and not barrier_display.empty:

                monthly_audit = pd.DataFrame()

                monthly_audit["Month"] = (
                    barrier_display[month_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                monthly_audit["Plan"] = (
                    pd.to_numeric(
                        barrier_display[plan_col],
                        errors="coerce"
                    ).fillna(0)
                    if plan_col
                    else 0
                )

                monthly_audit["Actual"] = (
                    pd.to_numeric(
                        barrier_display[actual_col],
                        errors="coerce"
                    ).fillna(0)
                    if actual_col
                    else 0
                )

                monthly_audit = monthly_audit[
                    monthly_audit["Month"] != ""
                ]

                # Sum values month-wise
                monthly_audit = (
                    monthly_audit
                    .groupby("Month", as_index=False)[
                        ["Plan", "Actual"]
                    ]
                    .sum()
                )

                if not monthly_audit.empty:

                    # Keep chronological month order where possible
                    month_order = [
                        "Jan-26", "Feb-26", "Mar-26",
                        "Apr-26", "May-26", "Jun-26",
                        "Jul-26", "Aug-26", "Sep-26",
                        "Oct-26", "Nov-26", "Dec-26"
                    ]

                    monthly_audit["_sort"] = (
                        monthly_audit["Month"]
                        .apply(
                            lambda x:
                            month_order.index(x)
                            if x in month_order
                            else 999
                        )
                    )

                    monthly_audit = (
                        monthly_audit
                        .sort_values("_sort")
                        .drop(columns="_sort")
                    )

                    # ------------------------------------------------
                    # PLOTLY BAR CHART
                    # ------------------------------------------------
                    fig_monthly = go.Figure()

                    fig_monthly.add_trace(
                        go.Bar(
                            x=monthly_audit["Month"],
                            y=monthly_audit["Plan"],
                            name="Plan",
                            marker_color="#4f97d1",
                            text=monthly_audit["Plan"].astype(int),
                            textposition="outside",
                            cliponaxis=False,
                        )
                    )

                    fig_monthly.add_trace(
                        go.Bar(
                            x=monthly_audit["Month"],
                            y=monthly_audit["Actual"],
                            name="Actual",
                            marker_color="#f5c542",
                            text=monthly_audit["Actual"].astype(int),
                            textposition="outside",
                            cliponaxis=False,
                        )
                    )

                    fig_monthly.update_layout(
                        title=dict(
                            text="BARRIER AUDIT CONDUCTED (PLAN VS ACTUAL)",
                            x=0,
                            xanchor="left",
                            font=dict(
                                size=15,
                                color="#173f70"
                            ),
                        ),

                        barmode="group",

                        height=300,

                        margin=dict(
                            l=45,
                            r=20,
                            t=55,
                            b=50
                        ),

                        font=dict(
                            size=9,
                            color="#173f70"
                        ),

                        legend=dict(
                            orientation="h",
                            y=1.08,
                            x=1,
                            xanchor="right",
                            yanchor="bottom",
                            font=dict(size=9),
                        ),

                        xaxis=dict(
                            title="Month",
                            title_font=dict(size=10),
                            tickfont=dict(size=9),
                            showgrid=False,
                        ),

                        yaxis=dict(
                            title="Number of Audits",
                            title_font=dict(size=10),
                            tickfont=dict(size=9),
                            rangemode="tozero",
                            gridcolor="#e5edf4",
                            dtick=5,
                        ),

                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )

                    st.plotly_chart(
                        fig_monthly,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                    )

                else:
                    st.info(
                        "No monthly Barrier Audit data available."
                    )


# ============================================================
# 13 — FAILURE DATA
# ============================================================

with failure_col:
    with st.container(border=True, height=520):

        show_module_title(
            "",
            "",
            "PSM CRITICAL EQUIPMENT/BARRIER (C4/C5)FAILURE DETAILS"
        )

        failure_df = clean_dataframe(failure_data)

        if failure_df.empty:
            st.info("No Failure Data available.")
        else:
            f_dept_col = find_col(failure_df, ["Department", "Dept"])
            f_month_col = find_col(failure_df, ["Month"])
            f_type_col = find_col(
                failure_df,
                ["PSM CE/Barrier", "PSM CE / Barrier", "PSM CE-Barriers"],
            )
            f_name_col = find_col(failure_df, ["Name"])
            f_reason_col = find_col(
                failure_df,
                ["Reason of Failure", "Failure Reason"],
            )

            failure_register = pd.DataFrame(index=failure_df.index)
            failure_register["Department"] = failure_df[f_dept_col] if f_dept_col else "-"
            failure_register["Month"] = failure_df[f_month_col] if f_month_col else "-"
            failure_register["PSM CE/Barrier"] = failure_df[f_type_col] if f_type_col else "-"
            failure_register["Name"] = failure_df[f_name_col] if f_name_col else "-"
            failure_register["Reason of Failure"] = failure_df[f_reason_col] if f_reason_col else "-"

            # ----------------------------------------------------
            # TOTAL FAILURE COUNTS — KEEP AT TOP
            # ----------------------------------------------------
            type_counts = {"PSM CE": 0, "Barrier": 0}
            if f_type_col:
                type_series = failure_df[f_type_col].astype(str).str.strip().str.lower()
                type_counts["PSM CE"] = int((type_series == "psm ce").sum())
                type_counts["Barrier"] = int((type_series == "barrier").sum())

            total_psm_ce = type_counts["PSM CE"]
            total_barrier = type_counts["Barrier"]
            total_psm_col, total_barrier_col = st.columns(2, gap="xxsmall")

            with total_psm_col:
                show_kpi_card(
                    "PSM CE",
                    total_psm_ce
                )

            with total_barrier_col:
                show_kpi_card(
                    "BARRIER",
                    total_barrier
                )

            # ----------------------------------------------------
            # GRAPHICAL REPRESENTATION — FAILURE COUNT
            # ----------------------------------------------------
            failure_chart_col_1, failure_chart_col_2 = st.columns([0.88, 1.12], gap="small")



            def highlight_failure_type(value):
                text = str(value).strip().lower()
                if text == "psm ce":
                    return "background-color: #dbeafe; color: #173f70; font-weight: 700;"
                if text == "barrier":
                    return "background-color: #fff1cc; color: #8a5a00; font-weight: 700;"
                return ""

            failure_styled = failure_register.style.map(
                highlight_failure_type,
                subset=["PSM CE/Barrier"],
            )

            st.markdown(
                '<div class="section-bar">Failure Data Register</div>',
                unsafe_allow_html=True,
            )

            # Keep the table only as tall as its actual rows so there is no
            # unnecessary blank area inside the Failure Data table.
            failure_table_height = min(330, max(100, 38 * (len(failure_register) + 1) + 8))

            st.dataframe(
                failure_styled,
                use_container_width=True,
                hide_index=True,
                height=failure_table_height,
                column_config={
                    "Department": st.column_config.TextColumn("Department"),
                    "Month": st.column_config.TextColumn("Month"),
                    "PSM CE/Barrier": st.column_config.TextColumn("PSM CE/Barrier"),
                    "Name": st.column_config.TextColumn("Name"),
                    "Reason of Failure": st.column_config.TextColumn("Reason of Failure"),
                },
            )
