import pytest
from mysql import connector

from test.util.connector_util import fetch_data_print
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


@pytest.fixture()
def create_total_sales_table(cursor):
    fetch_data_print(cursor, 'DROP TABLE IF EXISTS TotalSales;')
    fetch_data_print(cursor, 'CREATE TABLE TotalSales '
                             'SELECT productName, YEAR(orderDate) AS year, '
                             'COUNT(*) AS totalOrders, '
                             'SUM(OrderDetail.unitPrice * quantity) AS totalPrice FROM OrderDetail '
                             'INNER JOIN Product USING (productId) '
                             'INNER JOIN SalesOrder USING (orderId) '
                             'GROUP BY productName, year;')
    yield
    fetch_data_print(cursor, 'DROP TABLE IF EXISTS TotalSales;')
