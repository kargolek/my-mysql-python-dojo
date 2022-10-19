import datetime
from decimal import Decimal

from util.connector_util import ConnectorUtil


class TestSelectQueries:

    # MySQL SELECT Statement
    def test_should_select_all_from_category(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT * FROM Category;')

        assert data[0] == (1, 'Beverages', b'Soft drinks, coffees, teas, beers, and ales', None)
        assert data[3] == (4, 'Dairy Products', b'Cheeses', None)
        assert data[7] == (8, 'Seafood', b'Seaweed and fish', None)

    # MySQL SELECT Statement single column
    def test_should_select_contact_name_from_customer(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT contactName FROM Customer;')

        assert data[0] == ('Allen, Michael',)
        assert data[45] == ('Dressler, Marlies',)
        assert data[90] == ('Conn, Steve',)

    # MySQL SELECT Statement multiple columns
    def test_should_select_id_firstname_lastname_employee(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT employeeId, firstName, lastName FROM Employee '
                                                      'LIMIT 3;')

        assert data[0] == (1, 'Sara', 'Davis')
        assert data[1] == (2, 'Don', 'Funk')
        assert data[2] == (3, 'Judy', 'Lew')

    def test_should_select_distinctrow_and_concat_employee_name_surname_sales_order(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCTROW '
                                                      'CONCAT(Employee.firstname," ",Employee.lastname) AS empName '
                                                      'FROM SalesOrder '
                                                      'JOIN Employee '
                                                      'ON SalesOrder.employeeId = Employee.employeeId;')
        assert data[0][0] == 'Sven Buck'
        assert data[8][0] == 'Russell King'

    def test_should_select_distinct_country_customer(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCT Country FROM Customer;')

        assert data[0][0] == 'Germany'
        assert data[20][0] == 'Poland'

    def test_should_select_distinctrow_employee_name_surname_sales_order(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCTROW Employee.firstname, Employee.lastname '
                                                      'FROM SalesOrder '
                                                      'JOIN Employee '
                                                      'ON SalesOrder.employeeId = Employee.employeeId;')

        assert data[0] == ('Sven', 'Buck')
        assert data[8] == ('Russell', 'King')

    # MySQL WHERE Clause
    def test_should_select_product_name_by_product_id(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT productName FROM Product '
                                                      'WHERE productId = 5;')

        assert data[0][0] == 'Product EPEIM'

    # MySQL ORDER BY Keyword
    def test_should_select_order_detail_sorted_by_unit_price_desc_order_id_asc(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT * FROM OrderDetail '
                                                      'ORDER BY unitPrice DESC, orderId ASC '
                                                      'LIMIT 10;')

        assert data[0] == (714, 10518, 38, Decimal('263.50'), 15, Decimal('0.00'))

    # MySQL ORDER BY Keyword
    def test_should_select_order_detail_sorted_by_unit_price_desc_and_quantity_desc_order_id(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor,
                                              'SELECT * FROM OrderDetail '
                                              'ORDER BY unitPrice DESC, quantity DESC, orderId DESC '
                                              'LIMIT 20;')

        assert data[0] == (1894, 10981, 38, Decimal('263.50'), 60, Decimal('0.00'))
