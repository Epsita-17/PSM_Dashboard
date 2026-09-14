import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import re
import mimetypes
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# OPTIONAL AUTO REFRESH
# =========================================================
try:
    from streamlit_autorefresh import st_autorefresh

    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="PSSR Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ACTION STATE
# Upload / View use Streamlit modal dialogs exactly like PT.
# =========================================================

if "upload_pssr_no" not in st.session_state:
    st.session_state.upload_pssr_no = ""

if "view_pssr_no" not in st.session_state:
    st.session_state.view_pssr_no = ""

if "open_upload_pssr_dialog" not in st.session_state:
    st.session_state.open_upload_pssr_dialog = False

if "open_view_pssr_dialog" not in st.session_state:
    st.session_state.open_view_pssr_dialog = False

if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(
        interval=60 * 1000,
        key="pssr_auto_refresh"
    )

# =========================================================
# GOOGLE SHEET SETTINGS
# =========================================================
SPREADSHEET_ID = (
    "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
)

PSSR_SHEET_NAME = "PSSR"

PSSR_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv"
    f"&sheet={PSSR_SHEET_NAME}"
)


# =========================================================
# LOAD GOOGLE SHEET DATA
# =========================================================
@st.cache_data(ttl=30)
def get_pssr_data():
    try:

        data = pd.read_csv(PSSR_CSV_URL)

        data.columns = (
            data.columns
            .astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.strip()
        )

        for col in data.columns:

            if data[col].dtype == "object":
                data[col] = (
                    data[col]
                    .astype(str)
                    .str.replace(
                        "\xa0",
                        " ",
                        regex=False
                    )
                    .str.strip()
                )

        return data.replace({
            "nan": "",
            "NaN": "",
            "NAN": ""
        })

    except Exception as exc:

        st.error(
            f"Unable to load PSSR Google Sheet: {exc}"
        )

        return pd.DataFrame()


df = get_pssr_data()

if df.empty:
    st.error(
        "No data found in the PSSR Google Sheet."
    )

    st.stop()

# =========================================================
# DOCUMENT STORAGE
# Same working upload/view mechanism as pt.py,
# adapted only for PSSR reports.
# =========================================================

DOCUMENT_FOLDER = Path(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "pssr_documents"
    )
)

DOCUMENT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def safe_pssr_folder_name(pssr_no):
    value = str(pssr_no).strip()

    value = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        value
    )

    return value or "unknown_pssr"


def get_pssr_document_folder(pssr_no):
    folder = (
            DOCUMENT_FOLDER
            / safe_pssr_folder_name(pssr_no)
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def get_pssr_documents(pssr_no):
    folder = get_pssr_document_folder(
        pssr_no
    )

    return sorted(
        [
            p
            for p in folder.iterdir()
            if p.is_file()
        ],
        key=lambda p: p.name.lower()
    )


def save_pssr_document(
        pssr_no,
        uploaded_file
):
    folder = get_pssr_document_folder(
        pssr_no
    )

    original_name = Path(
        uploaded_file.name
    ).name

    stem = Path(
        original_name
    ).stem

    suffix = Path(
        original_name
    ).suffix

    safe_stem = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        stem
    ).strip("._-")

    safe_stem = (
            safe_stem
            or "document"
    )

    target = (
            folder
            / f"{safe_stem}{suffix}"
    )

    counter = 1

    while target.exists():
        target = (
                folder
                / f"{safe_stem}_{counter}{suffix}"
        )

        counter += 1

    target.write_bytes(
        uploaded_file.getbuffer()
    )

    return target


def get_pssr_document_mime_type(path):
    mime_type, _ = mimetypes.guess_type(
        str(path)
    )

    return (
            mime_type
            or "application/octet-stream"
    )


# =========================================================
# EXACT PSSR HEADER DETAILS
# =========================================================
REQUIRED_HEADERS = [
    "Sr No",
    "PSSR No.",
    "Department",
    "Section",
    "PSSR Description",
    "Due Date",
    "PSSR Completion Date",
    "Overdue/Pending/Completed",
    "Remarks"
]


def normalize_header(value):
    return (
        str(value)
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .lower()
    )


header_lookup = {
    normalize_header(col): col
    for col in df.columns
}


