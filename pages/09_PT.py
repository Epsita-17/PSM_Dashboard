import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import re
import mimetypes
from pathlib import Path
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PSM Dashboard - PT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "status_filter" not in st.session_state:
    st.session_state.status_filter = "All"

if "page_number" not in st.session_state:
    st.session_state.page_number = 1

if "department_selector" not in st.session_state:
    st.session_state.department_selector = "All Departments"

if "upload_pt_no" not in st.session_state:
    st.session_state.upload_pt_no = ""

if "view_pt_no" not in st.session_state:
    st.session_state.view_pt_no = ""

if "open_upload_dialog" not in st.session_state:
    st.session_state.open_upload_dialog = False

if "open_view_dialog" not in st.session_state:
    st.session_state.open_view_dialog = False


# =========================================================
# ACTION STATE
# Upload / View are opened in Streamlit modal dialogs.
# No query-parameter navigation is used, so the browser
# does not leave or reload the dashboard page.
# =========================================================

if "upload_pt_no" not in st.session_state:
    st.session_state.upload_pt_no = ""

if "view_pt_no" not in st.session_state:
    st.session_state.view_pt_no = ""


# =========================================================
# AUTO REFRESH
# =========================================================

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
    f"/gviz/tq?tqx=out:csv&sheet=PT"
)


@st.cache_data(ttl=60)
def get_pt_data():

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
            f"Unable to load Google Sheet PT: {exc}"
        )

        return pd.DataFrame()


df = get_pt_data()


# =========================================================
# DOCUMENT STORAGE
# =========================================================

DOCUMENT_FOLDER = Path(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "pt_documents"
    )
)

DOCUMENT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def safe_pt_folder_name(pt_no):
    value = str(pt_no).strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value or "unknown_pt"


def get_pt_document_folder(pt_no):
    folder = DOCUMENT_FOLDER / safe_pt_folder_name(pt_no)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_pt_documents(pt_no):
    folder = get_pt_document_folder(pt_no)
    return sorted(
        [p for p in folder.iterdir() if p.is_file()],
        key=lambda p: p.name.lower()
    )


def save_pt_document(pt_no, uploaded_file):
    folder = get_pt_document_folder(pt_no)

    original_name = Path(uploaded_file.name).name
    stem = Path(original_name).stem
    suffix = Path(original_name).suffix

    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("._-")
    safe_stem = safe_stem or "document"

    target = folder / f"{safe_stem}{suffix}"
    counter = 1

    while target.exists():
        target = folder / f"{safe_stem}_{counter}{suffix}"
        counter += 1

    target.write_bytes(uploaded_file.getbuffer())
    return target


def get_document_mime_type(path):
    mime_type, _ = mimetypes.guess_type(str(path))
    return mime_type or "application/octet-stream"


# =========================================================
# ONLY COLUMNS REQUIRED FROM GOOGLE SHEET: PT
# =========================================================

required_columns = [
    "PT No.",
    "Department",
    "Name of PT",
    "Status  (Ongoing/Completed)"
]

STATUS_COLUMN = "Status  (Ongoing/Completed)"


# =========================================================
# CHECK DATA
# =========================================================

if df.empty:

    st.error(
        "No data found in Google Sheet: PT."
    )

    st.stop()


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "Some required columns are missing from Google Sheet: PT."
    )

    st.write("Missing columns:")
    st.write(missing_columns)

    st.write("Columns found in PT:")
    st.write(df.columns.tolist())

    st.stop()


# =========================================================
# GLOBAL CSS
# LIGHT 3D INDUSTRIAL THEME
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
    transform: translateY(-3px) !important;
}

