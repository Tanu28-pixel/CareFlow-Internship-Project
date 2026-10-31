"""
CareFlow: Clinical Pathway Rules
Defines and exports expected pathway rules.
"""

import csv
from pathlib import Path

EXPECTED_PATHWAY = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "Treatment",
    "Discharge"
]

OPTIONAL_ACTIVITIES = [
    "X-Ray",
    "Lab Test"
]


def create_pathway_rules():

    output_dir = Path(__file__).resolve().parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "clinical_pathway_rules.csv"

    rows = []

    for order, activity in enumerate(EXPECTED_PATHWAY, start=1):
        rows.append({
            "Activity_Name": activity,
            "Activity_Type": "Required",
            "Sequence_Order": order
        })

    for activity in OPTIONAL_ACTIVITIES:
        rows.append({
            "Activity_Name": activity,
            "Activity_Type": "Optional",
            "Sequence_Order": "Between Consultation and Treatment"
        })

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Activity_Name",
                "Activity_Type",
                "Sequence_Order"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Clinical pathway rules saved successfully!")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    create_pathway_rules()