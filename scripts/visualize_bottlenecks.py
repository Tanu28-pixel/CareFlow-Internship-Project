
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project files
project_dir = Path(__file__).resolve().parent.parent
input_file = project_dir / "outputs" / "bottleneck_analysis.csv"
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

# Load bottleneck analysis
df = pd.read_csv(input_file)

if df.empty:
    raise ValueError("Bottleneck analysis file contains no results.")

# Select the 10 transitions with the highest average waiting time
top10 = df.nlargest(10, "Average_Wait_Minutes").copy()
top10["Transition"] = (
    top10["Activity_Name"] + " → " + top10["Next_Activity"]
)
top10 = top10.sort_values("Average_Wait_Minutes")

# Create chart
plt.figure(figsize=(12, 7))
plt.barh(top10["Transition"], top10["Average_Wait_Minutes"])
plt.xlabel("Average Waiting Time (minutes)")
plt.ylabel("Activity Transition")
plt.title("CareFlow: Top 10 Patient Pathway Waiting Times")
plt.tight_layout()

# Save chart
chart_file = output_dir / "bottleneck_waiting_times.png"
plt.savefig(chart_file, dpi=300, bbox_inches="tight")
plt.close()

print("Bottleneck visualization created successfully!")
print(f"Transitions displayed: {len(top10)}")
print(f"Chart saved to: {chart_file}")
