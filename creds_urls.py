import requests


## API CREDS
api_url = "https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api/v20.3/"
username = "test.user@sb-veevartsm.com"
password = "Kaotiija5"
auth_url = "auth/"
deployment_object_url = "vobjects/"
deployment_table_url = "study_deployment__c/"


# Database connection parameters
db_host = "localhost"
db_user = "veeva"
db_password = "veeva"
db_name = "veeva_vault"

# Token - Session ID
def get_auth_token():
    return requests.post(api_url + auth_url,  data={"username": username, "password": password}).json()['sessionId']


## HEADERS for get, post, and put
headers_get = {"Authorization": get_auth_token(),
           "Content-Type": "application/json",
           "Accept": "application/json"
            }

headers_post = {"Authorization": get_auth_token(),
            "Content-Type": "text/csv",
            "Accept": "text/csv",
            }

headers_put = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': get_auth_token()
  }

