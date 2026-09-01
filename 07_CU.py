import io
import re
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM Dashboard - Central Utility",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GOOGLE SHEET
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

# IMPORTANT:
# These are the GIDs supplied for the Central Utility dashboard.
# PT and the other modules are NOT read by row count from the
# whole workbook. Each module is loaded from its own tab/GID.
SHEETS = {
    "PT": "1997330551",
    "PHA": "1151637695",
    "PHA Recommendation": "1114420199",
    "MOC": "1493447251",
    "PSSR": "1914804736",
    "PS Incident": "354502422",   # corrected: Incident
    "Training": "1071736559",       # corrected: Training
    "SOC-SOL": "510439154",
    "Critical Equipment": None,
    "Alarm": None,
    "Barrier Audit": None,
}


# ============================================================
# STYLE
# ============================================================
st.markdown(
    """
    <style>

    .stApp {
        background:#f3f8fc;
    }

    #MainMenu, footer {
        visibility:hidden;
    }

    /* REMOVE STREAMLIT TOP BAR / DEPLOY SPACE */
    header[data-testid="stHeader"] {
        display:none !important;
    }

   .block-container {
    padding:0rem 0.35rem 0rem 0.35rem !important;
    margin-bottom:0px !important;
    max-width:100%;
}

/* REMOVE BOTTOM SPACE */
[data-testid="stAppViewContainer"] {
    padding-bottom:0px !important;
}

[data-testid="stMainBlockContainer"] {
    padding-bottom:0px !important;
    margin-bottom:0px !important;
}

section.main {
    padding-bottom:0px !important;
    margin-bottom:0px !important;
}

   div[data-testid="stMetric"] {
    background:#ffffff;
    border:1px solid #cbddea;
    border-radius:7px;
    padding:6px 6px !important;
    min-height:72px;
    overflow:visible !important;
}

    div[data-testid="stMetricLabel"] {
    font-size:9px !important;
    font-weight:800 !important;
    color:#20384f !important;
    white-space:nowrap !important;
    overflow:visible !important;
    text-overflow:clip !important;
    line-height:1.1 !important;
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] > div,
div[data-testid="stMetricLabel"] p {
    overflow:visible !important;
    text-overflow:clip !important;
    white-space:nowrap !important;
    max-width:none !important;
}

div[data-testid="stMetricLabel"] p {
    margin:0 !important;
    padding:0 !important;
    font-size:8px !important;
    line-height:1.1 !important;
}
    div[data-testid="stMetricValue"] {
        color:#123f77 !important;
        font-size:24px !important;
        font-weight:900 !important;
    }

    .module-card {
        background:#ffffff;
        border:1px solid #d3e0ea;
        border-radius:7px;
        padding:7px;
        margin-bottom:8px;
        box-shadow:0 1px 4px rgba(20,65,95,.06);
    }

    .module-title {
        color:#073f78;
        font-size:12px;
        font-weight:900;
        margin-bottom:6px;
    }

    .section-bar {
        background:#07518b;
        color:#ffffff;
        border-radius:4px;
        padding:6px 8px;
        font-size:10px;
        font-weight:900;
        margin:4px 0 6px 0;
    }

    .live-bar {
        background:#ffffff;
        border:1px solid #cbddea;
        border-radius:4px;
        padding:5px 8px;
        color:#4f6678;
        font-size:10px;
        margin-bottom:6px;
    }

    .footer {
        text-align:center;
        color:#627689;
        background:#edf4f8;
        border-top:1px solid #cbdce7;
        padding:7px;
        font-size:10px;
        font-weight:800;
        margin-top:8px;
    }

    .small-note {
        font-size:9px;
        color:#6c7f8f;
    }

    .stDataFrame {
        border:1px solid #d5e0e8;
    }


    /* ========================================================
       REDUCE SPACE BETWEEN HEADER AND REFRESH BUTTON
       ======================================================== */

    div[data-testid="stButton"] {
        margin-top:-35px !important;
        margin-bottom:0px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Central Utility HEADER
# DO NOT CHANGE THIS HEADER
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

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    background: #f4f9fc;
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

    border-top: 2px solid #0b91d1;
    border-bottom: 3px solid #1487c2;

    box-shadow:
        0 4px 12px rgba(21,92,130,.18);
}

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

    background-size: 15px 15px;
    opacity: .65;
}

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

.title {
    color: #153e68;
    font-size: 24px;
    font-weight: 950;
    letter-spacing: 5px;
    line-height: 1;
    margin-bottom: 5px;

    text-shadow:
        0 1px 1px rgba(255,255,255,.9);
}

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
            #176ca5 0%,
            #07518b 55%,
            #063e70 100%
        );

    border: 1px solid #0877ba;
    border-radius: 14px;

    color: #ffd21a;

    font-size: 42px;
    font-weight: 950;
    letter-spacing: 1px;

    box-shadow:
        0 7px 16px rgba(11,83,130,.25),
        inset 0 1px 0 rgba(255,255,255,.28),
        inset 0 -5px 12px rgba(0,35,75,.16);
}

.pillar::before,
.pillar::after {
    position: absolute;

    top: 50%;
    transform: translateY(-50%);

    color: #51c5ff;
    font-size: 21px;
    font-weight: 950;
    letter-spacing: -5px;

    text-shadow:
        0 1px 5px rgba(0,100,160,.5);
}

.pillar::before {
    content: "◀◀";
    left: 17px;
}

.pillar::after {
    content: "▶▶";
    right: 17px;
}

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
            #075b8e,
            #1188c4,
            #075b8e
        );

    border: 1px solid #078fd2;
    border-radius: 7px;

    color: #ffffff;

    font-size: 10px;
    font-weight: 900;
    letter-spacing: 1.8px;

    box-shadow:
        0 4px 9px rgba(10,93,140,.20),
        inset 0 1px 0 rgba(255,255,255,.25);
}

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
            #00a9ff 18%,
            #ffffff 50%,
            #00a9ff 82%,
            transparent
        );

    box-shadow:
        0 0 8px rgba(0,169,255,.55);
}

.corner-light {
    position: absolute;
    z-index: 10;

    width: 110px;
    height: 3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00baff,
            transparent
        );

    box-shadow:
        0 0 8px rgba(0,186,255,.55);
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

    <div class="content">

        <div class="title">
            PSM DASHBOARD
        </div>

        <div class="pillar">
            Central Utility
        </div>

        <div class="subtitle">
            PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        </div>

    </div>

</div>

</body>
</html>
"""

st.components.v1.html(
    header_html,
    height=170,
    scrolling=False
)
# ============================================================
# HELPERS
# ============================================================
def norm(value):
    """Normalize text for safe column/department matching."""
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def find_col(df, candidates):
    """Find a column using exact normalized match, then partial match."""
    if df is None or df.empty:
        return None

    normalized = {norm(c): c for c in df.columns}

    for candidate in candidates:
        key = norm(candidate)
        if key in normalized:
            return normalized[key]

    for column in df.columns:
        ckey = norm(column)
        for candidate in candidates:
            nkey = norm(candidate)
            if nkey in ckey or ckey in nkey:
                return column

    return None


def clean_dataframe(df):
    if df is None or df.empty:
        return pd.DataFrame()

    out = df.copy()
    out.columns = [
        str(c).strip().replace("\n", " ").replace("\r", " ")
        for c in out.columns
    ]

    out = out.dropna(how="all").copy()

    for c in out.columns:
        if out[c].dtype == "object":
            out[c] = out[c].astype(str).str.strip()

    return out


def filter_central_utility(df):
    """
    Filter only Central utility records.

    VERY IMPORTANT:
    If a Department column exists, we MUST filter it.
    The old code returned the entire sheet when the Department
    column was not found, which is how a workbook row count such
    as 94 could incorrectly become TOTAL PT = 94.

    If no Department column exists, the sheet is treated as a
    module-specific sheet and its rows are retained.
    """
    df = clean_dataframe(df)

    if df.empty:
        return df

    department_col = find_col(
        df,
        [
            "Department",
            "Departments",
            "Dept",
            "Department Name",
            "Department_Name",
            "Dept Name",
            "Dept_Name",
        ],
    )

    if department_col is None:
        # Some module sheets may be dedicated to one module and
        # have no Department field. Do NOT destroy valid data.
        return df.copy()

    department = (
        df[department_col]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # Matches:
    # Central Utility
    # Central Utility
    # Central Utility
    # Central Utility
    # etc.
    mask = department.str.contains(
        r"CENTRAL\s*[-_/ ]*\s*UTILITY",
        regex=True,
        na=False,
    )

    return df.loc[mask].copy()


def load_csv_from_url(url):
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    # Google export is normally UTF-8 CSV.
    # Use StringIO so pandas gets a text stream.
    return pd.read_csv(io.StringIO(response.content.decode("utf-8-sig")))


@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(gid):
    """
    Load ONE exact Google Sheet tab by GID.

    This avoids the previous problem where the code used sheet
    names and could end up reading the wrong tab.
    """
    if not gid:
        return pd.DataFrame()

    export_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=csv&gid={gid}"
    )

    try:
        df = load_csv_from_url(export_url)
        return clean_dataframe(df)
    except Exception:
        # Fallback to Google visualization endpoint.
        gviz_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{SPREADSHEET_ID}/gviz/tq?"
            f"tqx=out:csv&gid={gid}"
        )

        try:
            df = load_csv_from_url(gviz_url)
            return clean_dataframe(df)
        except Exception:
            return pd.DataFrame()


