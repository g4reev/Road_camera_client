import os
from datetime import datetime
import mysql.connector

from dotenv import load_dotenv

from mysql.connector import Error


load_dotenv()


host_ip = os.getenv('host_ip_arena')
user_loc = os.getenv('user_arena')
password_loc = os.getenv('password_arena')
db_name_loc = os.getenv('db_name_arena')

now_time = datetime.now().today()   # 86400 sec on 1 day

now_time_uix = now_time.timestamp()


print(f'Время по UIX {now_time_uix}')

print(f'Время по now {now_time}')




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
        result = cursor.fetchone()        
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        

connection = create_connection(host_ip, user_loc, password_loc, db_name_loc)
print('hello')

# Добавить в запрос фильтрацию по времени- время с поля time в формате UIX со сдвигом 2 часа

query_avd_speed = (
    f"SELECT CAST(AVG(speed) AS CHAR(6)) "
    f"FROM pictures "
    f"WHERE speed > 0 AND time BETWEEN {now_time_uix-86400} AND {now_time_uix}"
)
print(query_avd_speed)
day_avg_speed = execute_read_query(connection, query_avd_speed)

query_cam_info = (
    f"SELECT COUNT(id) AS COUNT, photo_path, ctl_place, i_crypt "
    f"FROM pictures "
    f"WHERE time BETWEEN {now_time_uix-86400} AND {now_time_uix} "
    f"GROUP BY "
    f"ctl_place"
)
print(query_cam_info)
day_cam_info = execute_read_query(connection, query_cam_info)

cam_id = day_cam_info[1][0:7]

print(f'Средняя скорость за последние 24 часа равна {day_avg_speed[0]} км/ч. Контрольное время замера: {now_time}')
print(f'Количество проездов за сутки {day_cam_info[0]}')
print(f'Зав. номер камеры: {cam_id} Место установки камеры: {day_cam_info[2]}, координаты: {day_cam_info[3]}')
