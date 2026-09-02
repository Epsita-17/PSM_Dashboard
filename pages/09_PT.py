import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh
from components.psm_theme import apply_psm_theme, psm_header, psm_section

apply_psm_theme()


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

if "upload_pt_no" not in st.session_state:
    st.session_state.upload_pt_no = ""

if "open_upload_dialog" not in st.session_state:
    st.session_state.open_upload_dialog = False

if "view_pt_no" not in st.session_state:
    st.session_state.view_pt_no = ""


# =========================================================
# AUTO REFRESH
# =========================================================

if not st.session_state.open_upload_dialog:
    st_autorefresh(
        interval=1000,
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
            f"Unable to load Google Sheet Sheet2: {exc}"
        )

        return pd.DataFrame()


df = get_pt_data()


# =========================================================
# DOCUMENT STORAGE
# =========================================================

DOCUMENT_FOLDER = "pt_documents"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [

    "Sr No",
    "PT No.",
    "Department",
    "Name of PT",
    "Status  (Ongoing/Completed)",
    "Product",
    "Process",
    "Location",
    "Valid Till",
    "Approved  (Yes/No)",
    "P&ID updated",
    "PFD",
    "Equipment Datasheets",
    "Design basis",
    "Process parameters",
    "SOC",
    "SOL",
    "Chemical Properties",
    "MSDS/SDS Available",
    "Process chemistry",
    "Documents updated",
    "Attach PT Softcopy Link",
    "Remarks",
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
# LIGHT 3D INDUSTRIAL THEME
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   FULL SCREEN / NO TOP GAP
   ===================================================== */

#MainMenu,
header,
footer,
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    display: none !important;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
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
            #f7fbfe 45%,
            #eef5f9 100%
        ) !important;

    color: #17324d !important;
}


/* =====================================================
   REMOVE DARK GRID
   ===================================================== */

.stApp::before {
    display: none !important;
}


/* =====================================================
   COMPACT SPACING
   ===================================================== */

[data-testid="stVerticalBlock"] {
    gap: 0.00rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}


/* =====================================================
   FILTER LABELS
   ===================================================== */

[data-testid="stSelectbox"] label {
    color: #173b5c !important;

    font-size: 12px !important;

    font-weight: 900 !important;

    letter-spacing: .5px !important;

    margin-bottom: 3px !important;

    padding-left: 7px !important;
}


/* =====================================================
   SELECT BOX
   ===================================================== */

div[data-baseweb="select"] > div {

    height: 38px !important;

    min-height: 38px !important;

    border-radius: 7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f4f8fb 100%
        ) !important;

    border:
        1px solid #b8d5e8 !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 2px 6px rgba(22,72,110,.08) !important;
}

div[data-baseweb="select"]:hover > div {

    border-color: #2493d0 !important;

    box-shadow:
        0 3px 9px rgba(24,126,181,.15) !important;
}

div[data-baseweb="select"] * {

    color: #23445f !important;

    font-size: 11px !important;
}

div[data-baseweb="select"] svg {

    fill: #176da0 !important;
}


/* =====================================================
   TEXT INPUT
   ===================================================== */

div[data-testid="stTextInput"] input {

    height: 40px !important;

    min-height: 40px !important;

    border-radius: 7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f5f9fc
        ) !important;

    border:
        1px solid #b7d2e5 !important;

    color: #173b57 !important;

    font-size: 11px !important;

    box-shadow:
        inset 0 1px 2px rgba(0,0,0,.03),
        0 2px 6px rgba(22,72,110,.07) !important;
}

div[data-testid="stTextInput"] input:focus {

    border-color: #168fe0 !important;

    box-shadow:
        0 0 0 1px #168fe0,
        0 3px 10px rgba(22,143,224,.12) !important;
}

div[data-testid="stTextInput"] input::placeholder {

    color: #71869a !important;
}


/* =====================================================
   ALL BUTTONS
   ===================================================== */

div.stButton > button {

    height: 36px !important;

    min-height: 36px !important;

    border-radius: 7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #edf5fa 100%
        ) !important;

    border:
        1px solid #a9cde4 !important;

    color: #14578a !important;

    font-size: 12px !important;

    font-weight: 900 !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 2px 6px rgba(22,72,110,.10) !important;

    transition:
        all .18s ease !important;
}

