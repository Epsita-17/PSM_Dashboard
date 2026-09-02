import os
import re
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import plotly.express as px
import streamlit as st

from components.psm_theme import psm_header, psm_section


# ============================================================
# GOOGLE SHEET
# ============================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"


# ============================================================
# PSM MODULE -> GOOGLE SHEET TAB
# ============================================================

SHEETS = {
    "PT": "Sheet2",
    "PHA": "PHA",
    "PHA Recommendations": "PHA Recommendations",
    "MOC": "MOC",
    "PSSR": "PSSR",
    "Training": "Training & Competency",
    "SOC-SOL": "SOC-SOL Deviation",
    "PS Incident": "PS Incident",
    "Critical Equipment": "PSM Critical Equipment",
    "Alarm": "Alarm Categorisation",
    "Barrier Audit": "Barrier Audit",
}

MODULES = list(SHEETS.keys())


# ============================================================
# MODULE COLORS
# ============================================================

MODULE_COLORS = {
    "PT": "#1976D2",
    "PHA": "#2EAD68",
    "PHA Recommendations": "#08A6A6",
    "MOC": "#F39C12",
    "PSSR": "#E53935",
    "Training": "#7650C8",
    "SOC-SOL": "#00A6B2",
    "PS Incident": "#E83E8C",
    "Critical Equipment": "#8FA500",
    "Alarm": "#FF8C00",
    "Barrier Audit": "#455A64",
}


# ============================================================
# DOCUMENT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENT_ROOT = BASE_DIR / "department_documents"

DOCUMENT_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SAFE FILE NAME
# ============================================================

def safe_filename(filename):
    """
    Convert uploaded filename into a safe filename.
    """

    name = Path(filename).name

    name = re.sub(
        r"[^A-Za-z0-9._ -]",
        "_",
        name
    )

    return name


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value):
    if value is None:
        return ""

    text = str(value)

    text = (
        text
        .replace("\xa0", " ")
        .replace("\n", " ")
        .strip()
        .upper()
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=60)
def load_sheet(sheet_name):

    encoded_sheet = quote(
        str(sheet_name),
        safe=""
    )

    url = (
        "https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}"
        "/gviz/tq"
        f"?tqx=out:csv&sheet={encoded_sheet}"
    )

    try:

        df = pd.read_csv(url)

        if df.empty:
            return pd.DataFrame()

        # ----------------------------------------------------
        # CLEAN COLUMN NAMES
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.replace(
                "\xa0",
                " ",
                regex=False
            )
            .str.replace(
                "\n",
                " ",
                regex=False
            )
            .str.strip()
        )

        # ----------------------------------------------------
        # CLEAN TEXT DATA
        # ----------------------------------------------------

        for column in df.columns:

            if df[column].dtype == "object":

                df[column] = (
                    df[column]
                    .astype(str)
                    .str.replace(
                        "\xa0",
                        " ",
                        regex=False
                    )
                    .str.replace(
                        "\n",
                        " ",
                        regex=False
                    )
                    .str.strip()
                )

        # ----------------------------------------------------
        # REMOVE INVALID TEXT
        # ----------------------------------------------------

        df = df.replace(
            {
                "nan": "",
                "NaN": "",
                "NAN": "",
                "None": "",
                "none": "",
                "NULL": "",
                "null": "",
            }
        )

        # ----------------------------------------------------
        # REMOVE EMPTY ROWS
        # ----------------------------------------------------

        df = df.dropna(
            how="all"
        )

        return df

    except Exception as exc:

        st.warning(
            f"Unable to load Google Sheet "
            f"'{sheet_name}': {exc}"
        )

        return pd.DataFrame()


# ============================================================
# FIND DEPARTMENT COLUMN
# ============================================================

def find_department_column(df):

    if df is None or df.empty:
        return None

    normalized = {}

    for column in df.columns:

        name = normalize_text(column)

        name = (
            name
            .replace("_", " ")
            .replace("-", " ")
        )

        normalized[name] = column

    preferred = [
        "DEPARTMENT",
        "DEPARTMENT NAME",
        "DEPT",
        "DEPT NAME",
        "DEPARTMENT AREA",
        "DEPARTMENT/AREA",
        "AREA",
        "AREA NAME",
        "PLANT AREA",
        "LOCATION",
    ]

    for item in preferred:

        if item in normalized:
            return normalized[item]

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    for column in df.columns:

        name = normalize_text(column)

        if (
            "DEPARTMENT" in name
            or "DEPT" in name
        ):
            return column

    return None


