import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import html
import re
import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="Operating Procedure | PSM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

#=============================================================
#HEADER CODE
#=============================================================


# ============================================================
# REMOVE STREAMLIT TOP SPACE
# ============================================================

st.markdown("""
<style>

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    background: #ffffff !important;
}

.stApp {
    background: #ffffff !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 100% !important;
    margin-top: -20px !important;
}

footer {
    display: none !important;
    visibility: hidden !important;
}

</style>
""", unsafe_allow_html=True)


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

now = datetime.now(ZoneInfo("Asia/Kolkata"))

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
    width: calc(100% + 10px);
    margin-left: -5px;
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

    padding: 10px;

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

    top: 6px;

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

    left: 0;

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

    height: 9px;

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

                OPERATING PROCEDURE (OP)

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

GOOGLE_SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
SHEET_NAME = "OP"

COL_DEPT = "Department"
COL_AREA = "Area as per selected PT"
COL_PROC = "Procedure Name"
COL_SOP = "Procedure No./SOP No."
COL_CAT = "SOP Category"

CATEGORY_LIST = [
    "Initial Start-up",
    "Normal Start-up / Start-up after Turnaround or Emergency Shutdown",
    "Normal Operation",
    "Normal Shutdown",
    "Emergency Shutdown",
    "Emergency Operation",
]

CATEGORY_COLORS = {
    "Initial Start-up": "#2867a8",
    "Normal Start-up / Start-up after Turnaround or Emergency Shutdown": "#009b95",
    "Normal Operation": "#3e9442",
    "Normal Shutdown": "#d77a08",
    "Emergency Shutdown": "#d92332",
    "Emergency Operation": "#7650a8",
}

CATEGORY_LIGHT = {
    "Initial Start-up": "#f3f8fe",
    "Normal Start-up / Start-up after Turnaround or Emergency Shutdown": "#effafa",
    "Normal Operation": "#f2faf2",
    "Normal Shutdown": "#fff8ed",
    "Emergency Shutdown": "#fff3f4",
    "Emergency Operation": "#f7f2fc",
}

