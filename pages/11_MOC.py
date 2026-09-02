import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import html

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Management of Change (MOC) Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEET_NAME = "MOC"

GOOGLE_SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}/gviz/tq"
    f"?tqx=out:csv&sheet={SHEET_NAME}"
)

# ============================================================
# COMPLETE CSS
# ============================================================

st.html(
    """
<style>

/* ============================================================
   LIGHT PREMIUM / 3D GLASS THEME
   ONLY THEME MODIFIED — FUNCTIONALITY UNCHANGED
   ============================================================ */

:root {
    --navy: #18284F;
    --blue: #287BE0;
    --purple: #7659E8;
    --green: #32B878;
    --red: #E83D68;
    --orange: #F29A2E;
    --cyan: #20B9BD;
    --text: #172B4D;
    --muted: #667085;
    --border: #E7EAF2;
    --surface: #FFFFFF;
    --background: #F5F7FB;
}

/* ---------- Overall Background ---------- */

html,
body,
.stApp {
    margin: 0 !important;
    padding: 0 !important;

    background:
        radial-gradient(
            circle at 12% 4%,
            rgba(54, 129, 255, 0.24),
            transparent 28%
        ),
        radial-gradient(
            circle at 88% 12%,
            rgba(106, 74, 226, 0.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #071C4F 0%,
            #0A2D70 45%,
            #152E76 72%,
            #211C68 100%
        ) !important;

    color: #172B4D;
}

/* ---------- Hide Streamlit UI ---------- */

[data-testid="stHeader"],
[data-testid="stToolbar"],
header,
footer,
#MainMenu {
    display: none !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
    background: transparent !important;
}

.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0px 0px 0px 0px !important;
    margin: 0 !important;
}

/* ---------- Streamlit Spacing ---------- */

[data-testid="stVerticalBlock"] {
    gap: 0.38rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}

/* ============================================================
   HEADER
   ============================================================ */

.dashboard-header {
    width: 100%;
    height: 70px;

    display: flex;
    align-items: center;

    padding: 0 17px;
    box-sizing: border-box;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.98),
            rgba(249,250,255,0.96)
        );

    border: 1px solid rgba(220,225,238,0.95);

    border-radius: 15px;

    box-shadow:
        0 10px 28px rgba(2, 18, 55, 0.15),
        0 2px 5px rgba(56, 72, 120, 0.04);

    position: relative;
    overflow: hidden;
}

.dashboard-header::after {
    content: "";
    position: absolute;

    width: 220px;
    height: 120px;

    right: 12%;
    top: -95px;

    background:
        radial-gradient(
            circle,
            rgba(102,133,255,0.12),
            transparent 70%
        );

    pointer-events: none;
}

.dashboard-logo {
    width: 46px;
    height: 46px;

    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-right: 13px;

    color: #FFFFFF;
    font-size: 24px;

    background:
        linear-gradient(
            145deg,
            #4E9AFF 0%,
            #287BE0 48%,
            #7659E8 100%
        );

    box-shadow:
        0 8px 16px rgba(55,111,225,0.24),
        inset 1px 1px 2px rgba(255,255,255,0.55),
        inset -2px -2px 4px rgba(48,79,170,0.20);
}

.dashboard-title {
    color: var(--navy);

    font-size: 25px;
    font-weight: 750;

    letter-spacing: -0.45px;
}

/* ============================================================
   KPI CARDS
   SAME CARD PATTERN AS LOWER CHART / REGISTER CARDS
   ============================================================ */

.kpi-card {
    height: 145px;

    position: relative;

    padding: 17px 20px;

    box-sizing: border-box;

    overflow: hidden;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.99),
            rgba(247,250,255,0.98)
        );

    border: 1px solid #DCE4EF;

    box-shadow:
        0 10px 28px rgba(2, 18, 55, 0.16),
        0 2px 7px rgba(2, 18, 55, 0.08);

    backdrop-filter: blur(8px);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 14px 32px rgba(2, 18, 55, 0.20),
        0 3px 8px rgba(2, 18, 55, 0.10);
}

/* Same subtle top/right glow used by the chart cards */
.kpi-card::before {
    content: "";

    position: absolute;

    width: 180px;
    height: 140px;

    right: -58px;
    top: -64px;

    border-radius: 50%;

    pointer-events: none;
}

.kpi-blue::before {
    background:
        radial-gradient(
            circle,
            rgba(40,123,224,0.14),
            transparent 68%
        );
}

.kpi-green::before {
    background:
        radial-gradient(
            circle,
            rgba(50,184,120,0.14),
            transparent 68%
        );
}

.kpi-red::before {
    background:
        radial-gradient(
            circle,
            rgba(232,61,104,0.13),
            transparent 68%
        );
}

.kpi-orange::before {
    background:
        radial-gradient(
            circle,
            rgba(242,154,46,0.15),
            transparent 68%
        );
}

.kpi-title {
    color: #233A61;

    font-size: 15px;
    font-weight: 700;

    position: relative;
    z-index: 2;
}

.kpi-number {
    margin-top: 9px;

    font-size: 34px;
    line-height: 1;

    font-weight: 800;

    letter-spacing: -0.7px;

    position: relative;
    z-index: 2;
}

.kpi-blue .kpi-number {
    color: #287BE0;
}

.kpi-green .kpi-number {
    color: #18A968;
}

.kpi-red .kpi-number {
    color: #E83D68;
}

.kpi-orange .kpi-number {
    color: #EA841A;
}

/* Glossy icon matching the lower-card action icon style */
.kpi-icon {
    position: absolute;

    right: 19px;
    top: 18px;

    width: 62px;
    height: 62px;

    border-radius: 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 28px;

    z-index: 2;

    box-shadow:
        0 10px 20px rgba(28,52,100,0.13),
        inset 2px 2px 4px rgba(255,255,255,0.80),
        inset -2px -2px 5px rgba(40,70,120,0.08);
}

.kpi-blue .kpi-icon {
    color: #287BE0;
    background:
        linear-gradient(
            145deg,
            #EEF6FF,
            #D5E8FF
        );
}

.kpi-green .kpi-icon {
    color: #18A968;
    background:
        linear-gradient(
            145deg,
            #EEFFF5,
            #D8F5E5
        );
}

.kpi-red .kpi-icon {
    color: #E83D68;
    background:
        linear-gradient(
            145deg,
            #FFF1F5,
            #FFE0E9
        );
}

.kpi-orange .kpi-icon {
    color: #EA841A;
    background:
        linear-gradient(
            145deg,
            #FFF8EA,
            #FFEBCB
        );
}

/* Bottom progress line = same visual language as the reference */
.kpi-line {
    position: absolute;

    left: 20px;
    right: 20px;
    bottom: 16px;

    width: auto;
    height: 6px;

    border-radius: 10px;

    z-index: 2;
}

.kpi-blue .kpi-line {
    background:
        linear-gradient(
            90deg,
            #287BE0 0%,
            #287BE0 72%,
            #DCE8F7 72%,
            #DCE8F7 100%
        );
}

.kpi-green .kpi-line {
    background:
        linear-gradient(
            90deg,
            #32B878 0%,
            #32B878 48%,
            #DDEEE5 48%,
            #DDEEE5 100%
        );
}

.kpi-red .kpi-line {
    background:
        linear-gradient(
            90deg,
            #E83D68 0%,
            #E83D68 48%,
            #F2DDE4 48%,
            #F2DDE4 100%
        );
}

.kpi-orange .kpi-line {
    background:
        linear-gradient(
            90deg,
            #F29A2E 0%,
            #F29A2E 35%,
            #F2E2C7 35%,
            #F2E2C7 100%
        );
}

/* ============================================================
   CHART CARDS
   ============================================================ */

.chart-card {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.99),
            rgba(247,250,255,0.98)
        );

    border: 1px solid #DCE4EF;

    border-radius: 15px;

    overflow: hidden;

    box-shadow:
        0 10px 28px rgba(2, 18, 55, 0.16),
        0 2px 7px rgba(2, 18, 55, 0.08);
}

.chart-title {
    height: 43px;

    display: flex;
    align-items: center;

    padding: 0 14px;

    color: #1C3155;

    font-size: 14px;
    font-weight: 700;

    letter-spacing: -0.1px;
}

.chart-icon {
    color: #287BE0;
    margin-right: 7px;
}

/* ============================================================
   MOC REGISTER
   ============================================================ */

.register-card {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.99),
            rgba(247,250,255,0.98)
        );

    border: 1px solid #DCE4EF;

    border-radius: 15px;

    overflow: hidden;

    margin-top: 5px;

    box-shadow:
        0 10px 28px rgba(2, 18, 55, 0.16),
        0 2px 7px rgba(2, 18, 55, 0.08);
}

.register-header {
    height: 48px;

    display: flex;
    align-items: center;

    padding: 0 15px;

    color: #1C3155;

    font-size: 17px;
    font-weight: 750;

    border-bottom: 1px solid #E6EAF1;
}

.register-icon {
    color: #287BE0;
    margin-right: 8px;
}

/* ============================================================
   INPUTS
   ============================================================ */

div[data-testid="stTextInput"] {
    margin: 0 !important;
}

div[data-testid="stTextInput"] input {
    height: 37px !important;
    min-height: 37px !important;

    border-radius: 9px !important;

    border: 1px solid #DDE3ED !important;

    background: rgba(255,255,255,0.96) !important;

    color: #344054 !important;

    font-size: 11px !important;

    box-shadow:
        inset 0 1px 2px rgba(25,40,75,0.025),
        0 2px 5px rgba(25,40,75,0.025);
}

div[data-testid="stTextInput"] input:focus {
    border-color: #8CB7F4 !important;

    box-shadow:
        0 0 0 3px rgba(40,123,224,0.08) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #98A2B3 !important;
}

/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-testid="stSelectbox"] {
    margin: 0 !important;
}

div[data-testid="stSelectbox"] > div > div {
    min-height: 37px !important;
    height: 37px !important;

    border-radius: 9px !important;

    border: 1px solid #DDE3ED !important;

    background: rgba(255,255,255,0.96) !important;

    box-shadow:
        0 2px 5px rgba(25,40,75,0.025);
}

div[data-testid="stSelectbox"] * {
    font-size: 11px !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton {
    margin: 0 !important;
}

.stButton > button {
    height: 37px !important;
    min-height: 37px !important;

    border-radius: 9px !important;

    border: 1px solid #DDE3ED !important;

    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F7F9FD
        ) !important;

    color: #344054 !important;

    font-size: 11px !important;
    font-weight: 650 !important;

    box-shadow:
        0 3px 8px rgba(45,62,110,0.055),
        inset 1px 1px 1px rgba(255,255,255,0.8);

    transition: all 0.18s ease;
}

.stButton > button:hover {
    border-color: #9CBDF0 !important;

    color: #287BE0 !important;

    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F0F6FF
        ) !important;

    transform: translateY(-1px);
}

/* ============================================================
   TABLE
   ============================================================ */

.moc-table {
    width: 100%;

    border-collapse: collapse;

    table-layout: fixed;

    background: #FFFFFF;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    box-shadow:
        0 3px 12px rgba(45,62,110,0.025);
}

.moc-table th {
    background:
        linear-gradient(
            180deg,
            #F3F7FD,
            #EDF3FB
        );

    color: #29415F;

    padding: 9px 6px;

    border: 1px solid #DEE5EF;

    font-size: 10px;

    font-weight: 700;

    text-align: center;
}

.moc-table td {
    background: #FFFFFF;

    color: #344054;

    padding: 8px 6px;

    border: 1px solid #E7EBF1;

    font-size: 10px;

    text-align: center;

    vertical-align: middle;

    height: 37px;
}

.moc-table tr:nth-child(even) td {
    background: #FBFCFF;
}

.moc-table tr:hover td {
    background: #F6F9FF;
}

.moc-table td.left {
    text-align: left;
}

.moc-table td.description {
    text-align: left;
    line-height: 1.25;
}

/* ============================================================
   STATUS PILLS
   ============================================================ */

.status-pill {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 62px;

    padding: 4px 10px;

    border-radius: 15px;

    font-size: 9px;
    font-weight: 650;

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.65);
}

.status-open {
    color: #D97706;
    background: #FFF3E2;
}

.status-closed {
    color: #16834A;
    background: #EAF8EF;
}

.status-other {
    color: #667085;
    background: #F2F4F7;
}

/* ============================================================
   TYPE PILLS
   ============================================================ */

.type-pill {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 72px;

    padding: 4px 8px;

    border-radius: 15px;

    font-size: 9px;
    font-weight: 650;

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.7);
}

.type-permanent {
    color: #16834A;
    background: #EAF8EF;
}

.type-temporary {
    color: #D97706;
    background: #FFF2DF;
}

.type-emergency {
    color: #D93657;
    background: #FDECEF;
}

.type-other {
    color: #287BE0;
    background: #EDF5FF;
}

/* ============================================================
   CATEGORY PILLS
   ============================================================ */

.category-pill {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 70px;

    padding: 4px 8px;

    border-radius: 15px;

    font-size: 9px;
    font-weight: 650;

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.7);
}

.cat-technology {
    color: #287BE0;
    background: #EDF5FF;
}

.cat-personnel {
    color: #7254C9;
    background: #F1EDFF;
}

.cat-facility {
    color: #159A9C;
    background: #E9F9FA;
}

.cat-other {
    color: #667085;
    background: #F2F4F7;
}

/* ============================================================
   VIEW BUTTON
   ============================================================ */

.view-link {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 58px;

    padding: 4px 8px;

    border: 1px solid #DCE4EE;

    border-radius: 7px;

    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F5F8FD
        );

    color: #287BE0 !important;

    text-decoration: none !important;

    font-size: 9px;
    font-weight: 650;

    box-shadow:
        0 2px 5px rgba(45,62,110,0.04);
}

.view-link:hover {
    background: #F0F6FF;

    border-color: #9BBFF0;
}

/* ============================================================
   PAGE INFO
   ============================================================ */

.page-info {
    color: #667085;

    font-size: 10px;

    padding-top: 7px;
}

/* ============================================================
   HIDE LABELS
   ============================================================ */

label[data-testid="stWidgetLabel"] {
    display: none !important;
}


/* ============================================================
   STREAMLIT CHART CARD SURFACE
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F7FAFF
        ) !important;

    border: 1px solid #DCE4EF !important;

    border-radius: 15px !important;

    box-shadow:
        0 10px 28px rgba(2,18,55,0.15),
        0 2px 7px rgba(2,18,55,0.07) !important;

    overflow: hidden !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
}

</style>
"""
)
# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=60)
def load_moc_data():

    try:

        data = pd.read_csv(
            GOOGLE_SHEET_URL
        )

        # ----------------------------------------------------
        # CLEAN HEADERS
        # ----------------------------------------------------

        data.columns = (
            data.columns
            .astype(str)
            .str.replace(
                "\xa0",
                " ",
                regex=False
            )
            .str.replace(
                "\n",
                " ",
                regex=False
            )
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
            .str.strip()
        )

        # ----------------------------------------------------
        # CLEAN CELL VALUES
        # ----------------------------------------------------

        for col in data.columns:

            if data[col].dtype == "object":

                data[col] = (
                    data[col]
                    .fillna("")
                    .astype(str)
                    .str.replace(
                        "\xa0",
                        " ",
                        regex=False
                    )
                    .str.strip()
                )

        return data

    except Exception as e:

        st.error(
            "Unable to load MOC data from Google Sheet."
        )

        st.code(
            str(e)
        )

        return pd.DataFrame()


