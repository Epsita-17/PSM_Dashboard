import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PSM Dashboard - PHA",
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
# =========================================================

DOCUMENT_FOLDER = "pha_documents"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)

# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [

    "Sr No",
    "PHA No",
    "Department",
    "Name of PHA",
    "Status  (Ongoing/Completed)",
    "Upload Document",
    "View Document"
]

STATUS_COLUMN = "Status  (Ongoing/Completed)"

# =========================================================
# CHECK DATA
# =========================================================

if df.empty:
    st.error(
        "No data found in Google Sheet Sheet2."
    )

    st.stop()

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Some required columns are missing from Sheet2."
    )

    st.write("Missing columns:")
    st.write(missing_columns)

    st.write("Columns found in Sheet2:")
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

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# INDUSTRIAL REFERENCE HEADER
# =========================================================

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

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}

body {
    background: #06111f;
}


/* =====================================================
   MAIN HEADER FRAME
   ===================================================== */

.header {

    position: relative;

    width: 100%;
    height: 100px;

    overflow: hidden;

    background:

        radial-gradient(
            ellipse at center,
            rgba(15,91,150,.32) 0%,
            rgba(5,29,52,.96) 48%,
            #020b16 100%
        );

    border-top:
        1px solid #238ed8;

    border-bottom:
        2px solid #0a83d0;

    box-shadow:

        0 0 0 1px rgba(0,153,255,.18),

        0 5px 18px
        rgba(0,0,0,.42),

        inset 0 1px 0
        rgba(255,255,255,.08);
}


/* =====================================================
   SUBTLE TECH GRID
   ===================================================== */

.header::before {

    content: "";

    position: absolute;

    inset: 0;

    background:

        linear-gradient(
            rgba(0,126,220,.055) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(0,126,220,.055) 1px,
            transparent 1px
        );

    background-size: 26px 26px;

    opacity: .75;
}


/* =====================================================
   BLUE SIDE LIGHT
   ===================================================== */

.header::after {

    content: "";

    position: absolute;

    inset: 0;

    background:

        linear-gradient(
            90deg,
            rgba(0,137,255,.20),
            transparent 14%,
            transparent 86%,
            rgba(0,137,255,.20)
        );

    pointer-events: none;
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
    height: 100px;

    z-index: 1;

    opacity: .72;
}

.industrial .steel {

    fill: #102b43;

    stroke: #2675a8;

    stroke-width: 1.3;
}

.industrial .highlight {

    fill: none;

    stroke: #49b8ff;

    stroke-width: 1.15;

    opacity: .65;
}

.industrial .warm {

    fill: #e9a63a;

    opacity: .82;
}

.industrial .glass {

    fill: #0b5c91;

    stroke: #4cbcff;

    stroke-width: .7;

    opacity: .55;
}

.tech {

    fill: none;

    stroke: #238bd0;

    stroke-width: 1;

    opacity: .25;
}


/* =====================================================
   SIDE FADE
   ===================================================== */

.side-fade {

    position: absolute;

    z-index: 3;

    top: 0;
    bottom: 0;

    width: 24%;

    pointer-events: none;
}

.side-fade.left {

    left: 0;

    background:
        linear-gradient(
            90deg,
            rgba(1,8,18,.74),
            transparent
        );
}

.side-fade.right {

    right: 0;

    background:
        linear-gradient(
            270deg,
            rgba(1,8,18,.74),
            transparent
        );
}


/* =====================================================
   CENTRAL 3D TITLE PLATE
   ===================================================== */

.title-plate {

    position: absolute;

    z-index: 10;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%);

    width:
        min(92%, 950px);

    height:
        72px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:

        linear-gradient(
            180deg,
            #124e80 0%,
            #07345f 45%,
            #031e3d 100%
        );

    border:
        2px solid #78cfff;

    border-radius:
        15px;

    box-shadow:

        0 0 0 3px rgba(6,36,65,.92),

        0 0 0 5px rgba(105,183,229,.55),

        0 8px 20px
        rgba(0,0,0,.52),

        0 0 22px
        rgba(0,139,255,.42),

        inset 0 2px 0
        rgba(255,255,255,.28),

        inset 0 -8px 15px
        rgba(0,0,0,.24);
}


