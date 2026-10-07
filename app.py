import streamlit as st
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PSM Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
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

    /* ========================================================
       MAIN PAGE
       ======================================================== */

    .stApp {
        background-color: #eef4f8;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* ========================================================
       STREAMLIT HEADER
       DO NOT HIDE THIS HEADER
       Native sidebar reopen control is inside it.
       ======================================================== */

   header[data-testid="stHeader"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: transparent !important;
    z-index: 999999 !important;
}

    /* ========================================================
   SIDEBAR - ALWAYS REOPENABLE
   ======================================================== */

/* Sidebar itself */
section[data-testid="stSidebar"] {
    visibility: visible !important;
}

/* Sidebar reopen control */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: fixed !important;
    left: 0 !important;
    top: 0 !important;
    z-index: 999999 !important;
}

/* Reopen button */
[data-testid="stSidebarCollapsedControl"] button {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 1000000 !important;
}

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #073f61 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #073f61 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

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

    /* ========================================================
       SIDEBAR NAVIGATION
       ======================================================== */

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

    /* ========================================================
       SIDEBAR DIVIDER
       ======================================================== */

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

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

    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR BRANDING
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="psm-sidebar-brand">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    #if LOGO_PATH.exists():

        #st.image(
            #str(LOGO_PATH),
            #width=185
        #)

    #else:

        #st.warning(
            #"Logo file not found:\n"
            #"assets/jsw_jfe_logo.png"
       #)


    # --------------------------------------------------------
    # PSM HEADER
    # --------------------------------------------------------

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

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.divider()

# ============================================================
# MAIN DASHBOARD PAGES
# ============================================================


# ------------------------------------------------------------
# 01 HOME
# ------------------------------------------------------------

home_page = st.Page(
    str(BASE_DIR / "pages" / "01_Home.py"),
    title="HOME",
    icon="🏠",
    default=True
)


# ------------------------------------------------------------
# 02 EXECUTIVE DASHBOARD
# ------------------------------------------------------------

executive_page = st.Page(
    str(BASE_DIR / "pages" / "02_Executive.py"),
    title="EXECUTIVE ",
    icon="📊"
)


# ------------------------------------------------------------
# 03 APEX COMMITTEE
# ------------------------------------------------------------

apex_page = st.Page(
    str(BASE_DIR / "pages" / "03_Apex_Committee.py"),
    title="APEX COMMITTEE",
    icon="📊"
)




# ------------------------------------------------------------
# 05 PSM SC CHAIRMAN
# ------------------------------------------------------------

PSM_SC_Chairman_page = st.Page(
    str(BASE_DIR / "pages" / "05_PSM_SC_Chairman.py"),
    title="PSM SC CHAIRMAN",
    icon="📊"
)


# ------------------------------------------------------------
# 06 PSM SC CONVENER DASHBOARD
# ------------------------------------------------------------

psm_sc_convener_page = st.Page(
    str(BASE_DIR / "pages" / "06_PSM_SC_Convener_Dashboard.py"),
    title="PSM SC CONVENER",
    icon="📊"
)


# ------------------------------------------------------------
# 07 ALL DEPARTMENTS
# ------------------------------------------------------------

all_departments_page = st.Page(
    str(BASE_DIR / "pages" / "07_All_Departments.py"),
    title="ALL DEPARTMENTS",
    icon="🏭"
)


# ============================================================
# INDIVIDUAL DEPARTMENT PAGES
# ============================================================

# ------------------------------------------------------------
# BLAST FURNACE
# ------------------------------------------------------------

blast_furnace_page = st.Page(
    str(BASE_DIR / "departments" / "01_Blast_Furnace.py"),
    title="BLAST FURNACE",
    icon="🏭"
)


# ------------------------------------------------------------
# COKE OVEN
# ------------------------------------------------------------

coke_oven_page = st.Page(
    str(BASE_DIR / "departments" / "02_Coke_Oven.py"),
    title="COKE OVEN",
    icon="🏭"
)


# ------------------------------------------------------------
# SMS-1
# ------------------------------------------------------------

sms_1_page = st.Page(
    str(BASE_DIR / "departments" / "04_SMS_1.py"),
    title="SMS-1",
    icon="🏭"
)


# ------------------------------------------------------------
# SMS-2
# ------------------------------------------------------------

sms_2_page = st.Page(
    str(BASE_DIR / "departments" / "05_SMS_2.py"),
    title="SMS-2",
    icon="🏭"
)


# ------------------------------------------------------------
# DRI
# ------------------------------------------------------------

dri_page = st.Page(
    str(BASE_DIR / "departments" / "06_DRI.py"),
    title="DRI",
    icon="🏭"
)


# ------------------------------------------------------------
# CENTRAL UTILITY
# ------------------------------------------------------------

cu_page = st.Page(
    str(BASE_DIR / "departments" / "07_CU.py"),
    title="CENTRAL UTILITY",
    icon="🏭"
)


# ------------------------------------------------------------
# CRM
# ------------------------------------------------------------

crm_page = st.Page(
    str(BASE_DIR / "departments" / "08_CRM.py"),
    title="CRM",
    icon="🏭"
)


# ------------------------------------------------------------
# WRM
# ------------------------------------------------------------

wrm_page = st.Page(
    str(BASE_DIR / "departments" / "09_WRM.py"),
    title="WRM",
    icon="🏭"
)


# ------------------------------------------------------------
# CPP
# ------------------------------------------------------------

cpp_page = st.Page(
    str(BASE_DIR / "departments" / "10_CPP.py"),
    title="CPP",
    icon="🏭"
)


# ------------------------------------------------------------
# SINTER
# ------------------------------------------------------------

sinter_page = st.Page(
    str(BASE_DIR / "departments" / "11_Sinter.py"),
    title="SINTER",
    icon="🏭"
)


