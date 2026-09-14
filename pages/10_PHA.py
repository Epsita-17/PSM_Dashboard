import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import re
import mimetypes
from datetime import datetime
from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
from openpyxl import load_workbook
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PSM Dashboard - PHA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "status_filter" not in st.session_state:
    st.session_state.status_filter = "All"

if "page_number" not in st.session_state:
    st.session_state.page_number = 1

if "recommendation_page_number" not in st.session_state:
    st.session_state.recommendation_page_number = 1

if "department_selector" not in st.session_state:
    st.session_state.department_selector = "All Departments"

if "upload_pha_no" not in st.session_state:
    st.session_state.upload_pha_no = ""

if "open_upload_dialog" not in st.session_state:
    st.session_state.open_upload_dialog = False

if "view_pha_no" not in st.session_state:
    st.session_state.view_pha_no = ""

if "open_view_dialog" not in st.session_state:
    st.session_state.open_view_dialog = False

# =========================================================
# AUTO REFRESH
# IMPORTANT:
# Do not refresh while upload dialog is open.
# This prevents the upload popup from unexpectedly closing.
# =========================================================

if not st.session_state.open_upload_dialog:
    st_autorefresh(
        interval=100000,
        key="psm_auto_refresh"
    )

# =========================================================
# GOOGLE SHEET - SHEET2
# =========================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEET2_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet=PHA"
)
PHA_RECOMMENDATION_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet=PHA%20RECOMENDATION"
)


@st.cache_data(ttl=60)
def get_pha_data():
    try:
        data = pd.read_csv(SHEET2_CSV_URL)

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
                    .str.replace("\xa0", " ", regex=False)
                    .str.strip()
                )

        data = data.replace(
            {
                "nan": "",
                "NaN": "",
                "NAN": ""
            }
        )

        return data

    except Exception as exc:

        st.error(
            f"Unable to load Google Sheet Sheet2: {exc}"
        )

        return pd.DataFrame()


df = get_pha_data()


# =========================================================
# GOOGLE SHEET UPLOAD DOCUMENT LINKS
# =========================================================
# The PHA "View Document" dashboard column uses the link
# from the SAME Google Sheet row's "Upload Document" cell.
#
# This supports:
#   1. A normal URL stored directly in the cell.
#   2. A Google Sheets rich-text hyperlink.
#   3. A HYPERLINK(...) formula.
# =========================================================

PHA_UPLOAD_COLUMN = "Upload Document"
PHA_NO_COLUMN = "PHA No"


@st.cache_data(ttl=60)
def get_pha_upload_document_links():
    links = {}

    try:
        xlsx_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{SPREADSHEET_ID}/export?format=xlsx"
        )

        request = Request(
            xlsx_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(request, timeout=30) as response:
            workbook_bytes = response.read()

        workbook = load_workbook(
            filename=BytesIO(workbook_bytes),
            read_only=False,
            data_only=False
        )

        if "PHA" not in workbook.sheetnames:
            workbook.close()
            return links

        worksheet = workbook["PHA"]

        headers = {}

        for cell in worksheet[1]:
            if cell.value is not None:
                header = (
                    str(cell.value)
                    .replace("\xa0", " ")
                    .replace("\n", " ")
                    .strip()
                )
                headers[header] = cell.column

        pha_col = headers.get(PHA_NO_COLUMN)
        upload_col = headers.get(PHA_UPLOAD_COLUMN)

        if not pha_col or not upload_col:
            workbook.close()
            return links

        formula_pattern = re.compile(
            r'=HYPERLINK\s*\(\s*["\']([^"\']+)["\']',
            re.IGNORECASE
        )

        for row_number in range(
            2,
            worksheet.max_row + 1
        ):

            pha_cell = worksheet.cell(
                row=row_number,
                column=pha_col
            )

            upload_cell = worksheet.cell(
                row=row_number,
                column=upload_col
            )

            pha_number = (
                ""
                if pha_cell.value is None
                else str(pha_cell.value).strip()
            )

            if not pha_number:
                continue

            document_link = ""

            # Rich-text / normal Excel hyperlink target.
            if (
                upload_cell.hyperlink
                and upload_cell.hyperlink.target
            ):
                document_link = (
                    str(upload_cell.hyperlink.target)
                    .strip()
                )

            # HYPERLINK("url","text") formula.
            if (
                not document_link
                and isinstance(upload_cell.value, str)
            ):
                match = formula_pattern.search(
                    upload_cell.value
                )

                if match:
                    document_link = (
                        match.group(1)
                        .strip()
                    )

            # Plain URL.
            if (
                not document_link
                and isinstance(upload_cell.value, str)
            ):
                candidate = upload_cell.value.strip()

                if re.match(
                    r"^https?://",
                    candidate,
                    re.IGNORECASE
                ):
                    document_link = candidate

            if document_link:
                links[pha_number] = document_link

        workbook.close()

    except Exception:
        # CSV fallback below will still work when the cell
        # itself contains the actual URL.
        return links

    return links


pha_upload_document_links = (
    get_pha_upload_document_links()
)


@st.cache_data(ttl=60)
def get_pha_recommendation_data():
    try:

        data = pd.read_csv(
            PHA_RECOMMENDATION_CSV_URL
        )

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

        data = data.replace(
            {
                "nan": "",
                "NaN": "",
                "NAN": ""
            }
        )

        return data

    except Exception as exc:

        st.error(
            f"Unable to load PHA RECOMENDATION sheet: {exc}"
        )

        return pd.DataFrame()


pha_recommendation_df = get_pha_recommendation_data()

# =========================================================
# DOCUMENT STORAGE
# PT.PY IMPLEMENTATION ADAPTED ONLY FOR PHA
# =========================================================

DOCUMENT_FOLDER = Path(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "pha_documents"
    )
)

DOCUMENT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def safe_pha_folder_name(pha_no):
    value = str(pha_no).strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value or "unknown_pha"


def get_pha_document_folder(pha_no):
    folder = DOCUMENT_FOLDER / safe_pha_folder_name(pha_no)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_pha_documents(pha_no):
    folder = get_pha_document_folder(pha_no)
    return sorted(
        [p for p in folder.iterdir() if p.is_file()],
        key=lambda p: p.name.lower()
    )


def save_pha_document(pha_no, uploaded_file):
    folder = get_pha_document_folder(pha_no)

    # Delete the previous document for this PHA.
    for old_file in folder.iterdir():
        if old_file.is_file():
            try:
                old_file.unlink()
            except OSError:
                pass

    # Save only the newly uploaded document.
    original_name = Path(uploaded_file.name).name
    stem = Path(original_name).stem
    suffix = Path(original_name).suffix

    safe_stem = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        stem
    ).strip("._-")

    safe_stem = safe_stem or "document"

    target = folder / f"{safe_stem}{suffix}"

    target.write_bytes(
        uploaded_file.getbuffer()
    )

    return target


def get_document_mime_type(path):
    mime_type, _ = mimetypes.guess_type(str(path))
    return mime_type or "application/octet-stream"


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [

    "Sr No",
    "PHA No",
    "Department",
    "Name of PHA",
    "Status  (Ongoing/Completed)",
    "Upload Document"
]

