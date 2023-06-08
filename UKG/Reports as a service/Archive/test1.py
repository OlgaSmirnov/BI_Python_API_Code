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


get_available_reports()