/* Department */
div[data-testid="stColumn"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"],
div[data-testid="column"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"] {
    transform: translateY(-3px) !important;
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
    height: 105px;
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
    margin-left: 78px;
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
    color: #0a4e91;

    text-align: center;
}

.kpi-value.green {
    color: #159447 !important;
}

.kpi-value.orange {
    color: #f0a000 !important;
}

.kpi-description {
    color: #304d6d;
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

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# PREMIUM 3D INDUSTRIAL HEADER — REFERENCE MATCH
# =========================================================

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "jsw_jfe_logo.jpg"
)

if not os.path.exists(LOGO_PATH):
    st.error(f"Logo file not found: {LOGO_PATH}")
    st.stop()

with open(LOGO_PATH, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode("utf-8")


header_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    background: #ffffff;
}


/* =====================================================
   MAIN OUTER HEADER
   — FULL CORNER CURVE LIKE REFERENCE
   ===================================================== */

.header {
    position: relative;

    width: calc(100% - 8px);
    height: 150px;

    /* Move the complete header slightly downward */
    margin: 8px 4px 0;

    overflow: hidden;

    background:
        radial-gradient(
            ellipse at center,
            #0a3552 0%,
            #062239 35%,
            #031421 67%,
            #010910 100%
        );

    border: 1px solid #51c7f5;

    border-radius: 20px;

    box-shadow:
        0 0 0 2px rgba(4,34,52,.92),
        0 4px 14px rgba(0,0,0,.40),
        inset 0 1px 0 rgba(255,255,255,.12),
        inset 0 -1px 0 rgba(48,194,241,.75);
}


/* =====================================================
   SECONDARY INNER CURVED FRAME
   ===================================================== */

.header-frame {
    position: absolute;

    inset: 5px;

    z-index: 40;

    border: 1px solid rgba(69,190,237,.48);

    border-radius: 15px;

    pointer-events: none;

    box-shadow:
        inset 0 0 18px rgba(0,151,220,.13);
}


/* =====================================================
   TOP REFLECTIVE GLOW
   ===================================================== */

.header-glow {
    position: absolute;

    z-index: 6;

    left: 17%;
    right: 17%;
    top: 2px;

    height: 28px;

    background:
        radial-gradient(
            ellipse,
            rgba(170,235,255,.20) 0%,
            rgba(65,194,242,.10) 35%,
            transparent 72%
        );

    filter: blur(3px);

    pointer-events: none;
}


/* =====================================================
   TECHNICAL GRID
   ===================================================== */

.header::before {
    content: "";

    position: absolute;

    inset: 0;

    background:
        linear-gradient(
            rgba(38,184,242,.045) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(38,184,242,.045) 1px,
            transparent 1px
        );

    background-size: 28px 28px;

    opacity: .9;
}


/* =====================================================
   INDUSTRIAL BACKGROUND
   ===================================================== */

.industrial {
    position: absolute;

    left: 0;
    right: 0;
    bottom: 0;

    width: 100%;
    height: 145px;

    z-index: 2;

    opacity: .55;
}

.industrial .steel {
    fill: #12364e;
    stroke: #2999c4;
    stroke-width: 1.1;
}

.industrial .highlight {
    fill: none;
    stroke: #39c5f5;
    stroke-width: 1;
    opacity: .58;
}

.industrial .warm {
    fill: #f2ad23;
    opacity: .78;
}

.industrial .glass {
    fill: #0a5e92;
    stroke: #53d4ff;
    stroke-width: .7;
    opacity: .45;
}

.tech {
    fill: none;
    stroke: #2ca6d8;
    stroke-width: .8;
    opacity: .18;
}


/* =====================================================
   LOGO PANEL
   — WIDE RECTANGULAR, NOT SQUARE
   ===================================================== */

.logo-panel {
    position: absolute;

    z-index: 30;

    left: 2.6%;
    top: 50%;

    transform: translateY(-50%);

    width: 17.0%;
    max-width: 325px;
    min-width: 235px;

    height: 108px;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 6px 10px;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f9fbfd 42%,
            #e4edf3 100%
        );

    border: 1px solid #a5bccb;

    border-radius: 14px;

    box-shadow:
        0 7px 15px rgba(0,0,0,.40),
        0 0 0 2px rgba(20,63,86,.82),
        inset 0 2px 0 rgba(255,255,255,.98),
        inset 0 -4px 7px rgba(75,105,124,.14);
}

.logo-panel::before {
    content: "";

    position: absolute;

    inset: -4px;

    border-radius: 17px;

    border: 1px solid rgba(84,202,247,.68);

    pointer-events: none;
}

.logo-panel::after {
    content: "";

    position: absolute;

    left: 12%;
    right: 12%;
    top: -3px;

    height: 3px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8fe6ff,
            transparent
        );

    box-shadow:
        0 0 8px rgba(72,204,250,.82);
}

.header-logo {
    display: block;

    width: 100%;
    height: 100%;

    object-fit: contain;
    object-position: center;

    border-radius: 6px;
}


/* =====================================================
   CENTRAL TITLE FRAME
   — LARGE 3D BEVELED PANEL
   ===================================================== */

.title-frame {
    position: absolute;

    z-index: 22;

    left: 50%;
    top: 50%;

    /* Exact horizontal + vertical centering */
    transform: translate(-50%, -50%);

    width: 53%;
    max-width: 995px;
    min-width: 600px;

    height: 112px;

    padding: 3px;

    background:
        linear-gradient(
            135deg,
            #f0fbff 0%,
            #7d9cac 8%,
            #dcecf4 16%,
            #254c63 29%,
            #092337 48%,
            #597f91 70%,
            #eaf8ff 86%,
            #617e8d 100%
        );

    border-radius: 17px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.58),
        0 0 22px rgba(0,160,245,.34);
}


/* INNER TITLE SURFACE */

.title-inner {
    position: relative;

    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: column;

    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            ellipse at 50% 25%,
            #174c6c 0%,
            #0b304b 38%,
            #041b2c 100%
        );

    border: 1px solid #67d4ff;

    border-radius: 13px;

    overflow: hidden;

    box-shadow:
        inset 0 3px 0 rgba(255,255,255,.22),
        inset 0 -10px 18px rgba(0,0,0,.30),
        0 0 15px rgba(28,183,242,.25);
}


/* TOP BLUE REFLECTION */

