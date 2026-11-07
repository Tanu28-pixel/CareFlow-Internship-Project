
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "standardized_event_logs.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_summary.csv"

events = pd.read_csv(INPUT_FILE)
results = pd.read_csv(OUTPUT_FILE, keep_default_na=False)

checks = []

checks.append(("All 200 patients included", len(results) == 200))
checks.append(("No duplicate patient IDs", results["Case_ID"].is_unique))
checks.append(("No missing values", not results.isnull().any().any()))
checks.append(("No negative repeat counts",
               (results["Total_Repeated_Events"] >= 0).all()))

expected_repeated = (
    events.groupby(["Case_ID", "Activity_Name"])
    .size()
    .reset_index(name="count")
)

expected_repeated = expected_repeated[
    expected_repeated["count"] > 1
]

expected_patients = expected_repeated["Case_ID"].nunique()

actual_patients = (
    results["Repeated_Activity_Types"] > 0
).sum()

checks.append((
    "Repeated patient count matches event logs",
    expected_patients == actual_patients
))

print("\nPATHWAY DEVIATION VALIDATION")
print("-" * 45)

for name, passed in checks:
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

print("-" * 45)
print(f"Total checks: {len(checks)}")
print(f"Passed: {sum(value for _, value in checks)}")
print(f"Failed: {sum(not value for _, value in checks)}")

if not all(value for _, value in checks):
    raise SystemExit("Validation failed!")

print("\nAll validation checks passed!")