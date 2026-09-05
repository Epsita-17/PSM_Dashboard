import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import re
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Training Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GOOGLE SHEET
# =========================================================

SPREADSHEET_ID = (
    "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
)

TRAINING_SHEET_NAME = "TRAINING"

TRAINING_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet="
    f"{TRAINING_SHEET_NAME}"
)


# =========================================================
# LOAD GOOGLE SHEET
# =========================================================

@st.cache_data(ttl=60)
def get_training_data():

    try:

        data = pd.read_csv(
            TRAINING_CSV_URL
        )

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
            f"Unable to load Google Sheet "
            f"'{TRAINING_SHEET_NAME}': {exc}"
        )

        return pd.DataFrame()


df = get_training_data()


if df.empty:

    st.error(
        f"No data found in Google Sheet tab "
        f"'{TRAINING_SHEET_NAME}'."
    )

    st.stop()


# =========================================================
# COLUMN NORMALIZATION
# =========================================================

def clean_column_name(value):

    value = str(value)

    value = (
        value
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .lower()
    )

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    return value.strip("_")


column_map = {
    clean_column_name(col): col
    for col in df.columns
}


def find_column(possible_names):

    for name in possible_names:

        key = clean_column_name(name)

        if key in column_map:

            return column_map[key]

    for key, original in column_map.items():

        for name in possible_names:

            search_key = clean_column_name(name)

            if (
                search_key in key
                or key in search_key
            ):

                return original

    return None


# =========================================================
# COLUMN DETECTION
# =========================================================

COL_MODULE = find_column([
    "Module",
    "Pillar",
    "Training Module",
    "Training Pillar",
    "Topic",
    "Process"
])

COL_DEPARTMENT = find_column([
    "Department",
    "Departments",
    "Dept"
])

COL_MONTH = find_column([
    "Month",
    "Training Month",
    "Date",
    "Training Date"
])

COL_LEVEL = find_column([
    "Level",
    "L08",
    "L08 Level",
    "Employee Level",
    "Grade"
])

COL_PERSON_TYPE = find_column([
    "Person Type",
    "Employee Type",
    "Worker Type",
    "Associate / Contractual",
    "Associate Type"
])

COL_STATUS = find_column([
    "Status",
    "Training Status",
    "Completion Status"
])

COL_TOTAL = find_column([
    "Total",
    "Total Employees",
    "Total Workers",
    "Total Headcount",
    "Total Associates"
])

COL_TRAINED = find_column([
    "Trained",
    "Training Completed",
    "Completed",
    "No. Trained",
    "Number Trained"
])

COL_COMPLETION = find_column([
    "Completion %",
    "Completion Percentage",
    "Completion",
    "Training Completion %",
    "%"
])


# =========================================================
# DATA PREPARATION
# =========================================================

work = df.copy()


if COL_DEPARTMENT:

    work["_department"] = (
        work[COL_DEPARTMENT]
        .fillna("")
        .astype(str)
        .str.strip()
    )

else:

    work["_department"] = "Others"


if COL_MODULE:

    work["_module"] = (
        work[COL_MODULE]
        .fillna("")
        .astype(str)
        .str.strip()
    )

else:

    work["_module"] = "Other"


if COL_MONTH:

    work["_date"] = pd.to_datetime(
        work[COL_MONTH],
        errors="coerce",
        dayfirst=True
    )

else:

    work["_date"] = pd.NaT


if COL_LEVEL:

    work["_level"] = (
        work[COL_LEVEL]
        .fillna("")
        .astype(str)
        .str.strip()
    )

else:

    work["_level"] = ""


if COL_PERSON_TYPE:

    work["_person_type"] = (
        work[COL_PERSON_TYPE]
        .fillna("")
        .astype(str)
        .str.strip()
    )

else:

    work["_person_type"] = ""


