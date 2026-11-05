import pandas as pd

# Load original and generated data
original = pd.read_csv("data/standardized_event_logs.csv")
delays = pd.read_csv("outputs/patient_delay_analysis.csv")

# Validation checks
assert len(delays) == len(original) - original["Case_ID"].nunique()
assert delays["Waiting_Time_Minutes"].notna().all()
assert (delays["Waiting_Time_Minutes"] >= 0).all()

assert set(delays["Delay_Risk"].unique()).issubset(
    {"Low", "Medium", "High"}
)

assert (
    delays["Waiting_Time_Minutes"].lt(60)
    == delays["Delay_Risk"].eq("Low")
).all()

assert (
    (
        delays["Waiting_Time_Minutes"].ge(60)
        & delays["Waiting_Time_Minutes"].lt(90)
    )
    == delays["Delay_Risk"].eq("Medium")
).all()

assert (
    delays["Waiting_Time_Minutes"].ge(90)
    == delays["Delay_Risk"].eq("High")
).all()

print("All patient delay validation checks passed!")
print("Total validated transitions:", len(delays))
print("Unique patients:", delays["Case_ID"].nunique())