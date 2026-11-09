\# CareFlow – Clinical Pathway Process Mining



\## Project Overview



CareFlow is a data analytics and process mining project that analyzes simulated hospital patient journey event logs to understand patient flow, identify waiting-time bottlenecks, evaluate pathway conformance, and detect repeated activities and patient delays.



The project demonstrates how Python, SQL, Google BigQuery, dbt, and PM4Py can be combined to build a data pipeline and generate process intelligence from structured event-log data.



\*\*Note:\*\* This project uses synthetic hospital event data for educational and analytical purposes. It does not use real patient records and is not a clinically validated decision-support system.



\## Project Objectives



\- Generate and standardize hospital patient event logs.

\- Store and transform event data using Google BigQuery and dbt.

\- Discover patient pathways using process mining.

\- Analyze activity frequency and waiting times.

\- Identify process bottlenecks and patient journey patterns.

\- Define clinical pathway rules and evaluate process conformance.

\- Analyze patient delays and categorize delay risk.

\- Identify repeated activities and pathway deviation patterns.

\- Validate analytical outputs using Python scripts.



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Event-log generation, data processing, analysis, and validation |

| Pandas | Data manipulation and analysis |

| SQL | Data querying and analytical summaries |

| Google BigQuery | Cloud data warehouse |

| dbt | Data transformation and testing |

| PM4Py | Process mining and process model discovery |

| Graphviz | Process model visualization |

| Power BI | Planned / ongoing interactive reporting |

| Git and GitHub | Version control and project management |



\## Project Workflow



1\. \*\*Event Log Generation:\*\* Generate synthetic hospital event logs containing patient cases, activities, and timestamps.

2\. \*\*Data Standardization:\*\* Standardize event logs into a consistent structure for analysis.

3\. \*\*Data Warehousing:\*\* Load raw event logs into Google BigQuery.

4\. \*\*Data Transformation:\*\* Use dbt to create a staging model and apply data-quality tests.

5\. \*\*Process Discovery:\*\* Use PM4Py to discover patient activity flows and generate a process model.

6\. \*\*Bottleneck Analysis:\*\* Analyze waiting times and identify activities associated with longer delays.

7\. \*\*Patient Journey Analysis:\*\* Study patient activity sequences and common journey patterns.

8\. \*\*Pathway Conformance:\*\* Define pathway rules and compare observed activity sequences against those rules.

9\. \*\*Patient Delay Analysis:\*\* Analyze patient-level delays and summarize delay-risk categories.

10\. \*\*Pathway Deviation Analysis:\*\* Identify repeated activities and classify pathway patterns.

11\. \*\*Reporting:\*\* Prepare analytical outputs and develop a Power BI reporting layer.



\## Dataset Description



The project uses synthetic hospital event-log data.



Main dataset files:



\- `data/raw\_event\_logs.csv` – generated raw event logs.

\- `data/standardized\_event\_logs.csv` – standardized event-log dataset.

\- `data/activity\_frequency\_summary.csv` – activity frequency summary.

\- `data/waiting\_time\_analysis.csv` – waiting-time analysis data.



The standardized event log contains:



\- `Case\_ID` – patient case identifier.

\- `Activity\_Name` – activity performed during the patient journey.

\- `Timestamp` – date and time of the activity.



The project dataset contains 200 simulated patient cases and 1,365 activity events across seven activities:



\- Registration

\- Triage

\- Doctor Consultation

\- X-Ray

\- Treatment

\- Discharge

\- Lab Test



\## Data Engineering



\### Google BigQuery



The raw event logs were loaded into the BigQuery project:



\- Project: `careflow-511314`

\- Dataset: `careflow\_dataset`

\- Raw table: `raw\_event\_logs`

\- Staging view: `stg\_event\_logs`



\### dbt



The dbt project is located in `careflow\_dbt/`.



Key files:



\- `models/stg\_event\_logs.sql` – staging transformation.