STATUS_COLUMN = "Status  (Ongoing/Completed)"

# =========================================================
# CHECK DATA
# =========================================================

if df.empty:
    st.error(
        "No data found in Google Sheet PHA."
    )

    st.stop()

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Some required columns are missing from PHA."
    )

    st.write("Missing columns:")
    st.write(missing_columns)

    st.write("Columns found in PHA:")
    st.write(df.columns.tolist())

    st.stop()

# =========================================================
# GLOBAL CSS
# STEEL BLUE INDUSTRIAL THEME
# FONT SIZES AND LETTER SPACING RETAINED
# =========================================================

st.markdown(
    """
<style>
/* =====================================================
   REFERENCE-STYLE WHITE / NAVY INDUSTRIAL THEME
   VISUAL ONLY — NO DATA / LOGIC CHANGES
   ===================================================== */

* {
    box-sizing: border-box;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}

#MainMenu,
header,
footer,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 6px !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding: 0 !important;
}

iframe {
    display: block !important;
    border: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}


/* =====================================================
   MAIN BACKGROUND
   ===================================================== */

.stApp {
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f7faff 55%,
            #eef4fa 100%
        ) !important;

    color: #092d5c !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;
}

.stApp * {
    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


/* =====================================================
   SPACING
   ===================================================== */

[data-testid="stVerticalBlock"] {
    gap: 0.00rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}


/* =====================================================
   FILTER LABELS
   ===================================================== */

[data-testid="stSelectbox"] label {
    color: #092d5c !important;
    font-size: 12px !important;
    font-weight: 900 !important;
    letter-spacing: .35px !important;
    margin-bottom: 3px !important;
    padding-left: 4px !important;
}


/* =====================================================
   SELECT BOX
   ===================================================== */

div[data-baseweb="select"] > div {
    height: 38px !important;
    min-height: 38px !important;
    border-radius: 6px !important;

    background:
        #ffffff !important;

    border:
        1.5px solid #a9bfd8 !important;

    box-shadow:
        0 2px 5px rgba(8,45,92,.10),
        inset 0 1px 0 rgba(255,255,255,.95) !important;
}

div[data-baseweb="select"]:hover > div {
    border-color: #176fc1 !important;
    box-shadow:
        0 3px 8px rgba(8,76,135,.16) !important;
}

div[data-baseweb="select"] * {
    color: #092d5c !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}

div[data-baseweb="select"] svg {
    fill: #0a4e91 !important;
}


/* =====================================================
   MONTH + DEPARTMENT — ALIGN WITH RESET FILTERS
   ===================================================== */

/*
   IMPORTANT:
   Move only the two selectbox widgets.
   The 22px spacers and the Reset Filters 46px spacer
   remain unchanged, so the Reset Filters position is
   not affected.
*/

/* Month */
div[data-testid="stColumn"]:has(.month-filter-anchor)
div[data-testid="stSelectbox"],
div[data-testid="column"]:has(.month-filter-anchor)
div[data-testid="stSelectbox"] {
    transform: translateY(-5px) !important;
}

/* Department */
div[data-testid="stColumn"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"],
div[data-testid="column"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"] {
    transform: translateY(-5px) !important;
}


/* =====================================================
   TEXT INPUT
   ===================================================== */

div[data-testid="stTextInput"] input {
    height: 40px !important;
    min-height: 40px !important;
    border-radius: 6px !important;

    background:
        #ffffff !important;

    border:
        1.5px solid #a9bfd8 !important;

    color: #092d5c !important;

    font-size: 12px !important;
    font-weight: 600 !important;

    box-shadow:
        0 2px 5px rgba(8,45,92,.09),
        inset 0 1px 2px rgba(0,0,0,.025) !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #126bc0 !important;

    box-shadow:
        0 0 0 1px #126bc0,
        0 3px 9px rgba(18,107,192,.15) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #657990 !important;
    opacity: 1 !important;
}


/* =====================================================
   3D INDUSTRIAL BUTTONS
   ===================================================== */

div.stButton > button {
    height: 36px !important;
    min-height: 36px !important;

    border-radius: 6px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #e8f0f8 100%
        ) !important;

    border:
        1.5px solid #9db7d2 !important;

    color: #07366d !important;

    font-size: 12px !important;
    font-weight: 900 !important;

    box-shadow:
        0 3px 0 #7897b6,
        0 5px 9px rgba(6,48,91,.13),
        inset 0 1px 0 rgba(255,255,255,.95) !important;

    transition:
        transform .12s ease,
        box-shadow .12s ease,
        background .12s ease !important;
}

div.stButton > button:hover {
    border-color: #126bc0 !important;

    color: #ffffff !important;

    background:
        linear-gradient(
            180deg,
            #1685db 0%,
            #075ca8 100%
        ) !important;

    transform:
        translateY(-1px) !important;

    box-shadow:
        0 4px 0 #06477f,
        0 7px 13px rgba(4,74,135,.24),
        inset 0 1px 0 rgba(255,255,255,.28) !important;
}

div.stButton > button:active {
    transform:
        translateY(2px) !important;

    box-shadow:
        0 1px 0 #06477f,
        0 3px 6px rgba(4,74,135,.18) !important;
}

div.stButton > button:disabled {
    color: #8293a7 !important;
    background: #eef3f7 !important;
    border-color: #c5d2df !important;
    box-shadow: none !important;
}


/* =====================================================
   PT REGISTER TOOLBAR — ONLY THESE 4 BUTTONS
   ALL / COMPLETED / ONGOING / REFRESH DATA
   NORMAL = WHITE SHINING
   HOVER = DEEP OCEAN BLUE
   ===================================================== */

/* The toolbar is the horizontal block containing the
   Search input. Columns 2–5 are the four buttons. */

[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(2) button,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(3) button,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(4) button,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(5) button {

    background: #ffffff !important;
    background-image: none !important;

    color:
        #075985 !important;

    border:
        1.5px solid #b8cfe0 !important;

    box-shadow:
        0 2px 4px rgba(0,0,0,.12),
        inset 0 1px 0 #ffffff !important;

    transition:
        background .15s ease,
        color .15s ease,
        border-color .15s ease,
        transform .15s ease,
        box-shadow .15s ease !important;
}


/* Mouse over ONLY the four toolbar buttons */

[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(2) button:hover,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(3) button:hover,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(4) button:hover,
[data-testid="stHorizontalBlock"]:has(
    [data-testid="stTextInput"]
) > [data-testid="column"]:nth-child(5) button:hover {

    background:
        linear-gradient(
            180deg,
            #0b6f9f 0%,
            #064f73 52%,
            #043d5c 100%
        ) !important;

    color:
        #ffffff !important;

    border-color:
        #064f73 !important;

    transform:
        translateY(-1px) !important;

    box-shadow:
        0 4px 0 #032f46,
        0 8px 15px rgba(4,79,115,.30),
        inset 0 1px 0 rgba(255,255,255,.28) !important;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

.kpi-card {
    position: relative;
    height: 145px;
    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 72%,
            #edf4fa 100%
        );

    border:
        1.5px solid #c2d3e4;

    border-top:
        4px solid #176fc1;

    border-radius: 8px;

    padding: 17px 16px;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98);

    transition:
        transform .15s ease,
        box-shadow .15s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 7px 16px rgba(6,48,91,.17),
        0 2px 4px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,1);
}

.kpi-card.completed {
    border-top-color: #19a657;
}

.kpi-card.ongoing {
    border-top-color: #f18d05;
}


/* =====================================================
   KPI ICONS
   ===================================================== */

.kpi-icon {
    display: none !important;
}




/* =====================================================
   TOTAL PT — REMOVE ICON ONLY
   ===================================================== */

.kpi-card.total .kpi-icon {
    display: none;
}

.kpi-card.total .kpi-content {
    margin-left: 0 !important;
    width: 100% !important;
    height: 100% !important;

    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;
}


/* =====================================================
   KPI TEXT — HIGH CONTRAST
   ===================================================== */

.kpi-content {
    margin-left: 0 !important;
    margin-right: 0 !important;
    width: 100% !important;
    height: 100% !important;

    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;
}

.kpi-card .kpi-label,
.kpi-card .kpi-value {
    width: 100% !important;
    text-align: center !important;
    align-self: center !important;
}

.kpi-card .kpi-description {
    display: none !important;
}

.kpi-label {
    color: #092d5c;
    font-size: 15px;
    font-weight: 900;
    letter-spacing: .15px;

    text-align: center;
}

.kpi-card.completed .kpi-label {
    color: #08783c;
}

.kpi-card.ongoing .kpi-label {
    color: #b96700;
}

.kpi-value {
    font-size: 42px;
    line-height: 1;
    font-weight: 900;
    margin-top: 6px;
    color: #092d5c !important;

    text-align: center;
}

/* KPI NUMBER = SAME COLOR AS KPI TEXT */
.kpi-card.total .kpi-value {
    color: #092d5c !important;
}

.kpi-card.completed .kpi-value {
    color: #08783c !important;
}

.kpi-card.ongoing .kpi-value {
    color: #b96700 !important;
}

.kpi-value.green {
    color: #08783c !important;
}

.kpi-value.orange {
    color: #b96700 !important;
}

.kpi-description {
    color: #0a4e91 !important;
    font-size: 11px;
    font-weight: 700;
    margin-top: 7px;

    text-align: center;
}

.kpi-pattern {
    display: none !important;
}



.kpi-arrow {
    display: none !important;
}


/* =====================================================
   PT REGISTER PANEL
   ===================================================== */

.register-wrap {
    background: #ffffff;

    border:
        1.5px solid #b7cce1;

    border-radius:
        7px 7px 0 0;

    overflow: hidden;

    box-shadow:
        0 4px 10px rgba(7,45,82,.12);
}

.register-title {
    height: 40px;

    display: flex;
    align-items: center;

    padding: 0 17px;

    color: #ffffff;

    font-size: 18px;
    font-weight: 900;
    letter-spacing: .25px;

    background:
        linear-gradient(
            180deg,
            #0a4f91 0%,
            #063b70 100%
        );

    border-bottom:
        2px solid #176fc1;

    text-shadow:
        0 1px 2px rgba(0,0,0,.25);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.16);
}

.register-icon {
    margin-right: 9px;
    color: #ffffff;
}


/* =====================================================
   TABLE HEADER — REFERENCE MATCH
   ===================================================== */

.table-head {
    min-height: 43px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            180deg,
            #0b4f91 0%,
            #063c73 100%
        );

    color: #ffffff;

    border-right:
        1px solid #8caecc;

    border-top:
        1px solid #2879ba;

    border-bottom:
        1px solid #052f5b;

    font-size: 12px;
    line-height: 1.15;
    font-weight: 900;

    text-align: center;
    padding: 5px 3px;

    text-shadow:
        0 1px 2px rgba(0,0,0,.30);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.16);
}


/* =====================================================
   TABLE CELLS — DARK BLUE CLEAR TEXT
   ===================================================== */

.table-cell {
    min-height: 43px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        #ffffff;

    border-right:
        1px solid #c8d6e4;

    border-bottom:
        1px solid #c8d6e4;

    color:
        #092d5c;

    font-size:
        11px;

    line-height:
        1.18;

    font-weight:
        600;

    text-align:
        center;

    padding:
        5px 4px;

    word-break:
        break-word;
}

.table-cell.alt {
    background:
        #f3f7fb;
}

.table-cell.left {
    justify-content:
        flex-start;

    text-align:
        left;

    font-weight:
        650;
}
/* =====================================================
   STATUS — TEXT ONLY
   ===================================================== */

.status-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    min-width: auto;
    padding: 0;

    border-radius: 0;

    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

    font-size: 11px;
    font-weight: 900;
    letter-spacing: .1px;

    white-space: nowrap;
}


/* COMPLETED — GREEN TEXT ONLY */

.status-completed {
    background: transparent !important;
    border: none !important;
    color: #16A34A !important;
    box-shadow: none !important;
}


/* ONGOING — ORANGE TEXT ONLY */

.status-ongoing {
    background: transparent !important;
    border: none !important;
    color: #EA8A00 !important;
    box-shadow: none !important;
}
/* =====================================================
   STREAMLIT TABLE ACTION BUTTONS
   ===================================================== */

.table-cell + div button,
div[data-testid="column"] div.stButton > button {
    font-size: 11px !important;
    font-weight: 900 !important;
}
/* =====================================================
   RECORD BAR / PAGINATION
   ===================================================== */

.record-bar {
    height: 38px;

    display: flex;
    align-items: center;

    padding: 0 12px;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #edf3f8 100%
        );

    color:
        #173f6d;

    font-size:
        11px;

    font-weight:
        800;

    border-top:
        1px solid #c4d4e3;

    border-bottom:
        1px solid #c4d4e3;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.9);
}


/* =====================================================
   DOWNLOAD BUTTON
   ===================================================== */

div.stDownloadButton > button {
    border-radius: 6px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #e9f1f8
        ) !important;

    border:
        1.5px solid #9eb8d2 !important;

    color:
        #083c76 !important;

    font-size:
        11px !important;

    font-weight:
        900 !important;

    box-shadow:
        0 3px 0 #7895b1,
        0 5px 8px rgba(8,53,94,.12) !important;
}

div.stDownloadButton > button:hover {
    color: #ffffff !important;

    background:
        linear-gradient(
            180deg,
            #1685db,
            #075ca8
        ) !important;

    border-color:
        #075ca8 !important;
}


/* =====================================================
   INFO / ALERT
   ===================================================== */

div[data-testid="stAlert"] {
    border-radius: 6px !important;

    color: #123b68 !important;

    box-shadow:
        0 2px 7px rgba(20,70,100,.08) !important;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    height: 34px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #ffffff;

    background:
        linear-gradient(
            180deg,
            #0a4f91 0%,
            #063563 100%
        );

    font-size:
        11px;

    font-weight:
        800;

    border-top:
        2px solid #176fc1;

    box-shadow:
        0 -2px 8px rgba(0,0,0,.12);
}


/* =====================================================
   SCROLLBAR
   ===================================================== */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #e9f0f6;
}

::-webkit-scrollbar-thumb {
    background: #8daac4;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #527fa6;
}
/* =====================================================
   PHA-ONLY SECTIONS
   Same white / navy industrial visual language as reference
   ===================================================== */

.pha-recommendation-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    padding: 8px 0 4px 0;
}

.pha-recommendation-card {
    position: relative;
    min-height: 155px;
    overflow: hidden;
    background: linear-gradient(145deg,#ffffff 0%,#ffffff 72%,#edf4fa 100%);
    border: 1.5px solid #c2d3e4;
    border-top: 4px solid #176fc1;
    border-radius: 7px;
    padding: 12px 13px;
    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.pha-recommendation-card:hover {
    border-top-color: #0a4f91;
    transform: translateY(-1px);
    box-shadow:
        0 6px 14px rgba(6,48,91,.17),
        inset 0 1px 0 rgba(255,255,255,1);
}

.pha-rec-number {
    position:absolute;
    top:9px;
    right:10px;
    min-width:28px;
    height:25px;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:0 6px;
    border-radius:5px;
    background:#eaf2f8;
    border:1px solid #a9bfd8;
    color:#0a4e91;
    font-size:12px;
    font-weight:900;
}

.pha-rec-title {
    color:#092d5c;
    font-size:14px;
    font-weight:900;
    padding-right:38px;
    margin-bottom:8px;
    line-height:1.15;
}

.pha-rec-recommendation {
    min-height:52px;
    padding:7px 8px;
    margin-bottom:8px;
    border-radius:5px;
    background:#f3f7fb;
    border-left:3px solid #176fc1;
    border-top:1px solid #c8d6e4;
    border-right:1px solid #c8d6e4;
    border-bottom:1px solid #c8d6e4;
    color:#092d5c;
    font-size:10.5px;
    font-weight:700;
    line-height:1.3;
}

.pha-rec-label {
    display:block;
    color:#657990;
    font-size:8px;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.3px;
    margin-bottom:2px;
}

.pha-rec-value {
    color:#092d5c;
    font-size:10px;
    font-weight:700;
    line-height:1.2;
    word-break:break-word;
}

.pha-rec-details {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:6px;
}

.pha-rec-detail {
    min-height:36px;
    padding:6px 7px;
    background:#ffffff;
    border:1px solid #c8d6e4;
    border-radius:5px;
}

.pha-rec-status,
.pha-rec-approval {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-height:22px;
    padding:2px 7px;
    border-radius:4px;
    font-size:9px;
    font-weight:900;
    line-height:1.1;
}

.pha-rec-status {
    background:#fff5e5;
    border:1px solid #e5b66b;
    color:#b96700;
}

.pha-rec-approval {
    background:#edf8f1;
    border:1px solid #7bc59a;
    color:#08783c;
}

.pha-recommendation-empty {
    padding:18px;
    text-align:center;
    color:#657990;
    background:#ffffff;
    border:1px solid #b7cce1;
    border-radius:6px;
}

.pha-rec-summary {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:8px;
    padding:8px 0 6px 0;
}

.pha-rec-kpi {
    position:relative;
    height:105px;
    overflow:hidden;
    background:linear-gradient(145deg,#ffffff 0%,#ffffff 72%,#edf4fa 100%);
    border:1.5px solid #c2d3e4;
    border-top:4px solid #176fc1;
    border-radius:7px;
    padding:15px 16px;
    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.pha-rec-kpi.total { border-top-color:#176fc1; }
.pha-rec-kpi.approved,
.pha-rec-kpi.completed { border-top-color:#19a657; }
.pha-rec-kpi.rejected,
.pha-rec-kpi.overdue { border-top-color:#d9534f; }
.pha-rec-kpi.pending { border-top-color:#f18d05; }

.pha-rec-kpi-icon,
.pha-rec-kpi-pattern,
.pha-rec-kpi-arrow {
    display:none !important;
}

.pha-rec-kpi-content {
    margin-left:0 !important;
    width:100%;
    height:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
}

.pha-rec-kpi-label {
    color:#092d5c;
    font-size:14px;
    font-weight:900;
}

.pha-rec-kpi.approved .pha-rec-kpi-label,
.pha-rec-kpi.completed .pha-rec-kpi-label { color:#08783c; }

.pha-rec-kpi.rejected .pha-rec-kpi-label,
.pha-rec-kpi.overdue .pha-rec-kpi-label { color:#c63f3a; }

.pha-rec-kpi.pending .pha-rec-kpi-label { color:#b96700; }

.pha-rec-kpi-value {
    font-size:38px;
    line-height:1;
    font-weight:900;
    margin-top:5px;
    color:#0a4e91;
}

.pha-rec-kpi-description {
    color:#304d6d;
    font-size:10px;
    font-weight:700;
    margin-top:5px;
}

.recommendation-wrap {
    margin-top:5px;
    margin-bottom: 5px;
    background:#ffffff;
    border:1.5px solid #b7cce1;
    border-radius:7px 7px 0 0;
    overflow:hidden;
    box-shadow:0 4px 10px rgba(7,45,82,.12);
}

.recommendation-title {
    height:40px;
    display:flex;
    align-items:center;
    padding:0 17px;
    color:#ffffff;
    font-size:18px;
    font-weight:900;
    letter-spacing:.25px;
    background:linear-gradient(180deg,#0a4f91 0%,#063b70 100%);
    border-bottom:2px solid #176fc1;
}

.recommendation-icon { margin-right:9px; color:#ffffff; }

.recommendation-container {
    width:100%;
    overflow-x:auto;
    border-left:1px solid #b7cce1;
    border-right:1px solid #b7cce1;
    border-bottom:1px solid #b7cce1;
}

.recommendation-table {
    width:100%;
    border-collapse:collapse;
    table-layout:auto;
}

/* RECOMMENDATION COLUMN — DECREASE WIDTH */
.recommendation-table th:nth-child(2),
.recommendation-table td:nth-child(2) {
    width:400px !important;
    max-width:400px !important;
}

.recommendation-table th {
    background:linear-gradient(180deg,#0b4f91 0%,#063c73 100%);
    color:#ffffff;
    border:1px solid #8caecc;
    font-size:12px;
    font-weight:900;
    text-align:center;
    padding:7px 5px;
}

.recommendation-table td {
    background:#ffffff;
    color:#092d5c;
    border:1px solid #c8d6e4;
    font-size:10.5px;
    text-align:left;
    vertical-align:middle;
    padding:7px 6px;
    word-break:break-word;
}

/* RECOMENDATION REGISTER — SR NO CENTERED */
.recommendation-table th:first-child,
.recommendation-table td:first-child {
    text-align:center !important;
    vertical-align:middle !important;
}

.recommendation-table tr:nth-child(even) td { background:#f3f7fb; }
.recommendation-table tr:hover td { background:#e7f0f8; }

.recommendation-empty {
    padding:18px;
    text-align:center;
    color:#657990;
    font-size:11px;
    background:#ffffff;
    border:1px solid #b7cce1;
}

.recommendation-count {
    height:34px;
    display:flex;
    align-items:center;
    padding:0 12px;
    color:#173f6d;
    background:linear-gradient(180deg,#ffffff 0%,#edf3f8 100%);
    font-size:10.5px;
    font-weight:800;
    border-left:1px solid #b7cce1;
    border-right:1px solid #b7cce1;
    border-bottom:1px solid #b7cce1;
}

@media (max-width:1100px) {
    .pha-recommendation-grid,
    .pha-rec-summary {
        grid-template-columns:repeat(2,minmax(0,1fr));
    }
}

@media (max-width:700px) {
    .pha-recommendation-grid,
    .pha-rec-summary {
        grid-template-columns:1fr;
    }
}

/* =====================================================
   PT.PY REFERENCE FONT — FINAL OVERRIDE
   ===================================================== */

.stApp,
.stApp *,
.register-title,
.recommendation-title,
.table-head,
.table-cell,
.recommendation-table,
.recommendation-table th,
.recommendation-table td,
.record-bar,
div.stButton > button,
div[data-testid="stTextInput"] input {
    font-family: Arial, Helvetica, sans-serif !important;
}

.register-title,
.recommendation-title {
    font-size: 18px !important;
    font-weight: 900 !important;
}

.table-head,
.recommendation-table th {
    font-size: 12px !important;
    font-weight: 900 !important;
    line-height: 1.15 !important;
}

.table-cell {
    font-size: 11px !important;
    font-weight: 600 !important;
    line-height: 1.18 !important;
}

.table-cell.left {
    font-weight: 650 !important;
}

.status-pill {
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 11px !important;
    font-weight: 900 !important;
}

.recommendation-table td {
    font-size: 11px !important;
    font-weight: 600 !important;
    line-height: 1.18 !important;
}

div[data-testid="stTextInput"] input {
    font-size: 12px !important;
    font-weight: 600 !important;
}

div.stButton > button {
    font-size: 12px !important;
    font-weight: 900 !important;
}


/* PHA REGISTER — left-align COMPLETED / ONGOING in Status column */
.pha-table .pha-status-cell,
.pha-table .pha-status-cell * {
    text-align: left !important;
}


/* PHA REGISTER — keep Status text at the left side */
.pha-status-cell,
.pha-status-cell > *,
.pha-status-cell span,
.pha-status-cell div {
    text-align: left !important;
    justify-content: flex-start !important;
}


/* PHA REGISTER — Status left-side spacing */
.pha-status-cell {
    padding-left: 14px !important;
    box-sizing: border-box !important;
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

                PROCESS HAZARD ANALYSIS (PHA)

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


#==================================================================
# =========================================================
# RESET FILTER CALLBACK
# =========================================================

def reset_pha_filters():
    # Reset status filter
    st.session_state.status_filter = "All"

    # Always return pagination to page 1
    st.session_state.page_number = 1

    # Reset Department selectbox to All Departments
    st.session_state.department_selector = "All Departments"

    # Clear document popup state
    st.session_state.upload_pha_no = ""
    st.session_state.view_pha_no = ""
    st.session_state.open_upload_dialog = False
    st.session_state.open_view_dialog = False


# =========================================================
# FILTER SECTION
# =========================================================

filter_month, filter_department, filter_reset = st.columns(
    [1.0, 1.0, 0.34],
    gap="small"
)

# ---------------------------------------------------------
# MONTH
# ---------------------------------------------------------

with filter_month:
    # Same vertical spacing as all other controls
    st.markdown(
        "<div class='month-filter-anchor' style='height:22px;'></div>",
        unsafe_allow_html=True
    )

    selected_month = st.selectbox(
        "Month",
        [
            "August 2026",
            "July 2026",
            "June 2026",
            "May 2026",
            "April 2026",
            "March 2026"
        ],
        index=0
    )

# ---------------------------------------------------------
# DEPARTMENT
# ---------------------------------------------------------

with filter_department:
    # Same vertical spacing
    st.markdown(
        "<div class='department-filter-anchor' style='height:22px;'></div>",
        unsafe_allow_html=True
    )

    department_values = (
        df["Department"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    department_values = department_values[
        (department_values != "") &
        (department_values.str.lower() != "nan")
        ]

    department_options = [
                             "All Departments"
                         ] + sorted(
        department_values.unique().tolist(),
        key=lambda x: x.lower()
    )

    selected_department = st.selectbox(
        "Department",
        department_options,
        key="department_selector"
    )

# ---------------------------------------------------------
# RESET FILTER
# ---------------------------------------------------------

with filter_reset:
    # Same vertical spacing
    st.markdown(
        "<div style='height:40px;'></div>",
        unsafe_allow_html=True
    )

    st.button(
        "↻ Reset Filters",
        use_container_width=True,
        key="reset_pha_filters_button",
        on_click=reset_pha_filters
    )
# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if selected_department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["Department"]
        .fillna("")
        .astype(str)
        .str.strip()
        ==
        selected_department
        ]

filtered_df[STATUS_COLUMN] = (
    filtered_df[STATUS_COLUMN]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

# =========================================================
# KPI CALCULATION
# =========================================================

total_pha = len(filtered_df)

completed = int(
    (
            filtered_df[STATUS_COLUMN]
            ==
            "completed"
    ).sum()
)

ongoing = int(
    (
            filtered_df[STATUS_COLUMN]
            ==
            "ongoing"
    ).sum()
)

completion_percentage = (
    completed / total_pha * 100
    if total_pha
    else 0
)

# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3 = st.columns(
    3,
    gap="small"
)

cards = [

    (
        "▣",
        "TOTAL PHA",
        total_pha,
        "Total identified HA",
        "blue",
        ""
    ),

    (
        "✓",
        "COMPLETED",
        completed,
        f"{completion_percentage:.1f}% completed",
        "green",
        "completed"
    ),

    (
        "◌",
        "ONGOING",
        ongoing,
        "Currently under progress",
        "orange",
        "ongoing"
    )
]

for column, card in zip(
        [k1, k2, k3],
        cards
):
    icon, label, value, description, color, extra = card

    with column:
        st.html(
            f"""
<div class="kpi-card {extra}">

    <div class="kpi-icon">
        {icon}
    </div>

    <div class="kpi-content">

        <div class="kpi-label">
            {label}
        </div>

        <div class="kpi-value {color}">
            {value}
        </div>
</div>

    <div class="kpi-pattern"></div>

    <div class="kpi-arrow">›</div>

</div>
"""
        )

# =========================================================
# PHA RECOMENDATION - KPI SUMMARY
# =========================================================

st.html(
    """
<div class="recommendation-wrap">

    <div class="recommendation-title">
        <span class="recommendation-icon">⚠</span>
        PHA RECOMENDATION
    </div>

</div>
"""
)

# ---------------------------------------------------------
# CALCULATE COUNTS DIRECTLY FROM GOOGLE SHEET DATA
# ---------------------------------------------------------

total_recommendations = len(
    pha_recommendation_df
)

# Approved / Rejected
approval_column = (
    "Recommendation   (Approved/Rejected)"
)

if approval_column in pha_recommendation_df.columns:

    approval_values = (
        pha_recommendation_df[approval_column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    approved_recommendations = int(
        approval_values
        .str.contains(
            "approved",
            na=False
        )
        .sum()
    )

    rejected_recommendations = int(
        approval_values
        .str.contains(
            "rejected",
            na=False
        )
        .sum()
    )

else:

    approved_recommendations = 0
    rejected_recommendations = 0

# Overdue / Pending / Completion
status_column = (
    "Overdue/Pending/Completion"
)

if status_column in pha_recommendation_df.columns:

    recommendation_status_values = (
        pha_recommendation_df[status_column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    overdue_recommendations = int(
        recommendation_status_values
        .str.contains(
            "overdue",
            na=False
        )
        .sum()
    )

    completed_recommendations = int(
        recommendation_status_values
        .str.contains(
            "completion|completed",
            regex=True,
            na=False
        )
        .sum()
    )

    pending_recommendations = int(
        recommendation_status_values
        .str.contains(
            "pending",
            na=False
        )
        .sum()
    )

else:

    overdue_recommendations = 0
    completed_recommendations = 0
    pending_recommendations = 0

# ---------------------------------------------------------
# SIX KPI BOXES
# Same KPI component as TOP 3.
# Color follows the TOP ROW COLUMN reference:
# Column 1 = BLUE
# Column 2 = GREEN
# Column 3 = ORANGE
# ---------------------------------------------------------

recommendation_kpis = [

    (
        "▣",
        "TOTAL RECOMMENDATION",
        total_recommendations,
        "",
        "total"
    ),

    (
        "✓",
        "APPROVED",
        approved_recommendations,
        "Approved recommendations",
        "completed"
    ),

    (
        "✕",
        "REJECTED",
        rejected_recommendations,
        "Rejected recommendations",
        "ongoing"
    ),

    (
        "!",
        "OVERDUE",
        overdue_recommendations,
        "",
        "total"
    ),

    (
        "✓",
        "COMPLETED",
        completed_recommendations,
        "Completed recommendations",
        "completed"
    ),

    (
        "◌",
        "PENDING",
        pending_recommendations,
        "Pending recommendations",
        "ongoing"
    )
]

for row_start in range(
        0,
        len(recommendation_kpis),
        3
):
    if row_start == 3:
        st.markdown(
            "<div style='height:22px;'></div>",
            unsafe_allow_html=True
        )

    recommendation_row = st.columns(
        3,
        gap="small"
    )

    for column, card in zip(
            recommendation_row,
            recommendation_kpis[
                row_start:row_start + 3
            ]
    ):
        icon, label, value, description, card_class = card

        with column:
            # SAME HTML COMPONENT AS THE TOP 3.
            # Only the color class changes according to the
            # TOP ROW COLUMN reference.
            st.html(
                f"""
<div class="kpi-card {card_class}">

    <div class="kpi-icon">
        {icon}
    </div>

    <div class="kpi-content">

        <div class="kpi-label">
            {label}
        </div>

        <div class="kpi-value">
            {value}
        </div>
</div>

    <div class="kpi-pattern"></div>

    <div class="kpi-arrow">›</div>

</div>
"""
            )

# =========================================================
# PT REGISTER TITLE
# =========================================================

st.html(
    """
<div class="register-wrap">

    <div class="register-title">
        <span class="register-icon">▣</span>
        PHA REGISTER
    </div>

</div>
"""
)

# =========================================================
# REGISTER TOOLBAR
# =========================================================

search_col, all_col, completed_col, ongoing_col, refresh_col = st.columns(
    [4.2, .8, 1.15, 1.0, 1.15],
    gap="small"
)

with search_col:
    search_text = st.text_input(
        "Search",
        placeholder=(
            "Search PHA No, Name of PHA, "
            "Department, Product..."
        ),
        label_visibility="collapsed"
    )

with all_col:
    all_button = st.button(
        "All",
        use_container_width=True
    )

with completed_col:
    completed_button = st.button(
        "Completed",
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

with ongoing_col:
    ongoing_button = st.button(
        "Ongoing",
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

with refresh_col:
    if st.button(
            "↻ Refresh Data",
            use_container_width=True
    ):
        st.session_state.view_pha_no = ""
        st.session_state.upload_pha_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.cache_data.clear()
        st.rerun()

# =========================================================
# STATUS FILTER
# =========================================================

if all_button:

    st.session_state.status_filter = "All"
    st.session_state.page_number = 1
    st.session_state.view_pha_no = ""
    st.session_state.upload_pha_no = ""
    st.session_state.open_view_dialog = False
    st.session_state.open_upload_dialog = False

elif completed_button:

    st.session_state.status_filter = "Completed"
    st.session_state.page_number = 1
    st.session_state.view_pha_no = ""
    st.session_state.upload_pha_no = ""
    st.session_state.open_view_dialog = False
    st.session_state.open_upload_dialog = False

elif ongoing_button:

    st.session_state.status_filter = "Ongoing"
    st.session_state.page_number = 1
    st.session_state.view_pha_no = ""
    st.session_state.upload_pha_no = ""
    st.session_state.open_view_dialog = False
    st.session_state.open_upload_dialog = False

# =========================================================
# DISPLAY DATA
# =========================================================

display_df = filtered_df.copy()

if st.session_state.status_filter != "All":
    display_df = display_df[
        display_df[STATUS_COLUMN]
        ==
        st.session_state.status_filter.lower()
        ]

# =========================================================
# SEARCH
# =========================================================

if search_text:

    query = search_text.lower().strip()

    search_columns = [
        "PHA No",
        "Department",
        "Name of PHA",
    ]

    mask = pd.Series(
        False,
        index=display_df.index
    )

    for column in search_columns:
        mask = (
                mask
                |
                display_df[column]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    query,
                    na=False
                )
        )

    display_df = display_df[mask]

# =========================================================
# PAGINATION
# =========================================================

PAGE_SIZE = 5

total_records = len(display_df)

total_pages = max(
    1,
    (total_records + PAGE_SIZE - 1)
    //
    PAGE_SIZE
)

if st.session_state.page_number > total_pages:
    st.session_state.page_number = total_pages

page_number = st.session_state.page_number

start_index = (
                      page_number - 1
              ) * PAGE_SIZE

end_index = (
        start_index + PAGE_SIZE
)

page_df = display_df.iloc[
    start_index:end_index
].copy()

# =========================================================
# TABLE
# Google Sheet data shown as one normal HTML table.
# Upload Document remains a hidden SOURCE column only.
# View Document is a normal column directly beside Status.
# =========================================================

pha_table_html = """
<style>
.pha-register-container {
    width: 100%;
    overflow-x: hidden;
    margin: 0;
    padding: 0;
}

.pha-register-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    margin: 0;
    padding: 0;
}

