
import pandas as pd
from pathlib import Path

# Locate the project and load standardized event logs
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "standardized_event_logs.csv"

df = pd.read_csv(file_path)

# Validate required columns
required_columns = ["Case_ID", "Activity_Name", "Timestamp"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Prepare timestamps and sort patient events
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")
df = df.sort_values(["Case_ID", "Timestamp"])

# Calculate time between consecutive activities for each patient
df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)

df["Waiting_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

transitions = df.dropna(subset=["Next_Activity"]).copy()

# Summarize waiting time by activity transition
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

# Save results
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "bottleneck_analysis.csv"
summary.to_csv(output_file, index=False)

print("Bottleneck analysis completed!")
print(f"Patient cases: {df['Case_ID'].nunique()}")
print(f"Transitions analyzed: {len(transitions)}")
print("\nTop 10 transitions by average waiting time:")
print(summary.head(10).to_string(index=False))
print(f"\nResults saved to: {output_file}")
