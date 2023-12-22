# import pymysql
import requests
import creds_urls
import pymysql
import json

# mandatory fields
record = {	
    'project_id__c': 'V4A000000001001',
    'deployment_type__c': 'initial__c',
    'environment__c': 'dev__c',
    'build_version__c': 'v1.0.0_',
    'build_status__c': 'ready_for_deployment__c'
}


# read csv file with mandatory fields for creating new record
with open('new_record.csv', 'r') as file:
    csv_data = file.read()
 

# Create new record in veeva_vault api from csv with post request
# make sure your build_version in csv is unique
def create_new_record_from_csv():
    response = requests.post(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, data=csv_data, headers=creds_urls.headers_post)
    print (response.text)
        
    if response.status_code == 200:
        print("New record added successfully")
    else:
        print(f"Failed to add new record: {response.status_code}, {response.text}")
        

# Update the table in vault api
def create_new_record_with_post(payload):
    api_url = creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url
    print(payload)
    response = requests.request("POST", api_url, headers=creds_urls.headers_put, data=payload)
    print(response.text)
    # id_value = response["data"]["id"]
    # return(id_value)


def create_new_record_in_db_and_update_api(connection, table_name, record_data):
    base_build_version = record_data['build_version__c']
    current_build_version = base_build_version
    version_suffix = 1

    try:
        with connection.cursor() as cursor:
            while True:
                # Check if the current build_version already exists
                select_sql = f"SELECT COUNT(*) FROM {table_name} WHERE build_version__c = %s"
                cursor.execute(select_sql, (current_build_version,))
                if cursor.fetchone()[0] == 0:
                    break  # Unique build_version found, exit loop

                # Append a number to the build_version and try again
                current_build_version = f"{base_build_version}_{version_suffix}"
                version_suffix += 1

            # Update record_data with the unique build_version
            record_data['build_version__c'] = current_build_version

            # Insert new record
            # columns = ', '.join(f"`{col}`" for col in record_data.keys())  
            # placeholders = ', '.join(['%s'] * len(record_data))
            # insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            # print (tuple(record_data.values()))
            # cursor.execute(insert_sql, tuple(record_data.values()))

            # Commit the changes
            connection.commit()
            print(f"Record inserted successfully with build_version {current_build_version}.")
            
        
            print(create_new_record_with_post(record_data))

    except pymysql.MySQLError as e:
        print(f"Error while inserting data into database: {e}")
        return False


# creates new record in database with mandatory fields, and unique build_version, then updates the api valut object with the new record 
create_new_record_in_db_and_update_api(creds_urls.connection, 'deployment_data', record)