.pha-register-table th {
    background: #0b4f8a;
    color: #ffffff;
    border-right: 1px solid #d5e0ea;
    border-bottom: 1px solid #d5e0ea;
    height: 46px;
    padding: 8px 10px;
    text-align: center;
    vertical-align: middle;
    font-size: 12px;
    font-weight: 900;
    line-height: 1.15;
    box-sizing: border-box;
}

.pha-register-table td {
    height: 35px;
    padding: 5px 10px;
    border-right: 1px solid #d5e0ea;
    border-bottom: 1px solid #d5e0ea;
    color: #243b57;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.2;
    text-align: center;
    vertical-align: middle;
    box-sizing: border-box;
    background: #ffffff;
}

.pha-register-table tbody tr:nth-child(even) td {
    background: #f5f8fb;
}

.pha-register-table td.left {
    text-align: left !important;
    padding-left: 45px !important;
}

.pha-register-table td.left .status-completed,
.pha-register-table td.left .status-ongoing {
    display: inline-block;
    text-align: left !important;
}

.pha-register-table .pha-view-link {
    color: #174b87;
    text-decoration: none !important;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
}

.pha-register-table .pha-view-link:hover {
    color: #0b4f8a;
    text-decoration: none !important;
}

.pha-register-table .pha-no-link {
    color: #9aaabd;
    font-size: 12px;
    font-weight: 700;
}

