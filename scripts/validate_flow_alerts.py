import pandas as pd

source = pd.read_csv("outputs/bottleneck_analysis.csv")
results = pd.read_csv("outputs/patient_flow_alerts.csv")

print("PATIENT FLOW ALERT VALIDATION")
print("--------------------------------")

# Check total records
assert len(source) == len(results)
print("Record count check: PASS")

# Check duplicate transitions
assert not results["Transition"].duplicated().any()
print("Duplicate transition check: PASS")

# Check alert categories
valid_alerts = ["Normal", "Warning", "Critical"]
assert results["Alert_Level"].isin(valid_alerts).all()
print("Alert category check: PASS")

# Check missing values
assert not results.isnull().any().any()
print("Missing value check: PASS")

# Check threshold classification
for _, row in results.iterrows():
    wait = row["Average_Wait_Minutes"]
    alert = row["Alert_Level"]

    if wait >= 90:
        assert alert == "Critical"
    elif wait >= 60:
        assert alert == "Warning"
    else:
        assert alert == "Normal"

print("Threshold classification check: PASS")

# Check priority classification
valid_priorities = ["Low", "Medium", "High"]

assert results["Priority"].isin(valid_priorities).all()
print("Priority classification check: PASS")

# Verify priority matches alert level
for _, row in results.iterrows():
    if row["Alert_Level"] == "Critical":
        assert row["Priority"] == "High"
    elif row["Alert_Level"] == "Warning":
        assert row["Priority"] == "Medium"
    else:
        assert row["Priority"] == "Low"

print("Priority mapping check: PASS")

print("\nAll flow alert validations passed!")