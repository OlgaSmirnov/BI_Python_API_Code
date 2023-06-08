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

# Step 1: Get file path of report
report_path = helper_functions_labor_distribution.get_report_file_path('Locations')

 
## Step 2: Retrieve the report and export as a CSV
df = helper_functions_labor_distribution.retrieve_report(report_path) 
 


# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_Location')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""Code to create the table: 

CREATE TABLE ZZ_TEST_Location(
	Location_Code NVARCHAR(255),
	Location NVARCHAR(255),
	Inactivation_Date NVARCHAR(255),
	Inactive NVARCHAR(255))"""
