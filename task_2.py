# import pymysql
import requests
import pandas as pd

# Function to insert a new record
def insert_new_record(data):
    token = get_auth_token()
    headers = {"Authorization": token}
    response = requests.post(api_url + "objects/study_deployment__c", headers=headers, data=data)
    return response.status_code == 201

# Connect to your SQL database and read the data
connection = pymysql.connect(host='your_host', user='your_user', password='your_password', db='your_db')
df_new_records = pd.read_sql('SELECT * FROM your_new_records_table', connection)
connection.close()

# Insert new records
for index, row in df_new_records.iterrows():
    data = row.to_dict()
    if insert_new_record(data):
        print(f"Record {index} inserted successfully")
    else:
        print(f"Failed to insert record {index}")