/* =====================================================
   METALLIC BEVEL
   ===================================================== */

.title-plate::before {

    content: "";

    position: absolute;

    inset: -10px;

    z-index: -1;

    border-radius:
        20px;

    border:
        5px solid transparent;

    background:

        linear-gradient(
            145deg,
            #f5fbff 0%,
            #7d9bad 16%,
            #e7f0f5 28%,
            #536d7e 48%,
            #d8e7ef 68%,
            #668092 82%,
            #f5fbff 100%
        ) border-box;

    -webkit-mask:
        linear-gradient(#fff 0 0) padding-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite:
        xor;

    mask-composite:
        exclude;

    box-shadow:
        0 0 10px rgba(112,199,255,.35);
}


/* =====================================================
   BLUE INNER LIGHT
   ===================================================== */

.title-plate::after {

    content: "";

    position: absolute;

    left: 13px;
    right: 13px;
    top: 6px;

    height: 2px;

    border-radius: 10px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #50c8ff 18%,
            #d8f5ff 50%,
            #50c8ff 82%,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(55,190,255,.72);
}


/* =====================================================
   TITLE
   ===================================================== */

.title-text {

    position: relative;

    z-index: 12;

    color:
        #ffc400;

    font-size:
        clamp(30px, 3.2vw, 54px);

    font-weight:
        950;

    letter-spacing:
        1px;

    line-height:
        1;

    text-align:
        center;

    text-shadow:

        0 2px 0 #8c5f00,

        0 3px 5px
        rgba(0,0,0,.65),

        0 0 12px
        rgba(255,194,0,.22);
}


/* =====================================================
   NAVIGATION ARROWS
   ===================================================== */

.nav-arrow {

    position:
        absolute;

    z-index:
        13;

    top:
        50%;

    transform:
        translateY(-50%);

    color:
        #54c9ff;

    font-size:
        32px;

    line-height:
        1;

    font-weight:
        950;

    text-shadow:

        0 0 7px
        rgba(40,187,255,.9),

        0 2px 2px
        rgba(0,0,0,.65);
}

.nav-left {
    left: 28px;
}

.nav-right {
    right: 28px;
}


/* =====================================================
   CORNER ARMOUR
   ===================================================== */

.corner {

    position:
        absolute;

    z-index:
        9;

    width:
        180px;

    height:
        35px;

    border:
        2px solid #168bd4;

    background:
        linear-gradient(
            135deg,
            rgba(11,82,135,.85),
            rgba(4,27,49,.2)
        );

    box-shadow:
        0 0 12px
        rgba(0,133,255,.24),

        inset 0 1px 0
        rgba(255,255,255,.16);
}

.corner.left {

    left:
        -35px;

    top:
        4px;

    transform:
        skewX(-38deg);
}

.corner.right {

    right:
        -35px;

    top:
        4px;

    transform:
        skewX(38deg);
}


/* =====================================================
   TOP METAL RAIL
   ===================================================== */

.top-rail {

    position:
        absolute;

    z-index:
        11;

    left:
        31%;

    right:
        31%;

    top:
        3px;

    height:
        5px;

    border-radius:
        10px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #7594a7 10%,
            #eef8ff 35%,
            #4c728b 50%,
            #eef8ff 65%,
            #7594a7 90%,
            transparent
        );

    box-shadow:
        0 0 9px
        rgba(52,164,230,.55);
}


/* =====================================================
   BOTTOM BLUE ENERGY LINE
   ===================================================== */

