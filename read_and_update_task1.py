import requests
import creds_urls
import pymysql

# Establishing a connection to the database
connection = pymysql.connect(host=creds_urls.db_host, user=creds_urls.db_user, password=creds_urls.db_password, db=creds_urls.db_name)

 
token = creds_urls.get_auth_token()
print(token)


def get_deploy_table_content():
    return requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, headers=creds_urls.headers_get).json()
    

def read_deployment_status_directly_from_vault(): 
    response = get_deploy_table_content()
    table_ids = []
    data_from_all_tables = []

    for table in response['data']:            
        response_2 = requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table['id'] + "/", headers=creds_urls.headers_get).json()
        data_from_all_tables.append(response_2)
        
        if response_2['data'].get('build_status__c')[0] == 'draft__c':
            table_ids.append(table['id'])
            # print(response_2['data']['build_status__c'], table['id'])
        
    return table_ids

# Return all json content from all objects in study_deployment__c 
def get_table_content():
    
    response = get_deploy_table_content()
    data_from_all_tables = []

    for table in response['data']:            
        response_2 = requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table['id'] + "/", headers=creds_urls.headers_get).json()
        data_from_all_tables.append(response_2)

    return data_from_all_tables


# PUT - update record field
def update_records_ready_for_deployment_from_vault():
    tables_for_deployment = read_deployment_status_directly_from_vault()
    

    for table_id in tables_for_deployment:
        print(table_id)
        api_url = creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table_id
        payload = 'build_status__c=ready_for_deployment__c'
        response = requests.put(api_url, headers=creds_urls.headers_put, data=payload)
        print (response.request.body)
        
            
        if response.status_code == 200:
            print("Update successful")
        else:
            print("Update failed:", response.status_code, response.text)


def update_records_ready_for_deployment(connection):
    build_status_key = "build_status__c"
    deploy_ready_value = "ready_for_deployment__c"
    deploy_complete_value = "complete__c"
    

    try:
        # Read and update records in the database
        with connection.cursor() as cursor:
            # Select records where build_status__c is 'ready_for_deployment__c'
            select_sql = f"SELECT id FROM deployment_data WHERE build_status__c = '{deploy_ready_value}'"
            cursor.execute(select_sql)
            tables_for_deployment = [row[0] for row in cursor.fetchall()]

            # Update records in the database
            update_sql = f"UPDATE deployment_data SET build_status__c = %s WHERE build_status__c = '{deploy_ready_value}'"
            cursor.execute(update_sql, (deploy_complete_value))
        connection.commit()

        # Send PUT request to API for each updated record
        for table_id in tables_for_deployment:
            api_url = creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table_id
            print(f"Updating table ID: {table_id}")
            
            payload = f'{build_status_key}={deploy_complete_value}'
            response = requests.put(api_url, headers=creds_urls.headers_put, data=payload)
            
            if response.status_code == 200:
                print("Update successful for table ID:", table_id)
            else:
                print("Update failed for table ID:", table_id, "Status code:", response.status_code, "Response:", response.text)

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()


update_records_ready_for_deployment(connection)




            
            
            
# update_records_ready_for_deployment_from_vault()

connection.close()