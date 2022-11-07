from decimal import Decimal

from test.util.connector_util import fetch_data_print


class TestGroupingData:

    # MySQL GROUP BY clause
    def test_should_select_employee_lastname_buck_from_sales_order(self, cursor):
        data = fetch_data_print(cursor, 'SELECT lastName, firstName FROM SalesOrder '
                                        'JOIN Employee '
                                        'Employee USING (employeeId) '
                                        'WHERE lastName = "Buck" '
                                        'GROUP BY employeeId;')

        assert data[0] == ('Buck', 'Sven')

    # MySQL GROUP BY clause
    def test_should_count_orders_and_group_by_the_year(self, cursor):
        data = fetch_data_print(cursor, 'SELECT YEAR(orderDate) as year, COUNT(*) as orders FROM SalesOrder '
                                        'GROUP BY year;')

        assert data[0] == (2006, 152)
        assert data[1] == (2007, 408)
        assert data[2] == (2008, 270)

    # MySQL GROUP BY clause
    def test_should_count_orders_freight_and_group_by_the_year(self, cursor):
        data = fetch_data_print(cursor, 'SELECT YEAR(orderDate) as year, SUM(freight) as freight FROM SalesOrder '
                                        'GROUP BY year;')

        assert data[0] == (2006, Decimal('10279.87'))
        assert data[2] == (2008, Decimal('22194.05'))

    # MySQL GROUP BY clause
    def test_should_count_shipped_sales_by_shipper_in_2006(self, cursor):
        data = fetch_data_print(cursor, 'SELECT companyName, COUNT(*) as shipped FROM SalesOrder '
                                        'JOIN Shipper '
                                        'Shipper USING (shipperId) '
                                        'WHERE YEAR(orderDate) = 2006 '
                                        'GROUP BY companyName '
                                        'ORDER BY shipped DESC;')

        assert data[0] == ('Shipper ZHISN', 58)
        assert data[2] == ('Shipper GVSUA', 38)

    # MySQL GROUP BY clause
    def test_should_count_shipped_sales_by_shipper_in_2007(self, cursor):
        data = fetch_data_print(cursor, 'SELECT companyName, COUNT(*) as shipped FROM SalesOrder '
                                        'JOIN Shipper '
                                        'Shipper USING (shipperId) '
                                        'WHERE YEAR(orderDate) = 2007 '
                                        'GROUP BY companyName '
                                        'ORDER BY shipped DESC;')

        assert data[0] == ('Shipper ETYNR', 153)
        assert data[2] == ('Shipper ZHISN', 122)

    # MySQL GROUP BY clause
    def test_should_count_shipped_sales_by_shipper_in_2008(self, cursor):
        data = fetch_data_print(cursor, 'SELECT companyName, COUNT(*) as shipped FROM SalesOrder '
                                        'JOIN Shipper '
                                        'Shipper USING (shipperId) '
                                        'WHERE YEAR(orderDate) = 2008 '
                                        'GROUP BY companyName '
                                        'ORDER BY shipped DESC;')

        assert data[0] == ('Shipper ETYNR', 117)
        assert data[2] == ('Shipper ZHISN', 75)

    # MySQL GROUP BY clause
    def test_should_count_shipped_sales_by_shipper_all_time(self, cursor):
        data = fetch_data_print(cursor, 'SELECT companyName, COUNT(*) as shipped FROM SalesOrder '
                                        'JOIN Shipper '
                                        'Shipper USING (shipperId) '
                                        'GROUP BY companyName '
                                        'ORDER BY shipped DESC;')

        assert data[0] == ('Shipper ETYNR', 326)
        assert data[2] == ('Shipper GVSUA', 249)

    # MySQL HAVING clause
    def test_should_count_shipped_sales_by_shipper_all_time_more_than_255_shipped(self, cursor):
        data = fetch_data_print(cursor, 'SELECT companyName, COUNT(*) as shipped FROM SalesOrder '
                                        'JOIN Shipper '
                                        'Shipper USING (shipperId) '
                                        'GROUP BY companyName '
                                        'HAVING shipped > 255;')

        assert data[0] == ('Shipper ETYNR', 326)

    # MySQL HAVING clause
    def test_should_count_avg_discount_per_product_name_having_more_than_10_percent_in_all_orders(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productName, AVG(discount) as discounts FROM OrderDetail '
                                        'JOIN Product '
                                        'Product USING (productId) '
                                        'GROUP BY productName '
                                        'HAVING discounts > 0.1 '
                                        'ORDER BY discounts DESC;')

        assert data[0] == ('Product MYNXN', Decimal('0.108333'))
        assert data[1] == ('Product RECZE', Decimal('0.102273'))