df = load_moc_data()


# ============================================================
# REQUIRED MOC COLUMNS
# ============================================================

required_columns = [

    "Sr No",

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

    "SOP/SMP Revision (YES/NO)",

    "Training After SOP/SMP Revision (YES/NO)",

    "PSSR (YES/NO)",

    "Document Location",

    "Status",

    "Attach MOC Softcopy Link",

    "Remarks"
]


# ============================================================
# DATA CHECK
# ============================================================

if df.empty:

    st.error(
        "No records found in Google Sheet → MOC."
    )

    st.stop()


missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error(
        "Some MOC columns are missing."
    )

    st.write(
        "Missing columns:"
    )

    for col in missing_columns:

        st.write(
            f"• {col}"
        )

    st.write(
        "Columns received from Google Sheet:"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()


# ============================================================
# DATE CONVERSION
# ============================================================

df["Request Date"] = pd.to_datetime(
    df["Request Date"],
    errors="coerce",
    dayfirst=True
)

df["Implementation Date"] = pd.to_datetime(
    df["Implementation Date"],
    errors="coerce",
    dayfirst=True
)

df["Review Date"] = pd.to_datetime(
    df["Review Date"],
    errors="coerce",
    dayfirst=True
)


# ============================================================
# NORMALIZE STATUS
# ============================================================

def normalize_status(value):

    text = str(value).strip().lower()

    # Open / active MOC
    if text in [
        "open",
        "ongoing",
        "on going",
        "in progress",
        "in execution",
        "execution",
        "active"
    ]:
        return "Open"

    # Closed / completed MOC
    if text in [
        "closed",
        "complete",
        "completed",
        "closed moc",
        "implemented",
        "done"
    ]:
        return "Closed"

    # Other/blank values are not counted in Open or Closed
    return "Pending"


df["Status Display"] = (
    df["Status"]
    .apply(normalize_status)
)


# ============================================================
# NORMALIZE TYPE
# ============================================================

df["Type Display"] = (
    df[
        "Change Type (Permanent/Temporary/Emergency)"
    ]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.title()
)


# ============================================================
# NORMALIZE CATEGORY
# ============================================================

df["Category Display"] = (
    df[
        "Category of changes (Technology/Personnel/Facility)"
    ]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.title()
)


# ============================================================
# YEAR
# ============================================================

df["Year"] = (
    df["Request Date"]
    .dt.year
)


# ============================================================
# INDUSTRIAL PSM HEADER
# HEADER TAKEN FROM THE SECOND PHA CODE
# ============================================================

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
    background: #D0DBE3;
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
            rgba(55, 99, 130, .28) 0%,
            rgba(232, 240, 246, .68) 45%,
            rgba(248, 251, 253, .90) 100%
        ),

        linear-gradient(
            180deg,
            #E7EEF3 0%,
            #D2DEE7 100%
        );

    border-top:
        2px solid #557A95;

    border-bottom:
        3px solid #476A84;

    box-shadow:
        0 0 18px rgba(36, 91, 130, .16);
}


