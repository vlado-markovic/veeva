# import pymysql
import requests
import creds_urls



with open('new_record.csv', 'r') as file:
    csv_data = file.read()
    
    
def create_new_record():
    response = requests.post(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, data=csv_data, headers=creds_urls.headers_post)
    print (response.text)
        
    if response.status_code == 200:
        print("New record added successfully")
    else:
        print(f"Failed to add new record: {response.status_code}, {response.text}")
        
        
create_new_record()