\- `models/schema.yml` – model configuration and tests.

\- `dbt\_project.yml` – dbt project configuration.



The dbt staging model standardizes the event-log structure for downstream analysis.



Recorded execution results:



\- dbt run: 1 model passed.

\- dbt test: 3 tests passed.

\- Warnings: 0.

\- Errors: 0.



\## Process Mining and Analytical Modules



\### 1. Process Discovery



PM4Py is used to discover patient activity flows and generate a process model.



Outputs:

\- `outputs/careflow\_process\_model.pnml`

\- `outputs/careflow\_process\_model.png`



\### 2. Bottleneck and Waiting-Time Analysis



Analyzes time gaps between consecutive patient activities to identify potential bottlenecks.



Key scripts:

\- `scripts/analyze\_bottlenecks.py`

\- `scripts/validate\_bottleneck\_analysis.py`

\- `scripts/visualize\_bottlenecks.py`



Outputs:

\- `outputs/bottleneck\_analysis.csv`

\- `outputs/bottleneck\_waiting\_times.png`



\### 3. Patient Journey Analysis



Examines patient activity sequences and common journey patterns.



Key scripts:

\- `scripts/analyze\_patient\_journeys.py`

\- `scripts/validate\_patient\_journeys.py`



Outputs:

\- `outputs/patient\_journey\_sequences.csv`

\- `outputs/common\_patient\_journey\_summary.csv`



\### 4. Clinical Pathway Conformance



Defines expected pathway rules and checks observed patient activity sequences against those project-defined rules.



Key scripts:

\- `scripts/define\_clinical\_pathway\_rules.py`

\- `scripts/validate\_clinical\_pathway\_rules.py`

\- `scripts/check\_pathway\_conformance.py`

\- `scripts/validate\_conformance\_results.py`



Outputs:

\- `outputs/clinical\_pathway\_rules.csv`

\- `outputs/conformance\_results.csv`



\### 5. Patient Delay and Risk Analysis



Analyzes patient-level activity delays and summarizes delay-risk categories.



Key scripts:

\- `scripts/analyze\_patient\_delays.py`

\- `scripts/validate\_patient\_delays.py`

\- `scripts/summarize\_patient\_delay\_risk.py`

\- `scripts/validate\_patient\_delay\_summary.py`



Outputs:

\- `outputs/patient\_delay\_analysis.csv`

\- `outputs/patient\_delay\_risk\_summary.csv`



\### 6. Patient Flow Alerts



Generates patient-flow alerts based on the project's delay analysis.



Key scripts:

\- `scripts/generate\_flow\_alerts.py`

\- `scripts/validate\_flow\_alerts.py`



Output:

\- `outputs/patient\_flow\_alerts.csv`



\### 7. Repeated Activities and Pathway Deviations



Identifies repeated activities within patient journeys and classifies observed pathway patterns.



Key scripts:

\- `scripts/analyze\_pathway\_deviations.py`

\- `scripts/validate\_pathway\_deviations.py`

\- `scripts/analyze\_repeated\_activity\_frequency.py`

\- `scripts/validate\_repeated\_activity\_frequency.py`

\- `scripts/classify\_pathway\_deviations.py`

\- `scripts/validate\_pathway\_deviation\_patterns.py`



Outputs:

\- `outputs/pathway\_deviation\_summary.csv`

\- `outputs/repeated\_activity\_frequency.csv`

\- `outputs/pathway\_deviation\_patterns.csv`



\## Key Analytical Findings



The following findings are based on the current synthetic dataset and project analysis:



\- 200 simulated patient cases and 1,365 activity events were analyzed.

\- 56 patients (28%) had repeated activities.

\- 144 patients (72%) had no repeated activities.

\- Repeated activities were identified for Doctor Consultation and Triage among the 56 patients.

\- Doctor Consultation had 56 patients with repeated instances and 56 extra instances.

\- Triage had 56 patients with repeated instances and 56 extra instances.