/* TECH DOTS */

.header::before {

    content: "";

    position: absolute;

    inset: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(36, 91, 130, .14) 1.3px,
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
            rgba(36, 91, 130, .11) 7% 8%,
            transparent 8% 11%,
            rgba(36, 91, 130, .07) 11% 12%,
            transparent 12%
        ),

        linear-gradient(
            315deg,
            transparent 0 7%,
            rgba(36, 91, 130, .11) 7% 8%,
            transparent 8% 11%,
            rgba(36, 91, 130, .07) 11% 12%,
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
    height: 145px;

    opacity: .75;

    z-index: 1;
}

.industrial .steel {
    fill: #8295A4;
    stroke: #5D7385;
    stroke-width: 1.5;
}

.industrial .light {
    fill: none;
    stroke: #5E829D;
    stroke-width: 1.2;
    opacity: .65;
}

.industrial .window {
    fill: #7198B2;
    opacity: .75;
}

.hex {
    fill: none;
    stroke: #7C9CAF;
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
            #F5F8FA 0%,
            #E1EAF0 100%
        );

    border:
        1px solid #A8BDCC;

    border-radius:
        14px;

    color: #245B82;

    font-size: 42px;

    font-weight: 950;

    letter-spacing: 1px;

    box-shadow:

        0 0 18px
        rgba(36, 91, 130, .13),

        inset 0 0 20px
        rgba(89, 124, 94, .08);
}