div.stButton > button:hover {

    border-color: #168fe0 !important;

    color: #ffffff !important;

    background:
        linear-gradient(
            180deg,
            #168fe0,
            #0864a4
        ) !important;

    transform:
        translateY(-1px);

    box-shadow:
        0 5px 12px rgba(13,116,181,.22),
        inset 0 1px 0 rgba(255,255,255,.25) !important;
}

div.stButton > button:active {

    transform:
        translateY(1px);
}


/* =====================================================
   KPI CARDS
   ===================================================== */

.kpi-card {

    position: relative;

    height: 125px;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f7fbfd 62%,
            #edf5f9 100%
        );

    border:
        1px solid #c5dce9;

    border-top:
        3px solid #159ee4;

    border-radius: 9px;

    padding: 17px 18px;

    box-shadow:

        0 4px 12px
        rgba(28,78,110,.12),

        0 1px 2px
        rgba(28,78,110,.08),

        inset 0 1px 0
        rgba(255,255,255,.95);

    transition:
        transform .18s ease,
        box-shadow .18s ease;
}

.kpi-card:hover {

    transform:
        translateY(-2px);

    box-shadow:

        0 8px 20px
        rgba(28,78,110,.17),

        0 2px 5px
        rgba(28,78,110,.08),

        inset 0 1px 0
        rgba(255,255,255,1);
}

.kpi-card.completed {

    border-top-color:
        #18a957;
}

.kpi-card.ongoing {

    border-top-color:
        #f59d13;
}


/* =====================================================
   KPI ICON
   ===================================================== */

.kpi-icon {

    position: absolute;

    left: 23px;

    top: 24px;

    width: 60px;

    height: 60px;

    border-radius: 10px;

    display: flex;

    align-items: center;

    justify-content: center;

    color: #ffffff;

    font-size: 28px;

    background:
        linear-gradient(
            145deg,
            #39b8f4 0%,
            #0878c3 65%,
            #075e99 100%
        );

    border:
        1px solid #0c8ed2;

    box-shadow:

        0 5px 10px
        rgba(7,107,167,.24),

        inset 0 1px 0
        rgba(255,255,255,.35);
}

.kpi-card.completed .kpi-icon {

    background:
        linear-gradient(
            145deg,
            #36c978 0%,
            #149c53 65%,
            #08773c 100%
        );

    border-color:
        #19a85a;

    box-shadow:
        0 5px 10px
        rgba(12,133,67,.22),

        inset 0 1px 0
        rgba(255,255,255,.35);
}

.kpi-card.ongoing .kpi-icon {

    background:
        linear-gradient(
            145deg,
            #ffc34d 0%,
            #f49a0b 65%,
            #d87900 100%
        );

    border-color:
        #ee9705;

    box-shadow:
        0 5px 10px
        rgba(211,126,0,.22),

        inset 0 1px 0
        rgba(255,255,255,.35);
}


/* =====================================================
   KPI CONTENT
   ===================================================== */

.kpi-content {

    margin-left: 82px;
}

.kpi-label {

    color:
        #008bd0;

    font-size:
        16px;

    font-weight:
        950;

    letter-spacing:
        .3px;
}

.kpi-card.completed .kpi-label {

    color:
        #11984e;
}

.kpi-card.ongoing .kpi-label {

    color:
        #e88900;
}

.kpi-value {

    font-size:
        43px;

    line-height:
        1;

    font-weight:
        950;

    margin-top:
        7px;

    color:
        #173b5a;
}

.kpi-description {

    color:
        #5c7181;

    font-size:
        12px;

    margin-top:
        7px;
}


/* =====================================================
   KPI PATTERN
   ===================================================== */

.kpi-pattern {

    position: absolute;

    right: 18px;

    bottom: 17px;

    width: 120px;

    height: 58px;

    opacity: .30;

    background:
        repeating-linear-gradient(
            90deg,
            #52b9ed 0 8px,
            transparent 8px 14px
        );

    transform:
        skewY(-7deg);
}