.energy-line {

    position:
        absolute;

    z-index:
        15;

    left:
        0;

    bottom:
        0;

    width:
        100%;

    height:
        3px;

    background:

        linear-gradient(
            90deg,
            #07548d 0%,
            #0ca6ff 25%,
            #ffffff 50%,
            #0ca6ff 75%,
            #07548d 100%
        );

    box-shadow:

        0 0 7px
        #008dff,

        0 0 18px
        rgba(0,141,255,.75);
}


/* =====================================================
   FINAL KPI STYLE MATCH
   TOP 3 KPI + BOTTOM 6 KPI = SAME APPEARANCE
   ===================================================== */

/* Same card background, border, height, radius and shadow */
.kpi-card,
.pha-rec-kpi {
    position: relative !important;

    height: 105px !important;

    overflow: hidden !important;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 72%,
            #edf4fa 100%
        ) !important;

    border:
        1.5px solid #c2d3e4 !important;

    border-top:
        4px solid #176fc1 !important;

    border-radius:
        8px !important;

    padding:
        17px 16px !important;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98) !important;
}


/* Remove different green/orange/red top borders */
.kpi-card.completed,
.kpi-card.ongoing,
.pha-rec-kpi.total,
.pha-rec-kpi.approved,
.pha-rec-kpi.rejected,
.pha-rec-kpi.overdue,
.pha-rec-kpi.completed,
.pha-rec-kpi.pending {
    border-top:
        4px solid #176fc1 !important;
}


/* Same centered content structure */
.kpi-content,
.pha-rec-kpi-content {
    margin-left:
        0 !important;

    width:
        100% !important;

    height:
        100% !important;

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;
}


/* Same heading font */
.kpi-label,
.pha-rec-kpi-label {
    color:
        #092d5c !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        900 !important;

    letter-spacing:
        .15px !important;

    line-height:
        1.15 !important;

    text-align:
        center !important;
}


/* Same number font */
.kpi-value,
.pha-rec-kpi-value {
    color:
        #0a4e91 !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        42px !important;

    line-height:
        1 !important;

    font-weight:
        900 !important;

    margin-top:
        6px !important;

    text-align:
        center !important;
}


/* Same description font */
.kpi-description,
.pha-rec-kpi-description {
    color:
        #304d6d !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        11px !important;

    font-weight:
        700 !important;

    margin-top:
        7px !important;

    text-align:
        center !important;
}


/* Remove status-specific text colors */
.kpi-card.completed .kpi-label,
.kpi-card.ongoing .kpi-label,
.kpi-value.green,
.kpi-value.orange,
.pha-rec-kpi.approved .pha-rec-kpi-label,
.pha-rec-kpi.completed .pha-rec-kpi-label,
.pha-rec-kpi.rejected .pha-rec-kpi-label,
.pha-rec-kpi.overdue .pha-rec-kpi-label,
.pha-rec-kpi.pending .pha-rec-kpi-label {
    color:
        #092d5c !important;
}


/* All KPI numbers use the same blue */
.kpi-card.completed .kpi-value,
.kpi-card.ongoing .kpi-value,
.pha-rec-kpi.approved .pha-rec-kpi-value,
.pha-rec-kpi.completed .pha-rec-kpi-value,
.pha-rec-kpi.rejected .pha-rec-kpi-value,
.pha-rec-kpi.overdue .pha-rec-kpi-value,
.pha-rec-kpi.pending .pha-rec-kpi-value {
    color:
        #0a4e91 !important;
}


/* Same hover appearance */
.kpi-card:hover,
.pha-rec-kpi:hover {
    transform:
        translateY(-2px) !important;

    box-shadow:
        0 7px 16px rgba(6,48,91,.17),
        0 2px 4px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,1) !important;
}


/* No icons/patterns/arrows in either KPI group */
.kpi-icon,
.kpi-pattern,
.kpi-arrow,
.pha-rec-kpi-icon,
.pha-rec-kpi-pattern,
.pha-rec-kpi-arrow {
    display:
        none !important;
}


/* =====================================================
   FINAL KPI UNIFICATION
   ALL 9 CARDS USE THE SAME COMPONENT
   ===================================================== */

