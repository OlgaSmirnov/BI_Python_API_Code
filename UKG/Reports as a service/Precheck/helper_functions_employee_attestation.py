
##These functions will be used to help access our endpoints

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



####################################################################
def authenticate():
    """This function helps us log-in to the API. It returns the token, service_id, and instance_key""" 

    #Get the authentication token and instance key 
    
    #Our endpoint
    url="https://service5.ultipro.com/services/BIDataService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml"}
    
    #The body of our SOAP request
    body = """ <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">

    <s:Header>

    <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bidata/2/IBIDataService/LogOn</a:Action>

    <a:To s:mustUnderstand="1">https://servicehost/services/BiDataService</a:To>

    </s:Header>

    <s:Body>

    <LogOn xmlns="http://www.ultipro.com/dataservices/bidata/2">

    <logOnRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance">

    <UserName>001007445</UserName>

    <Password>Ilovewestseattle!@#$32109</Password>

    <ClientAccessKey>PLAB4</ClientAccessKey>

    <UserAccessKey>EQ4FK0000010</UserAccessKey>

    </logOnRequest>

    </LogOn>

    </s:Body>

    </s:Envelope> """
    
    #The response variable
    response = requests.post(url, headers=headers, data=body)
    
    
    #Write the response to a file
    open("file.xml", "w").write(response.text)

    #Open the file as an ElementTree object
    tree = ET.parse('file.xml')
    root = tree.getroot()

    #Get the token from the "Token" element in the tree
    for each in root.iter('{http://www.ultipro.com/dataservices/bidata/2}Token'):
        token = each.text
    #Get the service id
    for each in root.iter('{http://www.ultipro.com/dataservices/bidata/2}ServiceId'):
        service_id = each.text
    #Get the instance key
    for each in root.iter('{http://www.ultipro.com/dataservices/bidata/2}InstanceKey'):
        instance_key = each.text
    
    return (token, service_id, instance_key)


#####################################################################################################################

def get_available_reports():
    """This function return the names and path names for all available UKG reports""" 

    #Our endpoint
    url="https://service5.ultipro.com/services/BIDataService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml"}

    #Get the service id, token, instance_key
    token, service_id, instance_key = authenticate()
    
    body = """   
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">

    <s:Header>

    <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bidata/2/IBIDataService/GetReportList</a:Action>

    <a:To s:mustUnderstand="1">https://servicehost/services/BiDataService</a:To>

    </s:Header>

    <s:Body>

    <GetReportList xmlns="http://www.ultipro.com/dataservices/bidata/2">

    <context xmlns:i="http://www.w3.org/2001/XMLSchema-instance">

    <ServiceId>""" + service_id + """</ServiceId>

    <ClientAccessKey>PLAB4</ClientAccessKey>

    <!-- GUID, unique per user session -->

    <Token>""" + token + """</Token>

    <Status>Ok</Status>

    <StatusMessage i:nil="true" />

    <!-- GUID, unique per user session -->

    <InstanceKey>""" + instance_key + """</InstanceKey>

    </context>

    </GetReportList>

    </s:Body>

    </s:Envelope> """
    
    #Get the response
    response = requests.post(url, headers=headers, data=body)
    
    #Convert XML results to JSON
    o = xmltodict.parse(response.text)
    json_data = json.dumps(o)

    #Turn the JSON data into a Python dictionary
    a_dict = json.loads(json_data)
   

    #Index the Python dictionary 
    emp_dict = a_dict['s:Envelope']['s:Body']['GetReportListResponse']['GetReportListResult']['Reports']['Report']
   

    #Normalize the dictionary, and convert into a pandas dataframe
    df = pd.DataFrame.from_dict(pd.json_normalize(emp_dict), orient='columns')


    #Return the dataframe
    return df 

    #####################################################################################################################

