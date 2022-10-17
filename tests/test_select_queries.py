import datetime
from decimal import Decimal

from util.connector_util import ConnectorUtil


class TestSelectQueries:

    def test_should_select_all_from_category(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT * FROM Category;')

        assert data[0] == (1, 'Beverages', b'Soft drinks, coffees, teas, beers, and ales', None)
        assert data[3] == (4, 'Dairy Products', b'Cheeses', None)
        assert data[7] == (8, 'Seafood', b'Seaweed and fish', None)

    def test_should_select_contact_name_from_customer(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT contactName FROM Customer;')

        assert data[0] == ('Allen, Michael',)
        assert data[45] == ('Dressler, Marlies',)
        assert data[90] == ('Conn, Steve',)

    def test_should_select_id_firstname_lastname_employee(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT employeeId, firstName, lastName FROM Employee LIMIT 3;')

        assert data[0] == (1, 'Sara', 'Davis')
        assert data[1] == (2, 'Don', 'Funk')
        assert data[2] == (3, 'Judy', 'Lew')

    def test_should_select_product_name_by_product_id(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT productName FROM Product WHERE productId = 5;')

        assert data[0][0] == 'Product EPEIM'

    def test_should_select_sales_orders_where_freight_above_200_and_shipper_id_is_3(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT * FROM SalesOrder WHERE freight > 800 AND shipperId = 3;')

        assert data[0] == (10540, 63, 3, datetime.datetime(2007, 5, 19, 0, 0), datetime.datetime(2007, 6, 16, 0, 0),
                           datetime.datetime(2007, 6, 13, 0, 0), 3, Decimal('1007.64'), 'Ship to 63-C',
                           'Taucherstraße 3456', 'Cunewalde', None, '10281', 'Germany')