.title-inner::before {
    content: "";

    position: absolute;

    z-index: 1;

    left: 12%;
    right: 12%;
    top: 5px;

    height: 4px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(192,242,255,.95),
            rgba(73,202,248,1),
            rgba(192,242,255,.95),
            transparent
        );

    box-shadow:
        0 0 10px rgba(72,210,255,.90);
}


/* CENTRAL HIGHLIGHT */

.title-inner::after {
    content: "";

    position: absolute;

    z-index: 1;

    left: 38%;
    right: 38%;
    top: 0;

    height: 8px;

    background:
        radial-gradient(
            ellipse,
            rgba(128,228,255,.9),
            transparent 70%
        );

    filter: blur(2px);
}


/* =====================================================
   3D TITLE TEXT
   ===================================================== */

.title-text {
    position: relative;

    z-index: 5;

    display: flex;
    flex-direction: row;

    align-items: center;
    justify-content: center;

    width: 100%;
    height: 100%;

    line-height: .88;
    white-space: nowrap;
    text-align: center;

    font-weight: 950;
    letter-spacing: 1px;
}


/* PROCESS */

.title-process {
    font-size: clamp(25px, 2.55vw, 43px);

    color: #ffffff;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #ffffff 40%,
            #f2fbff 65%,
            #d4f1ff 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* TECHNOLOGY */

.title-technology {
    margin-top: 4px;

    font-size: clamp(27px, 2.85vw, 48px);

    color: #35c6ff;

    color: #ffffff;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #ffffff 40%,
            #f2fbff 65%,
            #d4f1ff 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* PT GOLD */

.title-pt {
    color: #ffc31b;

    background:
        linear-gradient(
            180deg,
            #fff39a 0%,
            #ffc51c 38%,
            #f09b00 70%,
            #c66b00 100%
        );

    -webkit-background-clip: text;
    background-clip: text;

    -webkit-text-fill-color: transparent;
}


/* =====================================================
   TITLE BOTTOM ACCENT
   ===================================================== */

.title-line {
    position: absolute;

    z-index: 6;

    left: 21%;
    right: 21%;
    bottom: 9px;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #22baf3 18%,
            #d3f7ff 50%,
            #22baf3 82%,
            transparent
        );

    box-shadow:
        0 0 8px rgba(44,195,250,.85);
}


/* =====================================================
   TITLE SIDE WINGS
   ===================================================== */

.title-wing {
    position: absolute;

    z-index: 19;

    top: 50%;

    width: 43px;
    height: 44px;

    transform: translateY(-50%);

    background:
        linear-gradient(
            135deg,
            #1a4862,
            #061d30
        );

    border-top: 1px solid #65d5ff;
    border-bottom: 1px solid #176b91;

    box-shadow:
        0 5px 10px rgba(0,0,0,.44);
}

.title-wing.left {
    left: 23.0%;

    clip-path:
        polygon(
            25% 0,
            100% 0,
            100% 100%,
            25% 100%,
            0 50%
        );
}

.title-wing.right {
    right: 23.0%;

    clip-path:
        polygon(
            0 0,
            75% 0,
            100% 50%,
            75% 100%,
            0 100%
        );
}


/* =====================================================
   TAGLINE
   ===================================================== */

.tagline {
    position: absolute;

    z-index: 27;

    left: 50%;
    bottom: 6px;

    transform: translateX(-50%);

    color: #a9ddec;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 2px;

    white-space: nowrap;
}


/* =====================================================
   RIGHT DATE/TIME PANEL
   — SAME WIDE RECTANGULAR PROPORTION AS LOGO
   ===================================================== */

.status-panel {
    position: absolute;

    z-index: 30;

    right: 2.6%;
    top: 50%;

    transform: translateY(-50%);

    width: 17.0%;
    max-width: 325px;
    min-width: 235px;

    height: 108px;

    padding: 8px 13px;

    background:
        linear-gradient(
            145deg,
            #123c55 0%,
            #08263b 45%,
            #031522 100%
        );

    border: 1px solid #55c7ee;

    border-radius: 14px;

    box-shadow:
        0 7px 15px rgba(0,0,0,.48),
        0 0 0 2px rgba(12,50,70,.92),
        inset 0 2px 0 rgba(255,255,255,.13),
        inset 0 -6px 12px rgba(0,0,0,.30);
}

.status-panel::before {
    content: "";

    position: absolute;

    inset: -4px;

    border-radius: 17px;

    border: 1px solid rgba(83,202,246,.62);

    pointer-events: none;
}

.status-panel::after {
    content: "";

    position: absolute;

    left: 12%;
    right: 12%;
    top: -3px;

    height: 3px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8fe8ff,
            transparent
        );

    box-shadow:
        0 0 8px rgba(71,204,250,.82);
}


/* ONLINE */

.status-top {
    height: 20px;

    display: flex;

    align-items: center;
    justify-content: center;

    gap: 8px;

    color: #a9ddec;

    font-size: 8px;

    font-weight: 900;

    letter-spacing: 1.2px;
}

.status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #2de57f;

    box-shadow:
        0 0 8px rgba(45,229,127,.95);
}


/* DIVIDER */