# ------------------------------------------------------------
# TUBE MILL
# ------------------------------------------------------------

tube_mill_page = st.Page(
    str(BASE_DIR / "departments" / "12_Tube_Mill.py"),
    title="TUBE MILL",
    icon="🏭"
)


# ------------------------------------------------------------
# CSP
# ------------------------------------------------------------

csp_page = st.Page(
    str(BASE_DIR / "departments" / "13_CSP.py"),
    title="CSP",
    icon="🏭"
)


# ------------------------------------------------------------
# PELLET & BENEFICIATION
# ------------------------------------------------------------

pellet_beneficiation_page = st.Page(
    str(BASE_DIR / "departments" / "14_Pellet_Beneficiation.py"),
    title="PELLET & BENEFICIATION",
    icon="🏭"
)


# ------------------------------------------------------------
# LCP
# ------------------------------------------------------------

lcp_page = st.Page(
    str(BASE_DIR / "departments" / "15_LCP.py"),
    title="LCP",
    icon="🏭"
)


# ------------------------------------------------------------
# RMHS
# ------------------------------------------------------------

rmhs_page = st.Page(
    str(BASE_DIR / "departments" / "17_RMHS.py"),
    title="RMHS",
    icon="🏭"
)

# ------------------------------------------------------------
# PROJECTS
# ------------------------------------------------------------

projects_page = st.Page(
    str(BASE_DIR / "departments" / "18_Projects.py"),
    title="PROJECTS",
    icon="🏭"
)



# ============================================================
# PSM MODULE PAGES
# ============================================================


# ------------------------------------------------------------
# 09 PT
# ------------------------------------------------------------

pt_page = st.Page(
    str(BASE_DIR / "pages" / "09_PT.py"),
    title="PT",
    icon="🛡️"
)


# ------------------------------------------------------------
# 10 PHA
# ------------------------------------------------------------

pha_page = st.Page(
    str(BASE_DIR / "pages" / "10_PHA.py"),
    title="PHA",
    icon="🛡️"
)


# ------------------------------------------------------------
# 11 MOC
# ------------------------------------------------------------

moc_page = st.Page(
    str(BASE_DIR / "pages" / "11_MOC.py"),
    title="MOC",
    icon="🛡️"
)


# ------------------------------------------------------------
# 12 PSSR
# ------------------------------------------------------------

pssr_page = st.Page(
    str(BASE_DIR / "pages" / "12_PSSR.py"),
    title="PSSR",
    icon="🛡️"
)


# ------------------------------------------------------------
# 13 TRAINING
# ------------------------------------------------------------

training_page = st.Page(
    str(BASE_DIR / "pages" / "13_Training.py"),
    title="TRAINING",
    icon="🛡️"
)


# ------------------------------------------------------------
# 15 OP
# ------------------------------------------------------------

op_page = st.Page(
    str(BASE_DIR / "pages" / "15_OP.py"),
    title="OP",
    icon="🛡️"
)


# ------------------------------------------------------------
# 14 PROCESS SAFETY INCIDENT
# ------------------------------------------------------------

psi_page = st.Page(
    str(BASE_DIR / "pages" / "14_PSI.py"),
    title="PROCESS SAFETY INCIDENT",
    icon="🛡️"
)

# ------------------------------------------------------------
# 17 AUDIT
# ------------------------------------------------------------

audit_page = st.Page(
    str(BASE_DIR / "pages" / "17_Audit.py"),
    title="AUDIT",
    icon="🛡️"
)

# ------------------------------------------------------------
# 18 INCIDENT LIBRARY
# ------------------------------------------------------------
incident_library_page = st.Page(
    str(BASE_DIR / "pages" / "18_Incident Library.py"),
    title="INCIDENT LIBRARY",
    icon="🛡️"
)

# ------------------------------------------------------------
# 19 ALARM & INTERLOCK MANAGEMENT
# ------------------------------------------------------------

alarm_interlock_management_page = st.Page(
    str(BASE_DIR / "pages" / "19_ALARM_&_INTERLOCK_MANAGEMENT.py"),
    title="ALARM & INTERLOCK MANAGEMENT",
    icon="🛡️"
)

# ------------------------------------------------------------
# 20 PSM CE & BARRIER HEALTH
# ------------------------------------------------------------

psm_ce_barrier_health_page = st.Page(
    str(BASE_DIR / "pages" / "20_PSM CE & BARRIER HEALTH.py"),
    title="PSM CE & BARRIER HEALTH",
    icon="🛡️"
)

# ------------------------------------------------------------
# 21 PSM CE & BARRIER HEALTH
# ------------------------------------------------------------

MIQA_page = st.Page(
    str(BASE_DIR / "pages" / "21_MIQA.py"),
    title="MIQA",
    icon="🛡️"
)

# 22 JSW SAFETY STANDARDS
# ------------------------------------------------------------

jsw_safety_standards_page = st.Page(
    str(BASE_DIR / "pages" / "22_JSW_Safety_Standards.py"),
    title="JSW SAFETY STANDARDS",
    icon="🛡️"
)



# ============================================================
# REPORTS
# ============================================================

reports_page = st.Page(
    str(BASE_DIR / "pages" / "16_Document Repository.py"),
    title="DOCUMENT REPOSITORY",
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
            PSM_SC_Chairman_page,
            psm_sc_convener_page
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
            lcp_page,
            rmhs_page,
            projects_page
        ],

        "PSM MODULES": [
    pt_page,
    pha_page,
    moc_page,
    pssr_page,
    training_page,
    op_page,
    psi_page,
    audit_page,
    incident_library_page,
    alarm_interlock_management_page,
    psm_ce_barrier_health_page,
    MIQA_page,
    jsw_safety_standards_page
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