def get_report_parameters(filepath):

    #Our endpoint
    url="https://service5.ultipro.com/services/BIDataService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml"}

    #Get the service id, token, instance_key
    token, service_id, instance_key = authenticate()
    
    body = """   
                <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">

                <s:Header>

                <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bidata/2/IBIDataService/GetReportParameters</a:Action>

                <a:To s:mustUnderstand="1">https://servicehost/services/BiDataService</a:To>

                </s:Header>

                <s:Body>

                <GetReportParameters xmlns="http://www.ultipro.com/dataservices/bidata/2">

                <reportPath>""" + filepath + """</reportPath>

                <context xmlns:i="http://www.w3.org/2001/XMLSchema-instance">

                <ServiceId>""" + service_id + """</ServiceId>

                <ClientAccessKey>PLAB4</ClientAccessKey>

                <!-- GUID, unique per user session -->

                <Token>""" + token + """</Token>

                <Status>Ok</Status>

                <StatusMessage i:nil="true" />

                <!-- GUID, unique per user session -->

                <InstanceKey>""" + instance_key + """</InstanceKey>

                </context>

                </GetReportParameters>

                </s:Body>

                </s:Envelope> """
    
    #Get the response
    response = requests.post(url, headers=headers, data=body)
    
    #Convert XML results to JSON
    o = xmltodict.parse(response.text)
    json_data = json.dumps(o)

    #Turn the JSON data into a Python dictionary
    a_dict = json.loads(json_data)


    #Index the Python dictionary 
    #emp_dict = a_dict['s:Envelope']['s:Body']['GetReportListResponse']['GetReportListResult']['Reports']['Report']
    emp_dict = a_dict['s:Envelope']['s:Body']


    #Normalize the dictionary, and convert into a pandas dataframe
    df = pd.DataFrame.from_dict(pd.json_normalize(emp_dict), orient='columns')


    #Return the dataframe
    return df 








    #####################################################################################################################

   
def get_report_file_path(report_name):
    """This function accepts a report name, and returns its file path in Cognos"""

    #Get the list of available reports
    report_lst = get_available_reports()

    #Find the report path for the report name inserted into the function
    report_path = report_lst[report_lst['ReportName'] == report_name]['ReportPath'].values[0]


    #Return the report path
    return report_path 


#####################################################################################################################


def get_available_precheck_reports():
    """This function return the names and path names for all available precheck reports""" 

    #Get the list of reports
    report_lst = get_available_reports()

    #Get the precheck deduction report pathnames
    return report_lst[report_lst['ReportName'].str.contains('pre', regex=True, case=False)]

#####################################################################################################################
def get_report_key(report_file_path):
    """Get the report key, based on a specified file path. The report key will help us access the report""" 

    #Authenticate to get the token and instance key
    token, service_id, instance_key = authenticate()

    #Our endpoint
    url="https://service5.ultipro.com/services/BIDataService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml"}


    #The body of our SOAP request
    body = """   
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">

    <s:Header>

    <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bidata/2/IBIDataService/ExecuteReport</a:Action>

    <a:To s:mustUnderstand="1">https://servicehost/services/BiDataService</a:To>

    </s:Header>

    <s:Body>

    <ExecuteReport xmlns="http://www.ultipro.com/dataservices/bidata/2">

    <request xmlns:i="http://www.w3.org/2001/XMLSchema-instance">

    <ReportPath>""" + report_file_path + """</ReportPath>

    <ReportParameters>

    <ReportParameter>

    <Name>Month</Name>

    <Value>1</Value>

    <Required>false</Required>

    <DataType>xsdDouble</DataType>

    <MultiValued>true</MultiValued>

    </ReportParameter>

    </ReportParameters>

    </request>

    <context xmlns:i="http://www.w3.org/2001/XMLSchema-instance">

    <ServiceId>3ccd26d5-94b2-4c0f-b88a-5ccfbe3d7fb0</ServiceId>

    <ClientAccessKey>PLAB4</ClientAccessKey>

    <Token>""" + token + """</Token>

    <Status>Ok</Status>

    <StatusMessage i:nil="true" />

    <InstanceKey>""" + instance_key + """</InstanceKey>

    </context>

    </ExecuteReport>

    </s:Body>

    </s:Envelope> """
    
    #Get the response
    response = requests.post(url, headers=headers, data=body)
    
    #Write the response to a file
    open("file.xml", "w").write(response.text)
    
    #Open the file as an ElementTree object
    tree = ET.parse('file.xml')
    root = tree.getroot()

    #Get the report key from the "ReportKey" element in the tree
    for each in root.iter('{http://www.ultipro.com/dataservices/bidata/2}ReportKey'):
        r_key = each.text

    #Return the report key
    return r_key 

 #####################################################################################################################

