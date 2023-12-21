import creds_urls
import pymysql
import json
from read_and_update_task1 import get_deploy_table_content

# - populate db with response data
# - read table - find update field, then send request
# - create new rec by using the data from table


# Establishing a connection to the database
connection = pymysql.connect(host=creds_urls.db_host, user=creds_urls.db_user, password=creds_urls.db_password, db=creds_urls.db_name)
def create_table():
    try:
        with connection.cursor() as cursor:
            # SQL to create table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS deployment_data (
                id VARCHAR(255) PRIMARY KEY,
                client_name__c VARCHAR(255),
                global_id__sys VARCHAR(255),
                name__v VARCHAR(255),
                populate_database__c TINYINT(1),
                drug_supply__c VARCHAR(255),
                build_notes__c TEXT,
                system_change_request_number__c VARCHAR(255),
                study_url__c VARCHAR(255),
                project_id__c VARCHAR(255),
                created_date__v DATETIME,
                test_cycle_number__c VARCHAR(255),
                production_sql_updates__c TEXT,
                csv_attachment_order_of_operations__c TEXT,
                created_by__v INT,
                protocol__c VARCHAR(255),
                omni_audit_update__c TINYINT(1),
                sponsor__c VARCHAR(255),
                object_type__v VARCHAR(255),
                system_change_request__c TINYINT(1),
                modified_by__v INT,
                deployment_type__c TEXT, -- Serialized JSON array
                verify_the_backup_was_done__c TINYINT(1),
                modified_date__v DATETIME,
                nightly_task_runtime__c VARCHAR(255),
                build_version__c VARCHAR(255),
                system_version__c VARCHAR(255),
                country__c TEXT, -- Serialized JSON array
                build_status__c TEXT, -- Serialized JSON array
                status__v TEXT -- Serialized JSON array 
            );
            """
            cursor.execute(create_table_sql)
            connection.commit()

            # Query to get column names
            show_columns_sql = "SHOW COLUMNS FROM deployment_data;"
            cursor.execute(show_columns_sql)
            columns = cursor.fetchall()

            print("Columns in 'deployment_data' table:")
            for column in columns:
                print(column[0])

    except Exception as e:
        print(f"Error: {e}")


def populate_table_from_json(json_data, connection):
    for data in json_data:
        
        try:
            # Parse the JSON data
            data = json.loads(json_data)['data']

            # SQL INSERT statement
            insert_sql = """
            INSERT INTO deployment_data (
                id, client_name__c, global_id__sys, name__v, populate_database__c,
                drug_supply__c, build_notes__c, system_change_request_number__c,
                study_url__c, project_id__c, created_date__v, test_cycle_number__c,
                production_sql_updates__c, csv_attachment_order_of_operations__c,
                created_by__v, protocol__c, omni_audit_update__c, sponsor__c,
                object_type__v, system_change_request__c, modified_by__v,
                deployment_type__c, verify_the_backup_was_done__c, modified_date__v,
                nightly_task_runtime__c, build_version__c, system_version__c,
                country__c, build_status__c, status__v
            ) VALUES (
                %(id)s, %(client_name__c)s, %(global_id__sys)s, %(name__v)s, %(populate_database__c)s,
                %(drug_supply__c)s, %(build_notes__c)s, %(system_change_request_number__c)s,
                %(study_url__c)s, %(project_id__c)s, %(created_date__v)s, %(test_cycle_number__c)s,
                %(production_sql_updates__c)s, %(csv_attachment_order_of_operations__c)s,
                %(created_by__v)s, %(protocol__c)s, %(omni_audit_update__c)s, %(sponsor__c)s,
                %(object_type__v)s, %(system_change_request__c)s, %(modified_by__v)s,
                %(deployment_type__c)s, %(verify_the_backup_was_done__c)s, %(modified_date__v)s,
                %(nightly_task_runtime__c)s, %(build_version__c)s, %(system_version__c)s,
                %(country__c)s, %(build_status__c)s, %(status__v)s
            )
            """

            with connection.cursor() as cursor:
                cursor.execute(insert_sql, data)
            connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

def read_from_table():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM deployment_data")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error reading from table: {e}")

# Populate the database with the initial GET response
response_data = get_deploy_table_content()['data']
create_table()



populate_table_from_json(response_data, connection)

# insert_into_table(response_data)

# Reading data from the database for further processing
data_from_db = read_from_table()

# Process data_from_db as needed...

# Your existing functions to interact with the API...
# ...

# Remember to close the database connection when done
connection.close()