if COL_STATUS:

    work["_status"] = (
        work[COL_STATUS]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

else:

    work["_status"] = ""


# =========================================================
# NUMERIC DATA
# =========================================================

def numeric_column(column):

    if column is None:

        return pd.Series(
            0,
            index=work.index,
            dtype=float
        )

    return pd.to_numeric(

        work[column]
        .astype(str)
        .str.replace(
            ",",
            "",
            regex=False
        )
        .str.replace(
            "%",
            "",
            regex=False
        )
        .str.strip(),

        errors="coerce"

    ).fillna(0)


work["_total"] = numeric_column(
    COL_TOTAL
)

work["_trained"] = numeric_column(
    COL_TRAINED
)

work["_completion"] = numeric_column(
    COL_COMPLETION
)


if COL_COMPLETION is None:

    work["_completion"] = 0.0

    valid_total = (
        work["_total"] > 0
    )

    work.loc[
        valid_total,
        "_completion"
    ] = (

        work.loc[
            valid_total,
            "_trained"
        ]

        /

        work.loc[
            valid_total,
            "_total"
        ]

        *

        100
    )


# =========================================================
# COMPLETE VISUAL CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   REMOVE DEFAULT STREAMLIT SPACE
   ========================================================= */

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
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {

    margin:0 !important;
    padding:0 !important;

    overflow-x:hidden !important;
}


[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {

    width:100% !important;

    max-width:none !important;

    margin:0 !important;

    padding:0 8px !important;
}


[data-testid="stAppViewContainer"] > .main > div {

    padding:0 !important;
}


/* =========================================================
   LIGHT BLUE BACKGROUND
   ========================================================= */

.stApp {

    background:

        linear-gradient(
            180deg,
            #eaf7fc 0%,
            #e4f3fa 48%,
            #dceef7 100%
        ) !important;

    color:#111111 !important;
}


[data-testid="stVerticalBlock"] {
    gap:0 !important;
}


[data-testid="stHorizontalBlock"] {
    gap:7px !important;
}


/* =========================================================
   FILTER
   ========================================================= */

.filter-title {

    color:#193d77;

    font-size:10px;

    font-weight:900;

    letter-spacing:.4px;

    margin:0 0 2px 3px;
}


div[data-baseweb="select"] > div {

    height:28px !important;

    min-height:28px !important;

    border-radius:7px !important;

    background:#ffffff !important;

    border:1px solid #cbdde6 !important;

    box-shadow:

        inset 0 1px 0 #ffffff,

        0 3px 8px
        rgba(55,90,110,.10) !important;
}


div[data-baseweb="select"] * {

    color:#111111 !important;

    font-size:10px !important;
}


div[data-baseweb="select"] svg {

    fill:#193d77 !important;
}


/* =========================================================
   MILKY WHITE KPI
   ========================================================= */

.kpi-card {

    position:relative;

    height:118px;

    overflow:hidden;

    background:

        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 22%,
            #fffefe 45%,
            #fbfdfe 68%,
            #edf6fa 100%
        );

    border:1px solid #cbdde6;

    border-radius:15px;

    padding:9px 10px;

    box-shadow:

        0 12px 26px
        rgba(55,90,110,.16),

        0 5px 10px
        rgba(55,90,110,.08),

        inset 0 2px 0 #ffffff,

        inset 0 -7px 14px
        rgba(175,202,215,.18);
}


/* =========================================================
   GLOSS
   ========================================================= */

.kpi-card::before {

    content:"";

    position:absolute;

    top:0;

    left:0;

    right:0;

    height:50%;

    background:

        linear-gradient(
            180deg,
            rgba(255,255,255,1),
            rgba(255,255,255,.92),
            rgba(255,255,255,.35),
            transparent
        );

    border-radius:
        15px 15px 50% 50%;

    pointer-events:none;
}


/* =========================================================
   KPI LABEL
   ========================================================= */

.kpi-label {

    position:relative;

    z-index:2;

    color:#193d77;

    font-size:11px;

    font-weight:950;

    text-align:center;

    letter-spacing:.35px;

    line-height:1.25;

    min-height:25px;

    text-shadow:
        0 1px 0 #ffffff;
}


/* =========================================================
   KPI VALUE
   ========================================================= */

.kpi-value {

    position:relative;

    z-index:2;

    color:#163f7a;

    font-size:33px;

    line-height:1;

    font-weight:950;

    text-align:center;

    margin-top:3px;

    text-shadow:
        0 2px 1px rgba(0,0,0,.08);
}


.kpi-value.blue {
    color:#163f7a;
}


.kpi-value.red {
    color:#d52d34;
}


.kpi-sub {

    position:relative;

    z-index:2;

    color:#29465f;

    font-size:10px;

    font-weight:750;

    text-align:center;

    margin-top:6px;
}


/* =========================================================
   DONUT
   ========================================================= */

.donut-card {

    height:118px;

    position:relative;

    display:flex;

    align-items:center;

    justify-content:center;

    background:

        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 25%,
            #fffefe 50%,
            #f8fcfd 75%,
            #edf6fa 100%
        );

    border:1px solid #cbdde6;

    border-radius:15px;

    box-shadow:

        0 12px 26px
        rgba(55,90,110,.16),

        0 5px 10px
        rgba(55,90,110,.08),

        inset 0 2px 0 #ffffff,

        inset 0 -7px 14px
        rgba(175,202,215,.18);
}


