\# CareFlow – Clinical Pathway Process Mining

\## Technical Project Documentation



\## 1. Introduction



CareFlow is a clinical pathway process mining project designed to analyze simulated hospital patient journeys using event-log data.



The project focuses on understanding how patients move through different hospital activities, identifying waiting-time bottlenecks, analyzing pathway conformance, and detecting repeated activities and patient delays.



It combines Python, SQL, Google BigQuery, dbt, and PM4Py to demonstrate a structured data engineering and analytics workflow.



\*\*Project type:\*\* Data Analytics and Process Mining

\*\*Dataset:\*\* Synthetic hospital event logs

\*\*Patient cases:\*\* 200

\*\*Total events:\*\* 1,365

\*\*Unique activities:\*\* 7



\## 2. Problem Statement



Hospital processes involve multiple activities, including registration, triage, consultation, testing, treatment, and discharge.



Analyzing these activities can help identify:



\- Delays between consecutive activities.

\- Frequently repeated activities.

\- Differences between observed and expected patient pathways.

\- Patient journey patterns.

\- Potential process bottlenecks.



CareFlow demonstrates how event-log analysis and process mining can be used to explore these operational patterns.



\## 3. Project Objectives



1\. Generate synthetic hospital event-log data.

2\. Standardize event records for analysis.

3\. Store and transform event data using Google BigQuery and dbt.

4\. Discover patient pathways using PM4Py.

5\. Analyze waiting times and process bottlenecks.

6\. Examine patient journey sequences.

7\. Define clinical pathway rules.

8\. Evaluate pathway conformance.

9\. Analyze patient-level delays and risk categories.

10\. Identify repeated activities and pathway deviation patterns.

11\. Validate analytical results using Python.



\## 4. Dataset and Event Log Structure



The project uses simulated patient event logs.



\### Dataset fields



| Column | Description |

|---|---|

| Case\_ID | Unique patient case identifier |

| Activity\_Name | Activity performed during the patient journey |

| Timestamp | Date and time of the activity |



\### Activities



The dataset contains seven activities:



1\. Registration

2\. Triage

3\. Doctor Consultation

4\. X-Ray

5\. Treatment

6\. Discharge

7\. Lab Test



\### Dataset statistics



| Metric | Value |

|---|---:|

| Patient cases | 200 |

| Total events | 1,365 |

| Unique activities | 7 |

| Average events per patient | 6.825 |



The main dataset files are:



\- `raw\_event\_logs.csv`

\- `standardized\_event\_logs.csv`



\## 5. Technology and Tools



\### Python

Used for:

\- Synthetic event-log generation.

\- Data standardization.

\- Patient journey analysis.

\- Waiting-time and bottleneck analysis.

\- Patient delay analysis.

\- Repeated activity analysis.

\- Validation of analytical outputs.



\### Pandas

Used for loading, transforming, grouping, and analyzing event-log data.



\### SQL

Used for querying event logs and generating analytical summaries.



\### Google BigQuery

Used as the cloud data warehouse.



Project configuration:

\- Project ID: `careflow-511314`

\- Dataset: `careflow\_dataset`

\- Raw table: `raw\_event\_logs`

\- Staging view: `stg\_event\_logs`



\### dbt

Used to transform and test event-log data.



Important files:

\- `dbt\_project.yml`

\- `models/stg\_event\_logs.sql`

\- `models/schema.yml`



Recorded results:

\- dbt models passed: 1

\- dbt tests passed: 3

\- Warnings: 0

\- Errors: 0



\### PM4Py

Used for process discovery and generation of a process model from event-log data.



\### Graphviz

Used to visualize the discovered process model.



\### Power BI

Used as the reporting layer for project insights. The interactive dashboard is planned for the final project stage.



\### Git and GitHub

Used for version control and maintaining the project repository.



\## 6. Project Implementation



\### Phase 1: Event Log Generation



A Python script generates synthetic hospital event logs.



Script:

\- `scripts/generate\_event\_logs.py`



The generated records represent patient cases, activities, and timestamps.



\### Phase 2: Event Log Standardization



The raw event logs are transformed into a standardized structure.



Script:

\- `scripts/standardize\_event\_logs.py`



Output:

\- `data/standardized\_event\_logs.csv`



\### Phase 3: Data Warehousing and Transformation



The raw event logs are loaded into Google BigQuery.



The dbt staging model prepares event-log data for downstream analysis.



Model:

\- `careflow\_dbt/models/stg\_event\_logs.sql`



The schema configuration contains the dbt model tests.



\### Phase 4: Process Discovery



PM4Py is used to discover the patient activity flow from the standardized event logs.



Script:

\- `scripts/discover\_process\_model.py`



Outputs:

\- `outputs/careflow\_process\_model.pnml`

\- `outputs/careflow\_process\_model.png`



The process model provides a visual representation of observed activity transitions.



\### Phase 5: Bottleneck and Waiting-Time Analysis



This phase examines the time between consecutive patient activities.



Scripts:

\- `scripts/analyze\_bottlenecks.py`

\- `scripts/validate\_bottleneck\_analysis.py`

\- `scripts/visualize\_bottlenecks.py`



Outputs:

\- `outputs/bottleneck\_analysis.csv`

\- `outputs/bottleneck\_waiting\_times.png`



The analysis helps identify activities and transitions associated with longer waiting times.



\### Phase 6: Patient Journey Analysis