.status-divider {
    height: 1px;

    margin: 3px 8px 4px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #3cc2ed,
            transparent
        );
}


/* DATE/TIME ROW */

.status-row {
    height: 29px;

    display: flex;

    align-items: center;
    justify-content: flex-start;

    gap: 9px;

    padding-left: 16px;

    color: #ffffff;

    font-size: 15px;

    font-weight: 900;

    letter-spacing: .45px;

    font-variant-numeric: tabular-nums;
}

.status-row.time {
    color: #c4f2ff;
}

#current-date,
#current-time {
    text-align: left;
    font-variant-numeric: tabular-nums;
}

.status-icon {
    width: 18px;

    color: #20c3f7;

    font-size: 15px;

    text-align: center;
}

.status-label {
    width: 39px;

    color: #b9dfed;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: .25px;

    text-align: left;
}


/* =====================================================
   BOTTOM METALLIC RAIL
   ===================================================== */

.bottom-rail {
    position: absolute;

    z-index: 35;

    left: 0;
    right: 0;
    bottom: 0;

    height: 7px;

    background:
        linear-gradient(
            90deg,
            #063d64 0%,
            #1399d0 20%,
            #91e8ff 50%,
            #1399d0 80%,
            #063d64 100%
        );

    box-shadow:
        0 0 9px rgba(35,194,249,.90);
}

.bottom-rail::before,
.bottom-rail::after {
    content: "";

    position: absolute;

    top: 1px;

    width: 82px;
    height: 5px;

    background:
        repeating-linear-gradient(
            135deg,
            transparent 0 8px,
            rgba(255,255,255,.80) 8px 11px,
            transparent 11px 18px
        );
}

.bottom-rail::before {
    left: 18%;
}

.bottom-rail::after {
    right: 18%;
}


/* =====================================================
   RESPONSIVE
   ===================================================== */

@media (max-width: 1200px) {

    .logo-panel,
    .status-panel {
        width: 18%;
        min-width: 205px;
        height: 94px;
    }

    .title-frame {
        width: 49%;
        min-width: 500px;
        height: 100px;
    }

    .title-wing {
        display: none;
    }

    .tagline {
        font-size: 7px;
    }
}

@media (max-width: 900px) {

    .header {
        height: 125px;
        border-radius: 16px;
    }

    .industrial {
        height: 120px;
    }

    .logo-panel {
        left: 1.5%;
        width: 19%;
        min-width: 150px;
        height: 78px;
        border-radius: 11px;
    }

    .title-frame {
        width: 47%;
        min-width: 280px;
        height: 84px;
        border-radius: 12px;
    }

    .title-inner {
        border-radius: 9px;
    }

    .title-process {
        font-size: 21px;
    }

    .title-technology {
        font-size: 23px;
    }

    .status-panel {
        right: 1.5%;
        width: 19%;
        min-width: 150px;
        height: 78px;
        border-radius: 11px;
        padding: 5px 7px;
    }

    .status-row {
        font-size: 10px;
        height: 22px;
    }

    .status-top {
        font-size: 6px;
        height: 15px;
    }

    .tagline {
        display: none;
    }
}

</style>
</head>

<body>

