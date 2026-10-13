import io
import re
import smtplib
import requests
import pandas as pd

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from html import escape
from pathlib import Path

import tomllib


# ============================================================
# GOOGLE SHEET CONFIGURATION
# Same configuration as your existing PSM Dashboard
# ============================================================

SPREADSHEET_ID = "1--X0TT5Ts92EKAxrhV-fQgqeTHBX3rDVc1Egg74MewM"

SHEETS = {
    "MOC": "1493447251",
    "PSSR": "1914804736",
    "Interlock": "1595602222",
    "PSM CE": "1552637895",
}


# ============================================================
# DEPARTMENTS
# Same department list as your dashboard
# ============================================================

ALL_DEPARTMENTS = [
    "Blast Furnace",
    "Coke Oven",
    "SMS-1",
    "SMS-2",
    "DRI",
    "Central Utility",
    "CRM",
    "WRM",
    "CPP",
    "Sinter",
    "Tube Mill",
    "CSP",
    "Pellet & Beneficiation",
    "LCP",
]


# ============================================================
# BASIC DATA FUNCTIONS
# ============================================================

def clean_dataframe(df):

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    df.columns = [
        str(c).strip().replace("\n", " ").replace("\r", " ")
        for c in df.columns
    ]

    df = df.dropna(how="all").copy()

    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()

    return df


def norm(value):

    return re.sub(
        r"[^a-z0-9]+",
        "",
        str(value).strip().lower()
    )


def find_col(df, candidates):

    if df is None or df.empty:
        return None

    normalized = {
        norm(col): col
        for col in df.columns
    }

    for candidate in candidates:

        key = norm(candidate)

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# DEPARTMENT FILTER
# Same basic department matching used by dashboard
# ============================================================

