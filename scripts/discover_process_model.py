
import pandas as pd
import pm4py
from pathlib import Path
from google.cloud import bigquery

# Project configuration
PROJECT_ID = "careflow-511314"
TABLE_ID = f"{PROJECT_ID}.careflow_dataset.stg_event_logs"

project_dir = Path(__file__).resolve().parent.parent
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

# Read cleaned event data directly from BigQuery
client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT
    case_id AS Case_ID,
    activity_name AS Activity_Name,
    event_timestamp AS Timestamp
FROM `{TABLE_ID}`
WHERE case_id IS NOT NULL
  AND activity_name IS NOT NULL
  AND event_timestamp IS NOT NULL
ORDER BY case_id, event_timestamp
"""

df = client.query(query).to_dataframe()

if df.empty:
    raise ValueError("No event data returned from BigQuery.")

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")

print("BigQuery staging data loaded successfully!")
print(f"Total events: {len(df)}")
print(f"Unique cases: {df['Case_ID'].nunique()}")
print(f"Unique activities: {df['Activity_Name'].nunique()}")

# Convert to the PM4Py event-log format
df = df.rename(
    columns={
        "Case_ID": "case:concept:name",
        "Activity_Name": "concept:name",
        "Timestamp": "time:timestamp",
    }
)

event_log = pm4py.convert_to_event_log(df)
print(f"PM4Py event log created: {len(event_log)} cases")

# Discover the process model
process_tree = pm4py.discover_process_tree_inductive(event_log)
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

# Save the process model
pnml_path = output_dir / "careflow_process_model.pnml"
pm4py.write_pnml(
    net,
    initial_marking,
    final_marking,
    str(pnml_path),
)

# Save a visual diagram
png_path = output_dir / "careflow_process_model.png"
pm4py.save_vis_petri_net(
    net,
    initial_marking,
    final_marking,
    str(png_path),
)

print("Process model discovered successfully!")
print(f"PNML saved to: {pnml_path}")
print(f"PNG saved to: {png_path}")
