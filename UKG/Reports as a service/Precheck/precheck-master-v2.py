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
report_path = helper_functions.get_report_file_path('Pre-Check Master')



## Step 2: Retrieve the report
df = helper_functions.retrieve_report(report_path) 

#Clean the columns
#df['period_control_date'] = df['period_control_date'].str.replace('T', ' ')
#df['period_end_date'] = df['period_end_date'].str.replace('T', ' ')
df.rename(columns={'last,_first_mi': 'last_first_mi'}, inplace=True)

"""#Display a 0 for null numeric columns
df['hourly_pay_rate'] = df['hourly_pay_rate'].astype(str).replace("'@xs:nil': 'true'", '0')
df['annual_salary'] = df['annual_salary'].astype(str).replace("'@xs:nil': 'true'", '0')
df['total_hours'] = df['total_hours'].astype(str).replace("'@xs:nil': 'true'", '0')
df['check_amount'] = df['check_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['direct_deposit_amount'] = df['direct_deposit_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['net_amount'] = df['net_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['total_earning_amount'] = df['total_earning_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['total_deduction_amount'] = df['total_deduction_amount'].astype(str).replace("'@xs:nil': 'true'", '0')
df['total_taxes'] = df['total_taxes'].astype(str).replace("'@xs:nil': 'true'", '0')"""


# Step 3: Export the report into a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions.create_sql_table_v2('STG_PreCheck_Master')

# Step 5: Close the API connection
helper_functions.close_api_connection()