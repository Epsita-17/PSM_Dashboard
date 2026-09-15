# ============================================================
# PSM SC CONVENER DASHBOARD
# All-Department Governance / Review / Action Dashboard
# Built from the existing PSM All Departments data structure
# ============================================================

import io
import re
import base64
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from openpyxl import load_workbook
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM SC Convener Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GOOGLE SHEET - SAME SOURCE AS ALL DEPARTMENTS DASHBOARD
# ============================================================
SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEETS = {
    "PT": "1997330551",
    "PHA": "1151637695",
    "PHA Recommendation": "1114420199",
    "MOC": "1493447251",
    "PSSR": "1914804736",
    "PS Incident": "354502422",
    "Training": "1071736559",
    "SOC-SOL": "510439154",
    "Interlock": "1552637895",
    "PSM CE": "1552637895",
    "Failure Data": "1071263265",
    "Barrier Audit": "1741048982",
    "Audit Compliance": "1790395364",
}

ALL_DEPARTMENTS = [
    "Blast Furnace",
    "Coke Oven",
    "SMS-1",
    "SMS-2",
    "DRI",
    "Central Utility",
    "CRM",
    "WRM",
    "CPP",
    "Sinter",
    "Tube Mill",
    "CSP",
    "Pellet & Beneficiation",
    "LCP",
]


