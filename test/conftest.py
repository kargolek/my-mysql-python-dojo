import pytest
from mysql import connector

from test.util.secrets import Secrets


@pytest.fixture(scope='class')
def msql_connector():
    conn = connector.connect(host='127.0.0.1',
                             port=3306,
                             database='Northwind',
                             user=Secrets.MYSQL_USER,
                             password=Secrets.MYSQL_PASSWORD)
    yield conn
    conn.close()


@pytest.fixture(scope='class')
def cursor(msql_connector):
    cursor = msql_connector.cursor()
    yield cursor
    cursor.close()
