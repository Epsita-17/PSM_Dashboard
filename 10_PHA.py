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
   STEEL BLUE INDUSTRIAL BACKGROUND
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            #dfe8df 0%,
            #e7eee7 25%,
            #d5e0d5 55%,
            #cbd8cb 100%
        ) !important;

    color: #24332b !important;
}


/* =====================================================
   SUBTLE INDUSTRIAL GRID
   ===================================================== */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        linear-gradient(
            rgba(70, 105, 78, 0.045) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(70, 105, 78, 0.045) 1px,
            transparent 1px
        );

    background-size: 32px 32px;
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
   FILTERS
   ===================================================== */

[data-testid="stSelectbox"] label {
    color: #56665b !important;
    font-size: 12px !important;
    font-weight: 900 !important;
    letter-spacing: .5px !important;
    margin-bottom: 2px !important;
    padding-left: 8px !important;
}

div[data-baseweb="select"] > div {
    height: 38px !important;
    min-height: 38px !important;
    border-radius: 6px !important;

    background:
        linear-gradient(
            180deg,
            #fbfcf8,
            #eef3eb
        ) !important;

    border: 1px solid #aebfac !important;

    box-shadow:
        inset 0 0 8px rgba(0,130,190,.10) !important;
}

div[data-baseweb="select"] * {
    color: #26362c !important;
    font-size: 11px !important;
}

div[data-baseweb="select"] svg {
    fill: #52665a !important;
}

div[data-testid="stTextInput"] input {
    height: 40px !important;
    min-height: 40px !important;
    border-radius: 6px !important;

    background:
        linear-gradient(
            180deg,
            #fbfcf8,
            #eef3eb
        ) !important;

    border: 1px solid #aabbaa !important;
    color: #24332b !important;
    font-size: 11px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #7a897f !important;
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
            #ffffff,
            #edf2ea
        ) !important;

    border: 1px solid #9daf9f !important;

    color: #52665a !important;

    font-size: 12px !important;
    font-weight: 900 !important;

    box-shadow:
        inset 0 0 10px rgba(0,123,211,.08),
        0 1px 5px rgba(0,0,0,.22) !important;
}

div.stButton > button:hover {
    border-color: #13a8ff !important;
    color: #ffffff !important;

    background:
        linear-gradient(
            180deg,
            #e5eee3,
            #d9e5d8
        ) !important;

    box-shadow:
        0 0 12px rgba(13,163,255,.32),
        inset 0 0 12px rgba(13,163,255,.08) !important;
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
            135deg,
            #f7faf5 0%,
            #e8efe6 100%
        );

    border: 1px solid #aebead;
    border-top: 2px solid #7da482;

    border-radius: 8px;

    padding: 17px 18px;

    box-shadow:
        0 4px 12px rgba(0,0,0,.28),
        inset 0 0 18px rgba(0,124,211,.045);
}

.kpi-card.completed {
    border-top-color: #5aa477;
}

.kpi-card.ongoing {
    border-top-color: #d99a35;
}

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
            180deg,
            #17618d,
            #0c3e5d
        );

    border: 1px solid #00a8ff;

    box-shadow:
        0 0 12px rgba(0,161,255,.23),
        inset 0 0 14px rgba(0,161,255,.10);
}

.kpi-card.completed .kpi-icon {
    background:
        linear-gradient(
            180deg,
            #6fb48a,
            #e4f2e7
        );

    border-color: #5aa477;

    box-shadow:
        0 0 12px rgba(25,237,103,.22);
}

.kpi-card.ongoing .kpi-icon {
    background:
        linear-gradient(
            180deg,
            #d8aa58,
            #f8ecd2
        );

    border-color: #d99a35;

    box-shadow:
        0 0 12px rgba(255,159,0,.23);
}

.kpi-content {
    margin-left: 82px;
}

.kpi-label {
    color: #00d0ff;
    font-size: 16px;
    font-weight: 950;
    letter-spacing: .3px;
}

.kpi-card.completed .kpi-label {
    color: #4d9869;
}

.kpi-card.ongoing .kpi-label {
    color: #bd7d16;
}

.kpi-value {
    font-size: 43px;
    line-height: 1;
    font-weight: 950;
    margin-top: 7px;
    color: #24342b;
}

.kpi-description {
    color: #68766d;
    font-size: 12px;
    margin-top: 7px;
}

.kpi-pattern {
    position: absolute;
    right: 18px;
    bottom: 17px;

    width: 120px;
    height: 58px;

    opacity: .24;

    background:
        repeating-linear-gradient(
            90deg,
            #9fbea2 0 8px,
            transparent 8px 14px
        );

    transform: skewY(-7deg);
}