.pha-register-table .status-completed,
.pha-register-table .status-ongoing {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 12px;
    font-weight: 800;
    white-space: nowrap;
}

.pha-register-table .status-completed {
    color: #16A34A !important;
}

.pha-register-table .status-ongoing {
    color: #EA8A00 !important;
}
</style>

<div class="pha-register-container">
<table class="pha-register-table">
<colgroup>
    <col style="width:8%;">
    <col style="width:15%;">
    <col style="width:19%;">
    <col style="width:27%;">
    <col style="width:16%;">
    <col style="width:15%;">
</colgroup>
<thead>
<tr>
    <th>Sr No</th>
    <th>PHA No</th>
    <th>Department</th>
    <th>Name of PHA</th>
    <th>Status</th>
    <th>View Document</th>
</tr>
</thead>
<tbody>
"""

for row_number, (_, row) in enumerate(page_df.iterrows()):
    sr_no = str(row["Sr No"]).strip()
    pha_no = str(row["PHA No"]).strip()
    department = str(row["Department"]).strip()
    name_pha = str(row["Name of PHA"]).strip()
    status = str(row[STATUS_COLUMN]).strip()

    if sr_no.lower() == "nan":
        sr_no = ""
    if pha_no.lower() == "nan":
        pha_no = ""
    if department.lower() == "nan":
        department = ""
    if name_pha.lower() == "nan":
        name_pha = ""
    if status.lower() == "nan":
        status = ""

    def esc(value):
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    sr_no_html = esc(sr_no)
    pha_no_html = esc(pha_no)
    department_html = esc(department)
    name_html = esc(name_pha)

    if status.lower() == "completed":
        status_html = '<span class="status-completed">● COMPLETED</span>'
    elif status.lower() == "ongoing":
        status_html = '<span class="status-ongoing">● ONGOING</span>'
    else:
        status_html = esc(status)

    # Fetch the link from the SAME Google Sheet row's hidden Upload Document cell.
    document_link = pha_upload_document_links.get(pha_no, "")

    if not document_link:
        raw_upload_value = row.get(PHA_UPLOAD_COLUMN, "")
        if not pd.isna(raw_upload_value):
            candidate_link = str(raw_upload_value).strip()
            if re.match(r"^https?://", candidate_link, re.IGNORECASE):
                document_link = candidate_link

    if document_link:
        safe_link = (
            document_link
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        view_html = (
            f'<a class="pha-view-link" href="{safe_link}" '
            f'target="_blank" rel="noopener noreferrer">◉ View</a>'
        )
    else:
        view_html = '<span class="pha-no-link">No Link</span>'

    pha_table_html += f"""
