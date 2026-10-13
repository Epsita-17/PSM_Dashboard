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
    padding: 0.2rem 1.25rem 0.5rem 1.25rem !important;
    margin-top: 0 !important;
    overflow: visible !important;
}

    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    iframe {
        display: block !important;
        margin-top: -65px !important;
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



import html
import re
import time
from pathlib import Path
from urllib.parse import quote
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components

# ============================================================ 
# CONFIGURATION 
# ============================================================ 

st.set_page_config(
    page_title="JSAP Audit Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
SHEET_NAME = "JSAP"
REGISTER_SHEET_NAME = "psm_data"
REGISTER_GID = "823112064"
REFRESH_SECONDS = 60

SERVICE_ACCOUNT_FILE = (
        Path(__file__).resolve().parent / "service_account.json"
)

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={quote(SHEET_NAME)}"
)

# ============================================================ 
# PAGE STYLING 
# ============================================================ 

st.markdown(
    """ 
    <style> 
    html, body, [data-testid="stAppViewContainer"] { 
        background: #FFFFFF !important; 
        color: #10377D !important; 
    } 

    [data-testid="stHeader"] { 
        background: #FFFFFF !important; 
        height: 0 !important; 
        min-height: 0 !important; 
    } 

    [data-testid="stToolbar"], 
    [data-testid="stDecoration"], 
    footer { 
        display: none !important; 
    } 

    /* Prevent the page title from being clipped at the top. */ 
    .block-container { 
        width: 100% !important; 
        max-width: 1900px !important; 
        padding: 2.5rem 1.25rem 1rem 1.25rem !important; 
        margin-top: 0 !important; 
        overflow: visible !important; 
    } 

    .section-title { 
        color: #10377D; 
        font-family: Arial, sans-serif; 
        font-size: 27px; 
        font-weight: 800; 
        line-height: 1.4; 
        margin: 0; 
        padding: 2px 0 0 0; 
        overflow: visible; 
    } 

    .red-underline { 
        width: 150px; 
        height: 5px; 
        background: #F5223B; 
        margin-top: 8px; 
        margin-bottom: 15px; 
    } 

    [data-testid="stAlert"] { 
        border-radius: 10px; 
    } 

    /* Avoid clipping content in Streamlit's layout containers. */ 
    [data-testid="stVerticalBlock"], 
    [data-testid="stHorizontalBlock"], 
    [data-testid="column"] { 
        overflow: visible !important; 
    } 

    @media (max-width: 1000px) { 
        .block-container { 
            padding: 1.8rem 0.6rem 1rem 0.6rem !important; 
        } 

        .section-title { 
            font-size: 23px; 
        } 
    } 
    </style> 
    """,
    unsafe_allow_html=True,
)

# ============================================================ 
# SCORE MATRIX CARDS 
# ============================================================ 

SCORE_LEVELS = [
    ("< 40%", "Not Acceptable", "#F5224A", "#FFF0F3", "#FFC2D0"),
    ("40 – 59%", "Developing", "#E94C25", "#FFF0E9", "#FFC6B5"),
    ("60 – 79%", "Acceptable", "#8B7516", "#FFF9DF", "#FFE78A"),
    ("80 – 89%", "Mature", "#1762BC", "#EBF4FF", "#BBD9FF"),
    ("90 – 99%", "Leading", "#21845D", "#EAF7F0", "#BCE5D0"),
    ("100%", "Best Practice", "#21845D", "#EDF7F1", "#BCE5D0"),
]


def render_score_matrix():
    cards = ""

    for score_range, label, color, background, border in SCORE_LEVELS:
        cards += f""" 
        <div class="score-card" 
             style="color:{color}; 
                    background:{background}; 
                    border-color:{border};"> 
            <strong>{html.escape(score_range)}</strong> 
            <span>{html.escape(label)}</span> 
        </div> 
        """

    page = f""" 
    <!DOCTYPE html> 
    <html> 
    <head> 
    <meta charset="UTF-8"> 
    <style> 
        * {{ box-sizing: border-box; }} 

        html, body {{ 
            width: 100%; 
            height: 100%; 
            margin: 0; 
            background: #FFFFFF; 
            font-family: Arial, sans-serif; 
            overflow: hidden; 
        }} 

        body {{ 
            padding-top: 60px; 
        }} 

        .matrix {{ 
            display: flex; 
            flex-wrap: nowrap; 
            justify-content: flex-end; 
            align-items: stretch; 
            gap: 6px; 
            width: 100%; 
        }} 

        .score-card {{ 
            flex: 1 1 0; 
            min-width: 0; 
            height: 50px; 
            padding: 5px 3px; 
            border: 1px solid; 
            border-radius: 11px; 
            text-align: center; 
            line-height: 1.35; 
        }} 

        .score-card strong {{ 
            display: block; 
            font-size: 12px; 
            font-weight: 800; 
            white-space: nowrap; 
        }} 

        .score-card span {{ 
            display: block; 
            font-size: 11px; 
            white-space: nowrap; 
        }} 

        @media(max-width: 650px) {{ 
            body {{ padding-top: 12px; }} 

            .matrix {{ 
                flex-wrap: wrap; 
            }} 

            .score-card {{ 
                flex: 1 1 28%; 
                height: 50px; 
            }} 

            .score-card span {{ 
                white-space: normal; 
            }} 
        }} 
    </style> 
    </head> 
    <body> 
        <div class="matrix">{cards}</div> 
    </body> 
    </html> 
    """

    components.html(page, height=115, scrolling=False)


# ============================================================ 
# GOOGLE SHEETS ACCESS 
# ============================================================ 

def extract_url(cell):
    """Extract report links from Google Sheets cell metadata."""

    url = cell.get("hyperlink", "")
    if url:
        return url

    url = (
        cell.get("userEnteredFormat", {})
        .get("textFormat", {})
        .get("link", {})
        .get("uri", "")
    )
    if url:
        return url

    for run in cell.get("textFormatRuns", []):
        url = (
            run.get("format", {})
            .get("link", {})
            .get("uri", "")
        )
        if url:
            return url

    formula = (
        cell.get("userEnteredValue", {})
        .get("formulaValue", "")
    )

    if formula:
        match = re.search(
            r'HYPERLINK\(\s*"((?:[^"]|"")*)"',
            formula,
            flags=re.IGNORECASE,
        )
        if match:
            return match.group(1).replace('""', '"')

    value = cell.get("formattedValue", "").strip()

    if value.startswith(("https://", "http://")):
        return value

    return ""


def load_from_google_api():
    """Fetch Google Sheets values and rich-text hyperlinks."""

    try:
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import AuthorizedSession
    except ImportError as exc:
        raise RuntimeError(
            "Google authentication packages are missing. Install them in "
            "the active project interpreter with: "
            "python -m pip install --upgrade google-auth requests pandas"
        ) from exc

    if not SERVICE_ACCOUNT_FILE.is_file():
        raise FileNotFoundError(
            f"Service account file not found: {SERVICE_ACCOUNT_FILE}"
        )

    credentials = Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ],
    )

    session = AuthorizedSession(credentials)

    fields = (
        "sheets(properties(title),data("
        "rowData(values("
        "formattedValue,hyperlink,userEnteredValue,"
        "userEnteredFormat(textFormat(link(uri))),"
        "textFormatRuns(format(link(uri)))"
        "))))"
    )

    response = session.get(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}",
        params={
            "includeGridData": "true",
            "fields": fields,
        },
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        timeout=30,
    )
    response.raise_for_status()
    workbook = response.json()

    sheet = next(
        (
            item
            for item in workbook.get("sheets", [])
            if item.get("properties", {}).get("title") == SHEET_NAME
        ),
        None,
    )

    if sheet is None:
        raise ValueError(f'Worksheet "{SHEET_NAME}" was not found.')

    grid_data = sheet.get("data", [])
    raw_rows = grid_data[0].get("rowData", []) if grid_data else []

    if not raw_rows:
        raise ValueError("The JSAP worksheet is empty.")

    headers = [
        cell.get("formattedValue", "").strip()
        for cell in raw_rows[0].get("values", [])
    ]
    headers = [
        name if name else f"Unnamed_{i}"
        for i, name in enumerate(headers)
    ]

    records = []
    link_records = []

    for row in raw_rows[1:]:
        cells = row.get("values", [])
        values = []
        urls = []

        for i in range(len(headers)):
            cell = cells[i] if i < len(cells) else {}
            values.append(cell.get("formattedValue", ""))
            urls.append(extract_url(cell))

        records.append(values)
        link_records.append(urls)

    return (
        pd.DataFrame(records, columns=headers),
        pd.DataFrame(link_records, columns=headers),
    )

