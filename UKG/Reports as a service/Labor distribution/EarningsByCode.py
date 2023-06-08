#Import our libraries
import time
import requests
import json
import xml.etree.ElementTree as ET  # for parsing XML
import xmltodict
import pandas as pd
import csv
import base64 
import sqlalchemy

#Import our helper functions
import helper_functions_labor_distribution

# Step 1: Get the file report path we need
report_path = helper_functions_labor_distribution.get_report_file_path('Earnings_by_Code')


## Step 2: Retrieve the report and export as a CSV
df = helper_functions_labor_distribution.retrieve_report(report_path) 


# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_Earnings_by_Code')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""Code to create the table: 

CREATE TABLE ZZ_TEST_EarningsByCode(
	company NVARCHAR(255), 
	employee_name NVARCHAR(255), 
	employee_number NVARCHAR(255), 
	job_code NVARCHAR(255), 
	earnings_code NVARCHAR(255), 
	location_code NVARCHAR(255), 
	location NVARCHAR(255), 
	allocated_earning_amount NVARCHAR(255), 
	allocated_earning_hours NVARCHAR(255), 
	allocation_percent NVARCHAR(255), 
	period_control_date NVARCHAR(255), 
	org_level_3_code NVARCHAR(255), 
	gl_base_segment NVARCHAR(255), 
	gl_sub_account NVARCHAR(255), 
	period_start_date NVARCHAR(255), 
	period_end_date NVARCHAR(255), 
	pay_group NVARCHAR(255), 
	pay_group_code NVARCHAR(255))"""