<tr>
    <td>{sr_no_html}</td>
    <td>{pha_no_html}</td>
    <td class="left">{department_html}</td>
    <td class="left">{name_html}</td>
    <td class="left">{status_html}</td>
    <td>{view_html}</td>
</tr>
"""

pha_table_html += """
</tbody>
</table>
</div>
"""

st.html(pha_table_html)

# =========================================================
# RECORD COUNT + PAGINATION
# =========================================================

count_left, page_left, page_center, page_right = st.columns(
    [2.2, 1.0, 1.8, 1.0],
    gap="small"
)

with count_left:
    first_record = (
        start_index + 1
        if total_records
        else 0
    )

    last_record = min(
        end_index,
        total_records
    )

    st.html(
        f"""
<div class="record-bar">
    Showing {first_record} to {last_record}
    of {total_records} entries
</div>
"""
    )

with page_left:
    if st.button(
            "‹",
            disabled=(
                    page_number <= 1
            ),
            use_container_width=True
    ):
        st.session_state.page_number -= 1
        st.session_state.view_pha_no = ""
        st.session_state.upload_pha_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()

with page_center:
    st.html(
        f"""
<div class="record-bar"
     style="justify-content:center;">
    {page_number} &nbsp; / &nbsp; {total_pages}
</div>
"""
    )

with page_right:
    if st.button(
            "›",
            disabled=(
                    page_number >= total_pages
            ),
            use_container_width=True
    ):
        st.session_state.page_number += 1
        st.session_state.view_pha_no = ""
        st.session_state.upload_pha_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()

# =========================================================
# RECOMENDATION REGISTER
# 5 ROWS PER PAGE
# =========================================================

st.html(
    """
