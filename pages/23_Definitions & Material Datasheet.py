#=============================================================
#HEADER CODE
#=============================================================
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PSM Digital Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# REMOVE STREAMLIT TOP SPACE
# ============================================================

st.markdown(
    """
    <style>

    html,
    body {
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }



    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
    padding-top: 0 !important;
    margin-top: -15px !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    iframe {
        display: block !important;
        margin-top: -5px !important;
        padding-top: 0 !important;
        border: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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

    width: 100%;

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

    top: 0;

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

                DEFINITIONS & MATERIAL DATASHEET

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


st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] > div:has(> iframe) {
        margin-bottom: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



import streamlit as st
import pandas as pd
import html
from urllib.parse import quote

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Definitions & Material Datasheet",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SPREADSHEET_ID = "1hseNjE88OlNp-zmEIsIDdx8c6qs49gYakaSQvvShBO4"
DEFINITIONS_SHEET = "Definitions"
MATERIAL_SHEET = "Material"

TABLE_HEIGHT = 520
BOTTOM_GAP = 25
TITLE_SEARCH_GAP = 16
SEARCH_TABLE_GAP = 12

# =========================================================
# CSS
# =========================================================
st.markdown(
    f""" 
    <style> 
    #MainMenu, footer, header {{ 
        visibility: hidden; 
    }} 

    .stApp {{ 
        background: #ffffff; 
        color: #263746; 
    }} 

    .block-container {{ 
        max-width: 100%; 
        padding: 0.2rem 0.65rem 0.5rem 0.65rem !important; 
        margin-top: 0 !important;
    }} 

    /* Restore real vertical spacing */ 
    [data-testid="stVerticalBlock"] {{ 
        gap: 0.5rem !important; 
    }} 

    [data-testid="stHorizontalBlock"] {{ 
        gap: 0.55rem !important; 
        align-items: stretch; 
    }} 

    [data-testid="column"] {{ 
        min-width: 0 !important; 
        padding: 0 !important; 
    }} 

    /* Individual bordered sections */ 
    div[data-testid="stVerticalBlockBorderWrapper"] {{ 
        border: 1.5px solid #d1dbe5 !important; 
        border-radius: 9px !important; 
        background: #ffffff !important; 
        padding: 10px !important; 
        box-sizing: border-box; 
    }} 

    /* Prevent child blocks from collapsing into each other */ 
    div[data-testid="stVerticalBlockBorderWrapper"] 
    > div[data-testid="stVerticalBlock"] {{ 
        display: flex !important; 
        flex-direction: column !important; 
        gap: 0.5rem !important; 
        min-width: 0 !important; 
    }} 

    /* Section title */ 
    .section-heading {{ 
        display: block; 
        position: relative; 
        width: 100%; 
        flex-shrink: 0; 
        box-sizing: border-box; 
        color: #ffffff; 
        font-size: 22px; 
        font-weight: 750; 
        line-height: 1.35; 
        padding: 12px 14px; 
        border-radius: 6px; 
        margin: 0 0 {TITLE_SEARCH_GAP}px 0 !important; 
    }} 

    .definitions-heading {{ 
        background: #1769aa; 
        border-left: 6px solid #0d4778; 
    }} 

    .material-heading {{ 
        background: #d9363e; 
        border-left: 6px solid #a82029; 
    }} 

    /* Search widget: separate block beneath title */ 
    div[data-testid="stSelectbox"] {{ 
        display: block !important; 
        position: relative !important; 
        width: 100% !important; 
        flex-shrink: 0 !important; 
        clear: both !important; 
        margin: 0 0 {SEARCH_TABLE_GAP}px 0 !important; 
        padding: 0 !important; 
    }} 

    div[data-testid="stSelectbox"] > div {{ 
        width: 100%; 
        margin: 0 !important; 
    }} 

    div[data-testid="stSelectbox"] > div > div {{ 
        min-height: 43px; 
        border-radius: 7px; 
        background: #ffffff; 
        border-color: #cbd5df; 
        box-shadow: none; 
    }} 

    /* Scrollable table */ 
    .table-scroll {{ 
        display: block; 
        position: relative; 
        width: 100%; 
        height: {TABLE_HEIGHT}px; 
        min-height: {TABLE_HEIGHT}px; 
        max-height: {TABLE_HEIGHT}px; 
        flex-shrink: 0; 
        overflow: auto; 
        border: 1px solid #d7e0e8; 
        border-radius: 5px; 
        box-sizing: border-box; 
        background: #ffffff; 
        margin: 0 !important; 
        padding: 0 !important; 
        scrollbar-width: thin; 
        scrollbar-color: #aab8c6 #f2f5f8; 
    }} 

    .table-scroll::-webkit-scrollbar {{ 
        width: 8px; 
        height: 8px; 
    }} 

    .table-scroll::-webkit-scrollbar-thumb {{ 
        background: #aab8c6; 
        border-radius: 8px; 
    }} 

    .table-scroll::-webkit-scrollbar-track {{ 
        background: #f2f5f8; 
    }} 

    /* Table formatting */ 
    .data-table {{ 
        border-collapse: separate; 
        border-spacing: 0; 
        width: 100%; 
        font-size: 12.5px; 
        color: #263746; 
        margin: 0; 
    }} 

    .data-table th, 
    .data-table td {{ 
        padding: 9px; 
        text-align: left; 
        vertical-align: top; 
        border-right: 1px solid #dfe6ed; 
        border-bottom: 1px solid #dfe6ed; 
        min-width: 85px; 
        overflow-wrap: anywhere; 
        white-space: normal; 
        box-sizing: border-box; 
    }} 

    .data-table th {{ 
        position: sticky; 
        top: 0; 
        z-index: 5; 
        color: #ffffff; 
        font-weight: 700; 
        white-space: normal; 
    }} 

    .definitions-table th {{ 
        background: #1769aa; 
    }} 

    .material-table th {{ 
        background: #d9363e; 
    }} 

    /* Definitions alternate row colours */ 
    .definitions-table tbody tr:nth-child(odd) td {{ 
        background: #ffffff; 
    }} 

    .definitions-table tbody tr:nth-child(even) td {{ 
        background: #eef6fd; 
    }} 

    /* Material rows alternate across every column */ 
    .material-table tbody tr:nth-child(odd) td {{ 
        background: #ffffff; 
    }} 

    .material-table tbody tr:nth-child(even) td {{ 
        background: #fff0f0; 
    }} 

    /* Bold property and material names */ 
    .definitions-table tbody td:first-child, 
    .material-table tbody td:first-child {{ 
        font-weight: 700; 
    }} 

    .data-table tbody tr:hover td {{ 
        background: #fff0c2 !important; 
    }} 

    .data-table th:last-child, 
    .data-table td:last-child {{ 
        border-right: none; 
    }} 

    .empty-message {{ 
        padding: 18px; 
        color: #687a89; 
        font-size: 13px; 
    }} 

    /* Visible gap below each table, inside its section */ 
    .table-bottom-spacer {{ 
        display: block; 
        width: 100%; 
        height: {BOTTOM_GAP}px; 
        min-height: {BOTTOM_GAP}px; 
        flex: 0 0 {BOTTOM_GAP}px; 
        box-sizing: border-box; 
    }} 

    @media (max-width: 850px) {{ 
        .block-container {{ 
            padding-left: 0.35rem !important; 
            padding-right: 0.35rem !important; 
        }} 

        [data-testid="stHorizontalBlock"] {{ 
            gap: 0.4rem !important; 
        }} 

        div[data-testid="stVerticalBlockBorderWrapper"] {{ 
            padding: 7px !important; 
        }} 

        .section-heading {{ 
            font-size: 18px; 
            padding: 10px; 
        }} 

        .data-table {{ 
            font-size: 11px; 
        }} 

        .data-table th, 
        .data-table td {{ 
            padding: 7px; 
        }} 
    }} 
    </style> 
    """,
    unsafe_allow_html=True
)


# =========================================================
# GOOGLE SHEETS DATA LOADER
# =========================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_google_sheet(sheet_name):
    encoded_name = quote(sheet_name, safe="")

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/gviz/tq?"
        f"tqx=out:csv&sheet={encoded_name}"
    )

    df = pd.read_csv(url)
    df.columns = [str(col).strip() for col in df.columns]
    df = df.dropna(how="all")

    empty_columns = [
        col for col in df.columns
        if str(col).startswith("Unnamed:")
           and df[col].isna().all()
    ]

    if empty_columns:
        df = df.drop(columns=empty_columns)

    serial_names = {
        "s. no.", "s.no.", "s no", "s. no",
        "serial no", "serial number", "sl. no.",
        "sl no", "sl.no.", "sr. no.", "sr no"
    }

    remove_columns = [
        col for col in df.columns
        if str(col).strip().casefold() in serial_names
    ]

    if remove_columns:
        df = df.drop(columns=remove_columns)

    for col in df.columns:
        if (
                pd.api.types.is_object_dtype(df[col])
                or pd.api.types.is_string_dtype(df[col])
        ):
            df[col] = df[col].map(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

    return df


def get_data():
    definitions = pd.DataFrame()
    materials = pd.DataFrame()
    errors = []

    try:
        definitions = load_google_sheet(DEFINITIONS_SHEET)
    except Exception as exc:
        errors.append(f"Definitions sheet could not load: {exc}")

    try:
        materials = load_google_sheet(MATERIAL_SHEET)
    except Exception as exc:
        errors.append(f"Material sheet could not load: {exc}")

    return definitions, materials, errors


# =========================================================
# COLUMN HELPERS
# =========================================================
def find_column(df, requested_name):
    for col in df.columns:
        if str(col).strip().casefold() == requested_name.casefold():
            return col
    return None


def get_column_options(df, requested_column):
    actual_column = find_column(df, requested_column)

    if df.empty or actual_column is None:
        return []

    values = (
        df[actual_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[values != ""]

    return sorted(values.unique().tolist(), key=str.casefold)


# =========================================================
# FILTER FUNCTIONS
# =========================================================
def filter_by_column(df, requested_column, selected_value):
    if df.empty or selected_value == "All":
        return df.copy()

    actual_column = find_column(df, requested_column)

    if actual_column is None:
        return df.iloc[0:0].copy()

    mask = (
        df[actual_column]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(selected_value.casefold())
        .fillna(False)
    )

    return df.loc[mask].copy()


def filter_material(df, selected_material):
    if df.empty or selected_material == "All":
        return df.copy()

    material_column = (
            find_column(df, "Material")
            or find_column(df, "Substance")
    )

    if material_column is None:
        return df.iloc[0:0].copy()

    mask = (
        df[material_column]
        .astype("string")
        .str.strip()
        .str.casefold()
        .eq(selected_material.casefold())
        .fillna(False)
    )

    return df.loc[mask].copy()


# =========================================================
# HTML TABLE RENDERER
# =========================================================
def render_table(df, table_class):
    if df.empty:
        st.markdown(
            """ 
            <div class="table-scroll"> 
                <div class="empty-message"> 
                    No matching data found. 
                </div> 
            </div> 
            """,
            unsafe_allow_html=True
        )
        return

    headers = "".join(
        f"<th>{html.escape(str(col))}</th>"
        for col in df.columns
    )

    rows = []

    for _, row in df.iterrows():
        cells = "".join(
            "<td>"
            + html.escape(
                "" if pd.isna(value) else str(value)
            )
            + "</td>"
            for value in row
        )
        rows.append(f"<tr>{cells}</tr>")

    st.markdown(
        f""" 
        <div class="table-scroll"> 
            <table class="data-table {table_class}"> 
                <thead><tr>{headers}</tr></thead> 
                <tbody>{''.join(rows)}</tbody> 
            </table> 
        </div> 
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BOTTOM SPACER
# =========================================================
def add_bottom_spacer():
    st.markdown(
        f""" 
        <div class="table-bottom-spacer" 
             style="height:{BOTTOM_GAP}px; 
                    min-height:{BOTTOM_GAP}px;"> 
        </div> 
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TRANSPOSE MATERIAL TABLE
# =========================================================
def transpose_material_table(df):
    if df.empty:
        return pd.DataFrame(columns=["Property", "Value"])

    if len(df) == 1:
        row = df.iloc[0]

        return pd.DataFrame({
            "Property": [str(col) for col in df.columns],
            "Value": [
                "" if pd.isna(value) else str(value)
                for value in row.tolist()
            ]
        })

    transposed = df.T.reset_index()
    transposed.columns = (
            ["Property"]
            + [f"Record {i + 1}" for i in range(len(df))]
    )

    transposed["Property"] = transposed["Property"].astype(str)

    for col in transposed.columns[1:]:
        transposed[col] = transposed[col].map(
            lambda value: "" if pd.isna(value) else str(value)
        )

    return transposed


# =========================================================
# LOAD DATA
# =========================================================
definitions_df, material_df, errors = get_data()

for error in errors:
    st.error(
        error
        + " Verify the sheet tab names and sharing permissions."
    )

# =========================================================
# SIDE-BY-SIDE SECTIONS
# =========================================================
left_col, right_col = st.columns([1, 1], gap="small")

# =========================================================
# DEFINITIONS SECTION
# =========================================================
with left_col:
    with st.container(border=True):
        st.markdown(
            """ 
            <div class="section-heading definitions-heading"> 
                Definitions 
            </div> 
            """,
            unsafe_allow_html=True
        )

        property_options = get_column_options(
            definitions_df,
            "Property"
        )

        selected_property = st.selectbox(
            "Property search",
            options=["All"] + property_options,
            index=0,
            key="property_search",
            label_visibility="collapsed",
            placeholder="Search by property...",
            help="Type to find or select a property."
        )

        filtered_definitions = filter_by_column(
            definitions_df,
            "Property",
            selected_property
        )

        render_table(filtered_definitions, "definitions-table")
        add_bottom_spacer()

    # =========================================================
# MATERIAL DATASHEET SECTION
# =========================================================
with right_col:
    with st.container(border=True):
        st.markdown(
            """ 
            <div class="section-heading material-heading"> 
                Material Datasheet 
            </div> 
            """,
            unsafe_allow_html=True
        )

        material_column = (
                find_column(material_df, "Material")
                or find_column(material_df, "Substance")
        )

        material_options = (
            get_column_options(material_df, material_column)
            if material_column
            else []
        )

        selected_material = st.selectbox(
            "Material search",
            options=["All"] + material_options,
            index=0,
            key="material_search",
            label_visibility="collapsed",
            placeholder="Search by material...",
            help="Type to find Coke, BF Gas, LPG, or another material."
        )

        if selected_material == "All":
            render_table(material_df, "material-table")
        else:
            selected_df = filter_material(
                material_df,
                selected_material
            )
            transposed_df = transpose_material_table(selected_df)
            render_table(transposed_df, "material-table")

        add_bottom_spacer()

