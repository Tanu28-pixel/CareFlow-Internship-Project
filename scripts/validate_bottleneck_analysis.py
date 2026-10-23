
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
input_file = project_dir / "outputs" / "bottleneck_analysis.csv"

required_columns = [
    "Activity_Name",
    "Next_Activity",
    "Transition_Count",
    "Average_Wait_Minutes",
    "Median_Wait_Minutes",
    "Maximum_Wait_Minutes",
]

if not input_file.exists():
    raise FileNotFoundError(f"Analysis file not found: {input_file}")

df = pd.read_csv(input_file)

if df.empty:
    raise ValueError("Bottleneck analysis file is empty.")

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

if df[required_columns].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

if (df["Transition_Count"] <= 0).any():
    raise ValueError("Transition counts must be positive.")

time_columns = [
    "Average_Wait_Minutes",
    "Median_Wait_Minutes",
    "Maximum_Wait_Minutes",
]

if (df[time_columns] < 0).any().any():
    raise ValueError("Negative waiting times found.")

if df.duplicated(["Activity_Name", "Next_Activity"]).any():
    raise ValueError("Duplicate activity transitions found.")

print("Bottleneck output validation passed!")
print(f"Transitions validated: {len(df)}")
print("Required columns: present")
print("Missing values: none")
print("Waiting times: non-negative")
print("Transition pairs: unique")