<div class="recommendation-wrap">

    <div class="recommendation-title">
        <span class="recommendation-icon">⚠</span>
        RECOMENDATION REGISTER
    </div>

</div>
"""
)

recommendation_register_columns = [
    "Sr No",
    "Recommendation",
    "PHA No.",
    "Department",
    "Target Date",
    "Completion Date",
    "Status (Open/Close)"
]

missing_register_columns = [
    column
    for column in recommendation_register_columns
    if column not in pha_recommendation_df.columns
]

if pha_recommendation_df.empty:

    st.html(
        """
<div class="recommendation-empty">
    No RECOMENDATION REGISTER data found.
</div>
"""
    )

elif missing_register_columns:

    st.error(
        "RECOMENDATION REGISTER headers not found."
    )

    st.write(
        missing_register_columns
    )

else:

    recommendation_register_df = (
        pha_recommendation_df[
            recommendation_register_columns
        ]
        .copy()
    )

    # =====================================================
    # PAGINATION - 5 ROWS
    # =====================================================

    recommendation_rows_per_page = 5

    if "recommendation_page_number" not in st.session_state:
        st.session_state.recommendation_page_number = 1

    total_recommendation_records = len(
        recommendation_register_df
    )

    recommendation_total_pages = max(
        1,
        (
                total_recommendation_records
                + recommendation_rows_per_page
                - 1
        )
        // recommendation_rows_per_page
    )

    recommendation_page_number = (
        st.session_state.recommendation_page_number
    )

    if recommendation_page_number > recommendation_total_pages:
        recommendation_page_number = (
            recommendation_total_pages
        )

        st.session_state.recommendation_page_number = (
            recommendation_page_number
        )

    recommendation_start_index = (
                                         recommendation_page_number - 1
                                 ) * recommendation_rows_per_page

    recommendation_end_index = (
            recommendation_start_index
            + recommendation_rows_per_page
    )

    recommendation_display_df = (
        recommendation_register_df.iloc[
            recommendation_start_index:
            recommendation_end_index
        ]
        .copy()
    )

    # =====================================================
    # TABLE
    # =====================================================

    recommendation_register_html = """
