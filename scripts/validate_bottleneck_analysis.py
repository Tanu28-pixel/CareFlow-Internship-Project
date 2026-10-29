
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
event_file = project_dir / "data" / "standardized_event_logs.csv"
analysis_file = project_dir / "outputs" / "bottleneck_analysis.csv"

required_columns = [
    "Activity_Name",
    "Next_Activity",
    "Transition_Count",
    "Average_Wait_Minutes",
    "Median_Wait_Minutes",
    "Maximum_Wait_Minutes",
]

# Check that required files exist
for file_path in [event_file, analysis_file]:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

# Load source event log and bottleneck summary
# Load source event log and bottleneck summary
events = pd.read_csv(event_file)
summary = pd.read_csv(analysis_file)

# Convert source timestamps from text to datetime
events["Timestamp"] = pd.to_datetime(
    events["Timestamp"], errors="raise"
)

if events.empty:
    raise ValueError("Source event log is empty.")

if summary.empty:
    raise ValueError("Bottleneck analysis file is empty.")

# Validate source columns
source_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing_source = [
    col for col in source_columns if col not in events.columns
]
if missing_source:
    raise ValueError(f"Missing source columns: {missing_source}")

# Validate summary columns
missing_columns = [
    col for col in required_columns if col not in summary.columns
]
if missing_columns:
    raise ValueError(f"Missing summary columns: {missing_columns}")

# Check missing values
if events[source_columns].isnull().any().any():
    raise ValueError("Missing values found in source event log.")

if summary[required_columns].isnull().any().any():
    raise ValueError("Missing values found in bottleneck summary.")


# Prepare source events and derive every consecutive transition
events["Next_Activity"] = (
    events.groupby("Case_ID")["Activity_Name"].shift(-1)
)
events["Next_Timestamp"] = (
    events.groupby("Case_ID")["Timestamp"].shift(-1)
)

events["Waiting_Minutes"] = (
    events["Next_Timestamp"] - events["Timestamp"]
).dt.total_seconds() / 60

transitions = events.dropna(
    subset=["Next_Activity", "Waiting_Minutes"]
).copy()

if transitions.empty:
    raise ValueError("No consecutive activity transitions found.")

# Validate source waiting times
if (transitions["Waiting_Minutes"] < 0).any():
    raise ValueError("Negative waiting times found in source events.")


if (events["Waiting_Minutes"].dropna() < 0).any():
    raise ValueError("Negative waiting times found in source events.")

# Validate summary values
if (summary["Transition_Count"] <= 0).any():
    raise ValueError("Transition counts must be positive.")

time_columns = [
    "Average_Wait_Minutes",
    "Median_Wait_Minutes",
    "Maximum_Wait_Minutes",
]

if (summary[time_columns] < 0).any().any():
    raise ValueError("Negative waiting times found in summary.")

if summary.duplicated(["Activity_Name", "Next_Activity"]).any():
    raise ValueError("Duplicate activity transitions found.")

# Independently calculate expected results from the source
expected = (
    transitions.groupby(["Activity_Name", "Next_Activity"])
    .agg(
        Expected_Count=("Waiting_Minutes", "count"),
        Expected_Average=("Waiting_Minutes", "mean"),
        Expected_Median=("Waiting_Minutes", "median"),
        Expected_Maximum=("Waiting_Minutes", "max"),
    )
    .reset_index()
)

# Compare source transition pairs with summary transition pairs
comparison = expected.merge(
    summary,
    on=["Activity_Name", "Next_Activity"],
    how="outer",
    indicator=True,
)

if (comparison["_merge"] != "both").any():
    raise ValueError(
        "Source and summary transition pairs do not match."
    )

# Compare counts and waiting-time statistics
checks = [
    ("Expected_Count", "Transition_Count"),
    ("Expected_Average", "Average_Wait_Minutes"),
    ("Expected_Median", "Median_Wait_Minutes"),
    ("Expected_Maximum", "Maximum_Wait_Minutes"),
]

for expected_col, actual_col in checks:
    if not (
        comparison[expected_col].astype(float).round(6)
        == comparison[actual_col].astype(float).round(6)
    ).all():
        raise ValueError(
            f"Validation failed: {actual_col} does not match source data."
        )

if int(summary["Transition_Count"].sum()) != len(transitions):
    raise ValueError("Total transition counts do not match source events.")

print("Bottleneck output validation passed!")
print(f"Source events: {len(events)}")
print(f"Source transitions: {len(transitions)}")
print(f"Unique transitions validated: {len(summary)}")
print("Transition pairs: complete and unique")
print("Transition counts: match source")
print("Waiting-time statistics: match source")
print("Missing values and negative waiting times: none")