def find_header(header):
    key = normalize_header(header)

    if key in header_lookup:
        return header_lookup[key]

    return None


COL_SR = find_header("Sr No")
COL_PSSR_NO = find_header("PSSR No.")
COL_DEPARTMENT = find_header("Department")
COL_SECTION = find_header("Section")
COL_DESCRIPTION = find_header("PSSR Description")
COL_DUE_DATE = find_header("Due Date")
COL_COMPLETION_DATE = find_header(
    "PSSR Completion Date"
)
COL_STATUS = find_header(
    "Overdue/Pending/Completed"
)
COL_REMARKS = find_header("Remarks")

# =========================================================
# GOOGLE SHEET VIEW LINK
# =========================================================
COL_REPORT_LINK = None

for _candidate in [
    "View Report",
    "Report Link",
    "Document Link",
    "Document",
    "Report",
    "PSSR Report"
]:
    COL_REPORT_LINK = find_header(_candidate)
    if COL_REPORT_LINK:
        break


def get_google_sheet_row_url(row_index):
    sheet_row = int(row_index) + 2
    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/edit"
        f"#gid=0&range=A{sheet_row}"
    )


def get_report_link(row, row_index):
    if COL_REPORT_LINK:
        raw = str(row.get(COL_REPORT_LINK, "")).strip()

        if raw and raw.lower() not in {"nan", "none"}:

            if raw.startswith(("http://", "https://")):
                return raw

            match = re.search(
                r'https?://[^"\\s)]+',
                raw
            )

            if match:
                return match.group(0)

    return get_google_sheet_row_url(row_index)


missing_columns = []

for name, column in [
    ("Sr No", COL_SR),
    ("PSSR No.", COL_PSSR_NO),
    ("Department", COL_DEPARTMENT),
    ("Section", COL_SECTION),
    ("PSSR Description", COL_DESCRIPTION),
    ("Due Date", COL_DUE_DATE),
    ("PSSR Completion Date", COL_COMPLETION_DATE),
    ("Overdue/Pending/Completed", COL_STATUS),
    ("Remarks", COL_REMARKS)
]:

    if column is None:
        missing_columns.append(name)

if missing_columns:
    st.error(
        "The following PSSR headers are missing:"
    )

    st.write(missing_columns)

    st.write(
        "Headers found in Google Sheet:"
    )

    st.write(df.columns.tolist())

    st.stop()

# =========================================================
# DATA PREPARATION
# =========================================================
work = df.copy()

work["_department"] = (
    work[COL_DEPARTMENT]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_section"] = (
    work[COL_SECTION]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_description"] = (
    work[COL_DESCRIPTION]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_pssr_no"] = (
    work[COL_PSSR_NO]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_remarks"] = (
    work[COL_REMARKS]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_status_raw"] = (
    work[COL_STATUS]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

work["_due_date"] = pd.to_datetime(
    work[COL_DUE_DATE],
    errors="coerce",
    dayfirst=True
)

work["_completion_date"] = pd.to_datetime(
    work[COL_COMPLETION_DATE],
    errors="coerce",
    dayfirst=True
)


# =========================================================
# STATUS NORMALIZATION
# =========================================================
def normalize_status(row):
    status = str(
        row["_status_raw"]
    ).strip().lower()

    if "overdue" in status:
        return "Overdue"

    if "pending" in status:
        return "Pending"

    if "completed" in status or "complete" in status:
        return "Completed"

    # If status is blank, use completion date
    if pd.notna(row["_completion_date"]):
        return "Completed"

    # Otherwise determine overdue from Due Date
    if pd.notna(row["_due_date"]):

        today = pd.Timestamp.today().normalize()

        if row["_due_date"] < today:
            return "Overdue"

    return "Pending"


work["_status"] = work.apply(
    normalize_status,
    axis=1
)

# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>

/* ======================================================
   PAGE
   ====================================================== */

#MainMenu,
header,
footer,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display:none !important;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    margin:0 !important;
    padding:0 !important;
}

[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    width:100% !important;
    max-width:none !important;
    margin:0 !important;
    padding:0 8px !important;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #f8fbfd 0%,
            #f4f9fc 55%,
            #edf5f9 100%
        ) !important;
}

