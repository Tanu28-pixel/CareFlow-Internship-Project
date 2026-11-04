import pandas as pd
from pathlib import Path

# Load bottleneck analysis
input_file = Path("outputs/bottleneck_analysis.csv")
df = pd.read_csv(input_file)

# Define configurable thresholds
WARNING_THRESHOLD = 60
CRITICAL_THRESHOLD = 90

# Classify waiting-time risk
def classify_waiting_time(wait):
    if wait >= CRITICAL_THRESHOLD:
        return "Critical"
    elif wait >= WARNING_THRESHOLD:
        return "Warning"
    else:
        return "Normal"

df["Alert_Level"] = df["Average_Wait_Minutes"].apply(
    classify_waiting_time
)

def assign_priority(alert):
    if alert == "Critical":
        return "High"
    elif alert == "Warning":
        return "Medium"
    return "Low"

df["Priority"] = df["Alert_Level"].apply(assign_priority)
# Add transition description
df["Transition"] = (
    df["Activity_Name"] + " -> " + df["Next_Activity"]
)

# Save early-warning report
output_file = Path("outputs/patient_flow_alerts.csv")
df.to_csv(output_file, index=False)

# Display summary
print("PATIENT FLOW EARLY-WARNING REPORT")
print("---------------------------------")
print(df[["Transition", "Average_Wait_Minutes", "Alert_Level"]])

print("\nAlert Summary:")
print(df["Alert_Level"].value_counts())

print(f"\nReport saved to: {output_file}")