<div class="recommendation-container">

<table class="recommendation-table">

<thead>
<tr>
"""

    for column in recommendation_register_columns:
        display_column = (
            "Status"
            if column == "Status (Open/Close)"
            else column
        )

        recommendation_register_html += (
            f"<th>{display_column}</th>"
        )

    recommendation_register_html += """
</tr>
</thead>

<tbody>
"""

    for _, row in recommendation_display_df.iterrows():

        recommendation_register_html += "<tr>"

        for column in recommendation_register_columns:

            value = row[column]

            if pd.isna(value):
                value = ""
            else:
                value = str(value).strip()

            value = (
                value
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
            )

            recommendation_register_html += (
                f"<td>{value}</td>"
            )

        recommendation_register_html += "</tr>"

    recommendation_register_html += """
</tbody>

</table>

</div>
"""

    st.html(
        recommendation_register_html
    )

    # =====================================================
    # RECORD COUNT
    # =====================================================

    recommendation_first_record = (
        recommendation_start_index + 1
        if total_recommendation_records
        else 0
    )

    recommendation_last_record = min(
        recommendation_end_index,
        total_recommendation_records
    )

    st.html(
        f"""
<div class="record-bar">
    Showing {recommendation_first_record}
    to {recommendation_last_record}
    of {total_recommendation_records}
    entries
