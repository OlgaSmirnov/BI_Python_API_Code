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

# Step 1: Get the file path
report_path = helper_functions_labor_distribution.get_report_file_path('EmployeeAllocation')


## Step 2: Retrieve the report and export as a CSV
df = helper_functions_labor_distribution.retrieve_employee_allocation_report(report_path) 



# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_EmployeeAllocation')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""The code to create the SQL Table:
CREATE TABLE ZZ_TEST_EmployeeAllocation(
	employee NVARCHAR(255), 
	employee_bame NVARCHAR(255), 
	Job NVARCHAR(255), 
	pay_group NVARCHAR(255), 
	location NVARCHAR(255), 
	location_code NVARCHAR(255), 
	annual NVARCHAR(255), 
	hourly NVARCHAR(255), 
	employment_status NVARCHAR(255), 
	allocation NVARCHAR(255), 
	job_code NVARCHAR(255), 
	location_code_2 NVARCHAR(255), 
	location2 NVARCHAR(255), 
	org_level_3_code NVARCHAR(255), 
	scheduled_work_hours NVARCHAR(255))"""
