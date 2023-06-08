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

# Step 1: Get report path
report_path = helper_functions_labor_distribution.get_report_file_path('Organizational Levels')


## Step 2: Retrieve the report and export as a CSV
df = helper_functions_labor_distribution.retrieve_report(report_path) 


# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_OrgLevel')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""The code to create the SQL table:
CREATE TABLE ZZ_TEST_Organizational_Levels(
	gl_segement VARCHAR(255),
	level_ VARCHAR(255),
	manager_name VARCHAR(255),
	manager_alternate_email VARCHAR(255),
	manager_email VARCHAR(255),
	organization_code VARCHAR(255),
	organization VARCHAR(255),
	status_code VARCHAR(255),
	status_ VARCHAR(255))"""
