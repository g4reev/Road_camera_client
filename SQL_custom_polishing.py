import logging
import os
import platform
import subprocess
from datetime import date, timedelta

from dotenv import load_dotenv
from mysql import connector


def ping(host):
    """ Function of ping {host}"""

    result = False
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '2', host]
    result = subprocess.call(command) == 0
    logger.debug(f'Ping {host} take result: {result}')
    return result


def create_connection(host_name, user_name, user_password, database_name):
    """ Creat connetion to database """

    connection = None
    try:
        if ping(host_name) or ping(host_name):
            connection = connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=database_name
            )
            logger.debug(f"Connection to MySQL DB {database_name} successful")
        else:
            logger.error(f"Host {host_name} is not available")
            return False
    except connector.Error as e:
        logger.error(f"The error '{e}' occurred. Check login and password")
        return False
    return connection


def execute_query(connection, query):
    """Execute query on Database"""

    logger.debug(f"Query to DB: {query}")
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.debug("Query executed successfully in")
    except connector.Error as e:
        logger.error(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    """Read query on Database"""

    logger.debug(f"Query to DB: {query}")
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        logger.debug(f"Query to DB result: {result}")
        return result
    except connector.Error as e:
        logger.error(f"The error '{e}' occurred. Query to DB result: {result}")
        return result


def lost_conetion(type, ser_number):
    """logs devices who doesnt connect"""
    pass


def context_insert(
        type, ser_number, latitude, longitude, place,
        average_speed, transits, date, status, connection):
    logger.debug(
        f"Insert day information for: {type}, {ser_number}, "
        f"{latitude}, {longitude}, {place}, {average_speed}, "
        f"{transits}, {date}, {status}"
    )
    query_check = (
        f"SELECT id "
        f"FROM day_information "
        f"WHERE ser_number = '{ser_number}' AND type = '{type}'"
    )
    existing_row = execute_read_query(connection, query_check)
    if existing_row is None or existing_row == []:
        query_insert = (
            f"INSERT INTO day_information "
            f"(type, ser_number, latitude, longitude, place, average_speed, "
            f"transits, date, status) "
            f"VALUES ("
            f"'{type}', '{ser_number}', '{latitude}', '{longitude}', "
            f"'{place}', {average_speed}, {transits}, '{date}', '{status}')"
        )
        execute_query(connection, query_insert)
    else:
        logger.debug(f"device is be {type}, {ser_number}")
        query_insert = (
            f"UPDATE day_information "
            f"SET status = '{status}', average_speed = {average_speed}, "
            f"transits = {transits}, date = '{date}' "
            f"WHERE ser_number = '{ser_number}' AND type = '{type}'"
        )
        execute_query(connection, query_insert)


def main_quertes(id, con_loc):

    query_device_data = (
        f"SELECT d.id, d.ip_address, d.type, d.ser_number, d.latitude, "
        f"d.longitude, d.place, d.login, d.pass, s.base, s.table_name, "
        f"s.column_speed, s.column_date "
        f"FROM device AS d "
        f"JOIN device_db_strucure AS s "
        f"ON s.type = d.type "
        f"WHERE d.id > {id} "
        f"ORDER BY d.id "
        f"LIMIT 1"
    )

    device = execute_read_query(con_loc, query_device_data)
    if device == [] or device is None:
        logger.debug(f"Device with id = {id} is last")
        return []
    connection_remote = create_connection(
        device[1], device[7], device[8], device[9]
    )
    logger.debug(f"id is {device[0]}")
    if connection_remote:
        query_avd_speed = (
            f"SELECT ROUND(AVG({device[11]}), 2) "
            f"FROM {device[10]} "
            f"WHERE {device[11]} > 0 AND {device[12]} LIKE '{yesterday}%' "
        )
        day_avg_speed = execute_read_query(connection_remote, query_avd_speed)
        if day_avg_speed is None or day_avg_speed == []:
            logger.error(f"Not correct answer from DB device id: {device[0]}")
            db_answer_error.append(device[0])
        else:
            query_transits = (
                f"SELECT COUNT(id) AS COUNT "
                f"FROM {device[10]} "
                f"WHERE {device[12]} LIKE '{yesterday}%' "
            )
            transits = execute_read_query(connection_remote, query_transits)
            if transits is None or transits == []:
                logger.error(
                    f"Not correct 2-nd answer "
                    f"from DB device id: {device[0]}"
                )
                db_answer_error.append(device[0])
            else:
                context_insert(
                    *device[2:7], day_avg_speed[0], transits[0], yesterday,
                    'Test', con_loc
                )
    else:
        not_connet_id.append(device[0])  # add ip логин и пароль в лог
        lost_conetion(*device[2:4])
    return device[0]


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        filename='./logs/main.log',
        filemode='w',
        format='%(asctime)s, %(levelname)s, %(message)s, %(funcName)s'
    )
    logger = logging.getLogger(__name__)
    load_dotenv()
    host_ip = os.getenv('host_ip_test')
    user = os.getenv('user_test')
    password = os.getenv('password_test')
    db_name = os.getenv('db_name_test')
    today = date.today()   # 86400 sec on 1 day
    last_day = today - timedelta(days=1)
    yesterday = last_day.strftime("%Y_%m_%d")
    logger.debug(f'Start app! Take data on date: {yesterday}')
    not_connet_id = []
    db_answer_error = []

    connection_loc = create_connection(host_ip, user, password, db_name)
    id_i = 0  # 122 158
    job = 1

    while job != []:
        job = main_quertes(id_i, connection_loc)
        if job != [] or job is not None:
            id_i = job
        else:
            break
    logger.error(f"Not connect device id: \n{db_answer_error}")
    logger.error(f"Not correct answer from DB device id: \n{not_connet_id}")