.kpi-card.completed .kpi-pattern {
    background:
        repeating-linear-gradient(
            90deg,
            #8fc6a0 0 8px,
            transparent 8px 14px
        );
}

.kpi-card.ongoing .kpi-pattern {
    background:
        repeating-linear-gradient(
            90deg,
            #e3b66b 0 8px,
            transparent 8px 14px
        );
}

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

    color: #14a9ff;

    border: 1px solid #a5b6a7;

    background: #edf3ea;

    font-size: 17px;
}


/* =====================================================
   PT REGISTER
   ===================================================== */

.register-wrap {
    background:
        linear-gradient(
            180deg,
            #f5f8f2,
            #e8efe7
        );

    border: 1px solid #adbead;

    border-radius: 8px 8px 0 0;

    overflow: hidden;

    box-shadow:
        0 4px 14px rgba(0,0,0,.28);
}

.register-title {
    height: 51px;

    display: flex;
    align-items: center;

    padding: 0 20px;

    color: #24342b;

    font-size: 19px;
    font-weight: 950;

    background:
        linear-gradient(
            90deg,
            #e0e9df,
            #dce8dc,
            #e0e9df
        );

    border-bottom:
        1px solid #8aa88f;

    text-shadow:
        0 1px 5px rgba(0,0,0,.6);
}

.register-icon {
    margin-right: 10px;
    color: #34483a;
}


/* =====================================================
   TABLE HEADER
   ===================================================== */

.table-head {
    min-height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            180deg,
            #dce8dc,
            #cfdccc
        );

    color: #2d4434;

    border-right:
        1px solid #a9bca9;

    border-top:
        1px solid #9fb39f;

    border-bottom:
        1px solid #9fb39f;

    font-size: 14px;
    font-weight: 950;

    text-align: center;

    padding: 4px;

    text-shadow:
        0 1px 3px rgba(0,0,0,.6);
}


/* =====================================================
   TABLE CELLS
   PRODUCT / PROCESS / LOCATION ARE NOT DISPLAYED
   ===================================================== */

.table-cell {
    min-height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            90deg,
            #f7faf5,
            #edf3ea
        );

    border-right:
        1px solid #c1cec0;

    border-bottom:
        1px solid #cbd7ca;

    color: #3c5042;

    font-size: 11px;

    text-align: center;

    padding: 4px;

    word-break: break-word;

    text-shadow:
        0 1px 2px rgba(0,0,0,.55);
}

.table-cell.alt {
    background:
        linear-gradient(
            90deg,
            #f0f5ed,
            #e5ede3
        );
}

.table-cell.left {
    justify-content: flex-start;
    text-align: left;
}


/* =====================================================
   STATUS
   ===================================================== */

.status-pill {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 106px;

    padding: 4px 10px;

    border-radius: 6px;

    font-size: 10px;
    font-weight: 950;

    background: #e8eee6;
}

.status-completed {
    background: #e2f1e5;

    border:
        1px solid #73aa82;

    color: #43865b;

    box-shadow:
        inset 0 0 8px rgba(35,237,102,.08);
}

.status-ongoing {
    background: #fff0d1;

    border:
        1px solid #d6a34a;

    color: #b87510;

    box-shadow:
        inset 0 0 8px rgba(255,163,0,.08);
}


/* =====================================================
   RECORD BAR
   ===================================================== */

.record-bar {
    height: 39px;

    display: flex;
    align-items: center;

    padding: 0 14px;

    background: #e8efe6;

    color: #68786d;

    font-size: 11px;
    font-weight: 800;

    border-top:
        1px solid #b7c7b5;

    border-bottom:
        1px solid #c5d2c3;
}


/* =====================================================
   PHA RECOMENDATION - KPI STYLE BOXES
   ===================================================== */

.pha-recommendation-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    padding: 10px 0 4px 0;
}

.pha-recommendation-card {
    position: relative;
    min-height: 175px;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #f7faf5 0%,
            #e8efe6 100%
        );

    border: 1px solid #aebead;
    border-top: 3px solid #7da482;
    border-radius: 8px;

    padding: 12px 13px;

    box-shadow:
        0 4px 12px rgba(0,0,0,.25),
        inset 0 0 16px rgba(70,105,78,.04);
}

.pha-recommendation-card:hover {
    border-top-color: #d99a24;

    background:
        linear-gradient(
            135deg,
            #ffffff 0%,
            #edf3ea 100%
        );

    box-shadow:
        0 5px 15px rgba(0,0,0,.28);
}

.pha-rec-number {
    position: absolute;
    top: 10px;
    right: 11px;

    min-width: 30px;
    height: 28px;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 0 7px;

    border-radius: 6px;

    background: #dce8dc;
    border: 1px solid #9fb39f;

    color: #34483a;

    font-size: 13px;
    font-weight: 950;
}

