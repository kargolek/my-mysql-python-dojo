import datetime
from decimal import Decimal

from test.util.connector_util import fetch_data_print


class TestSortingData:

    # MySQL ORDER BY DESC AND ASC
    def test_should_select_order_detail_sorted_by_unit_price_desc_order_id_asc(self, cursor):
        data = fetch_data_print(cursor, 'SELECT * FROM OrderDetail '
                                        'ORDER BY unitPrice DESC, orderId ASC '
                                        'LIMIT 10;')

        assert data[0] == (714, 10518, 38, Decimal('263.50'), 15, Decimal('0.00'))

    # MySQL ORDER BY DESC
    def test_should_select_order_detail_sorted_by_unit_price_desc_and_quantity_desc_order_id(self, cursor):
        data = fetch_data_print(cursor,
                                'SELECT * FROM OrderDetail '
                                'ORDER BY unitPrice DESC, quantity DESC, orderId DESC '
                                'LIMIT 20;')

        assert data[0] == (1894, 10981, 38, Decimal('263.50'), 60, Decimal('0.00'))

    # MySQL ORDER BY DESC ASC
    def test_should_select_employee_name_lastname_and_order_lastname_by_asc(self, cursor):
        data = fetch_data_print(cursor, 'SELECT CONCAT(lastname, " ", firstname) AS employeeName '
                                        'FROM Employee '
                                        'ORDER BY lastname ASC;')

        assert data[0][0] == 'Buck Sven'

    # MySQL ORDER BY DESC
    def test_should_select_the_youngest_employee(self, cursor):
        data = fetch_data_print(cursor,
                                'SELECT CONCAT(lastname, " ", firstname) AS employeeName, birthDate '
                                'FROM Employee '
                                'ORDER BY birthDate DESC;')

        assert data[0][0] == 'Dolgopyatova Zoya'
        assert data[0][1] == datetime.datetime(1976, 1, 27, 0, 0)
