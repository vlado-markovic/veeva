import creds_urls
import pymysql

# - populate db with response data
# - read table - find update field, then send post update
# - create new rec by using the data from table


# Establishing a connection to the database
connection = pymysql.connect(host=creds_urls.db_host, user=creds_urls.db_user, password=creds_urls.db_password, db=creds_urls.db_name)



def read_from_table():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM deployment_data")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error reading from table: {e}")


def create_record(build_status):
    pass

def read_record(id):
    pass

def update(id, data):
    pass

def delete(id):
    pass



# Reading data from the database for further processing
# data_from_db = read_from_table()

# Process data_from_db as needed...

# Your existing functions to interact with the API...
# ...

# Remember to close the database connection when done
connection.close()