.pha-rec-title {
    color: #648c69;

    font-size: 15px;
    font-weight: 950;

    padding-right: 42px;
    margin-bottom: 9px;

    line-height: 1.15;
}

.pha-rec-recommendation {
    min-height: 55px;

    padding: 8px 9px;
    margin-bottom: 9px;

    border-radius: 6px;

    background:
        linear-gradient(
            90deg,
            #e5ede3,
            #f7faf5
        );

    border-left: 3px solid #7da482;
    border-top: 1px solid #c1cec0;
    border-right: 1px solid #c1cec0;
    border-bottom: 1px solid #c1cec0;

    color: #24342b;

    font-size: 11px;
    font-weight: 850;

    line-height: 1.35;
}

.pha-rec-label {
    display: block;

    color: #68786d;

    font-size: 8px;
    font-weight: 950;

    text-transform: uppercase;
    letter-spacing: .35px;

    margin-bottom: 3px;
}

.pha-rec-value {
    color: #24342b;

    font-size: 10px;
    font-weight: 850;

    line-height: 1.25;

    word-break: break-word;
}

.pha-rec-details {
    display: grid;
    grid-template-columns: 1fr 1fr;

    gap: 7px;
}

.pha-rec-detail {
    min-height: 39px;

    padding: 6px 8px;

    background: #f7faf5;

    border: 1px solid #c1cec0;
    border-radius: 6px;
}

.pha-rec-status {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-height: 23px;

    padding: 3px 8px;

    border-radius: 5px;

    background: #fff0d1;
    border: 1px solid #d6a34a;

    color: #b87510;

    font-size: 9px;
    font-weight: 950;

    line-height: 1.15;
}

.pha-rec-approval {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-height: 23px;

    padding: 3px 8px;

    border-radius: 5px;

    background: #e8eee6;
    border: 1px solid #aebead;

    color: #56665b;

    font-size: 9px;
    font-weight: 950;

    line-height: 1.15;
}

.pha-recommendation-empty {
    padding: 20px;

    text-align: center;

    color: #728277;

    background: #e8efe7;

    border: 1px solid #adbead;
    border-radius: 8px;
}

/* Responsive: keep 3 boxes on normal desktop,
   reduce only on narrow screens. */
@media (max-width: 1100px) {
    .pha-recommendation-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 700px) {
    .pha-recommendation-grid {
        grid-template-columns: 1fr;
    }
}


/* =====================================================
   PHA RECOMENDATION KPI SUMMARY
   ===================================================== */

.pha-rec-summary {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    padding: 10px 0 8px 0;
}

.pha-rec-kpi {
    position: relative;
    height: 125px;
    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #f7faf5 0%,
            #e8efe6 100%
        );

    border: 1px solid #aebead;
    border-top: 2px solid #7da482;
    border-radius: 8px;

    padding: 17px 18px;

    box-shadow:
        0 4px 12px rgba(0,0,0,.28),
        inset 0 0 18px rgba(70,105,78,.045);
}

.pha-rec-kpi.total {
    border-top-color: #168bc7;
}

.pha-rec-kpi.approved,
.pha-rec-kpi.completed {
    border-top-color: #5aa477;
}

.pha-rec-kpi.rejected,
.pha-rec-kpi.overdue {
    border-top-color: #d45b5b;
}

.pha-rec-kpi.pending {
    border-top-color: #d99a35;
}

.pha-rec-kpi-icon {
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

    font-size: 27px;
    font-weight: 900;

    background:
        linear-gradient(
            180deg,
            #17618d,
            #0c3e5d
        );

    border: 1px solid #00a8ff;

    box-shadow:
        0 0 12px rgba(0,161,255,.23),
        inset 0 0 14px rgba(0,161,255,.10);
}

.pha-rec-kpi.approved .pha-rec-kpi-icon,
.pha-rec-kpi.completed .pha-rec-kpi-icon {
    background:
        linear-gradient(
            180deg,
            #6fb48a,
            #e4f2e7
        );

    border-color: #5aa477;
}

.pha-rec-kpi.rejected .pha-rec-kpi-icon,
.pha-rec-kpi.overdue .pha-rec-kpi-icon {
    background:
        linear-gradient(
            180deg,
            #d76c6c,
            #f7dddd
        );

    border-color: #d45b5b;
}

.pha-rec-kpi.pending .pha-rec-kpi-icon {
    background:
        linear-gradient(
            180deg,
            #d8aa58,
            #f8ecd2
        );

    border-color: #d99a35;
}

.pha-rec-kpi-content {
    margin-left: 82px;
}

