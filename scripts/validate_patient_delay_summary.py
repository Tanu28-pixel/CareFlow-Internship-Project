import pandas as pd

summary = pd.read_csv("outputs/patient_delay_risk_summary.csv")
delays = pd.read_csv("outputs/patient_delay_analysis.csv")

# Check patient count
assert len(summary) == 200
assert summary["Case_ID"].nunique() == 200

# Check transition counts
expected = delays.groupby("Case_ID").size().sort_index()
actual = summary.set_index("Case_ID")["Total_Transitions"].sort_index()

assert expected.equals(actual)

# Check waiting time values
assert summary["Average_Waiting_Time"].notna().all()
assert summary["Maximum_Waiting_Time"].notna().all()

# Check risk classifications
assert set(summary["Overall_Delay_Risk"].unique()).issubset(
    {"Low", "Medium", "High"}
)

print("All patient-level summary validation checks passed!")
print("Total patients validated:", len(summary))
print("\nRisk distribution:")
print(summary["Overall_Delay_Risk"].value_counts())