def load_module(name):
    """Load a module and then apply the Central Utility filter."""
    raw = load_google_sheet(SHEETS.get(name))
    return filter_central_utility(raw)


def status_counts(df):
    result = {
        "total": 0,
        "completed": 0,
        "ongoing": 0,
        "pending": 0,
        "overdue": 0,
        "open": 0,
        "closed": 0,
    }

    if df is None or df.empty:
        return result

    result["total"] = len(df)

    status_col = find_col(
        df,
        [
            "Status",
            "Current Status",
            "Action Status",
            "Completion Status",
            "Investigation Status",
            "Recommendation Status",
        ],
    )

    if status_col is None:
        return result

    s = (
        df[status_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    result["completed"] = int(
        s.str.contains(r"\bcompleted?\b|\bcomplete\b", regex=True).sum()
    )

    result["ongoing"] = int(
        s.str.contains(r"ongoing|in progress|in-progress", regex=True).sum()
    )

    result["pending"] = int(
        s.str.contains(r"pending", regex=True).sum()
    )

    result["overdue"] = int(
        s.str.contains(r"overdue", regex=True).sum()
    )

    result["open"] = int(
        s.str.fullmatch(r"open", case=False, na=False).sum()
    )

    result["closed"] = int(
        s.str.fullmatch(r"closed", case=False, na=False).sum()
    )

    return result


def make_register(df, id_names, description_names, status_names):
    if df is None or df.empty:
        return pd.DataFrame()

    id_col = find_col(df, id_names)
    desc_col = find_col(df, description_names)
    status_col = find_col(df, status_names)

    result = pd.DataFrame(index=df.index)

    # -----------------------------
    # ID / NUMBER
    # -----------------------------
    if id_col:
        result["No."] = (
            df[id_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )
    else:
        result["No."] = [
            f"{i + 1:03d}" for i in range(len(df))
        ]

    # -----------------------------
    # DESCRIPTION
    # -----------------------------
    if desc_col:
        result["Description"] = (
            df[desc_col]
            .fillna("-")
            .astype(str)
            .str.strip()
        )
    else:
        result["Description"] = "-"

    # -----------------------------
    # STATUS
    # -----------------------------
    if status_col:
        result["Status"] = (
            df[status_col]
            .fillna("-")
            .astype(str)
            .str.strip()
        )
    else:
        result["Status"] = "-"

    return result.reset_index(drop=True).head(5)


# ============================================================
# STATUS COLOUR
# ============================================================

def status_style(value):
    value = str(value).strip().lower()

    if value in ["completed", "complete", "closed"]:
        return "color: #008000; font-weight: 800;"

    elif value in ["ongoing", "in progress", "in-progress", "pending"]:
        return "color: #e67e00; font-weight: 800;"

    elif value in ["overdue", "open"]:
        return "color: #d71920; font-weight: 800;"

    else:
        return "color: #333333;"


# ============================================================
# REGISTER DISPLAY
# ============================================================

def show_register(title, df, id_names, description_names, status_names):

    st.markdown(
        f'<div class="section-bar">{title}</div>',
        unsafe_allow_html=True,
    )

    register_df = make_register(
        df,
        id_names,
        description_names,
        status_names,
    )

    if register_df.empty:

        st.info("No Central Utility records found.")

    else:

        # Apply colour ONLY to Status column
        styled_df = (
            register_df.style
            .map(
                status_style,
                subset=["Status"]
            )
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            height=178,
        )


def show_module_title(number, icon, title):
    st.markdown(
        f'<div class="module-title">🔴 {number} {icon} {title}</div>',
        unsafe_allow_html=True,
    )


def show_metric_row(items):
    cols = st.columns(len(items), gap="small")
    for c, (label, value) in zip(cols, items):
        with c:
            st.metric(label, value)


def get_date_column(df):
    return find_col(
        df,
        [
            "Date",
            "Audit Date",
            "Last Audit Date",
            "Deviation Date",
            "Record Date",
            "Incident Date",
        ],
    )


# ============================================================
# LOAD DATA
# ============================================================
if st.button("↻ Refresh Data", key="refresh_data"):
    st.cache_data.clear()
    st.rerun()

loaded = {}

for module_name in SHEETS:
    loaded[module_name] = load_module(module_name)

pt = loaded["PT"]
pha = loaded["PHA"]
rec = loaded["PHA Recommendation"]
moc = loaded["MOC"]
pssr = loaded["PSSR"]
training = loaded["Training"]
soc = loaded["SOC-SOL"]
incident = loaded["PS Incident"]
audit = loaded["Barrier Audit"]


# ============================================================
# LIVE DATA BAR
# ============================================================
module_count = sum(
    1 for df in loaded.values()
    if df is not None and not df.empty
)

st.markdown(
    f"""
    <div class="live-bar">
        <b>LIVE DATA: Google Sheet → Central Utility</b>
        &nbsp; | &nbsp;
        Refresh: 5 minutes
        &nbsp; | &nbsp;
        Modules with data: <b>{module_count}</b>
        &nbsp; | &nbsp;
        Last load: <b>{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</b>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ROW 1 — PT / PHA / RECOMMENDATION / MOC
# ============================================================
a, b, c, d = st.columns(4, gap="small")


with a:

    with st.container(border=True):

        # PT HEADER
        show_module_title(
            1,
            "",
            "PROCESS TECHNOLOGY (PT)"
        )

        # PT KPI
        x = status_counts(pt)

        show_metric_row([
            ("TOTAL PT", x["total"]),
            ("COMPLETED", x["completed"]),
            ("ONGOING", x["ongoing"]),
        ])

        # PT REGISTER
        show_register(
            "PT REGISTER",
            pt,
            ["PT No", "PT No.", "PT ID", "ID"],
            ["PT Description", "Description", "PT Name"],
            ["Status", "Current Status"],
        )

# ============================================================
# 2 — PROCESS HAZARD ANALYSIS (PHA)
# ============================================================


with b:

    with st.container(border=True):

        show_module_title(
            2,
            "△",
            "PROCESS HAZARD ANALYSIS (PHA)"
        )

        x = status_counts(pha)

        show_metric_row([
            ("TOTAL PHA", x["total"]),
            ("COMPLETED", x["completed"]),
            ("ONGOING", x["ongoing"]),
        ])

        show_register(
            "PHA REGISTER",
            pha,
            [
                "PHA No",
                "PHA No.",
                "PHA ID",
                "ID"
            ],
            [
                "PHA Description",
                "Description",
                "PHA Name"
            ],
            [
                "Status",
                "Current Status"
            ],
        )



# ============================================================
# 3 — PHA RECOMMENDATION
# ============================================================

with c:

    with st.container(border=True):

        show_module_title(
            3,
            "♧",
            "PHA RECOMMENDATION"
        )

        x = status_counts(rec)

        show_metric_row([
            (
                "TOTAL RECOMMENDATIONS",
                x["total"]
            ),
            (
                "OPEN",
                x["open"]
            ),
            (
                "CLOSED",
                x["closed"]
            ),
        ])

        show_register(
            "RECOMMENDATION REGISTER",
            rec,
            [
                "PHA No",
                "PHA No.",
                "Recommendation No",
                "Recommendation ID",
                "ID"
            ],
            [
                "Recommendation Description",
                "Recommendation",
                "Description"
            ],
            [
                "Status",
                "Action Status",
                "Recommendation Status"
            ],
        )



# ============================================================
# 4 — MANAGEMENT OF CHANGE (MOC)
# ============================================================

with d:
    with st.container(
            border=True,
            height=365
    ):

        show_module_title(
            3,
            "♙",
            "MOC"
        )

        x = status_counts(moc)

        show_metric_row([
            ("TOTAL MOC", x["total"]),
            ("OPEN", x["open"]),
            ("CLOSED", x["closed"]),
        ])

        # ----------------------------------------------------
        # MOC COLUMN MAPPING
        # ----------------------------------------------------

        moc_change_type_col = find_col(
            moc,
            [
                "Change Type (Permanent/Temporary/Emergency)",
                "Change Type (Permanent / Temporary / Emergency)",
                "Change Type",
                "MOC Change Type",
                "Type of Change",
                "Type",
            ],
        )

        moc_category_col = find_col(
            moc,
            [
                "Category of changes (Technology/Personnel/Facility)",
                "Category of changes (Technology / Personnel / Facility)",
                "Category of Changes",
                "MOC Category",
                "Change Category",
                "Category",
            ],
        )

        moc_chart = moc.copy()

        # ----------------------------------------------------
        # FILTER Central Utility
        # ----------------------------------------------------

        moc_department_col = find_col(
            moc,
            [
                "Department",
                "Departments",
                "Dept",
                "Department Name",
            ],
        )

        if moc_department_col:
            moc_chart = moc_chart[
                moc_chart[moc_department_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.contains(
                    "Central Utility",
                    case=False,
                    na=False
                )
            ].copy()

        # ----------------------------------------------------
        # TWO DONUT CHARTS
        # ----------------------------------------------------

        p1, p2 = st.columns(
            2,
            gap="small"
        )

        # ====================================================
        # TYPE-WISE
        # ====================================================

        with p1:

            st.markdown(
                """
                <div style="
                    text-align:center;
                    color:#173f70;
                    font-size:10px;
                    font-weight:800;
                    margin-bottom:4px;
                ">
                    TYPE-WISE DISTRIBUTION
                </div>
                """,
                unsafe_allow_html=True,
            )

            if (
                moc_change_type_col
                and not moc_chart.empty
            ):

                type_data = (
                    moc_chart[moc_change_type_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                type_data = type_data[
                    type_data != ""
                ]

                type_counts = (
                    type_data.value_counts()
                )

                if not type_counts.empty:

                    type_labels = [
                        f"{label} {int(value)} "
                        f"({value / type_counts.sum() * 100:.0f}%)"
                        for label, value
                        in zip(
                            type_counts.index,
                            type_counts.values
                        )
                    ]

                    fig_type = go.Figure(
                        data=[
                            go.Pie(
                                labels=type_labels,
                                values=type_counts.values,
                                hole=0.58,
                                textinfo="none",
                                domain=dict(
                                    x=[0.00, 0.55],
                                    y=[0.08, 0.92],
                                ),
                                hovertemplate=(
                                    "%{label}"
                                    "<extra></extra>"
                                ),
                            )
                        ]
                    )

                    fig_type.update_layout(
                        height=180,
                        margin=dict(
                            l=0,
                            r=0,
                            t=0,
                            b=0
                        ),
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            x=0.72,
                            y=0.5,
                            xanchor="left",
                            yanchor="middle",
                            font=dict(size=8),
                        ),
                        font=dict(size=8),
                    )

                    st.plotly_chart(
                        fig_type,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="bf_moc_type_donut",
                    )

                else:

                    st.info(
                        "No MOC Type data found."
                    )

            else:

                st.info(
                    "MOC Change Type column not found."
                )

        # ====================================================
        # CATEGORY-WISE
        # ====================================================

        with p2:

            st.markdown(
                """
                <div style="
                    text-align:center;
                    color:#173f70;
                    font-size:10px;
                    font-weight:800;
                    margin-bottom:4px;
                ">
                    CATEGORY-WISE DISTRIBUTION
                </div>
                """,
                unsafe_allow_html=True,
            )

            if (
                moc_category_col
                and not moc_chart.empty
            ):

                category_data = (
                    moc_chart[moc_category_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                category_data = category_data[
                    category_data != ""
                ]

                category_counts = (
                    category_data.value_counts()
                )

                if not category_counts.empty:

                    category_labels = [
                        f"{label} {int(value)} "
                        f"({value / category_counts.sum() * 100:.0f}%)"
                        for label, value
                        in zip(
                            category_counts.index,
                            category_counts.values
                        )
                    ]

                    fig_category = go.Figure(
                        data=[
                            go.Pie(
                                labels=category_labels,
                                values=category_counts.values,
                                hole=0.58,
                                textinfo="none",
                                domain=dict(
                                    x=[0.00, 0.55],
                                    y=[0.08, 0.92],
                                ),
                                hovertemplate=(
                                    "%{label}"
                                    "<extra></extra>"
                                ),
                            )
                        ]
                    )

                    fig_category.update_layout(
                        height=180,
                        margin=dict(
                            l=0,
                            r=0,
                            t=0,
                            b=0
                        ),
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            x=0.72,
                            y=0.5,
                            xanchor="left",
                            yanchor="middle",
                            font=dict(size=8),
                        ),
                        font=dict(size=8),
                    )

                    st.plotly_chart(
                        fig_category,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="bf_moc_category_donut",
                    )

                else:

                    st.info(
                        "No MOC Category data found."
                    )

            else:

                st.info(
                    "MOC Category column not found."
                )


# ============================================================
# ROW 2 — PSSR / INCIDENT / TRAINING
# ============================================================

a, b, c = st.columns(
    [1.20, 1.40, 1.40],
    gap="small"
)


# ============================================================
# 5 — PSSR
# ============================================================

with a:

    with st.container(border=True):

        show_module_title(
            5,
            "",
            "PRE-STARTUP SAFETY REVIEW (PSSR)"
        )

        x = status_counts(pssr)

        show_metric_row([
            ("TOTAL PSSR", x["total"]),
            ("COMPLETED", x["completed"]),
            ("PENDING", x["pending"]),
            ("OVERDUE", x["overdue"]),
        ])

        show_register(
            "PSSR REGISTER",
            pssr,
            [
                "PSSR No",
                "PSSR No.",
                "PSSR ID",
                "ID"
            ],
            [
                "PSSR Description",
                "Description",
                "PSSR Name"
            ],
            [
                "Status",
                "Current Status"
            ],
        )


# ============================================================
# 6 — PROCESS SAFETY INCIDENT
# ============================================================

with b:

    with st.container(
        border=True,
        height=365
    ):

        show_module_title(
            6,
            "⚠",
            "PROCESS SAFETY INCIDENT"
        )

        # ----------------------------------------------------
        # COLUMN MAPPING
        # B = Department → Total Incidents
        # F = Incident Classification
        # G = Incident Level
        # J = Investigation Status
        # ----------------------------------------------------

        if len(incident.columns) >= 2:
            department_col = incident.columns[1]
        else:
            department_col = None

        if len(incident.columns) >= 6:
            classification_col = incident.columns[5]
        else:
            classification_col = find_col(
                incident,
                [
                    "Incident Classification",
                    "Incident classification",
                    "Classification",
                ]
            )

        if len(incident.columns) >= 7:
            level_col = incident.columns[6]
        else:
            level_col = find_col(
                incident,
                [
                    "Incident Level",
                    "Incident level",
                    "Level",
                ]
            )

        if len(incident.columns) >= 10:
            investigation_status_col = (
                incident.columns[9]
            )
        else:
            investigation_status_col = find_col(
                incident,
                [
                    "Investigation status",
                    "Investigation Status",
                    "Investigation",
                    "Status",
                ]
            )

        # ----------------------------------------------------
        # TOTAL INCIDENTS — COLUMN B
        # ----------------------------------------------------

        total_incidents = 0

        if (
            department_col
            and not incident.empty
        ):

            department_values = (
                incident[department_col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            total_incidents = (
                department_values
                .replace(
                    [
                        "",
                        "-",
                        "nan",
                        "None"
                    ],
                    pd.NA
                )
                .notna()
                .sum()
            )

        # ----------------------------------------------------
        # INVESTIGATION STATUS — COLUMN J
        # ----------------------------------------------------

        investigation_completed = 0
        investigation_pending = 0

        if (
            investigation_status_col
            and not incident.empty
        ):

            investigation_values = (
                incident[
                    investigation_status_col
                ]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            investigation_completed = (
                investigation_values
                .isin(
                    [
                        "completed",
                        "complete",
                        "closed",
                        "done",
                    ]
                )
                .sum()
            )

            investigation_pending = (
                investigation_values
                .isin(
                    [
                        "pending",
                        "ongoing",
                        "open",
                        "in progress",
                        "in-progress",
                    ]
                )
                .sum()
            )

        # ----------------------------------------------------
        # COMPACT KPI CARDS
        # ----------------------------------------------------

        m1, m2, m3 = st.columns(
            [0.70, 0.70, 0.70],
            gap="small"
        )

        with m1:

            st.metric(
                "TOTAL INCIDENTS",
                int(total_incidents)
            )

        with m2:

            st.metric(
                "INVESTIGATION COMPLETED",
                int(investigation_completed)
            )

        with m3:

            st.metric(
                "INVESTIGATION PENDING",
                int(investigation_pending)
            )

        # ====================================================
        # TWO PSI GRAPHS
        # ====================================================

        p1, p2 = st.columns(
            2,
            gap="small"
        )

        # ====================================================
        # CLASSIFICATION-WISE
        # ====================================================

        with p1:

            st.caption(
                "CLASSIFICATION-WISE DISTRIBUTION"
            )

            if (
                classification_col
                and not incident.empty
            ):

                classification_values = (
                    incident[
                        classification_col
                    ]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                classification_values = (
                    classification_values[
                        ~classification_values.isin(
                            [
                                "",
                                "-",
                                "nan",
                                "none"
                            ]
                        )
                    ]
                )

                # ------------------------------------------------
                # STANDARDIZE CLASSIFICATION
                # Serious must be checked FIRST
                # ------------------------------------------------

                classification_values = (
                    classification_values.map(
                        lambda x:
                        "Serious Process Incident"
                        if (
                            "serious" in x
                            and "process" in x
                            and "incident" in x
                        )
                        else
                        "Process Incident"
                        if (
                            "process" in x
                            and "incident" in x
                        )
                        else
                        "Near Miss"
                        if (
                            "near" in x
                            and "miss" in x
                        )
                        else x.title()
                    )
                )

                classification_counts = (
                    classification_values
                    .value_counts()
                )

                classification_order = [
                    "Near Miss",
                    "Process Incident",
                    "Serious Process Incident",
                ]

                classification_counts = (
                    classification_counts
                    .reindex(
                        classification_order,
                        fill_value=0
                    )
                )

                classification_counts = (
                    classification_counts[
                        classification_counts > 0
                    ]
                )

                if not classification_counts.empty:

                    fig_class = go.Figure()

                    fig_class.add_trace(
                        go.Bar(
                            x=classification_counts.values,
                            y=classification_counts.index,
                            orientation="h",
                            width=0.50,
                            text=classification_counts.values,
                            textposition="outside",

                            marker=dict(
                                color=[
                                    "#0751a5"
                                    if x == "Near Miss"
                                    else "#e31b23"
                                    if x == "Process Incident"
                                    else "#808080"
                                    for x
                                    in classification_counts.index
                                ]
                            ),

                            hovertemplate=(
                                "%{y}: %{x}"
                                "<extra></extra>"
                            ),
                        )
                    )

                    fig_class.update_layout(
                        height=180,
                        margin=dict(
                            l=5,
                            r=25,
                            t=5,
                            b=5
                        ),
                        showlegend=False,
                        font=dict(size=9),

                        xaxis=dict(
                            title=None,
                            dtick=1,
                            showgrid=True,
                            gridcolor="#e1e7ef",
                            zeroline=False,
                        ),

                        yaxis=dict(
                            title=None,
                            autorange="reversed",
                        ),

                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )

                    st.plotly_chart(
                        fig_class,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="psi_classification_chart",
                    )

                else:

                    st.info(
                        "No incident classification data."
                    )

            else:

                st.info(
                    "Incident Classification column not found."
                )

        # ====================================================
        # LEVEL-WISE
        # ====================================================

        with p2:

            st.caption(
                "LEVEL-WISE DISTRIBUTION"
            )

            if (
                level_col
                and not incident.empty
            ):

                level_values = (
                    incident[level_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                level_values = (
                    level_values[
                        ~level_values.isin(
                            [
                                "",
                                "-",
                                "nan",
                                "none"
                            ]
                        )
                    ]
                )

                level_values = (
                    level_values.map(
                        lambda x:
                        "Level 1"
                        if "level 1" in x
                        else
                        "Level 2"
                        if "level 2" in x
                        else
                        "Level 3"
                        if "level 3" in x
                        else
                        "Level 4"
                        if "level 4" in x
                        else x.title()
                    )
                )

                level_counts = (
                    level_values
                    .value_counts()
                )

                level_order = [
                    "Level 1",
                    "Level 2",
                    "Level 3",
                    "Level 4",
                ]

                level_counts = (
                    level_counts
                    .reindex(
                        level_order,
                        fill_value=0
                    )
                )

                level_counts = (
                    level_counts[
                        level_counts > 0
                    ]
                )

                if not level_counts.empty:

                    fig_level = go.Figure()

                    fig_level.add_trace(
                        go.Bar(
                            x=level_counts.values,
                            y=level_counts.index,
                            orientation="h",
                            width=0.50,
                            text=level_counts.values,
                            textposition="outside",

                            marker=dict(
                                color=[
                                    "#0751a5"
                                    if x == "Level 1"
                                    else "#e31b23"
                                    if x == "Level 2"
                                    else "#808080"
                                    if x == "Level 3"
                                    else "#173f70"
                                    for x
                                    in level_counts.index
                                ]
                            ),

                            hovertemplate=(
                                "%{y}: %{x}"
                                "<extra></extra>"
                            ),
                        )
                    )

                    fig_level.update_layout(
                        height=180,
                        margin=dict(
                            l=5,
                            r=25,
                            t=5,
                            b=5
                        ),
                        showlegend=False,
                        font=dict(size=9),

                        xaxis=dict(
                            title=None,
                            dtick=1,
                            showgrid=True,
                            gridcolor="#e1e7ef",
                            zeroline=False,
                        ),

                        yaxis=dict(
                            title=None,
                            autorange="reversed",
                        ),

                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )

                    st.plotly_chart(
                        fig_level,
                        use_container_width=True,
                        config={
                            "displayModeBar": False
                        },
                        key="psi_level_chart",
                    )

                else:

                    st.info(
                        "No incident level data."
                    )

            else:

                st.info(
                    "Incident Level column not found."
                )


# ============================================================
# 7 — TRAINING
# ============================================================

with c:

    with st.container(
        border=True,
        height=365
    ):

        show_module_title(
            7,
            "♙",
            "TRAINING"
        )


        if (
            training is None
            or training.empty
        ):

            st.info(
                "No Central Utility training data found."
            )

        else:

            tr = training.copy()

            # ------------------------------------------------
            # FIND COLUMNS
            # ------------------------------------------------

            process_col = find_col(
                tr,
                ["Process"]
            )

            department_col = find_col(
                tr,
                ["Departments"]
            )

            total_l08_col = find_col(
                tr,
                [
                    "Total Employees (L08 & Above)"
                ]
            )

            total_below_l08_col = find_col(
                tr,
                [
                    "Total Employees (Below L08)"
                ]
            )

            total_associates_col = find_col(
                tr,
                [
                    "Total Associates"
                ]
            )

            total_contractual_col = find_col(
                tr,
                [
                    "Total Contractual Workers"
                ]
            )

            completed_l08_col = find_col(
                tr,
                [
                    "Completed Training (L08 & Above)"
                ]
            )

            completed_below_l08_col = find_col(
                tr,
                [
                    "Completed Training (Below L08)"
                ]
            )

            completed_associates_col = find_col(
                tr,
                [
                    "Completed Training (Associates)"
                ]
            )

            completed_contractual_col = find_col(
                tr,
                [
                    "Completed Training (Contracts)"
                ]
            )

            required_columns = [
                process_col,
                total_l08_col,
                total_below_l08_col,
                total_associates_col,
                total_contractual_col,
                completed_l08_col,
                completed_below_l08_col,
                completed_associates_col,
                completed_contractual_col,
            ]

            if any(
                col is None
                for col in required_columns
            ):

                st.error(
                    "Training Google Sheet column mapping error."
                )

            else:

                def to_number(series):

                    return pd.to_numeric(
                        series
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
                    )

                # ------------------------------------------------
                # BUILD HEATMAP DATA
                # ------------------------------------------------

                heatmap_df = pd.DataFrame()

                heatmap_df["Module"] = (
                    tr[process_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                total_l08 = to_number(
                    tr[total_l08_col]
                )

                total_below_l08 = to_number(
                    tr[total_below_l08_col]
                )

                total_associates = to_number(
                    tr[total_associates_col]
                )

                total_contractual = to_number(
                    tr[total_contractual_col]
                )

                completed_l08 = to_number(
                    tr[completed_l08_col]
                )

                completed_below_l08 = to_number(
                    tr[completed_below_l08_col]
                )

                completed_associates = to_number(
                    tr[completed_associates_col]
                )

                completed_contractual = to_number(
                    tr[completed_contractual_col]
                )

                # ------------------------------------------------
                # COMPLETION %
                # Completed / Total × 100
                # ------------------------------------------------

                heatmap_df["L08 & Above"] = (
                    completed_l08
                    .div(
                        total_l08.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Below L08"] = (
                    completed_below_l08
                    .div(
                        total_below_l08.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Associates"] = (
                    completed_associates
                    .div(
                        total_associates.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df["Contractual"] = (
                    completed_contractual
                    .div(
                        total_contractual.replace(
                            0,
                            float("nan")
                        )
                    )
                    .mul(100)
                )

                heatmap_df = heatmap_df[
                    heatmap_df["Module"]
                    .str.strip() != ""
                ].copy()

                # ------------------------------------------------
                # MODULE ORDER
                # ------------------------------------------------

                module_order = [
                    "PSM GA",
                    "PT",
                    "PHA",
                    "MOC",
                    "OP",
                    "BOWTIE",
                    "PSSR",
                    "LOPA",
                    "MIQA",
                ]

                heatmap_df["_order"] = (
                    heatmap_df["Module"]
                    .apply(
                        lambda x:
                        module_order.index(x)
                        if x in module_order
                        else 999
                    )
                )

                heatmap_df = (
                    heatmap_df
                    .sort_values(
                        ["_order", "Module"]
                    )
                    .drop(
                        columns="_order"
                    )
                )

                # ------------------------------------------------
                # DISPLAY DATA
                # ------------------------------------------------

                display_df = heatmap_df.copy()

                percentage_columns = [
                    "L08 & Above",
                    "Below L08",
                    "Associates",
                    "Contractual",
                ]

                for column in percentage_columns:

                    display_df[column] = (
                        display_df[column]
                        .apply(
                            lambda x:
                            "—"
                            if pd.isna(x)
                            else f"{x:.2f}%"
                        )
                    )

                # ------------------------------------------------
                # HEATMAP STYLE
                # ------------------------------------------------

                def heatmap_style(column):

                    styles = []

                    for value in column:

                        numeric = pd.to_numeric(
                            str(value)
                            .replace("%", ""),
                            errors="coerce"
                        )

                        if pd.isna(numeric):

                            styles.append(
                                "background-color:#ffffff;"
                                "color:#8a97a5;"
                                "text-align:center;"
                            )

                        else:

                            numeric = max(
                                0,
                                min(
                                    100,
                                    float(numeric)
                                )
                            )

                            if numeric <= 50:

                                ratio = numeric / 50

                                red = 255

                                green = int(
                                    220
                                    + (
                                        25 * ratio
                                    )
                                )

                                blue = int(
                                    220
                                    - (
                                        70 * ratio
                                    )
                                )

                            else:

                                ratio = (
                                    numeric - 50
                                ) / 50

                                red = int(
                                    255
                                    - (
                                        55 * ratio
                                    )
                                )

                                green = 245

                                blue = int(
                                    150
                                    + (
                                        45 * ratio
                                    )
                                )

                            styles.append(
                                f"background-color:"
                                f"rgb({red},{green},{blue});"
                                "color:#173f70;"
                                "font-weight:700;"
                                "text-align:center;"
                            )

                    return styles

                styled_df = (
                    display_df.style
                    .apply(
                        heatmap_style,
                        subset=percentage_columns,
                        axis=0,
                    )
                    .set_properties(
                        subset=["Module"],
                        **{
                            "font-weight": "700",
                            "color": "#173f70",
                            "text-align": "left",
                        }
                    )
                    .set_properties(
                        **{
                            "font-size": "10px",
                            "border": "1px solid #d6e1eb",
                        }
                    )
                    .set_table_styles(
                        [
                            {
                                "selector": "th",
                                "props": [
                                    (
                                        "background-color",
                                        "#073f7c"
                                    ),
                                    (
                                        "color",
                                        "white"
                                    ),
                                    (
                                        "font-weight",
                                        "700"
                                    ),
                                    (
                                        "text-align",
                                        "center"
                                    ),
                                    (
                                        "font-size",
                                        "10px"
                                    ),
                                ],
                            }
                        ]
                    )
                )

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    height=245,
                    key="bf_training_heatmap",
                )


# ============================================================
# ROW 3 — SOC / SOL + AUDIT
# ============================================================

a, b = st.columns(
    [1.35, 1.65],
    gap="small"
)


# ============================================================
# 8 — SOC / SOL DEVIATION
# ============================================================

with a:

    with st.container(border=True):

        show_module_title(
            8,
            "",
            "SOC / SOL DEVIATION"
        )

        if (
            soc is None
            or soc.empty
        ):

            st.info(
                "No SOC / SOL data available."
            )

        else:

            month_col = find_col(
                soc,
                [
                    "Month",
                    "MONTH",
                    "month"
                ]
            )

            department_col = find_col(
                soc,
                [
                    "Department",
                    "DEPARTMENT",
                    "department"
                ]
            )

            soc_col = find_col(
                soc,
                [
                    "SOC Deviation Nos.",
                    "SOC Deviation No.",
                    "SOC Deviation",
                    "SOC"
                ]
            )

            sol_col = find_col(
                soc,
                [
                    "SOL Deviation Nos.",
                    "SOL Deviation No.",
                    "SOL Deviation",
                    "SOL"
                ]
            )

            if month_col is None:

                st.error(
                    "Month column not found in SOC / SOL Google Sheet."
                )

            else:

                df_socsol = soc.copy()

                # ------------------------------------------------
                # MONTH
                # ------------------------------------------------

                df_socsol["_MONTH"] = (
                    df_socsol[month_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

                df_socsol = df_socsol[
                    df_socsol["_MONTH"] != ""
                ].copy()

                # ------------------------------------------------
                # Central Utility FILTER
                # ------------------------------------------------

                if department_col is not None:
                    df_socsol["_DEPARTMENT"] = (
                        df_socsol[department_col]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                        .str.lower()
                    )

                    df_socsol = df_socsol[
                        df_socsol["_DEPARTMENT"].str.contains(
                            "Central Utility",
                            case=False,
                            na=False
                        )
                    ].copy()

                # ------------------------------------------------
                # SOC
                # ------------------------------------------------

                if soc_col is not None:

                    df_socsol["_SOC_VALUE"] = (
                        pd.to_numeric(
                            df_socsol[soc_col],
                            errors="coerce"
                        )
                        .fillna(0)
                    )

                else:

                    df_socsol["_SOC_VALUE"] = 0

                # ------------------------------------------------
                # SOL
                # ------------------------------------------------

                if sol_col is not None:

                    df_socsol["_SOL_VALUE"] = (
                        pd.to_numeric(
                            df_socsol[sol_col],
                            errors="coerce"
                        )
                        .fillna(0)
                    )

                else:

                    df_socsol["_SOL_VALUE"] = 0

                # ------------------------------------------------
                # FY MONTHS
                # ------------------------------------------------

                fy_months = [
                    "April-26",
                    "May-26",
                    "June-26",
                    "July-26",
                    "August-26",
                    "September-26",
                    "October-26",
                    "November-26",
                    "December-26",
                    "January-27",
                    "February-27",
                    "March-27",
                ]

                soc_monthly = (
                    df_socsol
                    .groupby(
                        "_MONTH",
                        as_index=False
                    )["_SOC_VALUE"]
                    .sum()
                )

                sol_monthly = (
                    df_socsol
                    .groupby(
                        "_MONTH",
                        as_index=False
                    )["_SOL_VALUE"]
                    .sum()
                )

                monthly = pd.DataFrame(
                    {
                        "_MONTH": fy_months
                    }
                )

                monthly = monthly.merge(
                    soc_monthly,
                    on="_MONTH",
                    how="left"
                )

                monthly = monthly.merge(
                    sol_monthly,
                    on="_MONTH",
                    how="left"
                )

                monthly["_SOC_VALUE"] = (
                    monthly["_SOC_VALUE"]
                    .fillna(0)
                )

                monthly["_SOL_VALUE"] = (
                    monthly["_SOL_VALUE"]
                    .fillna(0)
                )

                # ------------------------------------------------
                # GRAPH
                # ------------------------------------------------

                fig = go.Figure()

                # SOC
                fig.add_trace(
                    go.Scatter(
                        x=monthly["_MONTH"],
                        y=monthly["_SOC_VALUE"],
                        mode="lines+markers+text",
                        name="SOC Deviation",
                        text=(
                            monthly["_SOC_VALUE"]
                            .astype(int)
                        ),
                        textposition="top center",
                        line=dict(
                            width=3
                        ),
                        marker=dict(
                            size=7
                        ),
                        hovertemplate=(
                            "<b>SOC</b><br>"
                            "Month: %{x}<br>"
                            "Deviation: %{y}"
                            "<extra></extra>"
                        )
                    )
                )

                # SOL
                fig.add_trace(
                    go.Scatter(
                        x=monthly["_MONTH"],
                        y=monthly["_SOL_VALUE"],
                        mode="lines+markers+text",
                        name="SOL Deviation",
                        text=(
                            monthly["_SOL_VALUE"]
                            .astype(int)
                        ),
                        textposition="bottom center",
                        line=dict(
                            width=3,
                            dash="solid"
                        ),
                        marker=dict(
                            size=7
                        ),
                        hovertemplate=(
                            "<b>SOL</b><br>"
                            "Month: %{x}<br>"
                            "Deviation: %{y}"
                            "<extra></extra>"
                        )
                    )
                )

                fig.update_layout(
                    height=280,

                    margin=dict(
                        l=45,
                        r=20,
                        t=45,
                        b=45
                    ),

                    title=dict(
                        text=(
                            "MONTH-WISE DISTRIBUTION "
                            "OF SOC / SOL DEVIATION"
                        ),
                        x=0.5,
                        xanchor="center",
                        font=dict(
                            size=12,
                            color="#173f73"
                        )
                    ),

                    xaxis=dict(
                        title="Month",
                        categoryorder="array",
                        categoryarray=fy_months,
                        tickangle=-45,
                        showgrid=False
                    ),

                    yaxis=dict(
                        title="No. of Deviations",
                        rangemode="tozero",
                        showgrid=True,
                        dtick=1
                    ),

                    legend=dict(
                        orientation="v",
                        x=0.78,
                        y=1.28,
                        xanchor="left",
                        yanchor="top",
                        font=dict(size=9),
                        bgcolor="rgba(255,255,255,0)"
                    ),

                    plot_bgcolor="white",
                    paper_bgcolor="white",

                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    },
                    key="bf_soc_sol_deviation_chart"
                )


# ============================================================
# 9 — AUDIT / COMPLIANCE
# ============================================================

with b:

    with st.container(
            border=True,
            height=340
    ):

        show_module_title(
            9,
            "♙",
            "AUDIT / COMPLIANCE"
        )

        audit_date_col = find_col(
            audit,
            [
                "Audit Date",
                "Last Audit Date",
                "Date"
            ],
        )

        compliance_col = find_col(
            audit,
            [
                "Compliance",
                "Compliance %",
                "Score",
                "Audit Score",
                "Percentage",
            ],
        )

        q1, q2 = st.columns(
            2,
            gap="small"
        )

        # ====================================================
        # LEFT SIDE
        # ====================================================

        with q1:

            if (
                audit_date_col
                and not audit.empty
            ):

                dates = pd.to_datetime(
                    audit[audit_date_col],
                    errors="coerce"
                ).dropna()

                if not dates.empty:

                    st.metric(
                        "LAST AUDIT DATE",
                        dates.max().strftime(
                            "%d-%b-%Y"
                        )
                    )

                else:

                    st.metric(
                        "LAST AUDIT DATE",
                        "—"
                    )

            else:

                st.metric(
                    "LAST AUDIT DATE",
                    "—"
                )

            if (
                compliance_col
                and not audit.empty
            ):

                values = pd.to_numeric(
                    audit[compliance_col]
                    .astype(str)
                    .str.replace(
                        "%",
                        "",
                        regex=False
                    ),
                    errors="coerce"
                ).dropna()

                if not values.empty:

                    value = float(
                        values.iloc[-1]
                    )

                    if value <= 1:
                        value *= 100

                    st.metric(
                        "AUDIT COMPLIANCE",
                        f"{value:.0f}%"
                    )

                else:

                    st.metric(
                        "AUDIT COMPLIANCE",
                        "—"
                    )

            else:

                st.metric(
                    "AUDIT COMPLIANCE",
                    "—"
                )

        # ====================================================
        # RIGHT SIDE
        # ====================================================

        with q2:

            # ========================================================
            # AUDIT LOGO + TITLE
            # ========================================================

            logo_col, title_col = st.columns(
                [0.30, 0.70],
                gap="small"
            )

            with logo_col:

                st.markdown(
                    """
                    <div style="
                        font-size:65px;
                        line-height:1;
                        text-align:center;
                        padding-top:5px;
                    ">
                        📋
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with title_col:

                st.markdown(
                    """
                    <div style="
                        font-size:13px;
                        font-weight:700;
                        color:#173f70;
                        padding-top:25px;
                        white-space:nowrap;
                    ">
                        View detailed Audit Compliance report
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # ========================================================
            # UPLOAD PDF
            # ========================================================

            audit_upload = st.file_uploader(
                "Upload Audit Compliance Report",
                type=["pdf"],
                key="audit_compliance_upload"
            )

            # ========================================================
            # VIEW BUTTON
            # ========================================================

            if audit_upload is not None:

                st.caption(
                    f"📄 {audit_upload.name}"
                )

                view_report = st.button(
                    "VIEW AUDIT COMPLIANCE REPORT ↗",
                    key="view_audit_report",
                    type="primary",
                    use_container_width=True
                )

                if view_report:
                    import base64

                    pdf_bytes = audit_upload.getvalue()

                    pdf_base64 = (
                        base64.b64encode(
                            pdf_bytes
                        ).decode("utf-8")
                    )


                    @st.dialog(
                        "AUDIT COMPLIANCE REPORT",
                        width="large"
                    )
                    def show_audit_report(
                            pdf_data
                    ):
                        st.markdown(
                            "### 📋 Audit Compliance Report"
                        )

                        st.markdown(
                            f"""
                            <iframe
                                src="data:application/pdf;base64,{pdf_data}"
                                width="100%"
                                height="700px">
                            </iframe>
                            """,
                            unsafe_allow_html=True
                        )


                    show_audit_report(
                        pdf_base64
                    )

            else:

                st.caption(
                    "Upload the Audit Compliance PDF "
                    "to enable the View option."
                )