\- The pathway deviation pattern summary classified 28% of patients as having repeated Triage and Consultation and 72% as having no repeated activity.



These are analytical patterns in the simulated data. Repeated activities or deviations from project-defined pathway rules should not automatically be interpreted as clinical errors.



\## Validation and Data Quality



The project includes dedicated validation scripts for data quality and analytical outputs.



Validation covers:

\- Missing values and data completeness.

\- Event-log structure and consistency.

\- Patient journey analysis.

\- Bottleneck analysis.

\- Clinical pathway rules and conformance results.

\- Patient delay analysis and risk summaries.

\- Repeated activity frequency.

\- Pathway deviation summaries.



The Day 18 pathway-deviation work completed 14 out of 14 validation checks successfully.



\## Repository Structure



```text

CareFlow/

│

├── data/

│   ├── raw\_event\_logs.csv

│   ├── standardized\_event\_logs.csv

│   ├── activity\_frequency\_summary.csv

│   └── waiting\_time\_analysis.csv

│

├── careflow\_dbt/

│   ├── models/

│   │   ├── stg\_event\_logs.sql

│   │   └── schema.yml

│   └── dbt\_project.yml

│

├── scripts/

│   ├── generate\_event\_logs.py

│   ├── standardize\_event\_logs.py

│   ├── discover\_process\_model.py

│   ├── analyze\_bottlenecks.py

│   ├── analyze\_patient\_journeys.py

│   ├── define\_clinical\_pathway\_rules.py

│   ├── check\_pathway\_conformance.py

│   ├── analyze\_patient\_delays.py

│   ├── generate\_flow\_alerts.py

│   ├── analyze\_pathway\_deviations.py

│   └── validation scripts

│

├── SQL/

│   ├── activity\_frequency.sql

│   ├── patient\_journey\_sequences.sql

│   ├── repeated\_activities.sql

│   └── waiting\_time\_analysis.sql

│

├── outputs/

│   ├── bottleneck\_analysis.csv

│   ├── careflow\_process\_model.png

│   ├── careflow\_process\_model.pnml

│   ├── conformance\_results.csv

│   ├── patient\_delay\_analysis.csv

│   ├── patient\_delay\_risk\_summary.csv

│   ├── patient\_flow\_alerts.csv

│   ├── patient\_journey\_sequences.csv

│   ├── pathway\_deviation\_summary.csv

│   ├── pathway\_deviation\_patterns.csv

│   └── repeated\_activity\_frequency.csv

│

├── documentation/

├── CareFlow\_Overview.pbix

└── README.md

```



\## Limitations



\- The dataset is synthetic and may not represent real hospital operations.

\- Findings depend on the simulated activity sequences and timestamps.

\- Pathway conformance depends on the rules defined for this project.

\- Delay-risk categories are analytical classifications, not clinical risk assessments.

\- The project is a prototype for process analytics and does not provide medical recommendations.



\## Future Scope



\- Develop a complete interactive Power BI dashboard.

\- Add more patient-flow KPIs and drill-down analysis.

\- Expand pathway rules and test additional simulated scenarios.

\- Improve delay monitoring and alert visualizations.

\- Explore predictive analytics for patient-flow delays.



\## How to Run



1\. Clone the repository.

2\. Set up and activate a Python virtual environment.

3\. Install the required Python packages used by the project.

4\. Run the event-log generation and standardization scripts when recreating the dataset.

5\. Configure Google BigQuery credentials and project settings before running warehouse steps.

6\. Run dbt commands from the `careflow\_dbt` directory:



```bash

dbt run

dbt test

```



7\. Run the required Python analysis and validation scripts from the project root.



\## Author



\*\*Tanvi Jadhav\*\*



GitHub: \[Tanu28-pixel](https://github.com/Tanu28-pixel)



Project: \[CareFlow Internship Project](https://github.com/Tanu28-pixel/CareFlow-Internship-Project)