.donut-wrap {

    position:relative;

    width:70px;

    height:70px;
}


.donut-svg {

    width:70px;

    height:70px;

    transform:rotate(-90deg);
}


.donut-bg {

    fill:none;

    stroke:#e1e9ee;

    stroke-width:8;
}


.donut-progress {

    fill:none;

    stroke:#193d77;

    stroke-width:8;

    stroke-linecap:butt;
}


/* =========================================================
   FIRST KPI NUMBER
   COLOUR UNCHANGED
   ONLY SIZE LARGE
   ========================================================= */

.donut-text {

    position:absolute;

    left:0;

    right:0;

    top:20px;

    text-align:center;

    font-size:26px;

    font-weight:950;

    color:#193d77;

    text-shadow:
        0 1px 0 #ffffff;
}


.donut-title {

    position:absolute;

    top:9px;

    left:0;

    right:0;

    text-align:center;

    font-size:9px;

    color:#193d77;

    font-weight:950;
}


.donut-bottom {

    position:absolute;

    bottom:7px;

    left:0;

    right:0;

    text-align:center;

    font-size:9px;

    color:#193d77;
}


/* =========================================================
   MAIN CHART CARD
   ========================================================= */

.chart-panel {

    position:relative;

    width:100%;

    background:

        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 20%,
            #fffefe 43%,
            #fbfdfe 68%,
            #eef6fa 100%
        );

    border:1px solid #c8dbe5;

    border-radius:17px;

    overflow:hidden;

    box-shadow:

        0 14px 30px
        rgba(50,85,105,.18),

        0 6px 12px
        rgba(50,85,105,.10),

        inset 0 2px 0
        rgba(255,255,255,1),

        inset 0 -10px 20px
        rgba(170,200,215,.16);
}


/* =========================================================
   WHITE GLOSS ON CHART CARD
   ========================================================= */

.chart-panel::before {

    content:"";

    position:absolute;

    top:0;

    left:0;

    right:0;

    height:40%;

    background:

        linear-gradient(
            180deg,
            rgba(255,255,255,1) 0%,
            rgba(255,255,255,.96) 25%,
            rgba(255,255,255,.60) 55%,
            rgba(255,255,255,0) 100%
        );

    border-radius:
        17px 17px 50% 50%;

    pointer-events:none;

    z-index:1;
}


/* =========================================================
   CHART TITLE
   ========================================================= */

.chart-panel-title {

    position:relative;

    z-index:3;

    height:38px;

    display:flex;

    align-items:center;

    justify-content:center;

    padding:0 14px;

    color:#193d77 !important;

    font-size:11px;

    font-weight:950;

    letter-spacing:.3px;

    text-align:center;

    background:

        linear-gradient(
            180deg,
            #ffffff 0%,
            #ffffff 60%,
            #f5fafc 100%
        );

    border-bottom:1px solid #d5e3e9;

    box-shadow:

        inset 0 1px 0 #ffffff,

        0 2px 6px
        rgba(50,80,100,.07);
}


/* =========================================================
   ACTUAL CHART AREA
   ========================================================= */

.chart-content {

    position:relative;

    z-index:2;

    padding:5px 7px 7px 7px;

    background:#ffffff !important;
}


/* =========================================================
   FORCE PLOTLY CONTAINER WHITE
   ========================================================= */

[data-testid="stPlotlyChart"] {

    background:#ffffff !important;

    border-radius:11px !important;

    overflow:hidden !important;

}


[data-testid="stPlotlyChart"] > div {

    background:#ffffff !important;

    border-radius:11px !important;

}


/* =========================================================
   MODULE TABLE PANEL
   ========================================================= */