# ============================================================
# DEPARTMENT MATCHING
# ============================================================

def department_matches(
    value,
    department
):

    actual = normalize_text(value)
    target = normalize_text(department)

    if actual == "":
        return False

    if actual == target:
        return True

    # --------------------------------------------------------
    # BLAST FURNACE
    #
    # This allows:
    #
    # BLAST FURNACE
    # BLAST FURNACE-1
    # BLAST FURNACE-2
    # BF
    # --------------------------------------------------------

    if target == "BLAST FURNACE":

        if actual in [
            "BF",
            "BLAST FURNACE",
            "BLAST FURNACE 1",
            "BLAST FURNACE 2",
            "BLAST FURNACE-1",
            "BLAST FURNACE-2",
        ]:
            return True

    # --------------------------------------------------------
    # GENERAL PREFIX MATCH
    # --------------------------------------------------------

    if actual.startswith(
        target + "-"
    ):
        return True

    if actual.startswith(
        target + " "
    ):
        return True

    return False


# ============================================================
# FILTER DEPARTMENT DATA
# ============================================================

def filter_department_data(
    df,
    department
):

    if df is None or df.empty:
        return pd.DataFrame()

    department_column = find_department_column(df)

    if department_column is None:
        return pd.DataFrame()

    mask = df[
        department_column
    ].apply(
        lambda value:
        department_matches(
            value,
            department
        )
    )

    return df.loc[
        mask
    ].copy()


# ============================================================
# LOAD ALL MODULE DATA
# ============================================================

def load_all_modules():

    module_data = {}

    for module_name, sheet_name in SHEETS.items():

        module_data[module_name] = load_sheet(
            sheet_name
        )

    return module_data


# ============================================================
# FIND STATUS COLUMN
# ============================================================

def find_status_column(df):

    if df is None or df.empty:
        return None

    preferred = [
        "STATUS",
        "STATUS (ONGOING/COMPLETED)",
        "STATUS  (ONGOING/COMPLETED)",
        "OVERDUE/PENDING/COMPLETED",
        "CURRENT STATUS",
        "ACTIVITY STATUS",
        "RECOMMENDATION STATUS",
    ]

    normalized = {}

    for column in df.columns:

        name = normalize_text(column)

        normalized[name] = column

    for item in preferred:

        if item in normalized:
            return normalized[item]

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    for column in df.columns:

        name = normalize_text(column)

        if "STATUS" in name:
            return column

    return None


# ============================================================
# STATUS COUNTS
# ============================================================

