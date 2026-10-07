import streamlit as st
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "jsw_jfe_logo.png"
PSM_WHEEL_PATH = BASE_DIR / "PSM_Wheel.png"

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
# LOGIN AUTHENTICATION
# ============================================================

def _image_data_uri(path: Path, mime_type: str) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def login_page():

    wheel_data = _image_data_uri(PSM_WHEEL_PATH, "image/png")

    st.markdown(
        """
        <style>

        /* =====================================================
           LOGIN PAGE
           ===================================================== */

        .stApp {
            background: #073f61 !important;
        }

        .main .block-container {
            position: relative !important;
            z-index: 2 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }

        .login-bg {
            position: fixed;
            inset: 0;
            background: linear-gradient(
                135deg,
                #031d34 0%,
                #073f61 55%,
                #0b5a82 100%
            );
            z-index: 0;
            pointer-events: none;
        }

        .login-wheel {
            position: fixed;
            width: 700px;
            height: 700px;
            max-width: 75vw;
            max-height: 75vh;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            object-fit: contain;
            opacity: 0.10;
            z-index: 1;
            pointer-events: none;
        }

        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }

        header[data-testid="stHeader"] {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        /* Login title */
        .login-title {
            color: #073f61 !important;
            font-family: Arial, sans-serif !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            letter-spacing: 0.4px !important;
            line-height: 1.15 !important;
            text-align: center !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Login subtitle */
        .login-subtitle {
            color: #f28c00 !important;
            font-family: Arial, sans-serif !important;
            font-size: 12px !important;
            font-weight: 800 !important;
            letter-spacing: 2.4px !important;
            text-align: center !important;
            margin: 8px 0 0 0 !important;
            padding: 0 !important;
        }

        /* White login card */
        .login-card {
            background: #ffffff !important;
            border-radius: 14px !important;
            padding: 32px 38px 28px 38px !important;
            margin-top: 16vh !important;
            box-shadow: 0 18px 50px rgba(0,0,0,0.32) !important;
            box-sizing: border-box !important;
            text-align: center !important;
        }

        /* User ID / Password labels */
        div[data-testid="stTextInput"] label {
            color: #173b5b !important;
            font-weight: 700 !important;
            font-size: 13px !important;
        }

        /* Input fields */
        div[data-testid="stTextInput"] input {
            height: 42px !important;
            border: 1px solid #b9c8d6 !important;
            border-radius: 6px !important;
            color: #173b5b !important;
            font-size: 14px !important;
            background: #ffffff !important;
        }

        /* Login button */
        div[data-testid="stButton"] > button {
            width: 100% !important;
            height: 44px !important;
            margin-top: 8px !important;
            background: #073f61 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 7px !important;
            font-size: 15px !important;
            font-weight: 800 !important;
        }

        div[data-testid="stButton"] > button:hover {
            background: #0b5a82 !important;
            color: #ffffff !important;
        }

        div[data-testid="stTextInput"],
        div[data-testid="stButton"] {
            position: relative !important;
            z-index: 20 !important;
        }


        .login-footer {
            color: #718096 !important;
            font-family: Arial, sans-serif !important;
            font-size: 10px !important;
            text-align: center !important;
            margin-top: 18px !important;
        }

        </style>
        """.replace("__WHEEL_DATA__", wheel_data),
        unsafe_allow_html=True
    )

    # Fixed background and transparent wheel. The wheel is kept
    # behind all Streamlit controls.
    st.markdown(
        f"""
        <div class="login-bg"></div>
        <img class="login-wheel" src="{wheel_data}" alt="">
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # CENTER LOGIN FORM
    # ========================================================

    left, center, right = st.columns([1, 1.05, 1])

    with center:

        # ----------------------------------------------------
        # LOGIN CARD HEADER
        # Use inline styles for maximum Streamlit compatibility.
        # This prevents raw HTML from appearing as text.
        # ----------------------------------------------------

        logo_data = _image_data_uri(LOGO_PATH, "image/png")

        st.markdown(
            """
            <div style="
                background:#ffffff;
                border-radius:14px;
                padding:22px 30px 22px 30px;
                margin-top:12vh;
                box-shadow:0 18px 50px rgba(0,0,0,0.32);
                box-sizing:border-box;
                text-align:center;
                position:relative;
                z-index:20;
            ">
                <img
                    src="__LOGO_DATA__"
                    style="
                        width:190px;
                        max-width:85%;
                        height:auto;
                        display:block;
                        margin:0 auto 16px auto;
                    "
                >
                <div style="
                    color:#073f61;
                    font-family:Arial,sans-serif;
                    font-size:24px;
                    font-weight:900;
                    letter-spacing:0.4px;
                    line-height:1.15;
                    margin:0;
                    padding:0;
                ">
                    PROCESS SAFETY MANAGEMENT
                </div>
            </div>
            """.replace("__LOGO_DATA__", logo_data),
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='position:relative;z-index:20;text-align:center;color:#f28c00;font-family:Arial,sans-serif;font-size:12px;font-weight:900;letter-spacing:2.4px;margin:7px 0 10px 0;'>DIGITAL VISION WALL</div>",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # LOGIN INPUTS
        # ----------------------------------------------------

        username = st.text_input(
            "User ID",
            placeholder="Enter User ID",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            placeholder="Enter Password",
            type="password",
            key="login_password"
        )

        login_clicked = st.button(
            "LOGIN",
            use_container_width=True
        )

        # ----------------------------------------------------
        # LOGIN VALIDATION
        # ----------------------------------------------------

        if login_clicked:

            try:
                correct_username = st.secrets["login"]["username"]
                correct_password = st.secrets["login"]["password"]

            except Exception:
                st.error(
                    "Login configuration not found. "
                    "Add [login] username and password to "
                    ".streamlit/secrets.toml."
                )
                st.stop()

            if (
                username.strip() == str(correct_username).strip()
                and password == str(correct_password)
            ):

                st.session_state["authenticated"] = True

                st.session_state.pop(
                    "login_username",
                    None
                )

                st.session_state.pop(
                    "login_password",
                    None
                )

                st.rerun()

            else:
                st.error("Invalid User ID or Password")

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        st.markdown(
            """
            <div style="
                color:#718096;
                font-family:Arial,sans-serif;
                font-size:10px;
                text-align:center;
                margin-top:18px;
            ">
                JSW JFE Steel Limited
                &nbsp; | &nbsp;
                Process Safety Management
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CHECK LOGIN STATUS
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


# ============================================================
# SHOW LOGIN BEFORE DASHBOARD
# ============================================================

if not st.session_state["authenticated"]:
    login_page()
    st.stop()


# ============================================================
# PROJECT PATHS
# ============================================================



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

    /* ========================================================
       LOGOUT BUTTON
       ======================================================== */

    section[data-testid="stSidebar"]
    div[data-testid="stButton"]
    button[data-testid="stBaseButton-secondary"] {
        background: #d62828 !important;
        background-color: #d62828 !important;
        color: #ffffff !important;
        border: 1px solid #d62828 !important;
        font-weight: 900 !important;
        font-size: 14px !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stButton"]
    button[data-testid="stBaseButton-secondary"]:hover {
        background: #b71c1c !important;
        background-color: #b71c1c !important;
        color: #ffffff !important;
        border-color: #b71c1c !important;
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
            🛡️ PROCESS SAFETY MANAGEMENT
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
# LOGOUT BUTTON
# ============================================================

with st.sidebar:

    if st.button("⏻  LOGOUT", key="logout_button"):

        st.session_state["authenticated"] = False
        st.session_state.pop("login_username", None)
        st.session_state.pop("login_password", None)

        st.rerun()


# ============================================================
# RUN APPLICATION
# ============================================================

pg.run()
