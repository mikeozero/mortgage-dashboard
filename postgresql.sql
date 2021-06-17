CREATE TABLE "Acct_perf" (
	"ACCT_NUM" int NOT NULL,
	"PRD_CD" int NOT NULL,
	"CREDIT_RISK_INDICATOR" varchar(20),
	"TM_ON_BOOK" int,
	"DAY_PST_DUE" int,
	"RMNG_AMORT_PERIOD" int,
	"DEFLT_INSUR_CD" varchar(20),
	"CRNT_AUTH_LIMIT_AMT" decimal,
	"OS_BAL_AMT" decimal,
	"PRPTY_TYPE_CD" varchar(20),
	"PRPTY_POSTAL_CD" char(6),
	"CRNT_LTV_RATIO" FLOAT,
	"MTH_END_DT" DATE,
	"INSURANCE_FEE_INDICATOR" varchar(5),
	PRIMARY KEY ("ACCT_NUM")
);

CREATE TABLE "DATA_PRODUCT_MAPPING_LKP" (
	"PRD_CD" int NOT NULL,
	"IB_CB_INDICATOR" char(2) NOT NULL,
	"PRD_LVL1" varchar(100),
	"PRD_LVL2" varchar(100),
	"PRD_LVL3" varchar(100),
	"PRD_LVL4" varchar(100),
	"PRD_LVL5" varchar(100),
	"EFF_FROM_DT" DATE,
	"EFF_TO_DT" DATE,
	"CRNT_F" char(1),
	"INSRT_PROCESS_TMSTMP" decimal,
	"UPDT_PROCESS_TMSTMP" decimal,
	PRIMARY KEY ("PRD_CD")
);

ALTER TABLE "Acct_perf" ADD CONSTRAINT "Acct_perf_fk0" FOREIGN KEY ("PRD_CD") REFERENCES "DATA_PRODUCT_MAPPING_LKP"("PRD_CD");



-- after load data into above tables, create view VW_RESD_MTGE_OA_RISK :
-- 代码中的::相当于cast(xxx as int/varchar)

create view VW_RESD_MTGE_OA_RISK as
SELECT a."ACCT_NUM",
    p."PRD_CD",
    concat(
        CASE
            WHEN "substring"(a."MTH_END_DT"::character varying::text, 6, 2)::integer = ANY (ARRAY[1, 11, 12]) THEN 'Q1'::text
            WHEN "substring"(a."MTH_END_DT"::character varying::text, 6, 2)::integer = ANY (ARRAY[2, 3, 4]) THEN 'Q2'::text
            WHEN "substring"(a."MTH_END_DT"::character varying::text, 6, 2)::integer = ANY (ARRAY[5, 6, 7]) THEN 'Q3'::text
            WHEN "substring"(a."MTH_END_DT"::character varying::text, 6, 2)::integer = ANY (ARRAY[8, 9, 10]) THEN 'Q4'::text
            ELSE NULL::text
        END, '-',
        CASE
            WHEN "substring"(a."MTH_END_DT"::character varying::text, 6, 2)::integer = ANY (ARRAY[11, 12]) THEN (("substring"(a."MTH_END_DT"::character varying::text, 3, 2)::integer + 1)::character varying)::text
            ELSE "substring"(a."MTH_END_DT"::character varying::text, 3, 2)
        END) AS "QUARTER_YEAR",
        CASE
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = ANY (ARRAY['T'::text, 'S'::text, 'R'::text]) THEN 'Prairies'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = ANY (ARRAY['A'::text, 'B'::text, 'C'::text, 'E'::text]) THEN 'Atlantic'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = ANY (ARRAY['H'::text, 'G'::text, 'J'::text]) THEN 'Quebec'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = ANY (ARRAY['P'::text, 'L'::text, 'N'::text, 'K'::text]) THEN 'Ontario'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = 'V'::text THEN 'BC'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = 'M'::text THEN 'Toronto'::text
            WHEN "substring"(a."PRPTY_POSTAL_CD"::text, 1, 1) = ANY (ARRAY['X'::text, 'Y'::text]) THEN 'Other'::text
            ELSE 'Ontario'::text
        END AS "REGION",
    a."DAY_PST_DUE",
    a."DEFLT_INSUR_CD",
    a."PRPTY_TYPE_CD",
    a."OS_BAL_AMT",
    a."CRNT_LTV_RATIO",
    round(a."OS_BAL_AMT"::double precision / a."CRNT_LTV_RATIO") AS "CRNT_PRPTY_VAL_AMT",
    p."PRD_LVL4" AS "PRD_TYPE",
    p."EFF_FROM_DT" AS "PRD_EFF_FROM_DT",
    p."EFF_TO_DT" AS "PRD_EFF_TO_DT"
   FROM "Acct_perf" a
     JOIN "DATA_PRODUCT_MAPPING_LKP" p ON a."PRD_CD" = p."PRD_CD"
  WHERE p."PRD_LVL4"::text = 'Standard Mortgages'::text
  ORDER BY a."ACCT_NUM";