.kpi-card.completed .kpi-pattern {

    background:
        repeating-linear-gradient(
            90deg,
            #42bd7a 0 8px,
            transparent 8px 14px
        );
}

.kpi-card.ongoing .kpi-pattern {

    background:
        repeating-linear-gradient(
            90deg,
            #f6bb59 0 8px,
            transparent 8px 14px
        );
}


/* =====================================================
   KPI ARROW
   ===================================================== */

.kpi-arrow {

    position: absolute;

    right: 13px;

    bottom: 12px;

    width: 29px;

    height: 29px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    color:
        #087bc1;

    border:
        1px solid #75b9dd;

    background:
        #ffffff;

    font-size:
        17px;

    box-shadow:
        0 2px 5px rgba(17,92,135,.12);
}


/* =====================================================
   PT REGISTER
   ===================================================== */

.register-wrap {

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f4f9fc
        );

    border:
        1px solid #c5dce9;

    border-radius:
        8px 8px 0 0;

    overflow:
        hidden;

    box-shadow:
        0 4px 12px
        rgba(28,78,110,.10);
}

.register-title {

    height:
        51px;

    display:
        flex;

    align-items:
        center;

    padding:
        0 20px;

    color:
        #163b5b;

    font-size:
        19px;

    font-weight:
        950;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #eef6fa
        );

    border-bottom:
        2px solid #158fd0;

    text-shadow:
        none;
}

.register-icon {

    margin-right:
        10px;

    color:
        #087fc3;
}


/* =====================================================
   TABLE HEADER
   ===================================================== */

.table-head {

    min-height:
        42px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            180deg,
            #1679bd 0%,
            #075896 100%
        );

    color:
        #ffffff;

    border-right:
        1px solid #7fb8d8;

    border-top:
        1px solid #3b9bd0;

    border-bottom:
        1px solid #064e85;

    font-size:
        14px;

    font-weight:
        950;

    text-align:
        center;

    padding:
        4px;

    text-shadow:
        0 1px 2px rgba(0,0,0,.25);

    box-shadow:
        inset 0 1px 0
        rgba(255,255,255,.18);
}


/* =====================================================
   TABLE CELLS
   ===================================================== */

.table-cell {

    min-height:
        42px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f7fafc
        );

    border-right:
        1px solid #d7e4ec;

    border-bottom:
        1px solid #d7e4ec;

    color:
        #213c55;

    font-size:
        11px;

    text-align:
        center;

    padding:
        4px;

    word-break:
        break-word;

    text-shadow:
        none;
}

.table-cell.alt {

    background:
        linear-gradient(
            180deg,
            #f5f9fb,
            #edf4f8
        );
}

.table-cell.left {

    justify-content:
        flex-start;

    text-align:
        left;
}


/* =====================================================
   STATUS
   ===================================================== */

.status-pill {

    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    min-width:
        106px;

    padding:
        4px 10px;

    border-radius:
        6px;

    font-size:
        10px;

    font-weight:
        950;

    background:
        #f5f8fa;
}


/* COMPLETED */

.status-completed {

    background:
        #ecfaf2;

    border:
        1px solid #8bd5aa;

    color:
        #108b49;

    box-shadow:
        inset 0 1px 3px
        rgba(16,139,73,.06),

        0 1px 3px
        rgba(16,139,73,.08);
}


/* ONGOING */

.status-ongoing {

    background:
        #fff7e8;

    border:
        1px solid #f3c66e;

    color:
        #d88300;

    box-shadow:
        inset 0 1px 3px
        rgba(216,131,0,.06),

        0 1px 3px
        rgba(216,131,0,.08);
}


/* =====================================================
   RECORD BAR
   ===================================================== */

.record-bar {

    height:
        39px;

    display:
        flex;

    align-items:
        center;

    padding:
        0 14px;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f1f6f9
        );

    color:
        #526b7d;

    font-size:
        11px;

    font-weight:
        800;

    border-top:
        1px solid #d4e2eb;

    border-bottom:
        1px solid #d4e2eb;

    box-shadow:
        inset 0 1px 0
        rgba(255,255,255,.9);
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {

    height:
        34px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    color:
        #587084;

    background:
        linear-gradient(
            180deg,
            #f8fbfd,
            #eaf2f6
        );

    font-size:
        11px;

    font-weight:
        800;

    border-top:
        1px solid #c8dce8;

    box-shadow:
        0 -2px 8px
        rgba(0,0,0,.06);
}