# ============================================================
# GLOBAL CSS
# ============================================================
st.markdown(""" 
<style> 
html, body, [data-testid="stAppViewContainer"] { 
    background: #ffffff !important; 
    font-family: Arial, Helvetica, sans-serif !important; 
    margin: 0 !important; 
    padding: 0 !important; 
} 
[data-testid="stHeader"], [data-testid="stToolbar"], 
[data-testid="stDecoration"] { display: none !important; } 
[data-testid="stAppViewContainer"] > .main, 
[data-testid="stAppViewBlockContainer"], 
[data-testid="stMainBlockContainer"] { 
    padding-top: 0 !important; 
    margin-top: 0 !important; 
} 
.block-container { 
    max-width: 100% !important; 
    padding: 1px 8px 14px 8px !important; 
} 
[data-testid="stVerticalBlock"] { gap: 0.12rem !important; } 

/* Use the same Arial-style font throughout every native Streamlit element */ 
body, button, input, textarea, select, label, p, span, div, table, th, td, .stMarkdown, .stSelectbox { 
    font-family: Arial, Helvetica, sans-serif !important; 
} 
[data-testid="stSelectbox"] label { 
    color: #30435e !important; 
    font-size: 12px !important; 
    font-weight: 700 !important; 
    margin-bottom: 2px !important; 
} 
[data-testid="stSelectbox"] > div > div { 
    border: 1px solid #c9d7e7 !important; 
    border-radius: 8px !important; 
    background: #ffffff !important; 
    min-height: 36px !important; 
} 
iframe {
    border: 0 !important;
} 
</style> 
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data(ttl=120, show_spinner=False)
def load_data():
    url = (
        f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )
    data = pd.read_csv(url)
    data.columns = [str(c).strip() for c in data.columns]
    return data


try:
    df = load_data()
except Exception as e:
    st.error(f'Unable to fetch Google Sheet tab "{SHEET_NAME}": {e}')
    st.stop()

required = [COL_DEPT, COL_AREA, COL_PROC, COL_SOP, COL_CAT]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Required column(s) missing from OP: " + ", ".join(missing))
    st.stop()

for col in required:
    df[col] = df[col].fillna("").astype(str).str.strip()
df = df[df[COL_AREA].ne("")].copy()


def norm_text(value):
    return re.sub(r"\s+", " ", str(value).strip()).lower()


def sop_key(value, procedure_name=""):
    value = str(value).strip()
    return norm_text(value) if value else norm_text(procedure_name)


def distinct_sops(frame):
    if frame.empty:
        return frame.copy()
    temp = frame.copy()
    temp["_sop_key"] = [
        sop_key(sop, proc)
        for sop, proc in zip(temp[COL_SOP], temp[COL_PROC])
    ]
    temp = temp[temp["_sop_key"].ne("")]
    return temp.drop_duplicates("_sop_key")


def unique_clean(series):
    values = series.dropna().astype(str).str.strip()
    values = values[values.ne("")]
    return sorted(values.unique().tolist(), key=lambda x: x.lower())


def category_matches(value, target):
    text = norm_text(value)
    aliases = {
        "Initial Start-up": [
            "initial start-up", "initial startup", "initial start up"
        ],
        "Normal Start-up / Start-up after Turnaround or Emergency Shutdown": [
            "normal start-up", "normal startup", "normal start up",
            "start-up after turnaround", "startup after turnaround",
            "start-up after emergency shutdown", "startup after emergency shutdown"
        ],
        "Normal Operation": ["normal operation"],
        "Normal Shutdown": ["normal shutdown"],
        "Emergency Shutdown": ["emergency shutdown"],
        "Emergency Operation": ["emergency operation"],
    }
    return any(norm_text(alias) in text for alias in aliases[target])


# ============================================================
# FILTERS - ONLY THE TWO SELECT BOXES
# ============================================================
all_departments = unique_clean(df[COL_DEPT])
ALL_DEPARTMENTS = "All Departments"
ALL_AREAS = "All Areas"

dep_col, area_col = st.columns(2, gap="medium")

with dep_col:
    selected_department = st.selectbox(
        "Department",
        [ALL_DEPARTMENTS] + all_departments,
        index=0,
        key="department_selector",
    )

if selected_department == ALL_DEPARTMENTS:
    department_df = df.copy()
else:
    department_df = df[
        df[COL_DEPT].map(norm_text) == norm_text(selected_department)
        ].copy()

filtered_areas = unique_clean(department_df[COL_AREA])
area_options = [ALL_AREAS] + filtered_areas

with area_col:
    selected_area = st.selectbox(
        "Area",
        area_options,
        index=0,
        key="area_selector",
    )

if selected_area == ALL_AREAS:
    area_df = department_df.copy()
else:
    area_df = department_df[
        department_df[COL_AREA].map(norm_text) == norm_text(selected_area)
        ].copy()

area_sops = distinct_sops(area_df)
total_sops = len(area_sops)

# ============================================================
# KPI CALCULATIONS
# First KPI = TOTAL SOPs, followed by six category KPIs
# ============================================================
category_data = []
for category in CATEGORY_LIST:
    cat_df = area_sops[
        area_sops[COL_CAT].map(
            lambda value, target=category: category_matches(value, target)
        )
    ].copy()
    category_data.append((category, len(cat_df)))

# ============================================================
# KPI HTML
# ============================================================
kpi_parts = []

# Total SOP KPI first
kpi_parts.append(f""" 
<div class="kpi-card total-kpi" style="--accent:#173f78;--light:#f4f8fd;"> 
    <div class="kpi-accent"></div> 
    <div class="kpi-label">Total SOPs</div> 
    <div class="kpi-number">{total_sops}</div> 
    <div class="kpi-sub">Distinct SOPs</div> 
</div> 
""")

for category, count in category_data:
    color = CATEGORY_COLORS[category]
    light = CATEGORY_LIGHT[category]
    kpi_parts.append(f""" 
<div class="kpi-card" style="--accent:{color};--light:{light};"> 
    <div class="kpi-accent"></div> 
    <div class="kpi-label">{html.escape(category)}</div> 
    <div class="kpi-number">{count}</div> 
    <div class="kpi-sub">SOPs</div> 
</div> 
""")

kpi_html = f""" 
<style> 
* {{ box-sizing: border-box; }} 
html, body {{ margin:0; padding:0; background:#fff; font-family:Arial, Helvetica, sans-serif !important; }} 
* {{ font-family:Arial, Helvetica, sans-serif !important; }} 
.kpi-wrap {{ width:100%; padding:0; }} 
.kpi-grid {{ 
    display:grid; 
    grid-template-columns:repeat(4,minmax(0,1fr)); 
    gap:10px; 
}} 
.kpi-card {{ 
    position:relative; 
    min-height:108px; 
    border:1px solid #d5dfeb; 
    border-radius:11px; 
    background:var(--light); 
    overflow:hidden; 
    padding:13px 14px 11px 19px; 
    box-shadow:0 3px 10px rgba(23,63,120,.055); 
}} 
.kpi-accent {{ 
    position:absolute; 
    left:0; 
    top:0; 
    bottom:0; 
    width:5px; 
    background:var(--accent); 
}} 
.kpi-label {{ 
    color:var(--accent); 
    font-size:12px; 
    line-height:1.15; 
    font-weight:800; 
    min-height:28px; 
}} 
.kpi-number {{ 
    color:var(--accent); 
    font-size:30px; 
    line-height:1; 
    font-weight:900; 
    margin-top:5px; 
}} 
.kpi-sub {{ 
    color:var(--accent); 
    font-size:9px; 
    font-weight:700; 
    margin-top:3px; 
}} 
@media(max-width:1050px) {{ .kpi-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} }} 
@media(max-width:700px) {{ .kpi-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }} 
</style> 
<div class="kpi-wrap"><div class="kpi-grid">{''.join(kpi_parts)}</div></div> 
"""
st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
components.html(kpi_html, height=240, scrolling=False)

st.markdown("<div style=\"height:12px;\"></div>", unsafe_allow_html=True)


# ============================================================
# SIMPLE SUMMARY TABLES
# ============================================================

def get_area_status(area_name):
    one_df = department_df[
        department_df[COL_AREA].map(norm_text) == norm_text(area_name)
        ].copy()
    one_sops = distinct_sops(one_df)
    total = len(one_sops)
    if total == 0:
        return "To be Started", 0
    categorized = int(one_sops[COL_CAT].map(lambda x: norm_text(x) != "").sum())
    if categorized == 0:
        return "To be Started", total
    if categorized < total:
        return "Pending", total
    return "Completed", total


status_style = {
    "Completed": ("#eaf7ed", "#b8dfc1", "#21733a"),
    "Pending": ("#fff7df", "#efd58a", "#9a6900"),
    "To be Started": ("#fff0f1", "#efb9be", "#b51e27"),
}

summary_area_rows = []
summary_status_rows = []
summary_sop_rows = []

for area in filtered_areas:
    status, sop_count = get_area_status(area)
    bg, border, text = status_style[status]
    summary_area_rows.append(
        f"<tr><td>{html.escape(area)}</td><td>{html.escape(selected_department if selected_department != ALL_DEPARTMENTS else unique_clean(department_df[COL_DEPT])[0] if len(unique_clean(department_df[COL_DEPT])) == 1 else 'Multiple Departments')}</td></tr>"
    )
    summary_status_rows.append(
        f"<tr><td>{html.escape(area)}</td><td><span class='status-pill' style='background:{bg};border-color:{border};color:{text};'>{html.escape(status)}</span></td></tr>"
    )
    summary_sop_rows.append(
        f"<tr><td>{html.escape(area)}</td><td>{sop_count}</td></tr>"
    )

if selected_area != ALL_AREAS:
    # Keep the area table focused on the selected area while retaining the same format.
    pass

summary_html = f""" 
<style> 
* {{ box-sizing:border-box; }} 
html,body {{ margin:0; padding:0; background:#fff; font-family:Arial, Helvetica, sans-serif !important; color:#263b59; }} 
* {{ font-family:Arial, Helvetica, sans-serif !important; }} 
.summary-section {{ 
    width:100%; 
    border:1px solid #d5dfeb; 
    border-radius:12px; 
    background:#fff; 
    padding:12px; 
    box-shadow:0 3px 10px rgba(23,63,120,.045); 
    margin-top:2px; 
    margin-bottom:0; 
    padding-bottom:14px; 
}} 
.summary-heading {{ 
    color:#173f78; 
    font-size:16px; 
    font-weight:850; 
    margin:0 0 9px 0; 
}} 
.summary-grid {{ 
    display:grid; 
    grid-template-columns:repeat(3,minmax(0,1fr)); 
    gap:10px; 
}} 
.summary-card {{ 
    border:1px solid #dce5ee; 
    border-radius:9px; 
    overflow:hidden; 
    background:#fff; 
}} 
.summary-card-title {{ 
    padding:10px 11px; 
    color:#173f78; 
    font-size:12px; 
    font-weight:850; 
    background:#f7faff; 
    border-bottom:1px solid #dce5ee; 
}} 
.summary-body {{ 
    height:190px; 
    overflow-y:auto; 
    overflow-x:hidden; 
    scrollbar-color:#9aabc0 #f4f7fa; 
}} 
.summary-body::-webkit-scrollbar {{ width:7px; }} 
.summary-body::-webkit-scrollbar-track {{ background:#f4f7fa; }} 
.summary-body::-webkit-scrollbar-thumb {{ background:#9aabc0; border-radius:8px; }} 
.summary-table {{ 
    width:100%; 
    border-collapse:collapse; 
    table-layout:fixed; 
    font-size:10px; 
}} 
.summary-table col:first-child {{ width:72%; }} 
.summary-table col:last-child {{ width:28%; }} 
.summary-table th,.summary-table td {{ 
    height:38px; 
    padding:7px 8px; 
    border-bottom:1px solid #e6ecf2; 
    vertical-align:middle; 
    text-align:left; 
    overflow-wrap:anywhere; 
}} 
.summary-table th:last-child,.summary-table td:last-child {{ text-align:center; }} 
.summary-table th {{ color:#2b405c; font-weight:800; background:#f8fafc; position:sticky; top:0; z-index:2; }} 
.summary-table tr:last-child td {{ border-bottom:0; }} 
.status-pill {{ 
    display:inline-block; 
    min-width:78px; 
    padding:4px 7px; 
    border:1px solid; 
    border-radius:6px; 
    text-align:center; 
    font-size:9px; 
    font-weight:800; 
}} 
@media(max-width:850px) {{ .summary-grid {{ grid-template-columns:1fr; }} }} 
</style> 
<div class="summary-section"> 
    <div class="summary-heading">Operating Procedure Summary</div> 
    <div class="summary-grid"> 
        <div class="summary-card"> 
            <div class="summary-card-title">Areas considered for OP Implementation</div> 
            <div class="summary-body"><table class="summary-table"> 
                <colgroup><col><col></colgroup> 
                <thead><tr><th>Area</th><th>Department</th></tr></thead> 
                <tbody>{''.join(summary_area_rows) or '<tr><td colspan="2">No records</td></tr>'}</tbody> 
            </table></div> 
        </div> 
        <div class="summary-card"> 
            <div class="summary-card-title">SOP Categorization Status</div> 
            <div class="summary-body"><table class="summary-table"> 
                <colgroup><col><col></colgroup> 
                <thead><tr><th>Area</th><th>Status</th></tr></thead> 
                <tbody>{''.join(summary_status_rows) or '<tr><td colspan="2">No records</td></tr>'}</tbody> 
            </table></div> 
        </div> 
        <div class="summary-card"> 
            <div class="summary-card-title">Total Nos. of SOPs</div> 
            <div class="summary-body"><table class="summary-table"> 
                <colgroup><col><col></colgroup> 
                <thead><tr><th>Area</th><th>SOPs</th></tr></thead> 
                <tbody>{''.join(summary_sop_rows) or '<tr><td colspan="2">No records</td></tr>'}</tbody> 
            </table></div> 
            <div style="display:flex;justify-content:space-between;padding:8px 8px;border-top:1px solid #e3eaf2;color:#30435e;font-size:10px;font-weight:800;"> 
                <span>Total Distinct SOPs</span><span>{total_sops}</span> 
            </div> 
        </div> 
    </div> 
</div> 
"""
components.html(summary_html, height=325, scrolling=False)

st.markdown("<div style=\"height:14px;\"></div>", unsafe_allow_html=True)

# ============================================================
# CATEGORY-WISE SOP REGISTER
# No top accent, no left accent, and exact equal column alignment
# ============================================================
register_cards = []

for category in CATEGORY_LIST:
    color = CATEGORY_COLORS[category]
    light = CATEGORY_LIGHT[category]

    cat_df = area_df[
        area_df[COL_CAT].map(
            lambda value, target=category: category_matches(value, target)
        )
    ].copy()
    cat_df = distinct_sops(cat_df)

    rows = []
    for _, row in cat_df.iterrows():
        procedure = str(row[COL_PROC]).strip() or "—"
        sop_number = str(row[COL_SOP]).strip() or "—"
        rows.append(
            f""" 
            <tr> 
                <td>{html.escape(procedure)}</td> 
                <td>{html.escape(sop_number)}</td> 
            </tr> 
            """
        )

    body = "".join(rows)
    if not body:
        body = '<tr><td colspan="2" class="no-records">No records for this category</td></tr>'

    register_cards.append(f""" 
    <div class="category-card" style="--accent:{color};--light:{light};"> 
        <div class="category-head"> 
            <div class="category-name">{html.escape(category)}</div> 
            <div class="category-count">{len(cat_df)}</div> 
        </div> 
        <div class="cat-body"> 
            <table class="register-table"> 
                <colgroup><col class="procedure-col"><col class="sop-col"></colgroup> 
                <thead> 
                    <tr><th>Procedure Name</th><th>Procedure No./<br>SOP No.</th></tr> 
                </thead> 
                <tbody>{body}</tbody> 
            </table> 
        </div> 
    </div> 
    """)

register_html = f""" 
<style> 
* {{ box-sizing:border-box; }} 
html,body {{ margin:0; padding:0; background:#fff; font-family:Arial, Helvetica, sans-serif !important; color:#263b59; }} 
* {{ font-family:Arial, Helvetica, sans-serif !important; }} 
.register-section {{ 
    width:100%; 
    border:1px solid #d5dfeb; 
    border-radius:12px; 
    background:#fff; 
    padding:12px; 
    box-shadow:0 3px 10px rgba(23,63,120,.045); 
    margin-top:10px; 
}} 
.register-title {{ 
    color:#173f78; 
    font-size:16px; 
    font-weight:850; 
    margin:0 0 10px 0; 
}} 
.register-grid {{ 
    display:grid; 
    grid-template-columns:repeat(3,minmax(0,1fr)); 
    gap:10px; 
}} 
.category-card {{ 
    height:315px; 
    border:1px solid #d5dfeb; 
    border-radius:10px; 
    background:#fff; 
    overflow:hidden; 
    box-shadow:0 2px 8px rgba(23,63,120,.04); 
}} 
.category-head {{ 
    min-height:52px; 
    padding:8px 10px; 
    display:flex; 
    align-items:center; 
    gap:7px; 
    background:var(--light); 
    border-bottom:1px solid #dce5ee; 
}} 
.category-name {{ 
    flex:1; 
    color:var(--accent); 
    font-size:10.5px; 
    line-height:1.18; 
    font-weight:850; 
}} 
.category-count {{ 
    flex:0 0 auto; 
    min-width:29px; 
    height:24px; 
    padding:0 7px; 
    display:flex; 
    align-items:center; 
    justify-content:center; 
    border-radius:12px; 
    background:#fff; 
    border:1px solid var(--accent); 
    color:var(--accent); 
    font-size:11px; 
    font-weight:900; 
}} 
.cat-body {{ height:263px; overflow-y:auto; scrollbar-color:#8ba0b9 #f2f5f8; }} 
.cat-body::-webkit-scrollbar {{ width:7px; }} 
.cat-body::-webkit-scrollbar-track {{ background:#f2f5f8; }} 
.cat-body::-webkit-scrollbar-thumb {{ background:#8ba0b9; border-radius:8px; }} 
.register-table {{ 
    width:100%; 
    border-collapse:collapse; 
    table-layout:fixed; 
    font-size:9px; 
}} 
.register-table .procedure-col {{ width:75%; }} 
.register-table .sop-col {{ width:25%; }} 
.register-table th,.register-table td {{ 
    border-bottom:1px solid #e2e9f0; 
    border-right:1px solid #e2e9f0; 
    padding:8px 8px; 
    vertical-align:top; 
    overflow-wrap:anywhere; 
}} 
.register-table th:last-child,.register-table td:last-child {{ border-right:0; }} 
.register-table th {{ 
    background:var(--light); 
    color:var(--accent); 
    font-weight:850; 
    line-height:1.2; 
    text-align:left; 
    position:sticky; 
    top:0; 
    z-index:1; 
}} 
.register-table th:last-child,.register-table td:last-child {{ text-align:center; }} 
.register-table td {{ color:#33465f; line-height:1.35; }} 
.register-table td:last-child {{ color:#263d5c; font-weight:750; }} 
.no-records {{ height:220px; text-align:center !important; vertical-align:middle !important; color:#8795a8 !important; font-weight:600 !important; }} 
@media(max-width:1100px) {{ .register-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }} 
@media(max-width:700px) {{ .register-grid {{ grid-template-columns:1fr; }} }} 
</style> 
<div class="register-section"> 
    <div class="register-title">Category-wise SOP Register</div> 
    <div class="register-grid">{''.join(register_cards)}</div> 
</div> 
"""
components.html(register_html, height=690, scrolling=False)