<div class="header">

    <!-- INNER CURVED FRAME -->
    <div class="header-frame"></div>

    <!-- TOP GLOSS -->
    <div class="header-glow"></div>


    <!-- INDUSTRIAL BACKGROUND -->

    <svg
        class="industrial"
        viewBox="0 0 1672 145"
        preserveAspectRatio="none"
        aria-hidden="true">

        <!-- LEFT PLANT -->

        <g>

            <rect class="steel"
                  x="48" y="58"
                  width="22" height="82"
                  rx="3"/>

            <rect class="steel"
                  x="82" y="40"
                  width="34" height="100"
                  rx="5"/>

            <rect class="steel"
                  x="88" y="23"
                  width="22" height="19"/>

            <rect class="steel"
                  x="93" y="10"
                  width="12" height="15"/>

            <circle class="warm"
                    cx="99" cy="58" r="3"/>

            <circle class="warm"
                    cx="99" cy="81" r="3"/>

            <circle class="warm"
                    cx="99" cy="104" r="3"/>

            <path class="highlight"
                  d="
                    M99 10 V140
                    M84 62 H114
                    M84 86 H114
                    M84 110 H114
                  "/>

            <rect class="steel"
                  x="137" y="72"
                  width="52" height="68"
                  rx="25"/>

            <path class="highlight"
                  d="
                    M137 91 H189
                    M137 114 H189
                  "/>

            <circle class="glass"
                    cx="163" cy="102" r="5"/>

        </g>


        <!-- LEFT PIPING -->

        <g class="highlight">

            <path d="
                M0 121
                H310
                V92
                H395
            "/>

            <path d="
                M35 132
                H270
                V108
                H420
            "/>

            <path d="
                M170 77
                H285
                V52
                H380
            "/>

            <path d="
                M247 140
                V70
                H335
            "/>

        </g>


        <!-- RIGHT PLANT -->

        <g>

            <rect class="steel"
                  x="1430" y="57"
                  width="22" height="83"
                  rx="3"/>

            <rect class="steel"
                  x="1470" y="40"
                  width="34" height="100"
                  rx="5"/>

            <rect class="steel"
                  x="1476" y="23"
                  width="22" height="19"/>

            <rect class="steel"
                  x="1481" y="10"
                  width="12" height="15"/>

            <circle class="warm"
                    cx="1487" cy="58" r="3"/>

            <circle class="warm"
                    cx="1487" cy="81" r="3"/>

            <circle class="warm"
                    cx="1487" cy="104" r="3"/>

            <path class="highlight"
                  d="
                    M1487 10 V140
                    M1472 62 H1502
                    M1472 86 H1502
                    M1472 110 H1502
                  "/>

            <rect class="steel"
                  x="1533" y="72"
                  width="52" height="68"
                  rx="25"/>

            <path class="highlight"
                  d="
                    M1533 91 H1585
                    M1533 114 H1585
                  "/>

            <circle class="glass"
                    cx="1559" cy="102" r="5"/>

        </g>


        <!-- RIGHT PIPING -->

        <g class="highlight">

            <path d="
                M1672 121
                H1362
                V92
                H1277
            "/>

            <path d="
                M1637 132
                H1402
                V108
                H1252
            "/>

            <path d="
                M1502 77
                H1387
                V52
                H1292
            "/>

            <path d="
                M1425 140
                V70
                H1337
            "/>

        </g>


        <!-- TECHNICAL HEXAGONS -->

        <g class="tech">

            <path d="
                M270 25
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M309 58
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M1366 25
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

            <path d="
                M1405 58
                l18 -11
                l18 11
                v22
                l-18 11
                l-18-11z
            "/>

        </g>

    </svg>


    <!-- LOGO -->

    <div class="logo-panel">

        <img
            class="header-logo"
            src="data:image/jpeg;base64,LOGO_BASE64"
            alt="JSW JFE Steel Limited"
        >

    </div>


    <!-- TITLE SIDE WINGS -->

    <div class="title-wing left"></div>
    <div class="title-wing right"></div>


    <!-- CENTRAL 3D TITLE -->

    <div class="title-frame">

        <div class="title-inner">

            <div class="title-text">

                <div class="title-process">
                    PROCESS
                </div>

                <div class="title-technology">
                    TECHNOLOGY
                    <span class="title-pt">(PT)</span>
                </div>

            </div>

            <div class="title-line"></div>

        </div>

    </div>


    <!-- TAGLINE -->

    <div class="tagline">
        PROCESS SAFETY MANAGEMENT • DIGITAL OPERATIONS
    </div>


    <!-- RIGHT DATE / TIME PANEL -->

    <div class="status-panel">

        <div class="status-top">

            <span class="status-dot"></span>

            <span>SYSTEM ONLINE</span>

        </div>

        <div class="status-divider"></div>

        <div class="status-row">

            <span class="status-icon">▣</span>

            <span class="status-label">Date:</span>

            <span id="current-date">
                03.09.2026
            </span>

        </div>

        <div class="status-row time">

            <span class="status-icon">◷</span>

            <span class="status-label">Time:</span>

            <span id="current-time">
                00.00.00
            </span>

        </div>

    </div>


    <!-- BOTTOM RAIL -->

    <div class="bottom-rail"></div>

</div>


<script>

function updateDateTime() {

    const now = new Date();


    /* =================================================
       DATE — DD.MM.YYYY
       ================================================= */

    const dateParts = new Intl.DateTimeFormat(
        "en-GB",
        {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            timeZone: "Asia/Kolkata"
        }
    ).formatToParts(now);

    let day = "";
    let month = "";
    let year = "";

    dateParts.forEach(function(part) {

        if (part.type === "day") {
            day = part.value;
        }

        if (part.type === "month") {
            month = part.value;
        }

        if (part.type === "year") {
            year = part.value;
        }

    });

    document.getElementById("current-date").textContent =
        day + "." + month + "." + year;


    /* =================================================
       TIME — HH.MM.SS AM/PM
       ================================================= */

    const timeParts = new Intl.DateTimeFormat(
        "en-GB",
        {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,
            timeZone: "Asia/Kolkata"
        }
    ).formatToParts(now);

    let hour = "";
    let minute = "";
    let second = "";
    let dayPeriod = "";

    timeParts.forEach(function(part) {

        if (part.type === "hour") {
            hour = part.value;
        }

        if (part.type === "minute") {
            minute = part.value;
        }

        if (part.type === "second") {
            second = part.value;
        }

        if (part.type === "dayPeriod") {
            dayPeriod = part.value.toUpperCase();
        }

    });

    document.getElementById("current-time").textContent =
        hour + "." + minute + "." + second + " " + dayPeriod;
}


updateDateTime();

setInterval(
    updateDateTime,
    1000
);

</script>