# ============================================================
# STYLE
# ============================================================
st.markdown(
    """
<style>
.stApp { background:#f3f8fc; }
#MainMenu, footer { visibility:hidden; }

.block-container {
    padding:0.25rem 0.35rem 0rem 0.35rem !important;
    max-width:100%;
}

div[data-testid="stMetric"] {
    background:#ffffff;
    border:1px solid #cbddea;
    border-radius:7px;
    padding:7px !important;
    min-height:78px;
}

div[data-testid="stMetricLabel"] {
    font-size:9px !important;
    font-weight:800 !important;
    color:#20384f !important;
    white-space:nowrap !important;
}

div[data-testid="stMetricValue"] {
    color:#123f77 !important;
    font-size:25px !important;
    font-weight:900 !important;
}

.convener-card {
    background:#ffffff;
    border:1px solid #d3e0ea;
    border-radius:8px;
    padding:9px;
    margin-bottom:8px;
    box-shadow:0 1px 4px rgba(20,65,95,.06);
}

.section-bar {
    background:#07518b;
    color:#ffffff;
    border-radius:4px;
    padding:6px 9px;
    font-size:11px;
    font-weight:900;
    margin:3px 0 7px 0;
}

.sub-title {
    color:#173f70;
    font-size:10px;
    font-weight:900;
    margin:4px 0;
}

.live-bar {
    background:#ffffff;
    border:1px solid #cbddea;
    border-radius:5px;
    padding:5px 9px;
    color:#4f6678;
    font-size:10px;
    margin:4px 0 7px 0;
}

.priority-box {
    background:#fff8f8;
    border:1px solid #efc9c9;
    border-radius:5px;
    padding:7px;
}

.footer {
    text-align:center;
    color:#627689;
    background:#edf4f8;
    border-top:1px solid #cbdce7;
    padding:7px;
    font-size:9px;
    font-weight:800;
    margin-top:7px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================
def norm(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def find_col(df, candidates):
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


def load_csv_from_url(url):
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    return pd.read_csv(
        io.StringIO(response.content.decode("utf-8-sig"))
    )


@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(gid):
    if not gid:
        return pd.DataFrame()

    export_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=csv&gid={gid}"
    )

    try:
        return clean_dataframe(load_csv_from_url(export_url))
    except Exception:
        try:
            gviz_url = (
                f"https://docs.google.com/spreadsheets/d/"
                f"{SPREADSHEET_ID}/gviz/tq?"
                f"tqx=out:csv&gid={gid}"
            )
            return clean_dataframe(load_csv_from_url(gviz_url))
        except Exception:
            return pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def load_interlock_sheet():
    """
    Uses the same header-based discovery approach as the existing
    All Departments dashboard so the actual Interlock register is used.
    """
    xlsx_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=xlsx"
    )

    try:
        response = requests.get(
            xlsx_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        workbook = load_workbook(
            filename=io.BytesIO(response.content),
            data_only=True,
            read_only=True,
        )

        required = {
            "sno",
            "department",
            "interlockdescription",
            "datebypassed",
            "presentstatusactionrequired",
        }

        for worksheet in workbook.worksheets:
            rows = worksheet.iter_rows(values_only=True)
            buffered = []
            header_found = None

            for row_number, row in enumerate(rows):
                buffered.append(row)
                if row_number >= 9:
                    break

                headers = {
                    re.sub(
                        r"[^a-z0-9]+",
                        "",
                        str(v).strip().lower()
                    )
                    for v in row
                    if v is not None
                }

                if required.issubset(headers):
                    header_found = row_number
                    break

            if header_found is None:
                continue

            all_rows = list(buffered)
            all_rows.extend(list(rows))

            headers = list(all_rows[header_found])
            valid_columns = [
                i for i, v in enumerate(headers)
                if v is not None and str(v).strip()
            ]

            clean_headers = [
                str(headers[i]).strip()
                for i in valid_columns
            ]

            records = []
            for row in all_rows[header_found + 1:]:
                values = [
                    row[i] if i < len(row) else None
                    for i in valid_columns
                ]
                if any(
                    v is not None and str(v).strip()
                    for v in values
                ):
                    records.append(values)

            workbook.close()
            return clean_dataframe(
                pd.DataFrame(records, columns=clean_headers)
            )

        workbook.close()

    except Exception:
        pass

    return pd.DataFrame()


@st.cache_data(ttl=300, show_spinner=False)
def load_psm_ce_sheet():
    """
    Uses distinctive PSM CE headers to locate the real register.
    """
    xlsx_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export?format=xlsx"
    )

    try:
        response = requests.get(
            xlsx_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        workbook = load_workbook(
            filename=io.BytesIO(response.content),
            data_only=True,
            read_only=True,
        )

        def nh(value):
            text = str(value).strip().lower()
            text = text.replace("–", "-").replace("—", "-")
            text = text.replace("&", "and")
            return re.sub(r"[^a-z0-9]+", "", text)

        for worksheet in workbook.worksheets:
            rows = worksheet.iter_rows(values_only=True)
            buffered = []
            header_found = None

            for row_number, row in enumerate(rows):
                buffered.append(row)
                if row_number >= 9:
                    break

                h = {nh(v) for v in row if v is not None}

                if (
                    "slno" in h
                    and "month" in h
                    and "department" in h
                    and any("noofpsmcefailedbreakdown" in x for x in h)
                    and any(
                        "complianceofpsmce" in x
                        and "mechanical" in x
                        and "generated" in x
                        for x in h
                    )
                    and any(
                        "complianceofpsmce" in x
                        and "mechanical" in x
                        and "completed" in x
                        for x in h
                    )
                    and any(
                        "complianceofpsmce" in x
                        and ("ei" in x or "eandi" in x)
                        and "generated" in x
                        for x in h
                    )
                    and any(
                        "complianceofpsmce" in x
                        and ("ei" in x or "eandi" in x)
                        and "completed" in x
                        for x in h
                    )
                ):
                    header_found = row_number
                    break

            if header_found is None:
                continue

            all_rows = list(buffered)
            all_rows.extend(list(rows))

            headers = list(all_rows[header_found])
            valid_columns = [
                i for i, v in enumerate(headers)
                if v is not None and str(v).strip()
            ]

            clean_headers = [
                str(headers[i]).strip()
                for i in valid_columns
            ]

            records = []
            for row in all_rows[header_found + 1:]:
                values = [
                    row[i] if i < len(row) else None
                    for i in valid_columns
                ]
                if any(
                    v is not None and str(v).strip()
                    for v in values
                ):
                    records.append(values)

            workbook.close()
            return clean_dataframe(
                pd.DataFrame(records, columns=clean_headers)
            )

        workbook.close()

    except Exception:
        pass

    return pd.DataFrame()


def filter_department(df, department):
    df = clean_dataframe(df)

    if df.empty:
        return df

    col = find_col(
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

    if col is None:
        return df.iloc[0:0].copy()

    values = df[col].fillna("").astype(str).str.strip()
    target = norm(department)

    if target == "blastfurnace":
        mask = values.str.contains(
            r"blast\s*[-_/ ]*\s*furnace",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "cokeoven":
        mask = values.str.contains(
            r"coke\s*[-_/ ]*oven",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "sms1":
        mask = values.str.contains(
            r"sms\s*[-_/ ]*1",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "sms2":
        mask = values.str.contains(
            r"sms\s*[-_/ ]*2",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "centralutility":
        mask = values.str.contains(
            r"central\s*[-_/ ]*utility",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "tubemill":
        mask = values.str.contains(
            r"tube\s*[-_/ ]*mill",
            case=False,
            regex=True,
            na=False,
        )
    elif target == "pelletbeneficiation":
        mask = values.str.contains(
            r"pellet.*beneficiation|beneficiation.*pellet",
            case=False,
            regex=True,
            na=False,
        )
    else:
        mask = values.map(norm).eq(target)

    return df.loc[mask].copy()


def status_series(df, candidates=None):
    if df is None or df.empty:
        return pd.Series(dtype=str)

    if candidates is None:
        candidates = [
            "Status",
            "Current Status",
            "Action Status",
            "Completion Status",
            "Investigation Status",
            "Recommendation Status",
        ]

    col = find_col(df, candidates)
    if col is None:
        return pd.Series([""] * len(df), index=df.index)

    return (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


def completion_rate(df, candidates=None):
    if df is None or df.empty:
        return None

    s = status_series(df, candidates)

    if s.empty or not (s != "").any():
        return None

    completed = s.str.contains(
        r"\bcompleted?\b|\bcomplete\b|\bclosed\b|\bdone\b",
        regex=True,
        na=False,
    ).sum()

    applicable = (s != "").sum()

    return round(
        float(completed) / float(applicable) * 100,
        1,
    ) if applicable else None


def pct_text(value):
    return "—" if value is None else f"{value:.0f}%"


def status_colour(value):
    if value is None:
        return "#8a97a5"
    if value >= 90:
        return "#18864b"
    if value >= 75:
        return "#d88a00"
    return "#d71920"


def numeric_total(df, col):
    if df is None or df.empty or col is None:
        return 0
    return int(
        pd.to_numeric(df[col], errors="coerce")
        .fillna(0)
        .sum()
    )


def module_open_count(df, candidates=None):
    if df is None or df.empty:
        return 0

    s = status_series(df, candidates)

    return int(
        s.str.contains(
            r"open|pending|ongoing|in progress|overdue",
            regex=True,
            na=False,
        ).sum()
    )


def build_priority_register():
    rows = []

    def add_records(df, module, id_candidates, desc_candidates, status_candidates):
        if df is None or df.empty:
            return

        id_col = find_col(df, id_candidates)
        desc_col = find_col(df, desc_candidates)
        stat_col = find_col(df, status_candidates)

        if stat_col is None:
            return

        s = (
            df[stat_col]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        mask = s.str.contains(
            r"open|pending|ongoing|in progress|overdue",
            regex=True,
            na=False,
        )

        pending = df.loc[mask].copy()

        for _, row in pending.iterrows():
            rows.append(
                {
                    "Module": module,
                    "Department": str(
                        row[find_col(
                            df,
                            ["Department", "Departments", "Dept"]
                        )]
                    ).strip()
                    if find_col(df, ["Department", "Departments", "Dept"])
                    else "—",
                    "Reference": str(row[id_col]).strip()
                    if id_col else "—",
                    "Action / Description": str(row[desc_col]).strip()
                    if desc_col else "—",
                    "Status": str(row[stat_col]).strip(),
                }
            )

    add_records(
        rec,
        "PHA Recommendation",
        ["PHA No", "Recommendation No", "Recommendation ID", "ID"],
        ["Recommendation Description", "Recommendation", "Description"],
        [
            "Status (Open/Close)",
            "Status Open Close",
            "Open/Close Status",
            "Recommendation Status",
            "Status",
        ],
    )

    add_records(
        moc,
        "MOC",
        ["MOC No", "MOC No.", "MOC Number", "MOC ID", "Request No", "ID"],
        ["Description of Change", "MOC Description", "Change Description", "Description"],
        ["Status (Open/Close)", "Status (Open / Close)", "MOC Status", "Status"],
    )

    add_records(
        pssr,
        "PSSR",
        ["PSSR No.", "PSSR No", "PSSR ID", "ID"],
        ["PSSR Description", "Description", "PSSR Name"],
        [
            "Overdue/Pending/Completed",
            "Overdue / Pending / Completed",
            "Status",
            "Current Status",
        ],
    )

    # Interlock uses a dedicated status field.
    if interlock is not None and not interlock.empty:
        status_col = find_col(
            interlock,
            [
                "Present Status / Action Required",
                "Present Status",
                "Status / Action Required",
                "Status",
            ],
        )
        dept_col = find_col(
            interlock,
            ["Department", "Departments", "Dept"]
        )
        desc_col = find_col(
            interlock,
            ["Interlock Description", "Interlock Details", "Description"]
        )
        sno_col = find_col(
            interlock,
            ["S.No.", "S No", "S.No", "Serial No", "Sr No"]
        )

        if status_col:
            s = (
                interlock[status_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )
            mask = s.str.contains(
                r"due\s*for\s*normalization|normalization\s*pending",
                regex=True,
                na=False,
            )

            for _, row in interlock.loc[mask].iterrows():
                rows.append(
                    {
                        "Module": "Interlock Bypass",
                        "Department": str(row[dept_col]).strip()
                        if dept_col else "—",
                        "Reference": str(row[sno_col]).strip()
                        if sno_col else "—",
                        "Action / Description": str(row[desc_col]).strip()
                        if desc_col else "—",
                        "Status": str(row[status_col]).strip(),
                    }
                )

    return pd.DataFrame(rows)


# ============================================================
# LOAD DATA
# ============================================================
pt = load_google_sheet(SHEETS["PT"])
pha = load_google_sheet(SHEETS["PHA"])
rec = load_google_sheet(SHEETS["PHA Recommendation"])
moc = load_google_sheet(SHEETS["MOC"])
pssr = load_google_sheet(SHEETS["PSSR"])
incident = load_google_sheet(SHEETS["PS Incident"])
training = load_google_sheet(SHEETS["Training"])
soc = load_google_sheet(SHEETS["SOC-SOL"])
interlock = load_interlock_sheet()
psm_ce = load_psm_ce_sheet()
failure_data = load_google_sheet(SHEETS["Failure Data"])
barrier = load_google_sheet(SHEETS["Barrier Audit"])
audit = load_google_sheet(SHEETS["Audit Compliance"])


# ============================================================
# HEADER
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "jsw_jfe_logo.jpg"


def image_to_base64(path):
    try:
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        pass
    return ""


logo_base64 = image_to_base64(logo_path)
now = datetime.now()

header_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    margin:0;
    font-family:Arial,Helvetica,sans-serif;
}}
.header {{
    height:92px;
    border-radius:7px;
    overflow:hidden;
    position:relative;
    background:linear-gradient(
        90deg,#031d34 0%,#052b49 45%,#07385c 100%
    );
    box-shadow:0 3px 9px rgba(0,0,0,.18);
}}
.logo {{
    position:absolute;
    left:8px;
    top:11px;
    width:180px;
    height:68px;
    background:#fff;
    border-radius:5px;
    display:flex;
    align-items:center;
    justify-content:center;
}}
.logo img {{
    width:100%;
    height:100%;
    object-fit:contain;
}}
.title {{
    position:absolute;
    left:50%;
    top:12px;
    transform:translateX(-50%);
    text-align:center;
    color:#fff;
    white-space:nowrap;
}}
.main {{
    font-size:27px;
    font-weight:900;
    letter-spacing:.4px;
}}
.main span {{
    color:#f28c00;
}}
.sub {{
    margin-top:7px;
    font-size:12px;
    letter-spacing:3.4px;
}}
.tag {{
    margin-top:6px;
    font-size:7px;
    letter-spacing:2px;
    color:rgba(255,255,255,.82);
}}
.right {{
    position:absolute;
    right:15px;
    top:15px;
    color:#fff;
    text-align:right;
    padding-left:15px;
    border-left:2px solid rgba(255,255,255,.55);
}}
.date {{
    font-size:10px;
}}
.time {{
    margin-top:4px;
    font-size:21px;
    font-weight:800;
}}
.orange {{
    position:absolute;
    bottom:0;
    left:0;
    width:100%;
    height:4px;
    background:#f28c00;
}}
</style>
</head>
<body>
<div class="header">
    <div class="logo">
        {"<img src='data:image/jpeg;base64," + logo_base64 + "'>" if logo_base64 else ""}
    </div>

    <div class="title">
        <div class="main">SC <span>CONVENER</span></div>
        <div class="sub">PSM DIGITAL DASHBOARD</div>
        <div class="tag">GOVERNANCE &nbsp;|&nbsp; REVIEW &nbsp;|&nbsp; ACTION &nbsp;|&nbsp; COMPLIANCE</div>
    </div>

    <div class="right">
        <div class="date">{now.strftime("%d %b %Y").upper()}</div>
        <div class="time">{now.strftime("%I:%M %p")}</div>
    </div>

    <div class="orange"></div>
</div>
</body>
</html>
"""

components.html(header_html, height=108, scrolling=False)


# ============================================================
# LIVE DATA BAR
# ============================================================
available_modules = sum(
    1
    for df in [
        pt, pha, rec, moc, pssr, incident, training,
        soc, interlock, psm_ce, failure_data, barrier, audit
    ]
    if df is not None and not df.empty
)

st.markdown(
    f"""
<div class="live-bar">
<b>LIVE PSM DATA</b>
&nbsp; | &nbsp; Google Sheet
&nbsp; | &nbsp; Auto refresh: 5 min
&nbsp; | &nbsp; Modules available: <b>{available_modules}/13</b>
&nbsp; | &nbsp; Last load:
<b>{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}</b>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GLOBAL DEPARTMENT FILTER
# ============================================================

filter_col, clear_col = st.columns([5, 1], gap="small")
with filter_col:
    selected_department = st.selectbox(
        "Select Department",
        ["All Departments"] + ALL_DEPARTMENTS,
        index=0,
        key="sc_convener_department_filter",
    )

with clear_col:
    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
    if st.button("↻ ALL", use_container_width=True, key="sc_convener_clear_filter"):
        st.session_state["sc_convener_department_filter"] = "All Departments"
        st.rerun()

# Apply the selected department to every dashboard data source.
def apply_global_filter(df):
    if selected_department == "All Departments":
        return df
    return filter_department(df, selected_department)

pt = apply_global_filter(pt)
pha = apply_global_filter(pha)
rec = apply_global_filter(rec)
moc = apply_global_filter(moc)
pssr = apply_global_filter(pssr)
incident = apply_global_filter(incident)
training = apply_global_filter(training)
soc = apply_global_filter(soc)
interlock = apply_global_filter(interlock)
psm_ce = apply_global_filter(psm_ce)
failure_data = apply_global_filter(failure_data)
barrier = apply_global_filter(barrier)
audit = apply_global_filter(audit)

# The scorecard and priority register are already built from these filtered
# dataframes, so the selected department automatically propagates to them.

st.markdown(
    f'<div class="live-bar"><b>VIEW:</b> {selected_department} &nbsp; | &nbsp; All KPI, chart and register data below follow this selection.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# EXECUTIVE KPI STRIP
# ============================================================
priority = build_priority_register()

total_departments = len(ALL_DEPARTMENTS)

total_psm_records = sum(
    len(df) for df in [
        pt, pha, rec, moc, pssr, incident,
        training, soc, interlock, psm_ce,
        failure_data, barrier, audit
    ]
    if df is not None
)

open_actions = len(priority)

# PSI
incident_dept_col = find_col(
    incident,
    ["Department", "Departments", "Dept"]
)
total_incidents = (
    int(
        incident[incident_dept_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace(["", "-", "nan", "None"], pd.NA)
        .notna()
        .sum()
    )
    if incident_dept_col and not incident.empty
    else 0
)

# PSM CE
failed_col = find_col(
    psm_ce,
    [
        "No. of PSM CE failed (Breakdown)",
        "No. Of PSM CE Failed (Breakdown)",
        "PSM CE Failed",
        "PSM CE Failed (Breakdown)",
    ],
)
total_ce_failed = numeric_total(psm_ce, failed_col)

# Barrier
assessed_col = find_col(
    barrier,
    ["Barrier Health (C4/C5) (Number) Assessed", "Assessed"]
)
unacceptable_col = find_col(
    barrier,
    [
        "Barrier Health (C4/C5) (Number) Unacceptable",
        "Unacceptable Barrier",
        "Unacceptable",
    ]
)
barrier_unacceptable = numeric_total(barrier, unacceptable_col)

# Training overall
training_completion = None
if not training.empty:
    total_cols = [
        find_col(training, ["Total Employees (L08 & Above)"]),
        find_col(training, ["Total Employees (Below L08)"]),
        find_col(training, ["Total Associates"]),
        find_col(training, ["Total Contractual Workers"]),
    ]
    done_cols = [
        find_col(training, ["Completed Training (L08 & Above)"]),
        find_col(training, ["Completed Training (Below L08)"]),
        find_col(training, ["Completed Training (Associates)"]),
        find_col(training, ["Completed Training (Contracts)"]),
    ]

    if all(total_cols) and all(done_cols):
        total_people = sum(numeric_total(training, c) for c in total_cols)
        done_people = sum(numeric_total(training, c) for c in done_cols)
        if total_people:
            training_completion = round(done_people / total_people * 100, 1)

# Audit
audit_date_col = find_col(
    audit,
    ["Audit Date", "Last Audit Date", "Date"]
)
audit_done = 0
audit_pending = 0
if audit_date_col and not audit.empty:
    audit_dates = pd.to_datetime(
        audit[audit_date_col],
        errors="coerce"
    )
    audit_done = int(audit_dates.notna().sum())
    audit_pending = int(audit_dates.isna().sum())

kpi_items = [
    ("DEPARTMENTS", total_departments),
    ("PSM RECORDS", total_psm_records),
    ("OPEN / PENDING ACTIONS", open_actions),
    ("PROCESS SAFETY INCIDENTS", total_incidents),
    ("PSM CE FAILED", total_ce_failed),
    ("BARRIER UNACCEPTABLE", barrier_unacceptable),
    ("TRAINING COMPLIANCE", pct_text(training_completion)),
    ("AUDIT PENDING", audit_pending),
]

kcols = st.columns(8, gap="small")
for col, (label, value) in zip(kcols, kpi_items):
    with col:
        st.metric(label, value)


# ============================================================
# DEPARTMENT SCORECARD
# ============================================================
st.markdown(
    '<div class="section-bar">DEPARTMENT-WISE PSM GOVERNANCE SCORECARD</div>',
    unsafe_allow_html=True,
)

score_rows = []

for dept in ALL_DEPARTMENTS:
    d_pt = filter_department(pt, dept)
    d_pha = filter_department(pha, dept)
    d_rec = filter_department(rec, dept)
    d_moc = filter_department(moc, dept)
    d_pssr = filter_department(pssr, dept)
    d_inc = filter_department(incident, dept)
    d_int = filter_department(interlock, dept)
    d_bar = filter_department(barrier, dept)

    rates = [
        completion_rate(d_pt),
        completion_rate(d_pha),
        completion_rate(
            d_rec,
            [
                "Status (Open/Close)",
                "Status Open Close",
                "Open/Close Status",
                "Recommendation Status",
                "Status",
            ],
        ),
        completion_rate(d_moc),
        completion_rate(
            d_pssr,
            [
                "Overdue/Pending/Completed",
                "Overdue / Pending / Completed",
                "Status",
                "Current Status",
            ],
        ),
    ]

    valid_rates = [x for x in rates if x is not None]
    overall = round(sum(valid_rates) / len(valid_rates), 1) if valid_rates else None

    open_count = sum(
        module_open_count(x)
        for x in [d_rec, d_moc, d_pssr]
    )

    # Interlock pending normalization
    int_status_col = find_col(
        d_int,
        [
            "Present Status / Action Required",
            "Present Status",
            "Status / Action Required",
            "Status",
        ]
    )
    if int_status_col and not d_int.empty:
        int_pending = int(
            d_int[int_status_col]
            .fillna("")
            .astype(str)
            .str.contains(
                r"due\s*for\s*normalization|normalization\s*pending",
                case=False,
                regex=True,
                na=False,
            )
            .sum()
        )
        open_count += int_pending

    # Incident count
    inc_count = len(d_inc)

    # Unacceptable barriers
    bar_bad = numeric_total(d_bar, unacceptable_col)

    score_rows.append(
        {
            "Department": dept,
            "PT": pct_text(rates[0]),
            "PHA": pct_text(rates[1]),
            "PHA Rec.": pct_text(rates[2]),
            "MOC": pct_text(rates[3]),
            "PSSR": pct_text(rates[4]),
            "Open Actions": open_count,
            "PSI": inc_count,
            "Unacceptable Barrier": bar_bad,
            "Overall": pct_text(overall),
        }
    )

score_df = pd.DataFrame(score_rows)

def score_style(value):
    text = str(value).replace("%", "").strip()
    try:
        v = float(text)
    except Exception:
        return "color:#7d8995;text-align:center;"

    if v >= 90:
        return "background-color:#dff2e6;color:#176b3a;font-weight:800;text-align:center;"
    if v >= 75:
        return "background-color:#fff0cf;color:#9a6500;font-weight:800;text-align:center;"
    return "background-color:#ffe0e0;color:#b51f2a;font-weight:800;text-align:center;"

styled_score = (
    score_df.style
    .map(
        score_style,
        subset=["PT", "PHA", "PHA Rec.", "MOC", "PSSR", "Overall"]
    )
    .set_properties(
        subset=["Department"],
        **{"font-weight":"800","color":"#173f70"}
    )
)

st.dataframe(
    styled_score,
    use_container_width=True,
    hide_index=True,
    height=390,
    column_config={
        "Department": st.column_config.TextColumn("Department"),
        "PT": st.column_config.TextColumn("PT"),
        "PHA": st.column_config.TextColumn("PHA"),
        "PHA Rec.": st.column_config.TextColumn("PHA Rec."),
        "MOC": st.column_config.TextColumn("MOC"),
        "PSSR": st.column_config.TextColumn("PSSR"),
        "Open Actions": st.column_config.NumberColumn("Open Actions"),
        "PSI": st.column_config.NumberColumn("PSI"),
        "Unacceptable Barrier": st.column_config.NumberColumn("Unacceptable Barrier"),
        "Overall": st.column_config.TextColumn("Overall PSM"),
    },
)


# ============================================================
# PRIORITY ACTIONS + RISK SNAPSHOT
# ============================================================
left, right = st.columns([1.45, 1], gap="small")


# ------------------------------------------------------------
# PRIORITY ACTION REGISTER
# ------------------------------------------------------------
with left:
    with st.container(border=True):
        st.markdown(
            '<div class="section-bar">SC CONVENER PRIORITY ACTION REGISTER</div>',
            unsafe_allow_html=True,
        )

        if priority.empty:
            st.success("No open / pending action records found.")
        else:
            priority = priority.copy()

            def priority_style(v):
                t = str(v).lower()
                if "overdue" in t:
                    return "background-color:#ffdede;color:#b51f2a;font-weight:800;"
                if "pending" in t or "open" in t:
                    return "background-color:#fff0cf;color:#9a6500;font-weight:800;"
                return ""

            priority_styled = priority.style.map(
                priority_style,
                subset=["Status"]
            )

            st.dataframe(
                priority_styled,
                use_container_width=True,
                hide_index=True,
                height=330,
                column_config={
                    "Module": st.column_config.TextColumn("Module"),
                    "Department": st.column_config.TextColumn("Department"),
                    "Reference": st.column_config.TextColumn("Ref."),
                    "Action / Description": st.column_config.TextColumn("Action / Description"),
                    "Status": st.column_config.TextColumn("Status"),
                },
            )


# ------------------------------------------------------------
# RISK SNAPSHOT
# ------------------------------------------------------------
with right:
    with st.container(border=True):
        st.markdown(
            '<div class="section-bar">PROCESS SAFETY RISK SNAPSHOT</div>',
            unsafe_allow_html=True,
        )

        # Incident classification
        classification_col = find_col(
            incident,
            [
                "Incident Classification",
                "Incident classification",
                "Classification",
            ],
        )

        level_col = find_col(
            incident,
            [
                "Incident Level",
                "Incident level",
                "Level",
            ],
        )

        if classification_col and not incident.empty:
            vals = (
                incident[classification_col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )
            vals = vals[vals != ""]

            def standard_classification(x):
                if "serious" in x and "process" in x and "incident" in x:
                    return "Serious Process Incident"
                if "process" in x and "incident" in x:
                    return "Process Incident"
                if "near" in x and "miss" in x:
                    return "Near Miss"
                return x.title()

            counts = vals.map(standard_classification).value_counts()

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=counts.values,
                        y=counts.index,
                        orientation="h",
                        text=counts.values,
                        textposition="outside",
                    )
                ]
            )
            fig.update_layout(
                height=170,
                margin=dict(l=5,r=20,t=5,b=5),
                showlegend=False,
                font=dict(size=9),
                xaxis=dict(dtick=1, showgrid=True),
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar":False},
            )

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("INCIDENTS", total_incidents)
        with r2:
            st.metric("PSM CE FAILED", total_ce_failed)
        with r3:
            st.metric("BARRIER UNACCEPTABLE", barrier_unacceptable)


# ============================================================
# TRAINING + PSM CE
# ============================================================
left, right = st.columns([1, 1], gap="small")


# ------------------------------------------------------------
# TRAINING
# ------------------------------------------------------------
with left:
    with st.container(border=True):
        st.markdown(
            '<div class="section-bar">TRAINING COMPLIANCE BY DEPARTMENT</div>',
            unsafe_allow_html=True,
        )

        if training.empty:
            st.info("No training data available.")
        else:
            dept_col = find_col(
                training,
                ["Department", "Departments", "Dept"]
            )
            process_col = find_col(training, ["Process"])

            total_cols = [
                find_col(training, ["Total Employees (L08 & Above)"]),
                find_col(training, ["Total Employees (Below L08)"]),
                find_col(training, ["Total Associates"]),
                find_col(training, ["Total Contractual Workers"]),
            ]
            done_cols = [
                find_col(training, ["Completed Training (L08 & Above)"]),
                find_col(training, ["Completed Training (Below L08)"]),
                find_col(training, ["Completed Training (Associates)"]),
                find_col(training, ["Completed Training (Contracts)"]),
            ]

            if dept_col and all(total_cols) and all(done_cols):
                tr = training.copy()

                for c in total_cols + done_cols:
                    tr[c] = pd.to_numeric(
                        tr[c].astype(str)
                        .str.replace(",", "", regex=False)
                        .str.replace("%", "", regex=False),
                        errors="coerce",
                    ).fillna(0)

                tr["Total"] = tr[total_cols].sum(axis=1)
                tr["Completed"] = tr[done_cols].sum(axis=1)

                tr["Compliance"] = (
                    tr["Completed"]
                    .div(tr["Total"].replace(0, pd.NA))
                    .mul(100)
                )

                train_dept = (
                    tr.groupby(dept_col, dropna=True)
                    .agg(
                        Total=("Total","sum"),
                        Completed=("Completed","sum")
                    )
                    .reset_index()
                )

                train_dept["Compliance"] = (
                    train_dept["Completed"]
                    .div(train_dept["Total"].replace(0,pd.NA))
                    .mul(100)
                    .round(1)
                )

                train_dept = train_dept.rename(
                    columns={dept_col:"Department"}
                )
                train_dept["Compliance"] = train_dept["Compliance"].apply(
                    lambda x: "—" if pd.isna(x) else f"{x:.0f}%"
                )

                st.dataframe(
                    train_dept[
                        ["Department","Total","Completed","Compliance"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                    height=300,
                )
            else:
                st.warning("Training columns could not be mapped.")


# ------------------------------------------------------------
# PSM CE
# ------------------------------------------------------------
with right:
    with st.container(border=True):
        st.markdown(
            '<div class="section-bar">PSM CE COMPLETION — DEPARTMENT VIEW</div>',
            unsafe_allow_html=True,
        )

        if psm_ce.empty:
            st.info("No PSM CE data available.")
        else:
            dept_col = find_col(psm_ce, ["Department","Dept"])

            mech_gen = find_col(
                psm_ce,
                [
                    "Compliance of PSM CE MO – Mechanical – Generated",
                    "Compliance of PSM CE MO - Mechanical - Generated",
                    "PSM CE MO Mechanical Generated",
                ]
            )
            mech_done = find_col(
                psm_ce,
                [
                    "Compliance of PSM CE MO – Mechanical – Completed",
                    "Compliance of PSM CE MO - Mechanical - Completed",
                    "PSM CE MO Mechanical Completed",
                ]
            )
            ei_gen = find_col(
                psm_ce,
                [
                    "Compliance of PSM CE MO – E&I – Generated",
                    "Compliance of PSM CE MO - E&I - Generated",
                    "PSM CE MO E&I Generated",
                ]
            )
            ei_done = find_col(
                psm_ce,
                [
                    "Compliance of PSM CE MO – E&I – Completed",
                    "Compliance of PSM CE MO - E&I - Completed",
                    "PSM CE MO E&I Completed",
                ]
            )

            if dept_col:
                ce = pd.DataFrame({
                    "Department": psm_ce[dept_col]
                    .fillna("")
                    .astype(str)
                    .str.strip(),
                    "M Generated": pd.to_numeric(
                        psm_ce[mech_gen], errors="coerce"
                    ).fillna(0) if mech_gen else 0,
                    "M Completed": pd.to_numeric(
                        psm_ce[mech_done], errors="coerce"
                    ).fillna(0) if mech_done else 0,
                    "E&I Generated": pd.to_numeric(
                        psm_ce[ei_gen], errors="coerce"
                    ).fillna(0) if ei_gen else 0,
                    "E&I Completed": pd.to_numeric(
                        psm_ce[ei_done], errors="coerce"
                    ).fillna(0) if ei_done else 0,
                })

                ce = (
                    ce.groupby("Department", as_index=False)
                    [["M Generated","M Completed","E&I Generated","E&I Completed"]]
                    .sum()
                )

                ce = ce[ce["Department"] != ""]

                ce["M %"] = (
                    ce["M Completed"]
                    .div(ce["M Generated"].replace(0,pd.NA))
                    .mul(100)
                )
                ce["E&I %"] = (
                    ce["E&I Completed"]
                    .div(ce["E&I Generated"].replace(0,pd.NA))
                    .mul(100)
                )

                display_ce = ce[
                    ["Department","M %","E&I %"]
                ].copy()

                for c in ["M %","E&I %"]:
                    display_ce[c] = display_ce[c].apply(
                        lambda x: "—" if pd.isna(x) else f"{x:.0f}%"
                    )

                st.dataframe(
                    display_ce,
                    use_container_width=True,
                    hide_index=True,
                    height=300,
                )


# ============================================================
# SOC / SOL MONTHLY TREND
# ============================================================
with st.container(border=True):
    st.markdown(
        '<div class="section-bar">SOC / SOL DEVIATION — MONTHLY TREND</div>',
        unsafe_allow_html=True,
    )

    if soc.empty:
        st.info("No SOC / SOL data available.")
    else:
        month_col = find_col(soc, ["Month"])
        soc_col = find_col(
            soc,
            ["SOC Deviation","SOC Deviation Nos.","SOC Deviation No.","SOC"]
        )
        sol_col = find_col(
            soc,
            ["SOL Deviation","SOL Deviation Nos.","SOL Deviation No.","SOL"]
        )

        if month_col and soc_col and sol_col:
            trend = pd.DataFrame({
                "Month": soc[month_col].fillna("").astype(str).str.strip(),
                "SOC": pd.to_numeric(soc[soc_col], errors="coerce").fillna(0),
                "SOL": pd.to_numeric(soc[sol_col], errors="coerce").fillna(0),
            })

            trend = (
                trend[trend["Month"] != ""]
                .groupby("Month", as_index=False)[["SOC","SOL"]]
                .sum()
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=trend["Month"],
                    y=trend["SOC"],
                    mode="lines+markers+text",
                    name="SOC",
                    text=trend["SOC"].astype(int),
                    textposition="top center",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=trend["Month"],
                    y=trend["SOL"],
                    mode="lines+markers+text",
                    name="SOL",
                    text=trend["SOL"].astype(int),
                    textposition="top center",
                )
            )

            fig.update_layout(
                height=260,
                margin=dict(l=45,r=20,t=15,b=55),
                font=dict(size=9),
                hovermode="x unified",
                xaxis=dict(tickangle=-35, showgrid=False),
                yaxis=dict(
                    title="No. of Deviations",
                    rangemode="tozero",
                    showgrid=True,
                ),
                legend=dict(
                    orientation="h",
                    y=1.05,
                    x=1,
                    xanchor="right"
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar":False},
            )
        else:
            st.warning("SOC / SOL columns could not be mapped.")


# ============================================================
# CONVENER REVIEW MESSAGE
# ============================================================
with st.container(border=True):
    st.markdown(
        '<div class="section-bar">SC CONVENER REVIEW FOCUS</div>',
        unsafe_allow_html=True,
    )

    focus_cols = st.columns(4, gap="small")

    focus_data = [
        (
            "ACTION CLOSURE",
            f"{open_actions:,} open / pending records",
            "Review ownership and target dates."
        ),
        (
            "PROCESS SAFETY",
            f"{total_incidents:,} process safety incidents",
            "Review classification, level and investigation status."
        ),
        (
            "BARRIER / PSM CE",
            f"{barrier_unacceptable:,} unacceptable barriers",
            "Prioritise weak / failed protection layers."
        ),
        (
            "PEOPLE / COMPETENCY",
            f"{pct_text(training_completion)} training compliance",
            "Focus on departments below the required target."
        ),
    ]

    for col, (title, value, note) in zip(focus_cols, focus_data):
        with col:
            st.markdown(
                f"""
                <div class="priority-box">
                    <div style="font-size:10px;font-weight:900;color:#173f70;">
                        {title}
                    </div>
                    <div style="font-size:17px;font-weight:900;color:#123f77;margin-top:4px;">
                        {value}
                    </div>
                    <div style="font-size:9px;color:#627689;margin-top:4px;">
                        {note}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
# ============================================================
# PSM MODULE NAVIGATION
# ============================================================

st.markdown("""
<style>

/* =========================================================
   PSM NAVIGATION HEADER
   ========================================================= */

.psm-nav-title {
    width: 100%;
    box-sizing: border-box;

    background: linear-gradient(
        90deg,
        #073f78 0%,
        #07518b 55%,
        #0b6096 100%
    );

    color: #ffffff;

    border-radius: 9px;

    padding: 10px 16px;

    margin: 6px 0 9px 0;

    min-height: 46px;

    font-size: 12px;
    font-weight: 900;

    letter-spacing: 0.5px;

    box-shadow:
        0 3px 9px rgba(15, 60, 95, 0.16);

    line-height: 26px;
}


/* Instruction text */

.psm-nav-title .nav-instruction {
    float: right;

    color: rgba(255, 255, 255, 0.82);

    font-size: 8px;

    font-weight: 700;

    letter-spacing: 0.3px;

    line-height: 26px;
}

/* =========================================================
   PAGE LINK CARD
   ========================================================= */

/* Outer Streamlit page-link block */
div[data-testid="stPageLink"] {
    margin: 0 !important;
    padding: 0 !important;
}


/* Actual clickable card */
div[data-testid="stPageLink"] a {
    position: relative !important;

    display: flex !important;

    align-items: center !important;

    justify-content: flex-start !important;

    width: 100% !important;

    min-height: 58px !important;

    box-sizing: border-box !important;

    padding: 9px 10px 9px 13px !important;

    background: #ffffff !important;

    border: 1px solid #d5e2ec !important;

    border-radius: 9px !important;

    color: #073f78 !important;

    text-decoration: none !important;

    box-shadow:
        0 2px 7px rgba(20, 65, 95, 0.08) !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease,
        background 0.18s ease !important;

    overflow: hidden !important;
}


/* =========================================================
   BLUE ACCENT STRIPE
   ========================================================= */

div[data-testid="stPageLink"] a::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background: #1261a0;

    border-radius: 9px 0 0 9px;
}


/* =========================================================
   HOVER EFFECT
   ========================================================= */

div[data-testid="stPageLink"] a:hover {

    transform: translateY(-3px) !important;

    background: #f8fbfe !important;

    border-color: #8eb6d2 !important;

    box-shadow:
        0 7px 15px rgba(18, 63, 100, 0.15) !important;
}


/* =========================================================
   PAGE LINK TEXT
   ========================================================= */

div[data-testid="stPageLink"] a p {

    margin: 0 !important;

    padding: 0 !important;

    color: #173f70 !important;

    font-size: 9px !important;

    font-weight: 900 !important;

    letter-spacing: 0.1px !important;

    white-space: nowrap !important;
}


/* =========================================================
   ICON
   ========================================================= */

div[data-testid="stPageLink"] a svg {

    width: 18px !important;

    height: 18px !important;

    margin-right: 6px !important;

    flex-shrink: 0 !important;
}


/* =========================================================
   REMOVE STREAMLIT EXCESS SPACING
   ========================================================= */

div[data-testid="stPageLink"] + div {
    margin-top: 0 !important;
}


/* =========================================================
   COLUMN SPACING
   ========================================================= */

div[data-testid="column"] {
    padding-left: 3px !important;
    padding-right: 3px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVIGATION HEADER
# ============================================================

st.markdown(
    """
    <div class="psm-nav-title">
        🔴 &nbsp; PSM MODULE NAVIGATION
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <span class="nav-instruction">
            CLICK A MODULE FOR DETAILED VIEW
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# MODULE NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4, nav5, nav6, nav7, nav8 = st.columns(
    8,
    gap="small"
)


with nav1:
    st.page_link(
        "pages/09_PT.py",
        label="PT",
        icon="📋"
    )


with nav2:
    st.page_link(
        "pages/10_PHA.py",
        label="PHA",
        icon="⚠️"
    )


with nav3:
    st.page_link(
        "pages/11_MOC.py",
        label="MOC",
        icon="🔄"
    )


with nav4:
    st.page_link(
        "pages/12_PSSR.py",
        label="PSSR",
        icon="🚀"
    )


with nav5:
    st.page_link(
        "pages/13_Training.py",
        label="TRAINING",
        icon="🎓"
    )


with nav6:
    st.page_link(
        "pages/14_PSI.py",
        label="PS INCIDENT",
        icon="🚨"
    )


with nav7:
    st.page_link(
        "pages/19_ALARM_&_INTERLOCK_MANAGEMENT.py",
        label="INTERLOCK",
        icon="⚙️"
    )


with nav8:
    st.page_link(
        "pages/20_PSM CE & BARRIER HEALTH.py",
        label="PSM CE / BARRIER",
        icon="🛡️"
    )
# ============================================================
# FOOTER
# ============================================================
st.markdown(
    f"""
<div class="footer">
PSM DIGITAL VISION WALL | SC CONVENER | ALL DEPARTMENTS |
LIVE GOOGLE SHEET DATA | LAST REFRESH {datetime.now().strftime("%d-%b-%Y %H:%M:%S")}
</div>
""",
    unsafe_allow_html=True,
)
