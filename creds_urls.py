import requests
import pymysql


## API CREDS
api_url = "https://sb-veevartsm-veeva-rtsm-sbx.veevavault.com/api/v20.3/"
username = "test.user@sb-veevartsm.com"
password = "****"
auth_url = "auth/"
deployment_object_url = "vobjects/"
deployment_table_url = "study_deployment__c/"


# Database connection parameters
db_host = "localhost"
db_user = "veeva"
db_password = "veeva"
db_name = "veeva_vault"

connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)

# Token - Session ID
def get_auth_token():
    return requests.post(api_url + auth_url,  data={"username": username, "password": password}).json()['sessionId']

print(get_auth_token())

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

