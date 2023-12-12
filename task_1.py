import requests
import pandas as pd
# import pymysql

api_url = "https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api/v20.3/"
username = "test.user@sb-veevartsm.com"
password = "Kaotiija5"

# {Authorization: {'responseStatus': 'SUCCESS', 'sessionId': '5C337C9EBA7D9F1D744DBCEEE98E26E5AA08531766A6E6BB99522BA6DBCD0EA57C09E869B87F3A969E6EAA2611A6A55E82823C50BCA49A6FC0CEE50DD22FD8C9', 'userId': 18234483, 'vaultIds': [{'id': 177737, 'name': 'Veeva RTSM SBX', 'url': 'https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api'}]




def get_auth_token():
    auth_url = "auth/"
    return requests.post(api_url + auth_url,  data={"username": username, "password": password}).json()['sessionId']
    


def read_study_deployment():
    token = get_auth_token()
    deployment_table_url = "vobjects/study_deployment__c/"
    headers = {"Authorization": token,
               "Content-Type": "application/json"
               }
    
    response = requests.get(api_url + deployment_table_url, headers=headers).json()
    
    fields = 'build_status__c'

    for table in response['data']:

        # print (api_url + deployment_table_url + table['id'] + "/")
            
        response_2 = requests.get(api_url + deployment_table_url + table['id'] + "/", headers=headers, params={'fields': fields})    
        records = response_2.json()
        
        
    print(records)
        
        
    # if response.status_code == 200:
    #     return pd.DataFrame(response.json()['data'])
    # else:
    #     raise Exception("Failed to fetch records")


read_study_deployment()


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
