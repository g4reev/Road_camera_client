import logging
import os
import platform
import subprocess
from datetime import date, timedelta

from dotenv import load_dotenv
from mysql import connector


class Device:

    def __init__(
            self,
            id: int = 0,
            type: str = 'type',
            ser_number: str = 'ser_number',
            latitude: str = 'latitude',
            longitude: str = ' longitude',
            place: str = 'place'):

        self.id = id
        self.type = type
        self.ser_number = ser_number
        self.latitude = latitude
        self.longitude = longitude
        self.place = place
        self.query = (
            f"SELECT d.id, d.ip_address, d.type, d.ser_number, d.latitude, "
            f"d.longitude, d.place, d.login, d.pass, s.base, s.table_name, "
            f"s.column_speed, s.column_date "
            f"FROM device AS d "
            f"JOIN device_db_strucure AS s "
            f"ON s.type = d.type "
            f"WHERE d.id > {self.id} "
            f"ORDER BY d.id "
            f"LIMIT 1"
        )

    def __call__(
            self,
            id: int = 0,
            type: str = 'type',
            ser_number: str = 'ser_number',
            latitude: str = 'latitude',
            longitude: str = ' longitude',
            place: str = 'place'):

        self.id = id
        self.type = type
        self.ser_number = ser_number
        self.latitude = latitude
        self.longitude = longitude
        self.place = place
        self.query = (
            f"SELECT d.id, d.ip_address, d.type, d.ser_number, d.latitude, "
            f"d.longitude, d.place, d.login, d.pass, s.base, s.table_name, "
            f"s.column_speed, s.column_date "
            f"FROM device AS d "
            f"JOIN device_db_strucure AS s "
            f"ON s.type = d.type "
            f"WHERE d.id > {self.id} "
            f"ORDER BY d.id "
            f"LIMIT 1"
        )

    def __str__(self) -> str:
        return (
            f'{self.id=}, {self.type=}, {self.ser_number=}, {self.latitude=},'
            f'{self.longitude=}, {self.place=}, {self.query=}'
        )


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


def execute_read_query(connection, query, detail: bool = False):
    """Read query on Database"""

    logger.debug(f"DB {query=}")
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        if detail:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        logger.debug(f"Query to DB {result=}")
        return result
    except connector.Error as e:
        logger.error(f"The error '{e}' occurred. Query to DB result: {result}")
        return result


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        filename='./logs/main.log',
        filemode='w',
        format='%(asctime)s, %(levelname)s, %(message)s, %(funcName)s'
    )
    logger = logging.getLogger(__name__)
    load_dotenv()
    last_day = date.today() - timedelta(days=1)
    yesterday = last_day.strftime("%Y_%m_%d")
    logger.debug(f'Start app! Take data on date: {yesterday}')

    connection_loc = create_connection(
        os.getenv('host_ip_test'),
        os.getenv('user_test'),
        os.getenv('password_test'),
        os.getenv('db_name_test')
    )
    # 122 158
    dev = Device(id=0)
    device = 1
    while device is not None:
        logger.debug(dev)
        print(dev)
        device = execute_read_query(connection_loc, dev.query)
        if device is None:
            logger.debug('Devices ran out!')
            break
        dev(device[0], *device[2:7])
        connection_remote = create_connection(device[1], *device[7:10])
        if connection_remote:
            query_info = (
                f"SELECT C1.avgspeed, C2.cnt "
                f"FROM "
                f"(SELECT ROUND(AVG({device[11]}), 2) AS avgspeed "
                f"FROM {device[10]} "
                f"WHERE {device[11]} > 0 AND "
                f"{device[12]} LIKE '{yesterday}%') C1, "
                f"(SELECT COUNT(id) AS cnt "
                f"FROM {device[10]} "
                f"WHERE {device[12]} LIKE '{yesterday}%') C2 "
            )
            day_info = execute_read_query(connection_remote, query_info)
            query_insert = (
                f"INSERT INTO day_information "
                f"(type, ser_number, latitude, longitude, place, average_speed, "
                f"transits, date, status) "
                f"VALUES ("
                f"'{dev.type}', '{dev.ser_number}', "
                f"'{dev.latitude}', '{dev.longitude}', "
                f"'{dev.place}', {day_info[0]}, {day_info[1]}, "
                f"'{yesterday}', 'Created')"
                f"ON DUPLICATE KEY UPDATE "
                f"status = 'Updated', average_speed = {day_info[0]}, "
                f"transits = {day_info[1]}, date = '{yesterday}' "
            )
            execute_query(connection_loc, query_insert)
