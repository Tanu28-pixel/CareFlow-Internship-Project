"""
CareFlow: Validate Conformance Results
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

JOURNEY_FILE = BASE_DIR / "outputs" / "patient_journey_sequences.csv"
RESULT_FILE = BASE_DIR / "outputs" / "conformance_results.csv"

journeys = pd.read_csv(JOURNEY_FILE)
results = pd.read_csv(RESULT_FILE)

# Check total patient cases
assert len(results) == len(journeys), "Patient count mismatch"

# Check duplicate patient IDs
assert results["Case_ID"].is_unique, "Duplicate patient IDs found"

# Check valid conformance statuses
valid_statuses = {"Conforming", "Non-Conforming"}

assert set(results["Conformance_Status"]).issubset(
    valid_statuses
), "Invalid conformance status found"

# Check missing values
assert not results.isnull().any().any(), "Missing values found"

# Check patient IDs match source
assert set(results["Case_ID"]) == set(journeys["Case_ID"]), (
    "Patient IDs do not match source data"
)

# Count verification
conforming = (results["Conformance_Status"] == "Conforming").sum()
non_conforming = (
    results["Conformance_Status"] == "Non-Conforming"
).sum()

assert conforming + non_conforming == len(journeys)

print("CONFORMANCE RESULTS VALIDATION")
print("--------------------------------")
print(f"Total patient cases: {len(results)}")
print(f"Conforming journeys: {conforming}")
print(f"Non-conforming journeys: {non_conforming}")
print("Patient count check: PASS")
print("Duplicate ID check: PASS")
print("Status check: PASS")
print("Missing value check: PASS")
print("Source ID matching: PASS")
print("All conformance validations passed!")