def load_from_public_csv():
    """Read the link-accessible Google Sheet as CSV."""

    url = f"{CSV_URL}&_refresh={time.time_ns()}"

    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    response.raise_for_status()

    # BytesIO is accepted by pandas and avoids editor type-inference issues
    # sometimes reported for StringIO(response.text).
    from io import BytesIO

    csv_buffer = BytesIO(response.content)
    df = pd.read_csv(
        csv_buffer,
        dtype=str,
        keep_default_na=False,
    )

    links_df = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns,
    )

    for column in df.columns:
        links_df[column] = df[column].apply(
            lambda value: (
                str(value).strip()
                if str(value).strip().startswith(("https://", "http://"))
                else ""
            )
        )

    return df, links_df

def load_sheet():
    if SERVICE_ACCOUNT_FILE.exists():
        return load_from_google_api()

    return load_from_public_csv()


# ============================================================
# PSM OBSERVATION REGISTER
# ============================================================

def load_register_data():
    """Load the psm_data register and its report hyperlinks."""
    if SERVICE_ACCOUNT_FILE.is_file():
        try:
            from google.oauth2.service_account import Credentials
            from google.auth.transport.requests import AuthorizedSession
        except ImportError as exc:
            raise RuntimeError(
                "Google authentication packages are missing. Install them with: "
                "python -m pip install --upgrade google-auth requests pandas"
            ) from exc

        credentials = Credentials.from_service_account_file(
            str(SERVICE_ACCOUNT_FILE),
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )
        session = AuthorizedSession(credentials)
        fields = (
            "sheets(properties(title),data(rowData(values("
            "formattedValue,hyperlink,userEnteredValue,"
            "userEnteredFormat(textFormat(link(uri))),"
            "textFormatRuns(format(link(uri)))"
            ")))))"
        )
        response = session.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}",
            params={"includeGridData": "true", "fields": fields},
            timeout=30,
        )
        response.raise_for_status()
        workbook = response.json()
        target = normalize(REGISTER_SHEET_NAME)
        sheet = next(
            (
                item for item in workbook.get("sheets", [])
                if normalize(item.get("properties", {}).get("title", "")) == target
            ),
            None,
        )
        if sheet is None:
            raise ValueError(
                f'Worksheet "{REGISTER_SHEET_NAME}" was not found in the spreadsheet.'
            )

        grid_data = sheet.get("data", [])
        raw_rows = grid_data[0].get("rowData", []) if grid_data else []
        if not raw_rows:
            return pd.DataFrame(), pd.DataFrame()

        headers = [
            cell.get("formattedValue", "").strip()
            for cell in raw_rows[0].get("values", [])
        ]
        headers = [name if name else f"Unnamed_{i}" for i, name in enumerate(headers)]
        records, link_records = [], []
        for row in raw_rows[1:]:
            cells = row.get("values", [])
            values, urls = [], []
            for i in range(len(headers)):
                cell = cells[i] if i < len(cells) else {}
                values.append(cell.get("formattedValue", ""))
                urls.append(extract_url(cell))
            records.append(values)
            link_records.append(urls)
        return (
            pd.DataFrame(records, columns=headers),
            pd.DataFrame(link_records, columns=headers),
        )

    # Public-CSV fallback uses the exact worksheet gid shown in the supplied screenshot.
    url = (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:csv&gid={REGISTER_GID}&_refresh={time.time_ns()}"
    )
    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    response.raise_for_status()
    from io import BytesIO
    df = pd.read_csv(BytesIO(response.content), dtype=str, keep_default_na=False)
    links_df = pd.DataFrame("", index=df.index, columns=df.columns)
    for column in df.columns:
        links_df[column] = df[column].apply(
            lambda value: str(value).strip()
            if str(value).strip().startswith(("https://", "http://"))
            else ""
        )
    return df, links_df