.pha-rec-kpi-label {
    color: #168bc7;
    font-size: 16px;
    font-weight: 950;
    letter-spacing: .3px;
}

.pha-rec-kpi.approved .pha-rec-kpi-label,
.pha-rec-kpi.completed .pha-rec-kpi-label {
    color: #4d9869;
}

.pha-rec-kpi.rejected .pha-rec-kpi-label,
.pha-rec-kpi.overdue .pha-rec-kpi-label {
    color: #c34d4d;
}

.pha-rec-kpi.pending .pha-rec-kpi-label {
    color: #bd7d16;
}

.pha-rec-kpi-value {
    font-size: 43px;
    line-height: 1;
    font-weight: 950;
    margin-top: 7px;
    color: #24342b;
}

.pha-rec-kpi-description {
    color: #68766d;
    font-size: 12px;
    margin-top: 7px;
}

.pha-rec-kpi-pattern {
    position: absolute;
    right: 18px;
    bottom: 17px;

    width: 120px;
    height: 58px;

    opacity: .24;

    background:
        repeating-linear-gradient(
            90deg,
            #9fbea2 0 8px,
            transparent 8px 14px
        );

    transform: skewY(-7deg);
}

.pha-rec-kpi.rejected .pha-rec-kpi-pattern,
.pha-rec-kpi.overdue .pha-rec-kpi-pattern {
    background:
        repeating-linear-gradient(
            90deg,
            #d98d8d 0 8px,
            transparent 8px 14px
        );
}

.pha-rec-kpi.pending .pha-rec-kpi-pattern {
    background:
        repeating-linear-gradient(
            90deg,
            #e3b66b 0 8px,
            transparent 8px 14px
        );
}

.pha-rec-kpi-arrow {
    position: absolute;
    right: 13px;
    bottom: 12px;

    width: 29px;
    height: 29px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    color: #14a9ff;

    border: 1px solid #a5b6a7;
    background: #edf3ea;

    font-size: 17px;
}

@media (max-width: 1100px) {
    .pha-rec-summary {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 700px) {
    .pha-rec-summary {
        grid-template-columns: 1fr;
    }
}

/* =====================================================
   PHA RECOMENDATION
   ===================================================== */

.recommendation-wrap {
    margin-top: 14px;

    background:
        linear-gradient(
            180deg,
            #f5f8f2,
            #e8efe7
        );

    border: 1px solid #adbead;

    border-radius: 8px 8px 0 0;

    overflow: hidden;

    box-shadow:
        0 4px 14px rgba(0,0,0,.28);
}

.recommendation-title {
    height: 51px;

    display: flex;
    align-items: center;

    padding: 0 20px;

    color: #24342b;

    font-size: 19px;
    font-weight: 950;

    background:
        linear-gradient(
            90deg,
            #e0e9df,
            #dce8dc,
            #e0e9df
        );

    border-bottom:
        1px solid #8aa88f;

    text-shadow:
        0 1px 5px rgba(0,0,0,.6);
}

.recommendation-icon {
    margin-right: 10px;
    color: #d99a24;
}

.recommendation-container {
    width: 100%;
    overflow-x: auto;

    border-left: 1px solid #adbead;
    border-right: 1px solid #adbead;
    border-bottom: 1px solid #adbead;
}

.recommendation-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
}

.recommendation-table th {
    background:
        linear-gradient(
            180deg,
            #dce8dc,
            #cfdccc
        );

    color: #2d4434;

    border: 1px solid #a9bca9;

    font-size: 13px;
    font-weight: 950;

    text-align: center;

    padding: 8px 6px;

    white-space: nowrap;
}

.recommendation-table td {
    background:
        linear-gradient(
            90deg,
            #f7faf5,
            #edf3ea
        );

    color: #3c5042;

    border: 1px solid #c1cec0;

    font-size: 11px;

    text-align: left;

    vertical-align: middle;

    padding: 8px 7px;

    word-break: break-word;
}

.recommendation-table tr:nth-child(even) td {
    background:
        linear-gradient(
            90deg,
            #f0f5ed,
            #e5ede3
        );
}

.recommendation-table tr:hover td {
    background: #d8e5d7;
}

.recommendation-empty {
    padding: 20px;

    text-align: center;

    color: #728277;

    font-size: 12px;

    background: #e8efe7;

    border: 1px solid #adbead;
}

.recommendation-count {
    height: 36px;

    display: flex;
    align-items: center;

    padding: 0 14px;

    color: #68786d;

    background: #e8efe6;

    font-size: 11px;
    font-weight: 800;

    border-left: 1px solid #adbead;
    border-right: 1px solid #adbead;
    border-bottom: 1px solid #adbead;
}

