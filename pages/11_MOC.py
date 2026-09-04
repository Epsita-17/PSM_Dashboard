import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import html
from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PSM Dashboard - MOC",
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

if "month_selector" not in st.session_state:
    st.session_state.month_selector = "All Months"


# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=100000,
    key="moc_auto_refresh"
)


# =========================================================
# GOOGLE SHEET - MOC
# =========================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

MOC_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet=MOC"
)


@st.cache_data(ttl=60)
def get_moc_data():

    try:

        data = pd.read_csv(MOC_CSV_URL)

        # -------------------------------------------------
        # CLEAN COLUMN NAMES
        # -------------------------------------------------

        data.columns = (
            data.columns
            .astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.strip()
        )

        # -------------------------------------------------
        # CLEAN TEXT DATA
        # -------------------------------------------------

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
            f"Unable to load Google Sheet MOC: {exc}"
        )

        return pd.DataFrame()


df = get_moc_data()


# =========================================================
# DOCUMENT STORAGE
# =========================================================

DOCUMENT_FOLDER = "moc_documents"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# =========================================================
# REQUIRED MOC COLUMNS
# =========================================================
required_columns = [
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
    "Remarks"
]

STATUS_COLUMN = "Status"
# =========================================================
# CHECK DATA
# =========================================================

if df.empty:

    st.error(
        "No data found in Google Sheet: MOC."
    )

    st.stop()


missing_columns = [

    column
    for column in required_columns
    if column not in df.columns

]

if missing_columns:

    st.error(
        "Some required columns are missing from Google Sheet: MOC."
    )

    st.write("Missing columns:")
    st.write(missing_columns)

    st.write("Columns found in MOC:")
    st.write(df.columns.tolist())

    st.stop()


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
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
   BACKGROUND
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
    gap: 0rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}


/* =====================================================
   SELECT LABEL
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

    background: #ffffff !important;

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
   MONTH + DEPARTMENT POSITION
   ===================================================== */

div[data-testid="stColumn"]:has(.month-filter-anchor)
div[data-testid="stSelectbox"],
div[data-testid="column"]:has(.month-filter-anchor)
div[data-testid="stSelectbox"] {

    transform:
        translateY(-3px) !important;
}