/* =====================================================
   STREAMLIT DOWNLOAD BUTTON
   ===================================================== */

div.stDownloadButton > button {

    border-radius:
        7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f1f7fa
        ) !important;

    border:
        1px solid #b8d5e7 !important;

    color:
        #116aa5 !important;

    box-shadow:
        0 2px 6px
        rgba(25,83,118,.10) !important;
}


/* =====================================================
   INFO / CAPTION
   ===================================================== */

div[data-testid="stAlert"] {

    border-radius:
        7px !important;

    box-shadow:
        0 2px 7px
        rgba(20,70,100,.08) !important;
}


/* =====================================================
   SCROLLBAR
   ===================================================== */

::-webkit-scrollbar {

    width:
        8px;

    height:
        8px;
}

::-webkit-scrollbar-track {

    background:
        #eef4f7;
}

::-webkit-scrollbar-thumb {

    background:
        #a9c9dc;

    border-radius:
        10px;
}

::-webkit-scrollbar-thumb:hover {

    background:
        #6ea9c8;
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

    background:
        #f4f9fc;
}

.header {

    position: relative;

    width: 100%;
    height: 145px;

    overflow: hidden;

    display: flex;

    align-items: center;
    justify-content: center;

    background:

        radial-gradient(
            ellipse at center,
            rgba(55,160,218,.24) 0%,
            rgba(223,242,252,.82) 45%,
            rgba(244,250,253,.98) 100%
        ),

        linear-gradient(
            180deg,
            #edf8fd 0%,
            #dceff8 100%
        );

    border-top:
        2px solid #0b91d1;

    border-bottom:
        3px solid #1487c2;

    box-shadow:
        0 4px 12px
        rgba(21,92,130,.18);
}


/* TECH DOTS */

.header::before {

    content: "";

    position: absolute;

    inset: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(0,122,190,.17) 1.2px,
            transparent 1.5px
        );

    background-size:
        15px 15px;

    opacity:
        .65;
}


/* SIDE INDUSTRIAL BLUE ANGLES */

.header::after {

    content: "";

    position: absolute;

    inset: 0;

    background:

        linear-gradient(
            135deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        ),

        linear-gradient(
            315deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        );
}


/* =====================================================
   INDUSTRIAL SVG
   ===================================================== */

.industrial {

    position: absolute;

    left: 0;
    right: 0;

    bottom: 0;

    width: 100%;
    height: 145px;

    opacity:
        .38;

    z-index:
        1;
}

.industrial .steel {

    fill:
        #a8c9da;

    stroke:
        #5791af;

    stroke-width:
        1.5;
}

.industrial .light {

    fill:
        none;

    stroke:
        #2e8bb9;

    stroke-width:
        1.2;

    opacity:
        .70;
}

.industrial .window {

    fill:
        #2787b5;

    opacity:
        .65;
}

.hex {

    fill:
        none;

    stroke:
        #278abd;

    stroke-width:
        1;

    opacity:
        .28;
}


/* =====================================================
   HEADER CONTENT
   ===================================================== */

.content {

    position:
        relative;

    z-index:
        8;

    width:
        100%;

    height:
        100%;

    display:
        flex;

    flex-direction:
        column;

    align-items:
        center;

    justify-content:
        center;

    text-align:
        center;
}


/* =====================================================
   PSM DASHBOARD
   ===================================================== */

.title {

    color:
        #153e68;

    font-size:
        24px;

    font-weight:
        950;

    letter-spacing:
        5px;

    line-height:
        1;

    margin-bottom:
        5px;

    text-shadow:
        0 1px 1px
        rgba(255,255,255,.9);
}


/* =====================================================
   PILLAR PT
   ===================================================== */

