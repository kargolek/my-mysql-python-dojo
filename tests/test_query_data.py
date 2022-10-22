import datetime
from decimal import Decimal

from util.connector_util import fetch_data_print


class TestQueryData:

    # MySQL SELECT Statement
    def test_should_select_all_from_category(self, cursor):
        data = fetch_data_print(cursor, 'SELECT * FROM Category;')

        assert data[0] == (1, 'Beverages', b'Soft drinks, coffees, teas, beers, and ales', None)
        assert data[3] == (4, 'Dairy Products', b'Cheeses', None)
        assert data[7] == (8, 'Seafood', b'Seaweed and fish', None)

    # MySQL SELECT Statement single column
    def test_should_select_contact_name_from_customer(self, cursor):
        data = fetch_data_print(cursor, 'SELECT contactName FROM Customer;')

        assert data[0] == ('Allen, Michael',)
        assert data[45] == ('Dressler, Marlies',)
        assert data[90] == ('Conn, Steve',)

    # MySQL SELECT Statement multiple columns
    def test_should_select_id_firstname_lastname_employee(self, cursor):
        data = fetch_data_print(cursor, 'SELECT employeeId, firstName, lastName FROM Employee '
                                        'LIMIT 3;')

        assert data[0] == (1, 'Sara', 'Davis')
        assert data[1] == (2, 'Don', 'Funk')
        assert data[2] == (3, 'Judy', 'Lew')