[data-testid="stVerticalBlock"] {
    gap:0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap:7px !important;
}


/* ======================================================
   FILTERS
   ====================================================== */

.filter-title {
    color:#193d77;
    font-size:13px;
    font-weight:900;
    margin:0 0 4px 3px !important;
    line-height:18px !important;
    position:relative !important;
    top:-14px !important;
    z-index:100 !important;
    display:block !important;
    height:18px !important;
    pointer-events:none !important;
}

div[data-baseweb="select"] > div {
    height:40px !important;
    min-height:30px !important;
    border-radius:6px !important;
    background:#ffffff !important;
    border:1px solid #d2dce3 !important;
}

div[data-baseweb="select"] * {
    color:#26384a !important;
    font-size:13px !important;
}

div[data-baseweb="select"] svg {
    fill:#193d77 !important;
}


/* ======================================================
   KPI CARDS
   ====================================================== */

.kpi-card {
    height:118px;
    border-top:4px solid #164b91;
    position:relative;
    overflow:hidden;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 30%,
            #fcfdfe 60%,
            #f3f8fa 100%
        );

    border:1px solid #dfe7eb;
    border-radius:9px;

    box-shadow:
        0 8px 20px rgba(55,90,110,.09),
        0 2px 5px rgba(55,90,110,.06),
        inset 0 1px 0 #ffffff;
}

.kpi-label {
    color:#193d77;
    font-size:14px;
    font-weight:950;
    text-align:center;
    padding-top:12px;
}

.kpi-value {
    color:#164b91;
    font-size:45px;
    line-height:1;
    font-weight:950;
    text-align:center;
    margin-top:9px;
}

.kpi-value.red {
    color:#d9272e;
}

/* ======================================================
   COMPLIANCE
   ====================================================== */

.compliance-card {
    height:118px;
    border-top:4px solid #164b91;
    position:relative;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f3f8fa
        );

    border:1px solid #dfe7eb;
    border-radius:9px;

    box-shadow:
        0 8px 20px rgba(55,90,110,.09),
        inset 0 1px 0 #ffffff;
}

.compliance-title {
    position:absolute;
    top:10px;
    left:0;
    right:0;
    text-align:center;

    font-size:11px;
    color:#193d77;
    font-weight:950;
}

.donut-wrap {
    width:80px;
    height:80px;
    position:relative;
    margin-top:8px;
}

.donut-svg {
    width:80px;
    height:80px;
    transform:rotate(-90deg);
}

.donut-bg {
    fill:none;
    stroke:#dfe5ea;
    stroke-width:10;
}

.donut-progress {
    fill:none;
    stroke:#164b91;
    stroke-width:10;
}

.donut-text {
    position:absolute;
    top:27px;
    left:0;
    right:0;

    text-align:center;

    font-size:22px;
    font-weight:950;
    color:#172b43;
}

.compliance-sub {
    position:absolute;
    bottom:7px;
    left:0;
    right:0;

    text-align:center;

    font-size:9px;
    color:#52677b;
}


/* ======================================================
   CHART PANELS
   ====================================================== */

.chart-panel {
    background:#ffffff;

    border:1px solid #dfe7eb;
    border-radius:9px;

    overflow:hidden;

    box-shadow:
        0 7px 18px rgba(55,90,110,.08),
        0 2px 5px rgba(55,90,110,.05);
}

.chart-title {
    height:35px;

    display:flex;
    align-items:center;

    padding:0 15px;

    color:#193d77;

    font-size:11px;
    font-weight:950;

    background:#ffffff;

    border-bottom:1px solid #edf1f4;
}

.chart-content {
    padding:2px 5px 5px;
    background:#ffffff;
}


/* ======================================================
   REGISTER
   ====================================================== */

.register-panel {
    background:#ffffff;

    border:1px solid #dfe7eb;
    border-radius:9px;

    overflow:hidden;

    box-shadow:
        0 7px 18px rgba(55,90,110,.08),
        0 2px 5px rgba(55,90,110,.05);
}

.register-title {
    height:31px;

    display:flex;
    align-items:center;

    padding:0 14px;

    color:#193d77;

    font-size:11px;
    font-weight:950;

    background:#ffffff;

    border-bottom:1px solid #e5ebef;
}

