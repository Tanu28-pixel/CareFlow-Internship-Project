
import pandas as pd
from pathlib import Path

# Locate project files
project_dir = Path(__file__).resolve().parent.parent
journey_file = project_dir / "outputs" / "patient_journey_sequences.csv"
summary_file = project_dir / "outputs" / "common_patient_journey_summary.csv"

# Check required files exist
for file_path in [journey_file, summary_file]:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

# Load outputs
journeys = pd.read_csv(journey_file)
summary = pd.read_csv(summary_file)

if journeys.empty:
    raise ValueError("Patient journey file is empty.")

if summary.empty:
    raise ValueError("Patient journey summary is empty.")

# Validate detailed journey columns
journey_columns = [
    "Case_ID",
    "Activity_Sequence",
    "First_Activity",
    "Last_Activity",
    "Total_Activities",
    "Journey_Start",
    "Journey_End",
    "Journey_Duration_Minutes",
]

missing_journey_columns = [
    col for col in journey_columns if col not in journeys.columns
]
if missing_journey_columns:
    raise ValueError(
        f"Missing journey columns: {missing_journey_columns}"
    )

# Validate summary columns
summary_columns = [
    "Activity_Sequence",
    "Patient_Count",
    "Average_Activities",
    "Average_Duration_Minutes",
]

missing_summary_columns = [
    col for col in summary_columns if col not in summary.columns
]
if missing_summary_columns:
    raise ValueError(
        f"Missing summary columns: {missing_summary_columns}"
    )

# Check required values
if journeys[journey_columns].isnull().any().any():
    raise ValueError("Missing values found in patient journeys.")

if summary[summary_columns].isnull().any().any():
    raise ValueError("Missing values found in journey summary.")

# Each patient should have exactly one detailed journey
if journeys["Case_ID"].duplicated().any():
    raise ValueError("Duplicate patient cases found.")

# Journey durations and activity counts must be valid
if (journeys["Total_Activities"] <= 0).any():
    raise ValueError("Invalid activity count found.")

if (journeys["Journey_Duration_Minutes"] < 0).any():
    raise ValueError("Negative journey duration found.")

if (summary["Patient_Count"] <= 0).any():
    raise ValueError("Summary patient counts must be positive.")

if summary["Activity_Sequence"].duplicated().any():
    raise ValueError("Duplicate journey sequences found in summary.")

# Check the summary accounts for every patient
if int(summary["Patient_Count"].sum()) != len(journeys):
    raise ValueError(
        "Summary patient counts do not match detailed journeys."
    )

# Independently verify summary counts
expected_counts = (
    journeys.groupby("Activity_Sequence")["Case_ID"]
    .nunique()
    .rename("Expected_Count")
)

comparison = summary.set_index("Activity_Sequence").join(
    expected_counts, how="outer"
)

if comparison.isnull().any().any():
    raise ValueError("Journey sequences differ between output files.")

if not (
    comparison["Patient_Count"].astype(int)
    == comparison["Expected_Count"].astype(int)
).all():
    raise ValueError("Journey summary counts do not match source journeys.")

print("Patient journey validation passed!")
print(f"Unique patient cases: {journeys['Case_ID'].nunique()}")
print(f"Distinct journey patterns: {len(summary)}")
print(f"Patients represented in summary: {int(summary['Patient_Count'].sum())}")
print("Required columns: present")
print("Missing values: none")
print("Patient cases: unique")
print("Journey summary counts: match detailed journeys")
