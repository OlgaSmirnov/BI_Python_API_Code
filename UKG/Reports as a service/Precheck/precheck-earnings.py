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

# Step 1: Get the report file path
report_path = helper_functions.get_report_file_path('Pre-Check Earnings')

## Step 2: Retrieve the report
df = helper_functions.retrieve_report(report_path) 


"""#Clean the columns
df['period_control_date'] = df['period_control_date'].str.replace('T', ' ')

#Display a 0 for null numeric columns
df['current_amount'] = df['current_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['current_hours'] = df['current_hours'].astype(str).replace("'@xs:nil': 'true'", '0')
df['base_amount'] = df['base_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['hourly_pay_rate'] = df['hourly_pay_rate'].astype(str).replace("'@xs:nil': 'true'", '0')
df['ytd_amount'] = df['ytd_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['pay_rate'] = df['pay_rate'].astype(str).replace("'@xs:nil': 'true'", '0')"""


# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions.create_sql_table_v2('STG_PreCheck_Earnings')

# Step 5: Close the API connection
helper_functions.close_api_connection()