</body>
</html>
"""

header_html = header_html.replace(
    "LOGO_BASE64",
    logo_base64
)

components.html(
    header_html,
    height=160,
    scrolling=False
)

# =========================================================
# RESET FILTER CALLBACK
# =========================================================

def reset_pt_filters():
    st.session_state.status_filter = "All"
    st.session_state.page_number = 1
    st.session_state.department_selector = "All Departments"
    st.session_state.view_pt_no = ""
    st.session_state.upload_pt_no = ""
    st.session_state.open_view_dialog = False
    st.session_state.open_upload_dialog = False


# =========================================================
# FILTER SECTION
# =========================================================

filter_month, filter_department, filter_reset = st.columns(
    [1.0, 1.0, 0.34],
    gap="small"
)
# =========================================================
# MONTH
# =========================================================

with filter_month:

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
# =========================================================
# DEPARTMENT
# =========================================================

with filter_department:

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


# =========================================================
# RESET FILTER
# =========================================================

with filter_reset:

    st.markdown(
        "<div style='height:46px;'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "↻ Reset Filters",
        use_container_width=True,
        key="reset_pt_filters_button",
        on_click=reset_pt_filters
    ):
        st.rerun()


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

total_pt = len(filtered_df)

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
    completed / total_pt * 100
    if total_pt
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
        "",
        "TOTAL PT",
        total_pt,
        "",
        "blue",
        "total"
    ),

    (
        "",
        "COMPLETED",
        completed,
        f"{completion_percentage:.1f}% completed",
        "green",
        "completed"
    ),

    (
        "",
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

        <div class="kpi-description">
            {description}
        </div>

    </div>

    <div class="kpi-pattern"></div>

    <div class="kpi-arrow">
        &gt;
    </div>

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
        PT REGISTER
    </div>
</div>
"""
)


# =========================================================
# PT REGISTER TOOLBAR
# =========================================================

search_col, all_col, completed_col, ongoing_col, refresh_col = st.columns(
    [2.8, 0.55, 0.85, 0.75, 1.05],
    gap="small"
)

with search_col:
    search_text = st.text_input(
        "Search",
        placeholder="Search PT No., Name of PT, Department...",
        label_visibility="collapsed",
        key="pt_search"
    )

with all_col:
    if st.button("All", use_container_width=True, key="pt_all"):
        st.session_state.status_filter = "All"
        st.session_state.page_number = 1
        st.rerun()

with completed_col:
    if st.button("Completed", use_container_width=True, key="pt_completed"):
        st.session_state.status_filter = "Completed"
        st.session_state.page_number = 1
        st.rerun()

with ongoing_col:
    if st.button("Ongoing", use_container_width=True, key="pt_ongoing"):
        st.session_state.status_filter = "Ongoing"
        st.session_state.page_number = 1
        st.rerun()

with refresh_col:
    if st.button("↻ Refresh Data", use_container_width=True, key="pt_refresh"):
        st.cache_data.clear()
        st.rerun()



# =========================================================
# SEARCH + STATUS FILTER
# =========================================================

display_df = filtered_df.copy()

if search_text.strip():
    q = search_text.strip().lower()

    search_mask = (
        display_df["PT No."].fillna("").astype(str).str.lower().str.contains(q, regex=False)
        | display_df["Department"].fillna("").astype(str).str.lower().str.contains(q, regex=False)
        | display_df["Name of PT"].fillna("").astype(str).str.lower().str.contains(q, regex=False)
        | display_df[STATUS_COLUMN].fillna("").astype(str).str.lower().str.contains(q, regex=False)
    )

    display_df = display_df[search_mask]

if st.session_state.status_filter != "All":
    display_df = display_df[
        display_df[STATUS_COLUMN].fillna("").astype(str).str.strip().str.lower()
        == st.session_state.status_filter.lower()
    ]


# =========================================================
# PT TABLE
# ONLY SIX COLUMNS SHOWN IN DASHBOARD
# =========================================================