Patient activity sequences are examined to understand common journey patterns.



Scripts:

\- `scripts/analyze\_patient\_journeys.py`

\- `scripts/validate\_patient\_journeys.py`



Outputs:

\- `outputs/patient\_journey\_sequences.csv`

\- `outputs/common\_patient\_journey\_summary.csv`



\### Phase 7: Clinical Pathway Rules and Conformance



Project-defined clinical pathway rules are created and compared with observed patient activity sequences.



Scripts:

\- `scripts/define\_clinical\_pathway\_rules.py`

\- `scripts/validate\_clinical\_pathway\_rules.py`

\- `scripts/check\_pathway\_conformance.py`

\- `scripts/validate\_conformance\_results.py`



Outputs:

\- `outputs/clinical\_pathway\_rules.csv`

\- `outputs/conformance\_results.csv`



This analysis identifies differences between observed activity sequences and the rules defined for the project.



\### Phase 8: Patient Delay and Risk Analysis



Patient-level activity delays are analyzed and summarized into delay-risk categories.



Scripts:

\- `scripts/analyze\_patient\_delays.py`

\- `scripts/validate\_patient\_delays.py`

\- `scripts/summarize\_patient\_delay\_risk.py`

\- `scripts/validate\_patient\_delay\_summary.py`



Outputs:

\- `outputs/patient\_delay\_analysis.csv`

\- `outputs/patient\_delay\_risk\_summary.csv`



\### Phase 9: Patient Flow Alerts



A Python-based analysis generates patient-flow alerts using the project's delay-analysis logic.



Scripts:

\- `scripts/generate\_flow\_alerts.py`

\- `scripts/validate\_flow\_alerts.py`



Output:

\- `outputs/patient\_flow\_alerts.csv`



\### Phase 10: Repeated Activities and Pathway Deviations



Patient activity sequences are analyzed to identify repeated activities and classify pathway patterns.



Scripts:

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



\## 7. Key Analytical Findings



\### Dataset overview



\- 200 simulated patient cases.

\- 1,365 activity events.

\- 7 unique activities.



\### Repeated activity analysis



The analysis identified:



| Category | Patients | Percentage |

|---|---:|---:|

| Repeated activities | 56 | 28% |

| No repeated activities | 144 | 72% |

| Total | 200 | 100% |



\### Repeated activity frequency



| Activity | Patients with repetition | Total instances | Extra instances |

|---|---:|---:|---:|

| Doctor Consultation | 56 | 112 | 56 |

| Triage | 56 | 112 | 56 |



\### Pathway deviation patterns



| Pattern | Patients | Percentage |

|---|---:|---:|

| No Repeated Activity | 144 | 72% |

| Repeated Triage and Consultation | 56 | 28% |



These results describe patterns in the simulated dataset. They should not be interpreted as evidence of clinical errors or inappropriate patient care.



\## 8. Validation and Quality Assurance



Dedicated validation scripts are maintained across the project.



Validation areas include:



\- Event-log completeness.

\- Missing-value checks.

\- Patient journey consistency.

\- Bottleneck analysis validation.

\- Clinical pathway rule validation.

\- Conformance result validation.

\- Patient delay validation.

\- Delay-risk summary validation.

\- Repeated activity frequency validation.

\- Pathway deviation pattern validation.



For the Day 18 pathway-deviation analysis, all 14 validation checks passed.



Recorded result:



\*\*14/14 validation checks passed.\*\*



\## 9. Project Deliverables



The project produces:



1\. Raw and standardized event-log datasets.

2\. BigQuery event-log storage and dbt staging transformation.

3\. Process discovery model in PNML format.

4\. Process model visualization.

5\. Bottleneck and waiting-time analysis.

6\. Patient journey sequences and summaries.

7\. Clinical pathway rules and conformance results.

8\. Patient delay analysis and risk summaries.

9\. Patient flow alerts.

10\. Repeated activity frequency analysis.

11\. Pathway deviation summaries.

12\. Validation scripts and reports.

13\. Project README and technical documentation.

14\. Power BI reporting file.



\## 10. Limitations



\- The dataset is synthetic and does not represent actual hospital records.

\- Simulated timestamps and activity sequences may not reflect real operational conditions.

\- The pathway rules are defined for this project and are not universal clinical standards.

\- Delay-risk categories are analytical classifications, not medical risk assessments.

\- Repeated activities do not necessarily indicate errors or poor-quality care.

\- The project is an educational process analytics prototype, not a production hospital monitoring system.



\## 11. Future Scope



\- Complete and improve the interactive Power BI dashboard.

\- Add patient-flow KPIs and interactive filters.

\- Explore additional simulated pathway scenarios.

\- Improve delay monitoring and alert visualization.

\- Expand pathway conformance analysis.

\- Explore predictive analytics for operational delays.



\## 12. Conclusion



CareFlow demonstrates an end-to-end analytical workflow for simulated hospital event logs.



By combining Python, SQL, BigQuery, dbt, and PM4Py, the project transforms structured event data into process models, waiting-time analysis, patient journey insights, pathway conformance results, and repeated activity analysis.



The project provides practical experience in data preparation, data warehousing, process mining, analytical validation, and reporting.



\## 13. Repository



GitHub: https://github.com/Tanu28-pixel/CareFlow-Internship-Project



\*\*Author:\*\* Tanvi Jadhav



\*\*Project:\*\* CareFlow – Clinical Pathway Process Mining