.pssr-table {
    width:100%;
    border-collapse:collapse;
    table-layout:fixed;

    font-family:Arial,sans-serif;
    font-size:10px;
}

.pssr-table th {
    background:#164b91;
    color:#ffffff;

    font-weight:900;

    padding:8px 5px;

    text-align:center;

    border-right:
        1px solid rgba(255,255,255,.35);

    white-space:nowrap;
}

.pssr-table td {
    height:36px;

    padding:5px 7px;

    text-align:center;

    border-bottom:1px solid #e5ebef;
    border-right:1px solid #e8edf0;

    color:#26384a;

    background:#ffffff;

    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
}

.pssr-table tr:nth-child(even) td {
    background:#fbfdfe;
}

.pssr-table td.left {
    text-align:left;
}

.status-badge {
    display:inline-flex;

    align-items:center;
    justify-content:center;

    min-width:68px;

    padding:4px 8px;

    border-radius:4px;

    font-size:9px;
    font-weight:900;
}

.status-completed {
    background:#e6f5ec;
    color:#27834c;
}

.status-pending {
    background:#fff5dc;
    color:#bd7910;
}

.status-overdue {
    background:#fde4e4;
    color:#d9272e;
}

.icon-btn {
    display:inline-flex;

    align-items:center;
    justify-content:center;

    width:25px;
    height:25px;

    border:1px solid #cbd9e2;
    border-radius:5px;

    background:#ffffff;
    color:#164b91;

    font-size:13px;
    text-decoration:none;
}

.remark-icon {
    font-size:16px;
    color:#164b91;
}

.register-footer {
    height:35px;

    display:flex;
    align-items:center;
    justify-content:space-between;

    padding:0 14px;

    color:#586b7b;
    font-size:9px;

    background:#ffffff;
}

.pagination {
    display:flex;
    align-items:center;
    gap:5px;
}

.page-btn {
    min-width:27px;
    height:25px;

    display:flex;
    align-items:center;
    justify-content:center;

    border:1px solid #d5dfe5;
    border-radius:5px;

    background:#ffffff;
    color:#26384a;

    font-size:10px;
}

.page-current {
    background:#164b91;
    border-color:#164b91;
    color:#ffffff;
    font-weight:900;
}


/* ======================================================
   FOOTER
   ====================================================== */

.footer {
    height:20px;

    display:flex;
    align-items:center;
    justify-content:center;

    color:#587084;

    background:
        linear-gradient(
            180deg,
            #f8fbfd,
            #eaf2f6
        );

    font-size:9px;
    font-weight:800;

    border-top:1px solid #d7e3ea;
}


</style>
""",
    unsafe_allow_html=True
)

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

    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
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
        margin-top: -0px !important;
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

    left: 15px;

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

    height: 7px;

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

                PRE-STARTUP SAFETY REVIEW (PSSR)

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

# =========================================================
# MONTH + DEPARTMENT FILTER
# =========================================================
filter_month, filter_department = st.columns(
    [1, 1],
    gap="small"
)

with filter_month:
    st.markdown(
        "<div class='filter-title'>MONTH</div>",
        unsafe_allow_html=True
    )

    valid_dates = (
        work["_due_date"]
        .dropna()
    )

    if not valid_dates.empty:

        month_values = (
            valid_dates
            .dt.to_period("M")
            .drop_duplicates()
            .sort_values(
                ascending=False
            )
        )

        month_labels = [
            period.strftime("%B %Y")
            for period in month_values
        ]

    else:

        month_labels = []

    month_options = [
                        "All Months"
                    ] + month_labels

    selected_month = st.selectbox(
        "Month",
        month_options,
        index=0,
        label_visibility="collapsed",
        key="pssr_month"
    )

with filter_department:
    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )

    departments = sorted(
        [
            str(x).strip()
            for x in
            work["_department"].unique()
            if str(x).strip()
        ],
        key=lambda x: x.lower()
    )

    department_options = [
                             "All Departments"
                         ] + departments

    selected_department = st.selectbox(
        "Department",
        department_options,
        index=0,
        label_visibility="collapsed",
        key="pssr_department"
    )

# =========================================================
# APPLY FILTER
# =========================================================
filtered_df = work.copy()

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["_department"]
        == selected_department
        ]

if selected_month != "All Months":
    month_period = pd.Period(
        pd.to_datetime(
            selected_month,
            format="%B %Y"
        ),
        freq="M"
    )

    filtered_df = filtered_df[
        filtered_df["_due_date"]
        .dt
        .to_period("M")
        == month_period
        ]

# =========================================================
# KPI CALCULATIONS
# =========================================================
total_pssr = len(filtered_df)

completed = int(
    (
            filtered_df["_status"]
            == "Completed"
    ).sum()
)

pending = int(
    (
            filtered_df["_status"]
            == "Pending"
    ).sum()
)

overdue = int(
    (
            filtered_df["_status"]
            == "Overdue"
    ).sum()
)

compliance = (
    completed / total_pssr * 100
    if total_pssr > 0
    else 0
)

# =========================================================
# KPI ROW
# =========================================================
k1, k2, k3, k4, k5 = st.columns(
    [1.05, 1.05, 1.05, 1.05, .95],
    gap="small"
)

# ---------------------------------------------------------
# TOTAL PSSR
# ---------------------------------------------------------
with k1:
    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                TOTAL PSSR
            </div>

            <div class="kpi-value">
                {total_pssr}
            </div>

        </div>
        """
    )