def render_psm_register():
    """Show PSM observation KPIs, department filter, and register table."""
    st.markdown(
        """
        <div style="height:8px;"></div>
        <div class="section-title">JSAP AUDIT OBSERVATIONS</div>
        <div class="red-underline"></div>
        """,
        unsafe_allow_html=True,
    )

    try:
        register_df, register_links = load_register_data()
    except Exception as exc:
        st.warning("The PSM observation register could not be loaded.")
        st.caption(f"{type(exc).__name__}: {exc}")
        return

    if register_df.empty:
        st.info("No records are available in the psm_data worksheet.")
        return

    # Use the expected register headings, with column-position fallbacks
    # matching the supplied sheet: A=S. No., C=Severity, D=Department, E=Compliance.
    def source_column(candidates, position):
        found = find_column(register_df, candidates)
        if found is not None:
            return found
        if len(register_df.columns) > position:
            return register_df.columns[position]
        return None

    serial_col = source_column(["S. No.", "S No", "Serial No", "S.No.", "Serial Number"], 0)
    observation_col = source_column(["Observation", "Observations"], 1)
    severity_col = source_column(["Severity", "Risk Level"], 2)
    department_col = source_column(["Department", "Dept"], 3)
    compliance_col = source_column(["Compliance", "Compliant", "Compliance Status"], 4)
    report_col = source_column(
        ["Compliance Report", "Compliance Rep", "Report", "Report Link"], 5
    )

    # Department filter applies to both the KPIs and the displayed register.
    departments = []
    if department_col is not None:
        departments = sorted(
            {
                cell_text(value)
                for value in register_df[department_col]
                if cell_text(value)
            },
            key=str.casefold,
        )

    # The first option shows the complete register; the remaining options
    # let users filter to any individual department.
    filter_col, spacer_col = st.columns([1.15, 3.85], gap="small")
    with filter_col:
        selected_department = st.selectbox(
            "Filter by Department",
            options=["All Departments"] + departments,
            index=0,
            key="psm_register_department_filter",
            help="Choose All Departments or one specific department.",
        )

    filtered_df = register_df.copy()
    filtered_links = register_links.copy()
    if selected_department != "All Departments" and department_col is not None:
        keep_mask = filtered_df[department_col].apply(cell_text).eq(selected_department)
        filtered_df = filtered_df.loc[keep_mask].copy()
        filtered_links = filtered_links.loc[keep_mask].copy()

    # KPI 1: count nonblank serial numbers in Column A (S. No.).
    if serial_col is not None:
        total_observations = int(
            filtered_df[serial_col].apply(cell_text).ne("").sum()
        )
    else:
        total_observations = len(filtered_df)

    # KPI 2: compliance percentage based on Column E. TRUE/YES/COMPLIANT
    # count as compliant; FALSE/NO/PENDING/blank do not.
    if compliance_col is not None:
        compliance_values = filtered_df[compliance_col].apply(cell_text).str.strip().str.upper()
        compliant_values = {"TRUE", "YES", "Y", "1", "COMPLIANT", "COMPLETE", "COMPLETED"}
        compliance_count = int(compliance_values.isin(compliant_values).sum())
        compliance_denominator = int(
            filtered_df[serial_col].apply(cell_text).ne("").sum()
        ) if serial_col is not None else len(filtered_df)
        compliance_percent = (
            100.0 * compliance_count / compliance_denominator
            if compliance_denominator else 0.0
        )
    else:
        compliance_count = 0
        compliance_percent = 0.0

    # KPI 3: severity distribution from Column C.
    severity_values = (
        filtered_df[severity_col].apply(cell_text).str.strip().str.casefold()
        if severity_col is not None
        else pd.Series([], dtype=str)
    )

    high_count = int(severity_values.isin({"high", "h", "critical"}).sum())
    medium_count = int(severity_values.isin({"medium", "med", "moderate", "m"}).sum())
    low_count = int(severity_values.isin({"low", "l", "minor"}).sum())

    # Severity percentage calculations
    high_percent = (high_count / total_observations * 100) if total_observations else 0.0
    medium_percent = (medium_count / total_observations * 100) if total_observations else 0.0
    low_percent = (low_count / total_observations * 100) if total_observations else 0.0

    # Eye-catching KPI cards with distinct colors, icon badges, and status text.
    st.markdown(
        """
        <style>
        .psm-kpi-card {
            position: relative;
            min-height: 132px;
            padding: 16px 16px 14px 17px;
            border-radius: 15px;
            border: 1px solid var(--kpi-border);
            border-top: 4px solid var(--kpi-accent);
            background: linear-gradient(145deg, var(--kpi-bg) 0%, #ffffff 90%);
            box-shadow: 0 5px 15px rgba(20, 45, 90, 0.09);
            overflow: hidden;
            transition: transform 160ms ease, box-shadow 160ms ease;
        }
        .psm-kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 9px 21px rgba(20, 45, 90, 0.15);
        }
        .psm-kpi-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 12px;
        }
        .psm-kpi-label {
            color: #344563;
            font-size: 11px;
            line-height: 1.25;
            font-weight: 800;
            letter-spacing: .55px;
            text-transform: uppercase;
        }
        .psm-kpi-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 34px;
            width: 34px;
            height: 34px;
            border-radius: 11px;
            background: var(--kpi-icon-bg);
            color: var(--kpi-accent);
            font-size: 19px;
        }
        .psm-kpi-value {
            color: var(--kpi-accent);
            font-size: clamp(25px, 2vw, 33px);
            line-height: 1.05;
            font-weight: 850;
            letter-spacing: -.7px;
            margin-bottom: 9px;
        }
        .psm-kpi-foot {
            color: #65748b;
            font-size: 10px;
            line-height: 1.35;
            font-weight: 600;
        }
        .psm-kpi-progress {
            height: 5px;
            margin-top: 10px;
            border-radius: 10px;
            background: rgba(100, 116, 139, .14);
            overflow: hidden;
        }
        .psm-kpi-progress > span {
            display: block;
            height: 100%;
            border-radius: 10px;
            background: var(--kpi-accent);
        }
        @media (max-width: 1100px) {
            .psm-kpi-card { padding: 13px 11px; min-height: 125px; }
            .psm-kpi-label { font-size: 10px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    kpi_cards = [
        {
            "label": "Total Observations",
            "value": f"{total_observations:,}",
            "foot": "Recorded observations",
            "icon": "▤",
            "accent": "#2452a4",
            "bg": "#edf4ff",
            "border": "#cbdcff",
            "icon_bg": "#dce9ff",
            "progress": 100 if total_observations else 0,
        },
        {
            "label": "Compliance",
            "value": f"{compliance_percent:.1f}%",
            "foot": f"{compliance_count:,} compliant observations",
            "icon": "✓",
            "accent": "#168451",
            "bg": "#eaf8f0",
            "border": "#b9e6cc",
            "icon_bg": "#d2f0df",
            "progress": max(0, min(100, compliance_percent)),
        },
        {
            "label": "High Severity",
            "value": f"{high_percent:.1f}%",
            "foot": f"{high_count:,} high-risk observations",
            "icon": "▲",
            "accent": "#d92d3a",
            "bg": "#fff0f1",
            "border": "#ffc9ce",
            "icon_bg": "#ffe0e3",
            "progress": 100 * high_count / total_observations if total_observations else 0,
        },
        {
            "label": "Medium Severity",
            "value": f"{medium_percent:.1f}%",
            "foot": f"{medium_count:,} moderate-risk observations",
            "icon": "◆",
            "accent": "#c47a00",
            "bg": "#fff7e5",
            "border": "#f5dda1",
            "icon_bg": "#ffedc2",
            "progress": 100 * medium_count / total_observations if total_observations else 0,
        },
        {
            "label": "Low Severity",
            "value": f"{low_percent:.1f}%",
            "foot": f"{low_count:,} low-risk observations",
            "icon": "●",
            "accent": "#087e9b",
            "bg": "#eaf8fc",
            "border": "#bce8f1",
            "icon_bg": "#d3f1f7",
            "progress": 100 * low_count / total_observations if total_observations else 0,
        },
    ]

    kpi_columns = st.columns(5, gap="small")
    for column, card in zip(kpi_columns, kpi_cards):
        with column:
            st.markdown(
                f"""
                <div class="psm-kpi-card" style="--kpi-accent:{card['accent']}; --kpi-bg:{card['bg']}; --kpi-border:{card['border']}; --kpi-icon-bg:{card['icon_bg']};">
                    <div class="psm-kpi-top">
                        <div class="psm-kpi-label">{card['label']}</div>
                        <div class="psm-kpi-icon">{card['icon']}</div>
                    </div>
                    <div class="psm-kpi-value">{card['value']}</div>
                    <div class="psm-kpi-foot">{card['foot']}</div>
                    <div class="psm-kpi-progress"><span style="width:{max(0, min(100, float(card['progress']))):.1f}%;"></span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        "<div style='height:12px;'></div>",
        unsafe_allow_html=True,
    )

    # Build display table from the filtered records.
    display_df = pd.DataFrame(index=filtered_df.index)
    display_map = {
        "S. No.": serial_col,
        "Observation": observation_col,
        "Severity": severity_col,
        "Department": department_col,
        "Compliance": compliance_col,
    }

    for display_name, source_name in display_map.items():
        if source_name is not None:
            display_df[display_name] = filtered_df[source_name].apply(cell_text)

    # Show clear symbols in the register: TRUE = check mark, FALSE = X.
    # Keep the original values in filtered_df so KPI calculations remain correct.
    if "Compliance" in display_df.columns:
        def compliance_symbol(value):
            normalized_value = cell_text(value).strip().casefold()
            if normalized_value in {"true", "yes", "y", "1", "compliant", "complete", "completed"}:
                return "✓"
            if normalized_value in {"false", "no", "n", "0", "non-compliant", "noncompliant", "incomplete"}:
                return "✕"
            return "—" if not normalized_value else cell_text(value)

        display_df["Compliance"] = display_df["Compliance"].apply(compliance_symbol)

        # Green check mark for compliant observations; red cross for non-compliant.
        def style_compliance_symbol(value):
            if value == "✓":
                return "color: #168451; font-weight: 900; font-size: 18px;"
            elif value == "✕":
                return "color: #D92D3A; font-weight: 900; font-size: 18px;"
            return "color: #718096;"

    if report_col is not None:
        urls = []
        for row_index, cell_value in enumerate(filtered_df[report_col]):
            value = cell_text(cell_value)
            url = value if value.startswith(("https://", "http://")) else ""
            if (
                not url
                and report_col in filtered_links.columns
                and row_index < len(filtered_links)
            ):
                url = cell_text(filtered_links.iloc[row_index][report_col])
            if not url:
                match = re.search(
                    r'HYPERLINK\(\s*"((?:[^"]|"")*)"',
                    value,
                    flags=re.IGNORECASE,
                )
                if match:
                    url = match.group(1).replace('""', '"')
            urls.append(url)
        display_df["Compliance Report"] = urls

    if display_df.empty:
        st.warning(
            "The psm_data worksheet was loaded, but the expected register columns "
            "were not found. Available columns: " + ", ".join(register_df.columns)
        )
        return

    column_config = {}
    if "Compliance Report" in display_df.columns:
        column_config["Compliance Report"] = st.column_config.LinkColumn(
            "Compliance Report",
            display_text="View Report",
            help="Open the linked compliance report",
        )

    # Apply red/green styling to the Compliance column
    table_df = display_df.reset_index(drop=True)

    if "Compliance" in table_df.columns:
        styled_table = table_df.style.apply(
            lambda column: [
                style_compliance_symbol(value)
                for value in column
            ],
            subset=["Compliance"],
            axis=0,
        )
    else:
        styled_table = table_df

    # ---------------------------------------------------------
    # REGISTER TABLE - WRAP OBSERVATION TEXT
    # Keep Streamlit's column resize controls enabled
    # ---------------------------------------------------------

    table_df = display_df.reset_index(drop=True)

    # Preserve green/red compliance styling
    if "Compliance" in table_df.columns:
        styled_table = table_df.style.apply(
            lambda column: [
                style_compliance_symbol(value)
                for value in column
            ],
            subset=["Compliance"],
            axis=0,
        )
    else:
        styled_table = table_df

    st.dataframe(
        styled_table,
        use_container_width=True,
        hide_index=True,
        height=min(600, max(200, 42 * (len(display_df) + 1))),
        column_config={
            "Observation": st.column_config.TextColumn(
                "Observation",
                width="large",
                help="Complete observation text. Resize this column as required.",
            ),
            "Compliance": st.column_config.TextColumn(
                "Compliance",
                width="small",
            ),
            "Severity": st.column_config.TextColumn(
                "Severity",
                width="small",
            ),
            "Department": st.column_config.TextColumn(
                "Department",
                width="medium",
            ),
            **column_config,
        },
    )


