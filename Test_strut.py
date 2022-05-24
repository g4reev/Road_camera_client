
from datetime import date, datetime, timedelta
from multiprocessing import connection
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import mysql.connector


(60, '10.133.0.83', 'krechet-sm', '1306019', '56.0459', '54.8028', ' г. Уфа, пр. Октября, Дежневский путепровод, опора №393 «УфаГорСвет» - на юг', 'prometheus', 'e9b711403ecaa5d92c88d086c0601057', 'main', 'events', 'target_speed', 'time')
(195, '10.133.2.59', 'scat-pp', '1906008', '55.999069', '54.714272', ' г. Уфа, ул. Менделеева, 145', 'prometheus', '742b1f653d878052cea31f87510643b7', 'main', 'events', 'target_speed', 'time')

host = '10.133.0.83'
user = 'prometheus'
password = 'e9b711403ecaa5d92c88d086c0601057'
db = 'main'

def create_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print(f"Connection to MySQL DB successful")            
    except Error as e:        
        print(f"The error '{e}' occurred")
        
    return connection

cnx = create_connection(host, user, password, db)

def execute_read_query(connection, query):
    if connection.is_connected():
        print("Is connect")
        cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        logs_insert(f"Query to DB result: {result}", log_file)       
        return result
    except Error as e:
        logs_insert(f"The error '{e}' occurred", log_file)
        logs_insert(f"Query to DB result: {result}", log_file)       
        return result

result = execute_read_query(cnx, "SELECT * FROM events")
print(result)


(105, '10.133.10.149', 'krechet-sm', '1709001', '55.9799', '54.7342', ' г. Уфа, Ул., Айская, 81. э\\о №23', 'prometheus', '215ee55dc14a9f78c2e15aabf6ec93fd', 'main', 'events', 'target_speed', 'time')

# new_flag = map()