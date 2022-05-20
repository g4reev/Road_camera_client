
import os
import platform
import subprocess

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
today = date.today()   # 86400 sec on 1 day
last_day = today - timedelta(days=1)
yesterday = last_day.strftime("%Y_%m_%d")
print(f'Вчера это: {yesterday}')

log_file = open(f"./logs/{yesterday}.log", "w+")

def logs_insert(context, filename):

    now = datetime.now()
    insert_log = f"{now}: {context}\n"
    print(insert_log)
    filename.write(insert_log)

def ping(host):

    result = False
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '2', host]
    result = subprocess.call(command) == 0
    return result

def create_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        if ping(host_name) or ping(host_name):
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=database_name
            )
            logs_insert(f"Connection to MySQL DB {database_name} successful", log_file)
        else:
            logs_insert(f"Host {host_name} is not available", log_file)
            return False     
    except Error as e:
        logs_insert(f"The error '{e}' occurred", log_file)
        logs_insert(f"Device {type} № {ser_number} is not available, check ip_address, login and password", log_file)       
        return False

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    logs_insert(f"Query to DB: {query}", log_file)
    try:
        cursor.execute(query)
        connection.commit()
        logs_insert(f"Query executed successfully in", log_file)
    except Error as e:
        logs_insert(f"The error '{e}' occurred", log_file)

def execute_read_query(connection, query):
    logs_insert(f"Query to DB: {query}", log_file)
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
    

def lost_conetion(type, ser_number):
    pass

def context_insert(type, ser_number, latitude, longitude, place,
    average_speed, transits, date, status, connection
):
    logs_insert(f"Insert day information for: {type}, {ser_number}, {latitude}, "
        f"{longitude}, {place}, {average_speed}, {transits}, {date}, {status}", log_file
    )
    query_check = (
        f"SELECT day_inf.id "
        f"FROM day_information AS day_inf "       
        f"WHERE day_inf.ser_number = {ser_number} AND day_inf.type = {type }"
    )
    existing_row = execute_read_query(connection, query_check)
    if existing_row:
        logs_insert(f"device id = {existing_row[0]} is be", log_file)
    else:
        query_insert = (
            f"INSERT INTO day_information "
            f"(type, ser_number, latitude, longitude, place, average_speed, transits, date, status) "
            f"VALUES ("
            f"'{type}', '{ser_number}', '{latitude}', '{longitude}', '{place}', {average_speed}, {transits}, '{date}', '{status}')"
        )        
        execute_query(connection, query_insert)    

connection_loc = create_connection(host_ip, user, password, db_name)
id_i = 158 #53 129 156 158 104

while device != []:    
    query_device_data = (
        f"SELECT d.id, d.ip_address, d.type, d.ser_number, d.latitude, d.longitude, "
        f"d.place, d.login, d.pass, s.base, s.table_name, s.column_speed, s.column_date "
        f"FROM device AS d "
        f"JOIN device_db_strucure AS s "
        f"ON s.type = d.type "
        f"WHERE d.id > {id_i} "
        f"ORDER BY d.id "
        f"LIMIT 1"
    )
    device = execute_read_query(connection_loc, query_device_data)    
    if device == [] or device == None:
        break
    id_i = device[0]
    connection_remote = create_connection(device[1], device[7], device[8], device[9])
    if connection_remote:
        query_avd_speed = (
            f"SELECT ROUND(AVG({device[11]}), 2) "
            f"FROM {device[10]} "
            f"WHERE {device[11]} > 0 AND {device[12]} LIKE '{yesterday}%' "
        )
        day_avg_speed = execute_read_query(connection_remote, query_avd_speed)
        query_transits = (
            f"SELECT COUNT(id) AS COUNT "
            f"FROM {device[10]} "
            f"WHERE {device[12]} LIKE '{yesterday}%' "
        )
        transits = execute_read_query(connection_remote, query_transits)
        context_insert(*device[2:7], day_avg_speed[0], transits[0], yesterday, 'Test', connection_loc)
    else:
        lost_conetion(*device[2:4])

log_file.close()