.pillar {

    position:
        relative;

    width:
        560px;

    height:
        66px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:

        linear-gradient(
            180deg,
            #176ca5 0%,
            #07518b 55%,
            #063e70 100%
        );

    border:
        1px solid #0877ba;

    border-radius:
        14px;

    color:
        #ffd21a;

    font-size:
        42px;

    font-weight:
        950;

    letter-spacing:
        1px;

    box-shadow:

        0 7px 16px
        rgba(11,83,130,.25),

        inset 0 1px 0
        rgba(255,255,255,.28),

        inset 0 -5px 12px
        rgba(0,35,75,.16);
}

.pillar::before,
.pillar::after {

    position:
        absolute;

    top:
        50%;

    transform:
        translateY(-50%);

    color:
        #51c5ff;

    font-size:
        21px;

    font-weight:
        950;

    letter-spacing:
        -5px;

    text-shadow:
        0 1px 5px
        rgba(0,100,160,.5);
}

.pillar::before {

    content:
        "◀◀";

    left:
        17px;
}

.pillar::after {

    content:
        "▶▶";

    right:
        17px;
}


/* =====================================================
   SUBTITLE
   ===================================================== */

.subtitle {

    margin-top:
        7px;

    height:
        25px;

    min-width:
        700px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    padding:
        4px 30px;

    background:

        linear-gradient(
            90deg,
            #075b8e,
            #1188c4,
            #075b8e
        );

    border:
        1px solid #078fd2;

    border-radius:
        7px;

    color:
        #ffffff;

    font-size:
        10px;

    font-weight:
        900;

    letter-spacing:
        1.8px;

    box-shadow:

        0 4px 9px
        rgba(10,93,140,.20),

        inset 0 1px 0
        rgba(255,255,255,.25);
}


/* =====================================================
   TOP BLUE ENERGY LINE
   ===================================================== */

.top-line {

    position:
        absolute;

    top:
        0;

    left:
        24%;

    width:
        52%;

    height:
        3px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00a9ff 18%,
            #ffffff 50%,
            #00a9ff 82%,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,169,255,.55);
}


/* =====================================================
   ANIMATED BOTTOM SCAN
   ===================================================== */

.scan {

    position:
        absolute;

    z-index:
        12;

    bottom:
        0;

    left:
        -16%;

    width:
        16%;

    height:
        4px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00b5ff,
            #ffffff,
            #00b5ff,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,181,255,.55);

    animation:
        scanline 3s linear infinite;
}

@keyframes scanline {

    0% {
        left:
            -16%;
    }

    100% {
        left:
            100%;
    }
}


/* =====================================================
   CORNER BLUE LIGHTS
   ===================================================== */

.corner-light {

    position:
        absolute;

    z-index:
        10;

    width:
        110px;

    height:
        3px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00baff,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,186,255,.55);
}

.corner-left {

    left:
        7%;

    top:
        7px;
}

.corner-right {

    right:
        7%;

    top:
        7px;
}

</style>
</head>

<body>

