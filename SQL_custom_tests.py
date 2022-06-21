
import os
import platform
import subprocess

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error


load_dotenv()
host_ip = os.getenv('host_ip_test')
user = os.getenv('user_test')
password = os.getenv('password_test')
db_name = os.getenv('db_name_test')
today = date.today()   # 86400 sec on 1 day
last_day = today - timedelta(days=1)
yesterday = last_day.strftime("%Y_%m_%d")
print(f'Вчера это: {yesterday}')

log_file = open(f"./logs/{yesterday}.log", "a")
log_file.seek(0, 2)
not_connet_id = []
db_answer_error = []

def logs_insert(context, filename):

    now = datetime.now()
    time_format = "%Y-%m-%d %H:%M:%S"
    insert_log = f"{now: {time_format}}: {context}\n"
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
        logs_insert(f"Check login and password", log_file)  
        logs_insert(f"The error '{e}' occurred", log_file)             
        return False
    return connection

def execute_query(connection, query):
    logs_insert(f"Query to DB: {query}", log_file)
    cursor = connection.cursor()    
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
        f"SELECT id "
        f"FROM day_information "       
        f"WHERE ser_number = '{ser_number}' AND type = '{type}'"
    )
    existing_row = execute_read_query(connection, query_check)
    if existing_row == None or existing_row == []:    
        query_insert = (
            f"INSERT INTO day_information "
            f"(type, ser_number, latitude, longitude, place, average_speed, transits, date, status) "
            f"VALUES ("
            f"'{type}', '{ser_number}', '{latitude}', '{longitude}', '{place}', {average_speed}, {transits}, '{date}', '{status}')"
        ) 
        execute_query(connection, query_insert)
    else:
        logs_insert(f"device is be", log_file)
        query_insert = (
            f"UPDATE day_information "
            f"SET status = '{status}', average_speed = {average_speed}, transits = {transits}, date = '{date}' "
            f"WHERE ser_number = '{ser_number}' AND type = '{type}'"
        )
        execute_query(connection, query_insert)

def main_quertes(id, con_loc):
    
    query_device_data = (
        f"SELECT d.id, d.ip_address, d.type, d.ser_number, d.latitude, d.longitude, "
        f"d.place, d.login, d.pass, s.base, s.table_name, s.column_speed, s.column_date "
        f"FROM device AS d "
        f"JOIN device_db_strucure AS s "
        f"ON s.type = d.type "
        f"WHERE d.id > {id} "
        f"ORDER BY d.id "
        f"LIMIT 1"
    )
    
    device = execute_read_query(con_loc, query_device_data)    
    if device == [] or device == None:
        logs_insert(f"Device with id = {id} is last", log_file)
        return []
    connection_remote = create_connection(device[1], device[7], device[8], device[9])
    print(device[0])
    if connection_remote:
        query_avd_speed = (
            f"SELECT ROUND(AVG({device[11]}), 2) "
            f"FROM {device[10]} "
            f"WHERE {device[11]} > 0 AND {device[12]} LIKE '{yesterday}%' "
        )
        day_avg_speed = execute_read_query(connection_remote, query_avd_speed)
        if day_avg_speed == None or day_avg_speed == []:
            logs_insert(f"Not correct answer1 from DB device id: {device[0]}", log_file)
            db_answer_error.append(device[0])
        else:
            query_transits = (
                f"SELECT COUNT(id) AS COUNT "
                f"FROM {device[10]} "
                f"WHERE {device[12]} LIKE '{yesterday}%' "
            )
            transits = execute_read_query(connection_remote, query_transits)
            if transits == None or transits == []:
                logs_insert(f"Not correct answer2 from DB device id: {device[0]}", log_file)
                db_answer_error.append(device[0])
            else:
                context_insert(*device[2:7], day_avg_speed[0], transits[0], yesterday, 'Test', con_loc)
    else:
        not_connet_id.append(device[0])  # добавить сюда ИП адрес логин и пароль в лог
        lost_conetion(*device[2:4])
    return device[0]

connection_loc = create_connection(host_ip, user, password, db_name)
id_i = 0 #122 158
job = 1

while job != []:
    job = main_quertes(id_i, connection_loc)
    print(job)
    if job != [] or job != None:
        id_i = job
        print(id_i)
    else:
        break
logs_insert(f"Not connect device id: \n{db_answer_error}", log_file)
logs_insert(f"Not correct answer from DB device id: \n{not_connet_id}", log_file)
log_file.close()
