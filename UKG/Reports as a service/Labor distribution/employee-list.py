#Import our libraries
import time
import requests
import json
import xml.etree.ElementTree as ET  # for parsing XML
import xmltodict
import pandas as pd
import csv
import base64 
import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR

#Import our helper functions
import helper_functions_labor_distribution

# Step 1: Get the report file path that we need
report_path = helper_functions_labor_distribution.get_report_file_path('Employee List')

## Step 2: Retrieve the report
df = helper_functions_labor_distribution.retrieve_report(report_path) 


# Step 3: Export the report to a CSV file
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_EmployeeList')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""
#Create table query
CREATE TABLE ZZ_TEST_Employee_List (
pay_group NVARCHAR(255),
 ssn NVARCHAR(255),
 employee_number NVARCHAR(255),
 employee_name NVARCHAR(255),
 address NVARCHAR(255),
 city NVARCHAR(255),
 state NVARCHAR(255),
 zip_code NVARCHAR(255),
 email_address NVARCHAR(255),
 alternate_email NVARCHAR(255),
 birth_date NVARCHAR(255),
 hourly_pay_rate NVARCHAR(255),
 annual NVARCHAR(255),
 scheduled_work_hours NVARCHAR(255),
 employment_type NVARCHAR(255),
 org_level_1_code NVARCHAR(255),
 org_level_1 NVARCHAR(255),
 job_code NVARCHAR(255),
 job NVARCHAR(255),
 alternate_title NVARCHAR(255),
 seniority_date NVARCHAR(255),
 last_hire_date NVARCHAR(255),
 employment_status NVARCHAR(255),
 org_level_2_code NVARCHAR(255),
 org_level_2 NVARCHAR(255),
 org_level_3_code NVARCHAR(255),
 termination_date NVARCHAR(255),
 first_name NVARCHAR(255),
 last_name NVARCHAR(255),
 middle_name NVARCHAR(255),
 supervisor_name NVARCHAR(255),
 supervisor_employee_number NVARCHAR(255),
 supervisor_email_address NVARCHAR(255),
 location NVARCHAR(255),
 location_code NVARCHAR(255))"""