.panel {

    position:relative;

    background:

        linear-gradient(
            145deg,
            #ffffff 0%,
            #ffffff 24%,
            #fffefe 48%,
            #f9fcfd 70%,
            #edf6fa 100%
        );

    border:1px solid #cbdde6;

    border-radius:13px;

    overflow:hidden;

    box-shadow:

        0 10px 23px
        rgba(55,90,110,.13),

        0 4px 8px
        rgba(55,90,110,.08),

        inset 0 2px 0 #ffffff,

        inset 0 -7px 13px
        rgba(175,202,215,.15);
}


.panel-title {

    height:28px;

    display:flex;

    align-items:center;

    padding:0 12px;

    color:#193d77;

    font-size:10px;

    font-weight:950;

    background:

        linear-gradient(
            180deg,
            #ffffff,
            #f7fbfc
        );

    border-bottom:1px solid #dce7ec;
}


/* =========================================================
   TABLE
   ========================================================= */

.training-table {

    width:100%;

    border-collapse:collapse;

    font-family:Arial,sans-serif;

    font-size:9px;
}


.training-table th {

    background:#193d77;

    color:#ffffff;

    font-weight:900;

    padding:5px 7px;

    text-align:center;
}


.training-table th:first-child {

    text-align:left;
}


.training-table td {

    padding:4px 7px;

    text-align:center;

    border-bottom:1px solid #e5ebef;

    color:#111111;

    font-weight:700;

    background:#ffffff;
}


.training-table td:first-child {

    text-align:left;

    font-weight:800;
}


.training-table tr:nth-child(even) td {

    background:#fbfdfe;
}


.training-table tr:nth-child(odd) td {

    background:#ffffff;
}


.training-table td.overall {

    font-weight:950;

    color:#193d77;
}


/* =========================================================
   FOOTER
   ========================================================= */

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
            Training Module (Training)
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
# FILTERS
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
        work["_date"]
        .dropna()
    )

    if not valid_dates.empty:

        month_periods = (
            valid_dates
            .dt
            .to_period("M")
            .drop_duplicates()
            .sort_values(
                ascending=False
            )
        )

        month_labels = [

            p.strftime("%B %Y")

            for p in month_periods

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

        label_visibility="collapsed"

    )


