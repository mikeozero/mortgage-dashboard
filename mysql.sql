CREATE DATABASE MORTGAGE;

USE MORTGAGE;

CREATE TABLE `Acct_perf` (
	`ACCT_NUM` int NOT NULL,
	`PRD_CD` int NOT NULL,
	`CREDIT_RISK_INDICATOR` varchar(20),
	`TM_ON_BOOK` int,
	`DAY_PST_DUE` int,
	`RMNG_AMORT_PERIOD` int,
	`DEFLT_INSUR_CD` varchar(20),
	`CRNT_AUTH_LIMIT_AMT` double,
	`OS_BAL_AMT` double,
	`PRPTY_TYPE_CD` varchar(20),
	`PRPTY_POSTAL_CD` char(6),
	`CRNT_LTV_RATIO` FLOAT,
	`MTH_END_DT` DATE,
	`INSURANCE_FEE_INDICATOR` varchar(5),
	PRIMARY KEY (`ACCT_NUM`)
);

CREATE TABLE `DATA_PRODUCT_MAPPING_LKP` (
	`PRD_CD` int NOT NULL,
	`IB_CB_INDICATOR` char(2) NOT NULL,
	`PRD_LVL1` varchar(100),
	`PRD_LVL2` varchar(100),
	`PRD_LVL3` varchar(100),
	`PRD_LVL4` varchar(100),
	`PRD_LVL5` varchar(100),
	`EFF_FROM_DT` DATE,
	`EFF_TO_DT` DATE,
	`CRNT_F` char(1),
	`INSRT_PROCESS_TMSTMP` double,
	`UPDT_PROCESS_TMSTMP` double,
	PRIMARY KEY (`PRD_CD`)
);

CREATE TABLE `Acct_Credit` (
	`ACCT_NUM` int NOT NULL,
	`PRD_CD` int,
	`MTH_END_DT` DATE,
	`CREDIT_RISK_INDICATOR` varchar(20),
	`DAY_PST_DUE` int,
	`POSTAL_CD` char(6),
	`OS_BAL_AMT` double,
	`PREMIUM` varchar(5),
	`CRNT_AUTH_LIMIT_AMT` double,
	`TM_ON_BOOK` int,
	PRIMARY KEY (`ACCT_NUM`)
);

ALTER TABLE `Acct_Credit` ADD CONSTRAINT `Acct_Credit_fk0` FOREIGN KEY (`PRD_CD`) REFERENCES `DATA_PRODUCT_MAPPING_LKP`(`PRD_CD`);

ALTER TABLE `Acct_perf` ADD CONSTRAINT `Acct_perf_fk0` FOREIGN KEY (`PRD_CD`) REFERENCES `DATA_PRODUCT_MAPPING_LKP`(`PRD_CD`);



-- after load data into above tables, create views:

