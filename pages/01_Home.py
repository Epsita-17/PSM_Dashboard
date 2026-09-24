import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JSW PSM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STREAMLIT PAGE CSS
# ============================================================

st.markdown("""
<style>

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    background: #ffffff !important;
}

.stApp {
    background: #ffffff !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 100% !important;
    margin-top: -20px !important;

}


footer {
    display: none !important;
    visibility: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD PSM WHEEL IMAGE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# PSM_Wheel.png is kept in the same folder as this Python file.
PSM_WHEEL_PATH = BASE_DIR / "PSM_Wheel.png"

try:

    with open(PSM_WHEEL_PATH, "rb") as image_file:

        psm_wheel_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

except FileNotFoundError:

    st.error(
        f"PSM Wheel image not found: {PSM_WHEEL_PATH}. "
        "Please keep PSM_Wheel.png in the same folder as this Python file."
    )

    st.stop()

# ============================================================
# MONTHS
# ============================================================

months = [
    "Apr-26",
    "May-26",
    "Jun-26",
    "Jul-26",
    "Aug-26",
    "Sep-26",
    "Oct-26",
    "Nov-26",
    "Dec-26",
    "Jan-27",
    "Feb-27",
    "Mar-27"
]

# ============================================================
# ROADMAP DATA
#
# 48 WEEKS
#
# Apr-26  = Week 1-4
# May-26  = Week 5-8
# Jun-26  = Week 9-12
# Jul-26  = Week 13-16
# Aug-26  = Week 17-20
# Sep-26  = Week 21-24
# Oct-26  = Week 25-28
# Nov-26  = Week 29-32
# Dec-26  = Week 33-36
# Jan-27  = Week 37-40
# Feb-27  = Week 41-44
# Mar-27  = Week 45-48
# ============================================================

roadmap_data = {

    "PT": [
        (1, 4, "2nd PT"),
        (17, 4, "3rd PT"),
        (33, 4, "4th PT")
    ],

    "PHA": [
        (5, 12, "2nd PHA"),
        (21, 12, "3rd PHA"),
        (37, 8, "4th PHA")
    ],

    "LOPA": [
        (13, 4, "For 2nd PHA"),
        (29, 4, "For 3rd PHA"),
        (45, 4, "For 4th PHA")
    ],

    "BOW TIE": [
        (13, 4, "For 2nd PHA"),
        (29, 4, "For 3rd PHA"),
        (45, 4, "For 4th PHA")
    ],

    "OP": [
        (1, 4, "1st OP"),
        (33, 4, "2nd OP")
    ],

    "MOC": [
        (1, 8, "MOC Training")
    ],

    "PSSR": [
        (1, 4, "PSSR Training")
    ],

    "MIQA": [
        (21, 16, "MIQA Training")
    ],

    "Incident Investigation": [
        (37, 12, "")
    ],

    "Emergency Plan": [
        (37, 12, "")
    ]
}


# ============================================================
# CREATE ROADMAP ROW
# ============================================================

def create_roadmap_row(activity, activities):
    row = f"""
    <tr>

        <td class="activity-name">
            {activity}
        </td>
    """

    current_week = 1

    # --------------------------------------------------------
    # ACTIVITY BLOCKS
    # --------------------------------------------------------

    for start, duration, label in activities:

        # EMPTY CELLS BEFORE ACTIVITY
        while current_week < start:
            row += """
                <td class="roadmap-week empty"></td>
            """

            current_week += 1

        # ----------------------------------------------------
        # MERGED ACTIVITY CELL
        # ----------------------------------------------------

        row += f"""
            <td
                class="roadmap-week activity"
                colspan="{duration}"
            >
                {label}
            </td>
        """

        current_week += duration

    # --------------------------------------------------------
    # EMPTY CELLS AFTER ACTIVITY
    # --------------------------------------------------------

    while current_week <= 48:
        row += """
            <td class="roadmap-week empty"></td>
        """

        current_week += 1

    row += """
    </tr>
    """

    return row


# ============================================================
# CREATE ALL ROADMAP ROWS
# ============================================================

roadmap_rows = ""

for activity, activities in roadmap_data.items():
    roadmap_rows += create_roadmap_row(
        activity,
        activities
    )

# ============================================================
# FY 25-26 ROADMAP DATA
# Source: attached "PSM Journey Plan(FY 25-26)" PDF
# ============================================================

months_25 = [
    "May-25", "Jun-25", "Jul-25", "Aug-25", "Sep-25",
    "Oct-25", "Nov-25", "Dec-25", "Jan-26", "Feb-26", "Mar-26"
]

# 44 weeks: May-25 to Mar-26, 4 weeks per month.
# Blue Plan blocks reproduced from the attached PDF.
fy25_plan_data = {
    "PT": [(3, 10, "1st PT")],
    "PHA": [(17, 20, "1st PHA")],
    "LOPA": [(29, 4, "")],
    "BOW TIE": [(33, 4, "")],
    "OP": [],
    "MOC": [],
    "PSSR": [],
    "MIQA": [],
    "Incident Investigation": [],
    "Emergency Plan": [],
}


def create_fy25_roadmap_rows():
    rows = ""

    for activity, activities in fy25_plan_data.items():

        # PLAN
        rows += f"""
        <tr>
            <td class="activity-name-fy25" rowspan="2">{activity}</td>
            <td class="plan-actual-cell-fy25">Plan</td>
        """

        current_week = 1

        for start, duration, label in activities:
            while current_week < start:
                rows += '<td class="roadmap-week-fy25 empty"></td>'
                current_week += 1

            rows += f"""
                <td class="roadmap-week-fy25 activity-fy25" colspan="{duration}">
                    {label}
                </td>
            """
            current_week += duration

        while current_week <= 44:
            rows += '<td class="roadmap-week-fy25 empty"></td>'
            current_week += 1

        rows += "</tr>"

        # ACTUAL — blank because the attached PDF has no blue Actual blocks.
        rows += """
        <tr>
            <td class="plan-actual-cell-fy25">Actual</td>
        """
        rows += '<td class="roadmap-week-fy25 empty"></td>' * 44
        rows += "</tr>"

    return rows


fy25_roadmap_rows = create_fy25_roadmap_rows()

fy25_month_header = ""
for month in months_25:
    fy25_month_header += f"""
        <th class="month-header-fy25" colspan="4">{month}</th>
    """

fy25_week_header = ""
for month in months_25:
    for week in range(1, 5):
        fy25_week_header += f"""
            <th class="week-header-fy25">{week}</th>
        """

# ============================================================
# MONTH HEADER
# ============================================================

month_header = ""

for month in months:
    month_header += f"""
        <th
            class="month-header"
            colspan="4"
        >
            {month}
        </th>
    """

# ============================================================
# WEEK HEADER
# ============================================================

week_header = ""

for month in months:

    for week in range(1, 5):
        week_header += f"""
            <th class="week-header">
                {week}
            </th>
        """

# ============================================================
# COMPLETE DASHBOARD HTML
# ============================================================

dashboard_html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">


<style>


/* ============================================================
   GLOBAL
   ============================================================ */

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: Arial, Helvetica, sans-serif;
}}


/* ============================================================
   COMMON SECTION GAP
   ============================================================ */

.section-gap {{

    height: 8px;

    width: 100%;

    margin: 0;

    padding: 0;

}}


/* ============================================================
   SECTION 1
   ============================================================ */

.info-section {{

    width: 100%;

    background: #ffffff;

    border: 2.5px solid #0876c9;

    border-radius: 15px;

    padding: 20px 24px;

    display: flex;

    align-items: stretch;

}}


/* ============================================================
   SECTION 1 COLUMNS
   ============================================================ */

.info-column {{

    width: 33.3333%;

    padding: 0 22px;

    color: #123f82;

    font-size: 16px;

    line-height: 1.28;

}}

.info-column:first-child {{

    padding-left: 0;

}}

.info-column:last-child {{

    padding-right: 0;

}}

.info-column:not(:last-child) {{

    border-right: 1.5px solid #4aa9e8;

}}


/* ============================================================
   SECTION 1 RED LINE
   ============================================================ */

.info-red-line {{

    width: 105px;

    height: 5px;

    background: #ff1717;

    margin-bottom: 12px;

}}


/* ============================================================
   SECTION 1 PARAGRAPH
   ============================================================ */

.info-column p {{

    margin: 0 0 10px 0;

}}


/* ============================================================
   TEXT COLOURS
   ============================================================ */

.jsw-red {{

    color: #e21b23;

    font-weight: 700;

}}

.psm-red {{

    color: #f01919;

    font-weight: 700;

}}

.blue-bold {{

    color: #123f82;

    font-weight: 700;

}}


/* ============================================================
   SECTION 2 - PSM WHEEL
   ============================================================ */

.psm-section {{

    width: 100%;

    background: #ffffff;

    border: 2.5px solid #0876c9;

    border-radius: 15px;

    padding: 18px 22px 20px 22px;

    margin: 0;

    overflow: hidden;

}}


/* ============================================================
   PSM RED LINE
   ============================================================ */

.psm-red-line {{

    width: 105px;

    height: 5px;

    background: #ff1717;

    margin-bottom: 10px;

}}


/* ============================================================
   PSM TITLE
   ============================================================ */

.psm-title {{

    color: #123f82;

    font-size: 30px;

    font-weight: 700;

    line-height: 1.15;

    margin: 0;

    padding-bottom: 10px;

    border-bottom: 3px solid #0876c9;

}}


/* ============================================================
   PSM IMAGE
   ============================================================ */

.psm-image-container {{

    width: 100%;

    text-align: center;

    margin-top: 8px;

    padding: 0;

    line-height: 0;

}}

.psm-image {{

    display: block;

    width: 100%;

    max-width: 100%;

    height: auto;

    margin: 0 auto;

}}


/* ============================================================
   SECTION 3 - ROADMAP
   ============================================================ */

.roadmap-section {{

    width: 100%;

    background: #ffffff;

    border: 2.5px solid #0876c9;

    border-radius: 15px;

    padding: 18px 20px 20px 20px;

    margin: 0;

    overflow: hidden;

}}


/* ============================================================
   ROADMAP RED LINE
   ============================================================ */

.roadmap-red-line {{

    width: 105px;

    height: 5px;

    background: #ff1717;

    margin-bottom: 10px;

}}


/* ============================================================
   ROADMAP TITLE
   ============================================================ */

.roadmap-title {{

    color: #123f82;

    font-size: 30px;

    font-weight: 700;

    line-height: 1.15;

    margin: 0;

    padding-bottom: 10px;

    border-bottom: 3px solid #0876c9;

}}


/* ============================================================
   ROADMAP TABLE
   ============================================================ */

.roadmap-table {{

    width: 100%;

    max-width: 100%;

    table-layout: fixed;

    border-collapse: collapse;

    border-spacing: 0;

    margin-top: 12px;

    margin-left: 0;

    margin-right: 0;

}}


/* ============================================================
   ACTIVITIES HEADER
   SAME COLOUR AS MONTHS
   ============================================================ */

.activities-header {{

    width: 14%;

    background: #b9dce9 !important;

    border: 1px solid #000000;

    color: #000000;

    font-size: 11px;

    font-weight: 700;

    text-align: center;

    vertical-align: middle;

    padding: 0;

}}


/* ============================================================
   MONTH HEADER
   ============================================================ */

.month-header {{

    background: #b9dce9 !important;

    border: 1px solid #000000;

    color: #000000;

    height: 42px;

    font-size: 11px;

    font-weight: 700;

    text-align: center;

    vertical-align: middle;

    padding: 0;

    white-space: nowrap;

}}


/* ============================================================
   WEEK HEADER
   SAME COLOUR AS MONTH
   ============================================================ */

.week-header {{

    background: #b9dce9 !important;

    border: 1px solid #000000;

    color: #000000;

    height: 25px;

    font-size: 8px;

    font-weight: 600;

    text-align: center;

    vertical-align: middle;

    padding: 0;

}}


/* ============================================================
   ACTIVITY NAME
   ============================================================ */

.activity-name {{

    width: 14%;

    height: 40px;

    background: #ffffff;

    border: 1px solid #000000;

    color: #000000;

    font-size: 11px;

    font-weight: 700;

    text-align: center;

    vertical-align: middle;

    padding: 0 2px;

    white-space: nowrap;

    overflow: hidden;

}}


/* ============================================================
   ALL WEEK CELLS
   ============================================================ */

.roadmap-week {{

    height: 40px;

    border: 1px solid #000000;

    padding: 0;

    margin: 0;

    text-align: center;

    vertical-align: middle;

    overflow: hidden;

}}


/* ============================================================
   EMPTY CELLS
   ============================================================ */

.roadmap-week.empty {{

    background: #ffffff;

}}


/* ============================================================
   MERGED ACTIVITY CELLS
   ============================================================ */

.roadmap-week.activity {{

    background: #17617e;

    color: #ffffff;

    border: 1px solid #000000;

    font-size: 9px;

    font-weight: 700;

    text-align: center;

    vertical-align: middle;

    white-space: nowrap;

    overflow: hidden;

    padding: 0 2px;

}}


/* ============================================================
   PREVENT HORIZONTAL OVERFLOW
   ============================================================ */

.roadmap-table,
.roadmap-table tr,
.roadmap-table td,
.roadmap-table th {{

    max-width: 100%;

}}


/* ============================================================
   FY 25-26 ROADMAP
   ============================================================ */

.roadmap-section-fy25 {{

    width: 100%;
    background: #ffffff;
    border: 2.5px solid #0876c9;
    border-radius: 15px;
    padding: 18px 20px 20px 20px;
    margin: 0;
    overflow: hidden;

}}

.roadmap-red-line-fy25 {{
    width: 105px;
    height: 5px;
    background: #ff1717;
    margin-bottom: 10px;
}}

.roadmap-title-fy25 {{
    color: #123f82;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.15;
    margin: 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #0876c9;
}}

.roadmap-table-fy25 {{
    width: 100%;
    max-width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    border-spacing: 0;
    margin-top: 12px;
}}

.activities-header-fy25 {{
    width: 12%;
    background: #b9dce9 !important;
    border: 1px solid #000000;
    color: #000000;
    font-size: 11px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    padding: 0;
}}

.plan-header-fy25 {{
    width: 4%;
    background: #b9dce9 !important;
    border: 1px solid #000000;
    color: #000000;
    font-size: 10px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    padding: 0;
}}

.month-header-fy25 {{
    background: #b9dce9 !important;
    border: 1px solid #000000;
    color: #000000;
    height: 42px;
    font-size: 11px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    padding: 0;
    white-space: nowrap;
}}

.week-header-fy25 {{
    background: #b9dce9 !important;
    border: 1px solid #000000;
    color: #000000;
    height: 25px;
    font-size: 8px;
    font-weight: 600;
    text-align: center;
    vertical-align: middle;
    padding: 0;
}}

.activity-name-fy25 {{
    width: 12%;
    height: 40px;
    background: #ffffff;
    border: 1px solid #000000;
    color: #000000;
    font-size: 11px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    padding: 0 2px;
    white-space: nowrap;
    overflow: hidden;
}}

.plan-actual-cell-fy25 {{
    width: 4%;
    height: 20px;
    background: #ffffff;
    border: 1px solid #000000;
    color: #000000;
    font-size: 9px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    padding: 0;
}}

.roadmap-week-fy25 {{
    height: 20px;
    border: 1px solid #000000;
    padding: 0;
    margin: 0;
    text-align: center;
    vertical-align: middle;
    overflow: hidden;
}}

.roadmap-week-fy25.empty {{
    background: #ffffff;
}}

.roadmap-week-fy25.activity-fy25 {{
    background: #17617e;
    color: #ffffff;
    border: 1px solid #000000;
    font-size: 9px;
    font-weight: 700;
    text-align: center;
    vertical-align: middle;
    white-space: nowrap;
    overflow: hidden;
    padding: 0 2px;
}}


/* ============================================================
   1400px AND BELOW
   ============================================================ */

@media screen and (max-width: 1400px) {{

    .month-header {{

        font-size: 10px;

    }}

    .week-header {{

        font-size: 7px;

    }}

    .activity-name {{

        font-size: 10px;

    }}

    .roadmap-week.activity {{

        font-size: 8px;

    }}

}}


/* ============================================================
   1100px AND BELOW
   ============================================================ */

@media screen and (max-width: 1100px) {{

    .info-column {{

        font-size: 14px;

    }}

    .psm-title,
    .roadmap-title {{

        font-size: 27px;

    }}

    .month-header {{

        font-size: 9px;

    }}

    .week-header {{

        font-size: 6px;

    }}

    .activity-name {{

        font-size: 9px;

    }}

    .roadmap-week.activity {{

        font-size: 7px;

    }}

}}


/* ============================================================
   MOBILE
   ============================================================ */

@media screen and (max-width: 800px) {{

    .info-section {{

        flex-direction: column;

    }}

    .info-column {{

        width: 100%;

        padding: 15px 0 !important;

        border-right: none !important;

        border-bottom: 1.5px solid #4aa9e8;

    }}

    .info-column:last-child {{

        border-bottom: none;

    }}

    .psm-title,
    .roadmap-title {{

        font-size: 22px;

    }}

}}


</style>

</head>


<body>


<!-- ============================================================
     SECTION 1
============================================================= -->

<div class="info-section">


    <!-- COLUMN 1 -->

    <div class="info-column">

        <div class="info-red-line"></div>

        <p>

            At
            <span class="jsw-red">JSW</span>,

            <span class="blue-bold">
                safety is a fundamental value and an integral
                part of operational excellence.
            </span>

        </p>

        <p>

            We are committed to protecting our

            <span class="blue-bold">
                people, assets, environment
            </span>

            and ensuring

            <span class="blue-bold">
                business continuity.
            </span>

        </p>

    </div>


    <!-- COLUMN 2 -->

    <div class="info-column">

        <div class="info-red-line"></div>

        <p>

            <span class="psm-red">
                Process Safety Management (PSM)
            </span>

            is a systematic framework for managing major
            process-related risks across the lifecycle of
            operations, from design and commissioning to
            operation, maintenance, modification and
            decommissioning.

        </p>

    </div>


    <!-- COLUMN 3 -->

    <div class="info-column">

        <div class="info-red-line"></div>

        <p>

            Through defined standards, procedures,
            assessments and continuous monitoring,

            <span class="blue-bold">
                JSW
            </span>

            ensures that safety barriers remain effective,
            strengthening

            <span class="blue-bold">
                operational discipline
            </span>

            and enabling

            <span class="blue-bold">
                safe, reliable and sustainable operations.
            </span>

        </p>

    </div>


</div>


<!-- ============================================================
     GAP 1 → 2
============================================================= -->

<div class="section-gap"></div>


<!-- ============================================================
     SECTION 2 - PSM WHEEL
============================================================= -->

<div class="psm-section">


    <div class="psm-red-line"></div>


    <div class="psm-title">
        PSM Wheel
    </div>


    <div class="psm-image-container">

        <img
            class="psm-image"
            src="data:image/png;base64,{psm_wheel_base64}"
            alt="PSM Wheel"
        >

    </div>


</div>


<!-- ============================================================
     GAP 2 → 3
     SAME GAP AS SECTION 1 → 2
============================================================= -->

<div class="section-gap"></div>


<!-- ============================================================
     SECTION 3 - ROADMAP
============================================================= -->

<div class="roadmap-section">


    <div class="roadmap-red-line"></div>


    <div class="roadmap-title">
        Roadmap (FY26-27)
    </div>


    <table class="roadmap-table">


        <!-- ====================================================
             MONTH HEADER
        ===================================================== -->

        <tr>

            <th
                class="activities-header"
                rowspan="2"
            >
                Activities
            </th>

            {month_header}

        </tr>


        <!-- ====================================================
             WEEK HEADER
        ===================================================== -->

        <tr>

            {week_header}

        </tr>


        <!-- ====================================================
             ROADMAP DATA
        ===================================================== -->

        {roadmap_rows}


    </table>


</div>


<!-- ============================================================
     SECTION 4 - ROADMAP FY25-26
============================================================= -->

<div class="section-gap"></div>

<div class="roadmap-section-fy25">

    <div class="roadmap-red-line-fy25"></div>

    <div class="roadmap-title-fy25">
        Roadmap (FY25-26)
    </div>

    <table class="roadmap-table-fy25">

        <tr>

            <th class="activities-header-fy25" rowspan="2">
                Activities
            </th>

            <th class="plan-header-fy25" rowspan="2">
                Status
            </th>

            {fy25_month_header}

        </tr>

        <tr>
            {fy25_week_header}
        </tr>

        {fy25_roadmap_rows}

    </table>

</div>


</body>

</html>

"""

# ============================================================
# RENDER COMPLETE DASHBOARD
# ============================================================

components.html(
    dashboard_html,
    height=3100,
    scrolling=False
)