.pillar::before,
.pillar::after {

    position: absolute;

    top: 50%;

    transform:
        translateY(-50%);

    color: #245B82;

    font-size: 21px;

    font-weight: 950;

    letter-spacing: -5px;

    text-shadow:
        0 0 8px rgba(36,140,210,.45);
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
            #245B82,
            #557B96,
            #245B82
        );

    border:
        1px solid #A8BDCC;

    border-radius:
        7px;

    color: #FFFFFF;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 1.8px;

    box-shadow:
        0 0 8px rgba(36, 91, 130, .10);
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
            #6C91AB 18%,
            #FFFFFF 50%,
            #6C91AB 82%,
            transparent
        );

    box-shadow:
        0 0 10px #6C91AB,
        0 0 22px rgba(36,140,210,.55);
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
            #6C91AB,
            #FFFFFF,
            #6C91AB,
            transparent
        );

    box-shadow:
        0 0 10px #6C91AB,
        0 0 24px rgba(36,140,210,.55);

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
            #6C91AB,
            transparent
        );

    box-shadow:
        0 0 10px #6C91AB;
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

        <div class="title">

        </div>

        <div class="pillar">
            PILLAR: MOC
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


# ============================================================
# YEAR / MONTH / DEPARTMENT CONTROLS
# REFRESH BOX REMOVED
# ============================================================
header_month, header_department = st.columns(
    [1.0, 1.0],
    gap="small"
)