<div class="header">

    <div class="top-line"></div>

    <div class="corner-light corner-left"></div>

    <div class="corner-light corner-right"></div>


    <svg class="industrial"
         viewBox="0 0 1672 145"
         preserveAspectRatio="none"
         aria-hidden="true">


        <!-- LEFT TOWER -->

        <g>

            <rect class="steel"
                  x="85"
                  y="24"
                  width="34"
                  height="116"
                  rx="4"/>

            <rect class="steel"
                  x="91"
                  y="9"
                  width="22"
                  height="18"/>

            <rect class="steel"
                  x="96"
                  y="0"
                  width="12"
                  height="12"/>

            <path class="light"
                  d="M102 0 L102 140
                     M87 55 L117 55
                     M87 78 L117 78
                     M87 103 L117 103"/>

            <circle class="window"
                    cx="102"
                    cy="43"
                    r="3"/>

            <circle class="window"
                    cx="102"
                    cy="67"
                    r="3"/>

            <circle class="window"
                    cx="102"
                    cy="91"
                    r="3"/>

        </g>


        <!-- LEFT STACK -->

        <g>

            <rect class="steel"
                  x="150"
                  y="52"
                  width="17"
                  height="88"/>

            <rect class="steel"
                  x="146"
                  y="48"
                  width="25"
                  height="8"/>

            <path class="light"
                  d="M158 52 L158 140"/>

        </g>


        <!-- LEFT PIPE NETWORK -->

        <g class="light">

            <path d="M55 113 H245 V85 H320"/>

            <path d="M120 125 H260 V105 H355"/>

            <path d="M180 96 H285 V65 H340"/>

            <path d="M215 130 V70 H280"/>

        </g>


        <!-- LEFT VESSEL -->

        <g>

            <rect class="steel"
                  x="260"
                  y="64"
                  width="58"
                  height="76"
                  rx="26"/>

            <path class="light"
                  d="M260 82 H318
                     M260 107 H318"/>

            <circle class="window"
                    cx="289"
                    cy="95"
                    r="4"/>

        </g>


        <!-- RIGHT TOWER -->

        <g>

            <rect class="steel"
                  x="1512"
                  y="25"
                  width="36"
                  height="115"
                  rx="4"/>

            <rect class="steel"
                  x="1518"
                  y="9"
                  width="24"
                  height="18"/>

            <rect class="steel"
                  x="1523"
                  y="0"
                  width="14"
                  height="12"/>

            <path class="light"
                  d="M1530 0 L1530 140
                     M1514 54 L1546 54
                     M1514 79 L1546 79
                     M1514 103 L1546 103"/>

            <circle class="window"
                    cx="1530"
                    cy="42"
                    r="3"/>

            <circle class="window"
                    cx="1530"
                    cy="66"
                    r="3"/>

            <circle class="window"
                    cx="1530"
                    cy="90"
                    r="3"/>

        </g>


        <!-- RIGHT STACK -->

        <g>

            <rect class="steel"
                  x="1450"
                  y="54"
                  width="18"
                  height="86"/>

            <rect class="steel"
                  x="1446"
                  y="49"
                  width="26"
                  height="8"/>

            <path class="light"
                  d="M1459 54 L1459 140"/>

        </g>


        <!-- RIGHT PIPE NETWORK -->

        <g class="light">

            <path d="M1620 112 H1425 V85 H1350"/>

            <path d="M1575 125 H1410 V104 H1330"/>

            <path d="M1500 95 H1390 V65 H1335"/>

            <path d="M1465 130 V70 H1390"/>

        </g>


        <!-- RIGHT VESSEL -->

        <g>

            <rect class="steel"
                  x="1350"
                  y="64"
                  width="58"
                  height="76"
                  rx="26"/>

            <path class="light"
                  d="M1350 82 H1408
                     M1350 107 H1408"/>

            <circle class="window"
                    cx="1379"
                    cy="95"
                    r="4"/>

        </g>


        <!-- CENTRAL LOW PIPE -->

        <g class="light">

            <path d="M0 137 H1672"/>

            <path d="M0 126 H420 V116 H650"/>

            <path d="M1672 126 H1250 V116 H1020"/>

        </g>


        <!-- HEXAGONAL TECHNICAL MOTIFS -->

        <g class="hex">

            <path d="M250 25 l18 -11 l18 11 v22 l-18 11 l-18-11 z"/>

            <path d="M282 54 l18 -11 l18 11 v22 l-18 11 l-18-11 z"/>

            <path d="M1335 25 l18 -11 l18 11 v22 l-18 11 l-18-11 z"/>

            <path d="M1370 54 l18 -11 l18 11 v22 l-18 11 l-18-11 z"/>

        </g>

    </svg>


    <div class="content">

        <div class="title">
            PSM DASHBOARD
        </div>

        <div class="pillar">
            PILLAR: PT
        </div>

        <div class="subtitle">
            PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        </div>

    </div>

    <div class="scan"></div>

</div>

</body>
</html>
"""

components.html(
    header_html,
    height=170,
    scrolling=False
)


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
        "<div style='height:22px;'></div>",
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
        "<div style='height:22px;'></div>",
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
        index=0,
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
        use_container_width=True
    ):

        st.session_state.status_filter = "All"

        st.session_state.page_number = 1

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
        "▣",
        "TOTAL PT",
        total_pt,
        "Total identified PT",
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

    <div class="kpi-arrow">
        ›
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

        <span class="register-icon">
            ▣
        </span>

        PT REGISTER

    </div>

</div>
"""
)


