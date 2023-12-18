import requests
import json
import pymysql
from read_and_update_task1 import get_deploy_table_content

get_deploy_table_content()

# Database connection parameters
db_host = "localhost"
db_user = "veeva"
db_password = "veeva"
db_name = "veeva_vault"

# Establishing a connection to the database
connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)

# Your existing API-related code...
# ...

def create_table():
    try:
        with connection.cursor() as cursor:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS deployment_data (
                id VARCHAR(255) PRIMARY KEY,
                client_name VARCHAR(255),
                global_id VARCHAR(255),
                name VARCHAR(255),
                build_status VARCHAR(255),
                created_date DATETIME
                # Add other fields as necessary
            );
            """
            cursor.execute(create_table_sql)
        connection.commit()
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_into_table(data):
    try:
        with connection.cursor() as cursor:
            for record in data:
                insert_sql = "INSERT INTO deployment_data (id, client_name, global_id, name, build_status, created_date) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_sql, (
                    record['id'],
                    record['client_name__c'],
                    record['global_id__sys'],
                    record['name__v'],
                    ', '.join(record['build_status__c']),
                    record['created_date__v']
                ))
        connection.commit()
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
insert_into_table(response_data)

# Reading data from the database for further processing
data_from_db = read_from_table()
# Process data_from_db as needed...

# Your existing functions to interact with the API...
# ...

# Remember to close the database connection when done
connection.close()