# ============================================================
# YEAR
# ============================================================

# ============================================================
# MONTH
# ============================================================

with header_month:

    month_options = [
        "All Months",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    selected_month = st.selectbox(
        "Month",
        month_options,
        index=0,
        label_visibility="collapsed"
    )


# ============================================================
# DEPARTMENT
# ============================================================

with header_department:

    department_options = sorted(
        df["Department"]
        .fillna("")
        .astype(str)
        .str.strip()
        .loc[
            lambda s: s != ""
        ]
        .unique()
        .tolist()
    )

    department_options = [
        "All Departments"
    ] + department_options

    selected_department = st.selectbox(
        "Department",
        department_options,
        index=0,
        label_visibility="collapsed"
    )


# ============================================================
# FILTER BY YEAR / MONTH / DEPARTMENT
# ============================================================

view_df = df.copy()


if selected_month != "All Months":

    selected_month_number = month_options.index(
        selected_month
    )

    view_df = view_df[
        view_df["Request Date"].dt.month
        ==
        selected_month_number
    ]


if selected_department != "All Departments":

    view_df = view_df[
        view_df["Department"]
        .fillna("")
        .astype(str)
        .str.strip()
        ==
        selected_department
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

# LIVE KPI CALCULATION FROM GOOGLE SHEET STATUS
# Change the Status in Google Sheet and click Refresh.
total_moc = int(len(view_df))

open_moc = int(
    (view_df["Status Display"] == "Open").sum()
)

closed_moc = int(
    (view_df["Status Display"] == "Closed").sum()
)

closure_percentage = (
    round(
        (closed_moc / total_moc) * 100,
        2
    )
    if total_moc > 0
    else 0
)


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4 = st.columns(
    4,
    gap="small"
)


# ============================================================
# TOTAL
# ============================================================

with k1:

    st.html(
        f"""
<div class="kpi-card kpi-blue">

    <div class="kpi-title">
        Total MOC
    </div>

    <div class="kpi-number">
        {total_moc:,}
    </div>

    <div style="
        position:relative;
        z-index:2;
        margin-top:6px;
        color:#667085;
        font-size:10px;
    ">
        Total Changes
    </div>

    <div class="kpi-icon">
        📄
    </div>

    <div class="kpi-line"></div>

</div>
        """
)


# ============================================================
# OPEN
# ============================================================

with k2:

    st.html(
        f"""
<div class="kpi-card kpi-green">

    <div class="kpi-title">
        Open MOC
    </div>

    <div class="kpi-number">
        {open_moc:,}
    </div>

    <div style="
        position:relative;
        z-index:2;
        margin-top:6px;
        color:#667085;
        font-size:10px;
    ">
        In Progress
    </div>

    <div class="kpi-icon">
        📁
    </div>

    <div class="kpi-line"></div>

</div>
        """
)


# ============================================================
# CLOSED
# ============================================================

with k3:

    st.html(
        f"""
<div class="kpi-card kpi-red">

    <div class="kpi-title">
        Closed MOC
    </div>

    <div class="kpi-number">
        {closed_moc:,}
    </div>

    <div style="
        position:relative;
        z-index:2;
        margin-top:6px;
        color:#667085;
        font-size:10px;
    ">
        Completed
    </div>

    <div class="kpi-icon">
        ✓
    </div>

    <div class="kpi-line"></div>

</div>
        """
)


# ============================================================
# CLOSURE
# ============================================================

with k4:

    st.html(
        f"""
<div class="kpi-card kpi-orange">

    <div class="kpi-title">
        MOC Closure %
    </div>

    <div class="kpi-number">
        {closure_percentage:.2f}%
    </div>

    <div style="
        position:relative;
        z-index:2;
        margin-top:6px;
        color:#667085;
        font-size:10px;
    ">
        Overall Closure
    </div>

    <div class="kpi-icon">
        ◔
    </div>

    <div class="kpi-line"></div>

</div>
        """
)


# ============================================================
# MONTH-WISE DATA
# ============================================================

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]


monthly_counts = (
    view_df
    .dropna(
        subset=["Request Date"]
    )
    .groupby(
        view_df[
            "Request Date"
        ].dt.month
    )
    .size()
)


monthly_values = [

    int(
        monthly_counts.get(
            month,
            0
        )
    )

    for month in range(
        1,
        13
    )
]


# ============================================================
# DEPARTMENT DATA
# ============================================================

department_data = (
    view_df
    .groupby(
        "Department"
    )
    .size()
    .reset_index(
        name="Count"
    )
    .sort_values(
        "Count",
        ascending=False
    )
)


# ============================================================
# MOC REGISTER HEADER
# ============================================================

st.html(
    """
<div class="register-card">

    <div class="register-header">

        <span class="register-icon">
            ▣
        </span>

        MOC Register

    </div>

</div>
    """
)


# ============================================================
# REGISTER FILTERS
# ============================================================

search_col, status_col, type_col, category_col, new_col = st.columns(
    [2.4, 0.9, 1.05, 1.05, 0.9],
    gap="small"
)


# ============================================================
# SEARCH
# ============================================================

with search_col:

    search_text = st.text_input(

        "Search",

        placeholder="Search MOC...",

        label_visibility="collapsed"
    )


# ============================================================
# STATUS FILTER
# ============================================================

with status_col:

    status_filter = st.selectbox(

        "Status",

        [
            "All",
            "Open",
            "Closed"
        ],

        label_visibility="collapsed"
    )


# ============================================================
# TYPE FILTER
# ============================================================

with type_col:

    type_options = [
        "All"
    ] + sorted(

        view_df[
            "Type Display"
        ]
        .dropna()
        .unique()
        .tolist()
    )


    type_filter = st.selectbox(

        "Type",

        type_options,

        label_visibility="collapsed"
    )


# ============================================================
# CATEGORY FILTER
# ============================================================

with category_col:

    category_options = [
        "All"
    ] + sorted(

        view_df[
            "Category Display"
        ]
        .dropna()
        .unique()
        .tolist()
    )


    category_filter = st.selectbox(

        "Category",

        category_options,

        label_visibility="collapsed"
    )


# ============================================================
# NEW MOC
# ============================================================

with new_col:

    st.button(
        "＋ New MOC",
        use_container_width=True
    )


# ============================================================
# REGISTER FILTERING
# ============================================================

register_df = view_df.copy()


if status_filter != "All":

    register_df = register_df[
        register_df[
            "Status Display"
        ]
        ==
        status_filter
    ]


if type_filter != "All":

    register_df = register_df[
        register_df[
            "Type Display"
        ]
        ==
        type_filter
    ]


if category_filter != "All":

    register_df = register_df[
        register_df[
            "Category Display"
        ]
        ==
        category_filter
    ]


# ============================================================
# SEARCH
# ============================================================

if search_text:

    query = (
        search_text
        .strip()
        .lower()
    )


    searchable_columns = [

        "MOC No",

        "Department",

        "Section",

        "Requestor Name",

        "Description of Change",

        "Risk Level",

        "Approval Status",

        "Approved By",

        "Status"

    ]


    mask = pd.Series(
        False,
        index=register_df.index
    )


    for column in searchable_columns:

        mask |= (

            register_df[
                column
            ]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                query,
                na=False
            )
        )


    register_df = register_df[
        mask
    ]