def status_counts(df):

    result = {
        "Completed": 0,
        "Ongoing": 0,
        "Pending": 0,
        "Overdue": 0,
        "Open": 0,
        "Closed": 0,
    }

    status_column = find_status_column(df)

    if status_column is None:
        return result

    values = (
        df[status_column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    for value in values:

        if value == "":
            continue

        if "completed" in value:
            result["Completed"] += 1

        elif "ongoing" in value:
            result["Ongoing"] += 1

        elif "overdue" in value:
            result["Overdue"] += 1

        elif "pending" in value:
            result["Pending"] += 1

        elif value == "open":
            result["Open"] += 1

        elif value == "closed":
            result["Closed"] += 1

    return result


# ============================================================
# DOCUMENT FOLDER
# ============================================================

def get_module_document_folder(
    department,
    module
):

    safe_department = safe_filename(
        department
    ).replace(
        " ",
        "_"
    )

    safe_module = safe_filename(
        module
    ).replace(
        " ",
        "_"
    )

    folder = (
        DOCUMENT_ROOT
        / safe_department
        / safe_module
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


# ============================================================
# SAVE DOCUMENT
# ============================================================

def save_uploaded_document(
    uploaded_file,
    department,
    module
):

    if uploaded_file is None:
        return None

    folder = get_module_document_folder(
        department,
        module
    )

    filename = safe_filename(
        uploaded_file.name
    )

    destination = folder / filename

    # --------------------------------------------------------
    # AVOID ACCIDENTAL OVERWRITE
    # --------------------------------------------------------

    if destination.exists():

        stem = destination.stem
        suffix = destination.suffix

        counter = 1

        while destination.exists():

            destination = (
                folder
                / f"{stem}_{counter}{suffix}"
            )

            counter += 1

    with open(
        destination,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return destination


# ============================================================
# GET SAVED DOCUMENTS
# ============================================================

def get_saved_documents(
    department,
    module
):

    folder = get_module_document_folder(
        department,
        module
    )

    if not folder.exists():
        return []

    files = [
        item
        for item in folder.iterdir()
        if item.is_file()
    ]

    return sorted(
        files,
        key=lambda item: item.name.lower()
    )


# ============================================================
# DOCUMENT UPLOAD SECTION
# ============================================================

def render_document_section(
    department,
    module
):

    documents = get_saved_documents(
        department,
        module
    )

    st.markdown(
        f"""
        <div style="
            background:#f7fbfd;
            border:1px solid #c8dce8;
            border-radius:8px;
            padding:10px 12px;
            margin-top:8px;
            margin-bottom:8px;
        ">

            <div style="
                font-size:13px;
                font-weight:900;
                color:#075b8e;
                margin-bottom:6px;
            ">
                📁 {module} DOCUMENTS
            </div>

            <div style="
                font-size:10px;
                color:#64798a;
            ">
                Upload and manage {module}
                supporting documents for
                {department}.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        f"Upload {module} document",
        type=[
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "csv",
            "jpg",
            "jpeg",
            "png",
        ],
        key=(
            f"upload_"
            f"{safe_filename(department)}_"
            f"{safe_filename(module)}"
        ),
    )

    if uploaded_file is not None:

        if st.button(
            f"Save {module} Document",
            key=(
                f"save_"
                f"{safe_filename(department)}_"
                f"{safe_filename(module)}"
            ),
            use_container_width=True,
        ):

            saved_path = save_uploaded_document(
                uploaded_file,
                department,
                module
            )

            if saved_path:

                st.success(
                    f"Document saved: "
                    f"{saved_path.name}"
                )

                st.rerun()

    # --------------------------------------------------------
    # EXISTING DOCUMENTS
    # --------------------------------------------------------

    documents = get_saved_documents(
        department,
        module
    )

    if documents:

        st.markdown(
            "##### Existing Documents"
        )

        for document in documents:

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.write(
                    f"📄 {document.name}"
                )

            with col2:

                try:

                    with open(
                        document,
                        "rb"
                    ) as file:

                        st.download_button(
                            "View / Download",
                            data=file.read(),
                            file_name=document.name,
                            key=(
                                f"download_"
                                f"{safe_filename(department)}_"
                                f"{safe_filename(module)}_"
                                f"{safe_filename(document.name)}"
                            ),
                            use_container_width=True,
                        )

                except Exception as exc:

                    st.warning(
                        f"Unable to read "
                        f"{document.name}: {exc}"
                    )

    else:

        st.caption(
            "No documents uploaded for this module."
        )


# ============================================================
# KPI CARD
# ============================================================

def render_kpi(
    container,
    title,
    value,
    subtitle,
    color
):

    with container:

        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #d7e5ee;
                border-top:4px solid {color};
                border-radius:8px;
                padding:9px 12px;
                height:92px;
                box-shadow:
                    0 2px 7px
                    rgba(0,60,100,0.08);
            ">

                <div style="
                    font-size:9px;
                    font-weight:900;
                    color:{color};
                    text-transform:uppercase;
                    letter-spacing:.4px;
                ">
                    {title}
                </div>

                <div style="
                    font-size:26px;
                    font-weight:900;
                    color:#173f63;
                    margin-top:4px;
                    line-height:1;
                ">
                    {value}
                </div>

                <div style="
                    font-size:9px;
                    color:#6b7f8d;
                    margin-top:5px;
                ">
                    {subtitle}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MODULE CARD
# ============================================================

def render_module_card(
    module,
    df,
    department
):

    total = len(df)

    counts = status_counts(
        df
    )

    completed = counts["Completed"]
    ongoing = counts["Ongoing"]

    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            border:1px solid #c8dce8;
            border-top:4px solid
                {MODULE_COLORS.get(module, "#1976D2")};
            border-radius:8px;
            padding:9px 12px;
            margin-bottom:7px;
        ">

            <div style="
                font-size:13px;
                font-weight:900;
                color:#173f63;
            ">
                {module}
            </div>

            <div style="
                display:flex;
                gap:18px;
                margin-top:6px;
                font-size:10px;
            ">

                <span>
                    <b>Total:</b> {total}
                </span>

                <span style="color:#159447;">
                    <b>Completed:</b> {completed}
                </span>

                <span style="color:#e88900;">
                    <b>Ongoing:</b> {ongoing}
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN DEPARTMENT DASHBOARD
# ============================================================

def render_department_dashboard(
    department="Blast Furnace"
):

    # ========================================================
    # HEADER
    # ========================================================

    psm_header(
        department.upper()
    )

    # ========================================================
    # SECTION
    # ========================================================

    psm_section(
        f"{department.upper()} PSM DASHBOARD"
    )

    # ========================================================
    # LOAD GOOGLE SHEETS
    # ========================================================

    with st.spinner(
        "Loading PSM data from Google Sheet..."
    ):

        all_data = load_all_modules()

    # ========================================================
    # FILTER BLAST FURNACE
    # ========================================================

    department_data = {}

    for module in MODULES:

        department_data[module] = (
            filter_department_data(
                all_data.get(
                    module,
                    pd.DataFrame()
                ),
                department
            )
        )

    # ========================================================
    # TOTAL RECORDS
    # ========================================================

    total_records = sum(
        len(df)
        for df in department_data.values()
    )

    active_modules = sum(
        1
        for df in department_data.values()
        if not df.empty
    )

    # ========================================================
    # TOP KPIs
    # ========================================================

    k1, k2, k3, k4 = st.columns(
        4,
        gap="small"
    )

    render_kpi(
        k1,
        "TOTAL PSM RECORDS",
        f"{total_records:,}",
        department,
        "#1976D2"
    )

    render_kpi(
        k2,
        "ACTIVE MODULES",
        f"{active_modules}",
        f"Of {len(MODULES)} modules",
        "#20A464"
    )

    completed_total = 0
    ongoing_total = 0

    for df in department_data.values():

        counts = status_counts(
            df
        )

        completed_total += counts[
            "Completed"
        ]

        ongoing_total += counts[
            "Ongoing"
        ]

    render_kpi(
        k3,
        "COMPLETED",
        f"{completed_total:,}",
        "Across PSM modules",
        "#159447"
    )

    render_kpi(
        k4,
        "ONGOING",
        f"{ongoing_total:,}",
        "Across PSM modules",
        "#F39C12"
    )

    # ========================================================
    # MODULE SUMMARY
    # ========================================================

    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True
    )

    psm_section(
        "PSM MODULE SUMMARY"
    )

    module_rows = []

    for module in MODULES:

        df = department_data[module]

        counts = status_counts(
            df
        )

        module_rows.append(
            {
                "Module": module,
                "Records": len(df),
                "Completed": counts["Completed"],
                "Ongoing": counts["Ongoing"],
                "Pending": counts["Pending"],
                "Overdue": counts["Overdue"],
                "Open": counts["Open"],
                "Closed": counts["Closed"],
            }
        )

    module_summary = pd.DataFrame(
        module_rows
    )

    # ========================================================
    # CHARTS
    # ========================================================

    chart1, chart2 = st.columns(
        [1.5, 1],
        gap="small"
    )

    # --------------------------------------------------------
    # MODULE BAR
    # --------------------------------------------------------

    with chart1:

        st.markdown(
            """
            <div style="
                font-size:12px;
                font-weight:900;
                color:#075b8e;
                margin:2px 0 4px 4px;
            ">
                BLAST FURNACE PSM MODULE RECORDS
            </div>
            """,
            unsafe_allow_html=True
        )

        chart_df = module_summary[
            module_summary["Records"] > 0
        ].copy()

        if not chart_df.empty:

            fig = px.bar(
                chart_df,
                x="Module",
                y="Records",
                text="Records",
                color="Module",
                color_discrete_map=MODULE_COLORS,
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig.update_layout(
                height=250,
                margin=dict(
                    l=35,
                    r=10,
                    t=15,
                    b=65,
                ),
                showlegend=False,
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    size=8
                ),
                xaxis=dict(
                    title=None,
                    tickangle=-35,
                ),
                yaxis=dict(
                    title="Records",
                    gridcolor="#e5edf2",
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

        else:

            st.info(
                "No Blast Furnace records found."
            )

    # --------------------------------------------------------
    # DONUT
    # --------------------------------------------------------

    with chart2:

        st.markdown(
            """
            <div style="
                font-size:12px;
                font-weight:900;
                color:#075b8e;
                margin:2px 0 4px 4px;
            ">
                MODULE-WISE SHARE
            </div>
            """,
            unsafe_allow_html=True
        )

        donut_df = module_summary[
            module_summary["Records"] > 0
        ].copy()

        if not donut_df.empty:

            fig = px.pie(
                donut_df,
                names="Module",
                values="Records",
                hole=0.58,
                color="Module",
                color_discrete_map=MODULE_COLORS,
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                hovertemplate=(
                    "<b>%{label}</b>"
                    "<br>Records: %{value}"
                    "<br>Share: %{percent}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=250,
                margin=dict(
                    l=5,
                    r=5,
                    t=5,
                    b=5,
                ),
                paper_bgcolor="white",
                font=dict(
                    size=8
                ),
                legend=dict(
                    orientation="v",
                    x=0.98,
                    y=0.5,
                    xanchor="left",
                    yanchor="middle",
                    font=dict(
                        size=8
                    ),
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

        else:

            st.info(
                "No module data available."
            )

    # ========================================================
    # MODULE SUMMARY TABLE
    # ========================================================

    psm_section(
        "BLAST FURNACE MODULE STATUS"
    )

    st.dataframe(
        module_summary,
        use_container_width=True,
        hide_index=True,
        height=300,
    )

    # ========================================================
    # MODULE DETAILS + DOCUMENTS
    # ========================================================

    psm_section(
        "MODULE DATA & DOCUMENT MANAGEMENT"
    )

    selected_module = st.selectbox(
        "Select PSM Module",
        MODULES,
        key=(
            f"selected_module_"
            f"{safe_filename(department)}"
        ),
    )

    selected_df = department_data.get(
        selected_module,
        pd.DataFrame()
    )

    # ========================================================
    # MODULE DATA
    # ========================================================

    st.markdown(
        f"""
        <div style="
            background:#eef7fc;
            border-left:4px solid
                {MODULE_COLORS.get(
                    selected_module,
                    "#1976D2"
                )};
            border-radius:6px;
            padding:8px 12px;
            margin-top:5px;
            margin-bottom:7px;
            font-size:12px;
            font-weight:800;
            color:#174c70;
        ">
            {department.upper()}
            → {selected_module}
            → {len(selected_df)} RECORDS
        </div>
        """,
        unsafe_allow_html=True
    )

    if selected_df.empty:

        st.info(
            f"No {selected_module} data "
            f"found for {department}."
        )

    else:

        st.dataframe(
            selected_df,
            use_container_width=True,
            hide_index=True,
            height=320,
        )

        # ----------------------------------------------------
        # DOWNLOAD FILTERED DATA
        # ----------------------------------------------------

        csv_data = selected_df.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(
            label=(
                f"⬇ Download "
                f"{selected_module} Data"
            ),
            data=csv_data,
            file_name=(
                f"{safe_filename(department)}_"
                f"{safe_filename(selected_module)}.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    # ========================================================
    # DOCUMENT MANAGEMENT
    # ========================================================

    with st.expander(
        f"📁 {selected_module} DOCUMENT MANAGEMENT",
        expanded=True,
    ):

        render_document_section(
            department,
            selected_module
        )

    # ========================================================
    # ALL MODULE DOCUMENT MANAGEMENT
    # ========================================================

    with st.expander(
        "📂 ALL PSM MODULE DOCUMENT MANAGEMENT",
        expanded=False,
    ):

        for module in MODULES:

            with st.expander(
                f"{module} "
                f"({len(department_data[module])} records)"
            ):

                render_document_section(
                    department,
                    module
                )

    # ========================================================
    # REFRESH
    # ========================================================

    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🔄 Refresh Google Sheet Data",
        use_container_width=True,
    ):

        load_sheet.clear()

        st.rerun()