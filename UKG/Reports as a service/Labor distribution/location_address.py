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

# Step 1: Get the report path
report_path = helper_functions_labor_distribution.get_report_file_path('Locations Address')

 
## Step 2: Retrieve the report and export as a CSV
df = helper_functions_labor_distribution.retrieve_report(report_path) 


# Step 3: Export the report as a CSV
df.to_csv('ukg_bulk_insert.csv', index=False)

# Step 4: Insert the report into BiData2 as a table
helper_functions_labor_distribution.create_sql_table_v2('STG_LocationAddress')

# Step 5: Close the API connection
helper_functions_labor_distribution.close_api_connection()

"""The code to create the SQL Table:
CREATE TABLE ZZ_TEST_Locations_Address(
	address1 VARCHAR(255),
	address2 VARCHAR(255),
	bar_code VARCHAR(255),
	bank_name VARCHAR(255),
	bank VARCHAR(255),
	city VARCHAR(255),
	comments VARCHAR(255),
	contact VARCHAR(255),
	country_code VARCHAR(255),
	country VARCHAR(255),
	county VARCHAR(255),
	fax_number VARCHAR(255),
	gl_account_number VARCHAR(255),
	location_code VARCHAR(255),
	location_ VARCHAR(255),
	location_name VARCHAR(255),
	import_code VARCHAR(255),
	inactive_date VARCHAR(255),
	is_inactive VARCHAR(255),
	mailstop VARCHAR(255),
	modem_number VARCHAR(255),
	phone_extention VARCHAR(255),
	phone_number VARCHAR(255),
	post_season_number_of_games VARCHAR(255),
	reporting_category_code VARCHAR(255),
	reporting_category VARCHAR(255),
	reporting_unit_number VARCHAR(255),
	season_number_of_games VARCHAR(255),
	state_ VARCHAR(255),
	zip_code VARCHAR(255))"""
