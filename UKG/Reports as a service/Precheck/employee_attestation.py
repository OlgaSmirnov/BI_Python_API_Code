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
import sys

#Set the path variable, so python can find the module, helper_functions_employee_attestation
sys.path.append(r"\\dc-bisql01\UKG\Reports as a service\Precheck")

#Import our helper functions
import helper_functions_employee_attestation

#Get the attestation data file path
report_file_path = helper_functions_employee_attestation.get_report_file_path('Attestation V4')

## Step 2: Retrieve the report
df = helper_functions_employee_attestation.retrieve_report(report_file_path) 

# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_employee_attestation.create_sql_table_v2('[BIData2].[dbo].[STG_EmployeeAttestation]')

# Step 5: Close the API connection
helper_functions_employee_attestation.close_api_connection()