def retrieve_report(report_file_path):
    """Accepts the report file path as an argument, and retrieves the report as a pandas dataframe""" 

    #Our endpoint
    url="https://service5.ultipro.com/services/BIStreamingService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml", 
            "charset": "utf-8",
            "SOAPAction": "http://www.ultipro.com/dataservices/bistream/2/IBIStreamService/RetrieveReport"}

    #Get the report key
    report_key = get_report_key(report_file_path)


    body = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">
        <s:Header>
            <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bistream/2/IBIStreamService/RetrieveReport</a:Action>
            <h:ReportKey xmlns:h="http://www.ultipro.com/dataservices/bistream/2" xmlns="http://www.ultipro.com/dataservices/bistream/2">""" + report_key + """</h:ReportKey>
            <a:MessageID>urn:uuid:8332571f-3a89-4442-ac80-27195b397b4d</a:MessageID>
            <a:ReplyTo>
                <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
            </a:ReplyTo>
            <a:To s:mustUnderstand="1">https://service5.ultipro.com/services/BIStreamingService</a:To>
        </s:Header>
        <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <RetrieveReportRequest xmlns="http://www.ultipro.com/dataservices/bistream/2"/>
        </s:Body>
    </s:Envelope>"""
    
    #Retrieve the report
    response = requests.post(url, headers=headers, data=body)
 
    #Write the response to a file
    open("file.xml", "w").write(response.text)

    #Open the file as an ElementTree object
    tree = ET.parse('file.xml')
    root = tree.getroot()

    #Get the token from the "Token" element in the tree
    for each in root.iter('{http://www.ultipro.com/dataservices/bistream/2}ReportStream'):
        encoded_report = each.text 
    
    #The report is encoded in base 64, so we  need to decode it.
    decoded = base64.b64decode(encoded_report).decode('utf-8')
    
    #Convert XML results to JSON
    o = xmltodict.parse(decoded)
    json_data = json.dumps(o)
    json_data

    #Turn the JSON data into a Python dictionary
    report_dict = json.loads(json_data)
    
    #Index the Python dictionary so we can retrieve the data
    values_dict = report_dict['dataset']['data']['row']
    
    #Put the data into a list of lists
    list_o_lst = []

    if len(values_dict) > 1:
        for each in values_dict:
            list_o_lst.append(each['value'])
    else:
        list_o_lst.append(values_dict['value'])

    #Turn the list of lists into a dataframe
    df = pd.DataFrame(list_o_lst)
    
    #Get the column names into a list
    column_names_dict = report_dict['dataset']['metadata']['item']

    column_names_lst = []

    #Iterate through the dictionary to grab the column names, and append them to column_names_lst
    for each in column_names_dict:

        #Grab the column name
        column = each['@name']

        #Turn the column name into lowercase
        column = column.lower()

        #Replace whitespace with underscore
        column = column.replace(' ', '_')

        #Append to new list
        column_names_lst.append(column)


    
    #Rename the columns in the dataframe, using column_names_lst
    df.columns = column_names_lst 

    
    #Remove brackets and curly braces from values in dataframe (these will interfere with the create_sql_table() function)
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('{', '', regex=False)
        df[col] = df[col].astype(str).str.replace('}', '', regex=False)
        df[col] = df[col].astype(str).str.replace('[', '', regex=False)
        df[col] = df[col].astype(str).str.replace(']', '', regex=False)
        df[col] = df[col].astype(str).str.replace(',', '_', regex=False)
        df[col] = df[col].astype(str).str.replace("'@xs:nil': 'true'", '', regex=False)   #Replace null values with ''
        df[col] = df[col].astype(str).str.replace(r'(\d{4}-\d{2}-\d{2})T', "\\1 ", regex=True)   #Remove the "T"s in the dates (The /1 presereves the first capture group)


    #Show the report results
    return df 

#####################################################################################################################

def create_sql_table(df, report_name):
    """The function reads in a dataframe containing our report. It then creates a corresponding table in BiData2 containing the report data. This function uses SQL alchemy and df.to_sql,
    and I am not currently using it due to inefficiencies in populating the database tables. Please use create_sql_table_v2() instead""" 

    
    #Create SQL alchemy engine
    engine = sal.create_engine('mssql+pyodbc://DC-BISQL01/BIData2?driver=SQL Server?Trusted_Connection=yes', fast_executemany=True)   #Fast_executemany: Optimizes insert statements for SQL server
    conn = engine.connect()
    
    #Create our connection object
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DC-BISQL01;'
                        'Database=BIData2;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor() 


    #Create a table from our dataframe
    df.to_sql(report_name, 
              engine, 
              if_exists='replace',
              index=False)
              #method='multi')
              #chunksize= round(2100 / len(df.columns)))


    #Close the connection to BiData2
    conn.close()

#####################################################################################################################


def create_sql_table_v2(table_name):
    """The function reads in a CSV file containing our report. It then truncates the PreCheck tables in BiData2, and repopulates them using the data from the CSV""" 

    #Our connection object
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DC-BISQL01;'
                      'Database=BIDATA2;'
                      'Trusted_Connection=yes;')

    #Our cursor object that is used for queries
    cursor = conn.cursor()

    #Truncate the table in BiData2
    cursor.execute("TRUNCATE TABLE " + table_name + ";")


    #Re-populate the table
    cursor.execute(
        r"""    
        -- import the file
        BULK INSERT """ + table_name + " " + 
        r"""FROM 'C:\BI_WH_Solution\Zack_Python_Code\BI_Python_API_Code\UKG\Reports as a service\Precheck\ukg_bulk_insert.csv'
        WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        FIRSTROW = 2)"""
    )

    #Commit the changes
    conn.commit()

    #Close the connection to the database
    conn.close()
    

#####################################################################################################################


def close_sql_connection():
    """The function closes the connection to BiData2""" 

    
    #Create SQL alchemy engine
    engine = sal.create_engine('mssql+pyodbc://DC-BISQL01/BIData2?driver=SQL Server?Trusted_Connection=yes')
    conn = engine.connect()
    
    #Create our connection object
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DC-BISQL01;'
                        'Database=BIData2;'
                        'Trusted_Connection=yes;')

    cursor = conn.cursor()

    
    #Close the connection to BiData2
    conn.close()

############################################################################################################################

def close_api_connection():
    """The function ends the API log-in session"""
    
    #Get the service id, token, instance_key
    token, service_id, instance_key = authenticate()


    #Our endpoint
    url="https://service5.ultipro.com/services/BIDataService"

    #The below headers variable specifies that we are sending the request to a SOAP API
    headers = {"content-type": "application/soap+xml"}


    #The body of our SOAP request
    body = """   
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing"> 
  <s:Header> 
  <a:Action s:mustUnderstand="1">http://www.ultipro.com/dataservices/bidata/2/IBIDataService/LogOff</a:Action>  
    <a:To s:mustUnderstand="1">http://servicehost/services/BiDataService</a:To>  
  </s:Header> 
  <s:Body> 
    <LogOff xmlns="http://www.ultipro.com/dataservices/bidata/2"> 
      <context xmlns:i="http://www.w3.org/2001/XMLSchema-instance"> 
        <ServiceId>""" + service_id + """</ServiceId>  
        <ClientAccessKey>PLAB4</ClientAccessKey>  
        <Token>""" + token + """</Token>  
        <Status>Ok</Status>  
        <StatusMessage i:nil="true" />  
        <InstanceKey>""" + instance_key + """</InstanceKey>  
      </context> 
    </LogOff> 
  </s:Body> 
</s:Envelope> """
    
    #Get the response
    response = requests.post(url, headers=headers, data=body)

    #Return the response
    return response.text