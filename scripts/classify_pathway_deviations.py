
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_summary.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_patterns.csv"

df = pd.read_csv(INPUT_FILE, keep_default_na=False)

def classify_pattern(activities):
    if activities == "None":
        return "No Repeated Activity"

    activity_set = set(activities.split(", "))

    if activity_set == {"Triage"}:
        return "Repeated Triage"

    if activity_set == {"Doctor Consultation"}:
        return "Repeated Doctor Consultation"

    if activity_set == {"Triage", "Doctor Consultation"}:
        return "Repeated Triage and Consultation"

    return "Other Repeated Activities"

df["Deviation_Pattern"] = df["Repeated_Activities"].apply(
    classify_pattern
)

summary = (
    df.groupby("Deviation_Pattern")
    .agg(
        Patient_Count=("Case_ID", "count"),
        Average_Repeated_Activity_Types=(
            "Repeated_Activity_Types", "mean"
        )
    )
    .reset_index()
)

summary["Patient_Percentage"] = (
    summary["Patient_Count"] / len(df) * 100
).round(2)

summary = summary.sort_values(
    "Patient_Count", ascending=False
)

summary.to_csv(OUTPUT_FILE, index=False)

print("Pathway deviation pattern classification completed!")
print("\nPattern summary:")
print(summary.to_string(index=False))
print("\nSaved to:", OUTPUT_FILE)
