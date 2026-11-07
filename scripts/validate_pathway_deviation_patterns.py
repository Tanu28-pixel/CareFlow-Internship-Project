
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_summary.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_patterns.csv"

source = pd.read_csv(INPUT_FILE, keep_default_na=False)
results = pd.read_csv(OUTPUT_FILE)

expected = (
    source.groupby("Deviation_Status")
    .size()
    .reset_index(name="Patient_Count")
)

expected["Deviation_Pattern"] = expected["Deviation_Status"].map({
    "No Repeated Activity": "No Repeated Activity",
    "Repeated Activity Detected": "Repeated Triage and Consultation"
})

expected["Average_Repeated_Activity_Types"] = (
    source.groupby("Deviation_Status")["Repeated_Activity_Types"]
    .mean().values
)

expected["Patient_Percentage"] = (
    expected["Patient_Count"] / len(source) * 100
).round(2)

expected = expected[
    ["Deviation_Pattern", "Patient_Count",
     "Average_Repeated_Activity_Types", "Patient_Percentage"]
].sort_values("Deviation_Pattern").reset_index(drop=True)

results = results.sort_values(
    "Deviation_Pattern"
).reset_index(drop=True)

checks = [
    ("Output is not empty", not results.empty),
    ("No missing values", not results.isnull().any().any()),
    ("Patient count totals 200", results["Patient_Count"].sum() == 200),
    ("Percentages total 100",
     round(results["Patient_Percentage"].sum(), 2) == 100.00),
    ("Pattern counts match source data",
     results.equals(expected))
]

print("\nPATHWAY DEVIATION PATTERN VALIDATION")
print("-" * 45)

for name, passed in checks:
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

print("-" * 45)
print(f"Passed: {sum(value for _, value in checks)}/{len(checks)}")

if not all(value for _, value in checks):
    raise SystemExit("Validation failed!")

print("\nAll validation checks passed!")
