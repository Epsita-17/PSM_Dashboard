import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Process Safety Incident Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GOOGLE SHEET
# =========================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

# CHANGED: PSSR -> PSI
PSI_SHEET_NAME = "PSI"

PSI_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SPREADSHEET_ID}"
    f"/gviz/tq?tqx=out:csv&sheet={PSI_SHEET_NAME}"
)


@st.cache_data(ttl=60)
def get_psi_data():
    try:

        data = pd.read_csv(PSI_CSV_URL)

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
            f"Unable to load Google Sheet "
            f"'{PSI_SHEET_NAME}': {exc}"
        )

        return pd.DataFrame()


df = get_psi_data()

if df.empty:
    st.error(
        f"No data found in Google Sheet "
        f"tab '{PSI_SHEET_NAME}'."
    )

    st.stop()

# =========================================================
# COLUMN MAPPING - PSI SHEET
# =========================================================
COL = {

    "sr_no": "Sr No",
    "department": "Department",
    "section": "Section",
    "description": "Incident Description",
    "incident_date": "Incident Date",
    "classification": "Incident Classification",
    "level": "Incident Level"

}

missing = [

    key

    for key, column in COL.items()

    if column not in df.columns

]

if missing:
    st.error(
        "Required PSI columns are missing: "
        + ", ".join(
            COL[key]
            for key in missing
        )
    )

    st.write(
        "Columns found in the PSI sheet:"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()

# =========================================================
# DATA PREPARATION
# =========================================================
work = df.copy()

# CHANGED: Incident Date is now the dashboard date
work["_due_date"] = pd.to_datetime(
    work[COL["incident_date"]],
    errors="coerce",
    dayfirst=True
)

work["_completion_date"] = pd.NaT

work["_department"] = (
    work[COL["department"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_section"] = (
    work[COL["section"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

work["_description"] = (
    work[COL["description"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =========================================================
# PSI CLASSIFICATION
# =========================================================
work["_classification_raw"] = (
    work[COL["classification"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =========================================================
# PSI LEVEL
# =========================================================
work["_level_raw"] = (
    work[COL["level"]]
    .fillna("")
    .astype(str)
    .str.strip()
)

# ---------------------------------------------------------
# Kept for compatibility with the existing KPI section.
# PSI sheet has no separate status column.
# ---------------------------------------------------------
work["_status_raw"] = ""


def normalize_psi_status(value):
    value = str(value).strip().lower()

    if "completed" in value:
        return "Completed"

    if "overdue" in value:
        return "Overdue"

    if "pending" in value:
        return "Pending"

    return "Pending"


work["_status_display"] = (
    work["_status_raw"]
    .apply(normalize_psi_status)
)

# CHANGED: trend uses Incident Date
work["_trend_date"] = work["_due_date"]

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(
    """
<style>

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
    overflow:hidden !important;
}


[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {

    width:100% !important;
    max-width:none !important;
    margin:0 !important;
    padding:0 3px !important;
}


[data-testid="stAppViewContainer"] > .main > div {
    padding:0 !important;
}


.stApp {

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #f7fbfe 48%,
            #eef5f9 100%
        ) !important;

    color:#17324d !important;
}


[data-testid="stVerticalBlock"] {
    gap:0 !important;
}


[data-testid="stHorizontalBlock"] {
    gap:5px !important;
}


/* =========================================================
   FILTERS
   ========================================================= */

.filter-title {

    color:#173b5c;

    font-size:12px;

    font-weight:900;

    letter-spacing:.4px;

    margin:0 0 0 3px;
}


div[data-baseweb="select"] > div {

    height:30px !important;

    min-height:30px !important;

    border-radius:7px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f4f8fb
        ) !important;

    border:1px solid #b8d5e8 !important;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 2px 6px rgba(22,72,110,.08) !important;
}


div[data-baseweb="select"] * {

    color:#23445f !important;

    font-size:11px !important;
}


div[data-baseweb="select"] svg {
    fill:#176da0 !important;
}


/* =========================================================
   KPI CARDS - SHINING STATUS COLORS
   ========================================================= */
.kpi-card {
    position:relative;
    height:108px;
    overflow:hidden;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    background:linear-gradient(145deg,#ffffff 0%,#fbfdff 55%,#eef6fa 100%);
    border:1px solid #c5dce9;
    border-top:5px solid #1686d9;
    border-radius:10px;
    padding:10px 12px;
    box-shadow:
        0 4px 12px rgba(28,78,110,.12),
        0 1px 2px rgba(28,78,110,.08),
        inset 0 1px 0 rgba(255,255,255,.98);
}

/* COMPLETED = GREEN */
.kpi-card.completed {
    border-top-color:#00c853;
    box-shadow:
        0 0 0 1px rgba(0,200,83,.10),
        0 0 12px rgba(0,200,83,.20),
        0 5px 14px rgba(28,78,110,.12),
        inset 0 1px 0 rgba(255,255,255,.98);
}

/* PENDING = RED */
.kpi-card.pending {
    border-top-color:#ff1744;
    box-shadow:
        0 0 0 1px rgba(255,23,68,.10),
        0 0 12px rgba(255,23,68,.20),
        0 5px 14px rgba(28,78,110,.12),
        inset 0 1px 0 rgba(255,255,255,.98);
}

/* ONGOING / STATUS = YELLOW */
.kpi-card.ongoing {
    border-top-color:#ffc400;
    box-shadow:
        0 0 0 1px rgba(255,196,0,.12),
        0 0 14px rgba(255,196,0,.24),
        0 5px 14px rgba(28,78,110,.12),
        inset 0 1px 0 rgba(255,255,255,.98);
}

/* TOTAL + COMPLIANCE = BLUE */
.kpi-card.compliance,
.kpi-card.total {
    border-top-color:#1686ff;
    box-shadow:
        0 0 0 1px rgba(22,134,255,.08),
        0 0 10px rgba(22,134,255,.14),
        0 5px 14px rgba(28,78,110,.12),
        inset 0 1px 0 rgba(255,255,255,.98);
}

/* Shining highlight on every KPI top strip */
.kpi-card::before {
    content:"";
    position:absolute;
    left:0;
    top:0;
    width:100%;
    height:5px;
    pointer-events:none;
    opacity:.95;
    background:linear-gradient(
        90deg,
        rgba(255,255,255,.18),
        rgba(255,255,255,.95),
        rgba(255,255,255,.18)
    );
}

.kpi-card::after {
    content:"";
    position:absolute;
    left:8%;
    right:8%;
    top:5px;
    height:1px;
    pointer-events:none;
    opacity:.75;
    background:linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,.95),
        transparent
    );
}

.kpi-icon { display:none !important; }

.kpi-content {
    margin-left:0 !important;
    width:100%;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
}

.kpi-label {
    color:#087bc1;
    font-size:13px;
    font-weight:950;
    letter-spacing:.45px;
    line-height:1.1;
    margin:0 !important;
}

.kpi-card.completed .kpi-label { color:#00a844; }
.kpi-card.pending .kpi-label { color:#e6002d; }
.kpi-card.ongoing .kpi-label { color:#d99f00; }
.kpi-card.compliance .kpi-label,
.kpi-card.total .kpi-label { color:#0876d1; }

.kpi-value {
    font-size:38px;
    line-height:1;
    font-weight:950;
    margin:7px 0 0 0 !important;
    color:#173b5a;
}

.kpi-value.green { color:#00ad4f; }
.kpi-value.red { color:#ed1738; }
.kpi-value.yellow { color:#e5a900; }
.kpi-value.blue { color:#1267d5; }


/* Compliance KPI value follows the blue compliance top-line color */
.kpi-card.compliance .kpi-value {
    color:#1267d5 !important;
    text-shadow:0 0 8px rgba(18,103,213,.16);
}

.kpi-description { display:none !important; }

/* =========================================================
   PANELS
   ========================================================= */

.panel {

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #f6fafc
        );

    border:1px solid #c5dce9;

    border-radius:9px;

    box-shadow:
        0 4px 12px rgba(28,78,110,.10);

    overflow:hidden;
}


.panel-title {

    height:25px;

    display:flex;

    align-items:center;

    padding:0 13px;

    color:#163b5b;

    font-size:11px;

    font-weight:950;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #eef6fa
        );

    border-bottom:2px solid #158fd0;
}


.chart-box {

    margin:6px 7px 7px 7px;

    padding:2px 5px 0 5px;

    background:#ffffff;

    border:1px solid #e2eaf0;

    border-radius:7px;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.95),
        0 1px 3px rgba(28,78,110,.06);

    overflow:hidden;
}


/* =========================================================
   LEVEL CARDS
   ========================================================= */

.level-card {

    height:100px;

    border:1px solid #c5dce9;

    border-radius:9px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f7fafc
        );

    box-shadow:
        0 3px 9px rgba(28,78,110,.08);

    text-align:center;

    padding-top:12px;
}


.level-title {

    font-size:12px;

    font-weight:950;

    letter-spacing:.4px;
}


.level-value {

    font-size:30px;

    line-height:1;

    font-weight:950;

    margin-top:7px;
}


.level-pct {

    color:#263c52;

    font-size:14px;

    margin-top:7px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    height:18px;

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

    font-size:11px;

    font-weight:800;

    border-top:1px solid #c8dce8;
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

        with open(file_path,
                  "rb") as file:

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

        "jsw_jfe_logo.jpg not found.\n"

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

<!--========================================================
         LEFT LOGO AREA
======================================================== -->
    <div
class="psm-left">

<!--====================================================
LOGO
==================================================== -->

        <div
class="logo-panel">

            <img


class="company-logo"


src="data:image/jpeg;base64,LOGO_IMAGE_BASE64"

                alt="JSW JFE Steel
Limited"

            >



        </div>





        <!--
====================================================

             LEFT VERTICAL LINE


==================================================== -->



        <div
class="vertical-line"></div>





        <!--
====================================================

             CENTER TITLE GROUP


==================================================== -->



        <div
class="title-area">





            <!-- MAIN TITLE -->



            <div
class="main-title">



                PROCESS SAFETY ANALYSIS (PSI)



                <span
class="main-title-orange"></span>



            </div>





            <!-- SUBTITLE -->



            <div
class="subtitle">



                PSM DIGITAL DASHBOARD



            </div>





            <!-- SUB-SUBTITLE -->



            <div
class="tagline">



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





    <!--
========================================================

         RIGHT DATE / TIME


======================================================== -->



    <div
class="psm-right">





        <div
class="date">



            CURRENT_DATE_VALUE



        </div>





        <div
class="time">



            CURRENT_TIME_VALUE



        </div>





        <div
class="right-line"></div>





    </div>





    <!--
========================================================

         ORANGE BOTTOM BAR


======================================================== -->



    <div
class="orange-bar"></div>





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
# FILTERS
# =========================================================
filter_month, filter_department = st.columns(
    [1.0, 1.0],
    gap="small"
)

with filter_month:
    st.markdown(
        "<div class='filter-title'>MONTH</div>",
        unsafe_allow_html=True
    )

    valid_dates = (
        work["_trend_date"]
        .dropna()
    )

    month_values = (

        valid_dates
        .dt
        .to_period("M")
        .drop_duplicates()
        .sort_values(
            ascending=False
        )

        if not valid_dates.empty

        else pd.Series(
            [],
            dtype="period[M]"
        )

    )

    month_labels = [

        p.strftime("%B %Y")

        for p in month_values

    ]

    month_options = [
                        "All Months"
                    ] + month_labels

    selected_month = st.selectbox(

        "Month",

        month_options,

        index=0,

        label_visibility="collapsed",

        key="psi_month"

    )

with filter_department:
    st.markdown(
        "<div class='filter-title'>DEPARTMENT</div>",
        unsafe_allow_html=True
    )

    department_options = [

                             "All Departments"

                         ] + sorted(

        [

            x

            for x in
            work["_department"]
            .unique()
            .tolist()

            if x and
               x.lower() != "nan"

        ],

        key=lambda x: x.lower()

    )

    selected_department = st.selectbox(

        "Department",

        department_options,

        index=0,

        label_visibility="collapsed",

        key="psi_department"

    )

# =========================================================
# APPLY FILTERS
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

        filtered_df["_trend_date"]
        .dt
        .to_period("M")
        == selected_period

        ]

trend_df = work.copy()

if selected_department != "All Departments":
    trend_df = trend_df[
        trend_df["_department"]
        == selected_department
        ]

# =========================================================
# KPI CALCULATIONS
# =========================================================
total_pssr = len(filtered_df)

completed = int(

    (
            filtered_df["_status_display"]
            == "Completed"
    ).sum()

)

pending = int(

    (
            filtered_df["_status_display"]
            == "Pending"
    ).sum()

)

overdue = int(

    (
            filtered_df["_status_display"]
            == "Overdue"
    ).sum()

)

pending_overdue = pending + overdue

compliance = (

    completed
    / total_pssr
    * 100

    if total_pssr

    else 0

)

# =========================================================
# ROW 1 KPI CARDS
# =========================================================
k1, k2, k3, k4, k5 = st.columns(
    [1, 1, 1, 1, 1],
    gap="small"
)

with k1:
    st.html(

        f"""
        <div class="kpi-card total">
<div class="kpi-content">

                <div class="kpi-label">
                    TOTAL INCIDENTS
                </div>

                <div class="kpi-value blue">
                    {total_pssr}
                </div>
</div>

        </div>
        """

    )

with k2:
    completed_pct = (

        completed
        / total_pssr
        * 100

        if total_pssr

        else 0

    )

    st.html(

        f"""
        <div class="kpi-card completed">
<div class="kpi-content">

                <div class="kpi-label">
                    INVESTIGATION COMPLETED
                </div>

                <div class="kpi-value green">
                    {completed}
                </div>
</div>

        </div>
        """

    )

with k3:
    pending_pct = (

        pending_overdue
        / total_pssr
        * 100

        if total_pssr

        else 0

    )

    st.html(

        f"""
        <div class="kpi-card pending">
<div class="kpi-content">

                <div class="kpi-label">
                    INVESTIGATION PENDING
                </div>

                <div class="kpi-value red">
                    {pending_overdue}
                </div>
</div>

        </div>
        """

    )

with k4:
    st.html(

        f"""
        <div class="kpi-card compliance">
<div class="kpi-content">

                <div class="kpi-label">
                    COMPLIANCE
                </div>

                <div class="kpi-value red">
                    {compliance:.1f}%
                </div>
</div>

        </div>
        """

    )

with k5:
    status_total = (
        total_pssr
        if total_pssr
        else 1
    )

    completed_pct_status = (

            completed
            / status_total
            * 100

    )

    st.html(

        f"""
        <div
            class="kpi-card ongoing"
            style="height:108px;"
        >

            <div
                class="kpi-content"
                style="margin-left:0;"
            >

                <div class="kpi-label">
                    INVESTIGATION STATUS
                </div>

                <div
                    style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                        margin-top:7px;
                    "
                >

                    <div
                        style="
                            width:54px;
                            height:54px;
                            border-radius:50%;

                            background:
                            conic-gradient(
                                #149c53
                                0 {completed_pct_status}%,

                                #d9272e
                                {completed_pct_status}% 100%
                            );

                            position:relative;

                            flex:0 0 54px;
                        "
                    >

                        <div
                            style="
                                position:absolute;

                                left:8px;
                                top:8px;

                                width:38px;
                                height:38px;

                                border-radius:50%;

                                background:#ffffff;

                                display:flex;

                                align-items:center;

                                justify-content:center;

                                color:#17324d;

                                font-size:13px;

                                font-weight:950;
                            "
                        >
                            {total_pssr}
                        </div>

                    </div>


                    <div
                        style="
                            font-size:10px;

                            line-height:1.55;

                            color:#263f53;

                            font-weight:800;
                        "
                    >

                        <span style="color:#149c53;">
                            ● Completed {completed}
                        </span>

                        <br>

                        <span style="color:#d9272e;">
                            ● Pending/Overdue {pending_overdue}
                        </span>

                    </div>

                </div>

            </div>

        </div>
        """

    )

# =========================================================
# MAIN CHART ROW
# =========================================================
c1, c2, c3 = st.columns(
    [1.05, 1.05, .72],
    gap="small"
)

# =========================================================
# INCIDENTS BY DEPARTMENTS
# =========================================================
with c1:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENTS BY DEPARTMENTS
            </div>

            <div class="chart-box">
        """

    )

    dept = (

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

    fig_dept = go.Figure()

    fig_dept.add_trace(

        go.Bar(

            x=dept.index.tolist(),

            y=dept.values.tolist(),

            text=dept.values.tolist(),

            textposition="outside",

            marker=dict(
                color=[
                    "#00E5FF", "#7C4DFF", "#FF4081", "#FFC400",
                    "#00E676", "#448AFF", "#FF6D00", "#D500F9",
                    "#00BFA5", "#FF1744", "#76FF03", "#536DFE"
                ][:len(dept)],
                line=dict(color="rgba(255,255,255,0.95)", width=1.5)
            ),

            hovertemplate=(

                "%{x}<br>"
                "Incidents: %{y}"
                "<extra></extra>"

            )

        )

    )

    fig_dept.update_layout(

        height=185,

        margin=dict(

            l=40,

            r=10,

            t=10,

            b=42

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        yaxis=dict(

            title="No. of Incidents",

            dtick=1,

            gridcolor="#e4edf3",

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

            title_font=dict(
                size=10
            ),

            showgrid=False

        )

    )

    st.plotly_chart(

        fig_dept,

        use_container_width=True,

        config={
            "displayModeBar": False
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# INCIDENTS MONTH-WISE TREND
# =========================================================
with c2:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENTS MONTH-WISE TREND
            </div>

            <div class="chart-box">
        """

    )

    trend_source = (

        trend_df

        .dropna(
            subset=["_trend_date"]
        )

        .copy()

    )

    if not trend_source.empty:

        trend_source["_month"] = (

            trend_source["_trend_date"]

            .dt
            .to_period("M")

        )

        trend = (

            trend_source

            .groupby("_month")

            .size()

            .sort_index()

        )

        trend_labels = [

            p.strftime("%b %y")

            for p in trend.index

        ]

        trend_values = (
            trend.values.tolist()
        )


    else:

        trend_labels = []

        trend_values = []

    fig_trend = go.Figure()

    fig_trend.add_trace(

        go.Scatter(

            x=trend_labels,

            y=trend_values,

            mode="lines+markers+text",

            text=trend_values,

            textposition="top center",

            line=dict(

                color="#123f7a",

                width=2

            ),

            marker=dict(

                size=7,

                color="#123f7a",

                line=dict(

                    color="#ffffff",

                    width=1.5

                )

            ),

            hovertemplate=(

                "%{x}<br>"
                "Incidents: %{y}"
                "<extra></extra>"

            )

        )

    )

    fig_trend.update_layout(

        height=185,

        margin=dict(

            l=35,

            r=10,

            t=10,

            b=35

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        yaxis=dict(

            title="No. of Incidents",

            dtick=1,

            gridcolor="#e4edf3",

            zeroline=False,

            tickfont=dict(
                size=9
            ),

            title_font=dict(
                size=10
            )

        ),

        xaxis=dict(

            tickfont=dict(
                size=9
            ),

            showgrid=False

        )

    )

    st.plotly_chart(

        fig_trend,

        use_container_width=True,

        config={
            "displayModeBar": False
        }

    )

    st.html(
        "</div></div>"
    )

# =========================================================
# INCIDENT CLASSIFICATION
# =========================================================
with c3:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENT CLASSIFICATION
            </div>

            <div class="chart-box">
        """

    )

    classification_labels = [

        "Near-Miss",

        "Process Safety Incident",

        "Serious Process Safety Incident"

    ]

    classification_values = [

        14,
        7,
        3

    ]

    labels_plot = (
        classification_labels[::-1]
    )

    values_plot = (
        classification_values[::-1]
    )

    fig_incident_classification = go.Figure()

    # =====================================================
    # BAR GRAPH
    # THIS IS KEPT UNCHANGED
    # =====================================================
    fig_incident_classification.add_trace(

        go.Bar(

            x=values_plot,

            y=labels_plot,

            orientation="h",

            text=values_plot,

            textposition="outside",

            cliponaxis=False,

            marker=dict(
                color=["#00E5FF", "#FF4081", "#FFC400"][:len(values_plot)],
                line=dict(color="rgba(255,255,255,0.95)", width=1.5)
            ),

            hovertemplate=(

                "%{y}<br>"
                "No. of Incidents: %{x}"
                "<extra></extra>"

            )

        )

    )

    classification_annotations = [

        dict(

            x=-1.05,

            y=2,

            xref="paper",

            yref="y",

            text="Near-Miss",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        ),

        dict(

            x=-1.05,

            y=1,

            xref="paper",

            yref="y",

            text="Process Safety Incident",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        ),

        dict(

            x=-1.05,

            y=0,

            xref="paper",

            yref="y",

            text="Serious Process Safety Incident",

            showarrow=False,

            xanchor="left",

            yanchor="middle",

            align="left",

            font=dict(

                family="Arial, sans-serif",

                size=9,

                color="#17324d"

            )

        )

    ]

    fig_incident_classification.update_layout(

        height=185,

        margin=dict(

            l=180,

            r=25,

            t=8,

            b=42

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        font=dict(

            family="Arial, sans-serif",

            size=10,

            color="#213c55"

        ),

        xaxis=dict(

            title="No. of Incidents",

            range=[0, 16],

            tickmode="array",

            tickvals=[

                0,
                5,
                10,
                15

            ],

            ticktext=[

                "0",
                "5",
                "10",
                "15"

            ],

            gridcolor="#e4edf3",

            gridwidth=1,

            zeroline=False,

            showline=False,

            tickfont=dict(

                size=9,

                color="#536a7b"

            ),

            title_font=dict(

                size=10,

                color="#17324d"

            )

        ),

        yaxis=dict(

            showticklabels=False,

            showgrid=False,

            zeroline=False,

            showline=False,

            range=[-0.5, 2.5]

        ),

        annotations=classification_annotations,

        showlegend=False,

        bargap=.48

    )

    st.plotly_chart(

        fig_incident_classification,

        use_container_width=True,

        config={

            "displayModeBar": False,

            "responsive": True

        }

    )

    st.html(

        """
            </div>
        </div>
        """

    )

# =========================================================
# THIRD ROW
# =========================================================
r3_left, r3_right = st.columns(

    [1.05, 2.00],

    gap="small"

)

# =========================================================
# INCIDENT LEVEL DISTRIBUTION
# =========================================================
with r3_left:
    st.html(

        """
        <div class="panel">

            <div class="panel-title">
                INCIDENT LEVEL DISTRIBUTION
            </div>

            <div class="chart-box">
        """

    )

    level_labels = [

        "Level 1",
        "Level 2",
        "Level 3",
        "Level 4"

    ]

    level_values = [

        int(
            (
                    filtered_df[COL["level"]]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "LEVEL 1"
            ).sum()
        ),

        int(
            (
                    filtered_df[COL["level"]]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "LEVEL 2"
            ).sum()
        ),

        int(
            (
                    filtered_df[COL["level"]]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "LEVEL 3"
            ).sum()
        ),

        int(
            (
                    filtered_df[COL["level"]]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "LEVEL 4"
            ).sum()
        )

    ]

    level_total = sum(
        level_values
    )

    fig_level = go.Figure(

        data=[

            go.Pie(

                labels=level_labels,

                values=level_values,

                hole=.58,

                sort=False,

                direction="clockwise",

                textinfo="none",

                domain=dict(

                    x=[
                        0.00,
                        0.58
                    ],

                    y=[
                        0.02,
                        0.98
                    ]

                ),

                marker=dict(

                    colors=[

                        "#18a957",
                        "#2455a4",
                        "#f4bd27",
                        "#d9272e"

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

        ]

    )

    fig_level.update_layout(

        height=150,

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        ),

        paper_bgcolor="#ffffff",

        plot_bgcolor="#ffffff",

        showlegend=True,

        legend=dict(

            orientation="v",

            x=0.62,

            y=0.50,

            xanchor="left",

            yanchor="middle",

            font=dict(

                family="Arial, sans-serif",

                size=10,

                color="#31485d"

            ),

            bgcolor="rgba(255,255,255,0)",

            traceorder="normal",

            itemsizing="constant"

        ),

        annotations=[

            dict(

                text=(

                    f"<b>{level_total}</b>"

                    "<br>"

                    "<span "
                    "style='font-size:9px'>"
                    "TOTAL"
                    "</span>"

                ),

                x=0.25,

                y=0.50,

                xref="paper",

                yref="paper",

                showarrow=False,

                align="center",

                font=dict(

                    family="Arial, sans-serif",

                    size=15,

                    color="#243c54"

                )

            )

        ]

    )

    st.plotly_chart(

        fig_level,

        use_container_width=True,

        config={

            "displayModeBar": False,

            "responsive": True

        }

    )

    st.html(

        """
            </div>
        </div>
        """

    )

# =========================================================
# LEVEL SUMMARY CARDS
# =========================================================
with r3_right:
    level_columns = st.columns(

        4,

        gap="small"

    )

    level_card_data = [

        (
            "LEVEL 1",
            level_values[0],
            (
                level_values[0]
                / level_total
                * 100
                if level_total
                else 0
            ),
            "#15984d"
        ),

        (
            "LEVEL 2",
            level_values[1],
            (
                level_values[1]
                / level_total
                * 100
                if level_total
                else 0
            ),
            "#2455a4"
        ),

        (
            "LEVEL 3",
            level_values[2],
            (
                level_values[2]
                / level_total
                * 100
                if level_total
                else 0
            ),
            "#d99c00"
        ),

        (
            "LEVEL 4",
            level_values[3],
            (
                level_values[3]
                / level_total
                * 100
                if level_total
                else 0
            ),
            "#d9272e"
        )

    ]

    for i, (

            title,
            value,
            percentage,
            text_color

    ) in enumerate(
        level_card_data
    ):
        with level_columns[i]:
            st.html(

                f"""
                <div
                    class="level-card"
                    style="
                        margin-top:6px;
                    "
                >

                    <div
                        class="level-title"
                        style="
                            color:{text_color};
                        "
                    >
                        {title}
                    </div>


                    <div
                        class="level-value"
                        style="
                            color:{text_color};
                        "
                    >
                        {value}
                    </div>


                    <div
                        class="level-pct"
                    >
                        {percentage:.1f}%
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

        🛡 &nbsp;

        © 2026 Process Safety Management Dashboard

        &nbsp; | &nbsp;

        Pillar: PROCESS SAFETY INCIDENT

    </div>
    """

)

# =========================================================
# PSI GOOGLE SHEET DATA - SHOW BELOW DASHBOARD
# =========================================================

st.markdown(
    """
    <div style="
        margin-top:15px;
        margin-bottom:0;
        padding:9px 12px;
        background:linear-gradient(
            180deg,
            #ffffff,
            #eef6fa
        );
        border:1px solid #c5dce9;
        border-bottom:2px solid #158fd0;
        border-radius:8px 8px 0 0;
        color:#173b5b;
        font-size:12px;
        font-weight:950;
        letter-spacing:.3px;
    ">
        PSI DATA - GOOGLE SHEET
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# GOOGLE SHEET DATA
# 5 ROWS AT A TIME
# ---------------------------------------------------------

PSI_PAGE_SIZE = 5

if "psi_google_sheet_page" not in st.session_state:
    st.session_state.psi_google_sheet_page = 0

psi_total_rows = len(df)

psi_total_pages = max(
    1,
    (psi_total_rows + PSI_PAGE_SIZE - 1)
    // PSI_PAGE_SIZE
)

psi_current_page = st.session_state.psi_google_sheet_page

if psi_current_page >= psi_total_pages:
    psi_current_page = psi_total_pages - 1
    st.session_state.psi_google_sheet_page = psi_current_page

if psi_current_page < 0:
    psi_current_page = 0
    st.session_state.psi_google_sheet_page = 0

psi_start = psi_current_page * PSI_PAGE_SIZE

psi_end = min(
    psi_start + PSI_PAGE_SIZE,
    psi_total_rows
)

psi_page_df = df.iloc[
    psi_start:psi_end
].copy()

# ---------------------------------------------------------
# ALIGNMENT
# Sr No = CENTER
# All other columns = LEFT
# ---------------------------------------------------------

if not psi_page_df.empty:

    # Convert ONLY Sr No to text so Streamlit does not
    # automatically right-align the numeric values.
    first_column = psi_page_df.columns[0]

    psi_page_df[first_column] = (
        psi_page_df[first_column]
        .fillna("")
        .astype(str)
    )

    psi_styled_df = psi_page_df.style

    # All Google Sheet parameters LEFT aligned
    psi_styled_df = psi_styled_df.set_properties(
        subset=list(psi_page_df.columns),
        **{
            "text-align": "left",
            "vertical-align": "middle"
        }
    )

    # ONLY Sr No CENTER aligned
    psi_styled_df = psi_styled_df.set_properties(
        subset=[first_column],
        **{
            "text-align": "center",
            "vertical-align": "middle"
        }
    )

    st.dataframe(
        psi_styled_df,
        use_container_width=True,
        height=255,
        hide_index=True
    )

else:

    st.info("No PSI data found in Google Sheet.")

# ---------------------------------------------------------
# PAGINATION INFORMATION
# Use st.html so <div> is NOT shown as text.
# ---------------------------------------------------------

psi_showing_from = (
    psi_start + 1
    if psi_total_rows > 0
    else 0
)

psi_showing_to = psi_end

st.html(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        height:34px;
        padding:0 10px;
        background:#ffffff;
        border:1px solid #dfe7eb;
        border-top:none;
        font-family:Arial,sans-serif;
        font-size:9px;
        color:#586b7b;
    ">
        <div>
            Showing {psi_showing_from}
            to {psi_showing_to}
            of {psi_total_rows} entries
        </div>

        <div>
            Page {psi_current_page + 1}
            of {psi_total_pages}
        </div>
    </div>
    """
)

# ---------------------------------------------------------
# PREVIOUS / NEXT BUTTONS
# ---------------------------------------------------------

psi_previous_col, psi_next_col = st.columns(
    [1, 1],
    gap="small"
)

with psi_previous_col:
    psi_previous_clicked = st.button(
        "← Previous",
        key="psi_google_sheet_previous",
        disabled=(
                psi_current_page == 0
        ),
        use_container_width=True
    )

with psi_next_col:
    psi_next_clicked = st.button(
        "Next →",
        key="psi_google_sheet_next",
        disabled=(
                psi_current_page
                >= psi_total_pages - 1
        ),
        use_container_width=True
    )

# ---------------------------------------------------------
# CHANGE PAGE
# ---------------------------------------------------------

if psi_previous_clicked:
    st.session_state.psi_google_sheet_page = max(
        0,
        psi_current_page - 1
    )

    st.rerun()

if psi_next_clicked:
    st.session_state.psi_google_sheet_page = min(
        psi_total_pages - 1,
        psi_current_page + 1
    )

    st.rerun()