/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    height: 34px;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #627268;

    background:
        linear-gradient(
            180deg,
            #e1eae0,
            #cfdccd
        );

    font-size: 11px;
    font-weight: 800;

    border-top:
        1px solid #91a992;

    box-shadow:
        0 -2px 10px rgba(0,0,0,.20);
}


/* =========================================================
   STEEL BLUE INDUSTRIAL THEME OVERRIDE
   No background image - color only
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 50% 0%,
            #F8FBFD 0%,
            #EEF3F7 32%,
            #E8EEF3 68%,
            #DDE6ED 100%) !important;
    color: #263B4A !important;
}

.stApp::before {
    background-image:
        linear-gradient(rgba(36,91,130,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(36,91,130,.035) 1px, transparent 1px) !important;
    background-size: 32px 32px !important;
}

/* Filters */
[data-testid="stSelectbox"] label {
    color: #526B7D !important;
}
div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input {
    background: linear-gradient(180deg,#FFFFFF,#E8EEF3) !important;
    border: 1px solid #A8BDCC !important;
    color: #263B4A !important;
}
div[data-baseweb="select"] * {
    color: #263B4A !important;
}
div[data-baseweb="select"] svg {
    fill: #245B82 !important;
}

/* 3D buttons */
div.stButton > button {
    background: linear-gradient(180deg,#FFFFFF 0%,#F4F8FB 42%,#D8E5EE 100%) !important;
    border: 1px solid #A8BDCC !important;
    color: #163A52 !important;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,.95),
        inset 0 -3px 5px rgba(36,91,130,.10),
        0 3px 0 #8FA9BA,
        0 5px 10px rgba(22,58,82,.18) !important;
}
div.stButton > button:hover {
    background: linear-gradient(180deg,#FFFFFF,#EAF4FA,#C9DCE9) !important;
    border-color: #245B82 !important;
    color: #163A52 !important;
    transform: translateY(-1px) !important;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,.98),
        inset 0 -3px 5px rgba(36,91,130,.12),
        0 4px 0 #7897AC,
        0 7px 14px rgba(36,91,130,.22) !important;
}
div.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow:
        inset 0 3px 7px rgba(22,58,82,.20),
        0 1px 0 #7897AC,
        0 2px 5px rgba(22,58,82,.18) !important;
}

/* KPI cards */
.kpi-card,
.pha-rec-kpi {
    background: linear-gradient(135deg,#FFFFFF 0%,#F8FBFD 55%,#E7EFF5 100%) !important;
    border-color: #A8BDCC !important;
    border-top-color: #245B82 !important;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,.95),
        inset 0 -5px 12px rgba(36,91,130,.05),
        0 4px 0 rgba(120,151,172,.30),
        0 8px 18px rgba(22,58,82,.16) !important;
}
.kpi-card.completed,
.pha-rec-kpi.approved,
.pha-rec-kpi.completed {
    border-top-color: #4F9A68 !important;
}
.kpi-card.ongoing,
.pha-rec-kpi.pending {
    border-top-color: #D89A2B !important;
}
.pha-rec-kpi.rejected,
.pha-rec-kpi.overdue {
    border-top-color: #D45B5B !important;
}
.kpi-value,
.pha-rec-kpi-value,
.kpi-description,
.pha-rec-kpi-description {
    color: #263B4A !important;
}
.kpi-label,
.pha-rec-kpi-label {
    color: #245B82 !important;
}

/* KPI icons */
.kpi-icon,
.pha-rec-kpi-icon {
    background: linear-gradient(180deg,#2F719D,#163A52) !important;
    border-color: #5C9CC4 !important;
    box-shadow:
        inset 0 2px 0 rgba(255,255,255,.25),
        0 5px 10px rgba(22,58,82,.25) !important;
}
.kpi-card.completed .kpi-icon,
.pha-rec-kpi.approved .pha-rec-kpi-icon,
.pha-rec-kpi.completed .pha-rec-kpi-icon {
    background: linear-gradient(180deg,#4FA66B,#247145) !important;
    border-color: #3C8D59 !important;
}
.kpi-card.ongoing .kpi-icon,
.pha-rec-kpi.pending .pha-rec-kpi-icon {
    background: linear-gradient(180deg,#F1B64D,#C47A10) !important;
    border-color: #D89A2B !important;
}
.pha-rec-kpi.rejected .pha-rec-kpi-icon,
.pha-rec-kpi.overdue .pha-rec-kpi-icon {
    background: linear-gradient(180deg,#E77A7A,#B83E3E) !important;
    border-color: #D45B5B !important;
}

/* Register containers */
.register-wrap,
.recommendation-wrap {
    background: linear-gradient(180deg,#FFFFFF,#EDF3F7) !important;
    border-color: #A8BDCC !important;
    box-shadow: 0 4px 14px rgba(22,58,82,.16) !important;
}
.register-title,
.recommendation-title {
    color: #163A52 !important;
    background: linear-gradient(90deg,#E4EDF3,#D7E3EB,#E4EDF3) !important;
    border-bottom-color: #8FA9BA !important;
    text-shadow: none !important;
}
.register-icon,
.recommendation-icon {
    color: #245B82 !important;
}

/* Table */
.table-head,
.recommendation-table th {
    background: linear-gradient(180deg,#245B82 0%,#163A52 100%) !important;
    color: #FFFFFF !important;
    border-color: #8EABC0 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,.25) !important;
}
.table-cell,
.recommendation-table td {
    background: linear-gradient(90deg,#FFFFFF,#F2F7FA) !important;
    color: #263B4A !important;
    border-color: #C4D4DF !important;
    text-shadow: none !important;
}
.table-cell.alt,
.recommendation-table tr:nth-child(even) td {
    background: linear-gradient(90deg,#F0F5F8,#E7EFF4) !important;
}
.recommendation-table tr:hover td {
    background: #DDEAF2 !important;
}

/* Status */
.status-completed {
    background: #E4F2E8 !important;
    border-color: #73A882 !important;
    color: #2F7D49 !important;
}
.status-ongoing {
    background: #FFF1D7 !important;
    border-color: #D6A34A !important;
    color: #B87510 !important;
}

/* Record bars / recommendation areas */
.record-bar,
.recommendation-count {
    background: #E7EFF4 !important;
    color: #526B7D !important;
    border-color: #B8CBD8 !important;
}
.pha-recommendation-card,
.pha-rec-detail,
.pha-rec-recommendation {
    background: linear-gradient(135deg,#FFFFFF,#EEF4F8) !important;
    border-color: #B7CBD8 !important;
    color: #263B4A !important;
}
.pha-rec-title {
    color: #245B82 !important;
}
.pha-rec-recommendation {
    border-left-color: #245B82 !important;
}
.pha-rec-number {
    background: #E3EDF3 !important;
    border-color: #A8BDCC !important;
    color: #163A52 !important;
}
.pha-rec-label {
    color: #607A8D !important;
}
.pha-rec-value {
    color: #263B4A !important;
}
.pha-rec-approval {
    background: #E7EFF4 !important;
    border-color: #A8BDCC !important;
    color: #526B7D !important;
}
.pha-recommendation-empty,
.recommendation-empty {
    background: #EDF3F7 !important;
    border-color: #A8BDCC !important;
    color: #607A8D !important;
}

/* Footer */
.footer {
    color: #EAF3F8 !important;
    background: linear-gradient(180deg,#245B82,#163A52) !important;
    border-top-color: #6F94AD !important;
    box-shadow: 0 -2px 10px rgba(22,58,82,.20) !important;
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
    background: #DDE6ED;
}

.header {

    position: relative;

    width: 100%;
    height: 100px;

    overflow: hidden;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            ellipse at center,
            rgba(115, 145, 118, .40) 0%,
            rgba(225, 235, 222, .55) 45%,
            rgba(241, 246, 238, .78) 100%
        ),

        linear-gradient(
            180deg,
            #E8EEF3 0%,
            #D2DFE8 100%
        );

    border-top:
        2px solid #245B82;

    border-bottom:
        3px solid #163A52;

    box-shadow:
        0 0 18px rgba(87, 120, 91, .18);
}


/* TECH DOTS */

.header::before {

    content: "";

    position: absolute;

    inset: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(90, 125, 95, .18) 1.3px,
            transparent 1.5px
        );

    background-size:
        15px 15px;

    opacity: .55;
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
            rgba(90, 125, 95, .14) 7% 8%,
            transparent 8% 11%,
            rgba(90, 125, 95, .09) 11% 12%,
            transparent 12%
        ),

        linear-gradient(
            315deg,
            transparent 0 7%,
            rgba(90, 125, 95, .14) 7% 8%,
            transparent 8% 11%,
            rgba(90, 125, 95, .09) 11% 12%,
            transparent 12%
        );
}


/* INDUSTRIAL SVG BACKGROUND */

.industrial {

    position: absolute;

    left: 0;
    right: 0;

    bottom: 0;

    width: 100%;
    height: 100px;

    opacity: .75;

    z-index: 1;
}

.industrial .steel {
    fill: #7C91A1;
    stroke: #5F788B;
    stroke-width: 1.5;
}

.industrial .light {
    fill: none;
    stroke: #5E829D;
    stroke-width: 1.2;
    opacity: .65;
}

.industrial .window {
    fill: #789DB5;
    opacity: .75;
}

.hex {
    fill: none;
    stroke: #7895A7;
    stroke-width: 1;
    opacity: .35;
}


/* CONTENT */

.content {

    position: relative;

    z-index: 8;

    width: 100%;
    height: 100%;

    display: flex;

    flex-direction: column;

    align-items: center;
    justify-content: center;

    text-align: center;
}


/* PSM DASHBOARD */

.title {

    color: #163A52;

    font-size: 24px;

    font-weight: 950;

    letter-spacing: 5px;

    line-height: 1;

    margin-bottom: 5px;

    text-shadow:
        0 2px 7px rgba(0,0,0,.65);
}


/* PILLAR PHA */

.pillar {

    position: relative;

    width: 560px;

    height: 66px;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            180deg,
            #edf3ea 0%,
            #F0F5F8 100%
        );

    border:
        1px solid #A8BDCC;

    border-radius:
        14px;

    color: #d99a24;

    font-size: 42px;

    font-weight: 950;

    letter-spacing: 1px;

    box-shadow:

        0 0 18px
        rgba(89, 124, 94, .13),

        inset 0 0 20px
        rgba(89, 124, 94, .08);
}

.pillar::before,
.pillar::after {

    position: absolute;

    top: 50%;

    transform:
        translateY(-50%);

    color: #648c69;

    font-size: 21px;

    font-weight: 950;

    letter-spacing: -5px;

    text-shadow:
        0 0 8px rgba(0,170,255,.45);
}

.pillar::before {

    content: "◀◀";

    left: 17px;
}

.pillar::after {

    content: "▶▶";

    right: 17px;
}


/* SUBTITLE */

.subtitle {

    margin-top: 7px;

    height: 25px;

    min-width: 700px;

    display: flex;

    align-items: center;
    justify-content: center;

    padding: 4px 30px;

    background:
        linear-gradient(
            90deg,
            #6f9675,
            #245B82,
            #6f9675
        );

    border:
        1px solid #A8BDCC;

    border-radius:
        7px;

    color: #ffffff;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 1.8px;

    box-shadow:
        0 0 8px rgba(89, 124, 94, .10);
}


/* TOP BLUE ENERGY LINE */

.top-line {

    position: absolute;

    top: 0;

    left: 24%;

    width: 52%;

    height: 3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #7da482 18%,
            #ffffff 50%,
            #7da482 82%,
            transparent
        );

    box-shadow:
        0 0 10px #7da482,
        0 0 22px rgba(0,169,255,.7);
}


/* ANIMATED BOTTOM SCAN */

.scan {

    position: absolute;

    z-index: 12;

    bottom: 0;

    left: -16%;

    width: 16%;

    height: 4px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #82a988,
            #ffffff,
            #82a988,
            transparent
        );

    box-shadow:
        0 0 10px #82a988,
        0 0 24px rgba(0,181,255,.75);

    animation:
        scanline 3s linear infinite;
}

@keyframes scanline {

    0% {
        left: -16%;
    }

    100% {
        left: 100%;
    }
}


/* CORNER BLUE LIGHTS */

.corner-light {

    position: absolute;

    z-index: 10;

    width: 110px;

    height: 3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #87ad8c,
            transparent
        );

    box-shadow:
        0 0 10px #87ad8c;
}

.corner-left {
    left: 7%;
    top: 7px;
}

.corner-right {
    right: 7%;
    top: 7px;
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
                  x="85" y="24"
                  width="34" height="116"
                  rx="4"/>

            <rect class="steel"
                  x="91" y="9"
                  width="22" height="18"/>

            <rect class="steel"
                  x="96" y="0"
                  width="12" height="12"/>

            <path class="light"
                  d="M102 0 L102 140
                     M87 55 L117 55
                     M87 78 L117 78
                     M87 103 L117 103"/>

            <circle class="window"
                    cx="102" cy="43" r="3"/>
            <circle class="window"
                    cx="102" cy="67" r="3"/>
            <circle class="window"
                    cx="102" cy="91" r="3"/>
        </g>

        <!-- LEFT STACK -->
        <g>
            <rect class="steel"
                  x="150" y="52"
                  width="17" height="88"/>

            <rect class="steel"
                  x="146" y="48"
                  width="25" height="8"/>

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
                  x="260" y="64"
                  width="58" height="76"
                  rx="26"/>

            <path class="light"
                  d="M260 82 H318
                     M260 107 H318"/>

            <circle class="window"
                    cx="289" cy="95" r="4"/>
        </g>

        <!-- RIGHT TOWER -->
        <g>
            <rect class="steel"
                  x="1512" y="25"
                  width="36" height="115"
                  rx="4"/>

            <rect class="steel"
                  x="1518" y="9"
                  width="24" height="18"/>

            <rect class="steel"
                  x="1523" y="0"
                  width="14" height="12"/>

            <path class="light"
                  d="M1530 0 L1530 140
                     M1514 54 L1546 54
                     M1514 79 L1546 79
                     M1514 103 L1546 103"/>

            <circle class="window"
                    cx="1530" cy="42" r="3"/>
            <circle class="window"
                    cx="1530" cy="66" r="3"/>
            <circle class="window"
                    cx="1530" cy="90" r="3"/>
        </g>

        <!-- RIGHT STACK -->
        <g>
            <rect class="steel"
                  x="1450" y="54"
                  width="18" height="86"/>

            <rect class="steel"
                  x="1446" y="49"
                  width="26" height="8"/>

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
                  x="1350" y="64"
                  width="58" height="76"
                  rx="26"/>

            <path class="light"
                  d="M1350 82 H1408
                     M1350 107 H1408"/>

            <circle class="window"
                    cx="1379" cy="95" r="4"/>
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



        <div class="pillar">
            PILLAR: PHA
        </div>

    </div>

    <div class="scan"></div>

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

# ---------------------------------------------------------
# DEPARTMENT
# ---------------------------------------------------------

with filter_department:
    # Same vertical spacing
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

# ---------------------------------------------------------
# RESET FILTER
# ---------------------------------------------------------

with filter_reset:
    # Same vertical spacing
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
# ---------------------------------------------------------

recommendation_kpis = [

    (
        "▣",
        "TOTAL RECOMMENDATION",
        total_recommendations,
        "Total recommendations",
        "total"
    ),

    (
        "✓",
        "APPROVED",
        approved_recommendations,
        "Approved recommendations",
        "approved"
    ),

    (
        "✕",
        "REJECTED",
        rejected_recommendations,
        "Rejected recommendations",
        "rejected"
    ),

    (
        "!",
        "OVERDUE",
        overdue_recommendations,
        "Overdue recommendations",
        "overdue"
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
        "pending"
    )
]

for row_start in range(
        0,
        len(recommendation_kpis),
        3
):

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
            st.html(
                f"""
<div class="pha-rec-kpi {card_class}">

    <div class="pha-rec-kpi-icon">
        {icon}
    </div>

    <div class="pha-rec-kpi-content">

        <div class="pha-rec-kpi-label">
            {label}
        </div>

        <div class="pha-rec-kpi-value">
            {value}
        </div>

        <div class="pha-rec-kpi-description">
            {description}
        </div>

    </div>

    <div class="pha-rec-kpi-pattern"></div>

    <div class="pha-rec-kpi-arrow">
        ›
    </div>

</div>
"""
            )

# =========================================================
# RECOMENDATION REGISTER
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

# =========================================================
# RECOMENDATION REGISTER - SELECTED HEADERS
# =========================================================

recommendation_register_columns = [
    "Department",
    "PHA No.",
    "PHA Description",
    "Recomendation",
    "Target Date",
    "Overdue/Pending/Completion",
    "Remarks"
]

# =========================================================
# RECOMENDATION REGISTER DATA
# =========================================================

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
        "Missing headers:"
    )

    st.write(
        missing_register_columns
    )

    st.write(
        "Available Google Sheet headers:"
    )

    st.write(
        pha_recommendation_df.columns.tolist()
    )

else:

    recommendation_register_df = (
        pha_recommendation_df[
            recommendation_register_columns
        ]
        .copy()
    )

    recommendation_register_html = """
<div class="recommendation-container">

<table class="recommendation-table">

<thead>
<tr>
"""

    # -----------------------------------------------------
    # HEADERS
    # -----------------------------------------------------

    for column in recommendation_register_columns:
        recommendation_register_html += (
            f"<th>{column}</th>"
        )

    recommendation_register_html += """
</tr>
</thead>

<tbody>
"""

    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    for _, row in recommendation_register_df.iterrows():

        recommendation_register_html += "<tr>"

        for column in recommendation_register_columns:

            value = row[column]

            if pd.isna(value):

                value = ""

            else:

                value = str(
                    value
                ).strip()

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

<div class="recommendation-count">
"""

    recommendation_register_html += (
        f"Showing "
        f"{len(recommendation_register_df)} "
        f"recommendation entries"
    )

    recommendation_register_html += """
</div>
"""

    st.html(
        recommendation_register_html
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

search_col, all_col, completed_col, ongoing_col, refresh_col, upload_col = st.columns(
    [4.2, .8, 1.15, 1.0, 1.15, 1.35],
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
        st.session_state.upload_pha_no = ""
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

