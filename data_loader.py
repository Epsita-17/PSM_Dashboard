from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data" / "departments"


def clean(value):
    """Convert blank Excel cells to 0."""
    return 0 if pd.isna(value) else value


def load_department_data(department):
    file_path = DATA_DIR / f"{department}.xlsx"

    if not file_path.exists():
        return None

    return pd.read_excel(
        file_path,
        sheet_name="PSM Dashboard",
        header=None
    )


def get_department_data(df):

    return {

        # PROCESS SAFETY INCIDENTS
        "incidents": {
            "monthly": {
                "level_1": clean(df.iloc[5, 1]),
                "level_2": clean(df.iloc[5, 2]),
                "level_3": clean(df.iloc[5, 3]),
                "level_4": clean(df.iloc[5, 4]),
                "investigation_pending_30": clean(df.iloc[5, 5]),
                "soc": clean(df.iloc[5, 6]),
                "sol": clean(df.iloc[5, 7]),
            },
            "ytd": {
                "level_1": clean(df.iloc[6, 1]),
                "level_2": clean(df.iloc[6, 2]),
                "level_3": clean(df.iloc[6, 3]),
                "level_4": clean(df.iloc[6, 4]),
                "investigation_pending_30": clean(df.iloc[6, 5]),
                "soc": clean(df.iloc[6, 6]),
                "sol": clean(df.iloc[6, 7]),
            }
        },

        # PSM CRITICAL EQUIPMENT
        "equipment": {
            "monthly": {
                "failure": clean(df.iloc[5, 8]),
                "mechanical_generated": clean(df.iloc[5, 9]),
                "mechanical_completed": clean(df.iloc[5, 10]),
                "iem_generated": clean(df.iloc[5, 11]),
                "iem_completed": clean(df.iloc[5, 12]),
                "z01_open": clean(df.iloc[5, 13]),
                "z01_closed": clean(df.iloc[5, 14]),
                "iem_open": clean(df.iloc[5, 15]),
                "iem_closed": clean(df.iloc[5, 16]),
            },
            "ytd": {
                "failure": clean(df.iloc[6, 8]),
                "mechanical_generated": clean(df.iloc[6, 9]),
                "mechanical_completed": clean(df.iloc[6, 10]),
                "iem_generated": clean(df.iloc[6, 11]),
                "iem_completed": clean(df.iloc[6, 12]),
                "z01_open": clean(df.iloc[6, 13]),
                "z01_closed": clean(df.iloc[6, 14]),
                "iem_open": clean(df.iloc[6, 15]),
                "iem_closed": clean(df.iloc[6, 16]),
            }
        },

        # BARRIER MANAGEMENT
        "barriers": {
            "monthly": {
                "audit_plan": clean(df.iloc[5, 17]),
                "audit_actual": clean(df.iloc[5, 18]),
                "total": clean(df.iloc[5, 19]),
                "assessed": clean(df.iloc[5, 20]),
                "unacceptable": clean(df.iloc[5, 21]),
            },
            "ytd": {
                "audit_plan": clean(df.iloc[6, 17]),
                "audit_actual": clean(df.iloc[6, 18]),
                "total": clean(df.iloc[6, 19]),
                "assessed": clean(df.iloc[6, 20]),
                "unacceptable": clean(df.iloc[6, 21]),
            }
        },

        # TABLE TOP EXERCISE
        "table_top": {
            "monthly": {
                "planned": clean(df.iloc[5, 22]),
                "actual": clean(df.iloc[5, 23]),
            },
            "ytd": {
                "planned": clean(df.iloc[6, 22]),
                "actual": clean(df.iloc[6, 23]),
            }
        },

        # RECOMMENDATIONS
        "recommendations": {
            "monthly": {
                "third_party_close": clean(df.iloc[10, 1]),
                "third_party_delayed": clean(df.iloc[10, 2]),
                "incident_close": clean(df.iloc[10, 3]),
                "incident_delayed": clean(df.iloc[10, 4]),
                "rcfa_overdue": clean(df.iloc[10, 5]),
                "pt_plan": clean(df.iloc[10, 6]),
                "pt_actual": clean(df.iloc[10, 7]),
                "pha_plan": clean(df.iloc[10, 8]),
                "pha_actual": clean(df.iloc[10, 9]),
                "pha_close": clean(df.iloc[10, 10]),
                "pha_delayed": clean(df.iloc[10, 11]),
                "audit_close": clean(df.iloc[10, 12]),
                "audit_delayed": clean(df.iloc[10, 13]),
            },
            "ytd": {
                "third_party_close": clean(df.iloc[11, 1]),
                "third_party_delayed": clean(df.iloc[11, 2]),
                "incident_close": clean(df.iloc[11, 3]),
                "incident_delayed": clean(df.iloc[11, 4]),
                "rcfa_overdue": clean(df.iloc[11, 5]),
                "pt_plan": clean(df.iloc[11, 6]),
                "pt_actual": clean(df.iloc[11, 7]),
                "pha_plan": clean(df.iloc[11, 8]),
                "pha_actual": clean(df.iloc[11, 9]),
                "pha_close": clean(df.iloc[11, 10]),
                "pha_delayed": clean(df.iloc[11, 11]),
                "audit_close": clean(df.iloc[11, 12]),
                "audit_delayed": clean(df.iloc[11, 13]),
            }
        },

        # MOC
        "moc": {
            "monthly": {
                "pending_15_days": clean(df.iloc[10, 14]),
                "kaizen_generated": clean(df.iloc[10, 16]),
                "emergency_temporary": clean(df.iloc[10, 18]),
                "temporary_overdue": clean(df.iloc[10, 20]),
            },
            "ytd": {
                "pending_15_days": clean(df.iloc[11, 14]),
                "kaizen_generated": clean(df.iloc[11, 16]),
                "emergency_temporary": clean(df.iloc[11, 18]),
                "temporary_overdue": clean(df.iloc[11, 20]),
            }
        },

        # INTERLOCK BYPASS
        "interlock": {
            "monthly": {
                "open": clean(df.iloc[10, 22]),
                "normalisation_overdue": clean(df.iloc[10, 23]),
            },
            "ytd": {
                "open": clean(df.iloc[11, 22]),
                "normalisation_overdue": clean(df.iloc[11, 23]),
            }
        }
    }


if __name__ == "__main__":

    df = load_department_data("DRI")

    if df is None:
        print("DRI Excel file not found.")

    else:
        data = get_department_data(df)

        print("DRI Excel loaded successfully.")
        print("Monthly incidents:", data["incidents"]["monthly"])
        print("Monthly equipment:", data["equipment"]["monthly"])
        print("Monthly barriers:", data["barriers"]["monthly"])
        print("Monthly MOC:", data["moc"]["monthly"])
        print("Monthly interlock:", data["interlock"]["monthly"])