with filter_department:

    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )

    department_values = sorted(

        [
            x

            for x in
            work["_department"]
            .unique()
            .tolist()

            if str(x).strip()

        ],

        key=lambda x:
        str(x).lower()

    )


    department_options = [
        "All Departments"
    ] + department_values


    selected_department = st.selectbox(

        "Department",

        department_options,

        index=0,

        label_visibility="collapsed"

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

    selected_period = pd.Period(

        pd.to_datetime(
            selected_month,
            format="%B %Y"
        ),

        freq="M"

    )

    filtered_df = filtered_df[

        filtered_df["_date"]
        .dt
        .to_period("M")
        == selected_period

    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

if COL_TOTAL:

    total_people = int(
        filtered_df["_total"].sum()
    )

else:

    total_people = len(
        filtered_df
    )


if COL_TRAINED:

    total_trained = int(
        filtered_df["_trained"].sum()
    )

else:

    total_trained = 0


if total_people > 0:

    overall_pct = (

        total_trained
        /
        total_people
        *
        100

    )

else:

    overall_pct = (

        filtered_df["_completion"].mean()

        if not filtered_df.empty

        else 0

    )


# =========================================================
# PERSON TYPE
# =========================================================

person_text = (
    filtered_df["_person_type"]
    .astype(str)
    .str.lower()
)


associate_mask = (
    person_text.str.contains(
        "associate|employee",
        regex=True,
        na=False
    )
)


contractual_mask = (
    person_text.str.contains(
        "contract|contractual",
        regex=True,
        na=False
    )
)


associate_df = filtered_df[
    associate_mask
]


contractual_df = filtered_df[
    contractual_mask
]


# =========================================================
# ASSOCIATES
# =========================================================

if associate_df.empty:

    associate_total = 0

    associate_trained = 0

else:

    associate_total = (

        int(
            associate_df["_total"].sum()
        )

        if COL_TOTAL

        else len(
            associate_df
        )

    )


    associate_trained = (

        int(
            associate_df["_trained"].sum()
        )

        if COL_TRAINED

        else 0

    )


associate_pct = (

    associate_trained
    /
    associate_total
    *
    100

    if associate_total > 0

    else 0

)


# =========================================================
# CONTRACTUAL
# =========================================================

if contractual_df.empty:

    contractual_total = 0

    contractual_trained = 0

else:

    contractual_total = (

        int(
            contractual_df["_total"].sum()
        )

        if COL_TOTAL

        else len(
            contractual_df
        )

    )


    contractual_trained = (

        int(
            contractual_df["_trained"].sum()
        )

        if COL_TRAINED

        else 0

    )


contractual_pct = (

    contractual_trained
    /
    contractual_total
    *
    100

    if contractual_total > 0

    else 0

)


# =========================================================
# L08 / BELOW L08
# =========================================================

level_text = (
    filtered_df["_level"]
    .astype(str)
    .str.lower()
)


l08_mask = (
    level_text.str.contains(
        r"l0?8|l09|l10|l11|l12|l13|l14|above",
        regex=True,
        na=False
    )
)


below_l08_mask = (
    level_text.str.contains(
        r"below|l0?[1-7]",
        regex=True,
        na=False
    )
)


l08_df = filtered_df[
    l08_mask
]


below_l08_df = filtered_df[
    below_l08_mask
]


def calculate_group_pct(group):

    if group.empty:

        return 0


    total = (

        group["_total"].sum()

        if COL_TOTAL

        else len(group)

    )


    trained = (

        group["_trained"].sum()

        if COL_TRAINED

        else 0

    )


    if total > 0:

        return (

            trained
            /
            total
            *
            100

        )


    return group[
        "_completion"
    ].mean()


l08_pct = calculate_group_pct(
    l08_df
)


below_l08_pct = calculate_group_pct(
    below_l08_df
)


# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4, k5, k6 = st.columns(

    [1.05, 1, 1.05, 1, 1, 1],

    gap="small"

)


# =========================================================
# KPI 1
# =========================================================

with k1:

    radius = 42

    circumference = (
        2
        *
        3.14159
        *
        radius
    )

    dash = (

        circumference
        *
        min(
            max(
                overall_pct,
                0
            ),
            100
        )
        /
        100

    )

    st.html(

        f"""
        <div class="donut-card">

            <div class="donut-title">
                OVERALL TRAINING COMPLETION
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
                            {dash:.1f}
                            {circumference:.1f}
                        "
                    />

                </svg>

                <div class="donut-text">

                    {overall_pct:.1f}%

                </div>

            </div>

            <div class="donut-bottom">

                Overall % Trained

            </div>

        </div>
        """
    )


# =========================================================
# KPI 2
# SYMBOL REMOVED
# =========================================================

with k2:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:18px;"
            >

                {associate_total:,}

            </div>

            <div class="kpi-sub">

                Trained:
                {associate_trained:,}
                ({associate_pct:.1f}%)

            </div>

        </div>
        """

    )


# =========================================================
# KPI 3
# SYMBOL REMOVED
# =========================================================

with k3:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL CONTRACTUAL
                WORKERS TRAINED

            </div>

            <div
                class="kpi-value red"
                style="margin-top:18px;"
            >

                {contractual_total:,}

            </div>

            <div class="kpi-sub">

                Trained:
                {contractual_trained:,}
                ({contractual_pct:.1f}%)

            </div>

        </div>
        """

    )


# =========================================================
# KPI 4
# =========================================================

