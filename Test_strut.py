
from datetime import date, datetime, timedelta
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    result = False
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '4', host]
    result = subprocess.call(command) == 0
    return result


if ping('10.133.14.149'):
                print ("Sexy it")


today = date.today()   # 86400 sec on 1 day
last_day = today - timedelta(days=1)
yesterday = last_day.strftime("%Y_%m_%d")
print(f'Вчера это: {yesterday}')

log_file = open(f"./logs/{yesterday}_test.log", "w+")

def logs_insert(context, filename):

    now = datetime.now()    
    insert_log = f"{now}: {context}\n"
    print(insert_log)
    filename.write(insert_log)

logs_insert(f"Connection to MySQL DB  successful", log_file)

logs_insert(f"Connection2 to MySQL DB successful", log_file)


(105, '10.133.10.149', 'krechet-sm', '1709001', '55.9799', '54.7342', ' г. Уфа, Ул., Айская, 81. э\\о №23', 'prometheus', '215ee55dc14a9f78c2e15aabf6ec93fd', 'main', 'events', 'target_speed', 'time')

# new_flag = map()