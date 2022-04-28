import os
import mysql.connector
from dotenv import load_dotenv

from mysql.connector import Error


load_dotenv()


host_ip = os.getenv('host_ip_arena')
user_loc = os.getenv('user_arena')
password_loc = os.getenv('password_arena')
db_name_loc = os.getenv('db_name_arena')


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        

connection = create_connection(host_ip, user_loc, password_loc, db_name_loc)
print('hello')

# Добавить в запрос фильтрацию по времени- время с поля time в формате UIX со сдвигом 2 часа
select_day_info = """
SELECT id, photo_path, speed, ctl_place
FROM pictures
WHERE speed > 0 AND time > 1651054983
"""
day_info = execute_read_query(connection, select_day_info)

for info in day_info:
    print(info)