# ============================================================
# DATA HELPERS
# ============================================================

def normalize(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def find_column(df, candidates):
    normalized_columns = {
        normalize(column): column for column in df.columns
    }

    for candidate in candidates:
        key = normalize(candidate)
        if key in normalized_columns:
            return normalized_columns[key]

    for candidate in candidates:
        key = normalize(candidate)

        for normalized, original in normalized_columns.items():
            if key in normalized:
                return original

    return None


def cell_text(value):
    if value is None or pd.isna(value):
        return ""

    value = str(value).strip()

    if value.lower() in {"nan", "none", "nat"}:
        return ""

    return value


def numeric_score(value):
    value = cell_text(value).replace("%", "").replace(",", "")

    if not value:
        return None

    try:
        number = float(value)
        return number if 0 <= number <= 100 else None
    except (ValueError, TypeError):
        return None

    # ============================================================


# BUILD THE PERFORMANCE GRAPH
# ============================================================

def build_chart(df, date_col, overall_col, safety_col):
    chart_df = df.copy().reset_index(drop=True)

    chart_df["_date"] = chart_df[date_col].apply(cell_text)

    chart_df["_overall"] = (
        chart_df[overall_col].apply(numeric_score)
        if overall_col else None
    )

    chart_df["_safety"] = (
        chart_df[safety_col].apply(numeric_score)
        if safety_col else None
    )

    valid_rows = (
            chart_df["_date"].ne("")
            | chart_df["_overall"].notna()
            | chart_df["_safety"].notna()
    )

    chart_df = chart_df.loc[valid_rows].copy()

    chart_df["_date"] = chart_df["_date"].where(
        chart_df["_date"].ne(""),
        "Audit without date",
    )

    point_count = len(chart_df)

    # Preserve the existing chart style.
    # Width grows with the number of records to enable horizontal scroll.
    graph_width = max(950, point_count * 115)

    # Keep the graph height fixed so it does not need vertical scrolling.
    graph_height = 400

    fig = go.Figure()

    if overall_col:
        fig.add_trace(
            go.Scatter(
                x=chart_df["_date"],
                y=chart_df["_overall"],
                mode="lines+markers+text",
                name="Unit Overall Score",
                connectgaps=False,
                line=dict(color="#10377D", width=3),
                marker=dict(color="#10377D", size=8),
                text=[
                    "" if pd.isna(value) else f"{value:g}"
                    for value in chart_df["_overall"]
                ],
                textposition="top center",
                textfont=dict(color="#10377D", size=12),
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Unit Overall Score: %{y}<extra></extra>"
                ),
            )
        )

    if safety_col:
        fig.add_trace(
            go.Scatter(
                x=chart_df["_date"],
                y=chart_df["_safety"],
                mode="lines+markers+text",
                name="Unit Process Safety Score",
                connectgaps=False,
                line=dict(color="#F5223B", width=3),
                marker=dict(color="#F5223B", size=8),
                text=[
                    "" if pd.isna(value) else f"{value:g}"
                    for value in chart_df["_safety"]
                ],
                textposition="bottom center",
                textfont=dict(color="#F5223B", size=12),
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Unit Process Safety Score: %{y}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        width=graph_width,
        height=graph_height,
        autosize=False,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=55, r=25, t=70, b=80),
        font=dict(
            family="Arial, sans-serif",
            color="#10377D",
            size=12,
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.08,
            yanchor="bottom",
            font=dict(size=12),
        ),
        hovermode="x",
        xaxis=dict(
            type="category",
            showgrid=True,
            gridcolor="#D5E4F8",
            griddash="dash",
            tickangle=25,
            automargin=True,
            fixedrange=True,
        ),
        yaxis=dict(
            range=[0, 105],
            dtick=20,
            showgrid=True,
            gridcolor="#D5E4F8",
            griddash="dash",
            zeroline=False,
            automargin=True,
            fixedrange=True,
        ),
        dragmode=False,
        uirevision="jsap-audit-chart",
        transition=dict(duration=0),
    )

    return fig, chart_df


