"""
CareFlow: Enhanced Patient Pathway Conformance Checking
"""

import pandas as pd
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent

JOURNEY_FILE = BASE_DIR / "outputs" / "patient_journey_sequences.csv"
RULES_FILE = BASE_DIR / "outputs" / "clinical_pathway_rules.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "conformance_results.csv"


def check_conformance():

    journeys = pd.read_csv(JOURNEY_FILE)
    rules = pd.read_csv(RULES_FILE)

    required = rules.loc[
        rules["Activity_Type"] == "Required",
        "Activity_Name"
    ].tolist()

    optional = rules.loc[
        rules["Activity_Type"] == "Optional",
        "Activity_Name"
    ].tolist()

    results = []

    for _, patient in journeys.iterrows():

        activities = [
            activity.strip()
            for activity in patient["Activity_Sequence"].split("->")
        ]

        missing = [a for a in required if a not in activities]

        positions = [
            activities.index(a)
            for a in required if a in activities
        ]

        correct_order = positions == sorted(positions)

        counts = Counter(activities)

        repeated = [
            a for a, count in counts.items() if count > 1
        ]

        unexpected = [
            a for a in activities
            if a not in required and a not in optional
        ]

        optional_positions_valid = all(
            activities.index(a) > activities.index("Doctor Consultation")
            and activities.index(a) < activities.index("Treatment")
            for a in optional if a in activities
        )

        conforming = (
            not missing
            and correct_order
            and not repeated
            and not unexpected
            and optional_positions_valid
        )

        results.append({
            "Case_ID": patient["Case_ID"],
            "Conformance_Status": (
                "Conforming" if conforming else "Non-Conforming"
            ),
           "Missing_Activities": ", ".join(missing) if missing else "No deviation",
"Repeated_Activities": ", ".join(repeated) if repeated else "No deviation",
"Unexpected_Activities": ", ".join(unexpected) if unexpected else "No deviation",
"Optional_Activities_Position_Valid": optional_positions_valid,
        })

    result_df = pd.DataFrame(results)

    result_df.to_csv(OUTPUT_FILE, index=False)

    print("ENHANCED PATIENT PATHWAY CONFORMANCE")
    print("------------------------------------")
    print(f"Patients analyzed: {len(result_df)}")
    print("\nConformance summary:")
    print(result_df["Conformance_Status"].value_counts())
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    check_conformance()