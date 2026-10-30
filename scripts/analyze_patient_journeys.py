
import pandas as pd
from pathlib import Path

# Locate project files
project_dir = Path(__file__).resolve().parent.parent
input_file = project_dir / "data" / "standardized_event_logs.csv"
output_dir = project_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Load event logs
df = pd.read_csv(input_file)

required_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

if df[required_columns].isnull().any().any():
    raise ValueError("Missing values found in required event-log columns.")

# Prepare and order patient events
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")
df = df.sort_values(["Case_ID", "Timestamp"]).copy()

# Build each patient's chronological activity sequence
journeys = (
    df.groupby("Case_ID")
    .agg(
        Activity_Sequence=(
            "Activity_Name",
            lambda activities: " -> ".join(activities.astype(str))
        ),
        First_Activity=("Activity_Name", "first"),
        Last_Activity=("Activity_Name", "last"),
        Total_Activities=("Activity_Name", "size"),
        Journey_Start=("Timestamp", "min"),
        Journey_End=("Timestamp", "max"),
    )
    .reset_index()
)

# Calculate journey duration in minutes
journeys["Journey_Duration_Minutes"] = (
    journeys["Journey_End"] - journeys["Journey_Start"]
).dt.total_seconds() / 60

# Summarize the most common complete activity sequences
sequence_summary = (
    journeys.groupby("Activity_Sequence")
    .agg(
        Patient_Count=("Case_ID", "nunique"),
        Average_Activities=("Total_Activities", "mean"),
        Average_Duration_Minutes=("Journey_Duration_Minutes", "mean"),
    )
    .reset_index()
    .sort_values(
        ["Patient_Count", "Average_Duration_Minutes"],
        ascending=[False, False],
    )
)

# Save detailed patient journeys and sequence summary
journey_file = output_dir / "patient_journey_sequences.csv"
summary_file = output_dir / "common_patient_journey_summary.csv"

journeys.to_csv(journey_file, index=False)
sequence_summary.to_csv(summary_file, index=False)

print("Patient journey analysis completed successfully!")
print(f"Patient cases analyzed: {journeys['Case_ID'].nunique()}")
print(f"Unique activity sequences: {len(sequence_summary)}")
print("\nTop 10 most common patient journeys:")
print(sequence_summary.head(10).to_string(index=False))
print(f"\nDetailed journeys saved to: {journey_file}")
print(f"Sequence summary saved to: {summary_file}")