# ============================================================
# PAGINATION
# ============================================================

PAGE_SIZE = 5


total_records = len(
    register_df
)


total_pages = max(

    1,

    (
        total_records
        +
        PAGE_SIZE
        -
        1
    )
    //
    PAGE_SIZE
)


if "moc_page" not in st.session_state:

    st.session_state.moc_page = 1


if (
    st.session_state.moc_page
    >
    total_pages
):

    st.session_state.moc_page = (
        total_pages
    )


page = st.session_state.moc_page


start_index = (
    page - 1
) * PAGE_SIZE


end_index = (
    start_index
    +
    PAGE_SIZE
)


page_df = register_df.iloc[
    start_index:end_index
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(value):

    if pd.isna(value):

        return ""

    return html.escape(
        str(value)
    )


def type_pill(value):

    text = safe_text(
        value
    )

    lower = text.lower()


    if "permanent" in lower:

        css = "type-permanent"

    elif "temporary" in lower:

        css = "type-temporary"

    elif "emergency" in lower:

        css = "type-emergency"

    else:

        css = "type-other"


    return (
        f'<span class="type-pill {css}">'
        f'{text}'
        f'</span>'
    )


def category_pill(value):

    text = safe_text(
        value
    )

    lower = text.lower()


    if "technology" in lower:

        css = "cat-technology"

    elif "personnel" in lower:

        css = "cat-personnel"

    elif "facility" in lower:

        css = "cat-facility"

    else:

        css = "cat-other"


    return (
        f'<span class="category-pill {css}">'
        f'{text}'
        f'</span>'
    )


def status_pill(value):

    text = safe_text(
        value
    )

    lower = text.lower()


    if lower == "open":

        css = "status-open"

    elif lower == "closed":

        css = "status-closed"

    else:

        css = "status-other"


    return (
        f'<span class="status-pill {css}">'
        f'{text}'
        f'</span>'
    )


# ============================================================
# BUILD REGISTER TABLE
# ============================================================

table_html = """

<table class="moc-table">

<colgroup>

    <col style="width:12%">

    <col style="width:12%">

    <col style="width:24%">

    <col style="width:11%">

    <col style="width:11%">

    <col style="width:9%">

    <col style="width:10%">

    <col style="width:11%">

</colgroup>


<thead>

<tr>

    <th>
        Department
    </th>

    <th>
        MOC No.
    </th>

    <th>
        Description of Change
    </th>

    <th>
        Type of MOC
    </th>

    <th>
        Category
    </th>

    <th>
        Status
    </th>

    <th>
        MOC Document
    </th>

    <th>
        Request Date
    </th>

</tr>

</thead>


<tbody>
"""


# ============================================================
# TABLE ROWS
# ============================================================

for _, row in page_df.iterrows():

    link = str(
        row[
            "Attach MOC Softcopy Link"
        ]
    ).strip()


    # --------------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------------

    if link.lower() in [
        "",
        "nan",
        "none"
    ]:

        document_html = (
            '<span style="color:#98a2b3;">'
            'No Link'
            '</span>'
        )

    else:

        document_html = (

            f'<a '

            f'class="view-link" '

            f'href="{safe_text(link)}" '

            f'target="_blank">'

            f'◉ View'

            f'</a>'
        )


    # --------------------------------------------------------
    # REQUEST DATE
    # --------------------------------------------------------

    request_date = row[
        "Request Date"
    ]


    if pd.notna(
        request_date
    ):

        request_date_text = (
            request_date
            .strftime(
                "%d-%m-%Y"
            )
        )

    else:

        request_date_text = ""


    # --------------------------------------------------------
    # TABLE ROW
    # --------------------------------------------------------

    table_html += f"""

<tr>

    <td>
        {safe_text(row["Department"])}
    </td>


    <td>

        <strong
            style="color:#20365c;"
        >
            {safe_text(row["MOC No"])}
        </strong>

    </td>


    <td class="description">

        {safe_text(
            row["Description of Change"]
        )}

    </td>


    <td>

        {type_pill(
            row["Type Display"]
        )}

    </td>


    <td>

        {category_pill(
            row["Category Display"]
        )}

    </td>


    <td>

        {status_pill(
            row["Status Display"]
        )}

    </td>


    <td>

        {document_html}

    </td>


    <td>

        {safe_text(
            request_date_text
        )}

    </td>

</tr>

"""


table_html += """

</tbody>

</table>

"""


# ============================================================
# DISPLAY TABLE
# ============================================================

st.html(
    table_html
)


# ============================================================
# PAGINATION
# ============================================================

page_left, page_first, page_prev, page_next, page_right = st.columns(
    [3.8, 0.45, 0.45, 0.45, 1.0],
    gap="small"
)


# ============================================================
# PAGE INFO
# ============================================================

with page_left:

    first_record = (

        start_index + 1

        if total_records > 0

        else 0
    )


    last_record = min(
        end_index,
        total_records
    )


    st.html(
        f"""
        <div class="page-info">

            Showing {first_record}
            to {last_record}
            of {total_records} entries

        </div>
        """
)


# ============================================================
# FIRST PAGE
# ============================================================

with page_first:

    if st.button(
        "«",
        disabled=(
            page <= 1
        ),
        key="moc_first"
    ):

        st.session_state.moc_page = 1

        st.rerun()


# ============================================================
# PREVIOUS
# ============================================================

with page_prev:

    if st.button(
        "‹",
        disabled=(
            page <= 1
        ),
        key="moc_previous"
    ):

        st.session_state.moc_page -= 1

        st.rerun()


# ============================================================
# NEXT
# ============================================================

with page_next:

    if st.button(
        "›",
        disabled=(
            page >= total_pages
        ),
        key="moc_next"
    ):

        st.session_state.moc_page += 1

        st.rerun()


# ============================================================
# PAGE NUMBER
# ============================================================

with page_right:

    st.html(
        f"""
        <div
            style="
                text-align:right;
                color:#667085;
                font-size:10px;
                padding-top:7px;
            "
        >
            Page {page}
            of
            {total_pages}
        </div>
        """
)

