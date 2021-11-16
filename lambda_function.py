import json
import psycopg2
from config import config
from datetime import datetime
import random
import string

def connect():
    # Connect to the PostgreSQL database server
    connection = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        # create a cursor
        cur = connection.cursor()

        # initializing string
        str_data = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))

        postgres_insert_query = """ INSERT INTO random_data (valor, fecha) VALUES(%s, %s);"""
        record_to_insert = (str_data, datetime.now())
        cur.execute(postgres_insert_query, record_to_insert)

        connection.commit()

	    # close the communication with the PostgreSQL
        cur.close()
        count = cur.rowcount
        return {
            'statusCode': 200,
            'body': json.dumps(str(count) + "Record inserted successfully into mobile table")
        }
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)
        return {
            'statusCode': 500,
            'body': json.dumps(str(error))
        }
    finally:
        # closing database connection.
        if connection:
            cur.close()
            connection.close()
            print("PostgreSQL connection is closed")

def lambda_handler(event, context):
    connect()
