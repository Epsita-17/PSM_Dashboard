import os
import streamlit as st

st.set_page_config(
    page_title="PSM Reports",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")

# =========================================================
# CSS
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    .reports-header {
        background: linear-gradient(90deg, #06284a, #0b4770);
        color: white;
        padding: 24px;
        border-radius: 0 0 16px 16px;
        border-bottom: 3px solid #1689e5;
        text-align: center;
        margin-bottom: 25px;
    }

    .reports-title {
        font-size: 30px;
        font-weight: 800;
    }

    .reports-subtitle {
        font-size: 14px;
        margin-top: 7px;
        font-weight: 600;
    }

    .section-title {
        color: #073b67;
        font-size: 20px;
        font-weight: 800;
        border-bottom: 2px solid #d6e3ef;
        padding-bottom: 8px;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    .report-card {
        background: white;
        border: 1px solid #d9e4ee;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
    }

    .report-name {
        color: #073b67;
        font-size: 16px;
        font-weight: 800;
    }

    .report-info {
        color: #64748b;
        font-size: 13px;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.html(
    """
    <div class="reports-header">
        <div class="reports-title">
            📄 PSM REPORTS
        </div>
        <div class="reports-subtitle">
            PROCESS SAFETY MANAGEMENT • REPORT & DOCUMENT CENTRE
        </div>
    </div>
    """
)

# =========================================================
# REPORT STORAGE
# =========================================================
st.html(
    '<div class="section-title">📁 PSM REPORT STORAGE</div>'
)

st.info(
    "This page is prepared for the PSM report/document repository. "
    "The SharePoint/OneDrive storage will be connected here."
)

# =========================================================
# REPORT CATEGORIES
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="report-card">
            <div class="report-name">📊 PSM Performance Reports</div>
            <div class="report-info">
                Monthly and yearly PSM performance reports
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="report-card">
            <div class="report-name">📋 Audit Reports</div>
            <div class="report-info">
                Internal, external and third-party audit reports
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="report-card">
            <div class="report-name">⚠️ Incident Reports</div>
            <div class="report-info">
                Process safety incident and investigation reports
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# LOCAL REPORT FOLDER
# =========================================================
st.html(
    '<div class="section-title">📂 AVAILABLE REPORTS</div>'
)

if os.path.isdir(REPORTS_DIR):

    files = sorted(os.listdir(REPORTS_DIR))

    if files:

        for file_name in files:

            file_path = os.path.join(REPORTS_DIR, file_name)

            if os.path.isfile(file_path):

                st.markdown(
                    f"""
                    <div class="report-card">
                        <div class="report-name">
                            📄 {file_name}
                        </div>
                        <div class="report-info">
                            Available in PSM Dashboard report storage
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No reports are currently stored in the local report folder."
        )

else:

    st.info(
        "Report storage folder is not created yet."
    )

# =========================================================
# UPLOAD REPORT
# =========================================================
st.html(
    '<div class="section-title">⬆️ ADD REPORT</div>'
)

uploaded_report = st.file_uploader(
    "Upload PSM Report",
    type=["xlsx", "xls", "pdf", "docx", "pptx"],
    key="report_upload"
)

if uploaded_report is not None:

    os.makedirs(REPORTS_DIR, exist_ok=True)

    save_path = os.path.join(
        REPORTS_DIR,
        uploaded_report.name
    )

    with open(save_path, "wb") as file:
        file.write(uploaded_report.getbuffer())

    st.success(
        f"Report uploaded successfully: {uploaded_report.name}"
    )

# =========================================================
# FUTURE SHAREPOINT CONNECTION
# =========================================================
st.html(
    '<div class="section-title">☁️ PSM ONEDRIVE / SHAREPOINT</div>'
)

st.warning(
    "SharePoint/OneDrive connection is not enabled yet. "
    "This section will be connected to the PSM document repository next."
)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div style="
        text-align:center;
        color:#687888;
        font-size:12px;
        padding:25px;
    ">
        PSM Dashboard v1.0 • JSW JFE Steel Limited
    </div>
    """,
    unsafe_allow_html=True
)