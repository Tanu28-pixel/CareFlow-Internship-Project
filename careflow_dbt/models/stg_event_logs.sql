
{{ config(
    materialized='view'
) }}

SELECT
    CAST(Case_ID AS STRING) AS case_id,
    TRIM(Activity_Name) AS activity_name,
    SAFE_CAST(Timestamp AS TIMESTAMP) AS event_timestamp
FROM `careflow-511314.careflow_dataset.raw_event_logs`
WHERE
    Case_ID IS NOT NULL
    AND Activity_Name IS NOT NULL
    AND Timestamp IS NOT NULL
    AND TRIM(Activity_Name) != ''