.kpi-card {
    height: 105px !important;
    position: relative !important;
    overflow: hidden !important;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 72%,
            #edf4fa 100%
        ) !important;

    border:
        1.5px solid #c2d3e4 !important;

    border-top:
        4px solid #176fc1 !important;

    border-radius:
        8px !important;

    padding:
        17px 16px !important;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98) !important;

    transition:
        transform .15s ease,
        box-shadow .15s ease !important;
}

.kpi-card:hover {
    transform:
        translateY(-2px) !important;

    box-shadow:
        0 7px 16px rgba(6,48,91,.17),
        0 2px 4px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,1) !important;
}

.kpi-card .kpi-content {
    margin-left:
        0 !important;

    width:
        100% !important;

    height:
        100% !important;

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;
}

.kpi-card .kpi-label {
    color:
        #092d5c !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        900 !important;

    letter-spacing:
        .15px !important;

    line-height:
        1.15 !important;

    text-align:
        center !important;
}

.kpi-card .kpi-value {
    color:
        #0a4e91 !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        42px !important;

    line-height:
        1 !important;

    font-weight:
        900 !important;

    margin-top:
        6px !important;

    text-align:
        center !important;
}

.kpi-card .kpi-description {
    color:
        #0a4e91 !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        11px !important;

    font-weight:
        700 !important;

    margin-top:
        7px !important;

    text-align:
        center !important;
}

.kpi-card .kpi-icon,
.kpi-card .kpi-pattern,
.kpi-card .kpi-arrow {
    display:
        none !important;
}


/* =====================================================
   FINAL: ALL KPI ROWS SAME COLORS AS TOP ROW
   ===================================================== */

.kpi-card .kpi-label,
.kpi-card.completed .kpi-label,
.kpi-card.ongoing .kpi-label {
    color: #092d5c !important;
}

.kpi-card .kpi-value,
.kpi-card .kpi-value.green,
.kpi-card .kpi-value.orange {
    color: #0a4e91 !important;
}

.kpi-card .kpi-description {
    color: #0a4e91 !important;
}


/* =====================================================
   FINAL STATUS COLOR SYSTEM
   SAME STATUS = SAME COLOR IN EVERY KPI ROW/COLUMN
   ===================================================== */

/* -----------------------------
   BLUE — TOTAL
   ----------------------------- */

.kpi-card.total .kpi-label,
.kpi-card.total .kpi-value,
.kpi-card.total .kpi-description {
    color: #0a4e91 !important;
}

.kpi-card.total {
    border-top-color: #176fc1 !important;
}


/* -----------------------------
   GREEN — COMPLETED + APPROVED
   ----------------------------- */

.kpi-card.completed .kpi-label,
.kpi-card.completed .kpi-value,
.kpi-card.completed .kpi-description,
.pha-rec-kpi.completed .pha-rec-kpi-label,
.pha-rec-kpi.completed .pha-rec-kpi-value,
.pha-rec-kpi.completed .pha-rec-kpi-description,
.pha-rec-kpi.approved .pha-rec-kpi-label,
.pha-rec-kpi.approved .pha-rec-kpi-value,
.pha-rec-kpi.approved .pha-rec-kpi-description {
    color: #159447 !important;
}

.kpi-card.completed,
.pha-rec-kpi.completed,
.pha-rec-kpi.approved {
    border-top-color: #19a657 !important;
}


/* -----------------------------
   RED — REJECTED + OVERDUE
   ----------------------------- */

.pha-rec-kpi.rejected .pha-rec-kpi-label,
.pha-rec-kpi.rejected .pha-rec-kpi-value,
.pha-rec-kpi.rejected .pha-rec-kpi-description,
.pha-rec-kpi.overdue .pha-rec-kpi-label,
.pha-rec-kpi.overdue .pha-rec-kpi-value,
.pha-rec-kpi.overdue .pha-rec-kpi-description {
    color: #d9534f !important;
}