with k4:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

                <br>

                (L08 & ABOVE)

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:15px;"
            >

                {l08_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# KPI 5
# =========================================================

with k5:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                TOTAL ASSOCIATES TRAINED

                <br>

                (BELOW L08)

            </div>

            <div
                class="kpi-value red"
                style="margin-top:15px;"
            >

                {below_l08_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# KPI 6
# =========================================================

with k6:

    st.html(

        f"""
        <div class="kpi-card">

            <div class="kpi-label">

                OVERALL TRAINING

                <br>

                COMPLETION

            </div>

            <div
                class="kpi-value blue"
                style="margin-top:15px;"
            >

                {overall_pct:.1f}%

            </div>

            <div class="kpi-sub">

                Completion %

            </div>

        </div>
        """

    )


# =========================================================
# PILLAR DATA
# =========================================================

pillar_data = (

    filtered_df

    .groupby("_module")

    .agg(

        total=("_total", "sum"),

        trained=("_trained", "sum"),

        completion=(
            "_completion",
            "mean"
        )

    )

)


if not pillar_data.empty:

    pillar_data["percentage"] = (

        pillar_data.apply(

            lambda row:

                (
                    row["trained"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else row["completion"],

            axis=1

        )

    )


    pillar_data = (

        pillar_data

        .sort_values(
            "percentage",
            ascending=False
        )

    )


# =========================================================
# DEPARTMENT DATA
# =========================================================

dept_data = (

    filtered_df

    .groupby("_department")

    .agg(

        total=("_total", "sum"),

        trained=("_trained", "sum"),

        completion=(
            "_completion",
            "mean"
        )

    )

)


if not dept_data.empty:

    dept_data["percentage"] = (

        dept_data.apply(

            lambda row:

                (
                    row["trained"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else row["completion"],

            axis=1

        )

    )


    dept_data = (

        dept_data

        .sort_values(
            "percentage",
            ascending=True
        )

    )


# =========================================================
# CHART ROW
# =========================================================

chart_left, chart_right = st.columns(

    [1, 1.08],

    gap="small"

)


# =========================================================
# PILLAR CHART
# =========================================================

with chart_left:

    st.html(

        """
        <div class="chart-panel">

            <div class="chart-panel-title">

                TRAINING COMPLETION BY PILLAR
                (PLANT WIDE)

            </div>

            <div class="chart-content">

        """

    )


    fig_pillar = go.Figure()


    if not pillar_data.empty:

        fig_pillar.add_trace(

            go.Bar(

                x=pillar_data.index.tolist(),

                y=pillar_data[
                    "percentage"
                ].tolist(),

                text=[

                    f"{x:.1f}%"

                    for x in
                    pillar_data[
                        "percentage"
                    ]

                ],

                textposition="outside",

                cliponaxis=False,

                marker=dict(

                    color="#2b66a8",

                    line=dict(

                        color="#164f8b",

                        width=1.2

                    )

                ),

                hovertemplate=

                    "%{x}<br>"
                    "Completion: "
                    "%{y:.1f}%"
                    "<extra></extra>"

            )

        )


    fig_pillar.update_layout(

        height=235,

        margin=dict(

            l=42,

            r=25,

            t=25,

            b=45

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial",

            color="#111111"

        ),

        yaxis=dict(

            range=[
                0,
                100
            ],

            dtick=25,

            title="Completion %",

            title_font=dict(

                size=10,

                color="#111111"

            ),

            tickfont=dict(

                size=8,

                color="#111111"

            ),

            gridcolor="#d2e4ed",

            gridwidth=1,

            zeroline=False,

            showline=False

        ),

        xaxis=dict(

            tickfont=dict(

                size=9,

                color="#111111"

            ),

            showgrid=False,

            showline=False,

            zeroline=False

        ),

        showlegend=False,

        bargap=.30

    )


    st.plotly_chart(

        fig_pillar,

        use_container_width=True,

        config={

            "displayModeBar":False,

            "responsive":True

        }

    )


    st.html(

        """
            </div>
        </div>
        """

    )


# =========================================================
# DEPARTMENT CHART
# =========================================================

with chart_right:

    st.html(

        """
        <div class="chart-panel">

            <div class="chart-panel-title">

                TRAINING COMPLETION BY DEPARTMENT
                (OVERALL %)

            </div>

            <div class="chart-content">

        """

    )


    fig_department = go.Figure()


    if not dept_data.empty:

        fig_department.add_trace(

            go.Bar(

                x=dept_data[
                    "percentage"
                ].tolist(),

                y=dept_data.index.tolist(),

                orientation="h",

                text=[

                    f"{x:.1f}%"

                    for x in
                    dept_data[
                        "percentage"
                    ]

                ],

                textposition="outside",

                cliponaxis=False,

                marker=dict(

                    color="#2b66a8",

                    line=dict(

                        color="#164f8b",

                        width=1.2

                    )

                ),

                hovertemplate=

                    "%{y}<br>"
                    "Completion: "
                    "%{x:.1f}%"
                    "<extra></extra>"

            )

        )


    fig_department.update_layout(

        height=235,

        margin=dict(

            l=80,

            r=50,

            t=25,

            b=40

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial",

            color="#111111"

        ),

        xaxis=dict(

            range=[
                0,
                100
            ],

            dtick=20,

            title="Overall Completion %",

            title_font=dict(

                size=10,

                color="#111111"

            ),

            tickfont=dict(

                size=8,

                color="#111111"

            ),

            gridcolor="#d2e4ed",

            gridwidth=1,

            zeroline=False,

            showline=False

        ),

        yaxis=dict(

            tickfont=dict(

                size=8,

                color="#111111"

            ),

            showgrid=False,

            showline=False,

            zeroline=False

        ),

        showlegend=False,

        bargap=.25

    )


    st.plotly_chart(

        fig_department,

        use_container_width=True,

        config={

            "displayModeBar":False,

            "responsive":True

        }

    )


    st.html(

        """
            </div>
        </div>
        """

    )


# =========================================================
# MODULE-WISE TABLE
# =========================================================

st.html(

    """
    <div
        class="panel"
        style="margin-top:6px;"
    >

        <div class="panel-title">

            MODULE WISE TRAINING COMPLETION
            BY DEPARTMENT (%)

        </div>

        <div style="
            padding:5px 6px 6px 6px;
        ">
    """

)


if (

    not filtered_df.empty

    and

    filtered_df["_module"]
    .notna()
    .any()

    and

    filtered_df["_department"]
    .notna()
    .any()

):

    pivot = (

        filtered_df

        .groupby(
            [
                "_module",
                "_department"
            ]
        )

        .agg(

            total=("_total", "sum"),

            trained=("_trained", "sum"),

            completion=(
                "_completion",
                "mean"
            )

        )

    )


    pivot["percentage"] = (

        pivot.apply(

            lambda row:

                (
                    row["trained"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else row["completion"],

            axis=1

        )

    )


    pivot = pivot.reset_index()


    table_data = pivot.pivot(

        index="_module",

        columns="_department",

        values="percentage"

    )


    table_data = (
        table_data
        .fillna(0)
    )


    # =====================================================
    # OVERALL MODULE
    # =====================================================

    overall_module = (

        filtered_df

        .groupby("_module")

        .agg(

            total=("_total", "sum"),

            trained=("_trained", "sum"),

            completion=(
                "_completion",
                "mean"
            )

        )

    )


    overall_module["Overall"] = (

        overall_module.apply(

            lambda row:

                (
                    row["trained"]
                    /
                    row["total"]
                    *
                    100
                )

                if row["total"] > 0

                else row["completion"],

            axis=1

        )

    )


    table_data["Overall"] = (
        overall_module["Overall"]
    )


    # =====================================================
    # DEPARTMENT ORDER
    # =====================================================

    preferred_departments = [

        "Blast Furnace-1",
        "Blast Furnace-2",
        "SMS-1",
        "SMS-2",
        "SMS",
        "PSM GA",
        "Coke Oven",
        "Power Plant",
        "Utilities",
        "Lime Plant",
        "Others"

    ]


    existing_columns = (
        table_data.columns.tolist()
    )


    ordered_departments = [

        x

        for x in
        preferred_departments

        if x in existing_columns

    ]


    remaining_departments = [

        x

        for x in existing_columns

        if x not in ordered_departments

        and x != "Overall"

    ]


    ordered_departments += sorted(

        remaining_departments,

        key=lambda x:
        str(x).lower()

    )


    if "Overall" in table_data.columns:

        ordered_departments.append(
            "Overall"
        )


    table_data = table_data[
        ordered_departments
    ]


    # =====================================================
    # BUILD TABLE
    # =====================================================

    html = """

    <table class="training-table">

        <thead>

            <tr>

                <th>
                    Module
                </th>

    """


    for col in table_data.columns:

        html += f"""

                <th>
                    {col}
                </th>

        """


    html += """

            </tr>

        </thead>

        <tbody>

    """


    for module_name, row in (
        table_data.iterrows()
    ):

        html += f"""

            <tr>

                <td>
                    {module_name}
                </td>

        """


        for col in table_data.columns:

            value = row[col]


            if pd.isna(value):

                value = 0


            extra_class = (

                "overall"

                if col == "Overall"

                else ""

            )


            html += f"""

                <td class="{extra_class}">

                    {value:.1f}%

                </td>

            """


        html += """

            </tr>

        """


    html += """

        </tbody>

    </table>

    """


    st.html(
        html
    )


else:

    st.info(
        "Module-wise training data is not available."
    )


st.html(

    """
        </div>
    </div>
    """

)


# =========================================================
# FOOTER
# =========================================================

st.html(

    """
    <div class="footer">

        📚 &nbsp;

        © 2026 Training Dashboard

        &nbsp; | &nbsp;

        Training

    </div>
    """

)

