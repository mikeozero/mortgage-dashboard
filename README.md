# mortgage-dashboard
**Using python+echarts to create a dashboard**  
**(cell phone, ipad and web browser friendly)**
![image](https://user-images.githubusercontent.com/53555169/122324619-1a64f500-cef7-11eb-8af6-e1a159b51f9a.png)

**The source data ('mortgage.csv' and 'Data_Product Hierarchy.xlsx') in sources/**

**1. readcsv.py:** directly read and process data from 'mortgage.csv'. to check the result, just modify the app.py file as below:  
![image](https://user-images.githubusercontent.com/53555169/122326425-4766d700-cefa-11eb-902b-88b4cc1b2683.png)

**2. mysql.sql:** DDL statements, create tables 'Acct_perf', 'DATA_PRODUCT_MAPPING_LKP' and view 'VW_RESD_MTGE_OA_RISK' in mysql.

**3. postgresql.sql:** DDL statements, create tables 'Acct_perf', 'DATA_PRODUCT_MAPPING_LKP' and view 'VW_RESD_MTGE_OA_RISK' in postgresql. postgresql is case sensitive, create table "Test"... and create table Test... are different. In SqlAlchemy, any table name or column name including uppercase letters will be added "" autometicly.

**4. models.py:** ETL source data into database (mysql | postgresql).  
![image](https://user-images.githubusercontent.com/53555169/122328828-4cc62080-cefe-11eb-836c-7e41ec7e7e4c.png)

**5. readdatabase.py:** read and process data from view 'VW_RESD_MTGE_OA_RISK'. to check the result, just modify the app.py file as below:  
![image](https://user-images.githubusercontent.com/53555169/122329156-e8579100-cefe-11eb-9b58-b4a32e26ff53.png)
