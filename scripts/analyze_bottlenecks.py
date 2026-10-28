

import pandas as pd
from pathlib import Path

# Locate the project and load standardized event logs
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "standardized_event_logs.csv"

if not file_path.exists():
    raise FileNotFoundError(f"Event log file not found: {file_path}")

df = pd.read_csv(file_path)

# Validate required columns
required_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

if df[required_columns].isnull().any().any():
    raise ValueError("Required event-log columns contain missing values.")

# Prepare timestamps and sort patient events
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")
df = df.sort_values(["Case_ID", "Timestamp"]).copy()

# Calculate time between consecutive activities for each patient
df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)

df["Waiting_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

transitions = df.dropna(subset=["Next_Activity"]).copy()

if transitions.empty:
    raise ValueError("No consecutive activity transitions were found.")

# Validate waiting times
if transitions["Waiting_Minutes"].isna().any():
    raise ValueError("Some transitions have missing waiting times.")

if (transitions["Waiting_Minutes"] < 0).any():
    raise ValueError(
        "Negative waiting times found. Check event timestamps and ordering."
    )

# Summarize EVERY observed activity transition
summary = (
    transitions.groupby(["Activity_Name", "Next_Activity"])
    .agg(
        Transition_Count=("Waiting_Minutes", "count"),
        Average_Wait_Minutes=("Waiting_Minutes", "mean"),
        Median_Wait_Minutes=("Waiting_Minutes", "median"),
        Maximum_Wait_Minutes=("Waiting_Minutes", "max"),
    )
    .reset_index()
    .sort_values("Average_Wait_Minutes", ascending=False)
)

# Validate summary
if summary.duplicated(["Activity_Name", "Next_Activity"]).any():
    raise ValueError("Duplicate transition pairs found in summary.")

if summary["Transition_Count"].sum() != len(transitions):
    raise ValueError("Transition counts do not match the source transitions.")

# Save results
output_dir = project_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "bottleneck_analysis.csv"
summary.to_csv(output_file, index=False)

print("Bottleneck analysis completed successfully!")
print(f"Patient cases: {df['Case_ID'].nunique()}")
print(f"Events: {len(df)}")
print(f"Transitions analyzed: {len(transitions)}")
print(f"Unique transition pairs: {len(summary)}")
print("\nTop 10 transitions by average waiting time:")
print(summary.head(10).to_string(index=False))
print(f"\nComplete transition summary saved to: {output_file}")
