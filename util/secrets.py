import os


class Secrets:
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')


