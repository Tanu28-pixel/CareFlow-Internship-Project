
from pathlib import Path
import pandas as pd

# Locate the raw event log
project_dir = Path(__file__).resolve().parent.parent
input_file = project_dir / "data" / "raw_event_logs.csv"
output_file = project_dir / "data" / "standardized_event_logs.csv"

# Load raw data
df = pd.read_csv(input_file)

# Standardize column names and text values
df.columns = df.columns.str.strip()

required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

df["Case_ID"] = df["Case_ID"].astype("string").str.strip()
df["Activity_Name"] = df["Activity_Name"].astype("string").str.strip()

# Convert timestamps to a consistent datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")

# Reject blank required fields
if df[required_columns].isna().any().any():
    raise ValueError("Required columns contain missing values.")

if (df["Case_ID"] == "").any() or (df["Activity_Name"] == "").any():
    raise ValueError("Case_ID or Activity_Name contains blank values.")

# Sort events chronologically within each patient case
df = df.sort_values(
    ["Case_ID", "Timestamp"],
    kind="stable"
).reset_index(drop=True)

# Save standardized event log
df.to_csv(output_file, index=False, date_format="%Y-%m-%d %H:%M:%S")

print("Standardization completed successfully.")
print("Rows:", len(df))
print("Unique patient cases:", df["Case_ID"].nunique())
print("Unique activities:", df["Activity_Name"].nunique())
print("Output file:", output_file)