ROWS_PER_PAGE = 5
total_entries = len(display_df)
total_pages = max(1, (total_entries + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)

if st.session_state.page_number > total_pages:
    st.session_state.page_number = total_pages

page_number = st.session_state.page_number
start_index = (page_number - 1) * ROWS_PER_PAGE
end_index = start_index + ROWS_PER_PAGE

page_df = display_df.iloc[start_index:end_index].copy()

# =========================================================
# PT TABLE
# The table appearance is retained. The two action columns
# use native Streamlit buttons so clicking them opens a
# modal dialog without URL navigation.
# =========================================================

# Table header remains the same HTML.
table_header = """
<div class="pt-table">
    <div class="pt-row pt-header">
        <div class="pt-cell">PT No.</div>
        <div class="pt-cell">Department</div>
        <div class="pt-cell">Name of PT</div>
        <div class="pt-cell">Status<br>(Ongoing/Completed)</div>
        <div class="pt-cell">Upload Document</div>
        <div class="pt-cell">View Document</div>
    </div>
</div>
"""

# We render each data row as a six-column Streamlit row.
# CSS below makes these rows visually match the existing
# PT table and removes the normal Streamlit column gap.
st.html(
    f"""
<style>
.pt-action-row [data-testid="stHorizontalBlock"] {{
    gap: 0 !important;
}}

.pt-action-row [data-testid="stColumn"] {{
    padding: 0 !important;
}}

.pt-action-cell {{
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
}}

.pt-action-cell.alt {{
    background: #f5f8fb;
}}

.pt-action-cell.left {{
    justify-content: flex-start;
    text-align: left;
}}

.pt-action-button-wrap {{
    height: 35px;
    display: flex;
    align-items: stretch;
}}

.pt-action-button-wrap > div {{
    width: 100%;
}}

.pt-action-button-wrap button {{
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
}}

.pt-action-button-wrap button:hover {{
    transform: none !important;
    box-shadow: none !important;
}}

.pt-upload-button button {{
    color: #e1262d !important;
}}

.pt-view-button button {{
    color: #174b87 !important;
}}

.pt-action-alt button {{
    background: #f5f8fb !important;
}}
</style>
"""
)

# Header
# Keep the original PT table heading styling exactly as in the dashboard.
st.html(
    f"""
<style>
.pt-table {{
    width: 100%;
    overflow: hidden;
    border: 1px solid #d5e0ea;
    background: #ffffff;
}}

.pt-row {{
    display: grid;
    grid-template-columns: 1.10fr 1.45fr 2.10fr 1.15fr 1.45fr 1.45fr;
}}

.pt-header {{
    min-height: 52px;
    background: linear-gradient(180deg, #205796 0%, #174b87 100%);
}}

.pt-header .pt-cell {{
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
}}

</style>
{table_header}
"""
)

for row_no, (_, row) in enumerate(page_df.iterrows()):
    alt = row_no % 2
    pt_no = str(row["PT No."]).strip()
    department = str(row["Department"]).strip()
    name_pt = str(row["Name of PT"]).strip()
    status = str(row[STATUS_COLUMN]).strip()

    if status.lower() == "completed":
        status_html = '<span class="status-completed">COMPLETED</span>'
    elif status.lower() == "ongoing":
        status_html = '<span class="status-ongoing">ONGOING</span>'
    else:
        status_html = f'<span class="status-normal">{status or "—"}</span>'

    # The marker lets CSS target only these row blocks.
    row_cols = st.columns(
        [1.10, 1.45, 2.10, 1.15, 1.45, 1.45],
        gap=None
    )

    with row_cols[0]:
        st.markdown(
            f'<div class="pt-action-cell {"alt" if alt else ""} left"><span class="pt-action-row-marker"></span>{pt_no}</div>',
            unsafe_allow_html=True
        )

    with row_cols[1]:
        st.markdown(
            f'<div class="pt-action-cell {"alt" if alt else ""} left">{department}</div>',
            unsafe_allow_html=True
        )

    with row_cols[2]:
        st.markdown(
            f'<div class="pt-action-cell {"alt" if alt else ""} left">{name_pt}</div>',
            unsafe_allow_html=True
        )

    with row_cols[3]:
        st.markdown(
            f'<div class="pt-action-cell {"alt" if alt else ""}">{status_html}</div>',
            unsafe_allow_html=True
        )

    with row_cols[4]:
        if st.button(
            "↑ Upload",
            key=f"upload_{safe_pt_folder_name(pt_no)}_{row_no}",
            use_container_width=True
        ):
            st.session_state.upload_pt_no = pt_no
            st.session_state.view_pt_no = ""
            st.session_state.open_upload_dialog = True
            st.session_state.open_view_dialog = False

    with row_cols[5]:
        if st.button(
            "◉ View",
            key=f"view_{safe_pt_folder_name(pt_no)}_{row_no}",
            use_container_width=True
        ):
            st.session_state.view_pt_no = pt_no
            st.session_state.upload_pt_no = ""
            st.session_state.open_view_dialog = True
            st.session_state.open_upload_dialog = False

# =========================================================
# ACTION BUTTON VISUAL TARGETING
# =========================================================
# This CSS is scoped only to the PT data rows.
st.markdown(
    """
<style>
div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker) {
    gap: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button,
div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
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

div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button {
    color: #e1262d !important;
}

div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
div[data-testid="stColumn"]:nth-child(6) button {
    color: #174b87 !important;
}

div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
div[data-testid="stColumn"]:nth-child(5) button:hover,
div[data-testid="stHorizontalBlock"]:has(.pt-action-row-marker)
div[data-testid="stColumn"]:nth-child(6) button:hover {
    background: #f5f8fb !important;
    color: inherit !important;
    border-color: #d5e0ea !important;
    box-shadow: none !important;
    transform: none !important;
}
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD DOCUMENT — VERY SMALL MODAL POPUP
# =========================================================

if st.session_state.open_upload_dialog and st.session_state.upload_pt_no:

    upload_pt = st.session_state.upload_pt_no
    st.session_state.open_upload_dialog = False

    @st.dialog("Upload Document", width="small")
    def upload_document_dialog():

        st.caption(f"PT No.  {upload_pt}")

        uploaded_file = st.file_uploader(
            "Choose file",
            type=[
                "pdf", "doc", "docx",
                "xls", "xlsx", "csv",
                "ppt", "pptx", "txt",
                "png", "jpg", "jpeg"
            ],
            key=f"uploader_dialog_{safe_pt_folder_name(upload_pt)}"
        )

        c1, c2 = st.columns(2, gap="small")

        with c1:
            if st.button(
                "Save",
                key=f"save_dialog_{safe_pt_folder_name(upload_pt)}",
                use_container_width=True,
                disabled=uploaded_file is None
            ):
                save_pt_document(upload_pt, uploaded_file)
                st.session_state.upload_pt_no = ""
                st.session_state.open_upload_dialog = False
                st.rerun()

        with c2:
            if st.button(
                "Cancel",
                key=f"cancel_dialog_{safe_pt_folder_name(upload_pt)}",
                use_container_width=True
            ):
                st.session_state.upload_pt_no = ""
                st.session_state.open_upload_dialog = False
                st.rerun()

    upload_document_dialog()


# =========================================================
# VIEW DOCUMENT — SEPARATE MODAL POPUP
# =========================================================

if st.session_state.open_view_dialog and st.session_state.view_pt_no:

    view_pt = st.session_state.view_pt_no
    st.session_state.open_view_dialog = False

    @st.dialog("View Document", width="large")
    def view_document_dialog():

        st.caption(f"PT No.  {view_pt}")

        documents = get_pt_documents(view_pt)

        if not documents:
            st.info("No document has been uploaded for this PT yet.")
            return

        document_names = [p.name for p in documents]

        selected_document_name = st.selectbox(
            "Select document",
            document_names,
            key=f"document_selector_{safe_pt_folder_name(view_pt)}"
        )

        selected_document = next(
            (p for p in documents if p.name == selected_document_name),
            None
        )

        if selected_document is None:
            return

        file_bytes = selected_document.read_bytes()
        mime_type = get_document_mime_type(selected_document)

        st.download_button(
            "↓ Download",
            data=file_bytes,
            file_name=selected_document.name,
            mime=mime_type,
            key=(
                f"download_{safe_pt_folder_name(view_pt)}_"
                f"{safe_pt_folder_name(selected_document.name)}"
            )
        )

        if mime_type == "application/pdf":

            pdf_base64 = base64.b64encode(file_bytes).decode("utf-8")

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

            st.image(file_bytes, use_container_width=True)

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
                    f"text_preview_{safe_pt_folder_name(view_pt)}_"
                    f"{safe_pt_folder_name(selected_document.name)}"
                )
            )

        else:

            st.info(
                "Preview is not available for this file type. "
                "Use Download to open the file."
            )

    view_document_dialog()


# =========================================================
# RECORD BAR + PAGINATION
# =========================================================

shown_from = start_index + 1 if total_entries else 0
shown_to = min(end_index, total_entries)

p1, p2, p3, p4, p5, p6 = st.columns(
    [3.2, 0.45, 0.45, 0.45, 0.45, 0.45],
    gap="small"
)

with p1:
    st.markdown(
        f"""
        <div style="
            height:38px;
            display:flex;
            align-items:center;
            padding-left:12px;
            color:#5d7085;
            font-size:11px;
            font-weight:600;
        ">
            Showing {shown_from} to {shown_to} of {total_entries} entries
        </div>
        """,
        unsafe_allow_html=True
    )

with p2:
    if st.button("«", key="page_first", use_container_width=True):
        st.session_state.page_number = 1
        st.session_state.view_pt_no = ""
        st.session_state.upload_pt_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()

with p3:
    if st.button("‹", key="page_prev", use_container_width=True):
        st.session_state.page_number = max(1, page_number - 1)
        st.session_state.view_pt_no = ""
        st.session_state.upload_pt_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()

with p4:
    st.markdown(
        f"""
        <div style="
            height:36px;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#174b87;
            color:white;
            border-radius:6px;
            font-size:12px;
            font-weight:900;
        ">{page_number}</div>
        """,
        unsafe_allow_html=True
    )

with p5:
    if st.button("›", key="page_next", use_container_width=True):
        st.session_state.page_number = min(total_pages, page_number + 1)
        st.session_state.view_pt_no = ""
        st.session_state.upload_pt_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()

with p6:
    if st.button("»", key="page_last", use_container_width=True):
        st.session_state.page_number = total_pages
        st.session_state.view_pt_no = ""
        st.session_state.upload_pt_no = ""
        st.session_state.open_view_dialog = False
        st.session_state.open_upload_dialog = False
        st.rerun()


# =========================================================
# GOOGLE SHEET SOURCE
# =========================================================
# The data source remains the Google Sheet tab named "PT".
#
# Fetched from PT:
#   1. PT No.
#   2. Department
#   3. Name of PT
#   4. Status (Ongoing/Completed)
#
# Upload Document and View Document are dashboard action
# columns and are NOT fetched as data columns from the sheet.
#
# The existing Month selector is retained. No Month column
# exists in the requested PT parameters, so no artificial
# month filter is applied.

