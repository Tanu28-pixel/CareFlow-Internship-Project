"""
CareFlow: Validate Clinical Pathway Rules
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_FILE = BASE_DIR / "outputs" / "clinical_pathway_rules.csv"

df = pd.read_csv(RULES_FILE)

required_activities = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "Treatment",
    "Discharge"
]

optional_activities = ["X-Ray", "Lab Test"]

# Check required activities
assert set(required_activities).issubset(
    set(df.loc[df["Activity_Type"] == "Required", "Activity_Name"])
)

# Check optional activities
assert set(optional_activities).issubset(
    set(df.loc[df["Activity_Type"] == "Optional", "Activity_Name"])
)

# Check duplicate activities
assert df["Activity_Name"].is_unique

# Check sequence order
required_df = df[df["Activity_Type"] == "Required"]

assert required_df["Sequence_Order"].astype(int).tolist() == [
    1, 2, 3, 4, 5
]

print("CLINICAL PATHWAY VALIDATION")
print("---------------------------")
print("Required activities: PASS")
print("Optional activities: PASS")
print("Duplicate activity check: PASS")
print("Sequence order check: PASS")
print("All clinical pathway rules validated successfully!")