# ---------------------------------------------------------
# COMPLETED
# ---------------------------------------------------------
with k2:
    completed_pct = (
        completed / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                COMPLETED PSSR
            </div>

            <div class="kpi-value">
                {completed}
            </div>

        </div>
        """
    )

# ---------------------------------------------------------
# PENDING
# ---------------------------------------------------------
with k3:
    pending_pct = (
        pending / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                PENDING PSSR
            </div>

            <div class="kpi-value red">
                {pending}
            </div>

        </div>
        """
    )

# ---------------------------------------------------------
# OVERDUE
# ---------------------------------------------------------
with k4:
    overdue_pct = (
        overdue / total_pssr * 100
        if total_pssr
        else 0
    )

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                OVERDUE PSSR
            </div>

            <div class="kpi-value red">
                {overdue}
            </div>

        </div>
        """
    )

# ---------------------------------------------------------
# COMPLIANCE
# ---------------------------------------------------------
with k5:
    radius = 40

    circumference = (
            2 * 3.14159265359 * radius
    )

    progress = (
            circumference
            * min(
        max(compliance, 0),
        100
    )
            / 100
    )

    st.html(
        f"""
        <div class="compliance-card">

            <div class="compliance-title">
                PSSR COMPLIANCE
            </div>

            <div class="donut-wrap">

                <svg
                    class="donut-svg"
                    viewBox="0 0 100 100"
                >

                    <circle
                        class="donut-bg"
                        cx="50"
                        cy="50"
                        r="{radius}"
                    />

                    <circle
                        class="donut-progress"
                        cx="50"
                        cy="50"
                        r="{radius}"
                        stroke-dasharray="
                            {progress:.2f}
                            {circumference:.2f}
                        "
                    />

                </svg>

                <div class="donut-text">
                    {compliance:.1f}%
                </div>

            </div>

            <div class="compliance-sub">

            </div>

        </div>
        """
    )

# =========================================================
# CHART ROW
# =========================================================
chart_left, chart_right = st.columns(
    [1.03, .97],
    gap="small"
)

# =========================================================
# DEPARTMENT-WISE PSSR
# =========================================================
with chart_left:
    st.html(
        """
        <div class="chart-panel">

            <div class="chart-title">
                NO. OF PSSR PERFORMED BY DEPARTMENT
            </div>

            <div class="chart-content">
        """
    )

    department_counts = (
        filtered_df["_department"]
        .replace(
            "",
            "Not Specified"
        )
        .value_counts()
        .sort_values(
            ascending=False
        )
    )

    fig_department = go.Figure()

    fig_department.add_trace(
        go.Bar(

            x=department_counts.index.tolist(),

            y=department_counts.values.tolist(),

            text=department_counts.values.tolist(),

            textposition="outside",

            cliponaxis=False,

            marker=dict(

                color=[
                    "#164b91", "#f28c00", "#2e8b57", "#8e44ad",
                    "#e74c3c", "#16a085", "#d35400", "#2980b9",
                    "#c0392b", "#7f8c8d"
                ][:len(department_counts)],

                line=dict(
                    color="#0a2d5a",
                    width=1
                )

            ),

            hovertemplate=(
                "%{x}<br>"
                "No. of PSSR: %{y}"
                "<extra></extra>"
            )
        )
    )

    max_value = (
        int(department_counts.max())
        if not department_counts.empty
        else 1
    )

    fig_department.update_layout(

        height=190,

        margin=dict(
            l=45,
            r=18,
            t=15,
            b=43
        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(
            family="Arial",
            color="#111111"
        ),

        yaxis=dict(

            title="No. of PSSR",

            range=[
                0,
                max(
                    max_value + 3,
                    5
                )
            ],

            dtick=5
            if max_value >= 10
            else 1,

            gridcolor="#dce7ed",

            zeroline=False,

            tickfont=dict(
                size=9
            ),

            title_font=dict(
                size=10
            )

        ),

        xaxis=dict(

            title="Department",

            tickfont=dict(
                size=9
            ),

            showgrid=False,

            title_font=dict(
                size=10
            )

        ),

        showlegend=False,

        bargap=.32

    )

    st.plotly_chart(

        fig_department,

        use_container_width=True,

        config={
            "displayModeBar": False,
            "responsive": True
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# STATUS SUMMARY
# =========================================================
with chart_right:
    st.html(
        """
        <div class="chart-panel">

            <div class="chart-title">
                PSSR STATUS SUMMARY
            </div>

            <div class="chart-content">
        """
    )

    status_labels = [
        "Completed",
        "Pending",
        "Overdue"
    ]

    status_values = [
        completed,
        pending,
        overdue
    ]

    fig_status = go.Figure()

    fig_status.add_trace(

        go.Pie(

            labels=status_labels,

            values=status_values,

            hole=.55,

            sort=False,

            direction="clockwise",

            textinfo="none",

            marker=dict(

                colors=[
                    "#164b91",
                    "#e51f28",
                    "#f36d72"
                ],

                line=dict(
                    color="#ffffff",
                    width=2
                )

            ),

            hovertemplate=(
                "%{label}: %{value}"
                "<extra></extra>"
            )

        )

    )

    fig_status.update_layout(

        height=190,

        margin=dict(
            l=5,
            r=5,
            t=0,
            b=0
        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        showlegend=True,

        legend=dict(

            orientation="v",

            x=.68,

            y=.50,

            xanchor="left",

            yanchor="middle",

            font=dict(
                family="Arial",
                size=10,
                color="#26384a"
            ),

            bgcolor="rgba(255,255,255,0)",

            itemsizing="constant"

        ),

        annotations=[

            dict(

                text=(
                    f"<b>{total_pssr}</b>"
                    "<br>"
                    "<span "
                    "style='font-size:10px'>"
                    "TOTAL"
                    "</span>"
                ),

                x=.50,

                y=.50,

                xref="paper",

                yref="paper",

                showarrow=False,

                align="center",

                font=dict(

                    family="Arial",

                    size=24,

                    color="#172b43"

                )

            )

        ]

    )

    st.plotly_chart(

        fig_status,

        use_container_width=True,

        config={
            "displayModeBar": False,
            "responsive": True
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# PSSR REGISTER
# =========================================================
st.html(
    """
    <div class="register-panel">

        <div class="register-title">
            PSSR REGISTER
        </div>
    """
)

# =========================================================
# PAGINATION
# =========================================================
PAGE_SIZE = 5

if "pssr_page" not in st.session_state:
    st.session_state.pssr_page = 1

total_pages = max(
    1,
    (
            len(filtered_df)
            + PAGE_SIZE
            - 1
    )
    // PAGE_SIZE
)

if st.session_state.pssr_page > total_pages:
    st.session_state.pssr_page = total_pages

page = st.session_state.pssr_page

start_idx = (
                    page - 1
            ) * PAGE_SIZE

end_idx = (
        start_idx
        + PAGE_SIZE
)

page_df = filtered_df.iloc[
    start_idx:end_idx
].copy()


# =========================================================
# HTML ESCAPE HELPER
# =========================================================

def escape_html(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# =========================================================

# TABLE
# =========================================================
# PSSR REGISTER
# Original PSSR columns are preserved.
# Only Upload / View are native Streamlit buttons,
# styled exactly like the working PT table.
# =========================================================

st.html(
    '''
<style>

.pssr-table-wrap {
    width: 100%;
    overflow: hidden;
    border: 1px solid #d5e0ea;
    background: #ffffff;
}

.pssr-action-row {
    display: grid;
    grid-template-columns:
        1.90fr
        1.90fr
        1.40fr
        1.00fr
        1.00fr
        1.80fr;
}

.pssr-action-header {
    min-height: 52px;
    background: linear-gradient(
        180deg,
        #205796 0%,
        #174b87 100%
    );
}

.pssr-action-header .pssr-action-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 7px 10px;
    border-right: 1px solid #d5e0ea;
    border-bottom: 1px solid #d5e0ea;
    color: #ffffff;
    font-size: 12px;
    font-weight: 900;
    text-align: center;
    line-height: 1.2;
}

.pssr-action-cell {
    min-height: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    border-right: 1px solid #d5e0ea;
    border-bottom: 1px solid #d5e0ea;
    color: #243b57;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.2;
    padding: 5px 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.pssr-action-cell.alt {
    background: #f5f8fb;
}

.pssr-action-cell.left {
    justify-content: flex-start;
    text-align: left;
}
.pssr-view-link {
    display:flex;
    align-items:center;
    justify-content:center;
    width:100%;
    height:35px;
    box-sizing:border-box;
    background:#ffffff;
    color:#174b87 !important;
    border-bottom:1px solid #d5e0ea;
    border-right:1px solid #d5e0ea;
    text-decoration:none !important;
    font-size:11px;
    font-weight:800;
}
.pssr-view-link:hover {
    background:#f5f8fb;
}


/* Keep the Google Sheet-style headline visible and tight. */
div[data-testid="stMarkdownContainer"]:has(.pssr-action-header) {
    margin: 0 !important;
    padding: 0 !important;
}

.pssr-action-header .pssr-action-cell {
    color: #ffffff !important;
    background: #205796 !important;
}

.pssr-status-completed {
    color: #0a9f43;
    font-weight: 900;
}

.pssr-status-ongoing,
.pssr-status-pending {
    color: #f28c00;
    font-weight: 900;
}

.pssr-status-overdue {
    color: #e1262d;
    font-weight: 900;
}

/* SAME VISUAL TARGET AS PT.PY */

div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker) {
    gap: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button,
div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(6) button {
    height: 35px !important;
    min-height: 35px !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 8px !important;
    border-radius: 0 !important;
    border: 0 !important;
    border-right: 1px solid #d5e0ea !important;
    border-bottom: 1px solid #d5e0ea !important;
    box-shadow: none !important;
    background: #ffffff !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    transform: none !important;
}

div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button {
    color: #e1262d !important;
}

div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(6) button {
    color: #174b87 !important;
}

div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button:hover,
div[data-testid="stHorizontalBlock"]:has(.pssr-action-row-marker)
div[data-testid="stColumn"]:nth-child(6) button:hover {
    background: #f5f8fb !important;
    color: inherit !important;
    border-color: #d5e0ea !important;
    box-shadow: none !important;
    transform: none !important;
}

</style>
'''
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '''
<div class="pssr-table-wrap">
    <div class="pssr-action-row pssr-action-header">
        <div class="pssr-action-cell">PSSR No.</div>
        <div class="pssr-action-cell">PSSR Description</div>
        <div class="pssr-action-cell">Department</div>
        <div class="pssr-action-cell">Status</div>
        <div class="pssr-action-cell">View Report</div>
        <div class="pssr-action-cell">Remark</div>
    </div>
    ''',
    unsafe_allow_html=True
)


def escape_html(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


for row_no, (_, row) in enumerate(page_df.iterrows()):

    alt = row_no % 2

    pssr_no = str(row["_pssr_no"]).strip()
    description = str(row["_description"]).strip()
    department = str(row["_department"]).strip()
    status = str(row["_status"]).strip()
    remarks = str(row["_remarks"]).strip()

    if status.lower() == "completed":
        status_html = (
            '<span class="pssr-status-completed">COMPLETED</span>'
        )
    elif status.lower() == "ongoing":
        status_html = (
            '<span class="pssr-status-ongoing">ONGOING</span>'
        )
    elif status.lower() == "overdue":
        status_html = (
            '<span class="pssr-status-overdue">OVERDUE</span>'
        )
    else:
        status_html = escape_html(status or "—")

    row_cols = st.columns(
        [
            1.90,
            1.90,
            1.40,
            1.00,
            1.00,
            1.80
        ],
        gap=None
    )

    with row_cols[0]:
        st.markdown(
            f'''
<div class="pssr-action-cell {"alt" if alt else ""} left">
    <span class="pssr-action-row-marker"></span>
    {escape_html(pssr_no)}
</div>
''',
            unsafe_allow_html=True
        )

    with row_cols[1]:
        st.markdown(
            f'''
<div class="pssr-action-cell {"alt" if alt else ""} left"
     title="{escape_html(description)}">
    {escape_html(description)}
</div>
''',
            unsafe_allow_html=True
        )

    with row_cols[2]:
        st.markdown(
            f'''
<div class="pssr-action-cell {"alt" if alt else ""}">
    {escape_html(department)}
</div>
''',
            unsafe_allow_html=True
        )

    with row_cols[3]:
        st.markdown(
            f'''
<div class="pssr-action-cell {"alt" if alt else ""}">
    {status_html}
</div>
''',
            unsafe_allow_html=True
        )

    with row_cols[4]:
        report_link = get_report_link(row, page_df.index[row_no])
        st.markdown(
            f"""
