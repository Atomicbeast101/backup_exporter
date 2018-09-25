from prometheus_client import start_http_server, Gauge
from datetime import date, timedelta, datetime
import time
import os

# Variables
MARIADB_PATH = '/backup/mariadb_backup/'
MONGODB_PATH = '/backup/mongodb_backup/'
CLOUD_PATH = '/backup/cloud_backup/'
DOCKER_PATH = '/backup/docker_backup/'
PORT = 9101
TIME_INTERVAL = 300

# Code
mariadb_s = Gauge('mariadb_backup', 'MariaDB Backup Status')
mongodb_s = Gauge('mongodb_backup', 'MongoDB Backup Status')
cloud_s = Gauge('cloud_backup', 'Cloud Backup Status')
docker_s = Gauge('docker_backup', 'Docker Backup Status')

def verify_dates(_path):
    date_list = list()
    for file_name in os.listdir(_path):
        str_date = file_name.split('.')[0]
        date_list.append(datetime.strptime(str_date, '%m-%d-%Y'))
    date_list.sort()
    first_date = date_list[0]
    last_date = datetime.today()
    date_set = set(date_list[0] + timedelta(x) for x in range((last_date - first_date).days))
    return sorted(date_set - set(date_list))

def mariadb():
    try:
        missing = verify_dates(MARIADB_PATH)
        if len(missing) > 0:
            mariadb_s.set(1)
        else:
            mariadb_s.set(2)
    except:
        mariadb_s.set(0)

def mongodb():
    try:
        missing = verify_dates(MONGODB_PATH)
        if len(missing) > 0:
            mongodb_s.set(1)
        else:
            mongodb_s.set(2)
    except:
        mongodb_s.set(0)

def cloud():
    try:
        missing = verify_dates(CLOUD_PATH)
        if len(missing) > 0:
            cloud_s.set(1)
        else:
            cloud_s.set(2)
    except:
        cloud_s.set(0)

def docker():
    try:
        missing = verify_dates(DOCKER_PATH)
        if len(missing) > 0:
            docker_s.set(1)
        else:
            docker_s.set(2)
    except:
        docker_s.set(0)

if __name__ == '__main__':
    start_http_server(PORT)
    while True:
        mariadb()
        mongodb()
        cloud()
        docker()
        time.sleep(TIME_INTERVAL)