-- create view VW_RESD_MTGE_OA_RISK:
create view VW_RESD_MTGE_OA_RISK as
select `a`.`ACCT_NUM` AS `ACCT_NUM`,`p`.`PRD_CD` AS `PRD_CD`,concat((case when (substr(`a`.`MTH_END_DT`,6,2) in (1,11,12)) then 'Q1' when (substr(`a`.`MTH_END_DT`,6,2) in (2,3,4)) then 'Q2' when (substr(`a`.`MTH_END_DT`,6,2) in (5,6,7)) then 'Q3' when (substr(`a`.`MTH_END_DT`,6,2) in (8,9,10)) then 'Q4' end),'-',(case when (substr(`a`.`MTH_END_DT`,6,2) in (11,12)) then (substr(`a`.`MTH_END_DT`,3,2) + 1) else substr(`a`.`MTH_END_DT`,3,2) end)) AS `QUARTER_YEAR`,
(case when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) in ('T','S','R')) then 'Prairies' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) in ('A','B','C','E')) then 'Atlantic' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) in ('H','G','J')) then 'Quebec' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) in ('P','L','N','K')) then 'Ontario' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) = 'V') then 'BC' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) = 'M') then 'Toronto' when (substr(`a`.`PRPTY_POSTAL_CD`,1,1) in ('X','Y')) then 'Other' else 'Ontario' end) AS `REGION`,
`a`.`DAY_PST_DUE` AS `DAY_PST_DUE`,`a`.`DEFLT_INSUR_CD` AS `DEFLT_INSUR_CD`,`a`.`PRPTY_TYPE_CD` AS `PRPTY_TYPE_CD`,`a`.`OS_BAL_AMT` AS `OS_BAL_AMT`,`a`.`CRNT_LTV_RATIO` AS `CRNT_LTV_RATIO`,(case when (`a`.`CRNT_LTV_RATIO` <> 0) then round((`a`.`OS_BAL_AMT` / `a`.`CRNT_LTV_RATIO`),0) else 0 end) AS `CRNT_PRPTY_VAL_AMT`,`p`.`PRD_LVL4` AS `PRD_TYPE`,`a`.`CRNT_AUTH_LIMIT_AMT` AS `CRNT_AUTH_LIMIT_AMT`,`a`.`RMNG_AMORT_PERIOD` AS `RMNG_AMORT_PERIOD`,`a`.`TM_ON_BOOK` AS `TM_ON_BOOK`,`p`.`EFF_FROM_DT` AS `PRD_EFF_FROM_DT`,`p`.`EFF_TO_DT` AS `PRD_EFF_TO_DT`
from (`Acct_perf` `a` join `DATA_PRODUCT_MAPPING_LKP` `p` on((`a`.`PRD_CD` = `p`.`PRD_CD`)))
where (`p`.`PRD_LVL4` = 'Standard Mortgages')
order by `a`.`ACCT_NUM`

-- create view VW_CREDIT_CARD_RISK:
create view VW_CREDIT_CARD_RISK as
select `a`.`ACCT_NUM` AS `ACCT_NUM`,`p`.`PRD_CD` AS `PRD_CD`,concat((case when (substr(`a`.`MTH_END_DT`,6,2) in (1,11,12)) then 'Q1' when (substr(`a`.`MTH_END_DT`,6,2) in (2,3,4)) then 'Q2' when (substr(`a`.`MTH_END_DT`,6,2) in (5,6,7)) then 'Q3' when (substr(`a`.`MTH_END_DT`,6,2) in (8,9,10)) then 'Q4' end),'-',(case when (substr(`a`.`MTH_END_DT`,6,2) in (11,12)) then (substr(`a`.`MTH_END_DT`,3,2) + 1) else substr(`a`.`MTH_END_DT`,3,2) end)) AS `QUARTER_YEAR`,
(case when (substr(`a`.`POSTAL_CD`,1,1) in ('T','S','R')) then 'Prairies' when (substr(`a`.`POSTAL_CD`,1,1) in ('A','B','C','E')) then 'Atlantic' when (substr(`a`.`POSTAL_CD`,1,1) in ('H','G','J')) then 'Quebec' when (substr(`a`.`POSTAL_CD`,1,1) in ('P','L','N','K')) then 'Ontario' when (substr(`a`.`POSTAL_CD`,1,1) = 'V') then 'BC' when (substr(`a`.`POSTAL_CD`,1,1) = 'M') then 'Toronto' when (substr(`a`.`POSTAL_CD`,1,1) in ('X','Y')) then 'Other' else 'Ontario' end) AS `REGION`,
`a`.`DAY_PST_DUE` AS `DAY_PST_DUE`,`a`.`CREDIT_RISK_INDICATOR` AS `CREDIT_RISK_INDICATOR`,`a`.`OS_BAL_AMT` AS `OS_BAL_AMT`,`p`.`PRD_LVL4` AS `PRD_TYPE`,`a`.`CRNT_AUTH_LIMIT_AMT` AS `CRNT_AUTH_LIMIT_AMT`,`a`.`TM_ON_BOOK` AS `TM_ON_BOOK`,`p`.`EFF_FROM_DT` AS `PRD_EFF_FROM_DT`,`p`.`EFF_TO_DT` AS `PRD_EFF_TO_DT`
from (`Acct_Credit` `a` join `DATA_PRODUCT_MAPPING_LKP` `p` on((`a`.`PRD_CD` = `p`.`PRD_CD`)))
where (`p`.`PRD_LVL3` = 'Credit Cards')
order by `a`.`ACCT_NUM`