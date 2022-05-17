import os
from datetime import date, datetime, timedelta
import mysql.connector

from dotenv import load_dotenv

from mysql.connector import Error
from zmq import device


load_dotenv()
host_ip = os.getenv('host_ip_test')
user = os.getenv('user_test')
password = os.getenv('password_test')
db_name = os.getenv('db_name_test')
now = date.today()   # 86400 sec on 1 day
last_day = now - timedelta(days=1)
yesterday = last_day.strftime("%Y_%m_%d")
print(f'Вчера это: {yesterday}')

def create_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print(f"Connection to MySQL DB {database_name} successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
     cursor = connection.cursor()
     try:
         cursor.execute(query)
         connection.commit()
         print("Query executed successfully")
     except Error as e:
         print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()        
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        

connection_loc = create_connection(host_ip, user, password, db_name)
query_device_data = (
    f"SELECT * "
    f"FROM device "
    f"WHERE id < 100"
)
devices = execute_read_query(connection_loc, query_device_data)
query_device_struc = (
    f"SELECT * "
    f"FROM device_db_strucure "
)
structure = execute_read_query(connection_loc, query_device_struc)
print(structure[0][1])
for d in devices:
    print(d)
    host_ip_d = d[1]
    user_d = d[7]
    password_d = d[8] 
    type_d = d[2]
    
    print(user_d)    
    db_name_d = 'Not Founded'
    for s in structure:
        if type_d == s[1]:
            db_name_d = s[2]
            table_d =s[3]
            field_d = s[4]
    if db_name_d == 'Not Founded':
        print(f'Тип устройства: {type_d} не найден в таблице device_db_strucure')

    connection_d = create_connection(host_ip_d, user_d, password_d, db_name_d)
    query_avd_speed = (
        f"SELECT CAST(AVG({field_d}) AS CHAR(6)) "
        f"FROM {table_d} "
        f"WHERE {field_d} > 0 AND small_path LIKE '{yesterday}%' "
    )
    print(query_avd_speed)
    day_avg_speed = execute_read_query(connection_d, query_avd_speed)
    avg_speed = float(day_avg_speed[0][0])
    print(avg_speed)
    query_transits = (
        f"SELECT COUNT(id) AS COUNT "
        f"FROM {table_d} "
        f"WHERE small_path LIKE '{yesterday}%' "
    )
    print(query_transits)
    transits_d = execute_read_query(connection_d, query_transits)
    transits = int(transits_d[0][0])
    print(transits)

    query_insert = (
        f"INSERT INTO day_information (type, ser_number, place, gps, transit, average_speed, date, status) "
        f"VALUES ("
        f"'{type_d}', '{d[3]}', '{d[6]}', 'N {d[4]} E {d[5]}', {transits}, {avg_speed}, '{yesterday}', 'test')"
    )
    print(query_insert)
    execute_query(connection_loc, query_insert)
    

for s in structure:
    print(s)


