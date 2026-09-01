import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import math

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="PSM Chairman Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# PATH
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DEPT_DIR = BASE_DIR / "data" / "departments"

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
.stApp{background:#eef4f8;}
.block-container{max-width:100%;padding:.45rem .55rem;}

.top{
    background:linear-gradient(100deg,#062c4b,#0c879a);
    border:2px solid #00a9d6;border-radius:12px;
    color:#fff;text-align:center;padding:12px 10px 10px;
}
.top-main{font-size:18px;font-weight:900;letter-spacing:.4px;}
.top-title{font-size:27px;font-weight:950;color:#ffd000;margin-top:3px;}
.top-sub{font-size:13px;font-weight:800;margin-top:2px;}
.online{
    display:inline-block;margin-top:7px;padding:4px 18px;
    border:1px solid #00e676;border-radius:20px;
    color:#6dff9a;background:#063f2c;font-weight:900;
}
.dot{color:#48ef8b;}

.sec{
    background:linear-gradient(90deg,#075879,#0c879a);
    color:#fff;text-align:center;font-weight:950;
    padding:8px;border-radius:7px;margin:7px 0 5px;
}

.card{
    background:#fff;border:1px solid #c2d5e0;border-radius:8px;
    padding:10px;text-align:center;min-height:82px;
}
.card-label{font-size:10px;font-weight:900;color:#31556c;}
.card-value{font-size:25px;font-weight:950;color:#123a56;margin-top:5px;}
.card-target{font-size:10px;color:#547286;margin-top:3px;}

.note{
    background:#e7f5ec;border:1px solid #55c58a;color:#075c39;
    border-radius:7px;padding:7px 10px;font-size:12px;font-weight:800;
}
.warn{
    background:#fff3d6;border:1px solid #e5b649;color:#765000;
    border-radius:7px;padding:7px 10px;font-size:12px;font-weight:800;
}

.pillar{
    background:#fff;border:1px solid #c3d6e1;border-radius:8px;
    padding:9px;text-align:center;min-height:105px;
}
.pn{font-size:10px;font-weight:900;color:#385a70;}
.pname{font-size:12px;font-weight:900;color:#153b55;min-height:30px;}
.pscore{font-size:24px;font-weight:950;margin-top:3px;}
.good{color:#198b35;}
.amber{color:#d88a00;}
.bad{color:#d92626;}
.na{color:#758695;}

table{font-size:12px;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================
def clean_num(v):
    if v is None:
        return 0.0
    try:
        if isinstance(v, str):
            v = v.replace(",", "").replace("%", "").strip()
        x = float(v)
        if math.isnan(x):
            return 0.0
        return x
    except Exception:
        return 0.0

def fmt(v):
    x = clean_num(v)
    return f"{x:.0f}" if x.is_integer() else f"{x:.1f}"

def ratio_score(actual, plan):
    plan = clean_num(plan)
    actual = clean_num(actual)
    if plan <= 0:
        return None
    return max(0, min(100, actual / plan * 100))

def status_class(score):
    if score is None:
        return "na"
    if score >= 90:
        return "good"
    if score >= 70:
        return "amber"
    return "bad"

def find_workbook_files():
    if not DEPT_DIR.exists():
        return []
    return sorted(
        p for p in DEPT_DIR.glob("*.xlsx")
        if not p.name.startswith("~$")
    )

@st.cache_data(ttl=30)
def read_department_files():
    result = {}
    for path in find_workbook_files():
        try:
            xls = pd.ExcelFile(path)
            if "PSM Dashboard" in xls.sheet_names:
                # Header=None is intentional because the supplied
                # department tracker uses multiple header rows.
                df = pd.read_excel(path, sheet_name="PSM Dashboard", header=None)
                result[path.stem] = df
        except Exception:
            pass
    return result

def get_row(df, label):
    if df.empty:
        return None
    for i in range(len(df)):
        for j in range(min(df.shape[1], 3)):
            value = str(df.iat[i, j]).strip().lower()
            if value == label.lower():
                return i
    return None

def cell(df, row, col):
    if row is None or row >= len(df) or col >= df.shape[1]:
        return 0
    return clean_num(df.iat[row, col])

# ============================================================
# LOAD REAL DATA
# ============================================================
files = read_department_files()

st.markdown("""
<div class="top">
    <div class="top-main">PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL</div>
    <div class="top-title">SCREEN 06 : PSM CHAIRMAN DASHBOARD</div>
    <div class="top-sub">
        Strategic Oversight | Governance Leadership | Risk Management | Performance Excellence
    </div>
    <div class="online"><span class="dot">●</span> PLANT STATUS : ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DEPARTMENT SELECTOR
# ============================================================
names = list(files.keys())

if names:
    selected = st.selectbox(
        "SELECT DEPARTMENT",
        ["All Departments"] + names,
        key="chairman_department"
    )
else:
    selected = "All Departments"

if selected == "All Departments":
    selected_files = files
else:
    selected_files = {selected: files[selected]}

# ============================================================
# AGGREGATION FROM THE REAL DEPARTMENT SHEETS
# ============================================================
# Row 5 in the supplied tracker = For the Month
# Row 6 in the supplied tracker = Year till date
month_label = "For the Month"
ytd_label = "Year till date"

month_values = {}
ytd_values = {}

for dept, df in selected_files.items():
    mr = get_row(df, month_label)
    yr = get_row(df, ytd_label)

    # Actual tracker column positions (0-based), based on the
    # supplied PSM Dashboard department sheet.
    cols = {
        "inc_l1": 1, "inc_l2": 2, "inc_l3": 3, "inc_l4": 4,
        "pending_inv": 5,
        "soc": 6, "sol": 7,
        "critical_failed": 8,
        "mech_gen": 9, "mech_done": 10,
        "iem_gen": 11, "iem_done": 12,
        "z01_open_mech": 13, "z01_closed_mech": 14,
        "z01_open_iem": 15, "z01_closed_iem": 16,
        "barrier_plan": 17, "barrier_actual": 18,
        "barrier_total": 19, "barrier_assessed": 20,
        "barrier_unacceptable": 21,
        "tabletop_plan": 22, "tabletop_actual": 23,
        "third_close": 1, "third_delayed": 2,
        "incident_rec_close": 3, "incident_rec_delayed": 4,
        "rcfa_overdue": 5,
        "pt_plan": 6, "pt_actual": 7,
        "pha_plan": 8, "pha_actual": 9,
        "pha_rec_close": 10, "pha_rec_delayed": 11,
        "audit_close": 12, "audit_delayed": 13,
        "moc_pending15": 14,
        "moc_kaizen": 16,
        "emergency_moc": 18,
        "temp_moc_overdue": 20,
        "bypass_open": 22,
        "normalisation_overdue": 23,
    }

    for k, c in cols.items():
        month_values[k] = month_values.get(k, 0) + cell(df, mr, c)
        ytd_values[k] = ytd_values.get(k, 0) + cell(df, yr, c)

# ============================================================
# TOP CARDS
# ============================================================
now = datetime.now()

c1, c2, c3, c4 = st.columns(4)

for col, label, value, target in [
    (c1, "DATE", now.strftime("%d-%b-%Y"), "Local system date"),
    (c2, "TIME", now.strftime("%I:%M:%S %p"), "Live application time"),
    (c3, "SELECTED DEPARTMENT", selected, "Real department workbook"),
    (c4, "REAL EXCEL FILES", len(selected_files), "Department files loaded"),
]:
    with col:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{label}</div>
                <div class="card-value" style="font-size:22px;">{value}</div>
                <div class="card-target">{target}</div>
            </div>""",
            unsafe_allow_html=True
        )

if files:
    st.markdown(
        f'<div class="note">🟢 REAL EXCEL DATA LOADED • '
        f'{len(selected_files)} department file(s) selected • '
        f'All values below are calculated from the department tracker.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="warn">🟡 No usable department Excel file found in '
        'data/departments. Put the department .xlsx files there.</div>',
        unsafe_allow_html=True
    )

# ============================================================
# 1. OVERALL PSM HEALTH INDEX
# ============================================================
st.markdown('<div class="sec">1. OVERALL PSM HEALTH INDEX</div>', unsafe_allow_html=True)

# Data-derived health indicators from the supplied tracker.
scores = []

for actual_key, plan_key in [
    ("pt_actual", "pt_plan"),
    ("pha_actual", "pha_plan"),
    ("barrier_actual", "barrier_plan"),
    ("tabletop_actual", "tabletop_plan"),
]:
    s = ratio_score(month_values.get(actual_key), month_values.get(plan_key))
    if s is not None:
        scores.append(s)

# Incident / overdue components: zero is best.
overdue_items = (
    month_values.get("pending_inv", 0)
    + month_values.get("rcfa_overdue", 0)
    + month_values.get("temp_moc_overdue", 0)
    + month_values.get("normalisation_overdue", 0)
)

if scores:
    health = sum(scores) / len(scores)
    # Penalise open/overdue items without creating a score when no data exists.
    health = max(0, min(100, health - min(overdue_items * 2, 20)))
    health_text = f"{health:.1f}%"
else:
    health = None
    health_text = "N/A"

a, b, c, d = st.columns(4)

cards = [
    ("OVERALL PSM SCORE", health_text, "Calculated from available tracker metrics"),
    ("LAST MONTH", "N/A", "No historical score column in department tracker"),
    ("LAST YEAR", "N/A", "No historical score column in department tracker"),
    ("OVERDUE / OPEN ITEMS", fmt(overdue_items), "Real tracker count"),
]

for col, (lab, val, sub) in zip([a,b,c,d], cards):
    with col:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{lab}</div>
                <div class="card-value">{val}</div>
                <div class="card-target">{sub}</div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 2. 14 PILLARS
# ============================================================
st.markdown('<div class="sec">2. PSM PILLAR SUMMARY — 14 PILLARS</div>', unsafe_allow_html=True)

# These are the standard dashboard pillar names. Scores are only
# calculated where a direct compliance ratio exists in the tracker.
pillars = [
    ("Process Safety Information", None),
    ("Process Hazard Analysis", ratio_score(month_values.get("pha_actual"), month_values.get("pha_plan"))),
    ("Operating Procedures", ratio_score(month_values.get("pt_actual"), month_values.get("pt_plan"))),
    ("Mechanical Integrity", ratio_score(
        month_values.get("mech_done") + month_values.get("iem_done"),
        month_values.get("mech_gen") + month_values.get("iem_gen")
    )),
    ("Training & Competency", None),
    ("Management of Change", None),
    ("Pre-Startup Safety Review", None),
    ("Contractor Safety", None),
    ("Emergency Preparedness", ratio_score(month_values.get("tabletop_actual"), month_values.get("tabletop_plan"))),
    ("Incident Investigation", ratio_score(
        month_values.get("incident_rec_close"),
        month_values.get("incident_rec_close") + month_values.get("incident_rec_delayed")
    )),
    ("Compliance & Audit", ratio_score(
        month_values.get("audit_close"),
        month_values.get("audit_close") + month_values.get("audit_delayed")
    )),
    ("Risk Management", ratio_score(
        month_values.get("barrier_assessed"),
        month_values.get("barrier_total")
    )),
    ("Management Review", None),
    ("PSM Governance", ratio_score(
        month_values.get("third_close"),
        month_values.get("third_close") + month_values.get("third_delayed")
    )),
]

cols = st.columns(2)

for i, (name, score) in enumerate(pillars):
    cls = status_class(score)
    text = "N/A" if score is None else f"{score:.0f}%"
    target = (
        "Data not available in current tracker"
        if score is None
        else ("≥ 90% Excellent" if score >= 90 else "70–89% Needs Attention" if score >= 70 else "< 70% Poor")
    )

    with cols[i % 2]:
        st.markdown(
            f"""<div class="pillar">
                <div class="pn">PILLAR {i+1}</div>
                <div class="pname">{name}</div>
                <div class="pscore {cls}">{text}</div>
                <div class="card-target">{target}</div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 3. STRATEGIC PRIORITY TRACKER
# ============================================================
st.markdown('<div class="sec">3. STRATEGIC PRIORITY TRACKER — CHAIRMAN VIEW</div>', unsafe_allow_html=True)

priority = pd.DataFrame([
    ["Process Safety Incidents", fmt(sum(month_values.get(k,0) for k in ["inc_l1","inc_l2","inc_l3","inc_l4"]))],
    ["Investigation Pending >30 Days", fmt(month_values.get("pending_inv",0))],
    ["PSM Critical Equipment Failures", fmt(month_values.get("critical_failed",0))],
    ["Barrier Unacceptable", fmt(month_values.get("barrier_unacceptable",0))],
    ["MOC Pending >15 Days", fmt(month_values.get("moc_pending15",0))],
    ["Interlock Bypass Open", fmt(month_values.get("bypass_open",0))],
    ["Normalisation Overdue", fmt(month_values.get("normalisation_overdue",0))],
], columns=["Priority Area", "Real Current Value"])

st.dataframe(priority, use_container_width=True, hide_index=True)

# ============================================================
# 4. KEY PERFORMANCE INDICATORS
# ============================================================
st.markdown('<div class="sec">4. KEY PERFORMANCE INDICATORS — REAL DATA</div>', unsafe_allow_html=True)

kpis = [
    ("PROCESS SAFETY INCIDENTS",
     sum(month_values.get(k,0) for k in ["inc_l1","inc_l2","inc_l3","inc_l4"])),
    ("INVESTIGATION PENDING >30 DAYS", month_values.get("pending_inv",0)),
    ("PSM CRITICAL EQUIPMENT FAILED", month_values.get("critical_failed",0)),
    ("PHA ON SCHEDULE", ratio_score(month_values.get("pha_actual"), month_values.get("pha_plan"))),
    ("PT ON SCHEDULE", ratio_score(month_values.get("pt_actual"), month_values.get("pt_plan"))),
    ("BARRIER HEALTH ASSESSED", ratio_score(month_values.get("barrier_assessed"), month_values.get("barrier_total"))),
]

kc = st.columns(3)
for i, (lab, val) in enumerate(kpis):
    value = "N/A" if val is None else (f"{val:.1f}%" if isinstance(val,float) and val <= 100 else fmt(val))
    with kc[i % 3]:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{lab}</div>
                <div class="card-value">{value}</div>
                <div class="card-target">Real Excel value</div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 5. DEPARTMENT PERFORMANCE
# ============================================================
st.markdown('<div class="sec">5. DEPARTMENT PERFORMANCE MATRIX</div>', unsafe_allow_html=True)

dept_rows = []

for dept, df in files.items():
    mr = get_row(df, month_label)

    pt_plan = cell(df, mr, 6)
    pt_actual = cell(df, mr, 7)
    pha_plan = cell(df, mr, 8)
    pha_actual = cell(df, mr, 9)

    parts = [
        s for s in [
            ratio_score(pt_actual, pt_plan),
            ratio_score(pha_actual, pha_plan)
        ] if s is not None
    ]

    score = sum(parts) / len(parts) if parts else None

    dept_rows.append({
        "Department": dept,
        "PSM Score": "N/A" if score is None else round(score, 1),
        "PT Plan": pt_plan,
        "PT Actual": pt_actual,
        "PHA Plan": pha_plan,
        "PHA Actual": pha_actual,
    })

st.dataframe(
    pd.DataFrame(dept_rows),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# 6. OVERDUE / CRITICAL ACTIONS
# ============================================================
st.markdown('<div class="sec">6. TOP OVERDUE / CRITICAL ITEMS</div>', unsafe_allow_html=True)

actions = pd.DataFrame([
    ["Investigation pending >30 days", month_values.get("pending_inv",0)],
    ["RCFA actions overdue", month_values.get("rcfa_overdue",0)],
    ["Temporary MOC restoration overdue", month_values.get("temp_moc_overdue",0)],
    ["Normalisation overdue", month_values.get("normalisation_overdue",0)],
    ["PHA recommendations delayed", month_values.get("pha_rec_delayed",0)],
    ["Audit recommendations delayed", month_values.get("audit_delayed",0)],
    ["Third-party recommendations delayed", month_values.get("third_delayed",0)],
], columns=["Action / Issue", "Count"])

st.dataframe(actions, use_container_width=True, hide_index=True)

# ============================================================
# 7. RISK / BARRIER EXPOSURE
# ============================================================
st.markdown('<div class="sec">7. RISK / BARRIER EXPOSURE SUMMARY</div>', unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

risk_cards = [
    ("TOTAL BARRIERS", month_values.get("barrier_total",0)),
    ("ASSESSED", month_values.get("barrier_assessed",0)),
    ("UNACCEPTABLE", month_values.get("barrier_unacceptable",0)),
    ("OPEN / BYPASS", month_values.get("bypass_open",0)),
]

for col, (lab, val) in zip([r1,r2,r3,r4], risk_cards):
    with col:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{lab}</div>
                <div class="card-value">{fmt(val)}</div>
                <div class="card-target">Real Excel value</div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 8. INCIDENT SUMMARY
# ============================================================
st.markdown('<div class="sec">8. INCIDENT SUMMARY — REAL DATA</div>', unsafe_allow_html=True)

inc = pd.DataFrame([
    ["Level 1", month_values.get("inc_l1",0)],
    ["Level 2", month_values.get("inc_l2",0)],
    ["Level 3", month_values.get("inc_l3",0)],
    ["Level 4", month_values.get("inc_l4",0)],
], columns=["Incident Level", "For the Month"])

st.dataframe(inc, use_container_width=True, hide_index=True)

# ============================================================
# 9. BUDGET / MOC
# ============================================================
st.markdown('<div class="sec">9. MOC / GOVERNANCE UTILIZATION</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

for col, (lab, val) in zip(
    [m1,m2,m3,m4],
    [
        ("MOC PENDING >15 DAYS", month_values.get("moc_pending15",0)),
        ("KAIZEN MOC", month_values.get("moc_kaizen",0)),
        ("EMERGENCY / TEMP MOC", month_values.get("emergency_moc",0)),
        ("TEMP MOC OVERDUE", month_values.get("temp_moc_overdue",0)),
    ]
):
    with col:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{lab}</div>
                <div class="card-value">{fmt(val)}</div>
                <div class="card-target">Real Excel value</div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 10. COMMITTEE / TABLE TOP
# ============================================================
st.markdown('<div class="sec">10. COMMITTEE / TABLE TOP EXERCISE OVERVIEW</div>', unsafe_allow_html=True)

t1, t2 = st.columns(2)

for col, lab, actual, plan in [
    (t1, "TABLE TOP EXERCISE", month_values.get("tabletop_actual",0), month_values.get("tabletop_plan",0)),
    (t2, "BARRIER AUDIT", month_values.get("barrier_actual",0), month_values.get("barrier_plan",0)),
]:
    score = ratio_score(actual, plan)
    with col:
        st.markdown(
            f"""<div class="card">
                <div class="card-label">{lab}</div>
                <div class="card-value">{fmt(actual)} / {fmt(plan)}</div>
                <div class="card-target">
                    Achievement: {"N/A" if score is None else f"{score:.1f}%"}
                </div>
            </div>""",
            unsafe_allow_html=True
        )

# ============================================================
# 11. DATA QUALITY / RECORD STATUS
# ============================================================
st.markdown('<div class="sec">11. DOCUMENT & RECORD DATA STATUS</div>', unsafe_allow_html=True)

st.info(
    "The supplied department tracker does not contain a dedicated "
    "document/records compliance table. No document score is fabricated."
)

# ============================================================
# 12. CHAIRMAN INSIGHTS
# ============================================================
st.markdown('<div class="sec">12. DATA-DRIVEN INSIGHTS FOR CHAIRMAN</div>', unsafe_allow_html=True)

insights = []

if month_values.get("pending_inv",0) > 0:
    insights.append(f"• {fmt(month_values['pending_inv'])} process-safety investigations are pending beyond 30 days.")

if month_values.get("critical_failed",0) > 0:
    insights.append(f"• {fmt(month_values['critical_failed'])} PSM critical equipment failure(s) are recorded.")

if month_values.get("barrier_unacceptable",0) > 0:
    insights.append(f"• {fmt(month_values['barrier_unacceptable'])} unacceptable barrier(s) are recorded.")

if month_values.get("normalisation_overdue",0) > 0:
    insights.append(f"• {fmt(month_values['normalisation_overdue'])} interlock normalisation item(s) are overdue.")

if not insights:
    insights.append("• No critical issue was identified from the available tracker values.")

st.markdown(
    '<div class="note">' + "<br>".join(insights) + '</div>',
    unsafe_allow_html=True
)

# ============================================================
# 13. DECISION / GOVERNANCE LOG
# ============================================================
st.markdown('<div class="sec">13. DECISION / GOVERNANCE LOG</div>', unsafe_allow_html=True)

gov = pd.DataFrame([
    ["Third-party recommendations delayed", month_values.get("third_delayed",0)],
    ["Incident investigation recommendations delayed", month_values.get("incident_rec_delayed",0)],
    ["PHA recommendations delayed", month_values.get("pha_rec_delayed",0)],
    ["Audit recommendations delayed", month_values.get("audit_delayed",0)],
    ["MOC pending >15 days", month_values.get("moc_pending15",0)],
], columns=["Governance Item", "Real Count"])

st.dataframe(gov, use_container_width=True, hide_index=True)

# ============================================================
# 14. QUICK ACTIONS
# ============================================================
st.markdown('<div class="sec">14. QUICK ACTION SHORTCUTS</div>', unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("🏭 All Departments", use_container_width=True):
        st.switch_page("pages/07_All_Departments.py")


with q3:
    st.download_button(
        "⬇️ Export Summary",
        data=pd.DataFrame(dept_rows).to_csv(index=False),
        file_name="PSM_Chairman_Department_Summary.csv",
        mime="text/csv",
        use_container_width=True
    )

with q4:
    if st.button("🔄 Refresh Real Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.caption(
    "Source: department Excel files in data/departments. "
    "No dashboard value is fabricated when the source field is unavailable."
)