<a href="{escape_html(report_link)}"
   target="_blank"
   class="pssr-view-link">◉ View</a>
""",
            unsafe_allow_html=True
        )

    with row_cols[5]:
        st.markdown(
            f'''
<div class="pssr-action-cell {"alt" if alt else ""}"
     title="{escape_html(remarks)}">
    <span class="remark-icon">▱</span>
</div>
''',
            unsafe_allow_html=True
        )

st.html("</div>")

# =========================================================
# REGISTER FOOTER
# =========================================================
shown_from = (
    start_idx + 1
    if len(filtered_df) > 0
    else 0
)

shown_to = min(
    end_idx,
    len(filtered_df)
)

st.html(
    f"""
    <div class="register-footer">

        <div>

            Showing
            {shown_from}
            to
            {shown_to}
            of
            {len(filtered_df)}
            entries

        </div>


        <div class="pagination">

            <span class="page-btn">
                «
            </span>

            <span class="page-btn">
                ‹
            </span>

            <span class="page-btn page-current">
                {page}
            </span>

            <span class="page-btn">
                {min(
        page + 1,
        total_pages
    )}
            </span>

            <span class="page-btn">
                …
            </span>

            <span class="page-btn">
                {total_pages}
            </span>

            <span class="page-btn">
                ›
            </span>

            <span class="page-btn">
                »
            </span>

        </div>

    </div>
    """
)

# =========================================================
# REAL PAGINATION BUTTONS
# =========================================================
if total_pages > 1:

    p1, p2, p3 = st.columns(
        [1, 1, 1]
    )

    with p1:

        if page > 1:

            if st.button(
                    "← Previous",
                    key="pssr_previous"
            ):
                st.session_state.pssr_page -= 1

                st.rerun()

    with p3:

        if page < total_pages:

            if st.button(
                    "Next →",
                    key="pssr_next"
            ):
                st.session_state.pssr_page += 1

                st.rerun()

st.html(
    "</div>"
)

# =========================================================
# FOOTER
# =========================================================
st.html(
    """
    <div class="footer">

        🛡 &nbsp;

        © 2026 Process Safety Management Dashboard

        &nbsp; | &nbsp;

        Pillar: PSSR

    </div>
    """
)

# =========================================================
# AUTO REFRESH MESSAGE
# =========================================================
if not AUTO_REFRESH_AVAILABLE:
    st.caption(
        "Automatic refresh is disabled. "
        "Install streamlit-autorefresh with: "
        "pip install streamlit-autorefresh"
    )

