import pandas as pd

# Load standardized event logs
df = pd.read_csv("data/standardized_event_logs.csv")

# Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort events patient-wise and chronologically
df = df.sort_values(["Case_ID", "Timestamp"])

# Calculate the next activity and timestamp for each patient
df["Next_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(-1)
df["Next_Timestamp"] = df.groupby("Case_ID")["Timestamp"].shift(-1)

# Calculate waiting time in minutes
df["Waiting_Time_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

# Remove final events without a next activity
delays = df.dropna(subset=["Next_Activity"]).copy()

# Classify individual transition delays
def classify_delay(minutes):
    if minutes < 60:
        return "Low"
    elif minutes < 90:
        return "Medium"
    else:
        return "High"

delays["Delay_Risk"] = delays["Waiting_Time_Minutes"].apply(classify_delay)

# Save patient-level transition report
delays.to_csv("outputs/patient_delay_analysis.csv", index=False)

print("Patient delay analysis completed!")
print("Total patient transitions:", len(delays))
print("\nDelay risk distribution:")
print(delays["Delay_Risk"].value_counts())
print("\nSample results:")
print(delays.head(10).to_string(index=False))