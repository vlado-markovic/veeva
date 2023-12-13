import requests
import pandas as pd
import json
# import pymysql

api_url = "https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api/v20.3/"
username = "test.user@sb-veevartsm.com"
password = "Kaotiija5"
auth_url = "auth/"
deployment_table_url = "vobjects/"
new_record_name = "SDeploy_TEST123_TEST_2.3.8675.3090_dummy"
deployment_status = 'build_status__c'
f = open("responseD.json")
new_record_data = f.read()


with open('output.csv', 'r') as file:
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
    return requests.get(api_url + deployment_table_url, headers=headers).json()
    

def create_new_record():
    # data = get_deploy_table_content()
    
    # f = open(new_record_content)
    # new_record_data = json.load(f)
    
    url_cre = api_url + deployment_table_url + new_record_name
    
    response = requests.post(api_url + deployment_table_url + new_record_name, data=csv_data, headers=headers_post)
    
        
    if response.status_code == 201:
        print("New record added successfully")
    else:
        print(f"Failed to add new record: {response.status_code}, {response.text}")


create_new_record()


def read_study_deployment():
    response = get_deploy_table_content()

    for table in response['data']:            
        response_2 = requests.get(api_url + deployment_table_url + table['id'] + "/", headers=headers_get).json()
        print (response_2)    
        
        print(response_2['data']['build_status__c'])
        
        
    # if response.status_code == 200:
    #     return pd.DataFrame(response.json()['data'])
    # else:
    #     raise Exception("Failed to fetch records")


# read_study_deployment()





def update_record(record_id, new_status):
    token = get_auth_token()
    headers = {"Authorization": token}
    data = {"status__c": new_status}
    response = requests.put(api_url + f"objects/study_deployment__c/{record_id}", headers=headers, data=data)
    return response.status_code == 200





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
