import requests
# import pandas as pd
import json
# import pymysql

api_url = "https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api/v20.3/"
username = "test.user@sb-veevartsm.com"
password = "Kaotiija5"
auth_url = "auth/"
deployment_object_url = "vobjects/"
deployment_table_url = "study_deployment__c/"
new_record_name = "SDeploy_TEST123_TEST_2.3.8675.3090_dummy"
deployment_status = 'build_status__c/'
f = open("responseD.json")
new_record_data = f.read()


with open('new_record.csv', 'r') as file:
    csv_data = file.read()


def get_auth_token():
    return requests.post(api_url + auth_url,  data={"username": username, "password": password}).json()['sessionId']
    
    
token = get_auth_token()
print(token)

headers_get = {"Authorization": token,
           "Content-Type": "application/json",
           "Accept": "application/json"
            }

headers_post = {"Authorization": token,
            "Content-Type": "text/csv",
            "Accept": "text/csv",
            }


def get_deploy_table_content():
    return requests.get(api_url + deployment_object_url + deployment_table_url, headers=headers_get).json()
    
print (get_deploy_table_content())

def create_new_record():
    response = requests.post(api_url + deployment_object_url + deployment_table_url, data=csv_data, headers=headers_post)
    print (response.text)
        
    if response.status_code == 200:
        print("New record added successfully")
    else:
        print(f"Failed to add new record: {response.status_code}, {response.text}")



def read_deployment_status(): 
    response = get_deploy_table_content()
    table_ids = []
    for table in response['data']:            
        response_2 = requests.get(api_url + deployment_object_url + deployment_table_url + table['id'] + "/", headers=headers_get).json()
        # print (response_2['data'].get('build_status__c'))    
        if response_2['data'].get('build_status__c')[0] == 'ready_for_deployment__c':
            table_ids.append(table['id'])
            print(response_2['data']['build_status__c'], table['id'])
        
    return table_ids

# read_deployment_status()

def update_records_ready_for_deployment():
    token = get_auth_token()
    tables_for_deployment = read_deployment_status()
    headers = {"Authorization": token}
    new_status = "Deployment Complete"
    data = {"build_status__c": new_status}

    for table in tables_for_deployment:
        response = requests.put(api_url + deployment_object_url + deployment_table_url + table + "/", headers=headers, data=data)
        print (response)


# update_records_ready_for_deployment()



# Main execution
# try:
#     # Read records
#     df = read_study_deployment()

#     # Update records where status is 'Ready for Deployment'
#     for index, row in df[df['status__c'] == 'Ready for Deployment'].iterrows():
#         if update_record(row['id'], 'Deployment Complete'):
#             df.at[index, 'status__c'] = 'Deployment Complete'

#     # Connect to your SQL database
#     connection = pymysql.connect(host='your_host', user='your_user', password='your_password', db='your_db')
#     cursor = connection.cursor()

#     # Write updated data to SQL database
#     df.to_sql('study_deployment', con=connection, if_exists='replace', index=False)

#     # Close the database connection
#     connection.close()

# except Exception as e:
#     print(f"An error occurred: {e}")
