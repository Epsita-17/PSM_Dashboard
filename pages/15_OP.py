import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import html
import re

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="PSM Digital Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================
GOOGLE_SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"
SHEET_NAME = "OP"

# Required Google Sheet columns
COL_DEPT = "Department"
COL_AREA = "Area as per selected PT"
COL_STATUS = "SOP Categorization"
COL_PROC = "Procedure Name"
COL_SOP = "Procedure No./SOP No."
COL_CAT = "SOP Category"

# ============================================================
# GLOBAL CSS
# ============================================================
st.markdown("""
<style>
html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: #f5f7fb !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    max-width: 100% !important;
    padding: 0 10px 8px 10px !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}

.stSelectbox label {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #23324d !important;
}

.stSelectbox > div > div {
    border-radius: 7px !important;
    min-height: 34px !important;
}

iframe {
    border: 0 !important;
}

@keyframes shine {
    0% { background-position: -300% 0; }
    100% { background-position: 300% 0; }
}

@keyframes softGlow {
    0%, 100% { box-shadow: 0 4px 16px rgba(36, 83, 150, .12); }
    50% { box-shadow: 0 5px 22px rgba(36, 83, 150, .22); }
}

.kpi-card {
    position: relative;
    min-height: 188px;
    border-radius: 11px;
    padding: 15px 17px;
    overflow: hidden;
    border: 1px solid rgba(120,145,180,.20);
    animation: softGlow 3.5s ease-in-out infinite;
}

.kpi-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        115deg,
        transparent 25%,
        rgba(255,255,255,.52) 45%,
        transparent 65%
    );
    background-size: 300% 100%;
    animation: shine 5s linear infinite;
    pointer-events: none;
}

.kpi-blue {
    background: linear-gradient(135deg,#f4f8ff,#edf4ff,#f9fbff);
}
.kpi-green {
    background: linear-gradient(135deg,#f3fbf8,#eaf8f3,#fbfffd);
}
.kpi-purple {
    background: linear-gradient(135deg,#fbf6ff,#f5edff,#fcf9ff);
}

.kpi-head {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 9px;
    color: #163e82;
    font-weight: 800;
    font-size: 13px;
}

.kpi-icon {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex: 0 0 auto;
}

.kpi-number {
    position: relative;
    z-index: 2;
    font-size: 30px;
    font-weight: 900;
    line-height: 1;
    margin-top: 4px;
    color: #17294b;
}

.kpi-subtitle {
    position: relative;
    z-index: 2;
    font-size: 11px;
    color: #202a3a;
    margin-top: 4px;
    font-weight: 600;
}

.kpi-rule {
    position: relative;
    z-index: 2;
    height: 1px;
    background: rgba(40,60,90,.17);
    margin: 10px 0 7px;
}

.kpi-section {
    position: relative;
    z-index: 2;
    font-size: 11px;
    color: #173d7d;
    font-weight: 800;
    margin-bottom: 4px;
}

.kpi-area {
    position: relative;
    z-index: 2;
    font-size: 10.5px;
    color: #28364e;
    padding: 2px 0 2px 15px;
    line-height: 1.45;
}

.kpi-area::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #3973cf;
    position: absolute;
    left: 1px;
    top: 7px;
}

.status-table,
.sop-table {
    position: relative;
    z-index: 2;
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
}

.status-table th,
.status-table td,
.sop-table th,
.sop-table td {
    border-bottom: 1px solid rgba(80,100,130,.13);
    padding: 6px 4px;
    text-align: left;
}

.status-table th,
.sop-table th {
    font-weight: 800;
    color: #202c40;
}

.status-table td:last-child,
.status-table th:last-child,
.sop-table td:last-child,
.sop-table th:last-child {
    text-align: center;
}

.status-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 7px;
    font-size: 10px;
    font-weight: 700;
    min-width: 86px;
    text-align: center;
}

.completed {
    background: linear-gradient(135deg,#e3f4df,#d6efd1);
    color: #245b28;
}
.ongoing {
    background: linear-gradient(135deg,#fff0c9,#ffe8b0);
    color: #8a5a00;
}
.tostart {
    background: linear-gradient(135deg,#fff0d7,#ffe4bb);
    color: #9a5c0a;
}

.section-panel {
    border: 1px solid rgba(110,125,150,.18);
    border-radius: 11px;
    background: rgba(255,255,255,.78);
    box-shadow: 0 2px 12px rgba(40,55,80,.07);
    overflow: hidden;
}

.section-title {
    color: #163d80;
    font-size: 13px;
    font-weight: 900;
    margin: 0 0 8px 2px;
}

.chart-box {
    min-height: 250px;
    padding: 12px 14px;
}

.register-panel {
    padding: 10px 10px 8px;
}

.category-card {
    border: 1px solid rgba(100,120,145,.17);
    border-radius: 10px;
    overflow: hidden;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(40,55,80,.07);
    height: 295px;
}

.category-head {
    min-height: 48px;
    padding: 7px 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid rgba(90,110,140,.15);
}

.category-name {
    flex: 1;
    font-size: 9px;
    line-height: 1.15;
    font-weight: 900;
}

.category-count {
    min-width: 25px;
    height: 23px;
    padding: 0 7px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 900;
    box-shadow: inset 0 0 8px rgba(255,255,255,.55);
}

.cat-blue .category-head { background: linear-gradient(135deg,#f3f7ff,#e9f1ff); color:#214f9b; }
.cat-blue .category-count { background:#6aa7ef; color:#103b7b; }

.cat-teal .category-head { background: linear-gradient(135deg,#f1fbfa,#e7f8f5); color:#18877f; }
.cat-teal .category-count { background:#75d0cc; color:#0e6963; }

.cat-green .category-head { background: linear-gradient(135deg,#f4fbf0,#e9f7e3); color:#398333; }
.cat-green .category-count { background:#92d77e; color:#286b21; }

.cat-orange .category-head { background: linear-gradient(135deg,#fff8ed,#fff0da); color:#cf7318; }
.cat-orange .category-count { background:#f7b45f; color:#8b4a00; }

.cat-red .category-head { background: linear-gradient(135deg,#fff4f4,#ffe9e9); color:#c73636; }
.cat-red .category-count { background:#ef8e8e; color:#8d2222; }

.cat-purple .category-head { background: linear-gradient(135deg,#fbf4ff,#f3e9ff); color:#70409b; }
.cat-purple .category-count { background:#b58de0; color:#542a7f; }

.table-head {
    display: grid;
    grid-template-columns: 1fr 74px;
    font-size: 8px;
    font-weight: 900;
    color: #26364d;
    background: rgba(225,232,242,.65);
    border-bottom: 1px solid rgba(90,110,140,.14);
}

.table-head div {
    padding: 6px 7px;
}

.table-head div:last-child {
    text-align: center;
    border-left: 1px solid rgba(90,110,140,.12);
}

.cat-body {
    height: 236px;
    overflow-y: auto;
}

.proc-row {
    display: grid;
    grid-template-columns: 1fr 74px;
    min-height: 54px;
    border-bottom: 1px solid rgba(90,110,140,.10);
    font-size: 8px;
    line-height: 1.35;
    color: #263248;
}

.proc-name {
    padding: 6px 7px;
}

.proc-no {
    padding: 6px 5px;
    border-left: 1px solid rgba(90,110,140,.10);
    font-weight: 700;
    text-align: center;
}

.no-records {
    height: 230px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #394457;
    font-size: 10px;
    text-align: center;
}

.no-records-icon {
    font-size: 35px;
    opacity: .62;
    margin-bottom: 7px;
}

.note {
    text-align: center;
    font-size: 10px;
    color: #566173;
    margin-top: 7px;
}

.error-box {
    padding: 16px;
    border-radius: 10px;
    background: #fff3f3;
    border: 1px solid #f0b9b9;
    color: #8b2222;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER - SAME HEADER CODE / DESIGN FROM Header.docx
# ============================================================
BASE_DIR = Path(__file__).resolve().parent

def image_to_base64(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        return ""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return ""

logo_path = BASE_DIR / "jsw_jfe_logo.jpg"
logo_base64 = image_to_base64(logo_path)
if not logo_base64:
    logo_base64 = ""

now = datetime.now(ZoneInfo("Asia/Kolkata"))
current_date = now.strftime("%d %b %Y").upper()
current_time = now.strftime("%I:%M %p")

header_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
.psm-header {
 position: relative;
 width: 100%;
 height: 90px;
 overflow: hidden;
 background: linear-gradient(90deg,#031d34 0%,#052b49 42%,#07385c 74%,#052b49 100%);
 border-radius: 7px;
 box-shadow: 0 3px 9px rgba(0,0,0,0.18);
}
.psm-left {
 position:absolute; left:0; top:0; width:100%; height:95px;
 display:flex; align-items:center; padding-left:4px;
 box-sizing:border-box; z-index:20; pointer-events:none;
}
.logo-panel {
 width:195px; height:68px; background:#fff; border-radius:5px; padding:4px;
 display:flex; align-items:center; justify-content:center; flex-shrink:0;
 box-sizing:border-box; box-shadow:0 3px 9px rgba(0,0,0,0.20);
 position:relative; top:-6px; left:5px;
}
.company-logo {
 width:100%; height:100%; object-fit:contain; object-position:center; display:block;
}
.vertical-line {
 width:2px; height:83px; background:rgba(255,255,255,0.65);
 margin-left:18px; margin-right:20px; flex-shrink:0;
}
.title-area {
 position:absolute; left:50%; top:0; height:95px;
 display:flex; flex-direction:column; justify-content:center; align-items:center;
 text-align:center; min-width:max-content; box-sizing:border-box;
 transform:translateX(-50%);
}
.main-title {
 color:#fff; font-family:"Arial Narrow","Roboto Condensed",Arial,sans-serif;
 font-size:27px; font-weight:900; line-height:1; letter-spacing:.3px;
 white-space:nowrap; margin:0; padding:0;
}
.main-title-orange { color:#f28c00; }
.subtitle {
 color:#fff; font-family:Arial,sans-serif; font-size:12px; font-weight:400;
 letter-spacing:3.6px; margin-top:8px; line-height:1; white-space:nowrap;
}
.tagline {
 color:rgba(255,255,255,.82); font-family:Arial,sans-serif; font-size:7px;
 font-weight:500; letter-spacing:2.2px; margin-top:6px; line-height:1; white-space:nowrap;
}
.psm-right {
 position:absolute; right:16px; top:0; width:15%; height:95px;
 display:flex; flex-direction:column; justify-content:center; align-items:flex-end;
 text-align:right; color:#fff; z-index:30; padding-left:18px; box-sizing:border-box;
}
.psm-right::before {
 content:""; position:absolute; left:15px; top:6px; width:2px; height:83px;
 background:rgba(255,255,255,.65);
}
.date {
 color:rgba(255,255,255,.95); font-family:Arial,sans-serif; font-size:11px;
 font-weight:400; letter-spacing:.7px; line-height:1; margin:0; padding:0;
}
.time {
 color:#fff; font-family:"Arial Narrow","Roboto Condensed",Arial,sans-serif;
 font-size:22px; font-weight:800; margin-top:4px; line-height:1; padding:0;
}
.right-line {
 width:80px; height:2px; background:rgba(255,255,255,.75); margin-top:7px; flex-shrink:0;
}
.orange-bar {
 position:absolute; left:0; bottom:0; width:100%; height:7px; background:#f28c00; z-index:50;
}
</style>
</head>
<body>
<div class="psm-header">
 <div class="psm-left">
  <div class="logo-panel">
   <img class="company-logo" src="data:image/jpeg;base64,LOGO_IMAGE_BASE64" alt="JSW JFE Steel Limited">
  </div>
  <div class="vertical-line"></div>
  <div class="title-area">
   <div class="main-title">OPERATING PROCEDURE (OP)</div>
   <div class="subtitle">PSM DIGITAL DASHBOARD</div>
   <div class="tagline">PEOPLE &nbsp; | &nbsp; PROCESS &nbsp; | &nbsp; RISK &nbsp; | &nbsp; COMPLIANCE</div>
  </div>
 </div>
 <div class="psm-right">
  <div class="date">CURRENT_DATE_VALUE</div>
  <div class="time">CURRENT_TIME_VALUE</div>
  <div class="right-line"></div>
 </div>
 <div class="orange-bar"></div>
</div>
</body>
</html>
"""

header_html = header_html.replace("LOGO_IMAGE_BASE64", logo_base64)
header_html = header_html.replace("CURRENT_DATE_VALUE", current_date)
header_html = header_html.replace("CURRENT_TIME_VALUE", current_time)
st.components.v1.html(header_html, height=100, scrolling=False)

# ============================================================
# GOOGLE SHEET DATA FETCH
# ============================================================
@st.cache_data(ttl=120, show_spinner=False)
def load_data():
    url = (
        f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.markdown(
        f'<div class="error-box">Unable to fetch Google Sheet "{SHEET_NAME}". '
        f'Please check that the sheet is shared for viewing and the tab name is OP.<br>'
        f'Details: {html.escape(str(e))}</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# CLEAN / NORMALIZE DATA
# ============================================================
required = [COL_DEPT, COL_AREA, COL_STATUS, COL_PROC, COL_SOP, COL_CAT]
missing = [c for c in required if c not in df.columns]

if missing:
    st.markdown(
        '<div class="error-box">Required column(s) missing from sheet OP: '
        + ", ".join(html.escape(x) for x in missing)
        + '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

for c in required:
    df[c] = df[c].fillna("").astype(str).str.strip()

df = df[df[COL_AREA].ne("")].copy()

def unique_clean(series):
    vals = series.dropna().astype(str).str.strip()
    vals = vals[vals.ne("")]
    return sorted(vals.unique().tolist(), key=lambda x: x.lower())

areas = unique_clean(df[COL_AREA])

if not areas:
    st.warning("No area data found in sheet OP.")
    st.stop()

ALL_AREAS = "All Areas"
area_options = [ALL_AREAS] + areas

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def norm_text(value):
    return re.sub(r"\s+", " ", str(value).strip()).lower()

def sop_key(value, procedure_name=""):
    value = str(value).strip()
    if value:
        return norm_text(value)
    return norm_text(procedure_name)

def distinct_sops(frame):
    if frame.empty:
        return frame.copy()
    temp = frame.copy()
    temp["_sop_key"] = [
        sop_key(s, p)
        for s, p in zip(temp[COL_SOP], temp[COL_PROC])
    ]
    temp = temp[temp["_sop_key"].ne("")]
    return temp.drop_duplicates("_sop_key")

def contains_any(text, words):
    t = norm_text(text)
    return any(w in t for w in words)

def category_matches(value, target):
    t = norm_text(value)
    aliases = {
        "Initial Start-up": [
            "initial start-up", "initial startup", "initial start up"
        ],
        "Normal Start-up / Start-up after Turnaround or Emergency Shutdown": [
            "normal start-up",
            "normal startup",
            "start-up after turnaround",
            "startup after turnaround",
            "start-up after emergency shutdown",
            "startup after emergency shutdown",
        ],
        "Normal Operation": ["normal operation"],
        "Shutdown": [
            "shutdown",
            "normal shutdown",
            "emergency shutdown"
        ],
        "Normal Shutdown": ["normal shutdown"],
        "Emergency Shutdown": ["emergency shutdown"],
        "Emergency Operation": ["emergency operation"],
    }
    return any(norm_text(a) in t for a in aliases[target])

def has_normal(value):
    t = norm_text(value)
    return (
        "normal operation" in t
        or "normal shutdown" in t
        or "normal start-up" in t
        or "normal startup" in t
        or "normal start up" in t
    )

def has_shutdown(value):
    t = norm_text(value)
    return (
        "normal shutdown" in t
        or "emergency shutdown" in t
        or "shutdown" in t
    )

# ============================================================
# AREA SELECTOR
# ============================================================
selected_area = st.selectbox(
    "Select Area",
    area_options,
    index=0,
    key="area_selector"
)

if selected_area == ALL_AREAS:
    area_df = df.copy()
else:
    area_df = df[df[COL_AREA].map(norm_text) == norm_text(selected_area)].copy()

area_sops = distinct_sops(area_df)

# ============================================================
# KPI DATA
# ============================================================
total_areas = len(areas)
total_sops = len(area_sops)

# Categorization status is calculated from SOP Category:
# no categorized SOP -> To be Started
# some but not all categorized -> Ongoing
# all SOPs categorized -> Completed
categorized = area_sops[COL_CAT].map(lambda x: norm_text(x) != "")
categorized_count = int(categorized.sum())

if total_sops == 0:
    status = "To be Started"
elif categorized_count == 0:
    status = "To be Started"
elif categorized_count < total_sops:
    status = "Ongoing"
else:
    status = "Completed"

status_class = {
    "Completed": "completed",
    "Ongoing": "ongoing",
    "To be Started": "tostart"
}[status]

# Build the area list used inside KPI card 1.
area_lines = "".join(
    f'<div class="area">{html.escape(a)}</div>'
    for a in areas
)

# ============================================================
# KPI ROWS FOR INDIVIDUAL AREA / ALL AREAS
# ============================================================
def get_area_kpi_values(area_name):
    one_df = df[
        df[COL_AREA].map(norm_text) == norm_text(area_name)
    ].copy()
    one_sops = distinct_sops(one_df)
    one_total = len(one_sops)

    if one_total == 0:
        one_status = "To be Started"
    else:
        one_categorized = one_sops[COL_CAT].map(
            lambda x: norm_text(x) != ""
        )
        one_count = int(one_categorized.sum())

        if one_count == 0:
            one_status = "To be Started"
        elif one_count < one_total:
            one_status = "Ongoing"
        else:
            one_status = "Completed"

    return one_status, one_total

if selected_area == ALL_AREAS:
    all_status_rows = []
    all_sop_rows = []

    for a in areas:
        a_status, a_sop_total = get_area_kpi_values(a)

        a_status_class = {
            "Completed": "completed",
            "Ongoing": "ongoing",
            "To be Started": "tostart"
        }[a_status]

        all_status_rows.append(
            f'<tr>'
            f'<td>{html.escape(a)}</td>'
            f'<td><span class="pill {a_status_class}">'
            f'{html.escape(a_status)}</span></td>'
            f'</tr>'
        )

        all_sop_rows.append(
            f'<tr>'
            f'<td>{html.escape(a)}</td>'
            f'<td>{a_sop_total}</td>'
            f'</tr>'
        )

    kpi2_rows = "".join(all_status_rows)
    kpi3_rows = "".join(all_sop_rows)
else:
    kpi2_rows = (
        f'<tr>'
        f'<td>{html.escape(selected_area)}</td>'
        f'<td><span class="pill {status_class}">'
        f'{html.escape(status)}</span></td>'
        f'</tr>'
    )

    kpi3_rows = (
        f'<tr>'
        f'<td>{html.escape(selected_area)}</td>'
        f'<td>{total_sops}</td>'
        f'</tr>'
    )

# ============================================================
# TOP 3 KPI CARDS
# IMPORTANT: These cards are rendered with components.html.
# This prevents Streamlit from showing the HTML source as text.
# ============================================================
kpi_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:transparent; font-family:Arial,sans-serif; }}
@keyframes shine {{
    0% {{ background-position:-300% 0; }}
    100% {{ background-position:300% 0; }}
}}
@keyframes glow {{
    0%,100% {{ box-shadow:0 4px 16px rgba(40,80,140,.12); }}
    50% {{ box-shadow:0 5px 24px rgba(40,80,140,.24); }}
}}
.grid {{
    width:100%;
    display:grid;
    grid-template-columns:1fr 1.08fr 1.08fr;
    gap:14px;
}}
.card {{
    position:relative;
    height:230px;
    border-radius:13px;
    padding:16px 18px 14px 18px;
    overflow:hidden;
    border:1px solid rgba(35,65,100,.22);
    box-shadow:
        0 4px 0 rgba(20,45,75,.14),
        0 10px 22px rgba(20,45,75,.17),
        inset 0 2px 0 rgba(255,255,255,.96),
        inset 0 -2px 5px rgba(40,60,90,.08);
}}
.card:before {{
    content:"";
    position:absolute;
    left:0;
    top:0;
    right:0;
    height:6px;
    border-radius:13px 13px 0 0;
}}
.card:after {{
    content:"";
    position:absolute;
    left:-12%;
    top:-65%;
    width:48%;
    height:230%;
    transform:rotate(27deg);
    background:linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,.08) 30%,
        rgba(255,255,255,.52) 50%,
        rgba(255,255,255,.08) 70%,
        transparent 100%
    );
    pointer-events:none;
}}
.blue {{
    background:
        radial-gradient(circle at 92% 15%,rgba(57,115,207,.22),transparent 30%),
        radial-gradient(circle at 10% 100%,rgba(93,156,235,.16),transparent 35%),
        linear-gradient(145deg,#e7f2ff 0%,#cfe3fb 48%,#f5f9ff 100%);
}}
.blue:before {{ background:linear-gradient(90deg,#245cae,#4d8fe0,#245cae); }}

.green {{
    background:
        radial-gradient(circle at 92% 15%,rgba(67,165,107,.22),transparent 30%),
        radial-gradient(circle at 10% 100%,rgba(93,190,132,.16),transparent 35%),
        linear-gradient(145deg,#e5f8ed 0%,#cdebd9 48%,#f5fcf8 100%);
}}
.green:before {{ background:linear-gradient(90deg,#2d8755,#55b878,#2d8755); }}

.purple {{
    background:
        radial-gradient(circle at 92% 15%,rgba(128,84,184,.22),transparent 30%),
        radial-gradient(circle at 10% 100%,rgba(164,119,211,.16),transparent 35%),
        linear-gradient(145deg,#f3e9fc 0%,#e3d2f5 48%,#fbf8ff 100%);
}}
.purple:before {{ background:linear-gradient(90deg,#68419b,#9164c3,#68419b); }}

.head {{
    position:relative;
    z-index:2;
    display:flex;
    align-items:center;
    gap:9px;
    color:#163e82;
    font-size:16px;
    font-weight:900;
}}
.icon {{
    width:40px;height:40px;border-radius:11px;
    display:flex;align-items:center;justify-content:center;
    font-size:27px;flex:0 0 auto;
    background:rgba(255,255,255,.55);
    border:1px solid rgba(255,255,255,.80);
    box-shadow:
        0 3px 8px rgba(30,55,90,.16),
        inset 0 1px 0 rgba(255,255,255,.96);
}}
.number {{
    position:relative;z-index:2;
    color:#17294b;
    font-size:40px;
    line-height:1;
    font-weight:900;
    margin-top:4px;
}}
.sub {{
    position:relative;z-index:2;
    color:#202a3a;
    font-size:14px;
    font-weight:700;
    margin-top:4px;
}}
.rule {{
    position:relative;z-index:2;
    height:1px;
    background:rgba(40,60,90,.17);
    margin:10px 0 7px;
}}
.section {{
    position:relative;z-index:2;
    color:#173d7d;
    font-size:13px;
    font-weight:800;
    margin-bottom:5px;
}}
.area {{
    position:relative;z-index:2;
    color:#28364e;
    font-size:12px;
    line-height:1.5;
    padding:2px 0 2px 15px;
}}
.area:before {{
    content:"";
    position:absolute;
    left:1px;top:7px;
    width:6px;height:6px;border-radius:50%;
    background:#3973cf;
}}
.kpi-scroll {{
    position:relative;
    z-index:2;
    height:112px;
    max-height:112px;
    overflow-y:scroll !important;
    overflow-x:hidden !important;
    padding-right:7px;
    scrollbar-width:auto;
    scrollbar-color:#6f829d rgba(255,255,255,.45);
}}
.kpi-scroll::-webkit-scrollbar {{
    width:8px !important;
    display:block !important;
}}
.kpi-scroll::-webkit-scrollbar-track {{
    background:rgba(255,255,255,.48);
    border-radius:8px;
}}
.kpi-scroll::-webkit-scrollbar-thumb {{
    background:#71839c;
    border-radius:8px;
    border:1px solid rgba(255,255,255,.6);
}}
.kpi-scroll::-webkit-scrollbar-thumb:hover {{
    background:#4e6685;
}}
table {{
    position:relative;z-index:2;
    width:100%;
    border-collapse:collapse;
    font-size:12px;
}}
th,td {{
    padding:8px 5px;
    border-bottom:1px solid rgba(80,100,130,.13);
    text-align:left;
}}
th {{ font-weight:800;color:#202c40; }}
td:last-child, th:last-child {{ text-align:center; }}
.pill {{
    display:inline-block;
    min-width:86px;
    padding:6px 15px;
    border-radius:7px;
    text-align:center;
    font-size:12px;
    font-weight:700;
}}
.completed {{ background:linear-gradient(135deg,#e3f4df,#d6efd1);color:#245b28; }}
.ongoing {{ background:linear-gradient(135deg,#fff0c9,#ffe8b0);color:#8a5a00; }}
.tostart {{ background:linear-gradient(135deg,#fff0d7,#ffe4bb);color:#9a5c0a; }}
.total-line {{
    position:relative;z-index:2;
    margin-top:10px;
    padding:9px 4px 0;
    border-top:1px solid rgba(80,100,130,.13);
    display:flex;
    justify-content:space-between;
    font-size:10px;
    font-weight:800;
    color:#263248;
}}
</style>
</head>
<body>
<div class="grid">

<div class="card blue">
    <div class="head">
        <div class="icon">⌖</div>
        <div>1. Areas under PSM</div>
    </div>
    <div class="number">{total_areas}</div>
    <div class="sub">Total Areas</div>
    <div class="rule"></div>
    <div class="kpi-scroll">
        <div class="section">Areas Considered</div>
        {area_lines}
    </div>
</div>

<div class="card green">
    <div class="head">
        <div class="icon">☑</div>
        <div>2. SOP Categorization Status</div>
    </div>
    <div style="height:12px;"></div>
    <div class="kpi-scroll">
        <table>
            <thead>
                <tr>
                    <th>Area as per Selected PT</th>
                    <th>SOP Categorization Status</th>
                </tr>
            </thead>
            <tbody>
                {kpi2_rows}
            </tbody>
        </table>
    </div>
</div>

<div class="card purple">
    <div class="head">
        <div class="icon">▤</div>
        <div>3. Total Nos. of SOPs</div>
    </div>
    <div style="height:12px;"></div>
    <div class="kpi-scroll">
        <table>
            <thead>
                <tr>
                    <th>Area as per Selected PT</th>
                    <th>No. of SOPs</th>
                </tr>
            </thead>
            <tbody>
                {kpi3_rows}
            </tbody>
        </table>
    </div>
    <div class="total-line">
        <span>Total Distinct SOPs</span>
        <span>{total_sops}</span>
    </div>
</div>

</div>
</body>
</html>
"""

st.components.v1.html(kpi_html, height=250, scrolling=False)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ============================================================
# CATEGORY ANALYSIS
# ============================================================
normal_sops = area_sops[
    area_sops[COL_CAT].map(has_normal)
].copy()

shutdown_sops = area_sops[
    area_sops[COL_CAT].map(has_shutdown)
].copy()

normal_count = len(distinct_sops(normal_sops))
shutdown_count = len(distinct_sops(shutdown_sops))

both_sops = area_sops[
    area_sops[COL_CAT].map(lambda x: has_normal(x) and has_shutdown(x))
].copy()
both_count = len(distinct_sops(both_sops))

# ============================================================
# MIDDLE LEFT: VENN-STYLE DISTINCT SOP OVERVIEW
# ============================================================

# ============================================================
# 4. SOP CATEGORIZATION OVERVIEW + CATEGORY BAR GRAPH
# Clean white 3D presentation
# ============================================================

def _sop_has_category(value, category):
    return category_matches(value, category)

normal_sops = set()
shutdown_sops = set()

for _, row in area_sops.iterrows():
    sop_no = norm_text(row[COL_SOP])
    if not sop_no:
        continue
    cat_value = row[COL_CAT]
    if _sop_has_category(cat_value, "Normal Operation"):
        normal_sops.add(sop_no)
    if _sop_has_category(cat_value, "Shutdown") or _sop_has_category(cat_value, "Normal Shutdown"):
        shutdown_sops.add(sop_no)

both_sops = normal_sops.intersection(shutdown_sops)
normal_total = len(normal_sops)
shutdown_total = len(shutdown_sops)
both_count = len(both_sops)

bar_categories = [
    ("Normal Operation", len(normal_sops), "#4d8fe0"),
    ("Shutdown", len(shutdown_sops), "#e85b62"),
    ("Both (Normal & Shutdown)", both_count, "#a06bd1"),
    ("Initial Start-up", 0, "#70a7df"),
    ("Normal Start-up / Start-up after Turnaround or Emergency Shutdown", 0, "#e0a13c"),
    ("Normal Shutdown", 0, "#d99148"),
    ("Emergency Shutdown", 0, "#d45c68"),
    ("Emergency Operation", 0, "#8b70b4"),
]

for i, (label, _, color) in enumerate(bar_categories):
    if label in ("Normal Operation", "Shutdown", "Both (Normal & Shutdown)"):
        continue
    count = sum(
        1 for _, row in area_sops.iterrows()
        if _sop_has_category(row[COL_CAT], label)
    )
    bar_categories[i] = (label, count, color)

max_bar = max([v for _, v, _ in bar_categories] + [1])
bar_scale = max(25, ((max_bar + 4) // 5) * 5)

overview_rows = f"""
<div class="overview-summary-row">
    <div class="summary-label normal-label"><span class="dot normal-dot"></span><span>Normal Operation</span></div>
    <div class="summary-value">{normal_total}</div>
    <div class="summary-label shutdown-label"><span class="dot shutdown-dot"></span><span>Shutdown</span></div>
    <div class="summary-value">{shutdown_total}</div>
</div>
<div class="overview-summary-row">
    <div class="summary-label both-label"><span class="dot both-dot"></span><span>Both (Normal &amp; Shutdown)</span></div>
    <div class="summary-value both-value">{both_count}</div>
    <div class="summary-label total-label"><span>Total Distinct SOPs</span></div>
    <div class="summary-value total-value">{len(area_sops)}</div>
</div>
"""

bar_rows = ""
for label, value, color in bar_categories:
    width = (value / bar_scale) * 100 if bar_scale else 0
    label_html = html.escape(label)
    if label == "Normal Start-up / Start-up after Turnaround or Emergency Shutdown":
        label_html = "Normal Start-up /<br>Start-up after Turnaround or<br>Emergency Shutdown"
    bar_rows += f"""
    <div class="bar-row">
        <div class="bar-label">{label_html}</div>
        <div class="bar-track">
            <div class="bar-fill" style="width:{width:.2f}%;background:linear-gradient(90deg,{color},{color}cc);"></div>
        </div>
        <div class="bar-value">{value}</div>
    </div>
    """

overview_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ box-sizing:border-box; }}
html,body {{ margin:0;padding:0;background:transparent;font-family:Arial,sans-serif;color:#172b4d; }}
.wrapper {{ width:100%;display:grid;grid-template-columns:1fr 1.06fr;gap:14px; }}
.panel {{
    height:355px;border-radius:14px;border:1px solid #dce5ef;
    background:
        radial-gradient(circle at 94% 8%,rgba(105,150,205,.10),transparent 22%),
        linear-gradient(145deg,#ffffff 0%,#fbfdff 72%,#f4f8fc 100%);
    box-shadow:0 3px 0 rgba(35,70,105,.08),0 9px 22px rgba(35,70,105,.13),inset 0 1px 0 rgba(255,255,255,.98);
    overflow:hidden;padding:15px 18px 14px;
}}
.title {{ font-size:16px;font-weight:900;color:#183d78;margin-bottom:7px; }}
.title-line {{ width:95px;height:4px;border-radius:4px;background:linear-gradient(90deg,#f0a13a,#f8c56d);margin-bottom:12px; }}
.overview-body {{ display:grid;grid-template-columns:1.08fr .72fr;gap:30px;height:275px;align-items:center; }}
.venn {{ position:relative;height:260px;transform:translateX(-4px); }}
.circle {{
    position:absolute;top:25px;width:178px;height:178px;border-radius:50%;
    display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-weight:800;
}}
.normal-circle {{
    left:8px;border:2px solid #58a3e8;
    background:radial-gradient(circle at 38% 30%,rgba(102,174,238,.30),rgba(102,174,238,.10));
    box-shadow:0 8px 16px rgba(64,130,194,.14),inset 0 1px 0 rgba(255,255,255,.8);color:#12609d;
}}
.shutdown-circle {{
    left:145px;border:2px solid #f06c70;
    background:radial-gradient(circle at 62% 30%,rgba(240,108,112,.28),rgba(240,108,112,.10));
    box-shadow:0 8px 16px rgba(194,74,78,.13),inset 0 1px 0 rgba(255,255,255,.8);color:#c73636;
}}
.overlap {{ position:absolute;left:132px;top:96px;width:68px;text-align:center;z-index:4;color:#713a9a;font-size:27px;font-weight:900; }}
.circle-name {{ font-size:12px;line-height:1.18;max-width:100px; }}
.circle-number {{ font-size:29px;line-height:1;margin-top:8px; }}
.summary {{
    border-radius:11px;background:linear-gradient(145deg,#ffffff,#f7fbff);
    border:1px solid #dbe5ef;box-shadow:0 5px 14px rgba(40,70,100,.10),inset 0 1px 0 #fff;
    padding:10px 12px;
}}
.summary-head {{
    display:grid;grid-template-columns:1fr 48px 1fr 42px;gap:5px;
    font-size:10px;font-weight:900;color:#30405a;padding-bottom:7px;border-bottom:1px solid #dce5ee;
}}
.summary-head span:nth-child(2),.summary-head span:nth-child(4) {{ text-align:center; }}
.overview-summary-row {{
    display:grid;grid-template-columns:1fr 40px 1fr 40px;gap:5px;align-items:center;
    min-height:48px;border-bottom:1px solid #e2e9f0;font-size:10px;
}}
.summary-label {{ display:flex;align-items:center;gap:6px;font-weight:700; }}
.summary-value {{ text-align:center;font-size:16px;font-weight:900; }}
.normal-label {{ color:#1765a2; }} .shutdown-label {{ color:#c63b3f; }}
.both-label {{ color:#75429b; }} .both-value {{ color:#75429b; }}
.total-label {{ color:#193f7e;font-weight:900; }} .total-value {{ color:#193f7e;font-size:18px; }}
.dot {{ width:7px;height:7px;border-radius:50%;flex:0 0 auto; }}
.normal-dot {{ background:#4d8fe0; }} .shutdown-dot {{ background:#e85b62; }} .both-dot {{ background:#a06bd1; }}

.chart {{ height:295px;padding-top:3px; }}
.bar-row {{ display:grid;grid-template-columns:210px 1fr 28px;gap:8px;align-items:center;min-height:31px; }}
.bar-label {{ text-align:right;font-size:9px;line-height:1.08;font-weight:700;color:#263a57; }}
.bar-track {{ height:17px;border-radius:4px;background:linear-gradient(180deg,#edf2f7,#e4eaf0);box-shadow:inset 0 1px 2px rgba(35,60,90,.10);overflow:hidden; }}
.bar-fill {{ height:100%;border-radius:4px;box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 2px 4px rgba(35,60,90,.12); }}
.bar-value {{ font-size:10px;font-weight:900;color:#203451; }}
.axis {{ margin-left:218px;margin-right:28px;margin-top:4px;border-top:1px solid #d7e0e9;padding-top:6px;text-align:center;font-size:9px;font-weight:800;color:#3d4b60; }}
</style>
</head>
<body>
<div class="wrapper">

<div class="panel">
    <div class="title">4. SOP Categorization Overview (Distinct SOPs)</div>
    <div class="title-line"></div>
    <div class="overview-body">
        <div class="venn">
            <div class="circle normal-circle">
                <div class="circle-name">Normal<br>Operation</div>
                <div class="circle-number">{normal_total}</div>
            </div>
            <div class="circle shutdown-circle">
                <div class="circle-name">Shutdown</div>
                <div class="circle-number">{shutdown_total}</div>
            </div>
            <div class="overlap">{both_count}</div>
        </div>
        <div class="summary">
            <div class="summary-head">
                <span>Category</span><span>No.</span><span></span><span>SOPs</span>
            </div>
            {overview_rows}
        </div>
    </div>
</div>

<div class="panel">
    <div class="title">SOPs by Category (Distinct SOPs)</div>
    <div class="title-line" style="background:linear-gradient(90deg,#39b87a,#79d2a5);"></div>
    <div class="chart">
        {bar_rows}
        <div class="axis">No. of SOPs</div>
    </div>
</div>

</div>
</body>
</html>
"""

st.components.v1.html(overview_html, height=380, scrolling=False)

# BOTTOM REGISTER
# ============================================================
st.markdown(
    '<div class="section-title">5. Category-wise SOP Register</div>',
    unsafe_allow_html=True
)

category_list = [
    ("Initial Start-up", "blue", "🚀"),
    ("Normal Start-up / Start-up after Turnaround or Emergency Shutdown", "teal", "♨"),
    ("Normal Operation", "green", "⚙"),
    ("Normal Shutdown", "orange", "♨"),
    ("Emergency Shutdown", "red", "⚠"),
    ("Emergency Operation", "purple", "♨"),
]

cols = st.columns(6, gap="small")

for col, (category, css, icon) in zip(cols, category_list):

    cat_df = area_df[
        area_df[COL_CAT].map(lambda x, c=category: category_matches(x, c))
    ].copy()

    cat_df = distinct_sops(cat_df)

    rows = []
    for _, r in cat_df.iterrows():
        proc = str(r[COL_PROC]).strip() or "—"
        sop = str(r[COL_SOP]).strip() or "—"

        rows.append(
            f"""
            <div class="proc-row">
                <div class="proc-name">{html.escape(proc)}</div>
                <div class="proc-no">{html.escape(sop)}</div>
            </div>
            """
        )

    body = "".join(rows)

    if not body:
        body = """
        <div class="no-records">
            <div class="no-records-icon">▱</div>
            <div>No records<br>for this category</div>
        </div>
        """

    # Fully self-contained HTML/CSS for each category card.
    card = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * {{ box-sizing:border-box; }}
    html,body {{
        margin:0;padding:0;background:transparent;
        font-family:Arial,sans-serif;
    }}
    .category-card {{
        width:100%;
        height:300px;
        border:1px solid rgba(100,120,145,.17);
        border-radius:10px;
        overflow:hidden;
        background:#fff;
        box-shadow:0 2px 10px rgba(40,55,80,.07);
    }}
    .category-head {{
        min-height:48px;
        padding:7px 8px;
        display:flex;
        align-items:center;
        gap:6px;
        border-bottom:1px solid rgba(90,110,140,.15);
    }}
    .icon {{
        width:24px;
        font-size:20px;
        text-align:center;
    }}
    .category-name {{
        flex:1;
        font-size:8.5px;
        line-height:1.12;
        font-weight:900;
    }}
    .count {{
        min-width:25px;height:23px;
        padding:0 7px;
        border-radius:12px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:11px;font-weight:900;
        box-shadow:inset 0 0 8px rgba(255,255,255,.55);
    }}
    .blue .category-head {{background:linear-gradient(135deg,#f3f7ff,#e9f1ff);color:#214f9b}}
    .blue .count {{background:#6aa7ef;color:#103b7b}}
    .teal .category-head {{background:linear-gradient(135deg,#f1fbfa,#e7f8f5);color:#18877f}}
    .teal .count {{background:#75d0cc;color:#0e6963}}
    .green .category-head {{background:linear-gradient(135deg,#f4fbf0,#e9f7e3);color:#398333}}
    .green .count {{background:#92d77e;color:#286b21}}
    .orange .category-head {{background:linear-gradient(135deg,#fff8ed,#fff0da);color:#cf7318}}
    .orange .count {{background:#f7b45f;color:#8b4a00}}
    .red .category-head {{background:linear-gradient(135deg,#fff4f4,#ffe9e9);color:#c73636}}
    .red .count {{background:#ef8e8e;color:#8d2222}}
    .purple .category-head {{background:linear-gradient(135deg,#fbf4ff,#f3e9ff);color:#70409b}}
    .purple .count {{background:#b58de0;color:#542a7f}}
    .table-head {{
        display:grid;
        grid-template-columns:1fr 74px;
        background:rgba(225,232,242,.65);
        border-bottom:1px solid rgba(90,110,140,.14);
        font-size:8px;
        font-weight:900;
        color:#26364d;
    }}
    .table-head div {{padding:6px 7px;}}
    .table-head div:last-child {{
        text-align:center;
        border-left:1px solid rgba(90,110,140,.12);
    }}
    .cat-body {{height:244px;overflow-y:auto;}}
    .proc-row {{
        display:grid;
        grid-template-columns:1fr 74px;
        min-height:54px;
        border-bottom:1px solid rgba(90,110,140,.10);
        font-size:8px;
        line-height:1.35;
        color:#263248;
    }}
    .proc-name {{padding:6px 7px;}}
    .proc-no {{
        padding:6px 5px;
        border-left:1px solid rgba(90,110,140,.10);
        font-weight:700;text-align:center;
    }}
    .no-records {{
        height:235px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        color:#394457;
        font-size:10px;
        text-align:center;
    }}
    .no-records-icon {{
        font-size:35px;
        opacity:.62;
        margin-bottom:7px;
    }}
    </style>
    </head>
    <body>
    <div class="category-card {css}">
        <div class="category-head">
            <div class="icon">{icon}</div>
            <div class="category-name">{html.escape(category)}</div>
            <div class="count">{len(cat_df)}</div>
        </div>
        <div class="table-head">
            <div>Procedure Name</div>
            <div>Procedure No./<br>SOP No.</div>
        </div>
        <div class="cat-body">
            {body}
        </div>
    </div>
    </body>
    </html>
    """

    with col:
        st.components.v1.html(card, height=305, scrolling=False)

st.markdown(
    '<div class="note">Note: SOPs can be categorized under multiple categories.</div>',
    unsafe_allow_html=True
)

# ============================================================
# FOOTER / AUTO REFRESH
# ============================================================
st.markdown(
    """
    <div style="text-align:right;font-size:8px;color:#8993a4;margin-top:2px;">
        Data source: Google Sheet • OP
    </div>
    """,
    unsafe_allow_html=True
)