.pha-rec-kpi.rejected,
.pha-rec-kpi.overdue {
    border-top-color: #d9534f !important;
}


/* -----------------------------
   ORANGE — ONGOING + PENDING
   ----------------------------- */

.kpi-card.ongoing .kpi-label,
.kpi-card.ongoing .kpi-value,
.kpi-card.ongoing .kpi-description,
.pha-rec-kpi.pending .pha-rec-kpi-label,
.pha-rec-kpi.pending .pha-rec-kpi-value,
.pha-rec-kpi.pending .pha-rec-kpi-description {
    color: #f0a000 !important;
}

.kpi-card.ongoing,
.pha-rec-kpi.pending {
    border-top-color: #f18d05 !important;
}


/* -----------------------------
   IMPORTANT:
   TOTAL RECOMMENDATION = BLUE
   ----------------------------- */

.pha-rec-kpi.total .pha-rec-kpi-label,
.pha-rec-kpi.total .pha-rec-kpi-value,
.pha-rec-kpi.total .pha-rec-kpi-description {
    color: #0a4e91 !important;
}

.pha-rec-kpi.total {
    border-top-color: #176fc1 !important;
}


/* =====================================================
   FINAL FIX — COLUMN COLORS MATCH TOP ROW
   ===================================================== */

/* ALL 9 CARDS: identical physical appearance */
.kpi-card {
    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 72%,
            #edf4fa 100%
        ) !important;

    border:
        1.5px solid #c2d3e4 !important;

    border-radius:
        8px !important;

    height:
        105px !important;

    padding:
        17px 16px !important;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98) !important;

    transition:
        transform .15s ease,
        box-shadow .15s ease !important;
}


/* =====================================================
   COLUMN 1 — BLUE
   TOP: TOTAL PHA
   LOWER: TOTAL RECOMMENDATION + OVERDUE
   ===================================================== */

.kpi-card.total {
    border-top:
        4px solid #176fc1 !important;
}

.kpi-card.total .kpi-label,
.kpi-card.total .kpi-value,
.kpi-card.total .kpi-description {
    color:
        #0a4e91 !important;
}


/* =====================================================
   COLUMN 2 — GREEN
   TOP: COMPLETED
   LOWER: APPROVED + COMPLETED
   ===================================================== */

.kpi-card.completed,
.kpi-card.approved {
    border-top:
        4px solid #19a657 !important;
}

.kpi-card.completed .kpi-label,
.kpi-card.completed .kpi-value,
.kpi-card.completed .kpi-description,
.kpi-card.approved .kpi-label,
.kpi-card.approved .kpi-value,
.kpi-card.approved .kpi-description {
    color:
        #159447 !important;
}


/* =====================================================
   COLUMN 3 — ORANGE
   TOP: ONGOING
   LOWER: REJECTED + PENDING
   ===================================================== */

.kpi-card.ongoing,
.kpi-card.rejected,
.kpi-card.pending {
    border-top:
        4px solid #f18d05 !important;
}

.kpi-card.ongoing .kpi-label,
.kpi-card.ongoing .kpi-value,
.kpi-card.ongoing .kpi-description,
.kpi-card.rejected .kpi-label,
.kpi-card.rejected .kpi-value,
.kpi-card.rejected .kpi-description,
.kpi-card.pending .kpi-label,
.kpi-card.pending .kpi-value,
.kpi-card.pending .kpi-description {
    color:
        #f0a000 !important;
}


/* =====================================================
   SAME HOVER / MOVEMENT FOR ALL 9
   ===================================================== */

.kpi-card:hover {
    transform:
        translateY(-2px) !important;

    box-shadow:
        0 7px 16px rgba(6,48,91,.17),
        0 2px 4px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,1) !important;
}


/* =====================================================
   SAME CONTENT ALIGNMENT FOR ALL 9
   ===================================================== */

