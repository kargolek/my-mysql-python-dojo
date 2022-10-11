import pytest
from mysql import connector
from util.secrets import Secrets


class TestSelectQueries:

    @pytest.fixture(scope='class')
    def init_msql_connector(self):
        conn = connector.connect(host='127.0.0.1',
                                 port=3306,
                                 database='Northwind',
                                 user=Secrets.MYSQL_USER,
                                 password=Secrets.MYSQL_PASSWORD)
        yield conn
        conn.close()

    @pytest.fixture(scope='class')
    def cursor(self, init_msql_connector):
        cursor = init_msql_connector.cursor()
        yield cursor
        cursor.close()

    def test_should_select_contact_name_from_customer(self, cursor):
        cursor.execute('SELECT contactName FROM Customer;')
        assert cursor.fetchall()[0] == ('Allen, Michael',)

    def test_should_select_all_from_category(self, cursor):
        cursor.execute('SELECT * FROM Category;')
        assert cursor.fetchall()[0] == (1, 'Beverages', b'Soft drinks, coffees, teas, beers, and ales', None)
