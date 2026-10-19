
import pandas as pd
import pm4py
from pathlib import Path

# Locate the project and standardized event log
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "standardized_event_logs.csv"

# Load the event log
df = pd.read_csv(file_path)

# Check required columns
required_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Prepare data for PM4Py
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")
df = df.rename(
    columns={
        "Case_ID": "case:concept:name",
        "Activity_Name": "concept:name",
        "Timestamp": "time:timestamp",
    }
)

# Sort events in chronological order within each case
df = df.sort_values(["case:concept:name", "time:timestamp"])

print("Event log loaded successfully!")
print(f"Total events: {len(df)}")
print(f"Unique cases: {df['case:concept:name'].nunique()}")
print(f"Unique activities: {df['concept:name'].nunique()}")

# Convert to a PM4Py event log
event_log = pm4py.convert_to_event_log(df)

print(f"PM4Py event log created: {len(event_log)} cases")