</div>
"""
    )

    # =====================================================
    # PAGINATION BUTTONS
    # =====================================================

    (
        recommendation_previous_col,
        recommendation_page_col,
        recommendation_next_col
    ) = st.columns(
        [1, 1, 1],
        gap="small"
    )

    with recommendation_previous_col:

        if st.button(
                "‹",
                key="recommendation_previous_button",
                disabled=(
                        recommendation_page_number <= 1
                ),
                use_container_width=True
        ):
            st.session_state.recommendation_page_number -= 1

            st.rerun()

    with recommendation_page_col:

        st.html(
            f"""
<div class="record-bar"
     style="justify-content:center;">
    {recommendation_page_number}
    &nbsp; / &nbsp;
    {recommendation_total_pages}
</div>
"""
        )

    with recommendation_next_col:

        if st.button(
                "›",
                key="recommendation_next_button",
                disabled=(
                        recommendation_page_number
                        >= recommendation_total_pages
                ),
                use_container_width=True
        ):
            st.session_state.recommendation_page_number += 1

            st.rerun()

# =========================================================
# UPLOAD DOCUMENT — VERY SMALL MODAL POPUP
# SAME AS PT.PY, ADAPTED ONLY TO PHA
# =========================================================

if st.session_state.open_upload_dialog and st.session_state.upload_pha_no:

    upload_pha = st.session_state.upload_pha_no
    st.session_state.open_upload_dialog = False


    @st.dialog("Upload Document", width="small")
    def upload_document_dialog():

        st.caption(f"PHA No.  {upload_pha}")

        uploaded_file = st.file_uploader(
            "Choose file",
            type=[
                "pdf", "doc", "docx",
                "xls", "xlsx", "csv",
                "ppt", "pptx", "txt",
                "png", "jpg", "jpeg"
            ],
            key=f"uploader_dialog_{safe_pha_folder_name(upload_pha)}"
        )

        c1, c2 = st.columns(2, gap="small")

        with c1:
            if st.button(
                    "Save",
                    key=f"save_dialog_{safe_pha_folder_name(upload_pha)}",
                    use_container_width=True,
                    disabled=uploaded_file is None
            ):
                save_pha_document(upload_pha, uploaded_file)
                st.session_state.upload_pha_no = ""
                st.session_state.open_upload_dialog = False
                st.rerun()

        with c2:
            if st.button(
                    "Cancel",
                    key=f"cancel_dialog_{safe_pha_folder_name(upload_pha)}",
                    use_container_width=True
            ):
                st.session_state.upload_pha_no = ""
                st.session_state.open_upload_dialog = False
                st.rerun()


    upload_document_dialog()

# =========================================================
# VIEW DOCUMENT — SEPARATE MODAL POPUP
# SHOW ONLY THE CURRENT / LATEST DOCUMENT
# =========================================================

if st.session_state.open_view_dialog and st.session_state.view_pha_no:

    view_pha = st.session_state.view_pha_no
    st.session_state.open_view_dialog = False


    @st.dialog("View Document", width="large")
    def view_document_dialog():

        st.caption(f"PHA No.  {view_pha}")

        documents = get_pha_documents(view_pha)

        if not documents:
            st.info(
                "No document has been uploaded for this PHA yet."
            )
            return

        # A new upload replaces the old file, so there
        # should be only one current document.
        selected_document = documents[-1]

        file_bytes = selected_document.read_bytes()
        mime_type = get_document_mime_type(
            selected_document
        )

        st.download_button(
            "↓ Download",
            data=file_bytes,
            file_name=selected_document.name,
            mime=mime_type,
            key=(
                f"download_{safe_pha_folder_name(view_pha)}_"
                f"{safe_pha_folder_name(selected_document.name)}"
            )
        )

        if mime_type == "application/pdf":

            pdf_base64 = (
                base64.b64encode(
                    file_bytes
                ).decode("utf-8")
            )

            components.html(
                f"""
<iframe
    src="data:application/pdf;base64,{pdf_base64}"
    width="100%"
    height="600"
    style="border:1px solid #d5e0ea;">
</iframe>
""",
                height=620,
                scrolling=False
            )

        elif mime_type.startswith("image/"):

            st.image(
                file_bytes,
                use_container_width=True
            )

        elif mime_type.startswith("text/"):

            text_preview = file_bytes.decode(
                "utf-8",
                errors="replace"
            )

            st.text_area(
                "Document preview",
                text_preview,
                height=450,
                disabled=True,
                key=(
                    f"text_preview_"
                    f"{safe_pha_folder_name(view_pha)}_"
                    f"{safe_pha_folder_name(selected_document.name)}"
                )
            )

        else:

            st.info(
                "Preview is not available for this file type. "
                "Use Download to open the file."
            )


    view_document_dialog()

# =========================================================
# FOOTER
# =========================================================

st.html(
    """
<div class="footer">
    🛡 &nbsp; © 2026 Process Safety Management Dashboard
    | Pillar: PHA
</div>
"""
)

