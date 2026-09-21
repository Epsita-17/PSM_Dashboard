import streamlit as st
import pandas as pd
import urllib.parse
import html
import re
import requests
from io import BytesIO
from openpyxl import load_workbook
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JSW Group Standards",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)
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



.block-container {
    padding: 0rem 0.35rem 0rem 0.35rem !important;
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    max-width: 100%;
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
   REFRESH BUTTON — KEEP BELOW HEADER
   ======================================================== */

div[data-testid="stButton"] {
    margin-top: 1px !important;
    margin-bottom: 1px !important;
}


    /* ========================================================
       MATCH CLICKABLE MODULE HEADINGS WITH NORMAL HEADINGS
       ======================================================== */
    [data-testid="stPageLink"] {
        margin-bottom:6px !important;
    }

    [data-testid="stPageLink"],
    [data-testid="stPageLink"] a,
    [data-testid="stPageLink"] a *,
    [data-testid="stPageLink"] p,
    [data-testid="stPageLink"] span,
    [data-testid="stPageLink"] div {
        color:#073f78 !important;
        font-size:12px !important;
        font-weight:900 !important;
        text-decoration:none !important;
    }

    [data-testid="stPageLink"] a:hover,
    [data-testid="stPageLink"] a:hover * {
        color:#073f78 !important;
        text-decoration:none !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

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

    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
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
        margin-top: -20px !important;
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

                JSW SAFETY STANDARDS

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
        margin-bottom: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================

SHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEET_NAME = "JSW Group Standards"

XLSX_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=xlsx"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       PAGE
       ======================================================== */

    .stApp {
        background: #ffffff;
    }


    .main .block-container {

        max-width: 100%;

        padding-top: 0.45rem;

        padding-left: 2.5rem;

        padding-right: 2.5rem;

        padding-bottom: 1rem;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULT ELEMENTS
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* ========================================================
       SEARCH BOX
       ======================================================== */

    div[data-testid="stTextInput"] {

        width: 100%;

        margin-top: 18px;

        margin-bottom: 0;
    }


    div[data-testid="stTextInput"] input {

        height: 48px !important;

        border: 1.5px solid #a9c1dd !important;

        border-radius: 9px !important;

        background: #f8fbff !important;

        color: #123f85 !important;

        font-family:
            Arial,
            Helvetica,
            sans-serif !important;

        font-size: 15px !important;

        font-weight: 400 !important;

        padding-left: 16px !important;

        box-shadow:
            0 1px 4px rgba(0,0,0,0.04) !important;
    }


    div[data-testid="stTextInput"] input:focus {

        border-color: #1268b3 !important;

        box-shadow:
            0 0 0 1px #1268b3 !important;
    }


    div[data-testid="stTextInput"] input::placeholder {

        color: #7d8da3 !important;

        opacity: 1 !important;
    }


    div[data-testid="stTextInput"] label {

        display: none !important;
    }


    /* ========================================================
       REMOVE STREAMLIT EXTRA SPACING
       ======================================================== */

    div[data-testid="stVerticalBlock"] {

        gap: 0.15rem;
    }


    /* ========================================================
       REMOVE IFRAME BORDER / EXTRA SPACE
       ======================================================== */

    iframe {

        border: none !important;

        display: block;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    if value is None:

        return ""


    value = str(value).strip()


    if value == "":

        return ""


    try:

        number = float(value)

        if number.is_integer():

            return str(
                int(number)
            )

    except Exception:

        pass


    return value


# ============================================================
# EXTRACT URL FROM CELL
# ============================================================

def extract_url_from_cell(cell):

    # --------------------------------------------------------
    # Actual hyperlink
    # --------------------------------------------------------

    try:

        if cell.hyperlink:

            target = cell.hyperlink.target

            if target:

                target = str(
                    target
                ).strip()

                if (
                    target.startswith("http://")
                    or
                    target.startswith("https://")
                ):

                    return target

    except Exception:

        pass


    # --------------------------------------------------------
    # Cell value
    # --------------------------------------------------------

    value = cell.value


    if value is None:

        return ""


    value = str(value).strip()


    if value == "":

        return ""


    # --------------------------------------------------------
    # Direct URL
    # --------------------------------------------------------

    if (
        value.startswith("http://")
        or
        value.startswith("https://")
    ):

        return value


    # --------------------------------------------------------
    # HYPERLINK formula
    # --------------------------------------------------------

    match = re.search(
        r'HYPERLINK\s*\(\s*["\'](https?://[^"\']+)["\']',
        value,
        flags=re.IGNORECASE
    )


    if match:

        return match.group(1)


    # --------------------------------------------------------
    # Any URL inside cell
    # --------------------------------------------------------

    match = re.search(
        r'https?://[^\s"\')]+',
        value
    )


    if match:

        return match.group(0)


    return ""


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False
)
def load_google_sheet():

    try:

        response = requests.get(
            XLSX_URL,
            timeout=30
        )

        response.raise_for_status()


        workbook = load_workbook(
            BytesIO(
                response.content
            ),
            data_only=False
        )


        if SHEET_NAME not in workbook.sheetnames:

            return (
                None,
                None,
                f"Sheet '{SHEET_NAME}' was not found. "
                f"Available sheets: {workbook.sheetnames}"
            )


        worksheet = workbook[
            SHEET_NAME
        ]


        rows = list(
            worksheet.iter_rows()
        )


        if not rows:

            return (
                None,
                None,
                "The selected sheet is empty."
            )


        # ====================================================
        # HEADERS
        # ====================================================

        headers = []


        for index, cell in enumerate(
            rows[0],
            start=1
        ):

            value = cell.value


            if value is None:

                value = f"Column_{index}"


            headers.append(
                str(value).strip()
            )


        # ====================================================
        # UNIQUE HEADERS
        # ====================================================

        unique_headers = []

        header_count = {}


        for header in headers:

            if header not in header_count:

                header_count[header] = 0

                unique_headers.append(
                    header
                )

            else:

                header_count[header] += 1

                unique_headers.append(
                    f"{header}_{header_count[header]}"
                )


        headers = unique_headers


        # ====================================================
        # DATA
        # ====================================================

        data = []

        hyperlink_data = []


        for row in rows[1:]:

            values = []

            links = []


            for column_index in range(
                len(headers)
            ):

                if column_index < len(row):

                    cell = row[
                        column_index
                    ]

                else:

                    cell = None


                # --------------------------------------------
                # VALUE
                # --------------------------------------------

                if cell is None:

                    value = ""

                else:

                    value = cell.value

                    if value is None:

                        value = ""


                values.append(
                    str(value).strip()
                )


                # --------------------------------------------
                # LINK
                # --------------------------------------------

                if cell is not None:

                    link = extract_url_from_cell(
                        cell
                    )

                else:

                    link = ""


                links.append(
                    link
                )


            # ------------------------------------------------
            # Ignore completely empty rows
            # ------------------------------------------------

            if all(
                str(value).strip() == ""
                for value in values
            ):

                continue


            data.append(
                values
            )

            hyperlink_data.append(
                links
            )


        # ====================================================
        # DATAFRAME
        # ====================================================

        df = pd.DataFrame(
            data,
            columns=headers
        )


        links_df = pd.DataFrame(
            hyperlink_data,
            columns=headers
        )


        return (
            df,
            links_df,
            None
        )


    except Exception as error:

        return (
            None,
            None,
            str(error)
        )


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(
    dataframe,
    possible_names
):

    normalized_columns = {}


    for column in dataframe.columns:

        normalized = re.sub(
            r"[^a-z0-9]",
            "",
            str(column).lower()
        )

        normalized_columns[
            normalized
        ] = column


    for name in possible_names:

        normalized_name = re.sub(
            r"[^a-z0-9]",
            "",
            name.lower()
        )


        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]


    return None


# ============================================================
# SAFE HTML
# ============================================================

def safe_text(value):

    if value is None:

        return ""


    return html.escape(
        str(value).strip()
    )


# ============================================================
# KPI HTML
# ============================================================

def create_kpi_html(total):

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <style>

    * {{
        box-sizing: border-box;
    }}


    html,
    body {{

        margin: 0;

        padding: 0;

        background: transparent;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        overflow: hidden;
    }}


    /* ========================================================
       KPI CARD
       ======================================================== */

    .kpi-card {{

        width: 100%;

        height: 82px;

        background: #eaf3ff;

        border: 1px solid #b9d2ee;

        border-radius: 10px;

        position: relative;

        overflow: hidden;

        box-shadow:
            0 1px 4px rgba(0,0,0,0.05);
    }}


    /* ========================================================
       BLUE ACCENT
       ======================================================== */

    .kpi-accent {{

        position: absolute;

        left: 0;

        top: 0;

        width: 12px;

        height: 100%;

        background: #1268b3;

        border-radius:
            10px 0 0 10px;
    }}


    /* ========================================================
       NUMBER
       ======================================================== */

    .kpi-number {{

        position: absolute;

        left: 56px;

        top: 7px;

        color: #123f85;

        font-size: 34px;

        font-weight: 700;

        line-height: 1;
    }}


    /* ========================================================
       TITLE
       ======================================================== */

    .kpi-title {{

        position: absolute;

        left: 56px;

        top: 48px;

        color: #123f85;

        font-size: 16px;

        font-weight: 600;

        line-height: 1;
    }}

    </style>

    </head>

    <body>

        <div class="kpi-card">

            <div class="kpi-accent"></div>

            <div class="kpi-number">
                {total}
            </div>

            <div class="kpi-title">
                Management Standards
            </div>

        </div>

    </body>

    </html>

    """


# ============================================================
# TABLE HTML
# ============================================================

def create_table_html(dataframe):

    rows_html = ""


    # ========================================================
    # ROWS
    # ========================================================

    for _, row in dataframe.iterrows():

        sno = safe_text(
            row["S. No."]
        )


        standard = safe_text(
            row["Management Standard"]
        )


        document_no = safe_text(
            row["Document No."]
        )


        revision = safe_text(
            row["Revision"]
        )


        document_url = str(
            row["Document URL"]
        ).strip()


        # ----------------------------------------------------
        # DOCUMENT BUTTON
        # ----------------------------------------------------

        if document_url:

            safe_url = html.escape(
                document_url,
                quote=True
            )


            document_button = f"""

            <a
                href="{safe_url}"
                target="_blank"
                rel="noopener noreferrer"
                class="view-btn"
            >
                View
            </a>

            """

        else:

            document_button = """

            <span class="not-available">
                Not Available
            </span>

            """


        # ----------------------------------------------------
        # ROW HTML
        # ----------------------------------------------------

        rows_html += f"""

        <tr>

            <td>
                {sno}
            </td>

            <td>
                {standard}
            </td>

            <td>
                {document_no}
            </td>

            <td>
                {revision}
            </td>

            <td class="document-cell">
                {document_button}
            </td>

        </tr>

        """


    # ========================================================
    # EMPTY SEARCH RESULT
    # ========================================================

    if rows_html == "":

        rows_html = """

        <tr>

            <td
                colspan="5"
                class="empty-row"
            >
                No procedures found.
            </td>

        </tr>

        """


    # ========================================================
    # COMPLETE HTML TABLE
    # ========================================================

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

    <meta charset="UTF-8">

    <style>

    * {{
        box-sizing: border-box;
    }}


    html,
    body {{

        margin: 0;

        padding: 0;

        background: transparent;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        /* IMPORTANT:
           No internal scrollbar */
        overflow: hidden;
    }}


    /* ========================================================
       TABLE WRAPPER
       ======================================================== */

    .table-wrapper {{

        width: 100%;

        border:
            1px solid #d2e0ee;

        border-radius: 9px;

        overflow: hidden;

        box-shadow:
            0 1px 5px rgba(0,0,0,0.05);
    }}


    /* ========================================================
       TABLE
       ======================================================== */

    table {{

        width: 100%;

        border-collapse: collapse;

        table-layout: fixed;

        font-family:
            Arial,
            Helvetica,
            sans-serif;
    }}


    /* ========================================================
       HEADER
       ======================================================== */

    th {{

        height: 43px;

        background: #dceeff;

        color: #123f85;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        font-size: 13px;

        font-weight: 700;

        line-height: 1.1;

        text-align: left;

        padding:
            6px 16px;

        border-right:
            1px solid #c8d9e9;

        border-bottom:
            1px solid #c8d9e9;

        vertical-align: middle;

        white-space: nowrap;
    }}


    /* ========================================================
       BODY
       ======================================================== */

    td {{

        height: 34px;

        background: #ffffff;

        color: #123f85;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        font-size: 13px;

        font-weight: 400;

        line-height: 1.1;

        padding:
            5px 16px;

        border-right:
            1px solid #d7e3ee;

        border-bottom:
            1px solid #d7e3ee;

        vertical-align: middle;
    }}


    /* ========================================================
       ALTERNATING ROWS
       ======================================================== */

    tr:nth-child(even) td {{

        background: #f7fbff;
    }}


    /* ========================================================
       HOVER
       ======================================================== */

    tr:hover td {{

        background: #eef6ff;
    }}


    /* ========================================================
       COLUMN WIDTHS
       ======================================================== */

    th:nth-child(1),
    td:nth-child(1) {{

        width: 7%;
    }}


    th:nth-child(2),
    td:nth-child(2) {{

        width: 36%;
    }}


    th:nth-child(3),
    td:nth-child(3) {{

        width: 26%;
    }}


    th:nth-child(4),
    td:nth-child(4) {{

        width: 14%;
    }}


    th:nth-child(5),
    td:nth-child(5) {{

        width: 17%;
    }}


    /* ========================================================
       DOCUMENT
       ======================================================== */

    .document-cell {{

        text-align: center;

        vertical-align: middle;
    }}


    /* ========================================================
       VIEW BUTTON
       ======================================================== */

    .view-btn {{

        display: inline-block;

        width: 82px;

        height: 25px;

        padding:
            4px 8px;

        background: #0875d1;

        color: #ffffff !important;

        text-decoration: none !important;

        border-radius: 5px;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        font-size: 12px;

        font-weight: 500;

        line-height: 17px;

        text-align: center;

        cursor: pointer;
    }}


    .view-btn:hover {{

        background: #005eb8;

        color: #ffffff !important;
    }}


    /* ========================================================
       NOT AVAILABLE
       ======================================================== */

    .not-available {{

        color: #8aa0b8;

        font-family:
            Arial,
            Helvetica,
            sans-serif;

        font-size: 12px;

        font-weight: 400;
    }}


    /* ========================================================
       EMPTY RESULT
       ======================================================== */

    .empty-row {{

        height: 60px;

        text-align: center;

        color: #7890ad;

        font-size: 13px;

        font-weight: 400;
    }}

    </style>

    </head>

    <body>

        <div class="table-wrapper">

            <table>

                <thead>

                    <tr>

                        <th>
                            S. No.
                        </th>

                        <th>
                            Management Standard
                        </th>

                        <th>
                            Document No.
                        </th>

                        <th>
                            Revision
                        </th>

                        <th style="text-align:center;">
                            Document
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {rows_html}

                </tbody>

            </table>

        </div>

    </body>

    </html>

    """


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # ========================================================
    # LOAD SHEET
    # ========================================================

    df, links_df, error = load_google_sheet()


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    if error:

        st.error(
            "Unable to read the Google Sheet."
        )

        st.code(error)

        return


    if df is None or df.empty:

        st.warning(
            "No data found in "
            "'JSW Group Standards'."
        )

        return


    # ========================================================
    # FIND REQUIRED COLUMNS
    # ========================================================

    sno_col = find_column(
        df,
        [
            "S. No.",
            "S.No.",
            "S No.",
            "S No",
            "Serial No",
            "Sl No",
            "Sl. No."
        ]
    )


    standard_col = find_column(
        df,
        [
            "Management Standard",
            "Management Standards",
            "Standard"
        ]
    )


    document_col = find_column(
        df,
        [
            "Document No.",
            "Document No",
            "Document Number"
        ]
    )


    revision_col = find_column(
        df,
        [
            "Revision",
            "Revision No",
            "Rev",
            "Rev."
        ]
    )


    view_col = find_column(
        df,
        [
            "View Document",
            "Document",
            "View",
            "Document Link",
            "Document URL",
            "URL",
            "Link"
        ]
    )


    # ========================================================
    # FALLBACK
    # ========================================================

    if len(df.columns) >= 5:

        if sno_col is None:

            sno_col = df.columns[0]


        if standard_col is None:

            standard_col = df.columns[1]


        if document_col is None:

            document_col = df.columns[2]


        if revision_col is None:

            revision_col = df.columns[3]


        if view_col is None:

            view_col = df.columns[4]


    # ========================================================
    # CREATE DISPLAY DATA
    # ========================================================

    display_df = pd.DataFrame({

        "S. No.":

            df[sno_col]
            .fillna("")
            .apply(
                format_number
            ),


        "Management Standard":

            df[standard_col]
            .fillna("")
            .astype(str)
            .str.strip(),


        "Document No.":

            df[document_col]
            .fillna("")
            .astype(str)
            .str.strip(),


        "Revision":

            df[revision_col]
            .fillna("")
            .apply(
                format_number
            )
    })


    # ========================================================
    # DOCUMENT LINKS
    # ========================================================

    document_urls = []


    for row_index in range(
        len(df)
    ):

        url = ""


        if (
            links_df is not None
            and
            view_col in links_df.columns
        ):

            try:

                url = str(
                    links_df.iloc[
                        row_index
                    ][view_col]
                ).strip()

            except Exception:

                url = ""


        document_urls.append(
            url
        )


    display_df[
        "Document URL"
    ] = document_urls


    # ========================================================
    # REMOVE EMPTY ROWS
    # ========================================================

    display_df = display_df[
        ~(
            (display_df["S. No."].str.strip() == "") &
            (display_df["Management Standard"].str.strip() == "") &
            (display_df["Document No."].str.strip() == "")
        )
    ].copy()


    # ========================================================
    # TOP ROW
    #
    # KPI + SEARCH ARE IN REAL STREAMLIT COLUMNS
    # ========================================================

    kpi_column, search_column = st.columns(
        [1.05, 0.90],
        gap="large"
    )


    # ========================================================
    # KPI
    # ========================================================

    with kpi_column:

        total_procedures = len(
            display_df
        )


        kpi_html = create_kpi_html(
            total_procedures
        )


        components.html(
            kpi_html,
            height=88,
            scrolling=False
        )


    # ========================================================
    # SEARCH
    # ========================================================

    with search_column:

        search_text = st.text_input(
            "Search procedures",
            placeholder="🔍  Search procedures...",
            label_visibility="collapsed",
            key="procedure_search"
        )


    # ========================================================
    # FILTER
    # ========================================================

    if search_text.strip():

        search_value = (
            search_text
            .strip()
            .lower()
        )


        search_mask = display_df.apply(

            lambda row:

            row.astype(str)
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
            .any(),

            axis=1
        )


        filtered_df = display_df[
            search_mask
        ].copy()

    else:

        filtered_df = display_df.copy()


    # ========================================================
    # CREATE TABLE
    # ========================================================

    table_html = create_table_html(
        filtered_df
    )


    # ========================================================
    # TABLE HEIGHT
    #
    # IMPORTANT:
    #
    # No internal scrolling.
    #
    # Height is deliberately generous so that ALL rows
    # remain visible and the normal browser/page scrollbar
    # handles the page.
    # ========================================================

    number_of_rows = max(
        len(filtered_df),
        1
    )


    # Header = 43px
    # Each row = approximately 34px
    # Extra safety = 35px

    table_height = (
        43
        +
        (number_of_rows * 34)
        +
        35
    )


    # Additional minimum
    table_height = max(
        table_height,
        100
    )


    # ========================================================
    # DISPLAY TABLE
    #
    # scrolling=False IS IMPORTANT
    # ========================================================

    components.html(
        table_html,
        height=table_height,
        scrolling=False
    )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        f"""
        <div style="
            text-align:right;
            color:#7890ad;
            font-family:Arial,Helvetica,sans-serif;
            font-size:11px;
            margin-top:3px;
            margin-bottom:5px;
        ">
            Showing {len(filtered_df)}
            of {total_procedures}
            procedures
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()

