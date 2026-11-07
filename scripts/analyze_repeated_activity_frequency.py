
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "standardized_event_logs.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "repeated_activity_frequency.csv"

df = pd.read_csv(INPUT_FILE)

# Count each activity for every patient
activity_counts = (
    df.groupby(["Case_ID", "Activity_Name"])
    .size()
    .reset_index(name="Activity_Count")
)

# Keep only activities performed more than once
repeated = activity_counts[
    activity_counts["Activity_Count"] > 1
].copy()

# Summarize repeated activity patterns
summary = (
    repeated.groupby("Activity_Name")
    .agg(
        Patients_With_Repetition=("Case_ID", "nunique"),
        Total_Activity_Instances=("Activity_Count", "sum")
    )
    .reset_index()
)

summary["Extra_Activity_Instances"] = (
    summary["Total_Activity_Instances"]
    - summary["Patients_With_Repetition"]
)

summary = summary.sort_values(
    "Extra_Activity_Instances",
    ascending=False
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

print("Repeated activity frequency analysis completed!")
print("\nActivity frequency summary:")
print(summary.to_string(index=False))
print("\nSaved to:", OUTPUT_FILE)
