import pandas as pd

df = pd.read_csv("outputs/patient_delay_analysis.csv")

# Summarize delays for each patient
summary = df.groupby("Case_ID").agg(
    Total_Transitions=("Waiting_Time_Minutes", "count"),
    Average_Waiting_Time=("Waiting_Time_Minutes", "mean"),
    Maximum_Waiting_Time=("Waiting_Time_Minutes", "max"),
    High_Risk_Delays=("Delay_Risk", lambda x: (x == "High").sum()),
    Medium_Risk_Delays=("Delay_Risk", lambda x: (x == "Medium").sum())
).reset_index()

# Assign overall patient risk
def patient_risk(row):
    if row["High_Risk_Delays"] > 0:
        return "High"
    elif row["Medium_Risk_Delays"] > 0:
        return "Medium"
    return "Low"

summary["Overall_Delay_Risk"] = summary.apply(patient_risk, axis=1)

summary.to_csv("outputs/patient_delay_risk_summary.csv", index=False)

print("Patient-level risk summary generated!")
print("\nOverall patient risk distribution:")
print(summary["Overall_Delay_Risk"].value_counts())
print("\nSample patient summary:")
print(summary.head(10).to_string(index=False))