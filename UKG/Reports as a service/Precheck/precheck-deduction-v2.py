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
import helper_functions

# Step 1: Get the file report path

report_path = helper_functions.get_report_file_path('Pre-Check Deduction')


## Step 2: Retrieve the report and export as a CSV
df = helper_functions.retrieve_report(report_path) 


#Remove the T's from the column names
#df['period_control_date'] = df['period_control_date'].str.replace('T', ' ')



# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions.create_sql_table_v2('STG_PreCheck_Deduction')

# Step 5: Close the API connection
helper_functions.close_api_connection()