div[data-testid="stColumn"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"],
div[data-testid="column"]:has(.department-filter-anchor)
div[data-testid="stSelectbox"] {

    transform:
        translateY(-3px) !important;
}


/* =====================================================
   TEXT INPUT
   ===================================================== */

div[data-testid="stTextInput"] input {

    height: 40px !important;

    min-height: 40px !important;

    border-radius: 6px !important;

    background: #ffffff !important;

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
   BUTTONS
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

    padding: 15px 10px;

    box-shadow:
        0 4px 10px rgba(6,48,91,.12),
        0 1px 2px rgba(6,48,91,.08),
        inset 0 1px 0 rgba(255,255,255,.98);
}

.kpi-card.completed {
    border-top-color: #19a657;
}

.kpi-card.ongoing {
    border-top-color: #f18d05;
}

.kpi-card.closure {
    border-top-color: #176fc1;
}


/* =====================================================
   KPI CONTENT
   ===================================================== */

.kpi-content {

    width: 100% !important;

    height: 100% !important;

    display: flex !important;

    flex-direction: column !important;

    align-items: center !important;

    justify-content: center !important;

    text-align: center !important;
}

.kpi-label {

    color: #092d5c;

    font-size: 14px;

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

.kpi-card.closure .kpi-label {
    color: #092d5c;
}

.kpi-value {

    font-size: 38px;

    line-height: 1;

    font-weight: 900;

    margin-top: 5px;

    color: #0a4e91;

    text-align: center;
}

.kpi-value.green {
    color: #159447 !important;
}

.kpi-value.orange {
    color: #f0a000 !important;
}

.kpi-value.blue {
    color: #0a4e91 !important;
}

.kpi-description {

    color: #304d6d;

    font-size: 10px;

    font-weight: 700;

    margin-top: 5px;

    text-align: center;
}


/* =====================================================
   REGISTER
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
}

.register-icon {

    margin-right: 9px;

    color: #ffffff;
}


/* =====================================================
   MOC TABLE
   ===================================================== */

.pt-table {

    width: 100%;

    overflow: hidden;

    border:
        1px solid #d5e0ea;

    background: #ffffff;
}

.pt-row {

    display: grid;

    grid-template-columns:
        0.80fr
        1.15fr
        0.95fr
        1.20fr
        3.00fr
        0.85fr
        1.00fr;
}

.pt-header {

    min-height: 52px;

    background:
        linear-gradient(
            180deg,
            #205796 0%,
            #174b87 100%
        );
}

.pt-cell {

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 7px 8px;

    border-right:
        1px solid #d5e0ea;

    border-bottom:
        1px solid #d5e0ea;

    color: #243b57;

    font-size: 11px;

    font-weight: 600;

    text-align: center;

    line-height: 1.2;

    word-break: break-word;
}

.pt-header .pt-cell {

    color: #ffffff;

    font-weight: 900;

    font-size: 11px;
}

.pt-left {

    justify-content: flex-start;

    text-align: left;
}

.pt-alt .pt-cell {

    background: #f5f8fb;
}


/* =====================================================
   STATUS
   ===================================================== */

.status-completed {

    color: #198754;

    font-weight: 900;
}

.status-ongoing {

    color: #e08a00;

    font-weight: 900;
}

.status-normal {

    color: #243b57;

    font-weight: 900;
}


/* =====================================================
   DOCUMENT LINK
   ===================================================== */

.action-view {

    color: #174b87;

    font-weight: 900;

    text-decoration: none;

    cursor: pointer;
}

.action-view:hover {

    color: #0b6f9f;

    text-decoration: underline;
}


/* =====================================================
   RECORD BAR
   ===================================================== */

.record-text {

    height: 38px;

    display: flex;

    align-items: center;

    padding-left: 12px;

    color: #5d7085;

    font-size: 11px;

    font-weight: 600;
}


/* =====================================================
   PAGINATION CURRENT PAGE
   ===================================================== */

.current-page {

    height: 36px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #174b87;

    color: #ffffff;

    border-radius: 6px;

    font-size: 12px;

    font-weight: 900;
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

    font-size: 11px;

    font-weight: 800;

    border-top:
        2px solid #176fc1;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# DARK INDUSTRIAL 3D HEADER
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
        min(75%, 1000px);

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
            Management of Change (MOC)
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

def reset_moc_filters():

    st.session_state.status_filter = "All"

    st.session_state.page_number = 1

    st.session_state.department_selector = "All Departments"

    st.session_state.month_selector = "All Months"


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

    request_dates_all = pd.to_datetime(
        df["Request Date"],
        errors="coerce"
    )

    month_periods = sorted(
        request_dates_all
        .dropna()
        .dt.to_period("M")
        .unique(),
        reverse=True
    )

    month_options = [
        "All Months"
    ]

    month_options += [
        period.strftime("%B %Y")
        for period in month_periods
    ]

    selected_month = st.selectbox(
        "Month",
        month_options,
        key="month_selector"
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
        (department_values != "")
        &
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

    st.button(
        "↻ Reset Filters",
        use_container_width=True,
        key="reset_moc_filters_button",
        on_click=reset_moc_filters
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# ---------------------------------------------------------
# MONTH FILTER
# ---------------------------------------------------------

if selected_month != "All Months":

    request_dates = pd.to_datetime(
        filtered_df["Request Date"],
        errors="coerce"
    )

    filtered_df = filtered_df[
        request_dates.dt.strftime("%B %Y")
        == selected_month
    ]


# ---------------------------------------------------------
# DEPARTMENT FILTER
# ---------------------------------------------------------

if selected_department != "All Departments":

    filtered_df = filtered_df[
        filtered_df["Department"]
        .fillna("")
        .astype(str)
        .str.strip()
        ==
        selected_department
    ]


# ---------------------------------------------------------
# STATUS CLEANING
# ---------------------------------------------------------

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

total_moc = len(filtered_df)


open_moc = int(
    (
        filtered_df[STATUS_COLUMN]
        .isin(
            [
                "open",
                "ongoing",
                "in progress"
            ]
        )
    ).sum()
)


closed_moc = int(
    (
        filtered_df[STATUS_COLUMN]
        .isin(
            [
                "closed",
                "completed"
            ]
        )
    ).sum()
)


moc_closure_percentage = (

    closed_moc / total_moc * 100

    if total_moc

    else 0

)


# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(
    4,
    gap="small"
)


cards = [

    (
        "TOTAL MOC",
        total_moc,
        "",
        "blue",
        "total"
    ),

    (
        "OPEN MOC",
        open_moc,
        "",
        "orange",
        "ongoing"
    ),

    (
        "CLOSED MOC",
        closed_moc,
        "",
        "green",
        "completed"
    ),

    (
        "MOC CLOSURE %",
        f"{moc_closure_percentage:.1f}%",
        "",
        "green",
        "closure"
    )

]


for column, card in zip(
    [k1, k2, k3, k4],
    cards
):

    label, value, description, color, extra = card

    with column:

        st.html(
            f"""
<div class="kpi-card {extra}">

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

</div>
"""
        )


# =========================================================
# MOC REGISTER TITLE
# =========================================================

st.html(
    """
<div class="register-wrap">

    <div class="register-title">

        <span class="register-icon">
            ▣
        </span>

        MOC REGISTER

    </div>

</div>
"""
)


# =========================================================
# MOC REGISTER TOOLBAR
# =========================================================

search_col, all_col, closed_col, open_col, refresh_col = st.columns(
    [2.8, 0.55, 0.85, 0.75, 1.05],
    gap="small"
)


# =========================================================
# SEARCH
# =========================================================

with search_col:

    search_text = st.text_input(

        "Search",

        placeholder=(
            "Search MOC No., Department, "
            "Section, Requestor, Description..."
        ),

        label_visibility="collapsed",

        key="moc_search"

    )


# =========================================================
# ALL
# =========================================================

with all_col:

    if st.button(
        "All",
        use_container_width=True,
        key="moc_all"
    ):

        st.session_state.status_filter = "All"

        st.session_state.page_number = 1

        st.rerun()


# =========================================================
# CLOSED
# =========================================================

with closed_col:

    if st.button(
        "Closed",
        use_container_width=True,
        key="moc_closed"
    ):

        st.session_state.status_filter = "Closed"

        st.session_state.page_number = 1

        st.rerun()


# =========================================================
# OPEN
# =========================================================

with open_col:

    if st.button(
        "Open",
        use_container_width=True,
        key="moc_open"
    ):

        st.session_state.status_filter = "Open"

        st.session_state.page_number = 1

        st.rerun()


# =========================================================
# REFRESH
# =========================================================

with refresh_col:

    if st.button(
        "↻ Refresh Data",
        use_container_width=True,
        key="moc_refresh"
    ):

        st.cache_data.clear()

        st.rerun()


# =========================================================
# SEARCH + STATUS FILTER
# =========================================================

display_df = filtered_df.copy()


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

if search_text.strip():

    q = search_text.strip().lower()

    search_mask = (

        display_df["MOC No"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

        |

        display_df["Department"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

        |

        display_df["Section"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

        |

        display_df["Requestor Name"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

        |

        display_df["Description of Change"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

        |

        display_df["Status"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            q,
            regex=False
        )

    )

    display_df = display_df[search_mask]


# ---------------------------------------------------------
# STATUS FILTER
# ---------------------------------------------------------

if st.session_state.status_filter != "All":

    if st.session_state.status_filter == "Open":

        display_df = display_df[
            display_df[STATUS_COLUMN]
            .isin(
                [
                    "open",
                    "ongoing",
                    "in progress"
                ]
            )
        ]

    elif st.session_state.status_filter == "Closed":

        display_df = display_df[
            display_df[STATUS_COLUMN]
            .isin(
                [
                    "closed",
                    "completed"
                ]
            )
        ]


# =========================================================
# PAGINATION
# =========================================================

ROWS_PER_PAGE = 5

total_entries = len(display_df)

total_pages = max(
    1,
    (
        total_entries
        + ROWS_PER_PAGE
        - 1
    )
    //
    ROWS_PER_PAGE
)


if st.session_state.page_number > total_pages:

    st.session_state.page_number = total_pages


page_number = st.session_state.page_number

start_index = (
    page_number - 1
) * ROWS_PER_PAGE

end_index = (
    start_index
    + ROWS_PER_PAGE
)

page_df = display_df.iloc[
    start_index:end_index
].copy()


# =========================================================
# MOC TABLE HTML
# =========================================================

rows_html = """

<div class="pt-table">

    <div class="pt-row pt-header">

        <div class="pt-cell">
            MOC No.
        </div>

        <div class="pt-cell">
            Department
        </div>

        <div class="pt-cell">
            Section
        </div>

        <div class="pt-cell">
            Requestor Name
        </div>

        <div class="pt-cell">
            Description of Change
        </div>

        <div class="pt-cell">
            Status
        </div>

        <div class="pt-cell">
            MOC Document
        </div>

    </div>

"""


# =========================================================
# BUILD TABLE ROWS
# =========================================================

for row_no, (_, row) in enumerate(
    page_df.iterrows()
):

    alt = (
        " pt-alt"
        if row_no % 2
        else ""
    )


    moc_no = html.escape(
        str(row["MOC No"]).strip()
    )


    department = html.escape(
        str(row["Department"]).strip()
    )


    section = html.escape(
        str(row["Section"]).strip()
    )


    requestor = html.escape(
        str(row["Requestor Name"]).strip()
    )


    description = html.escape(
        str(row["Description of Change"]).strip()
    )


    status = str(
        row["Status"]
    ).strip()


    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    if status.lower() in [
        "closed",
        "completed"
    ]:

        status_html = (
            '<span class="status-completed">'
            'CLOSED'
            '</span>'
        )

    elif status.lower() in [
        "open",
        "ongoing",
        "in progress"
    ]:

        status_html = (
            '<span class="status-ongoing">'
            'OPEN'
            '</span>'
        )

    else:

        status_html = (
            '<span class="status-normal">'
            +
            html.escape(
                status or "—"
            )
            +
            '</span>'
        )


    # -----------------------------------------------------
    # DOCUMENT LINK
    # -----------------------------------------------------

    document_link = str(
        row["Attach MOC Softcopy Link"]
    ).strip()


    if (

        document_link

        and

        document_link.lower()
        not in [
            "nan",
            "none",
            ""
        ]

    ):

        safe_link = html.escape(
            document_link,
            quote=True
        )

        document_html = f"""

        <a
            href="{safe_link}"
            target="_blank"
            rel="noopener noreferrer"
            class="action-view"
        >
            ◉ View
        </a>

        """

    else:

        document_html = """

        <span style="
            color:#9aa8b5;
            font-weight:700;
        ">
            —
        </span>

        """


    # -----------------------------------------------------
    # ROW
    # -----------------------------------------------------

    rows_html += f"""

    <div class="pt-row{alt}">

        <div class="pt-cell pt-left">
            {moc_no}
        </div>

        <div class="pt-cell pt-left">
            {department}
        </div>

        <div class="pt-cell pt-left">
            {section}
        </div>

        <div class="pt-cell pt-left">
            {requestor}
        </div>

        <div class="pt-cell pt-left">
            {description}
        </div>

        <div class="pt-cell">
            {status_html}
        </div>

        <div class="pt-cell">
            {document_html}
        </div>

    </div>

    """


rows_html += """

</div>

"""


# =========================================================
# DISPLAY TABLE
# =========================================================

st.html(
    f"""
{rows_html}
"""
)

# =========================================================
# RECORD BAR + PAGINATION
# FIXED HORIZONTAL LAYOUT
# =========================================================

shown_from = start_index + 1 if total_entries else 0
shown_to = min(end_index, total_entries)


# ---------------------------------------------------------
# MAIN PAGINATION ROW
# ---------------------------------------------------------

record_col, pagination_col = st.columns(
    [4.8, 3.2],
    gap="small"
)


# =========================================================
# RECORD COUNT - LEFT SIDE
# =========================================================

with record_col:

    st.markdown(
        f"""
        <div class="record-count-box">
            Showing {shown_from} to {shown_to} of {total_entries} entries
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGINATION - RIGHT SIDE
# =========================================================

with pagination_col:

    pg1, pg2, pg3, pg4, pg5, pg6, pg7 = st.columns(
        [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
        gap="small"
    )


    # -----------------------------------------------------
    # FIRST PAGE
    # -----------------------------------------------------

    with pg1:

        if st.button(
            "«",
            key="page_first",
            use_container_width=True
        ):

            st.session_state.page_number = 1

            st.rerun()


    # -----------------------------------------------------
    # PREVIOUS PAGE
    # -----------------------------------------------------

    with pg2:

        if st.button(
            "‹",
            key="page_prev",
            use_container_width=True
        ):

            st.session_state.page_number = max(
                1,
                page_number - 1
            )

            st.rerun()


    # -----------------------------------------------------
    # CURRENT PAGE
    # -----------------------------------------------------

    with pg3:

        st.markdown(
            f"""
            <div class="current-page">
                {page_number}
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # NEXT PAGE
    # -----------------------------------------------------

    with pg4:

        if st.button(
            "›",
            key="page_next",
            use_container_width=True
        ):

            st.session_state.page_number = min(
                total_pages,
                page_number + 1
            )

            st.rerun()


    # -----------------------------------------------------
    # LAST PAGE
    # -----------------------------------------------------

    with pg5:

        if st.button(
            "»",
            key="page_last",
            use_container_width=True
        ):

            st.session_state.page_number = total_pages

            st.rerun()
# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        &nbsp; | &nbsp;
        MANAGEMENT OF CHANGE
    </div>
    """,
    unsafe_allow_html=True
)

