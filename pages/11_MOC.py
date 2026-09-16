import streamlit as st
import pandas as pd
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from datetime import date

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM Dashboard - MOC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        margin-top: 0 !important;
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

                MANAGEMENT OF CHANGE(MOC)

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
# CONFIGURATION
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
MOC_SHEET_NAME = "MOC"
ROWS_PER_PAGE = 5
DATA_REFRESH_SECONDS = 20

MOC_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={MOC_SHEET_NAME}"
)

MOC_HTML_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:html&sheet={MOC_SHEET_NAME}"
)

# ============================================================
# SESSION STATE
# ============================================================
DEFAULT_STATE = {
    "moc_year": "2026-27",
    "moc_month": "All Months",
    "moc_department": "All Departments",
    "moc_status_filter": "All",
    "moc_search": "",
    "moc_page": 1,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_moc_filters():
    """
    Reset widget-backed state in a callback.

    The callback executes before Streamlit recreates the widgets,
    so this avoids the 'cannot be modified after widget...' error.
    """
    st.session_state["moc_year"] = "2026-27"
    st.session_state["moc_month"] = "All Months"
    st.session_state["moc_department"] = "All Departments"
    st.session_state["moc_status_filter"] = "All"
    st.session_state["moc_search"] = ""
    st.session_state["moc_page"] = 1


def reset_dependent_filters():
    st.session_state["moc_month"] = "All Months"
    st.session_state["moc_department"] = "All Departments"
    st.session_state["moc_page"] = 1


def reset_page():
    st.session_state["moc_page"] = 1


# ============================================================
# TEXT / DATE HELPERS
# ============================================================
def clean_text(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()

    if value.lower() in {
        "nan",
        "none",
        "nat",
        "<na>",
        "na",
        "n/a",
    }:
        return ""

    return value


def parse_one_date(value):
    """
    Robust Google-Sheet date parser.

    Handles:
      - DD/MM/YYYY
      - MM/DD/YYYY
      - YYYY-MM-DD
      - ISO timestamps
      - pandas Timestamp
      - Excel serial dates

    The previous version could leave valid dates as NaT, which
    caused records to disappear from the Financial Year filter.
    """
    if pd.isna(value):
        return pd.NaT

    if isinstance(value, pd.Timestamp):
        return value.normalize()

        # Excel / Google-sheet numeric serial date.
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 20000 <= float(value) <= 80000:
            try:
                return (
                        pd.Timestamp("1899-12-30")
                        + pd.to_timedelta(float(value), unit="D")
                ).normalize()
            except Exception:
                pass

    text = clean_text(value)

    if not text:
        return pd.NaT

        # Try modern pandas mixed-format parsing first.
    try:
        parsed = pd.to_datetime(
            text,
            errors="coerce",
            format="mixed",
            dayfirst=True,
        )
        if not pd.isna(parsed):
            return pd.Timestamp(parsed).normalize()
    except Exception:
        pass

        # Explicit common formats.
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m/%d/%y",
        "%m-%d-%y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in formats:
        try:
            parsed = pd.to_datetime(text, format=fmt, errors="coerce")
            if not pd.isna(parsed):
                return pd.Timestamp(parsed).normalize()
        except Exception:
            continue

            # Last fallback: try both date conventions.
    for dayfirst in (True, False):
        try:
            parsed = pd.to_datetime(
                text,
                errors="coerce",
                dayfirst=dayfirst,
            )
            if not pd.isna(parsed):
                return pd.Timestamp(parsed).normalize()
        except Exception:
            continue

    return pd.NaT


def parse_date_series(series):
    return series.apply(parse_one_date)


# ============================================================
# GOOGLE SHEET DATA
# ============================================================
class _SheetLinkParser(HTMLParser):
    """Extract hyperlinks from the MOC gviz HTML table by row/cell."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_anchor = False
        self.current_row = []
        self.rows = []
        self.current_cell_link = ""
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        tag = tag.lower()

        if tag == "table" and not self.in_table:
            self.in_table = True
            return

        if not self.in_table:
            return

        if tag == "tr":
            self.in_row = True
            self.current_row = []
            return

        if self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell_link = ""
            return

        if self.in_cell and tag == "a":
            href = attrs.get("href", "")
            if href:
                self.current_cell_link = href
            self.in_anchor = True

    def handle_endtag(self, tag):
        tag = tag.lower()

        if not self.in_table:
            return

        if tag == "a":
            self.in_anchor = False
        elif tag in {"td", "th"} and self.in_cell:
            self.current_row.append(self.current_cell_link)
            self.in_cell = False
            self.current_cell_link = ""
        elif tag == "tr" and self.in_row:
            self.rows.append(self.current_row)
            self.current_row = []
            self.in_row = False
        elif tag == "table":
            self.in_table = False


def _extract_sheet_document_links():
    """Return document-column hyperlinks from the rendered Google Sheet HTML.

    CSV export can return only the visible label of a HYPERLINK cell. The
    rendered HTML endpoint retains the actual href, so use it as a fallback
    when the CSV cell does not contain a usable URL.
    """
    try:
        import requests

        response = requests.get(
            MOC_HTML_URL,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        parser = _SheetLinkParser()
        parser.feed(response.text)

        if not parser.rows:
            return []

            # Find the table/header row containing the required column.
        header_index = None
        document_col = None
        for idx, row in enumerate(parser.rows):
            labels = [clean_text(cell) for cell in row]
            for col_idx, label in enumerate(labels):
                if label == "Attach MOC Softcopy Link":
                    header_index = idx
                    document_col = col_idx
                    break
            if document_col is not None:
                break

        if header_index is None or document_col is None:
            return []

        links = []
        for row in parser.rows[header_index + 1:]:
            links.append(
                row[document_col].strip()
                if document_col < len(row)
                else ""
            )
        return links
    except Exception:
        # The CSV remains the primary source. Hyperlink extraction is only
        # a fallback, so a blocked HTML endpoint must never break the app.
        return []


def _normalise_document_url(value):
    """Return a safe absolute document URL, or an empty string.

    A relative value such as 'Open Document' would otherwise make the browser
    navigate to the Streamlit app itself. Such values are deliberately not
    used as hrefs.
    """
    text = clean_text(value)
    if not text:
        return ""

        # Support markdown-style links if they are pasted into the sheet.
    markdown_match = re.search(r"\[[^\]]*\]\((https?://[^)]+)\)", text)
    if markdown_match:
        text = markdown_match.group(1).strip()

        # Handle Google Sheets HYPERLINK formula values if they reach the CSV.
    formula_match = re.search(
        r'HYPERLINK\s*\(\s*["\'](https?://[^"\']+)["\']',
        text,
        flags=re.IGNORECASE,
    )
    if formula_match:
        text = formula_match.group(1).strip()

        # Recover a raw absolute URL embedded in surrounding display text.
    raw_url_match = re.search(
        r'https?://[^\s"<>]+',
        text,
        flags=re.IGNORECASE,
    )
    if raw_url_match:
        text = raw_url_match.group(0).rstrip(".,;")

    text = text.strip().strip('"\'<>')

    if text.startswith("www."):
        text = "https://" + text

    parsed = urlparse(text)
    if parsed.scheme.lower() in {"http", "https"} and parsed.netloc:
        return text

    return ""


@st.cache_data(ttl=DATA_REFRESH_SECONDS, show_spinner=False)
def get_moc_data():
    """
    Reads the MOC tab directly from Google Sheets.

    CSV is the primary data source. The rendered HTML endpoint is used to
    recover the actual href for Google Sheets HYPERLINK cells because CSV
    export may return only their visible label.
    """
    try:
        data = pd.read_csv(MOC_CSV_URL)

        data.columns = (
            data.columns.astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.strip()
        )

        for col in data.columns:
            if data[col].dtype == "object":
                data[col] = (
                    data[col]
                    .astype("string")
                    .str.replace("\xa0", " ", regex=False)
                    .str.strip()
                )

                # Recover true hyperlinks when the CSV contains a display label such
        # as "Open Document" rather than the underlying URL.
        if "Attach MOC Softcopy Link" in data.columns:
            csv_links = data["Attach MOC Softcopy Link"].map(clean_text).tolist()
            html_links = _extract_sheet_document_links()

            merged_links = []
            for idx, csv_value in enumerate(csv_links):
                direct_url = _normalise_document_url(csv_value)
                if direct_url:
                    merged_links.append(direct_url)
                elif idx < len(html_links):
                    merged_links.append(
                        _normalise_document_url(html_links[idx])
                    )
                else:
                    merged_links.append("")

            data["Attach MOC Softcopy Link"] = merged_links

        return data

    except Exception as exc:
        st.error(f"Unable to load Google Sheet — MOC tab: {exc}")
        return pd.DataFrame()

    # ============================================================


# DATA PREPARATION
# ============================================================
REQUIRED_COLUMNS = [
    "MOC No",
    "Request Date",
    "Department",
    "Section",
    "Requestor Name",
    "Description of Change",
    "Change Type (Permanent/Temporary/Emergency)",
    "Category of changes (Technology/Personnel/Facility)",
    "Risk Level",
    "Approval Status",
    "Approved By",
    "Implementation Date",
    "Review Date",
    "SOP/SMP Revision  (YES/NO)",
    "Training After SOP/SMP Revision  (YES/NO)",
    "PSSR  (YES/NO)",
    "Document Location",
    "Status",
    "Attach MOC Softcopy Link",
    "Remarks",
]

TEXT_COLUMNS = [
    "MOC No",
    "Department",
    "Section",
    "Requestor Name",
    "Description of Change",
    "Approval Status",
    "Approved By",
    "Status",
    "Attach MOC Softcopy Link",
    "Remarks",
]


def prepare_data(raw):
    if raw.empty:
        return raw

    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]

    if missing:
        st.error("The following required columns are missing from the MOC tab:")
        st.write(missing)
        st.write("Columns currently found:", raw.columns.tolist())
        st.stop()

    data = raw.copy()

    for col in TEXT_COLUMNS:
        data[col] = data[col].map(clean_text)

        # IMPORTANT:
    # Do not use one rigid pd.to_datetime(dayfirst=True) conversion.
    # Google Sheet date formats can vary. The robust parser below
    # prevents valid rows from disappearing from FY 2026-27.
    data["Request Date Parsed"] = parse_date_series(
        data["Request Date"]
    )

    data["Financial Year"] = data["Request Date Parsed"].apply(
        financial_year
    )

    data["Month Key"] = data["Request Date Parsed"].dt.to_period("M")
    data["Month Display"] = data["Request Date Parsed"].dt.strftime("%b-%y")

    return data


def financial_year(dt):
    if pd.isna(dt):
        return ""

    year = int(dt.year)

    if int(dt.month) >= 4:
        return f"{year}-{str(year + 1)[-2:]}"

    return f"{year - 1}-{str(year)[-2:]}"


def normalize_status(value):
    return clean_text(value).lower()


def is_open_status(value):
    return normalize_status(value) in {
        "open",
        "ongoing",
        "in progress",
    }


def is_closed_status(value):
    return normalize_status(value) in {
        "closed",
        "completed",
    }


def is_pending_approval(value):
    status = normalize_status(value)

    if not status or "pending" not in status:
        return False

        # Generic "Pending" is counted as pending approval.
    if status == "pending":
        return True

        # Stage-specific pending approval.
    return any(stage in status for stage in ("cft", "trc", "hod"))


def calculate_pending_over_15(data):
    if data.empty:
        return 0

    pending_mask = data["Approval Status"].map(is_pending_approval)

    request_dates = pd.to_datetime(
        data["Request Date Parsed"],
        errors="coerce",
    )

    today = pd.Timestamp(date.today())
    age_days = (today - request_dates).dt.days

    return int(
        (pending_mask & age_days.gt(15)).sum()
    )


# ============================================================
# CSS
# ============================================================
st.markdown(
    """ 
<style> 
:root { 
    --navy: #173b73; 
    --blue: #137dcc; 
    --blue-dark: #0c5fa8; 
    --blue-soft: #eaf4ff; 
    --red: #df2433; 
    --orange: #ee8b12; 
    --green: #159447; 
    --purple: #8057e8; 
    --text: #315071; 
    --muted: #718199; 
    --border: #d5e0eb; 
    --page: #fbfcfe; 
} 

* { 
    box-sizing: border-box; 
} 

html, body, .stApp, 
[data-testid="stAppViewContainer"], 
[data-testid="stAppViewContainer"] > .main { 
    margin: 0 !important; 
    padding: 0 !important; 
    background: var(--page) !important; 
    color: var(--text) !important; 
    font-family: "Segoe UI", Arial, sans-serif !important; 
} 

.stApp * { 
    font-family: "Segoe UI", Arial, sans-serif; 
} 

[data-testid="stHeader"], 
[data-testid="stToolbar"], 
[data-testid="stDecoration"], 
#MainMenu, 
footer { 
    display: none !important; 
} 

.block-container, 
[data-testid="stMainBlockContainer"], 
[data-testid="stAppViewBlockContainer"] { 
    width: 100% !important; 
    max-width: 100% !important; 
    padding: 0 36px 32px !important; 
    margin: 0 !important; 
} 

[data-testid="stHorizontalBlock"] { 
    gap: 14px !important; 
} 

/* ============================================================ 
   TOP FILTERS 
   ============================================================ */ 
.filter-label { 
    color: var(--navy); 
    font-size: 12px; 
    font-weight: 750; 
    margin: 0 0 12px 2px; 
} 

div[data-testid="stSelectbox"] { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

div[data-baseweb="select"] > div { 
    height: 40px !important; 
    min-height: 40px !important; 
    background: #f1f4f8 !important; 
    border: 1px solid #dce4ec !important; 
    border-radius: 8px !important; 
    box-shadow: none !important; 
} 

div[data-baseweb="select"] > div:hover { 
    background: #ffffff !important; 
    border-color: #a9bfd8 !important; 
} 

div[data-baseweb="select"] * { 
    color: #354154 !important; 
    font-size: 13px !important; 
    font-weight: 500 !important; 
} 

div[data-baseweb="select"] svg { 
    fill: #27364a !important; 
} 

/* ============================================================ 
   KPI 
   ============================================================ */ 
.kpi-card { 
    position: relative; 
    width: 100%; 
    height: 118px !important; 
    min-height: 118px !important; 
    max-height: 118px !important; 
    box-sizing: border-box !important; 
    overflow: hidden; 
    background: #ffffff; 
    border: 1px solid var(--border); 
    border-radius: 9px; 
    padding: 14px 18px; 
    box-shadow: 0 3px 10px rgba(23,59,115,.055); 
} 

.kpi-card::before { 
    content: ""; 
    position: absolute; 
    left: 0; 
    top: 0; 
    bottom: 0; 
    width: 5px; 
} 

.kpi-card.blue::before { background: var(--blue); } 
.kpi-card.orange::before { background: var(--orange); } 
.kpi-card.green::before { background: var(--green); } 
.kpi-card.pending::before { background: var(--red); } 

.kpi-label { 
    color: var(--navy); 
    font-size: 12.5px; 
    line-height: 1.2; 
    font-weight: 750; 
} 

.kpi-value { 
    margin-top: 4px; 
    color: var(--navy); 
    font-size: 31px; 
    line-height: 1; 
    font-weight: 750; 
} 

.kpi-sub { 
    margin-top: 4px; 
    color: var(--muted); 
    font-size: 10.5px; 
    font-weight: 500; 
} 

/* Every KPI uses one consistent accent colour for title, value and subtitle. */ 
.kpi-card.blue .kpi-label, 
.kpi-card.blue .kpi-value, 
.kpi-card.blue .kpi-sub { 
    color: var(--blue); 
} 

.kpi-card.orange .kpi-label, 
.kpi-card.orange .kpi-value, 
.kpi-card.orange .kpi-sub { 
    color: var(--orange); 
} 

.kpi-card.green .kpi-label, 
.kpi-card.green .kpi-value, 
.kpi-card.green .kpi-sub { 
    color: var(--green); 
} 

.kpi-card.pending .kpi-label, 
.kpi-card.pending .kpi-value, 
.kpi-card.pending .kpi-sub { 
    color: var(--red); 
} 

/* ============================================================ 
   SECTION 
   ============================================================ */ 
.section-heading { 
    display: flex; 
    align-items: center; 
    width: 100%; 
    box-sizing: border-box; 
    margin: 10px 0 0 !important; 
    padding: 7px 16px 8px; 
    background: #edf5fd; 
    border: 1px solid #d7e6f4; 
    border-radius: 9px; 
    box-shadow: 0 2px 7px rgba(23,59,115,.035); 
} 

.section-title { 
    display: block; 
    color: var(--navy); 
    font-size: 25px; 
    line-height: 1.05; 
    font-weight: 750; 
    padding: 0; 
    margin: 0 !important; 
} 

/* ============================================================ 
   MOC TOOLBAR 
   ============================================================ */ 
div[data-testid="stTextInput"] { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

div[data-testid="stTextInput"] input { 
    height: 38px !important; 
    min-height: 38px !important; 
    max-height: 38px !important; 
    border-radius: 8px !important; 
    background: #f1f4f8 !important; 
    border: 1px solid #d7e1eb !important; 
    color: #354154 !important; 
    font-size: 12.5px !important; 
    font-weight: 500 !important; 
    box-shadow: none !important; 
} 

div[data-testid="stTextInput"] input::placeholder { 
    color: #7b8a9d !important; 
    opacity: 1 !important; 
} 

/* Search / All / Closed / Open / Refresh all use exactly 
   the same 38px height for perfect horizontal alignment. */ 
div[data-testid="stButton"] > button { 
    height: 38px !important; 
    min-height: 38px !important; 
    max-height: 38px !important; 
    padding: 0 10px !important; 
    border-radius: 8px !important; 
    background: #ffffff !important; 
    border: 1px solid #d2deea !important; 
    color: var(--navy) !important; 
    font-size: 12px !important; 
    font-weight: 600 !important; 
    line-height: 1 !important; 
} 

/* Toolbar refresh is icon-only and uses the same compact height. */ 
.moc-toolbar-refresh div.stButton > button, 
.moc-toolbar div.stButton > button, 
.st-key-moc_toolbar_refresh div.stButton > button { 
    height: 38px !important; 
    min-height: 38px !important; 
    max-height: 38px !important; 
    line-height: 1 !important; 
} 

.moc-toolbar-refresh div.stButton > button, 
.st-key-moc_toolbar_refresh div.stButton > button { 
    padding: 0 !important; 
    font-size: 13px !important; 
} 



/* Exact vertical alignment for MOC Register toolbar controls. */ 
.moc-toolbar { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

div[data-testid="stTextInput"], 
div[data-testid="stTextInput"] > div, 
div[data-testid="stTextInput"] > div > div { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

.moc-toolbar-refresh { 
    margin: 0 !important; 
    padding: 0 !important; 
} 


.st-key-moc_toolbar { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

.st-key-moc_toolbar [data-testid="stHorizontalBlock"] { 
    align-items: center !important; 
    margin: 0 !important; 
    padding: 0 !important; 
} 

.st-key-moc_toolbar [data-testid="stTextInput"], 
.st-key-moc_toolbar [data-testid="stButton"] { 
    margin: 0 !important; 
    padding: 0 !important; 
} 

.st-key-moc_toolbar [data-testid="stTextInput"] input, 
.st-key-moc_toolbar [data-testid="stButton"] > button { 
    margin: 0 !important; 
    transform: none !important; 
} 



/* ============================================================ 
   UNIFORM DASHBOARD COMPONENT SPACING 
   ~0.4 cm / 15px between every major component 
   ============================================================ */ 

/* Never let generic Streamlit vertical gaps add another large offset. */ 
/* The filter label/control pair stays compact; the 15px rhythm begins 
   only after the complete filter row. */ 
.filter-label { 
    margin-bottom: 8px !important; 
} 

/* Keep the MOC title itself visually compact. */ 
.section-title { 
    margin: 0 !important; 
} 

/* Compact MOC table rows. */ 
.moc-table tbody tr { 
    height: 52px !important; 
} 

.moc-table tbody td { 
    height: 52px !important; 
    min-height: 52px !important; 
    padding: 7px 10px !important; 
    vertical-align: middle !important; 
} 


/* ============================================================ 
   REFERENCE TYPOGRAPHY 
   Clean modern sans-serif matching the supplied reference. 
   ============================================================ */ 
html, body, [class*="st-"], button, input, textarea, select { 
    font-family: "Segoe UI", Arial, sans-serif !important; 
} 

.moc-dashboard, 
.moc-dashboard *, 
.moc-table, 
.moc-table *, 
.kpi-card, 
.kpi-card * { 
    font-family: "Segoe UI", Arial, sans-serif !important; 
} 


/* ============================================================ 
   CONSISTENT MAJOR-COMPONENT SPACING 
   0.4 cm ≈ 15px 
   ============================================================ */ 
/* Protect filter labels from clipping. */ 
.filter-label { 
    display: block !important; 
    height: auto !important; 
    min-height: 18px !important; 
    line-height: 18px !important; 
    margin: 0 0 8px 0 !important; 
    padding: 0 !important; 
    overflow: visible !important; 
} 

/* Never transform or offset major sections. */ 
.section-title, 
.table-shell, 
.st-key-moc_toolbar { 
    transform: none !important; 
} 

/* Compact table rows. */ 
.moc-table tbody tr { 
    height: 52px !important; 
} 
.moc-table tbody td { 
    height: 52px !important; 
    min-height: 52px !important; 
    padding: 7px 10px !important; 
    vertical-align: middle !important; 
} 




/* Keep the filter labels fully visible. */ 
.filter-label { 
    display: block !important; 
    height: auto !important; 
    min-height: 17px !important; 
    line-height: 17px !important; 
    margin: 0 0 8px 2px !important; 
    padding: 0 !important; 
    overflow: visible !important; 
} 

/* Never offset major components with transforms. */ 
.section-heading, 
.section-title, 
.st-key-moc_toolbar, 
.table-shell { 
    transform: none !important; 
} 

/* Compact table rows. */ 
.moc-table tbody tr { 
    height: 52px !important; 
} 

.moc-table tbody td { 
    height: 52px !important; 
    min-height: 52px !important; 
    padding: 7px 10px !important; 
    vertical-align: middle !important; 
} 


/* Final KPI dimensions — intentionally compact. */ 
.kpi-card { 
    height: 118px !important; 
    min-height: 118px !important; 
    max-height: 118px !important; 
    box-sizing: border-box !important; 
} 


/* ============================================================ 
   REFERENCE-STYLE DASHBOARD RHYTHM 
   The gap below is ONLY between major dashboard rows. 
   Streamlit's internal widget spacing remains untouched. 
   ============================================================ */ 

:root { 
    --dashboard-row-gap: 20px; 
    --kpi-height: 118px; 
    --table-row-height: 30px; 
} 

/* Filters → KPI row */ 
.kpi-row { 
    margin-top: var(--dashboard-row-gap) !important; 
} 

/* KPI row → MOC Register heading */ 
.section-heading { 
    margin-top: var(--dashboard-row-gap) !important; 
    margin-bottom: 0 !important; 
} 

/* MOC Register heading → search/filter toolbar */ 
.st-key-moc_toolbar { 
    margin-top: var(--dashboard-row-gap) !important; 
} 

/* Toolbar → actual table */ 
.table-shell { 
    margin-top: var(--dashboard-row-gap) !important; 
} 

/* Table → pagination */ 
.pagination-spacer { 
    height: var(--dashboard-row-gap) !important; 
    min-height: var(--dashboard-row-gap) !important; 
    margin: 0 !important; 
    padding: 0 !important; 
} 

/* Protect filter labels. */ 
.filter-label { 
    display: block !important; 
    height: auto !important; 
    min-height: 18px !important; 
    line-height: 18px !important; 
    margin: 0 0 8px 2px !important; 
    padding: 0 !important; 
    overflow: visible !important; 
} 

/* Compact, consistent table data rows. */ 
.moc-table tbody tr { 
    height: var(--table-row-height) !important; 
} 

.moc-table tbody td { 
    height: var(--table-row-height) !important; 
    min-height: var(--table-row-height) !important; 
    padding: 7px 10px !important; 
    vertical-align: middle !important; 
} 

/* ============================================================ 
   KPI CARDS — COMPACT REFERENCE PROPORTION 
   ============================================================ */ 
.kpi-card { 
    height: var(--kpi-height) !important; 
    min-height: var(--kpi-height) !important; 
    max-height: var(--kpi-height) !important; 
    box-sizing: border-box !important; 
    overflow: hidden !important; 
} 


/* FINAL KPI SIZE */ 
.kpi-card { 
    height: 118px !important; 
    min-height: 118px !important; 
    max-height: 118px !important; 
    box-sizing: border-box !important; 
} 

/* ============================================================ 
   TABLE 
   ============================================================ */ 
.table-shell { 
    width: 100%; 
    margin-top: 0 !important; 
    background: #ffffff; 
    border: 1px solid var(--border); 
    border-radius: 8px; 
    overflow: hidden; 
    box-shadow: 0 2px 8px rgba(23,59,115,.045); 
} 

.moc-table { 
    width: 100%; 
    border-collapse: collapse; 
    table-layout: fixed; 
} 

.moc-table th { 
    background: var(--blue-soft); 
    color: var(--navy); 
    border-right: 1px solid #d7e3ee; 
    border-bottom: 1px solid #cbd9e6; 
    padding: 11px 10px; 
    font-size: 12px; 
    font-weight: 750; 
    text-align: left; 
} 

.moc-table td { 
    color: #315071; 
    border-right: 1px solid #e1e8ef; 
    border-bottom: 1px solid #e3e9ef; 
    padding: 8px 10px; 
    height: 58px; 
    min-height: 58px; 
    box-sizing: border-box; 
    vertical-align: middle; 
    font-size: 11.5px; 
    font-weight: 500; 
    line-height: 1.28; 
    vertical-align: middle; 
    overflow-wrap: anywhere; 
} 

.moc-table tr:nth-child(even) td { 
    background: #fbfcfe; 
} 

.moc-table tr:hover td { 
    background: #f6faff; 
} 

.moc-table th:last-child, 
.moc-table td:last-child { 
    border-right: none; 
} 

.moc-table tbody tr { 
    height: 52px; 
} 

.moc-table tbody td { 
    vertical-align: middle; 
} 

.moc-no { 
    color: var(--navy); 
    font-weight: 650; 
} 

.status { 
    display: inline-flex; 
    align-items: center; 
    justify-content: center; 
    min-width: 57px; 
    padding: 4px 9px; 
    border-radius: 20px; 
    font-size: 10px; 
    font-weight: 750; 
} 

.status-open { 
    color: #b76a00; 
    background: #fff4dd; 
} 

.status-closed { 
    color: #14763d; 
    background: #eaf8f0; 
} 

.status-other { 
    color: #52667e; 
    background: #eef2f6; 
} 

.action-view { 
    color: var(--blue-dark); 
    font-weight: 700; 
    text-decoration: none; 
    cursor: pointer; 
} 

.action-view:hover { 
    text-decoration: underline; 
} 

.no-document { 
    color: #9aa8b7; 
} 

/* ============================================================ 
   PAGINATION 
   ============================================================ */ 
.pagination-spacer { 
    width: 100%; 
    height: 15px; 
} 

.st-key-moc_pagination [data-testid="stHorizontalBlock"] { 
    align-items: center !important; 
} 

.pagination-info { 
    color: #64768c; 
    font-size: 11px; 
    font-weight: 600; 
    line-height: 32px; 
    white-space: nowrap; 
    display: flex; 
    align-items: center; 
    justify-content: flex-end; 
    height: 32px; 
    text-align: right; 
    padding: 0 12px 0 0 !important; 
    margin: 0 !important; 
} 

.pagination-info strong { 
    color: var(--navy); 
    font-weight: 750; 
} 

.pagination-buttons { 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    width: 100%; 
    margin: 0 !important; 
    padding: 0 !important; 
} 

.st-key-moc_pagination .pagination-buttons div.stButton > button, 
.st-key-moc_pagination div.stButton > button { 
    width: 32px !important; 
    height: 32px !important; 
    min-width: 32px !important; 
    min-height: 32px !important; 
    max-width: 32px !important; 
    max-height: 32px !important; 
    margin: 0 auto !important; 
    padding: 0 !important; 
    border-radius: 7px !important; 
    background: #ffffff !important; 
    border: 1px solid #d0dce8 !important; 
    color: var(--navy) !important; 
    font-size: 15px !important; 
    line-height: 30px !important; 
} 

.st-key-moc_pagination .pagination-buttons div.stButton > button:disabled, 
.st-key-moc_pagination div.stButton > button:disabled { 
    opacity: .38 !important; 
} 

.st-key-moc_pagination [data-testid="stHorizontalBlock"] { 
    align-items: center !important; 
    gap: 8px !important; 
} 

/* Remove accidental widget label spacing */ 
div[data-testid="stButton"] > div { 
    margin: 0 !important; 
} 

@media (max-width: 1050px) { 
    .block-container { 
        padding-left: 18px !important; 
        padding-right: 18px !important; 
    } 

    .moc-table th, 
    .moc-table td { 
        font-size: 10.5px; 
        padding: 8px 10px; 
    } 
} 
</style> 
""",
    unsafe_allow_html=True,
)


# ============================================================
# DASHBOARD RENDER FUNCTION
# ============================================================
def render_dashboard():
    raw_df = get_moc_data()

    if raw_df.empty:
        st.error("No data found in Google Sheet: MOC.")
        return

    df = prepare_data(raw_df)

    # --------------------------------------------------------
    # Financial year options
    # --------------------------------------------------------
    today = date.today()

    current_fy = (
        f"{today.year}-{str(today.year + 1)[-2:]}"
        if today.month >= 4
        else f"{today.year - 1}-{str(today.year)[-2:]}"
    )

    preferred_fys = [current_fy, "2025-26"]

    data_fys = [
        clean_text(x)
        for x in df["Financial Year"].dropna().unique().tolist()
        if clean_text(x)
    ]

    year_options = []

    for fy in preferred_fys + sorted(data_fys, reverse=True):
        if fy and fy not in year_options:
            year_options.append(fy)

    if "2026-27" not in year_options:
        year_options.insert(0, "2026-27")

        # If an old browser/session contains a value no longer available,
    # reset it safely BEFORE the widget is created.
    if st.session_state["moc_year"] not in year_options:
        st.session_state["moc_year"] = year_options[0]

        # --------------------------------------------------------
    # Top filters
    # --------------------------------------------------------
    fy_col, month_col, dept_col = st.columns(
        [1, 1, 1],
        gap="small",
    )

    with fy_col:
        st.markdown(
            "<div class='filter-label'>Financial Year</div>",
            unsafe_allow_html=True,
        )

        selected_year = st.selectbox(
            "Financial Year",
            year_options,
            key="moc_year",
            on_change=reset_dependent_filters,
            label_visibility="collapsed",
        )

    fy_df = df[df["Financial Year"] == selected_year].copy()

    month_rows = (
        fy_df[["Month Key", "Month Display"]]
        .dropna(subset=["Month Key"])
        .drop_duplicates()
        .sort_values("Month Key", ascending=False)
    )

    month_options = ["All Months"] + month_rows["Month Display"].tolist()

    if st.session_state["moc_month"] not in month_options:
        st.session_state["moc_month"] = "All Months"

    with month_col:
        st.markdown(
            "<div class='filter-label'>Month</div>",
            unsafe_allow_html=True,
        )

        selected_month = st.selectbox(
            "Month",
            month_options,
            key="moc_month",
            on_change=reset_page,
            label_visibility="collapsed",
        )

    dept_source = fy_df.copy()

    if selected_month != "All Months":
        dept_source = dept_source[
            dept_source["Month Display"] == selected_month
            ]

    department_values = sorted(
        {
            clean_text(value)
            for value in dept_source["Department"].dropna()
            if clean_text(value)
        },
        key=str.lower,
    )

    department_options = ["All Departments"] + department_values

    if st.session_state["moc_department"] not in department_options:
        st.session_state["moc_department"] = "All Departments"

    with dept_col:
        st.markdown(
            "<div class='filter-label'>Department</div>",
            unsafe_allow_html=True,
        )

        selected_department = st.selectbox(
            "Department",
            department_options,
            key="moc_department",
            on_change=reset_page,
            label_visibility="collapsed",
        )

        # --------------------------------------------------------
    # Apply filters
    # --------------------------------------------------------
    filtered_df = df[df["Financial Year"] == selected_year].copy()

    if selected_month != "All Months":
        filtered_df = filtered_df[
            filtered_df["Month Display"] == selected_month
            ].copy()

    if selected_department != "All Departments":
        filtered_df = filtered_df[
            filtered_df["Department"].map(clean_text)
            == selected_department
            ].copy()

        # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------
    total_moc = len(filtered_df)

    open_moc = int(
        filtered_df["Status"].map(is_open_status).sum()
    )

    closed_moc = int(
        filtered_df["Status"].map(is_closed_status).sum()
    )

    closure_percentage = (
        closed_moc / total_moc * 100
        if total_moc
        else 0
    )

    pending_over_15 = calculate_pending_over_15(filtered_df)

    k1, k2, k3, k4, k5 = st.columns(
        [1, 1, 1, 1, 1.12],
        gap="small",
    )

    cards = [
        (
            "TOTAL MOC",
            str(total_moc),
            "Records in selected period",
            "blue",
        ),
        (
            "OPEN MOC",
            str(open_moc),
            "Currently open",
            "orange",
        ),
        (
            "CLOSED MOC",
            str(closed_moc),
            "Completed / closed",
            "green",
        ),
        (
            "MOC CLOSURE %",
            f"{closure_percentage:.1f}%",
            "Closed ÷ total",
            "blue",
        ),
        (
            "MoC PENDING > 15 DAYS",
            str(pending_over_15),
            "Pending at CFT / TRC / HOD",
            "pending",
        ),
    ]

    for column, (label, value, sub, accent) in zip(
            [k1, k2, k3, k4, k5],
            cards,
    ):
        value_class = accent

        with column:
            st.markdown(
                f""" 
                <div class="kpi-card {accent}"> 
                    <div class="kpi-label">{html.escape(label)}</div> 
                    <div class="kpi-value {value_class}"> 
                        {html.escape(value)} 
                    </div> 
                    <div class="kpi-sub">{html.escape(sub)}</div> 
                </div> 
                """,
                unsafe_allow_html=True,
            )

            # --------------------------------------------------------
    # MOC Register heading
    # --------------------------------------------------------
    st.markdown(
        """ 
        <div class="section-heading"> 
            <div class="section-title">MOC Register</div> 
        </div> 
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Register toolbar
    # --------------------------------------------------------
    with st.container(key="moc_toolbar"):
        search_col, all_col, closed_col, open_col, refresh_col = st.columns(
            [2.9, 0.52, 0.78, 0.70, 0.82],
            gap="small",
        )

        with search_col:
            search_text = st.text_input(
                "Search",
                placeholder=(
                    "Search MOC No., Department, Section, "
                    "Requestor, Description..."
                ),
                label_visibility="collapsed",
                key="moc_search",
            )

        with all_col:
            if st.button(
                    "All",
                    use_container_width=True,
                    key="moc_all",
            ):
                st.session_state["moc_status_filter"] = "All"
                st.session_state["moc_page"] = 1
                st.rerun()

        with closed_col:
            if st.button(
                    "Closed",
                    use_container_width=True,
                    key="moc_closed",
            ):
                st.session_state["moc_status_filter"] = "Closed"
                st.session_state["moc_page"] = 1
                st.rerun()

        with open_col:
            if st.button(
                    "Open",
                    use_container_width=True,
                    key="moc_open",
            ):
                st.session_state["moc_status_filter"] = "Open"
                st.session_state["moc_page"] = 1
                st.rerun()

        with refresh_col:
            if st.button(
                    "↻",
                    use_container_width=True,
                    key="moc_refresh",
                    help="Refresh data from Google Sheet",
            ):
                get_moc_data.clear()
                st.session_state["moc_page"] = 1
                st.rerun()

                # --------------------------------------------------------
    # Search + status filter
    # --------------------------------------------------------
    display_df = filtered_df.copy()

    if search_text.strip():
        query = search_text.strip().lower()

        searchable_columns = [
            "MOC No",
            "Department",
            "Section",
            "Requestor Name",
            "Description of Change",
            "Status",
        ]

        mask = pd.Series(
            False,
            index=display_df.index,
        )

        for column in searchable_columns:
            mask |= (
                display_df[column]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    query,
                    regex=False,
                    na=False,
                )
            )

        display_df = display_df[mask].copy()

    status_filter = st.session_state["moc_status_filter"]

    if status_filter == "Open":
        display_df = display_df[
            display_df["Status"].map(is_open_status)
        ].copy()

    elif status_filter == "Closed":
        display_df = display_df[
            display_df["Status"].map(is_closed_status)
        ].copy()

        # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------
    total_entries = len(display_df)

    total_pages = max(
        1,
        (total_entries + ROWS_PER_PAGE - 1)
        // ROWS_PER_PAGE,
    )

    if st.session_state["moc_page"] > total_pages:
        st.session_state["moc_page"] = total_pages

    page_number = st.session_state["moc_page"]

    start_index = (
                          page_number - 1
                  ) * ROWS_PER_PAGE

    end_index = start_index + ROWS_PER_PAGE

    page_df = display_df.iloc[
        start_index:end_index
    ].copy()

    # --------------------------------------------------------
    # HTML table
    # --------------------------------------------------------
    rows = []

    for _, row in page_df.iterrows():
        moc_no = clean_text(row["MOC No"])
        department = clean_text(row["Department"])
        section = clean_text(row["Section"])

        # Blank Requestor Name remains blank.
        requestor = clean_text(row["Requestor Name"])

        description = clean_text(
            row["Description of Change"]
        )

        status = clean_text(row["Status"])
        status_lower = status.lower()

        if status_lower in {"closed", "completed"}:
            status_html = (
                '<span class="status status-closed">'
                "CLOSED"
                "</span>"
            )
        elif status_lower in {
            "open",
            "ongoing",
            "in progress",
        }:
            status_html = (
                '<span class="status status-open">'
                "OPEN"
                "</span>"
            )
        else:
            status_html = (
                '<span class="status status-other">'
                f"{html.escape(status) if status else '—'}"
                "</span>"
            )

        document_link = _normalise_document_url(
            row["Attach MOC Softcopy Link"]
        )

        if document_link:
            safe_link = html.escape(
                document_link,
                quote=True,
            )

            document_html = (
                f'<a class="action-view" '
                f'href="{safe_link}" '
                'target="_blank" '
                'rel="noopener noreferrer" '
                'referrerpolicy="no-referrer" '
                'title="Open attached MOC document">'
                "Open Document"
                "</a>"
            )
        else:
            document_html = (
                '<span class="no-document">—</span>'
            )

        rows.append(
            "<tr>"
            f'<td class="moc-no">{html.escape(moc_no)}</td>'
            f"<td>{html.escape(department)}</td>"
            f"<td>{html.escape(section)}</td>"
            f"<td>{html.escape(requestor)}</td>"
            f"<td>{html.escape(description)}</td>"
            f"<td>{status_html}</td>"
            f"<td>{document_html}</td>"
            "</tr>"
        )

    if rows:
        table_rows_html = "".join(rows)
    else:
        table_rows_html = (
            "<tr>"
            '<td colspan="7" style="'
            "text-align:center;"
            "color:#8a98a9;"
            "padding:28px;"
            "font-size:12px;"
            '">'
            "No MOC records found for the selected filters."
            "</td>"
            "</tr>"
        )

        # IMPORTANT:
    # The HTML is emitted as one compact string. This prevents
    # Streamlit from rendering tags such as <thead>/<tr> as text.
    table_html = (
        '<div class="table-shell">'
        '<table class="moc-table">'
        "<colgroup>"
        '<col style="width:11%;">'
        '<col style="width:10%;">'
        '<col style="width:9%;">'
        '<col style="width:13%;">'
        '<col style="width:36%;">'
        '<col style="width:9%;">'
        '<col style="width:12%;">'
        "</colgroup>"
        "<thead>"
        "<tr>"
        "<th>MOC No.</th>"
        "<th>Department</th>"
        "<th>Section</th>"
        "<th>Requestor Name</th>"
        "<th>Description of Change</th>"
        "<th>Status</th>"
        "<th>MOC Document</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        f"{table_rows_html}"
        "</tbody>"
        "</table>"
        "</div>"
    )

    st.markdown(
        table_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Bottom-right pagination
    # --------------------------------------------------------
    page_to = min(
        end_index,
        total_entries,
    )

    if total_entries:
        records_text = (
            f"{page_to} of {total_entries} records"
        )
    else:
        records_text = "0 of 0 records"

    with st.container(key="moc_pagination"):
        # Extra breathing room keeps navigation visually separated
        # from the table. The controls share one horizontal baseline.
        st.markdown(
            '<div class="pagination-spacer"></div>',
            unsafe_allow_html=True,
        )

        p_spacer, p_info, p_prev, p_next = st.columns(
            [7.55, 2.15, 0.42, 0.42],
            gap="small",
        )

        with p_info:
            st.markdown(
                f""" 
                <div class=\"pagination-info\"> 
                    <strong>{records_text}</strong> 
                    &nbsp;&nbsp;·&nbsp;&nbsp; 
                    Page&nbsp;<strong>{page_number}</strong> 
                    &nbsp;of&nbsp;<strong>{total_pages}</strong> 
                </div> 
                """,
                unsafe_allow_html=True,
            )

        with p_prev:
            if st.button(
                    "‹",
                    use_container_width=True,
                    key="moc_previous",
                    disabled=(page_number <= 1),
                    help="Previous page",
            ):
                st.session_state["moc_page"] = max(
                    1,
                    page_number - 1,
                )
                st.rerun()

        with p_next:
            if st.button(
                    "›",
                    use_container_width=True,
                    key="moc_next",
                    disabled=(page_number >= total_pages),
                    help="Next page",
            ):
                st.session_state["moc_page"] = min(
                    total_pages,
                    page_number + 1,
                )
                st.rerun()


st.markdown(
    ''' 
    <style> 
    /* ============================================================ 
       FINAL REFERENCE-MATCH LAYOUT 
       One consistent gap between each MAJOR dashboard component. 
       Internal widget spacing is intentionally left unchanged. 
       ============================================================ */ 

    :root { 
        --major-row-gap: 12px; 
        --kpi-card-height: 90px; 
    } 

    /* KPI cards: genuinely 90px high */ 
    .kpi-card { 
        height: 90px !important; 
        min-height: 90px !important; 
        max-height: 90px !important; 
        box-sizing: border-box !important; 
        padding: 8px 18px !important; 
        overflow: hidden !important; 
    } 

    .kpi-label { 
        font-size: 12px !important; 
        line-height: 1.15 !important; 
    } 

    .kpi-value { 
        margin-top: 10px !important; 
        font-size: 27px !important; 
        line-height: 1 !important; 
    } 

    .kpi-sub { 
        margin-top: 10px !important; 
        font-size: 10px !important; 
        line-height: 1.1 !important; 
    } 

    /* KPI -> MOC Register 
       Target the Streamlit element containing the heading so 
       the margin cannot collapse inside the HTML heading. */ 
    .element-container:has(.section-heading) { 
        margin-top: var(--major-row-gap) !important; 
    } 

    .section-heading { 
        margin-top: 0 !important; 
        margin-bottom: 0 !important; 
    } 

    /* MOC Register -> search/status toolbar */ 
    .st-key-moc_toolbar { 
        margin-top: var(--major-row-gap) !important; 
    } 

    /* Search/status toolbar -> actual table */ 
    .element-container:has(.table-shell) { 
        margin-top: var(--major-row-gap) !important; 
    } 

    .table-shell { 
        margin-top: 0 !important; 
    } 

    /* Table -> pagination */ 
    .pagination-spacer { 
        height: var(--major-row-gap) !important; 
        min-height: var(--major-row-gap) !important; 
        max-height: var(--major-row-gap) !important; 
        margin: 0 !important; 
        padding: 0 !important; 
    } 

    /* Protect filter titles from clipping */ 
    .filter-label { 
        height: auto !important; 
        min-height: 18px !important; 
        line-height: 18px !important; 
        margin: 0 0 8px 2px !important; 
        padding: 0 !important; 
        overflow: visible !important; 
    } 

    /* Prevent accidental offsets */ 
    .section-heading, 
    .section-title, 
    .st-key-moc_toolbar, 
    .table-shell, 
    .kpi-card { 
        transform: none !important; 
    } 
    </style> 
    ''',
    unsafe_allow_html=True,
)

# ============================================================
# AUTOMATIC DATA REFRESH
# ============================================================
# Streamlit fragments allow the dashboard to rerun the data/UI
# every 20 seconds without requiring the user to click Refresh.
#
# If the installed Streamlit version does not support fragments,
# the normal app still works and the manual Refresh icon remains.
if hasattr(st, "fragment"):
    @st.fragment(run_every=f"{DATA_REFRESH_SECONDS}s")
    def _moc_dashboard_fragment():
        render_dashboard()


    _moc_dashboard_fragment()
else:
    render_dashboard()

