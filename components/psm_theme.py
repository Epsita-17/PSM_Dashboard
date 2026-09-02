import streamlit as st
import streamlit.components.v1 as components
from html import escape


# ============================================================
# COMMON PSM THEME
# ============================================================

def apply_psm_theme():

    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN STREAMLIT PAGE
           ===================================================== */

        .stApp {
            background: #f4f9fc;
        }

        .block-container {
            padding-top: 0.4rem;
            padding-left: 0.4rem;
            padding-right: 0.4rem;
            max-width: 100%;
        }


        /* =====================================================
           SECTION HEADER
           ===================================================== */

        .psm-section {
            width: 100%;
            margin: 8px 0 5px;
            padding: 9px 12px;

            background:
                linear-gradient(
                    180deg,
                    #1679bd 0%,
                    #075896 100%
                );

            border-radius: 7px;

            color: #ffffff;

            text-align: center;

            font-size: 14px;
            font-weight: 900;

            letter-spacing: 0.8px;

            box-shadow:
                0 3px 8px rgba(25, 83, 118, 0.12);
        }


        /* =====================================================
           KPI CARD
           ===================================================== */

        .psm-card {
            background: #ffffff;

            border: 1px solid #8db2d5;

            border-radius: 8px;

            padding: 12px;

            text-align: center;

            box-shadow:
                0 2px 6px rgba(25, 83, 118, 0.08);
        }


        .psm-card-title {
            color: #07366b;

            font-size: 12px;

            font-weight: 800;
        }


        .psm-card-value {
            color: #07366b;

            font-size: 28px;

            font-weight: 800;

            margin-top: 4px;
        }


        /* =====================================================
           STREAMLIT BUTTON
           ===================================================== */

        .stButton > button {

            border-radius: 7px !important;

            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f1f7fa
                ) !important;

            border:
                1px solid #b8d5e7 !important;

            color:
                #116aa5 !important;

            font-weight:
                800 !important;

            box-shadow:
                0 2px 6px
                rgba(25,83,118,.10) !important;
        }


        .stButton > button:hover {

            border-color:
                #078fd2 !important;

            color:
                #07518b !important;
        }


        /* =====================================================
           SELECTBOX
           ===================================================== */

        div[data-baseweb="select"] > div {

            border-color:
                #b8d5e7 !important;

            border-radius:
                7px !important;

            background:
                #ffffff !important;
        }


        /* =====================================================
           DOWNLOAD BUTTON
           ===================================================== */

        div.stDownloadButton > button {

            border-radius:
                7px !important;

            background:
                linear-gradient(
                    180deg,
                    #ffffff,
                    #f1f7fa
                ) !important;

            border:
                1px solid #b8d5e7 !important;

            color:
                #116aa5 !important;

            box-shadow:
                0 2px 6px
                rgba(25,83,118,.10) !important;
        }


        /* =====================================================
           DATAFRAME
           ===================================================== */

        [data-testid="stDataFrame"] {

            border:
                1px solid #b8d5e7;

            border-radius:
                7px;
        }


        /* =====================================================
           ALERT
           ===================================================== */

        div[data-testid="stAlert"] {

            border-radius:
                7px !important;

            box-shadow:
                0 2px 7px
                rgba(20,70,100,.08) !important;
        }


        /* =====================================================
           SCROLLBAR
           ===================================================== */

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #eef4f7;
        }

        ::-webkit-scrollbar-thumb {
            background: #a9c9dc;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #6ea9c8;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COMMON PSM HEADER
# ============================================================

def psm_header(pillar_name="PSM DASHBOARD"):

    pillar_name = escape(str(pillar_name))

    header_html = f"""
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

    width: 100%;
    height: 100%;

    overflow: hidden;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}}


body {{
    background:
        #f4f9fc;
}}


/* =====================================================
   HEADER
   ===================================================== */

.header {{

    position: relative;

    width: 100%;

    height: 145px;

    overflow: hidden;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        radial-gradient(
            ellipse at center,
            rgba(55,160,218,.24) 0%,
            rgba(223,242,252,.82) 45%,
            rgba(244,250,253,.98) 100%
        ),
        linear-gradient(
            180deg,
            #edf8fd 0%,
            #dceff8 100%
        );

    border-top:
        2px solid #0b91d1;

    border-bottom:
        3px solid #1487c2;

    box-shadow:
        0 4px 12px
        rgba(21,92,130,.18);
}}


/* =====================================================
   TECH DOTS
   ===================================================== */

.header::before {{

    content: "";

    position: absolute;

    inset: 0;

    background-image:
        radial-gradient(
            circle,
            rgba(0,122,190,.17) 1.2px,
            transparent 1.5px
        );

    background-size:
        15px 15px;

    opacity:
        .65;
}}


/* =====================================================
   SIDE INDUSTRIAL BLUE ANGLES
   ===================================================== */

.header::after {{

    content: "";

    position: absolute;

    inset: 0;

    background:

        linear-gradient(
            135deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        ),

        linear-gradient(
            315deg,
            transparent 0 7%,
            rgba(0,133,210,.12) 7% 8%,
            transparent 8% 11%,
            rgba(0,133,210,.08) 11% 12%,
            transparent 12%
        );
}}


/* =====================================================
   INDUSTRIAL SVG
   ===================================================== */

.industrial {{

    position: absolute;

    left: 0;
    right: 0;
    bottom: 0;

    width: 100%;

    height: 145px;

    opacity:
        .38;

    z-index:
        1;
}}


.industrial .steel {{

    fill:
        #a8c9da;

    stroke:
        #5791af;

    stroke-width:
        1.5;
}}


.industrial .light {{

    fill:
        none;

    stroke:
        #2e8bb9;

    stroke-width:
        1.2;

    opacity:
        .70;
}}


.industrial .window {{

    fill:
        #2787b5;

    opacity:
        .65;
}}


.hex {{

    fill:
        none;

    stroke:
        #278abd;

    stroke-width:
        1;

    opacity:
        .28;
}}


/* =====================================================
   HEADER CONTENT
   ===================================================== */

.content {{

    position:
        relative;

    z-index:
        8;

    width:
        100%;

    height:
        100%;

    display:
        flex;

    flex-direction:
        column;

    align-items:
        center;

    justify-content:
        center;

    text-align:
        center;
}}


/* =====================================================
   PSM DASHBOARD
   ===================================================== */

.title {{

    color:
        #153e68;

    font-size:
        24px;

    font-weight:
        950;

    letter-spacing:
        5px;

    line-height:
        1;

    margin-bottom:
        5px;

    text-shadow:
        0 1px 1px
        rgba(255,255,255,.9);
}}


/* =====================================================
   PILLAR
   ===================================================== */

.pillar {{

    position:
        relative;

    width:
        560px;

    max-width:
        90%;

    height:
        66px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            180deg,
            #176ca5 0%,
            #07518b 55%,
            #063e70 100%
        );

    border:
        1px solid #0877ba;

    border-radius:
        14px;

    color:
        #ffd21a;

    font-size:
        34px;

    font-weight:
        950;

    letter-spacing:
        1px;

    box-shadow:
        0 7px 16px
        rgba(11,83,130,.25),

        inset 0 1px 0
        rgba(255,255,255,.28),

        inset 0 -5px 12px
        rgba(0,35,75,.16);
}}


.pillar::before,
.pillar::after {{

    position:
        absolute;

    top:
        50%;

    transform:
        translateY(-50%);

    color:
        #51c5ff;

    font-size:
        21px;

    font-weight:
        950;

    letter-spacing:
        -5px;

    text-shadow:
        0 1px 5px
        rgba(0,100,160,.5);
}}


.pillar::before {{

    content:
        "◀◀";

    left:
        17px;
}}


.pillar::after {{

    content:
        "▶▶";

    right:
        17px;
}}


/* =====================================================
   SUBTITLE
   ===================================================== */

.subtitle {{

    margin-top:
        7px;

    height:
        25px;

    min-width:
        700px;

    max-width:
        90%;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    padding:
        4px 30px;

    background:
        linear-gradient(
            90deg,
            #075b8e,
            #1188c4,
            #075b8e
        );

    border:
        1px solid #078fd2;

    border-radius:
        7px;

    color:
        #ffffff;

    font-size:
        10px;

    font-weight:
        900;

    letter-spacing:
        1.8px;

    box-shadow:
        0 4px 9px
        rgba(10,93,140,.20),

        inset 0 1px 0
        rgba(255,255,255,.25);
}}


/* =====================================================
   TOP BLUE ENERGY LINE
   ===================================================== */

.top-line {{

    position:
        absolute;

    top:
        0;

    left:
        24%;

    width:
        52%;

    height:
        3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00a9ff 18%,
            #ffffff 50%,
            #00a9ff 82%,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,169,255,.55);
}}


/* =====================================================
   ANIMATED BOTTOM SCAN
   ===================================================== */

.scan {{

    position:
        absolute;

    z-index:
        12;

    bottom:
        0;

    left:
        -16%;

    width:
        16%;

    height:
        4px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00b5ff,
            #ffffff,
            #00b5ff,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,181,255,.55);

    animation:
        scanline 3s linear infinite;
}}


@keyframes scanline {{

    0% {{
        left:
            -16%;
    }}

    100% {{
        left:
            100%;
    }}
}}


/* =====================================================
   CORNER BLUE LIGHTS
   ===================================================== */

.corner-light {{

    position:
        absolute;

    z-index:
        10;

    width:
        110px;

    height:
        3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00baff,
            transparent
        );

    box-shadow:
        0 0 8px
        rgba(0,186,255,.55);
}}


.corner-left {{

    left:
        7%;

    top:
        7px;
}}


.corner-right {{

    right:
        7%;

    top:
        7px;
}}

</style>

</head>


<body>

<div class="header">

    <div class="top-line"></div>

    <div class="corner-light corner-left"></div>

    <div class="corner-light corner-right"></div>


    <!-- =================================================
         INDUSTRIAL BACKGROUND
         ================================================= -->

    <svg
        class="industrial"
        viewBox="0 0 1672 145"
        preserveAspectRatio="none"
        aria-hidden="true"
    >


        <!-- LEFT TOWER -->

        <g>

            <rect
                class="steel"
                x="85"
                y="24"
                width="34"
                height="116"
                rx="4"
            />

            <rect
                class="steel"
                x="91"
                y="9"
                width="22"
                height="18"
            />

            <rect
                class="steel"
                x="96"
                y="0"
                width="12"
                height="12"
            />

            <path
                class="light"
                d="
                    M102 0 L102 140
                    M87 55 L117 55
                    M87 78 L117 78
                    M87 103 L117 103
                "
            />

            <circle
                class="window"
                cx="102"
                cy="43"
                r="3"
            />

            <circle
                class="window"
                cx="102"
                cy="67"
                r="3"
            />

            <circle
                class="window"
                cx="102"
                cy="91"
                r="3"
            />

        </g>


        <!-- LEFT STACK -->

        <g>

            <rect
                class="steel"
                x="150"
                y="52"
                width="17"
                height="88"
            />

            <rect
                class="steel"
                x="146"
                y="48"
                width="25"
                height="8"
            />

            <path
                class="light"
                d="M158 52 L158 140"
            />

        </g>


        <!-- LEFT PIPE NETWORK -->

        <g class="light">

            <path
                d="M55 113 H245 V85 H320"
            />

            <path
                d="M120 125 H260 V105 H355"
            />

            <path
                d="M180 96 H285 V65 H340"
            />

            <path
                d="M215 130 V70 H280"
            />

        </g>


        <!-- LEFT VESSEL -->

        <g>

            <rect
                class="steel"
                x="260"
                y="64"
                width="58"
                height="76"
                rx="26"
            />

            <path
                class="light"
                d="
                    M260 82 H318
                    M260 107 H318
                "
            />

            <circle
                class="window"
                cx="289"
                cy="95"
                r="4"
            />

        </g>


        <!-- RIGHT TOWER -->

        <g>

            <rect
                class="steel"
                x="1512"
                y="25"
                width="36"
                height="115"
                rx="4"
            />

            <rect
                class="steel"
                x="1518"
                y="9"
                width="24"
                height="18"
            />

            <rect
                class="steel"
                x="1523"
                y="0"
                width="14"
                height="12"
            />

            <path
                class="light"
                d="
                    M1530 0 L1530 140
                    M1514 54 L1546 54
                    M1514 79 L1546 79
                    M1514 103 L1546 103
                "
            />

            <circle
                class="window"
                cx="1530"
                cy="42"
                r="3"
            />

            <circle
                class="window"
                cx="1530"
                cy="66"
                r="3"
            />

            <circle
                class="window"
                cx="1530"
                cy="90"
                r="3"
            />

        </g>


        <!-- RIGHT STACK -->

        <g>

            <rect
                class="steel"
                x="1450"
                y="54"
                width="18"
                height="86"
            />

            <rect
                class="steel"
                x="1446"
                y="49"
                width="26"
                height="8"
            />

            <path
                class="light"
                d="M1459 54 L1459 140"
            />

        </g>


        <!-- RIGHT PIPE NETWORK -->

        <g class="light">

            <path
                d="M1620 112 H1425 V85 H1350"
            />

            <path
                d="M1575 125 H1410 V104 H1330"
            />

            <path
                d="M1500 95 H1390 V65 H1335"
            />

            <path
                d="M1465 130 V70 H1390"
            />

        </g>


        <!-- RIGHT VESSEL -->

        <g>

            <rect
                class="steel"
                x="1350"
                y="64"
                width="58"
                height="76"
                rx="26"
            />

            <path
                class="light"
                d="
                    M1350 82 H1408
                    M1350 107 H1408
                "
            />

            <circle
                class="window"
                cx="1379"
                cy="95"
                r="4"
            />

        </g>


        <!-- CENTRAL LOW PIPE -->

        <g class="light">

            <path
                d="M0 137 H1672"
            />

            <path
                d="M0 126 H420 V116 H650"
            />

            <path
                d="M1672 126 H1250 V116 H1020"
            />

        </g>


        <!-- HEXAGONAL TECHNICAL MOTIFS -->

        <g class="hex">

            <path
                d="M250 25 l18 -11 l18 11 v22 l-18 11 l-18-11 z"
            />

            <path
                d="M282 54 l18 -11 l18 11 v22 l-18 11 l-18-11 z"
            />

            <path
                d="M1335 25 l18 -11 l18 11 v22 l-18 11 l-18-11 z"
            />

            <path
                d="M1370 54 l18 -11 l18 11 v22 l-18 11 l-18-11 z"
            />

        </g>


    </svg>


    <!-- =================================================
         HEADER CONTENT
         ================================================= -->

    <div class="content">

        <div class="title">
            PSM DASHBOARD
        </div>


        <div class="pillar">
    {pillar_name}
</div>


        <div class="subtitle">
            PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL
        </div>

    </div>


    <div class="scan"></div>

</div>

</body>

</html>
"""


    # =====================================================
    # IMPORTANT:
    # SAME METHOD USED IN PT PAGE
    # =====================================================

    components.html(
        header_html,
        height=170,
        scrolling=False
    )


# ============================================================
# COMMON SECTION HEADER
# ============================================================

def psm_section(title):

    st.markdown(
        f"""
        <div class="psm-section">
            {escape(str(title))}
        </div>
        """,
        unsafe_allow_html=True
    )