# ============================================================
# GRAPH IN A ROUNDED RECTANGLE
# Horizontal scroll only; no internal vertical scroll.
# ============================================================

def render_scrollable_graph(fig):
    graph_html = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "displayModeBar": False,
            "scrollZoom": False,
            "responsive": False,
            "doubleClick": False,
        },
    )

    page = f""" 
    <!DOCTYPE html> 
    <html> 
    <head> 
        <meta charset="UTF-8"> 
        <style> 
            * {{ 
                box-sizing: border-box; 
            }} 

            html, body {{ 
                margin: 0; 
                padding: 0; 
                width: 100%; 
                height: 100%; 
                background: #FFFFFF; 
                font-family: Arial, sans-serif; 
                overflow: hidden; 
            }} 

            .graph-viewport {{ 
                width: 100%; 
                height: 425px; 
                overflow-x: auto; 
                overflow-y: hidden; 
                border: 1px solid #D5E2F2; 
                border-radius: 14px; 
                background: #FFFFFF; 
                scrollbar-width: auto; 
                scrollbar-color: #AAB7C8 #F1F4F8; 
            }} 

            .graph-content {{ 
                width: max-content; 
                min-width: 100%; 
                height: 400px; 
                overflow: hidden; 
            }} 

            .graph-content > div {{ 
                height: 400px !important; 
            }} 

            .graph-viewport::-webkit-scrollbar {{ 
                height: 11px; 
                width: 0; 
            }} 

            .graph-viewport::-webkit-scrollbar-track {{ 
                background: #F1F4F8; 
                border-radius: 8px; 
            }} 

            .graph-viewport::-webkit-scrollbar-thumb {{ 
                background: #AAB7C8; 
                border-radius: 8px; 
            }} 

            .graph-viewport::-webkit-scrollbar-thumb:hover {{ 
                background: #7186A5; 
            }} 
        </style> 
    </head> 
    <body> 
        <div class="graph-viewport"> 
            <div class="graph-content"> 
                {graph_html} 
            </div> 
        </div> 
    </body> 
    </html> 
    """

    # The iframe is taller than the plot, so the plot itself has no
    # internal vertical scrollbar. Horizontal scrolling remains inside
    # the rounded graph rectangle.
    components.html(
        page,
        height=435,
        scrolling=False,
    )


