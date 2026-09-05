# ============================================================
# ALL DEPARTMENTS — HEADER
# ============================================================

from datetime import datetime
from pathlib import Path
import base64

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# LOGO PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

LOGO_PATH = (
    BASE_DIR.parent
    / "assets"
    / "jsw_jfe_logo.png"
)


# ============================================================
# LOAD LOGO
# ============================================================

if not LOGO_PATH.exists():
    raise FileNotFoundError(
        f"Logo file not found:\n{LOGO_PATH}"
    )

with open(LOGO_PATH, "rb") as f:
    logo_base64 = base64.b64encode(
        f.read()
    ).decode("utf-8")

logo_src = (
    f"data:image/png;base64,{logo_base64}"
)


# ============================================================
# DATE / TIME
# ============================================================

now = datetime.now()

date_text = now.strftime("%d-%b-%Y")
day_text = now.strftime("%A")
time_text = now.strftime("%I:%M:%S")
ampm_text = now.strftime("%p")


# ============================================================
# HEADER HTML
# ============================================================

header_html = f"""
<style>

html,
body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.psm-header {{

    width: 100%;

    height: 115px;

    box-sizing: border-box;

    position: relative;

    overflow: hidden;

    display: flex;

    align-items: center;

    padding: 6px 2%;

    background:
        linear-gradient(
            135deg,
            #ffffff 0%,
            #f5fbff 50%,
            #ffffff 100%
        );

    border-top: 3px solid #159ee5;

    border-bottom: 3px solid #159ee5;
}}


/* ============================================================
   LEFT DECORATION
   ============================================================ */

.psm-header::before {{

    content: "";

    position: absolute;

    left: 0;
    top: 0;

    width: 130px;
    height: 100%;

    background:
        linear-gradient(
            130deg,
            transparent 0%,
            transparent 34%,
            rgba(21,158,229,0.18) 35%,
            rgba(21,158,229,0.18) 48%,
            transparent 49%
        );

    pointer-events: none;
}}


/* ============================================================
   RIGHT DECORATION
   ============================================================ */

.psm-header::after {{

    content: "";

    position: absolute;

    right: 0;
    top: 0;

    width: 130px;
    height: 100%;

    background:
        linear-gradient(
            130deg,
            transparent 0%,
            transparent 34%,
            rgba(21,158,229,0.18) 35%,
            rgba(21,158,229,0.18) 48%,
            transparent 49%
        );

    transform: scaleX(-1);

    pointer-events: none;
}}


/* ============================================================
   LOGO AREA
   ============================================================ */

.psm-logo-area {{

    width: 29%;

    height: 100%;

    display: flex;

    align-items: center;

    justify-content: flex-start;

    z-index: 10;
}}


.psm-logo-box {{

    width: 100%;

    max-width: 350px;

    height: 88px;

    background: #ffffff;

    border: 2px solid #8ed7ff;

    border-radius: 16px;

    box-shadow:
        0 3px 10px rgba(0,80,140,0.14);

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 5px 12px;

    box-sizing: border-box;
}}


.psm-logo-img {{

    width: 220px;

    max-width: 95%;

    max-height: 58px;

    object-fit: contain;

    display: block;

    margin: 0 auto;
}}


/* ============================================================
   CENTER TITLE
   ============================================================ */

.psm-title-area {{

    flex: 1;

    height: 100%;

    display: flex;

    align-items: center;

    justify-content: center;

    margin-left: 2%;

    margin-right: 2%;

    z-index: 10;
}}


.psm-title-box {{

    width: 100%;

    max-width: 600px;

    height: 70px;

    background:
        linear-gradient(
            180deg,
            #0878c9 0%,
            #07528e 100%
        );

    border: 3px solid #8ed7ff;

    border-radius: 16px;

    box-shadow:
        0 4px 12px rgba(0,75,130,0.22),
        inset 0 0 18px rgba(255,255,255,0.08);

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 6px 15px;

    box-sizing: border-box;
}}


.psm-title-box h1 {{

    margin: 0;

    padding: 0;

    color: #ffd21c;

    font-size: 34px;

    font-weight: 900;

    letter-spacing: 1px;

    text-align: center;

    white-space: nowrap;
}}


/* ============================================================
   DATE / TIME AREA
   ============================================================ */

.psm-info-area {{

    width: 29%;

    height: 100%;

    display: flex;

    align-items: center;

    justify-content: flex-end;

    z-index: 10;
}}


.psm-info-box {{

    width: 100%;

    max-width: 350px;

    height: 75px;

    background: #ffffff;

    border: 2px solid #9ddaf7;

    border-radius: 16px;

    box-shadow:
        0 3px 10px rgba(0,80,140,0.12);

    padding: 6px 12px;

    box-sizing: border-box;
}}


.psm-info-row {{

    width: 100%;

    height: 100%;

    display: flex;

    align-items: center;

    justify-content: center;
}}


/* ============================================================
   DATE
   ============================================================ */

.psm-date-box {{

    width: 52%;

    height: 80%;

    display: flex;

    align-items: center;

    gap: 8px;

    border-right: 2px solid #b8dff5;

    padding-right: 12px;

    box-sizing: border-box;
}}


/* ============================================================
   TIME
   ============================================================ */

.psm-time-box {{

    width: 48%;

    height: 80%;

    display: flex;

    align-items: center;

    gap: 8px;

    padding-left: 12px;

    box-sizing: border-box;
}}


/* ============================================================
   ICON
   ============================================================ */

.psm-info-icon {{

    color: #159ee5;

    font-size: 27px;

    line-height: 1;
}}


/* ============================================================
   LABEL
   ============================================================ */

.psm-info-label {{

    color: #07528e;

    font-size: 9px;

    font-weight: 700;

    margin-bottom: 1px;
}}


/* ============================================================
   VALUE
   ============================================================ */

.psm-info-value {{

    color: #07528e;

    font-size: 14px;

    font-weight: 800;

    white-space: nowrap;
}}


/* ============================================================
   SUB VALUE
   ============================================================ */

.psm-info-sub {{

    color: #07528e;

    font-size: 10px;

    margin-top: 1px;
}}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1200px) {{

    .psm-header {{

        height: 105px;

        padding: 5px 1.5%;
    }}

    .psm-logo-box {{

        height: 80px;

        max-width: 310px;
    }}

    .psm-logo-img {{

        width: 190px;

        max-height: 52px;
    }}

    .psm-title-box {{

        height: 62px;

        max-width: 540px;
    }}

    .psm-title-box h1 {{

        font-size: 29px;
    }}

    .psm-info-box {{

        height: 68px;

        max-width: 320px;
    }}

    .psm-info-icon {{

        font-size: 24px;
    }}

    .psm-info-value {{

        font-size: 12px;
    }}

    .psm-info-label {{

        font-size: 8px;
    }}

    .psm-info-sub {{

        font-size: 9px;
    }}
}}

</style>


<!-- ============================================================
     HEADER
     ============================================================ -->

<div class="psm-header">


    <!-- ========================================================
         LEFT — JSW JFE LOGO
         ======================================================== -->

    <div class="psm-logo-area">

        <div class="psm-logo-box">

            <img
                class="psm-logo-img"
                src="{logo_src}"
                alt="JSW JFE Steel Limited"
            >

        </div>

    </div>


    <!-- ========================================================
         CENTER — ALL DEPARTMENTS
         ======================================================== -->

    <div class="psm-title-area">

        <div class="psm-title-box">

            <h1>
                ALL DEPARTMENTS
            </h1>

        </div>

    </div>


    <!-- ========================================================
         RIGHT — DATE / TIME
         ======================================================== -->

    <div class="psm-info-area">

        <div class="psm-info-box">

            <div class="psm-info-row">


                <!-- DATE -->

                <div class="psm-date-box">

                    <div class="psm-info-icon">
                        ▣
                    </div>

                    <div>

                        <div class="psm-info-label">
                            DATE
                        </div>

                        <div class="psm-info-value">
                            {date_text}
                        </div>

                        <div class="psm-info-sub">
                            {day_text}
                        </div>

                    </div>

                </div>


                <!-- TIME -->

                <div class="psm-time-box">

                    <div class="psm-info-icon">
                        ◷
                    </div>

                    <div>

                        <div class="psm-info-label">
                            TIME
                        </div>

                        <div class="psm-info-value">
                            {time_text}
                        </div>

                        <div class="psm-info-sub">
                            {ampm_text}
                        </div>

                    </div>

                </div>


            </div>

        </div>

    </div>


</div>
"""


# ============================================================
# DISPLAY HEADER
# ============================================================

components.html(
    header_html,
    height=120,
    scrolling=False,
)