def filter_department(df, department):

    df = clean_dataframe(df)

    if df.empty:
        return df

    department_col = find_col(
        df,
        [
            "Department",
            "Departments",
            "Dept",
            "Department Name",
            "Department_Name",
            "Dept Name",
            "Dept_Name",
        ]
    )

    if department_col is None:
        return pd.DataFrame(columns=df.columns)

    values = (
        df[department_col]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    selected = norm(department)

    # Special department handling
    if selected == "blastfurnace":

        mask = values.str.contains(
            r"blast\s*[-_/ ]*\s*furnace",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "cokeoven":

        mask = values.str.contains(
            r"coke\s*[-_/ ]*\s*oven",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "sms1":

        mask = values.str.contains(
            r"sms\s*[-_/ ]*1",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "sms2":

        mask = values.str.contains(
            r"sms\s*[-_/ ]*2",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "centralutility":

        mask = values.str.contains(
            r"central\s*[-_/ ]*\s*utility",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "tubemill":

        mask = values.str.contains(
            r"tube\s*[-_/ ]*\s*mill",
            case=False,
            regex=True,
            na=False,
        )

    elif selected == "pelletbeneficiation":

        mask = values.str.contains(
            r"pellet.*beneficiation|beneficiation.*pellet",
            case=False,
            regex=True,
            na=False,
        )

    else:

        mask = values.map(norm) == selected

    return df.loc[mask].copy()


# ============================================================
# GOOGLE SHEET LOADER
# ============================================================

def load_google_sheet(gid):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/export"
        f"?format=csv&gid={gid}"
    )

    response = requests.get(
        url,
        timeout=60,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    response.raise_for_status()

    df = pd.read_csv(
        io.StringIO(
            response.content.decode("utf-8-sig")
        )
    )

    return clean_dataframe(df)


# ============================================================
# STATUS COUNTING
# ============================================================

def status_counts(df, status_candidates):

    result = {
        "pending": 0,
        "open": 0,
        "completed": 0,
        "closed": 0,
    }

    if df is None or df.empty:
        return result

    status_col = find_col(
        df,
        status_candidates
    )

    if status_col is None:
        return result

    s = (
        df[status_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    result["completed"] = int(
        s.str.contains(
            r"\bcompleted?\b|\bcomplete\b",
            regex=True,
            na=False
        ).sum()
    )

    result["pending"] = int(
        s.str.contains(
            r"\bpending\b",
            regex=True,
            na=False
        ).sum()
    )

    result["open"] = int(
        s.str.fullmatch(
            r"open",
            case=False,
            na=False
        ).sum()
    )

    result["closed"] = int(
        s.str.fullmatch(
            r"closed",
            case=False,
            na=False
        ).sum()
    )

    return result


# ============================================================
# PSM CE STATUS
# Generated - Completed = Pending
# ============================================================

def psm_ce_counts(df):

    result = {
        "pending": 0,
        "open": 0,
        "completed": 0,
        "closed": 0,
    }

    if df is None or df.empty:
        return result

    generated_cols = [
        find_col(
            df,
            [
                "Compliance of PSM CE MO – Mechanical – Generated",
                "Compliance of PSM CE MO - Mechanical - Generated",
                "PSM CE MO Mechanical Generated",
            ]
        ),

        find_col(
            df,
            [
                "Compliance of PSM CE MO – E&I – Generated",
                "Compliance of PSM CE MO - E&I - Generated",
                "PSM CE MO E&I Generated",
            ]
        ),
    ]

    completed_cols = [
        find_col(
            df,
            [
                "Compliance of PSM CE MO – Mechanical – Completed",
                "Compliance of PSM CE MO - Mechanical - Completed",
                "PSM CE MO Mechanical Completed",
            ]
        ),

        find_col(
            df,
            [
                "Compliance of PSM CE MO – E&I – Completed",
                "Compliance of PSM CE MO - E&I - Completed",
                "PSM CE MO E&I Completed",
            ]
        ),
    ]

    generated = 0
    completed = 0

    for col in generated_cols:

        if col:
            generated += int(
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            )

    for col in completed_cols:

        if col:
            completed += int(
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            )

    completed = max(
        0,
        min(completed, generated)
    )

    result["pending"] = generated - completed
    result["completed"] = completed

    return result


# ============================================================
# BUILD EMAIL DATA
# ============================================================

def build_email_data():

    print("Reading Google Sheet data...")

    moc = load_google_sheet(
        SHEETS["MOC"]
    )

    pssr = load_google_sheet(
        SHEETS["PSSR"]
    )

    interlock = load_google_sheet(
        SHEETS["Interlock"]
    )

    psm_ce = load_google_sheet(
        SHEETS["PSM CE"]
    )

    print("MOC records:", len(moc))
    print("PSSR records:", len(pssr))
    print("Interlock records:", len(interlock))
    print("PSM CE records:", len(psm_ce))

    modules = {
        "MOC": (
            moc,
            [
                "Status (Open/Close)",
                "Status (Open / Close)",
                "Status",
                "Current Status",
                "MOC Status",
                "Action Status",
            ]
        ),

        "PSSR": (
            pssr,
            [
                "Status",
                "Current Status",
                "PSSR Status",
                "Action Status",
                "Completion Status",
            ]
        ),

        "Interlock": (
            interlock,
            [
                "Present Status / Action Required",
                "Present Status",
                "Status / Action Required",
                "Action Status",
                "Status",
            ]
        ),

        "PSM CE": (
            psm_ce,
            []
        ),
    }

    rows = []

    for department in ALL_DEPARTMENTS:

        for module, data in modules.items():

            df = data[0]
            candidates = data[1]

            if df.empty:
                continue

            dept_df = filter_department(
                df,
                department
            )

            if dept_df.empty:
                continue

            if module == "PSM CE":

                counts = psm_ce_counts(
                    dept_df
                )

            else:

                counts = status_counts(
                    dept_df,
                    candidates
                )

            total = (
                counts["pending"]
                + counts["open"]
                + counts["completed"]
                + counts["closed"]
            )

            if total <= 0:
                continue

            rows.append(
                {
                    "Department": department,
                    "Module": module,
                    "Pending": counts["pending"],
                    "Open": counts["open"],
                    "Completed": counts["completed"],
                    "Closed": counts["closed"],
                    "Total": total,
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "Department",
            "Module",
            "Pending",
            "Open",
            "Completed",
            "Closed",
            "Total",
        ]
    )


# ============================================================
# EMAIL HTML
# ============================================================

def build_email_html(df):

    from datetime import datetime
    from zoneinfo import ZoneInfo

    generated = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%d-%b-%Y %H:%M:%S"
    )

    if df.empty:

        table_html = """
        <p>
        No critical status records were identified.
        </p>
        """

    else:

        table_html = df.to_html(
            index=False,
            border=0,
            classes="status-table",
            justify="center"
        )

    html = f"""
    <html>

    <head>

    <style>

    body {{
        font-family: Arial, sans-serif;
        background: #f4f6f8;
        padding: 20px;
        color: #222;
    }}

    .container {{
        background: white;
        padding: 20px;
        border-radius: 8px;
    }}

    h2 {{
        color: #173f70;
        margin-bottom: 5px;
    }}

    .generated {{
        color: #666;
        margin-bottom: 18px;
    }}

    table.status-table {{
        border-collapse: collapse;
        width: 100%;
        font-size: 13px;
    }}

    table.status-table th {{
        background: #173f70;
        color: white;
        padding: 8px;
        border: 1px solid #ccc;
        text-align: center;
    }}

    table.status-table td {{
        padding: 7px;
        border: 1px solid #ccc;
        text-align: center;
    }}

    table.status-table tr:nth-child(even) {{
        background: #f5f7fa;
    }}

    .footer {{
        margin-top: 18px;
        font-size: 12px;
        color: #666;
    }}

    </style>

    </head>

    <body>

    <div class="container">

        <h2>
            PSM Critical Status — Module Wise
        </h2>

        <div class="generated">
            Department-wise critical status |
            Generated: {escape(generated)}
        </div>

        {table_html}

        <div class="footer">
            Status columns:
            Pending, Open, Completed, Closed and Total.
            <br><br>
            PSM CE Pending = Generated − Completed.
        </div>

    </div>

    </body>

    </html>
    """

    return html


# ============================================================
# READ EMAIL SETTINGS
# ============================================================

def load_email_settings():

    script_dir = Path(__file__).resolve().parent

    secrets_file = (
        script_dir
        / ".streamlit"
        / "secrets.toml"
    )

    if not secrets_file.exists():

        raise FileNotFoundError(
            f"secrets.toml not found:\n{secrets_file}"
        )

    with open(
        secrets_file,
        "rb"
    ) as f:

        secrets = tomllib.load(f)

    if "email" not in secrets:

        raise ValueError(
            "[email] section not found in secrets.toml"
        )

    return secrets["email"]


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(df):

    cfg = load_email_settings()

    smtp_server = str(
        cfg.get(
            "smtp_server",
            "smtp.office365.com"
        )
    )

    smtp_port = int(
        cfg.get(
            "smtp_port",
            587
        )
    )

    sender = str(
        cfg.get(
            "sender_email",
            ""
        )
    ).strip()

    password = str(
        cfg.get(
            "sender_password",
            ""
        )
    )

    recipients = str(
        cfg.get(
            "recipient_emails",
            ""
        )
    )

    recipient_list = [
        x.strip()
        for x in recipients.split(",")
        if x.strip()
    ]

    if not sender:

        raise ValueError(
            "sender_email is missing."
        )

    if not password:

        raise ValueError(
            "sender_password is missing."
        )

    if not recipient_list:

        raise ValueError(
            "recipient_emails is missing."
        )

    from datetime import datetime
    from zoneinfo import ZoneInfo

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%d-%b-%Y"
    )

    msg = MIMEMultipart(
        "alternative"
    )

    msg["Subject"] = (
        "PSM Critical Status – "
        "Department & Module Wise – "
        + today
    )

    msg["From"] = sender

    msg["To"] = ", ".join(
        recipient_list
    )

    html = build_email_html(
        df
    )

    msg.attach(
        MIMEText(
            html,
            "html",
            "utf-8"
        )
    )

    print("Connecting to email server...")

    with smtplib.SMTP(
        smtp_server,
        smtp_port,
        timeout=30
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.sendmail(
            sender,
            recipient_list,
            msg.as_string()
        )

    print(
        "Email sent successfully to:"
    )

    for recipient in recipient_list:
        print(
            "  ",
            recipient
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "PSM WEEKLY CRITICAL STATUS EMAIL"
    )

    print(
        "Monday 09:00 AM automatic email"
    )

    print("=" * 60)

    try:

        email_df = build_email_data()

        print(
            "\nRows prepared for email:",
            len(email_df)
        )

        if not email_df.empty:

            print("\nEmail data:")
            print(
                email_df.to_string(
                    index=False
                )
            )

        send_email(
            email_df
        )

        print(
            "\nSUCCESS: PSM email sent."
        )

    except Exception as exc:

        print(
            "\nERROR:"
        )

        print(
            str(exc)
        )

        raise