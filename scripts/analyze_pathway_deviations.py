
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "standardized_event_logs.csv"
OUTPUT_FILE = BASE_DIR / "outputs" / "pathway_deviation_summary.csv"

# Load event logs
df = pd.read_csv(INPUT_FILE)

# Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort patient activities chronologically
df = df.sort_values(["Case_ID", "Timestamp"])

# Count activities for each patient
activity_counts = (
    df.groupby(["Case_ID", "Activity_Name"])
    .size()
    .reset_index(name="Activity_Count")
)

# Identify repeated activities
repeated = activity_counts[
    activity_counts["Activity_Count"] > 1
].copy()

# Calculate number of repeated activity types per patient
repeated_summary = (
    repeated.groupby("Case_ID")
    .agg(
        Repeated_Activity_Types=("Activity_Name", "count"),
        Total_Repeated_Events=("Activity_Count", lambda x: (x - 1).sum()),
        Repeated_Activities=(
            "Activity_Name",
            lambda x: ", ".join(x)
        )
    )
    .reset_index()
)

# Add patients without repeated activities
all_patients = pd.DataFrame({
    "Case_ID": df["Case_ID"].unique()
})

result = all_patients.merge(
    repeated_summary,
    on="Case_ID",
    how="left"
)

result["Repeated_Activity_Types"] = (
    result["Repeated_Activity_Types"].fillna(0).astype(int)
)

result["Total_Repeated_Events"] = (
    result["Total_Repeated_Events"].fillna(0).astype(int)
)

result["Repeated_Activities"] = (
    result["Repeated_Activities"].fillna("None")
)

result["Deviation_Status"] = result[
    "Repeated_Activity_Types"
].apply(
    lambda x: "Repeated Activity Detected" if x > 0
    else "No Repeated Activity"
)

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_FILE, index=False)

print("Pathway deviation analysis completed!")
print("Total patients:", len(result))
print("Patients with repeated activities:",
      (result["Repeated_Activity_Types"] > 0).sum())
print("Patients without repeated activities:",
      (result["Repeated_Activity_Types"] == 0).sum())
print("\nRepeated activity summary:")
print(result.head(10).to_string(index=False))
print("\nSaved to:", OUTPUT_FILE)