.kpi-card .kpi-content {
    margin-left:
        0 !important;

    width:
        100% !important;

    height:
        100% !important;

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;
}


/* =====================================================
   SAME TYPOGRAPHY
   ===================================================== */

.kpi-card .kpi-label {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        900 !important;

    letter-spacing:
        .15px !important;

    line-height:
        1.15 !important;

    text-align:
        center !important;
}

.kpi-card .kpi-value {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        42px !important;

    line-height:
        1 !important;

    font-weight:
        900 !important;

    margin-top:
        6px !important;

    text-align:
        center !important;
}

.kpi-card .kpi-description {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        11px !important;

    font-weight:
        700 !important;

    margin-top:
        7px !important;

    text-align:
        center !important;
}


/* No icon/pattern/arrow — exactly like the current top cards */
.kpi-card .kpi-icon,
.kpi-card .kpi-pattern,
.kpi-card .kpi-arrow {
    display:
        none !important;
}


/* =====================================================
   FINAL DASHBOARD KPI STYLE
   TOP ROW IS THE COLOR REFERENCE
   COLUMN 1 = BLUE | COLUMN 2 = GREEN | COLUMN 3 = ORANGE
   ===================================================== */

/* ---------- COMMON CARD LOOK ---------- */

.kpi-card {
    position: relative !important;
    height: 105px !important;
    overflow: hidden !important;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 72%,
            #edf4fa 100%
        ) !important;

    border:
        1.5px solid #c2d3e4 !important;

    border-radius:
        8px !important;

    padding:
        17px 16px !important;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98) !important;

    transition:
        transform .15s ease,
        box-shadow .15s ease !important;
}


/* ---------- SAME HOVER FOR ALL BOXES ---------- */

.kpi-card:hover {
    transform:
        translateY(-2px) !important;

    box-shadow:
        0 7px 16px rgba(6,48,91,.17),
        0 2px 4px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,1) !important;
}


/* ---------- SAME CONTENT POSITION ---------- */

.kpi-content {
    margin-left:
        0 !important;

    width:
        100% !important;

    height:
        100% !important;

    display:
        flex !important;

    flex-direction:
        column !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    text-align:
        center !important;
}


/* ---------- SAME FONT ---------- */

.kpi-label {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        15px !important;

    font-weight:
        900 !important;

    letter-spacing:
        .15px !important;

    line-height:
        1.15 !important;

    text-align:
        center !important;
}

.kpi-value {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        42px !important;

    line-height:
        1 !important;

    font-weight:
        900 !important;

    margin-top:
        6px !important;

    text-align:
        center !important;
}

.kpi-description {
    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        11px !important;

    font-weight:
        700 !important;

    margin-top:
        7px !important;

    text-align:
        center !important;
}


/* =====================================================
   COLUMN 1 — BLUE
   TOTAL PHA
   TOTAL RECOMMENDATION
   OVERDUE
   ===================================================== */

.kpi-card.total,
.kpi-card.overdue {
    border-top:
        4px solid #176fc1 !important;
}

.kpi-card.total .kpi-label,
.kpi-card.total .kpi-value,
.kpi-card.total .kpi-description,
.kpi-card.overdue .kpi-label,
.kpi-card.overdue .kpi-value,
.kpi-card.overdue .kpi-description {
    color:
        #0a4e91 !important;
}


/* =====================================================
   COLUMN 2 — GREEN
   COMPLETED
   APPROVED
   COMPLETED
   ===================================================== */

.kpi-card.completed,
.kpi-card.approved {
    border-top:
        4px solid #19a657 !important;
}

.kpi-card.completed .kpi-label,
.kpi-card.completed .kpi-value,
.kpi-card.completed .kpi-description,
.kpi-card.approved .kpi-label,
.kpi-card.approved .kpi-value,
.kpi-card.approved .kpi-description {
    color:
        #159447 !important;
}


/* =====================================================
   COLUMN 3 — ORANGE
   ONGOING
   REJECTED
   PENDING
   ===================================================== */

