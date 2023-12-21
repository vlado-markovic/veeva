import requests
import creds_urls

 
token = creds_urls.get_auth_token()
print(token)


def get_deploy_table_content():
    return requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, headers=creds_urls.headers_get).json()
    

def read_deployment_status(): 
    response = get_deploy_table_content()
    table_ids = []

    for table in response['data']:            
        response_2 = requests.get(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url + table['id'] + "/", headers=creds_urls.headers_get).json()

        if response_2['data'].get('build_status__c')[0] == 'ready_for_deployment__c':
            table_ids.append(table['id'])
            # print(response_2['data']['build_status__c'], table['id'])
        
    return table_ids


def update_records_ready_for_deployment():
    tables_for_deployment = read_deployment_status()
    new_status = "complete__c"

    for table_id in tables_for_deployment:
        print(table_id)
        data = {
        "id": table_id,
        "build_status__c": new_status}
        response = requests.put(creds_urls.api_url + creds_urls.deployment_object_url + creds_urls.deployment_table_url, headers=creds_urls.headers_post, json=data)
        # print (response.request.body, data)
        
            
        if response.status_code == 200:
            print("Update successful")
        else:
            print("Update failed:", response.status_code, response.text)


# update_records_ready_for_deployment()

