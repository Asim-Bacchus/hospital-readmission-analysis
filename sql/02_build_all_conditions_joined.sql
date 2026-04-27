CREATE OR REPLACE TABLE all_readmissions AS
SELECT
    "Facility ID" AS facility_id,
    "Measure Name" AS condition,
    CAST("Excess Readmission Ratio" AS DOUBLE) AS excess_ratio
FROM read_csv_auto('data/raw/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv')
WHERE "Measure Name" IN (
    'READM-30-HF-HRRP',
    'READM-30-COPD-HRRP',
    'READM-30-PN-HRRP',
    'READM-30-AMI-HRRP',
    'READM-30-HIP-KNEE-HRRP',
    'READM-30-CABG-HRRP'
)
AND "Excess Readmission Ratio" NOT IN ('N/A', 'Too Few to Report', '')
AND "Excess Readmission Ratio" IS NOT NULL;

CREATE OR REPLACE TABLE hcahps_kpis AS
SELECT *
FROM read_csv_auto('data/processed/hospital_kpis_2024.csv');