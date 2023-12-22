import creds_urls
import pymysql


# Establishing a connection to the database
connection = pymysql.connect(host=creds_urls.db_host, user=creds_urls.db_user, password=creds_urls.db_password, db=creds_urls.db_name)

build_status_key = "build_status__c"
deploy_ready_value = "ready_for_deployment__c"
deploy_complete_value = "complete__c"

def read_from_table():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM deployment_data")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error reading from table: {e}")

# GET ID's from tables that contain ready_for_deployment__c status
def get_table_ids_for_deployment(connection):
    with connection.cursor() as cursor:

        # Select records where build_status__c is 'ready_for_deployment__c'
        select_sql = "SELECT id FROM deployment_data WHERE build_status__c = 'ready_for_deployment__c';"
        print(cursor.execute(select_sql))
        tables_for_deployment = [row[0] for row in cursor.fetchall()]
        return tables_for_deployment


# Update build_status__c if its value is ready_for_deployment__c
def update_deployment_value_in_db(connection):
    with connection.cursor() as cursor:

        # Update records in the database
        update_sql = "UPDATE deployment_data SET build_status__c = 'complete__C' WHERE build_status__c = 'ready_for_deployment__c'"
        cursor.execute(update_sql)
        connection.commit()
    

def create_record(build_status):
    pass

def read_record(id):
    pass

def update(id, data):
    pass

def delete(id):
    pass



# Remember to close the database connection when done
connection.close()