# ============================================================
# AUDIT REPORT TABLE
# ============================================================

def render_report_table(report_df):
    rows = []

    for _, row in report_df.iterrows():
        date_label = html.escape(cell_text(row["_date_label"]))
        url = cell_text(row["_report_url"])

        if url.startswith(("https://", "http://")):
            safe_url = html.escape(url, quote=True)

            report_content = (
                f'<a class="view-report" href="{safe_url}" '
                'target="_blank" rel="noopener noreferrer">'
                'View Report</a>'
            )
        else:
            report_content = (
                '<span class="no-report">Link unavailable</span>'
            )

        rows.append(
            f"<tr><td>{date_label}</td>"
            f"<td>{report_content}</td></tr>"
        )

        # Table height adjusts to the number of rows, up to the maximum.
    # This avoids a large blank area when only a few reports exist.
    table_height = min(260, 44 + 42 * len(rows))
    iframe_height = table_height + 8

    page = f""" 
    <!DOCTYPE html> 
    <html> 
    <head> 
    <meta charset="UTF-8"> 
    <style> 
        * {{ box-sizing: border-box; }} 

        html, body {{ 
            margin: 0; 
            padding: 0; 
            background: #FFFFFF; 
            color: #10377D; 
            font-family: Arial, sans-serif; 
            overflow: hidden; 
        }} 

        .table-scroll {{ 
            height: {table_height}px; 
            overflow-y: auto; 
            overflow-x: auto; 
            border: 1px solid #D5E2F2; 
            border-radius: 10px; 
        }} 

        table {{ 
            width: 100%; 
            border-collapse: separate; 
            border-spacing: 0; 
            table-layout: fixed; 
            text-align: center; 
        }} 

        thead th {{ 
            position: sticky; 
            top: 0; 
            z-index: 2; 
            background: #F1F3F7; 
            color: #10377D; 
            font-size: 15px; 
            font-weight: 800; 
            padding: 11px 8px; 
            height: 42px; 
            border-bottom: 1px solid #D5E2F2; 
        }} 

        td {{ 
            height: 42px; 
            padding: 6px 8px; 
            font-size: 14px; 
            background: #FFFFFF; 
            border-bottom: 1px solid #D5E2F2; 
            overflow-wrap: anywhere; 
        }} 

        th:first-child, td:first-child {{ 
            width: 50%; 
            border-right: 1px solid #D5E2F2; 
        }} 

        th:last-child, td:last-child {{ 
            width: 50%; 
        }} 

        .view-report {{ 
            display: inline-block; 
            padding: 6px 16px; 
            border-radius: 6px; 
            background: #10377D; 
            color: #FFFFFF !important; 
            text-decoration: none !important; 
            font-size: 12px; 
            font-weight: 700; 
            white-space: nowrap; 
        }} 

        .view-report:hover {{ 
            background: #174DA5; 
        }} 

        .no-report {{ 
            color: #777777; 
            font-size: 12px; 
        }} 

        tr:last-child td {{ 
            border-bottom: none; 
        }} 

        @media(max-width: 600px) {{ 
            thead th {{ 
                font-size: 12px; 
                padding: 8px 4px; 
            }} 

            td {{ 
                font-size: 12px; 
                padding: 5px 4px; 
            }} 

            .view-report {{ 
                padding: 6px 8px; 
                font-size: 11px; 
            }} 
        }} 
    </style> 
    </head> 
    <body> 
        <div class="table-scroll"> 
            <table> 
                <thead> 
                    <tr> 
                        <th>Audit Date</th> 
                        <th>Audit Report</th> 
                    </tr> 
                </thead> 
                <tbody> 
                    {''.join(rows)} 
                </tbody> 
            </table> 
        </div> 
    </body> 
    </html> 
    """

    components.html(
        page,
        height=iframe_height,
        scrolling=False,
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

@st.fragment(run_every=REFRESH_SECONDS)
def render_dashboard():
    try:
        df, links_df = load_sheet()
    except Exception as exc:
        st.error(
            "Google Sheets could not be refreshed. "
            "The dashboard cannot guarantee that displayed scores are current."
        )
        st.code(f"{type(exc).__name__}: {exc}")
        st.info(
            "Check that the JSAP worksheet exists and is accessible. "
            "If using service_account.json, verify the service account "
            "permissions and Google Sheets API configuration."
        )
        return

    date_col = find_column(
        df,
        ["Audit Date", "Audit Period", "Audit Dates", "Date"],
    )

    overall_col = find_column(
        df,
        ["Unit Overall Score", "Overall Score", "Unit Overall Audit Score"],
    )

    safety_col = find_column(
        df,
        [
            "Unit Process Safety Score",
            "Process Safety Score",
            "Unit PSM Score",
        ],
    )

    report_col = find_column(
        df,
        ["Audit Report", "Report Link", "Audit Report Link", "Report URL"],
    )

    # Remove blank rows without breaking report-link alignment.
    used_columns = [
        column
        for column in [date_col, overall_col, safety_col, report_col]
        if column is not None
    ]

    if used_columns:
        mask = df[used_columns].apply(
            lambda row: any(cell_text(value) for value in row),
            axis=1,
        )

        df = df.loc[mask].reset_index(drop=True)
        links_df = links_df.loc[mask].reset_index(drop=True)

        # --------------------------------------------------------
    # TITLE AND SCORE CARDS
    # --------------------------------------------------------

    left, right = st.columns([1.0, 1.65], gap="medium")

    with left:
        st.markdown(
            """ 
            <div class="section-title">JSAP AUDIT PERFORMANCE</div> 
            <div class="red-underline"></div> 
            """,
            unsafe_allow_html=True,
        )

    with right:
        render_score_matrix()

    st.markdown(
        '<div style="height:12px;"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # PERFORMANCE GRAPH
    # --------------------------------------------------------

    if date_col and (overall_col or safety_col):
        fig, chart_df = build_chart(
            df,
            date_col,
            overall_col,
            safety_col,
        )

        if not chart_df.empty:
            render_scrollable_graph(fig)
        else:
            st.info("No audit score data is available.")
    else:
        st.error(
            "Required score columns were not found. "
            f"Available columns: {', '.join(df.columns)}"
        )

        # --------------------------------------------------------
    # AUDIT REPORTS
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="height:8px;"></div>
        <div class="section-title">JSAP AUDIT REPORT</div>
        <div class="red-underline"></div>
        """,
        unsafe_allow_html=True,
    )

    if not date_col or not report_col:
        st.warning(
            "Audit Date or Audit Report column was not found. "
            f"Available columns: {', '.join(df.columns)}"
        )
        # Still render the independent observation register below.
        render_psm_register()
        return

    report_df = df.copy()
    report_df["_date_label"] = report_df[date_col].apply(cell_text)

    urls = []

    for row_index, value in enumerate(report_df[report_col]):
        text_value = cell_text(value)
        url = ""

        if text_value.startswith(("https://", "http://")):
            url = text_value

        if (
                not url
                and report_col in links_df.columns
                and row_index < len(links_df)
        ):
            url = cell_text(links_df.iloc[row_index][report_col])

        if not url:
            match = re.search(
                r'HYPERLINK\(\s*"((?:[^"]|"")*)"',
                text_value,
                flags=re.IGNORECASE,
            )

            if match:
                url = match.group(1).replace('""', '"')

        urls.append(url)

    report_df["_report_url"] = urls

    report_df = report_df[
        report_df["_date_label"].ne("")
        | report_df[report_col].apply(
            lambda value: bool(cell_text(value))
        )
        ]

    # ============================================================
    # JSAP AUDIT REPORT HEADING
    # ============================================================

    st.markdown(
        """
        <div style="height:8px;"></div>
        <div class="section-title">JSAP AUDIT REPORT</div>
        <div class="red-underline"></div>
        """,
        unsafe_allow_html=True,
    )

    if report_df.empty:
        st.info("No audit reports have been entered yet.")
    else:
        render_report_table(report_df)

    # --------------------------------------------------------
    # PSM OBSERVATION REGISTER
    # --------------------------------------------------------
    render_psm_register()

    # Start the dashboard.


# Data refreshes automatically every 60 seconds.
render_dashboard()
