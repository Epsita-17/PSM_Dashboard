import streamlit as st
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PSM Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

LOGO_PATH = BASE_DIR / "assets" / "jsw_jfe_logo.png"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN PAGE
       ================================ */

    .stApp {
        background-color: #eef4f8;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }


    /* ================================
       STREAMLIT HEADER
       ================================ */

    header[data-testid="stHeader"] {
        background-color: transparent;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background-color: #073f61 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #073f61 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }


    /* ================================
       SIDEBAR BRAND
       ================================ */

    .psm-sidebar-brand {
        width: 100%;
        text-align: center;
        padding-top: 8px;
        padding-bottom: 8px;
    }

    .psm-sidebar-logo {
        width: 185px;
        max-width: 100%;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .psm-sidebar-title {
        color: #ffffff !important;
        font-size: 19px;
        font-weight: 900;
        letter-spacing: 1px;
        line-height: 1.3;
        margin-top: 8px;
    }

    .psm-sidebar-subtitle {
        color: #dcecf7 !important;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.7px;
        line-height: 1.5;
        margin-top: 5px;
    }


    /* ================================
       SIDEBAR NAVIGATION
       ================================ */

    section[data-testid="stSidebar"]
    [data-testid="stSidebarNav"] {
        padding-top: 5px;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarNav"]
    span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarNav"]
    a {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarNav"]
    svg {
        color: #ffffff !important;
    }


    /* ================================
       SIDEBAR DIVIDER
       ================================ */

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25);
    }


    /* ================================
       METRIC CARDS
       ================================ */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #c5d6e2;
        border-radius: 10px;
        padding: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: #164461 !important;
        font-weight: 700;
    }


    /* ================================
       ALERTS
       ================================ */

    [data-testid="stAlert"] {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR BRANDING
# IMPORTANT:
# Logo + PSM Dashboard appears ABOVE Home
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="psm-sidebar-brand">',
        unsafe_allow_html=True
    )

    # ----------------------------
    # LOGO
    # ----------------------------

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=185
        )

    else:

        st.warning(
            "Logo file not found:\n"
            "assets/jsw_jfe_logo.png"
        )


    # ----------------------------
    # PSM HEADER
    # ----------------------------

    st.markdown(
        """
        <div class="psm-sidebar-title">
            🛡️ PSM DASHBOARD
        </div>

        <div class="psm-sidebar-subtitle">
            PROCESS SAFETY MANAGEMENT
        </div>

        <div class="psm-sidebar-subtitle">
            DIGITAL VISION WALL
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()


# ============================================================
# PAGE OBJECTS
# ============================================================

# ------------------------------------------------------------
# 01 HOME
# ------------------------------------------------------------

home_page = st.Page(
    "pages/01_Home.py",
    title="Home",
    icon="🏠",
    default=True
)


# ------------------------------------------------------------
# 02 EXECUTIVE DASHBOARD
# ------------------------------------------------------------

executive_page = st.Page(
    "pages/02_Executive_Dashboard.py",
    title="Executive Dashboard",
    icon="📊"
)


# ------------------------------------------------------------
# 03 APEX COMMITTEE
# ------------------------------------------------------------

apex_page = st.Page(
    "pages/03_Apex_Committee.py",
    title="Apex Committee",
    icon="👥"
)


# ------------------------------------------------------------
# 04 STEERING COMMITTEE
# ------------------------------------------------------------

steering_page = st.Page(
    "pages/04_Steering_Committee.py",
    title="Steering Committee",
    icon="🧭"
)


# ------------------------------------------------------------
# 05 SUB COMMITTEE CHAIRMAN
# ------------------------------------------------------------

sub_committee_chairman_page = st.Page(
    "pages/05_Sub_Committee_Chairman.py",
    title="Sub Committee Chairman",
    icon="👔"
)


# ------------------------------------------------------------
# 06 PSM CHAIRMAN DASHBOARD
# ------------------------------------------------------------

psm_chairman_page = st.Page(
    "pages/06_PSM_Chairman_Dashboard.py",
    title="PSM Chairman Dashboard",
    icon="👤"
)


# ------------------------------------------------------------
# 07 ALL DEPARTMENTS
# ------------------------------------------------------------

all_departments_page = st.Page(
    "pages/07_All_Departments.py",
    title="All Departments",
    icon="🏭"
)

# ============================================================
# INDIVIDUAL DEPARTMENT PAGES
# ============================================================

blast_furnace_page = st.Page(
    "departments/01_Blast_Furnace.py",
    title="Blast Furnace",
    icon="🔥"
)

coke_oven_page = st.Page(
    "departments/02_Coke_Oven.py",
    title="Coke Oven",
    icon="🏭"
)


sms_1_page = st.Page(
    "departments/04_SMS_1.py",
    title="SMS-1",
    icon="🏭"
)

sms_2_page = st.Page(
    "departments/05_SMS_2.py",
    title="SMS-2",
    icon="🏭"
)

dri_page = st.Page(
    "departments/06_DRI.py",
    title="DRI",
    icon="⚙️"
)

cu_page = st.Page(
    "departments/07_CU.py",
    title="Central Utility",
    icon="💧"
)

crm_page = st.Page(
    "departments/08_CRM.py",
    title="CRM",
    icon="⚙️"
)

wrm_page = st.Page(
    "departments/09_WRM.py",
    title="WRM",
    icon="⚙️"
)

cpp_page = st.Page(
    "departments/10_CPP.py",
    title="CPP",
    icon="⚡"
)

sinter_page = st.Page(
    "departments/11_Sinter.py",
    title="Sinter",
    icon="🏭"
)

tube_mill_page = st.Page(
    "departments/12_Tube_Mill.py",
    title="Tube Mill",
    icon="⚙️"
)

csp_page = st.Page(
    "departments/13_CSP.py",
    title="CSP",
    icon="🏭"
)

pellet_beneficiation_page = st.Page(
    "departments/14_Pellet_Beneficiation.py",
    title="Pellet & Beneficiation",
    icon="🏭"
)

lcp_page = st.Page(
    "departments/15_LCP.py",
    title="LCP",
    icon="⚙️"
)

# ------------------------------------------------------------
# 11 MOC
# ------------------------------------------------------------

moc_page = st.Page(
    "pages/11_MOC.py",
    title="MOC",
    icon="🔄"
)


# ------------------------------------------------------------
# 12 PSSR
# NEW PAGE
# ------------------------------------------------------------

pssr_page = st.Page(
    "pages/12_PSSR.py",
    title="PSSR",
    icon="✅"
)


# ------------------------------------------------------------
# 13 TRAINING
# NEW PAGE
# ------------------------------------------------------------

training_page = st.Page(
    "pages/13_Training.py",
    title="Training & Competency",
    icon="🎓"
)


# ------------------------------------------------------------
# 16 REPORTS
# ------------------------------------------------------------

reports_page = st.Page(
    "pages/16_Reports.py",
    title="Reports",
    icon="📄"
)
# ============================================================
# PSM MODULE PAGES
# ============================================================

pt_page = st.Page(
    str(BASE_DIR / "pages" / "09_PT.py"),
    title="PT",
    icon="🔍"
)

pha_page = st.Page(
    str(BASE_DIR / "pages" / "10_PHA.py"),
    title="PHA",
    icon="⚠️"
)

moc_page = st.Page(
    str(BASE_DIR / "pages" / "11_MOC.py"),
    title="MOC",
    icon="🔄"
)

pssr_page = st.Page(
    str(BASE_DIR / "pages" / "12_PSSR.py"),
    title="PSSR",
    icon="✅"
)

training_page = st.Page(
    str(BASE_DIR / "pages" / "13_Training.py"),
    title="Training & Competency",
    icon="🎓"
)

psi_page = st.Page(
    str(BASE_DIR / "pages" / "14_PSI.py"),
    title="Process Safety Incident",
    icon="🚨"
)

reports_page = st.Page(
    str(BASE_DIR / "pages" / "16_Reports.py"),
    title="Reports",
    icon="📄"
)

# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    {
        "MAIN": [
            home_page,
            executive_page,
            apex_page,
            steering_page,
            sub_committee_chairman_page,
            psm_chairman_page
        ],

        "PSM OVERVIEW": [
            all_departments_page
        ],

        "INDIVIDUAL DEPARTMENT": [
            blast_furnace_page,
            coke_oven_page,
            sms_1_page,
            sms_2_page,
            dri_page,
            cu_page,
            crm_page,
            wrm_page,
            cpp_page,
            sinter_page,
            tube_mill_page,
            csp_page,
            pellet_beneficiation_page,
            lcp_page
        ],

        "PSM MODULES": [
         pt_page,
         pha_page,
         moc_page,
         pssr_page,
         training_page,
         psi_page
        ],

        "REPORTING": [
            reports_page
        ]
    },
    position="sidebar"
)


# ============================================================
# RUN APPLICATION
# ============================================================

pg.run()