# =========================================================
# REGISTER TOOLBAR
# =========================================================

search_col, all_col, completed_col, ongoing_col, refresh_col, upload_col = st.columns(
    [4.2, .8, 1.15, 1.0, 1.15, 1.35],
    gap="small"
)


with search_col:

    search_text = st.text_input(
        "Search",
        placeholder=(
            "Search PT No., Name of PT, "
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


with ongoing_col:

    ongoing_button = st.button(
        "Ongoing",
        use_container_width=True
    )


with refresh_col:

    if st.button(
        "↻ Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


with upload_col:

    if st.button(
        "⬆ Upload Document",
        use_container_width=True
    ):

        st.session_state.upload_pt_no = ""

        st.session_state.open_upload_dialog = True

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
        "PT No.",
        "Department",
        "Name of PT",
        "Product",
        "Process",
        "Location",
        "Remarks"
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

PAGE_SIZE = 10

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
# =========================================================

table_widths = [
    .45,
    .85,
    1.25,
    1.65,
    .95,
    1.15,
    1.05
]

table_headers = [
    "Sr No",
    "PT No.",
    "Department",
    "Name of PT",
    "Status",
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


    # =====================================================
    # DATA CELLS
    # =====================================================

    row_values = [

        row["Sr No"],
        row["PT No."],
        row["Department"],
        row["Name of PT"]

    ]

    row_positions = [
        0,
        1,
        2,
        3
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


    # =====================================================
    # STATUS
    # =====================================================

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


    # =====================================================
    # UPLOAD
    # =====================================================

    with row_columns[5]:

        if st.button(
            "📤 Upload",
            key=(
                f"upload_{page_number}_"
                f"{row_number}_"
                f"{row['PT No.']}"
            ),
            use_container_width=True
        ):

            st.session_state.upload_pt_no = str(
                row["PT No."]
            )

            st.session_state.open_upload_dialog = True

            st.rerun()


    # =====================================================
    # VIEW
    # =====================================================

    with row_columns[6]:

        if st.button(
            "📄 View",
            key=(
                f"view_{page_number}_"
                f"{row_number}_"
                f"{row['PT No.']}"
            ),
            use_container_width=True
        ):

            st.session_state.view_pt_no = str(
                row["PT No."]
            )

            st.rerun()


# =========================================================
# VIEW DOCUMENT
# =========================================================

view_pt = st.session_state.get(
    "view_pt_no",
    ""
)

if view_pt:

    matching_files = []

    if os.path.exists(
        DOCUMENT_FOLDER
    ):

        for filename in os.listdir(
            DOCUMENT_FOLDER
        ):

            if filename.startswith(
                f"{view_pt}_"
            ):

                matching_files.append(
                    filename
                )


    if matching_files:

        st.info(
            f"Documents available for {view_pt}: "
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
            f"No uploaded document found for {view_pt}."
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

    {page_number}
    &nbsp; / &nbsp;
    {total_pages}

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
# UPLOAD DIALOG
# =========================================================

if st.session_state.get(
    "open_upload_dialog",
    False
):

    @st.dialog("📤 Upload PT Document")
    def upload_document_dialog():

        pt_no = st.session_state.get(
            "upload_pt_no",
            ""
        )

        if pt_no:

            st.write(
                f"PT No.: **{pt_no}**"
            )

        else:

            st.info(
                "Enter the PT number for this document."
            )

            pt_no = st.text_input(
                "PT No.",
                key="dialog_pt_no"
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

            if not pt_no:

                st.warning(
                    "Please enter PT No. first."
                )

            else:

                file_name = (
                    f"{pt_no}_"
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
                    f"Document uploaded successfully for {pt_no}"
                )

                st.session_state.open_upload_dialog = False

                st.session_state.upload_pt_no = ""

                st.rerun()


    upload_document_dialog()


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
<div class="footer">

    🛡 &nbsp;
    © 2026 Process Safety Management Dashboard
    |
    Pillar: PT

</div>
"""
)