.kpi-card.ongoing,
.kpi-card.rejected,
.kpi-card.pending {
    border-top:
        4px solid #f18d05 !important;
}

.kpi-card.ongoing .kpi-label,
.kpi-card.ongoing .kpi-value,
.kpi-card.ongoing .kpi-description,
.kpi-card.rejected .kpi-label,
.kpi-card.rejected .kpi-value,
.kpi-card.rejected .kpi-description,
.kpi-card.pending .kpi-label,
.kpi-card.pending .kpi-value,
.kpi-card.pending .kpi-description {
    color:
        #f0a000 !important;
}


/* =====================================================
   REMOVE OLD STATUS COLORS / ICONS
   ===================================================== */

.kpi-card .kpi-icon,
.kpi-card .kpi-pattern,
.kpi-card .kpi-arrow {
    display:
        none !important;
}

</style>
</head>

<body>

<div class="header">

    <div class="corner left"></div>
    <div class="corner right"></div>

    <div class="top-rail"></div>


    <svg
        class="industrial"
        viewBox="0 0 1672 145"
        preserveAspectRatio="none"
        aria-hidden="true">

        <!-- LEFT INDUSTRIAL PLANT -->

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


        <!-- RIGHT INDUSTRIAL PLANT -->

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


    <div class="side-fade left"></div>
    <div class="side-fade right"></div>


    <!-- CENTRAL 3D TITLE -->

    <div class="title-plate">

        <div class="nav-arrow nav-left">
            ◀◀
        </div>

        <div class="title-text">
            Process Hazard Analysis (PHA)
        </div>

        <div class="nav-arrow nav-right">
            ▶▶
        </div>

    </div>


    <div class="energy-line"></div>

</div>

</body>
</html>
"""

components.html(
    header_html,
    height=100,
    scrolling=False
)

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

        <div class="kpi-description">
            {description}
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

        <div class="kpi-description">
            {description}
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
        st.cache_data.clear()
        st.rerun()



# =========================================================
# STATUS FILTER
# =========================================================

if all_button:

    st.session_state.status_filter = "All"
    st.session_state.page_number = 1

elif completed_button:

    st.session_state.status_filter = "Completed"
    st.session_state.page_number = 1

elif ongoing_button:

    st.session_state.status_filter = "Ongoing"
    st.session_state.page_number = 1

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
# Product / Process / Location intentionally removed
# =========================================================

table_widths = [
    .45,  # Sr No
    .85,  # PHA
    1.25,  # Department
    1.65,  # Name
    .95,  # Status
    1.15,  # Upload
    1.05  # View
]

table_headers = [
    "Sr No",
    "PHA No",
    "Department",
    "Name of PHA",
    "Status  (Ongoing/Completed)",
    "Upload Document",
    "View Document"
]

header_columns = st.columns(
    table_widths,
    gap="small"
)

for column, header_text in zip(
        header_columns,
        table_headers
):
    with column:
        st.html(
            f"""
<div class="table-head">
    {header_text}
</div>
"""
        )

# =========================================================
# TABLE ROWS
# =========================================================

for row_number, (_, row) in enumerate(
        page_df.iterrows()
):

    row_columns = st.columns(
        table_widths,
        gap="small"
    )

    alternate = (
        " alt"
        if row_number % 2 == 1
        else ""
    )

    # -----------------------------------------------------
    # DATA CELLS
    # -----------------------------------------------------

    row_values = [

        row["Sr No"],
        row["PHA No"],
        row["Department"],
        row["Name of PHA"]

    ]

    row_positions = [
        0, 1, 2, 3
    ]

    for position, value in zip(
            row_positions,
            row_values
    ):

        with row_columns[position]:

            value_text = str(
                value
            ).strip()

            if value_text.lower() == "nan":
                value_text = ""

            left_class = (
                " left"
                if position in [2, 3]
                else ""
            )

            st.html(
                f"""
<div class="table-cell{alternate}{left_class}">
    {value_text}
