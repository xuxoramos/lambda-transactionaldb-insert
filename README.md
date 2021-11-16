# Lambda Function para inserción periódica en PostgreSQL

En mi clase de Bases de Datos no relacionales vemos, como módulo final, la construcción de Data Lakes.

Para este propósito, vamos a configurar los siguientes componentes en AWS:

1. Una instancia de EC2 con una _elastic ip_
2. Un PostgreSQL dentro de esa instancia de EC2, de acuerdo [a esta guía](https://computingforgeeks.com/how-to-install-postgresql-13-on-ubuntu/)
3. Crear una tabla de juguete que representará nuestros sistemas transaccionales
4. Crear una _lambda function_ que insertará en dicha tabla de juguete
5. Configurar un evento en AWS EventBridge para que se dispare cada 2 min y llame a la _lambda function_ de arriba

## Tabla de juguete

```sql
CREATE TABLE random_data (
	id serial4 NOT NULL,
	valor text NULL,
	fecha timestamp NULL,
	CONSTRAINT random_data_pkey PRIMARY KEY (id)
);
```

## Lambda Function

```python
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
```

## Evento en EventBridge

