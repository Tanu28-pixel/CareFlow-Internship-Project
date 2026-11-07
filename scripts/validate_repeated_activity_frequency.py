
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "standardized_event_logs.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "repeated_activity_frequency.csv"

events = pd.read_csv(INPUT_FILE)
results = pd.read_csv(OUTPUT_FILE)

# Independently calculate expected repeated activity counts
counts = (
    events.groupby(["Case_ID", "Activity_Name"])
    .size()
    .reset_index(name="Activity_Count")
)

repeated = counts[counts["Activity_Count"] > 1]

expected = (
    repeated.groupby("Activity_Name")
    .agg(
        Patients_With_Repetition=("Case_ID", "nunique"),
        Total_Activity_Instances=("Activity_Count", "sum")
    )
    .reset_index()
)

expected["Extra_Activity_Instances"] = (
    expected["Total_Activity_Instances"]
    - expected["Patients_With_Repetition"]
)

expected = expected.sort_values("Activity_Name").reset_index(drop=True)
results = results.sort_values("Activity_Name").reset_index(drop=True)

checks = [
    ("Output is not empty", not results.empty),
    ("No duplicate activity names", results["Activity_Name"].is_unique),
    ("No missing values", not results.isnull().any().any()),
    ("Activity counts match source data",
     results.equals(expected))
]

print("\nREPEATED ACTIVITY FREQUENCY VALIDATION")
print("-" * 45)

for name, passed in checks:
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

print("-" * 45)
print(f"Passed: {sum(value for _, value in checks)}/{len(checks)}")

if not all(value for _, value in checks):
    raise SystemExit("Validation failed!")

print("\nAll validation checks passed!")