</div>
"""
            )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    with row_columns[4]:

        status = str(
            row[STATUS_COLUMN]
        ).strip().lower()

        if status == "completed":

            status_html = """
<span class="status-pill status-completed">
    ● COMPLETED
</span>
"""

        elif status == "ongoing":

            status_html = """
<span class="status-pill status-ongoing">
    ● ONGOING
</span>
"""

        else:

            status_html = """
<span class="status-pill">
    —
</span>
"""

        st.html(
            f"""
<div class="table-cell{alternate}">
    {status_html}
</div>
"""
        )

    # -----------------------------------------------------
    # UPLOAD
    # -----------------------------------------------------

    with row_columns[5]:

        if st.button(
                "📤 Upload",
                key=(
                        f"upload_{page_number}_"
                        f"{row_number}_"
                        f"{row['PHA No']}"
                ),
                use_container_width=True
        ):
            st.session_state.upload_pha_no = str(
                row["PHA No"]
            )

            st.session_state.open_upload_dialog = True

            st.rerun()

    # -----------------------------------------------------
    # VIEW
    # -----------------------------------------------------

    with row_columns[6]:

        if st.button(
                "📄 View",
                key=(
                        f"view_{page_number}_"
                        f"{row_number}_"
                        f"{row['PHA No']}"
                ),
                use_container_width=True
        ):
            st.session_state.view_pha_no = str(
                row["PHA No"]
            )

            st.rerun()

# =========================================================
# VIEW DOCUMENT
# =========================================================

view_pha = st.session_state.get(
    "view_pha_no",
    ""
)

if view_pha:

    matching_files = []

    if os.path.exists(DOCUMENT_FOLDER):

        for filename in os.listdir(
                DOCUMENT_FOLDER
        ):

            if filename.startswith(
                    f"{view_pha}_"
            ):
                matching_files.append(
                    filename
                )

    if matching_files:

        st.info(
            f"Documents available for {view_pha}: "
            f"{len(matching_files)}"
        )

        for filename in matching_files:
            file_path = os.path.join(
                DOCUMENT_FOLDER,
                filename
            )

            with open(
                    file_path,
                    "rb"
            ) as document_file:
                st.download_button(
                    label=f"📄 {filename}",
                    data=document_file.read(),
                    file_name=filename,
                    key=f"download_{filename}"
                )

    else:

        st.caption(
            f"No uploaded document found for {view_pha}."
        )

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

        recommendation_register_html += (
            f"<th>{column}</th>"
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
# UPLOAD DIALOG
# =========================================================
# =========================================================
# UPLOAD DIALOG
# =========================================================

if st.session_state.get(
        "open_upload_dialog",
        False
):

    @st.dialog("📤 Upload PHA Document")
    def upload_document_dialog():

        pha_no = st.session_state.get(
            "upload_pha_no",
            ""
        )

        if pha_no:

            st.write(
                f"PHA No: **{pha_no}**"
            )

        else:

            st.info(
                "Enter the PHA number for this document."
            )

            pha_no = st.text_input(
                "PHA No.",
                key="dialog_pha_no"
            )

        uploaded_file = st.file_uploader(
            "Select document from your computer",
            type=[
                "pdf",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "ppt",
                "pptx",
                "jpg",
                "jpeg",
                "png"
            ],
            key="pt_upload_file"
        )

        if uploaded_file is not None:

            if not pha_no:

                st.warning(
                    "Please enter PHA No first."
                )

            else:

                file_name = (
                    f"{pha_no}_"
                    f"{uploaded_file.name}"
                )

                file_path = os.path.join(
                    DOCUMENT_FOLDER,
                    file_name
                )

                with open(
                        file_path,
                        "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                st.success(
                    f"Document uploaded successfully for {pha_no}"
                )

                st.session_state.open_upload_dialog = False
                st.session_state.upload_pha_no = ""

                st.rerun()


    upload_document_dialog()

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

