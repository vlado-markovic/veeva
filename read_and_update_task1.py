import requests
import creds_urls
import pymysql
from database_crud import update_deployment_value_in_db, get_table_ids_for_deployment


# Establishing a connection to the database
connection = pymysql.connect(host=creds_urls.db_host, user=creds_urls.db_user, password=creds_urls.db_password, db=creds_urls.db_name)

# Get content of study deployment c table
def get_deploy_table_content():
    return requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, headers=creds_urls.headers_get).json()
  
    
# Find the tables with ready for deploy status in veeva vault
def read_deployment_status_directly_from_vault(): 
    response = get_deploy_table_content()
    table_ids = []
    data_from_all_tables = []

    for table in response['data']:            
        response_2 = requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table['id'] + "/", headers=creds_urls.headers_get).json()
        data_from_all_tables.append(response_2)
        if response_2['data'].get('build_status__c')[0] == 'ready_for_deployment__c':
            table_ids.append(table['id'])
            # print(response_2['data']['build_status__c'], table['id'])
        
    return table_ids


# Return all json content from all objects in study_deployment__c API object
def get_table_content():
    response = get_deploy_table_content()
    data_from_all_tables = []

    for table in response['data']:            
        response_2 = requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table['id'] + "/", headers=creds_urls.headers_get).json()
        data_from_all_tables.append(response_2)

    return data_from_all_tables


# Send put request to update values
def put_request_to_veeva_vault(table_id, build_status_key, deploy_complete_value):
    api_url = creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + str(table_id)
    print(f"Updating table ID: {table_id}")
    
    payload = f'{build_status_key}={deploy_complete_value}'
    response = requests.put(api_url, headers=creds_urls.headers_put, data=payload)
    
    if response.status_code == 200:
        print("Update successful for table ID:", table_id)
    else:
        print("Update failed for table ID:", table_id, "Status code:", response.status_code, "Response:", response.text)


# PUT - update record field directly in veeva vault
def update_records_ready_for_deployment_from_vault():
    tables_for_deployment = read_deployment_status_directly_from_vault()
    build_status_key = "build_status__c"
    deploy_complete_value = "complete__c"
    
    for table_id in tables_for_deployment:
        put_request_to_veeva_vault(table_id, build_status_key, deploy_complete_value)
        

# Update records in db and veeva_vault
def update_records_ready_for_deployment_in_db_and_veeva_vault(connection):
    build_status_key = "build_status__c"
    deploy_complete_value = "complete__c"
    
    # Update fields ready for deplyoment in database and return table id's for api update
    tables_for_deployment = get_table_ids_for_deployment(connection)
    print(tables_for_deployment)
    
    update_deployment_value_in_db(connection)
    
    # Send PUT request to API for each updated record
    for table_id in tables_for_deployment:
        print(table_id)
        put_request_to_veeva_vault(table_id, build_status_key, deploy_complete_value)


# Update records in database and update api object in veeva vault - make sure there are records in db 
update_records_ready_for_deployment_in_db_and_veeva_vault(connection)

            
# Backup function to read data directly from vault and update it bypasing the db
# update_records_ready_for_deployment_from_vault()

connection.close()