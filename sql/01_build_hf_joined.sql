-- Filter readmissions to HF only, clean nulls, join to HCAHPS KPIs

CREATE OR REPLACE TABLE hf_readmissions AS
SELECT
    "Facility ID" AS facility_id,
    CAST("Excess Readmission Ratio" AS DOUBLE) AS hf_excess_ratio
FROM read_csv_auto('data/raw/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv')
WHERE "Measure Name" = 'READM-30-HF-HRRP'
  AND "Excess Readmission Ratio" NOT IN ('N/A', 'Too Few to Report', '')
  AND "Excess Readmission Ratio" IS NOT NULL;

CREATE OR REPLACE TABLE hcahps_kpis AS
SELECT *
FROM read_csv_auto('data/processed/hospital_kpis_2024.csv');

CREATE OR REPLACE TABLE hf_nurse_joined AS
SELECT
    h.facility_id,
    CAST(h.nurse_comm_stars AS INTEGER) AS nurse_comm_stars,
    r.hf_excess_ratio
FROM hcahps_kpis h
INNER JOIN hf_readmissions r ON h.facility_id = r.facility_id
WHERE h.nurse_comm_stars IS NOT NULL
  AND TRY_CAST(h.nurse_comm_stars AS INTEGER) IS NOT NULL;

COPY hf_nurse_joined TO 'data/processed/hf_nurse_comm_joined.csv' (HEADER, DELIMITER ',');